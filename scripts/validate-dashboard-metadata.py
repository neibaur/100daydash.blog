from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BLOG_DIR = ROOT / "web" / "src" / "content" / "blog"
DASHBOARDS_DIR = ROOT / "dashboards"
VALID_STATUSES = {"draft", "published", "archived"}
BLOG_REQUIRED_FIELDS = {
    "title",
    "description",
    "pubDate",
    "day",
    "dashboardSlug",
    "status",
    "tags",
    "dataSources",
}
DASHBOARD_REQUIRED_FIELDS = {
    "day",
    "title",
    "slug",
    "date",
    "status",
    "summary",
    "data_sources",
    "tools",
    "outputs",
}
DASHBOARD_FOLDER_PATTERN = re.compile(r"^day-(?P<day>\d{3})-(?P<slug>[a-z0-9][a-z0-9-]*)$")


@dataclass(frozen=True)
class BlogMetadata:
    path: Path
    fields: dict[str, object]


@dataclass(frozen=True)
class DashboardMetadata:
    path: Path
    folder: Path
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


def parse_mapping(lines: list[str]) -> dict[str, object]:
    fields: dict[str, object] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.startswith("  ") or line.startswith("    "):
            index += 1
            continue

        match = re.match(r"^([A-Za-z][A-Za-z0-9_]*):(?:\s*(.*))?$", line)
        if match is None:
            index += 1
            continue

        key, raw_value = match.groups()
        if raw_value is None or raw_value == "":
            items: list[object] = []
            index += 1
            while index < len(lines) and lines[index].startswith("  - "):
                item_line = lines[index].removeprefix("  - ")
                item_match = re.match(r"^([A-Za-z][A-Za-z0-9_]*):\s*(.*)$", item_line)
                if item_match is None:
                    items.append(parse_scalar(item_line))
                    index += 1
                    continue

                item: dict[str, object] = {item_match.group(1): parse_scalar(item_match.group(2))}
                index += 1
                while index < len(lines) and lines[index].startswith("    "):
                    child_match = re.match(
                        r"^\s{4}([A-Za-z][A-Za-z0-9_]*):\s*(.*)$",
                        lines[index],
                    )
                    if child_match is not None:
                        item[child_match.group(1)] = parse_scalar(child_match.group(2))
                    index += 1
                items.append(item)
            fields[key] = items
            continue

        fields[key] = parse_scalar(raw_value)
        index += 1

    return fields


def parse_frontmatter(path: Path) -> dict[str, object]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing frontmatter")

    end_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line == "---"),
        None,
    )
    if end_index is None:
        raise ValueError("unterminated frontmatter")
    return parse_mapping(lines[1:end_index])


def parse_metadata(path: Path) -> dict[str, object]:
    return parse_mapping(path.read_text(encoding="utf-8").splitlines())


def load_posts(blog_dir: Path = BLOG_DIR) -> list[BlogMetadata]:
    return [
        BlogMetadata(path=path, fields=parse_frontmatter(path))
        for path in sorted(blog_dir.glob("*.md"))
    ]


def load_dashboards(dashboards_dir: Path = DASHBOARDS_DIR) -> list[DashboardMetadata]:
    dashboards: list[DashboardMetadata] = []
    for folder in sorted(dashboards_dir.glob("day-[0-9][0-9][0-9]-*")):
        if not folder.is_dir():
            continue
        metadata_path = folder / "metadata.yml"
        fields = parse_metadata(metadata_path) if metadata_path.exists() else {}
        dashboards.append(DashboardMetadata(path=metadata_path, folder=folder, fields=fields))
    return dashboards


def validate_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def parse_folder_parts(folder_name: str) -> tuple[int, str] | None:
    match = DASHBOARD_FOLDER_PATTERN.match(folder_name)
    if match is None:
        return None
    return int(match.group("day")), match.group("slug")


def require_string(
    fields: dict[str, object],
    field: str,
    path: Path,
    errors: list[str],
) -> str | None:
    value = fields.get(field)
    if not isinstance(value, str) or not value:
        errors.append(f"{path}: {field} must be a non-empty string")
        return None
    return value


def require_int(fields: dict[str, object], field: str, path: Path, errors: list[str]) -> int | None:
    value = fields.get(field)
    if not isinstance(value, int):
        errors.append(f"{path}: {field} must be an integer")
        return None
    return value


def validate_data_sources(
    value: object,
    path: Path,
    field_name: str,
    errors: list[str],
    require_license: bool,
) -> None:
    if not isinstance(value, list):
        errors.append(f"{path}: {field_name} must be a list")
        return

    for index, source in enumerate(value):
        if isinstance(source, str) and source and not require_license:
            continue
        if not isinstance(source, dict):
            errors.append(f"{path}: {field_name}[{index}] must be an object")
            continue
        name = source.get("name")
        url = source.get("url")
        license_value = source.get("license")
        if not isinstance(name, str) or not name:
            errors.append(f"{path}: {field_name}[{index}].name must be a non-empty string")
        if not isinstance(url, str) or not validate_url(url):
            errors.append(f"{path}: {field_name}[{index}].url must be a valid URL")
        if require_license and (not isinstance(license_value, str) or not license_value):
            errors.append(f"{path}: {field_name}[{index}].license must be a non-empty string")


def validate_outputs(value: object, path: Path, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: outputs must be a non-empty list")
        return

    for index, output in enumerate(value):
        if not isinstance(output, dict):
            errors.append(f"{path}: outputs[{index}] must be an object")
            continue
        if not isinstance(output.get("type"), str) or not output["type"]:
            errors.append(f"{path}: outputs[{index}].type must be a non-empty string")
        if not isinstance(output.get("path"), str) or not output["path"]:
            errors.append(f"{path}: outputs[{index}].path must be a non-empty string")


def validate_blog_posts(
    posts: list[BlogMetadata],
    root: Path = ROOT,
    dashboards_dir: Path = DASHBOARDS_DIR,
) -> list[str]:
    errors: list[str] = []
    seen_days: dict[int, Path] = {}
    seen_slugs: dict[str, Path] = {}

    for post in posts:
        missing = BLOG_REQUIRED_FIELDS - post.fields.keys()
        if missing:
            errors.append(f"{post.path}: missing blog fields {sorted(missing)}")
            continue

        require_string(post.fields, "title", post.path, errors)
        require_string(post.fields, "description", post.path, errors)
        require_string(post.fields, "pubDate", post.path, errors)
        day = require_int(post.fields, "day", post.path, errors)
        slug = require_string(post.fields, "dashboardSlug", post.path, errors)
        status = require_string(post.fields, "status", post.path, errors)

        tags = post.fields.get("tags")
        if not isinstance(tags, list) or not all(isinstance(tag, str) and tag for tag in tags):
            errors.append(f"{post.path}: tags must be a list of non-empty strings")
        validate_data_sources(
            post.fields.get("dataSources"),
            post.path,
            "dataSources",
            errors,
            False,
        )

        if status is not None and status not in VALID_STATUSES:
            errors.append(f"{post.path}: invalid status {status!r}")
        if day is None or slug is None:
            continue

        if slug != "none":
            dashboard_dir = dashboards_dir / slug
            if not dashboard_dir.exists():
                errors.append(f"{post.path}: missing dashboard folder {dashboard_dir}")

            folder_parts = parse_folder_parts(slug)
            if folder_parts is None:
                errors.append(f"{post.path}: dashboardSlug must match day-NNN-slug")
            elif folder_parts[0] != day:
                errors.append(
                    f"{post.path}: day {day} does not match dashboardSlug day {folder_parts[0]}"
                )

        previous_day = seen_days.get(day)
        if previous_day is not None:
            errors.append(f"{post.path}: duplicate day {day} also used by {previous_day}")
        seen_days[day] = post.path

        if slug != "none":
            previous_slug = seen_slugs.get(slug)
            if previous_slug is not None:
                errors.append(f"{post.path}: duplicate slug {slug} also used by {previous_slug}")
            seen_slugs[slug] = post.path

        hero_image = post.fields.get("heroImage")
        if hero_image is not None:
            if not isinstance(hero_image, str) or not hero_image.startswith("/media/"):
                errors.append(f"{post.path}: heroImage must be a /media/ path")
            else:
                media_path = root / "web" / "public" / hero_image.removeprefix("/")
                if not media_path.exists():
                    errors.append(f"{post.path}: missing heroImage media {media_path}")

    return errors


def validate_dashboards(dashboards: list[DashboardMetadata]) -> list[str]:
    errors: list[str] = []

    for dashboard in dashboards:
        if not dashboard.path.exists():
            errors.append(f"{dashboard.folder}: missing metadata.yml")
            continue

        missing = DASHBOARD_REQUIRED_FIELDS - dashboard.fields.keys()
        if missing:
            errors.append(f"{dashboard.path}: missing dashboard fields {sorted(missing)}")
            continue

        folder_parts = parse_folder_parts(dashboard.folder.name)
        if folder_parts is None:
            errors.append(f"{dashboard.folder}: folder must match day-NNN-slug")
            continue

        folder_day, folder_slug = folder_parts
        day = require_int(dashboard.fields, "day", dashboard.path, errors)
        slug = require_string(dashboard.fields, "slug", dashboard.path, errors)
        require_string(dashboard.fields, "title", dashboard.path, errors)
        require_string(dashboard.fields, "date", dashboard.path, errors)
        status = require_string(dashboard.fields, "status", dashboard.path, errors)
        require_string(dashboard.fields, "summary", dashboard.path, errors)

        if day is not None and day != folder_day:
            errors.append(f"{dashboard.path}: day {day} does not match folder day {folder_day}")
        if slug is not None and slug != folder_slug:
            errors.append(
                f"{dashboard.path}: slug {slug!r} does not match folder slug {folder_slug!r}"
            )
        if status is not None and status not in VALID_STATUSES:
            errors.append(f"{dashboard.path}: invalid status {status!r}")

        tools = dashboard.fields.get("tools")
        if not isinstance(tools, list) or not all(isinstance(tool, str) and tool for tool in tools):
            errors.append(f"{dashboard.path}: tools must be a list of non-empty strings")
        validate_data_sources(
            dashboard.fields.get("data_sources"),
            dashboard.path,
            "data_sources",
            errors,
            True,
        )
        validate_outputs(dashboard.fields.get("outputs"), dashboard.path, errors)

    return errors


def validate_repository(
    posts: list[BlogMetadata],
    dashboards: list[DashboardMetadata],
    root: Path = ROOT,
    dashboards_dir: Path = DASHBOARDS_DIR,
) -> list[str]:
    errors = validate_blog_posts(posts, root, dashboards_dir)
    errors.extend(validate_dashboards(dashboards))

    post_slugs = {
        fields["dashboardSlug"]
        for fields in (post.fields for post in posts)
        if isinstance(fields.get("dashboardSlug"), str)
    }
    for dashboard in dashboards:
        if dashboard.folder.name not in post_slugs:
            errors.append(f"{dashboard.folder}: missing matching blog post")

    return errors


def main() -> None:
    errors = validate_repository(load_posts(), load_dashboards())
    if errors:
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("Dashboard metadata is valid.")


if __name__ == "__main__":
    main()
