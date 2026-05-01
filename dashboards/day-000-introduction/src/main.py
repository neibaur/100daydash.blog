from pathlib import Path


def render_placeholder_html(title: str) -> str:
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title}</title>
  </head>
  <body>
    <main>
      <h1>{title}</h1>
      <p>Repository skeleton, dashboard workspace, and blog pipeline initialized.</p>
    </main>
  </body>
</html>
"""


def write_dashboard(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    output_path.write_text(render_placeholder_html("Day 000: Building 100daydash.blog"))
    return output_path


def main() -> None:
    dashboard_dir = Path(__file__).resolve().parents[1]
    output_path = write_dashboard(dashboard_dir / "outputs" / "html")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
