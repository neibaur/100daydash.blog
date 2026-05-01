import csv
import importlib.util
import sys
from datetime import date
from pathlib import Path
from typing import Any


def load_module() -> Any:
    module_path = Path(__file__).resolve().parents[1] / "src" / "main.py"
    spec = importlib.util.spec_from_file_location("day_001_traffic_main", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_generate_traffic_rows_creates_100_days() -> None:
    module = load_module()

    rows = module.generate_traffic_rows(date(2026, 5, 1))

    assert len(rows) == 100
    assert rows[0].date.isoformat() == "2026-05-01"
    assert rows[-1].date.isoformat() == "2026-08-08"
    assert rows[-1].target_traffic > rows[0].target_traffic
    assert rows[-1].actual_traffic > rows[0].actual_traffic


def test_write_csv_creates_expected_columns(tmp_path: Path) -> None:
    module = load_module()
    rows = module.generate_traffic_rows(date(2026, 5, 1), days=2)
    output_path = tmp_path / "traffic.csv"

    module.write_csv(rows, output_path)

    with output_path.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        records = list(reader)

    assert reader.fieldnames == ["date", "target_traffic", "actual_traffic"]
    assert len(records) == 2


def test_render_chart_and_copy_preview(tmp_path: Path) -> None:
    module = load_module()
    rows = module.generate_traffic_rows(date(2026, 5, 1), days=10)
    preview_path = tmp_path / "outputs" / "images" / "preview.png"
    public_path = tmp_path / "web" / "public" / "media" / "preview.png"

    module.render_chart(rows, preview_path)
    module.copy_preview_to_web(preview_path, public_path)

    assert preview_path.exists()
    assert preview_path.stat().st_size > 0
    assert public_path.exists()
    assert public_path.read_bytes() == preview_path.read_bytes()
