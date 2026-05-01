from pathlib import Path


def main() -> None:
    output_dir = Path(__file__).resolve().parents[1] / "outputs" / "html"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_dir.joinpath("index.html").write_text("<h1>First Dashboard Test</h1>\n")


if __name__ == "__main__":
    main()
