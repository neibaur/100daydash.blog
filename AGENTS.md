# AGENTS.md

## 0. Purpose

This repository powers **100daydash.blog**, a monorepo for publishing **100 dashboards in 100 days**.

The project combines:

- **Narrative publishing**: daily Markdown blog posts
- **Rich media**: screenshots, videos, animated GIFs, and static exports
- **Interactive dashboards**: embedded HTML dashboards, hosted static assets, or dashboard links
- **Python dashboard logic**: data ingestion, transformation, validation, visualization, and exports

This file is the primary operating guide for AI coding agents such as **Cursor**, **Windsurf**, **Codex**, or similar tools.

Agents must follow this file before making structural, dependency, security, or architectural changes.

---

# 1. Progressive Disclosure Guide

This file is organized using progressive disclosure.

Agents should read in this order:

1. **Level 1**: non-negotiable rules
2. **Level 2**: repo responsibilities
3. **Level 3**: engineering principles
4. **Level 4**: dashboard standards
5. **Level 5**: quality and security gates
6. **Level 6**: CI/CD expectations
7. **Level 7**: scaffolding and automation
8. **Level 8**: definition of done

---

## Level 1: Read This First

Before editing code:

1. Understand the requested change.
2. Inspect existing files before modifying.
3. Make the smallest safe change.
4. Prefer local-first development.
5. Use trunk-based development.
6. Keep commits atomic.
7. Preserve existing behavior unless asked to change it.
8. Add or update tests for meaningful logic changes.
9. Update documentation when setup, behavior, standards, or structure changes.
10. Never commit secrets.

Do **not** introduce unnecessary:

- cloud services
- backend APIs
- databases
- auth systems
- paid services
- complex frameworks
- long-lived branches
- unrequested abstractions

The default goal is a fast, local-first, low-to-no-cost publishing workflow.

---

# 2. Repository Responsibilities

## `/web`

Astro + TypeScript frontend responsible for:

- Blog posts
- SEO
- routing
- layouts
- static assets
- rich media
- embedded dashboard outputs
- content collections
- homepage and archive pages

Use:

- Astro
- TypeScript
- pnpm
- ESLint
- Prettier
- Vitest where useful

Canonical blog post path:

```text
web/src/content/blog/
```

All daily Markdown posts must go in this directory.

Do not create competing directories such as:

```text
web/src/content/posts/
web/src/content/articles/
web/src/content/journal/
```

unless the architecture is intentionally changed and this file is updated.

---

## `/dashboards`

Python workspace responsible for:

- data ingestion
- data cleaning
- data validation
- data transformation
- visualization generation
- static dashboard exports
- screenshots or HTML outputs for the blog

Use:

- Python
- uv
- Ruff
- Mypy
- Pytest
- pytest-cov
- pytest-mock
- Bandit
- detect-secrets

Use **uv only** for Python dependency and environment management.

Do not create:

```text
requirements.txt
requirements-dev.txt
Pipfile
poetry.lock
```

unless explicitly requested.

The canonical Python dependency files are:

```text
pyproject.toml
uv.lock
```

---

## `/docs`

Documentation-as-code location for:

- architecture notes
- ADRs
- dashboard standards
- local development guide
- security notes
- CI/CD notes
- publishing workflow

---

## `.github`

Automation location for:

- CI validation
- security scans
- CodeQL
- dependency review
- optional deployment workflows

---

# 3. Development Principles

## 3.1 Trunk-Based Development

Use short-lived branches.

Preferred branch names:

```text
feat/day-001-dashboard-title
fix/web-seo-title
chore/init-quality-tools
docs/update-dashboard-standard
test/metadata-validator
```

Merge frequently into `main`.

Avoid long-lived feature branches.

---

## 3.2 Atomic Commits

Each commit should represent one logical change.

Good examples:

```text
docs: add project operating guide
chore: initialize astro frontend
chore: configure uv python workspace
feat: add day 000 introduction post
test: add dashboard metadata validation
ci: add codeql workflow
security: add gitleaks configuration
```

Avoid:

```text
misc updates
big changes
stuff
checkpoint
changes
```

---

## 3.3 Practical TDD & Coverage Gate

Use practical TDD, not ceremony.

Coverage Gate (Practical):

- Minimum 80% coverage is required for:
  - reusable modules
  - scripts in /scripts
  - shared utilities in /dashboards/common
  - validation logic

- For early-stage or exploratory dashboards:
  - focus on testing critical logic only
  - avoid over-testing one-off scripts

Coverage must be measured using:

- pytest-cov for Python
- vitest --coverage for TypeScript

Coverage requirement:

- Modified modules must maintain ≥ 80% coverage
- Shared and reusable modules should maintain ≥ 80% coverage overall

AI agents should prioritize meaningful coverage over artificial coverage.

AI agents must verify coverage using pytest-cov or vitest before declaring a task complete.

Prioritize testing edge cases: directory already exists, invalid metadata formats, and network failures in ingest.py.

Tests are expected for:

- Python data transforms
- reusable utility functions
- metadata validation
- file path generation
- data schema validation
- dashboard generation logic
- TypeScript utility functions

Tests are not required for:

- every static Markdown post
- every simple Astro component
- one-off exploratory notebooks
- placeholder content

When in doubt, test logic that could silently break future dashboards.

---

## 3.4 DRY, But Not Too Early

Avoid copy-pasting repeated:

- metadata schemas
- dashboard folder structures
- Astro layouts
- validation logic
- export paths
- chart helper functions

Prefer:

- shared templates
- typed metadata schemas
- utility functions
- reusable Astro components
- dashboard scaffolding scripts

However, do not over-abstract before at least 3 similar examples exist.

---

## 3.5 Local-First Development

The project should work locally without paid infrastructure.

Default assumptions:

- local Python execution
- local Astro build
- static output where possible
- GitHub Pages or similar low-cost hosting
- public datasets or checked-in sample data
- secrets only through local `.env` or GitHub Actions secrets

---

# 4. Dashboard Standards

Every dashboard must include either:

1. a standardized `README.md`, or
2. a complete metadata header in the related Markdown post.

Preferred approach: use both.

---

## 4.1 Dashboard Folder Structure

Preferred daily dashboard folder:

```text
dashboards/day-001-dashboard-slug/
├── README.md
├── src/
│   ├── ingest.py
│   ├── transform.py
│   ├── visualize.py
│   └── main.py
├── tests/
│   ├── test_ingest.py
│   ├── test_transform.py
│   └── test_visualize.py
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── .gitkeep
└── outputs/
    ├── images/
    │   └── .gitkeep
    ├── html/
    │   └── .gitkeep
    └── video/
        └── .gitkeep
```

For very small dashboards, this may be simplified, but the dashboard must still have:

```text
README.md
src/
tests/
outputs/
```

---

## 4.2 Required Dashboard Metadata

Each dashboard should define:

```yaml
day: 1
title: "Dashboard Title"
slug: "dashboard-title"
date: "YYYY-MM-DD"
status: "draft"
summary: "Short dashboard summary"
data_sources:
  - name: "Source Name"
    url: "https://example.com"
    license: "Public domain or source-specific license"
tools:
  - Python
  - Astro
  - Plotly
outputs:
  - type: screenshot
    path: outputs/images/preview.png
  - type: interactive
    path: outputs/html/index.html
```

Allowed statuses:

```text
draft
published
archived
```

---

## 4.3 Blog Post Frontmatter Standard

Daily posts must live in:

```text
web/src/content/blog/
```

Example:

```yaml
---
title: "Day 001: Dashboard Title"
description: "Short SEO-friendly description of the dashboard."
pubDate: "YYYY-MM-DD"
day: 1
dashboardSlug: "dashboard-title"
status: "draft"
tags:
  - dashboard
  - python
  - data-visualization
dataSources:
  - name: "Source Name"
    url: "https://example.com"
heroImage: "/media/day-001/preview.png"
---
```

---

## 4.4 Dashboard README Template

```md
# Day 001: Dashboard Title

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
- Blog post: `../../web/src/content/blog/day-001-dashboard-title.md`

## Run Locally

```bash
uv run python dashboards/day-001-dashboard-title/src/main.py
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
```

---

# 5. Initial Monorepo Directory Structure

```text
100daydash.blog/
├── AGENTS.md
├── README.md
├── .gitignore
├── .editorconfig
├── .env.example
├── .pre-commit-config.yaml
├── .gitleaks.toml
├── pyproject.toml
├── uv.lock
├── package.json
├── pnpm-lock.yaml
├── pnpm-workspace.yaml
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── security.yml
│       ├── codeql.yml
│       └── dependency-review.yml
│
├── docs/
│   ├── architecture.md
│   ├── dashboard-standard.md
│   ├── local-development.md
│   ├── security.md
│   └── adr/
│       └── 0001-monorepo-astro-python.md
│
├── web/
│   ├── astro.config.mjs
│   ├── package.json
│   ├── tsconfig.json
│   ├── eslint.config.js
│   ├── prettier.config.cjs
│   ├── vitest.config.ts
│   ├── public/
│   │   ├── favicon.svg
│   │   └── media/
│   │       └── day-000/
│   │           └── .gitkeep
│   └── src/
│       ├── components/
│       ├── content/
│       │   ├── config.ts
│       │   └── blog/
│       │       └── day-000-introduction.md
│       ├── layouts/
│       │   └── BlogPostLayout.astro
│       ├── pages/
│       │   ├── index.astro
│       │   └── blog/
│       ├── styles/
│       └── utils/
│
├── dashboards/
│   ├── README.md
│   ├── common/
│   │   ├── README.md
│   │   └── src/
│   ├── templates/
│   │   ├── dashboard-readme-template.md
│   │   └── metadata-template.yml
│   └── day-000-introduction/
│       ├── README.md
│       ├── src/
│       │   └── main.py
│       ├── tests/
│       │   └── test_main.py
│       ├── data/
│       │   ├── raw/
│       │   │   └── .gitkeep
│       │   └── processed/
│       │       └── .gitkeep
│       └── outputs/
│           ├── images/
│           │   └── .gitkeep
│           ├── html/
│           │   └── .gitkeep
│           └── video/
│               └── .gitkeep
│
└── scripts/
    ├── validate-dashboard-metadata.py
    └── new-dashboard.py
```

---

# 6. Python Environment Standard

Use **uv**.

Required files:

```text
pyproject.toml
uv.lock
```

Recommended initial setup:

```bash
uv init --bare
uv add --dev ruff mypy pytest pytest-cov pytest-mock bandit detect-secrets
```

Recommended `pyproject.toml` baseline:

```toml
[project]
name = "100daydash-blog"
version = "0.1.0"
description = "100 dashboards in 100 days"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "bandit>=1.7.10",
    "detect-secrets>=1.5.0",
    "mypy>=1.13.0",
    "pytest>=8.3.0",
    "pytest-cov>=5.0.0",
    "pytest-mock>=3.14.0",
    "ruff>=0.8.0",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",
    "F",
    "I",
    "B",
    "UP",
    "SIM",
]
ignore = []

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["dashboards", "scripts"]
python_files = ["test_*.py"]
addopts = "-ra --cov=dashboards --cov=scripts --cov-report=term-missing"

[tool.coverage.run]
branch = true
source = ["dashboards", "scripts"]

[tool.bandit]
exclude_dirs = ["tests", ".venv"]
```

---

# 7. Frontend Environment Standard

Use **pnpm**.

Required files:

```text
package.json
pnpm-lock.yaml
pnpm-workspace.yaml
web/package.json
```

Root `pnpm-workspace.yaml`:

```yaml
packages:
  - "web"
```

Recommended `/web/package.json` scripts:

```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "lint": "eslint .",
    "format": "prettier . --write",
    "format:check": "prettier . --check",
    "typecheck": "astro check",
    "test": "vitest run"
  }
}
```

---

# 8. Astro Content Collection Schema

Create:

```text
web/src/content/config.ts
```

Recommended baseline:

```ts
import { defineCollection, z } from "astro:content";

const blog = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    day: z.number().int().min(0).max(100),
    dashboardSlug: z.string(),
    status: z.enum(["draft", "published", "archived"]).default("draft"),
    tags: z.array(z.string()).default([]),
    dataSources: z
      .array(
        z.object({
          name: z.string(),
          url: z.string().url(),
        }),
      )
      .default([]),
    heroImage: z.string().optional(),
  }),
});

export const collections = { blog };
```

---

# 9. Security Requirements

Never commit:

- API keys
- tokens
- passwords
- private certificates
- `.env` files
- production secrets
- browser cookies
- downloaded private data
- personally identifiable information unless intentionally anonymized

Use:

- `.env.example`
- GitHub Actions secrets
- local environment variables

---

## 9.1 Default $0 Security Baseline

For open-source or low-to-no-cost setup, use:

- **CodeQL** for SAST
- **Gitleaks** for secret scanning
- **detect-secrets** for local/Python secret scanning
- **Bandit** for Python security checks
- **GitHub dependency review**
- **pnpm audit** or equivalent SCA
- **uv dependency review** where applicable

Checkmarx may be added later if available through work, school, or enterprise licensing.

Default SAST choice:

```text
CodeQL
```

Optional enterprise SAST:

```text
Checkmarx
```

---

# 10. GitHub Actions

## 10.1 CI Workflow

Create:

```text
.github/workflows/ci.yml
```

Suggested baseline:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  python-quality:
    name: Python Quality
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-groups

      - name: Ruff lint
        run: uv run ruff check .

      - name: Ruff format check
        run: uv run ruff format --check .

      - name: Mypy
        run: uv run mypy .

      - name: Pytest
        run: uv run pytest --cov

      - name: Bandit
        run: uv run bandit -r dashboards scripts

      - name: detect-secrets
        run: uv run detect-secrets scan --all-files

  web-quality:
    name: Web Quality
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: web

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up pnpm
        uses: pnpm/action-setup@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: pnpm
          cache-dependency-path: pnpm-lock.yaml

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm lint

      - name: Format check
        run: pnpm format:check

      - name: Typecheck
        run: pnpm typecheck

      - name: Test
        run: pnpm test

      - name: Build
        run: pnpm build
```

---

## 10.2 CodeQL Workflow

Create:

```text
.github/workflows/codeql.yml
```

Suggested baseline:

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "30 6 * * 1"

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest

    permissions:
      security-events: write
      packages: read
      actions: read
      contents: read

    strategy:
      fail-fast: false
      matrix:
        language: ["javascript-typescript", "python"]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: ${{ matrix.language }}

      - name: Autobuild
        uses: github/codeql-action/autobuild@v3

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
```

---

## 10.3 Security Workflow

Create:

```text
.github/workflows/security.yml
```

Suggested baseline:

```yaml
name: Security

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  gitleaks:
    name: Gitleaks
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
```

---

## 10.4 Dependency Review Workflow

Create:

```text
.github/workflows/dependency-review.yml
```

Suggested baseline:

```yaml
name: Dependency Review

on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: read

jobs:
  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Dependency Review
        uses: actions/dependency-review-action@v4
```

## 10.5 GitHub Actions Standards (2026 Update)

Node Runtime Standard:

- Prefer GitHub Actions that are compatible with Node 20+ or Node 24.
- Avoid deprecated Node 16-based actions.
- Do not rely on undocumented environment variables to force Node versions.

Action Versioning:

- Prefer latest stable major versions of actions.
- Examples:
  - actions/checkout@v4
  - actions/setup-node@v4
  - github/codeql-action@v4 or newer
- Update workflows when upgrading major versions.

Security Noise Reduction:

- Configure Gitleaks and detect-secrets to ignore:
  - .secrets.baseline
  - pnpm-lock.yaml
  - .venv/
- Use explicit allowlists via:
  - .gitleaks.toml
  - detect-secrets baseline
- Do not disable scanning globally.
---

# 11. Pre-Commit Baseline

Create:

```text
.pre-commit-config.yaml
```

Suggested baseline:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: ["--fix"]
      - id: ruff-format

  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.21.0
    hooks:
      - id: gitleaks
```

Install:

```bash
uv add --dev pre-commit
uv run pre-commit install
```

---

# 12. Dashboard Scaffolding Script Expectations

Create:

```text
scripts/new-dashboard.py
```

The script should:

1. accept a day number
2. accept a title
3. generate a slug
4. create the dashboard folder
5. create `README.md`
6. create `src/main.py`
7. create starter tests
8. create data/output directories with `.gitkeep`
9. create the matching blog post in `web/src/content/blog/`
10. prevent overwriting existing folders
11. print next-step commands

Example usage:

```bash
uv run python scripts/new-dashboard.py --day 1 --title "US EV Sales Trend"
```

Expected generated paths:

```text
dashboards/day-001-us-ev-sales-trend/
web/src/content/blog/day-001-us-ev-sales-trend.md
web/public/media/day-001-us-ev-sales-trend/
```

---

# 13. Metadata Validation Script Expectations

Create:

```text
scripts/validate-dashboard-metadata.py
```

The script should validate:

- every blog post has required frontmatter
- every dashboard has a matching folder
- every `dashboardSlug` maps to a dashboard folder
- `day` values are unique
- slugs are unique
- status is valid
- referenced media paths exist when status is `published`
- data source URLs are valid URL strings

Run in CI:

```bash
uv run python scripts/validate-dashboard-metadata.py
```

---

# 14. Day 0 Initialization Checklist

## A. Repo Setup

- [ ] Create GitHub repository: `100daydash.blog`
- [ ] Clone repository locally
- [ ] Create initial branch:

```bash
git checkout -b chore/day-0-init
```

- [ ] Add root files:
  - [ ] `README.md`
  - [ ] `AGENTS.md`
  - [ ] `.gitignore`
  - [ ] `.editorconfig`
  - [ ] `.env.example`

---

## B. Initialize Astro Frontend

- [ ] Create `/web` Astro app with TypeScript
- [ ] Use `pnpm`
- [ ] Add blog content collection
- [ ] Use canonical post path:

```text
web/src/content/blog/
```

- [ ] Add first post:

```text
web/src/content/blog/day-000-introduction.md
```

- [ ] Include frontmatter:

```yaml
---
title: "Day 0: Building 100daydash.blog"
description: "Setting up the foundation for 100 dashboards in 100 days."
pubDate: "YYYY-MM-DD"
day: 0
dashboardSlug: "day-000-introduction"
status: "draft"
tags:
  - dashboard
  - project-setup
  - astro
  - python
dataSources: []
---
```

---

## C. Initialize Python Dashboard Workspace

Use `uv`.

- [ ] Create `/dashboards`
- [ ] Add dashboard template folder
- [ ] Add `day-000-introduction`
- [ ] Add root `pyproject.toml`
- [ ] Add Python quality tools:

```bash
uv add --dev ruff mypy pytest pytest-cov bandit detect-secrets pytest-mock pre-commit
```

Do not create:

```text
requirements.txt
requirements-dev.txt
```

unless explicitly requested.

---

## D. Add Security Tooling

- [ ] Add `.gitleaks.toml`
- [ ] Add `.env.example`
- [ ] Add `.env` to `.gitignore`
- [ ] Add Gitleaks workflow
- [ ] Add CodeQL workflow
- [ ] Add dependency review workflow
- [ ] Add Bandit and detect-secrets to Python CI

Default SAST:

```text
CodeQL
```

Optional enterprise SAST:

```text
Checkmarx
```

---

## E. Add GitHub Actions

Create:

```text
.github/workflows/ci.yml
.github/workflows/security.yml
.github/workflows/codeql.yml
.github/workflows/dependency-review.yml
```

---

## F. First Blog Post

- [ ] Create `Day 0` post:

```text
web/src/content/blog/day-000-introduction.md
```

- [ ] Explain project purpose
- [ ] Explain the 100 dashboards in 100 days goal
- [ ] Include first architecture diagram or placeholder image
- [ ] Link to dashboard folder
- [ ] Add SEO title and description
- [ ] Confirm post renders locally

---

## G. Final Local Validation

Run:

```bash
# Python
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run pytest --cov
uv run bandit -r .
uv run detect-secrets scan --all-files

# Web
cd web
pnpm install
pnpm lint
pnpm format:check
pnpm typecheck
pnpm test
pnpm build
```

---

## H. Commit Atomically

Suggested commits:

```bash
git add AGENTS.md README.md docs/
git commit -m "docs: add project operating guide"

git add web/
git commit -m "chore: initialize astro frontend"

git add dashboards/ pyproject.toml uv.lock
git commit -m "chore: initialize python dashboard workspace"

git add .github/ .gitleaks.toml .env.example .pre-commit-config.yaml
git commit -m "chore: add ci and security checks"

git add web/src/content/blog/day-000-introduction.md
git commit -m "feat: add day 0 introduction post"
```

---

# 15. AI Agent Working Rules

When working as an AI agent:

1. Inspect existing files before modifying.
2. Do not overwrite user work without checking diffs.
3. Prefer small patches.
4. Keep generated files minimal.
5. Do not invent external credentials, services, or APIs.
6. Use placeholders in `.env.example`.
7. Avoid premature abstractions.
8. Avoid unnecessary cloud services.
9. Keep the project local-first.
10. Add TODOs only when useful and specific.
11. Do not create duplicate blog content directories.
12. Do not mix Python environment managers.
13. Do not introduce paid services by default.
14. Do not skip security scans just because the project is small.

Good TODO:

```text
TODO: Add dashboard image optimization after the first 5 media patterns are known.
```

Bad TODO:

```text
TODO: improve this
```

## 15.1 Safe Actions AI Agents May Perform

AI agents may perform these actions without additional human approval when they stay within the requested scope:

- Read, search, and summarize repository files.
- Create or edit documentation, Markdown posts, tests, scripts, Astro components, and Python code.
- Run local validation, formatting checks, tests, metadata validation, builds, and security scans.
- Read public API documentation and inspect safe read-only GET examples.
- Generate local fixtures, mock data, screenshots, static exports, and placeholder assets that do not contain secrets or private data.
- Update CI configuration when the change preserves or strengthens existing quality and security gates.

## 15.2 Unsafe Actions Requiring Explicit Human Approval

AI agents must ask for explicit human approval before performing any action that could mutate real systems, real state, real credentials, billing, or published content.

CRITICAL RULE:

AI agents may read public API documentation and inspect safe GET examples, but must NOT execute real-world POST, PUT, PATCH, DELETE, deployment, publishing, payment, credential, or data-mutating operations without explicit human approval.

This includes:

- Deploying, publishing, releasing, or changing production hosting settings.
- Running infrastructure apply, destroy, import, state migration, or remote-state commands.
- Creating, rotating, revoking, testing, or storing real credentials.
- Writing to external APIs, cloud services, databases, payment systems, analytics systems, or production dashboards.
- Running scripts that delete, overwrite, anonymize, upload, or transform real data irreversibly.
- Changing branch protection, repository secrets, environments, or access controls.

## 15.3 Protected Files and Directories

Treat these paths with extra care:

- `.github/workflows/`
- `.github/CODEOWNERS`
- `.github/pull_request_template.md`
- `.gitleaks.toml`
- `.secrets.baseline`
- `.env.example`
- `AGENTS.md`
- `pyproject.toml`
- `uv.lock`
- `package.json`
- `pnpm-lock.yaml`
- `pnpm-workspace.yaml`
- `scripts/`
- `dashboards/**/data/`
- `dashboards/**/outputs/`
- `web/src/content/blog/`
- `web/public/media/`
- `docs/adr/`

Do not delete, rewrite, or broad-format protected files unless the requested task requires it and the diff is small and reviewable.

## 15.4 Secrets, Generated Files, Real Data, and External Systems

- Never commit API keys, tokens, passwords, cookies, private keys, certificates, or real credentials.
- Keep `.env` and `.env.*` untracked except for safe placeholder files such as `.env.example`.
- Keep `.secrets.baseline` UTF-8 encoded.
- Do not commit raw private data, regulated data, non-anonymized personal data, production exports, or infrastructure state.
- Generated reports, coverage output, build output, virtual environments, dependency folders, and raw/processed data exports should remain ignored unless intentionally documented as a static artifact.
- CI must not call external production systems, mutate infrastructure, publish content, or require real credentials by default.

## 15.5 Mock vs Real Data Separation

Mock, fixture, sample, and synthetic data must be clearly separated from real data.

- Prefer `tests/fixtures/`, `sample`, or clearly named mock files for tests.
- Keep real downloaded data under ignored local data directories unless it is public, small, license-compatible, and intentionally committed.
- Do not use mock or test credentials against real state, production systems, real credentials, or irreversible data operations.
- Document data source licensing and limitations in dashboard README files or blog frontmatter.

## 15.6 Validation Commands

When validating dependency updates, AI agents should:
- Prefer validation commands documented in package.json, CI workflows, AGENTS.md, README, or repository scripts.
- Report missing commands but do not treat undocumented commands as failures.
- Do not invent validation commands that are not part of the repository contract.

Use the narrowest validation needed while working, then run the relevant final checks before declaring completion:

```bash
uv run python scripts/validate-dashboard-metadata.py
uv run pytest --cov
pnpm --filter web build
```

For broader changes, also run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
uv run bandit -r dashboards scripts -x "*/tests/*"
uv run detect-secrets scan --baseline .secrets.baseline
pnpm --filter web lint
pnpm --filter web typecheck
pnpm --filter web test
```

## 15.7 AI Definition of Done

AI-assisted changes are done when:

- The requested behavior or documentation change is complete.
- Existing workflows and quality gates are preserved or strengthened.
- Relevant validation commands pass locally.
- No secrets, real credentials, production exports, or infrastructure state are committed.
- Mock/test configuration has not been used against real state, production systems, real credentials, or irreversible data operations.
- Any deferred risky work is documented in `docs/migration-plan.md` or an ADR.

---

# 16. Definition of Done

A task is complete when:

- code builds locally
- relevant tests pass
- quality tools pass
- documentation is updated
- no secrets are committed
- changes are small and reviewable
- blog post paths use `web/src/content/blog/`
- Python uses `uv`
- frontend uses `pnpm`
- security baseline uses CodeQL unless another SAST tool is explicitly requested
- the blog can still render
- new dashboards follow the metadata standard
- CI config is updated if quality gates change
- agent-created files are intentional and necessary
- Code coverage is ≥ 80% for the modified modules
- scripts/validate-dashboard-metadata.py passes with zero errors

---

# 17. Non-Goals for Initial Setup

Do not add these during Day 0 unless explicitly requested:

- database
- authentication
- CMS
- paid hosting
- backend API
- user accounts
- Docker
- Kubernetes
- Terraform
- complex monorepo build orchestration
- enterprise Checkmarx integration
- analytics tracking
- newsletter system

These may be added later through explicit ADRs.
