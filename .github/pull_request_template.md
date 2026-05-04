## Summary

<!-- Describe what changed and why. Keep scope small and reviewable. -->

## Validation Performed

- [ ] `uv run python scripts/validate-dashboard-metadata.py`
- [ ] `uv run pytest --cov`
- [ ] `pnpm --filter web build`
- [ ] Other:

## Security Checklist

- [ ] No secrets, tokens, passwords, cookies, private keys, or real credentials were added.
- [ ] `.env` files and generated secret scan reports remain untracked.
- [ ] Secret scanning remains enabled; no scanner was disabled to make this pass.
- [ ] Public API documentation or safe GET examples were used only for reference.

**DO NOT use mock/test configuration against real state, production systems, real credentials, or irreversible data operations.**

## CI/CD Safety Checklist

- [ ] This change does not add stateful, mutating, deployment, publishing, or production operations to CI.
- [ ] Existing quality gates remain intact or stricter.
- [ ] Workflow permissions are least-privilege for the task.
- [ ] New automation is deterministic and local-first where practical.

## Data / Infrastructure Safety Checklist

- [ ] Mock, fixture, and sample data are clearly separated from real data.
- [ ] No private, sensitive, regulated, or non-anonymized data was committed.
- [ ] No real infrastructure state, Terraform state, production export, or credential-bearing artifact was committed.
- [ ] No real-world POST, PUT, PATCH, DELETE, deployment, payment, credential, or data-mutating operation was executed without explicit human approval.
