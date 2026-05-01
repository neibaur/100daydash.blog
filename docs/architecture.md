# Architecture

`100daydash.blog` is a local-first monorepo with two primary surfaces:

- An Astro site in `web/` for posts, routing, SEO, and public media.
- Python dashboard workspaces in `dashboards/` for data work and static exports.

Daily dashboards publish through Markdown posts in `web/src/content/blog/`. The
matching dashboard folder keeps source code, tests, data folders, and exported
assets together.
