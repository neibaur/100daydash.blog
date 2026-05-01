# Day 002: First Dashboard Test

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
- Blog post: `../../web/src/content/blog/day-002-first-dashboard-test.md`

## Run Locally

```bash
uv run python dashboards/day-002-first-dashboard-test/src/main.py
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
