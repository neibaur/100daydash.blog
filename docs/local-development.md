# Local Development

## Python

```bash
.venv\Scripts\uv.exe sync
.venv\Scripts\uv.exe run ruff check .
.venv\Scripts\uv.exe run pytest --cov
```

## Web

```bash
pnpm --dir web install
pnpm --dir web dev
pnpm --dir web build
```

Use `.env.example` for local configuration placeholders. Real secrets belong in
local `.env` files or GitHub Actions secrets.
