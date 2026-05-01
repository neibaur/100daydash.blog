# ADR 0001: Monorepo With Astro and Python

## Status

Accepted

## Context

The project needs narrative publishing, static assets, and repeatable dashboard
generation for 100 daily dashboards.

## Decision

Use a monorepo with Astro + TypeScript in `web/` and Python dashboard workspaces
in `dashboards/`. Manage Python dependencies with `uv` and frontend dependencies
with `pnpm`.

## Consequences

The repository stays local-first and low-cost while leaving room for daily
dashboard code, tests, generated media, and published posts to evolve together.
