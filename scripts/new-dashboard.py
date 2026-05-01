from __future__ import annotations

import argparse
import re
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Reporter = Callable[[str], None]


@dataclass(frozen=True)
class DashboardPaths:
    folder_name: str
    dashboard_dir: Path
    blog_post: Path
    media_dir: Path


class DashboardExistsError(RuntimeError):
    pass


class DashboardCreationError(RuntimeError):
    pass


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "dashboard"


def build_paths(day: int, title: str) -> DashboardPaths:
    slug = slugify(title)
    folder_name = f"day-{day:03d}-{slug}"
    return DashboardPaths(
        folder_name=folder_name,
        dashboard_dir=ROOT / "dashboards" / folder_name,
        blog_post=ROOT / "web" / "src" / "content" / "blog" / f"{folder_name}.md",
        media_dir=ROOT / "web" / "public" / "media" / folder_name,
    )


def ensure_available(paths: DashboardPaths) -> None:
    existing = [
        path for path in (paths.dashboard_dir, paths.blog_post, paths.media_dir) if path.exists()
    ]
    if existing:
        joined = "\n".join(str(path.relative_to(ROOT)) for path in existing)
        raise DashboardExistsError(f"Refusing to overwrite existing paths:\n{joined}")


def create_directory(path: Path, reporter: Reporter, *, exist_ok: bool = False) -> None:
    existed_before = path.exists()
    try:
        path.mkdir(parents=True, exist_ok=exist_ok)
    except FileExistsError as exc:
        raise DashboardExistsError(f"Directory already exists: {path.relative_to(ROOT)}") from exc
    except OSError as exc:
        message = f"Could not create directory {path.relative_to(ROOT)}: {exc}"
        raise DashboardCreationError(message) from exc
    action = "Using existing directory" if exist_ok and existed_before else "Created directory"
    reporter(f"{action}: {path.relative_to(ROOT)}")


def write_file(path: Path, content: str, reporter: Reporter) -> None:
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        message = f"Could not write file {path.relative_to(ROOT)}: {exc}"
        raise DashboardCreationError(message) from exc
    reporter(f"Created file: {path.relative_to(ROOT)}")


def create_dashboard(
    day: int,
    title: str,
    today: date | None = None,
    reporter: Reporter = print,
) -> DashboardPaths:
    today = today or date.today()
    paths = build_paths(day, title)
    ensure_available(paths)

    for directory in [
        paths.dashboard_dir / "src",
        paths.dashboard_dir / "tests",
        paths.dashboard_dir / "data" / "raw",
        paths.dashboard_dir / "data" / "processed",
        paths.dashboard_dir / "outputs" / "images",
        paths.dashboard_dir / "outputs" / "html",
        paths.dashboard_dir / "outputs" / "video",
        paths.media_dir,
    ]:
        create_directory(directory, reporter)

    create_directory(paths.blog_post.parent, reporter, exist_ok=True)

    for gitkeep in [
        paths.dashboard_dir / "data" / "raw" / ".gitkeep",
        paths.dashboard_dir / "data" / "processed" / ".gitkeep",
        paths.dashboard_dir / "outputs" / "images" / ".gitkeep",
        paths.dashboard_dir / "outputs" / "html" / ".gitkeep",
        paths.dashboard_dir / "outputs" / "video" / ".gitkeep",
        paths.media_dir / ".gitkeep",
    ]:
        write_file(gitkeep, "", reporter)

    write_file(
        paths.dashboard_dir / "metadata.yml",
        dashboard_metadata(day, title, paths.folder_name, today),
        reporter,
    )
    write_file(
        paths.dashboard_dir / "README.md",
        dashboard_readme(day, title, paths.folder_name),
        reporter,
    )
    write_file(paths.dashboard_dir / "src" / "main.py", dashboard_main(title), reporter)
    write_file(paths.dashboard_dir / "tests" / "test_main.py", dashboard_test(), reporter)
    write_file(paths.blog_post, blog_post(day, title, paths.folder_name, today), reporter)

    return paths


def dashboard_metadata(day: int, title: str, folder_name: str, pub_date: date) -> str:
    slug = folder_name.removeprefix(f"day-{day:03d}-")
    return f"""day: {day}
title: "{title}"
slug: "{slug}"
date: "{pub_date.isoformat()}"
status: "draft"
summary: "A dashboard exploring {title}."
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
"""


def dashboard_readme(day: int, title: str, folder_name: str) -> str:
    return f"""# Day {day:03d}: {title}

## Summary

Briefly explain the dashboard and why it exists.

## Question

What question does this dashboard answer?

## Data Sources

| Source | URL | License/Terms | Notes |
|---|---|---|---|
| Example | https://example.com | Public | Public dataset |

## Method

Explain the data ingestion, transformation, and visualization approach.

## Outputs

- Screenshot: `outputs/images/preview.png`
- Interactive dashboard: `outputs/html/index.html`
- Blog post: `../../web/src/content/blog/{folder_name}.md`

## Run Locally

```bash
uv run python dashboards/{folder_name}/src/main.py
```

## Quality Checks

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest --cov
uv run bandit -r .
uv run detect-secrets scan
```

## Assumptions

Document assumptions.

## Limitations

Document limitations.

## Future Improvements

Document what could be improved later.
"""


def dashboard_main(title: str) -> str:
    return f"""from pathlib import Path


def main() -> None:
    output_dir = Path(__file__).resolve().parents[1] / "outputs" / "html"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir.joinpath("index.html").write_text("<h1>{title}</h1>\\n")


if __name__ == "__main__":
    main()
"""


def dashboard_test() -> str:
    return """def test_placeholder() -> None:
    assert True
"""


def blog_post(day: int, title: str, folder_name: str, pub_date: date) -> str:
    return f"""---
title: "Day {day:03d}: {title}"
description: "A dashboard exploring {title}."
pubDate: "{pub_date.isoformat()}"
day: {day}
dashboardSlug: "{folder_name}"
status: "draft"
tags:
  - dashboard
  - python
  - data-visualization
dataSources: []
heroImage: "/media/{folder_name}/preview.png"
---

Write the dashboard story here.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new daily dashboard.")
    parser.add_argument("--day", type=int, required=True)
    parser.add_argument("--title", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        paths = create_dashboard(args.day, args.title)
    except DashboardExistsError as exc:
        print(f"Dashboard was not created: {exc}")
        raise SystemExit(1) from exc
    except DashboardCreationError as exc:
        print(f"Dashboard creation failed: {exc}")
        raise SystemExit(1) from exc

    print("Created dashboard:")
    print(f"- {paths.dashboard_dir.relative_to(ROOT)}")
    print(f"- {paths.blog_post.relative_to(ROOT)}")
    print(f"- {paths.media_dir.relative_to(ROOT)}")
    print("")
    print("Next steps:")
    print(f"uv run python dashboards/{paths.folder_name}/src/main.py")
    print("uv run python scripts/validate-dashboard-metadata.py")


if __name__ == "__main__":
    main()
