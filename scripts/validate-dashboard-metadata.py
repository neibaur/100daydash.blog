from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "web" / "src" / "content" / "blog"
DASHBOARDS_DIR = ROOT / "dashboards"
VALID_STATUSES = {"draft", "published", "archived"}
REQUIRED_FIELDS = {
    "title",
    "description",
    "pubDate",
    "day",
    "dashboardSlug",
    "status",
    "tags",
    "dataSources",
}


@dataclass(frozen=True)
class BlogMetadata:
    path: Path
    fields: dict[str, object]


def parse_scalar(value: str) -> object:
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    return value


def parse_frontmatter(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing frontmatter")

    fields: dict[str, object] = {}
    index = 1
    while index < len(lines):
        line = lines[index]
        if line == "---":
            return fields
        if not line.strip() or line.startswith("  - "):
            index += 1
            continue

        match = re.match(r"^([A-Za-z][A-Za-z0-9]*):(?:\s*(.*))?$", line)
        if match is None:
            index += 1
            continue

        key, raw_value = match.groups()
        if raw_value is None or raw_value == "":
            items: list[object] = []
            index += 1
            while index < len(lines) and lines[index].startswith("  - "):
                items.append(parse_scalar(lines[index].removeprefix("  - ")))
                index += 1
            fields[key] = items
            continue

        fields[key] = parse_scalar(raw_value)
        index += 1

    raise ValueError("unterminated frontmatter")


def load_posts() -> list[BlogMetadata]:
    return [
        BlogMetadata(path=path, fields=parse_frontmatter(path))
        for path in sorted(BLOG_DIR.glob("*.md"))
    ]


def validate_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_posts(posts: list[BlogMetadata]) -> list[str]:
    errors: list[str] = []
    seen_days: dict[int, Path] = {}
    seen_slugs: dict[str, Path] = {}

    for post in posts:
        missing = REQUIRED_FIELDS - post.fields.keys()
        if missing:
            errors.append(f"{post.path}: missing fields {sorted(missing)}")
            continue

        day = post.fields["day"]
        slug = post.fields["dashboardSlug"]
        status = post.fields["status"]

        if not isinstance(day, int):
            errors.append(f"{post.path}: day must be an integer")
            continue
        if not isinstance(slug, str):
            errors.append(f"{post.path}: dashboardSlug must be a string")
            continue
        if status not in VALID_STATUSES:
            errors.append(f"{post.path}: invalid status {status!r}")

        dashboard_dir = DASHBOARDS_DIR / slug
        if not dashboard_dir.exists():
            errors.append(f"{post.path}: missing dashboard folder {dashboard_dir}")

        previous_day = seen_days.get(day)
        if previous_day is not None:
            errors.append(f"{post.path}: duplicate day {day} also used by {previous_day}")
        seen_days[day] = post.path

        previous_slug = seen_slugs.get(slug)
        if previous_slug is not None:
            errors.append(f"{post.path}: duplicate slug {slug} also used by {previous_slug}")
        seen_slugs[slug] = post.path

        data_sources = post.fields["dataSources"]
        if not isinstance(data_sources, list):
            errors.append(f"{post.path}: dataSources must be a list")
        elif data_sources:
            errors.append(f"{post.path}: complex dataSources require Astro schema validation")

        hero_image = post.fields.get("heroImage")
        if status == "published" and isinstance(hero_image, str):
            media_path = ROOT / "web" / "public" / hero_image.removeprefix("/")
            if not media_path.exists():
                errors.append(f"{post.path}: missing published media {media_path}")

    dashboard_dirs = [
        path for path in DASHBOARDS_DIR.glob("day-[0-9][0-9][0-9]-*") if path.is_dir()
    ]
    post_slugs = {
        fields["dashboardSlug"]
        for fields in (post.fields for post in posts)
        if isinstance(fields.get("dashboardSlug"), str)
    }
    for dashboard_dir in dashboard_dirs:
        if dashboard_dir.name not in post_slugs:
            errors.append(f"{dashboard_dir}: missing matching blog post")

    return errors


def main() -> None:
    errors = validate_posts(load_posts())
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("Dashboard metadata is valid.")


if __name__ == "__main__":
    main()
