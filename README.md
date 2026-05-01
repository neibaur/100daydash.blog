# 100daydash.blog

100 dashboards in 100 days.

This repository contains the publishing system for `100daydash.blog`: an Astro
blog, Python dashboard workspaces, local-first automation, and the quality gates
needed to keep the project easy to maintain as the daily archive grows.

## Repository Layout

- `web/`: Astro + TypeScript site and blog content.
- `dashboards/`: Python dashboard source, tests, data folders, and exports.
- `docs/`: Architecture, development, security, and publishing notes.
- `scripts/`: Repository automation for dashboard scaffolding and validation.

## Local Development

```bash
.venv\Scripts\uv.exe sync
.venv\Scripts\uv.exe run pytest --cov
pnpm --dir web install
pnpm --dir web build
```

Use `uv` for Python dependencies and `pnpm` for the Astro frontend.
