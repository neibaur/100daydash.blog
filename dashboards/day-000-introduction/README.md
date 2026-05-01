# Day 000: Building 100daydash.blog

## Summary

This setup dashboard verifies the repository shape for 100 dashboards in 100
days.

## Question

What foundation is needed to publish dashboard code, outputs, and narrative posts
repeatably?

## Data Sources

| Source | URL | License/Terms | Notes |
|---|---|---|---|
| Project repository | https://100daydash.blog | Project-owned | Initial structure only |

## Method

The Day 0 script writes a tiny HTML placeholder that confirms the output path and
static export flow.

## Outputs

- Screenshot: `outputs/images/preview.png`
- Interactive dashboard: `outputs/html/index.html`
- Blog post: `../../web/src/content/blog/day-000-introduction.md`

## Run Locally

```bash
uv run python dashboards/day-000-introduction/src/main.py
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

Day 0 is a repository setup milestone rather than a data-heavy dashboard.

## Limitations

The current output is a placeholder and does not visualize an external dataset.

## Future Improvements

Replace the placeholder with a generated project progress dashboard after the
first several days establish real publishing metrics.
