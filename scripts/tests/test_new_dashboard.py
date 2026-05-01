import importlib.util
import sys
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from pytest_mock import MockerFixture


def load_module() -> Any:
    module_path = Path(__file__).resolve().parents[1] / "new-dashboard.py"
    spec = importlib.util.spec_from_file_location("new_dashboard", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_slugify_removes_punctuation() -> None:
    module = load_module()

    assert module.slugify("US EV Sales Trend!") == "us-ev-sales-trend"
    assert module.slugify("!!!") == "dashboard"


def test_blog_post_uses_canonical_slug() -> None:
    module = load_module()

    content = module.blog_post(
        1,
        "US EV Sales Trend",
        "day-001-us-ev-sales-trend",
        date(2026, 5, 2),
    )

    assert 'dashboardSlug: "day-001-us-ev-sales-trend"' in content
    assert 'pubDate: "2026-05-02"' in content


def test_create_dashboard_writes_expected_files(tmp_path: Path) -> None:
    module = load_module()
    module.ROOT = tmp_path
    created: list[str] = []

    paths = module.create_dashboard(
        1,
        "US EV Sales Trend",
        date(2026, 5, 2),
        reporter=created.append,
    )

    assert paths.folder_name == "day-001-us-ev-sales-trend"
    assert (paths.dashboard_dir / "README.md").exists()
    assert (paths.dashboard_dir / "metadata.yml").exists()
    assert (paths.dashboard_dir / "src" / "main.py").exists()
    assert (paths.dashboard_dir / "tests" / "test_main.py").exists()
    assert (paths.dashboard_dir / "data" / "raw" / ".gitkeep").exists()
    assert (paths.dashboard_dir / "outputs" / "html" / ".gitkeep").exists()
    assert paths.blog_post.exists()
    assert (paths.media_dir / ".gitkeep").exists()
    normalized = [message.replace("\\", "/") for message in created]
    assert "Created directory: dashboards/day-001-us-ev-sales-trend/src" in normalized
    assert "Created file: dashboards/day-001-us-ev-sales-trend/metadata.yml" in normalized


def test_create_dashboard_existing_directory_is_graceful(tmp_path: Path) -> None:
    module = load_module()
    module.ROOT = tmp_path
    existing = tmp_path / "dashboards" / "day-001-us-ev-sales-trend"
    existing.mkdir(parents=True)

    with pytest.raises(module.DashboardExistsError, match="Refusing to overwrite"):
        module.create_dashboard(1, "US EV Sales Trend", date(2026, 5, 2), reporter=lambda _: None)


def test_create_directory_wraps_os_error(tmp_path: Path, mocker: MockerFixture) -> None:
    module = load_module()
    module.ROOT = tmp_path
    mocker.patch.object(module.Path, "mkdir", side_effect=OSError("disk full"))

    with pytest.raises(module.DashboardCreationError, match="Could not create directory"):
        module.create_directory(tmp_path / "dashboards", lambda _: None)


def test_write_file_wraps_os_error(tmp_path: Path, mocker: MockerFixture) -> None:
    module = load_module()
    module.ROOT = tmp_path
    mocker.patch.object(module.Path, "write_text", side_effect=OSError("readonly"))

    with pytest.raises(module.DashboardCreationError, match="Could not write file"):
        module.write_file(tmp_path / "README.md", "content", lambda _: None)


def test_main_reports_existing_dashboard_without_traceback(
    tmp_path: Path,
    mocker: MockerFixture,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module = load_module()
    module.ROOT = tmp_path
    mocker.patch.object(
        module,
        "parse_args",
        return_value=type("Args", (), {"day": 1, "title": "US EV Sales Trend"})(),
    )
    mocker.patch.object(
        module,
        "create_dashboard",
        side_effect=module.DashboardExistsError("already exists"),
    )

    with pytest.raises(SystemExit) as exc_info:
        module.main()

    assert exc_info.value.code == 1
    assert "Dashboard was not created: already exists" in capsys.readouterr().out
