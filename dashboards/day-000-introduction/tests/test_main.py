import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_main_module() -> ModuleType:
    module_path = Path(__file__).resolve().parents[1] / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("day_000_main", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_render_placeholder_html_includes_title() -> None:
    module = load_main_module()

    html = module.render_placeholder_html("Day 000")

    assert "<h1>Day 000</h1>" in html


def test_write_dashboard_creates_index(tmp_path: Path) -> None:
    module = load_main_module()

    output_path = module.write_dashboard(tmp_path)

    assert output_path == tmp_path / "index.html"
    assert output_path.exists()
