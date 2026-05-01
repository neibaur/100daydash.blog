import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_module() -> ModuleType:
    module_path = Path(__file__).resolve().parents[1] / "validate-dashboard-metadata.py"
    spec = importlib.util.spec_from_file_location("validate_dashboard_metadata", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_frontmatter_reads_required_fields(tmp_path: Path) -> None:
    module = load_module()
    post = tmp_path / "post.md"
    post.write_text(
        """---
title: "Day 0"
description: "Description"
pubDate: "2026-05-01"
day: 0
dashboardSlug: "day-000-introduction"
status: "draft"
tags:
  - dashboard
dataSources: []
---
Body
""",
        encoding="utf-8",
    )

    fields = module.parse_frontmatter(post)

    assert fields["day"] == 0
    assert fields["tags"] == ["dashboard"]


def test_validate_url_accepts_https() -> None:
    module = load_module()

    assert module.validate_url("https://example.com")
