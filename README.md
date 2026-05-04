# 100daydash.blog

**100 dashboards in 100 days.**

This repository powers [100daydash.blog](https://100daydash.blog), a structured
project focused on building consistent, production-quality data artifacts on a
daily cadence.

This is not just a blog — it is a **dashboard delivery system** designed to
enforce quality, consistency, and repeatability from Day 1.

---

## 🚀 Project Goals

- Build 100 dashboards (or data artifacts) in 100 days
- Emphasize **consistency over complexity**
- Use **real data sources and APIs**
- Explore a wide range of tools:
  - Python, Power BI, Tableau, Cognos, SQL
  - Cloud platforms (Azure, AWS, GCP)
  - Multiple data storage patterns (files, APIs, databases)

---

## 🧱 Repository Structure

- `web/` — Astro + TypeScript frontend and blog content
- `dashboards/` — Python dashboard workspaces, data, and tests
- `docs/` — Architecture, development, and system design notes
- `scripts/` — Automation for scaffolding and validation

---

## ⚙️ Engineering Standards

This project is intentionally built with production-grade practices:

- **CI/CD**: GitHub Actions (tests, linting, formatting, security)
- **Testing**:
  - Python: `pytest`
  - Frontend: `vitest`
- **Formatting**: Prettier (enforced locally + CI)
- **Linting**: ESLint
- **Pre-commit hooks**:
  - Husky + lint-staged (fail-fast enforcement)
- **Security**:
  - CodeQL (advanced configuration)
  - Secret scanning
  - Dependabot (alerts + updates)

---

## 💻 Local Development

```bash
# Python environment
.venv\Scripts\uv.exe sync
.venv\Scripts\uv.exe run pytest --cov

# Frontend
pnpm --dir web install
pnpm --dir web build
```

---

## Governance

Lightweight governance keeps this portfolio production-minded without slowing daily publishing:

- [AI agent rules](AGENTS.md)
- [Pull request checklist](.github/pull_request_template.md)
- [CODEOWNERS](.github/CODEOWNERS)
- [Architecture notes](docs/architecture.md)
- [Dashboard standard](docs/dashboard-standard.md)
- [Security notes](docs/security.md)
- [Migration plan](docs/migration-plan.md)
