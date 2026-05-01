import importlib.util
import sys
from datetime import date
from pathlib import Path
from types import ModuleType


def load_module() -> ModuleType:
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
