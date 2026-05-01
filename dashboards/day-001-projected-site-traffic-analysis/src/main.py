from __future__ import annotations

# ruff: noqa: E402, I001

import csv
import shutil
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


DASHBOARD_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = DASHBOARD_DIR.parents[1]
RAW_DATA_PATH = DASHBOARD_DIR / "data" / "raw" / "traffic.csv"
PREVIEW_PATH = DASHBOARD_DIR / "outputs" / "images" / "preview.png"
PUBLIC_PREVIEW_PATH = (
    REPO_ROOT
    / "web"
    / "public"
    / "media"
    / "day-001-projected-site-traffic-analysis"
    / "preview.png"
)


@dataclass(frozen=True)
class TrafficRow:
    date: date
    target_traffic: int
    actual_traffic: int


def generate_traffic_rows(start_date: date, days: int = 100) -> list[TrafficRow]:
    rows: list[TrafficRow] = []
    for index in range(days):
        target = 1000 + (index * 42)
        weekly_cycle = [0, 12, -8, 18, -6, -22, 10][index % 7]
        ramp_variance = int(index * 1.4)
        actual = target + weekly_cycle + ramp_variance - 35
        rows.append(
            TrafficRow(
                date=start_date + timedelta(days=index),
                target_traffic=target,
                actual_traffic=actual,
            )
        )
    return rows


def write_csv(rows: list[TrafficRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["date", "target_traffic", "actual_traffic"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "date": row.date.isoformat(),
                    "target_traffic": row.target_traffic,
                    "actual_traffic": row.actual_traffic,
                }
            )


def render_chart(rows: list[TrafficRow], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dates = [row.date for row in rows]
    target = [row.target_traffic for row in rows]
    actual = [row.actual_traffic for row in rows]

    _, axis = plt.subplots(figsize=(12, 6.75))
    axis.plot(dates, target, label="Target traffic", color="#2563eb", linewidth=2.5)
    axis.plot(dates, actual, label="Actual traffic", color="#16a34a", linewidth=2.5)
    axis.set_title("Projected Site Traffic Analysis")
    axis.set_xlabel("Date")
    axis.set_ylabel("Daily visits")
    axis.grid(True, alpha=0.25)
    axis.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def copy_preview_to_web(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def main() -> None:
    rows = generate_traffic_rows(date(2026, 5, 1))
    write_csv(rows, RAW_DATA_PATH)
    render_chart(rows, PREVIEW_PATH)
    copy_preview_to_web(PREVIEW_PATH, PUBLIC_PREVIEW_PATH)
    print(f"Wrote {RAW_DATA_PATH}")
    print(f"Wrote {PREVIEW_PATH}")
    print(f"Wrote {PUBLIC_PREVIEW_PATH}")


if __name__ == "__main__":
    main()
