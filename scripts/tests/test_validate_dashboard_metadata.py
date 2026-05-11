import importlib.util
import sys
from pathlib import Path
from typing import Any


def load_module() -> Any:
    module_path = Path(__file__).resolve().parents[1] / "validate-dashboard-metadata.py"
    spec = importlib.util.spec_from_file_location("validate_dashboard_metadata", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_post(
    blog_dir: Path,
    filename: str = "day-001-us-ev-sales-trend.md",
    *,
    day: int = 1,
    slug: str = "day-001-us-ev-sales-trend",
    status: str = "draft",
    data_source_url: str = "https://example.com",
    hero_image: str | None = "/media/day-001-us-ev-sales-trend/preview.png",
) -> Path:
    blog_dir.mkdir(parents=True, exist_ok=True)
    post = blog_dir / filename
    hero_image_field = f'heroImage: "{hero_image}"\n' if hero_image is not None else ""
    post.write_text(
        f"""---
title: "Day 001: US EV Sales Trend"
description: "A dashboard exploring US EV sales."
pubDate: "2026-05-02"
day: {day}
dashboardSlug: "{slug}"
status: "{status}"
tags:
  - dashboard
dataSources:
  - name: "Example"
    url: "{data_source_url}"
{hero_image_field}---
Body
""",
        encoding="utf-8",
    )
    return post


def write_dashboard(dashboards_dir: Path, folder: str = "day-001-us-ev-sales-trend") -> Path:
    dashboard_dir = dashboards_dir / folder
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    dashboard_dir.joinpath("metadata.yml").write_text(
        """day: 1
title: "US EV Sales Trend"
slug: "us-ev-sales-trend"
date: "2026-05-02"
status: "draft"
summary: "A dashboard exploring US EV sales."
data_sources:
  - name: "Example"
    url: "https://example.com"
    license: "Public"
tools:
  - Python
  - Astro
outputs:
  - type: screenshot
    path: outputs/images/preview.png
  - type: interactive
    path: outputs/html/index.html
""",
        encoding="utf-8",
    )
    return dashboard_dir


def test_parse_frontmatter_reads_nested_data_sources(tmp_path: Path) -> None:
    module = load_module()
    post = write_post(tmp_path)

    fields = module.parse_frontmatter(post)

    assert fields["day"] == 1
    assert fields["tags"] == ["dashboard"]
    assert fields["dataSources"] == [{"name": "Example", "url": "https://example.com"}]


def test_validate_repository_accepts_valid_metadata(tmp_path: Path) -> None:
    module = load_module()
    blog_dir = tmp_path / "web" / "src" / "content" / "blog"
    dashboards_dir = tmp_path / "dashboards"
    media_dir = tmp_path / "web" / "public" / "media" / "day-001-us-ev-sales-trend"
    media_dir.mkdir(parents=True)
    media_dir.joinpath("preview.png").write_text("placeholder", encoding="utf-8")
    write_post(blog_dir)
    write_dashboard(dashboards_dir)

    errors = module.validate_repository(
        module.load_posts(blog_dir),
        module.load_dashboards(dashboards_dir),
        tmp_path,
        dashboards_dir,
    )

    assert errors == []


def test_validate_repository_reports_duplicate_days_and_slugs(tmp_path: Path) -> None:
    module = load_module()
    blog_dir = tmp_path / "web" / "src" / "content" / "blog"
    dashboards_dir = tmp_path / "dashboards"
    media_dir = tmp_path / "web" / "public" / "media" / "day-001-us-ev-sales-trend"
    media_dir.mkdir(parents=True)
    media_dir.joinpath("preview.png").write_text("placeholder", encoding="utf-8")
    write_post(blog_dir, "one.md")
    write_post(blog_dir, "two.md")
    write_dashboard(dashboards_dir)

    errors = module.validate_repository(
        module.load_posts(blog_dir),
        module.load_dashboards(dashboards_dir),
        tmp_path,
        dashboards_dir,
    )

    assert any("duplicate day 1" in error for error in errors)
    assert any("duplicate slug day-001-us-ev-sales-trend" in error for error in errors)


def test_validate_repository_allows_repeated_none_dashboard_slug(tmp_path: Path) -> None:
    module = load_module()
    blog_dir = tmp_path / "web" / "src" / "content" / "blog"
    dashboards_dir = tmp_path / "dashboards"
    write_post(blog_dir, "day-008-operations.md", day=8, slug="none", hero_image=None)
    write_post(blog_dir, "day-009-operations.md", day=9, slug="none", hero_image=None)

    errors = module.validate_repository(
        module.load_posts(blog_dir),
        module.load_dashboards(dashboards_dir),
        tmp_path,
        dashboards_dir,
    )

    assert errors == []


def test_validate_repository_reports_invalid_blog_metadata(tmp_path: Path) -> None:
    module = load_module()
    blog_dir = tmp_path / "web" / "src" / "content" / "blog"
    dashboards_dir = tmp_path / "dashboards"
    write_post(
        blog_dir,
        day=2,
        status="ready",
        data_source_url="not-a-url",
        hero_image="/media/day-001-us-ev-sales-trend/missing.png",
    )
    write_dashboard(dashboards_dir)

    errors = module.validate_repository(
        module.load_posts(blog_dir),
        module.load_dashboards(dashboards_dir),
        tmp_path,
        dashboards_dir,
    )

    assert any("invalid status 'ready'" in error for error in errors)
    assert any("dataSources[0].url must be a valid URL" in error for error in errors)
    assert any("day 2 does not match dashboardSlug day 1" in error for error in errors)
    assert any("missing heroImage media" in error for error in errors)


def test_validate_dashboards_reports_invalid_dashboard_metadata(tmp_path: Path) -> None:
    module = load_module()
    dashboard_dir = tmp_path / "dashboards" / "day-001-us-ev-sales-trend"
    dashboard_dir.mkdir(parents=True)
    dashboard_dir.joinpath("metadata.yml").write_text(
        """day: 2
title: ""
slug: "wrong"
date: "2026-05-02"
status: "ready"
summary: "Bad metadata"
data_sources:
  - name: ""
    url: "not-a-url"
tools: []
outputs:
  - type: ""
    path: ""
""",
        encoding="utf-8",
    )

    errors = module.validate_dashboards(module.load_dashboards(tmp_path / "dashboards"))

    assert any("day 2 does not match folder day 1" in error for error in errors)
    assert any(
        "slug 'wrong' does not match folder slug 'us-ev-sales-trend'" in error for error in errors
    )
    assert any("invalid status 'ready'" in error for error in errors)
    assert any("data_sources[0].url must be a valid URL" in error for error in errors)
    assert any("outputs[0].path must be a non-empty string" in error for error in errors)


def test_validate_repository_reports_missing_dashboard_metadata_and_blog_post(
    tmp_path: Path,
) -> None:
    module = load_module()
    dashboards_dir = tmp_path / "dashboards"
    (dashboards_dir / "day-001-us-ev-sales-trend").mkdir(parents=True)

    errors = module.validate_repository(
        [],
        module.load_dashboards(dashboards_dir),
        tmp_path,
        dashboards_dir,
    )

    assert any("missing metadata.yml" in error for error in errors)
    assert any("missing matching blog post" in error for error in errors)


def test_validate_url_accepts_https_and_rejects_relative() -> None:
    module = load_module()

    assert module.validate_url("https://example.com")
    assert not module.validate_url("/relative")
