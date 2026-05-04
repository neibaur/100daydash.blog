# Migration Plan

## Why Deferred

100daydash.blog is intentionally local-first and low-to-no-cost. Larger platform changes, deployment automation, cloud storage, analytics, CMS features, or infrastructure-as-code should wait until repeated dashboard patterns prove the need.

## Risks

- Premature cloud or deployment automation could introduce stateful CI behavior.
- Real API credentials or production datasets could leak if mock and real data paths are blurred.
- Framework or action upgrades could weaken branch protection, CodeQL, secret scanning, or coverage gates if validation is skipped.
- Dashboard publishing shortcuts could bypass metadata validation and make the archive inconsistent.

## Phased Approach

1. Document the proposed migration in an ADR before implementation.
2. Prototype locally with fixtures, mock data, or public read-only examples.
3. Add tests and validation around any reusable migration logic.
4. Run security scans and builds in CI without mutating external systems.
5. Require human approval before any production deployment, publishing, credential, or data-mutating operation.

## Validation Needed Before Implementation

- `uv run python scripts/validate-dashboard-metadata.py`
- `uv run pytest --cov`
- `pnpm --filter web build`
- Secret scanning with Gitleaks and detect-secrets
- Review of workflow permissions and branch protection impact
