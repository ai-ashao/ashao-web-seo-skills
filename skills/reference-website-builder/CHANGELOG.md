# Changelog

## 2.1.0

- Added collision-resistant `site-key` / `page-key` output isolation for high-fidelity multi-page work.
- Added deterministic computed-style, asset-discovery, state-diff, and responsive extraction recipes.
- Added an opt-in foreman pipeline for extract -> spec -> bounded parallel builder delivery.
- Added a mandatory high-fidelity pre-dispatch gate to reduce builder guessing.
- Strengthened equivalent-viewport visual QA, interaction-model verification, route preservation, and shared-foundation regression checks.
- Extended temporary asset manifests to schema v2 with page/site namespaces.
- Preserved the v2 lightweight default: ordinary `analyze`, `prototype`, and `adapt` work does not automatically incur the full reconstruction workflow.

## 2.0.0

- Consolidated competitor UI analysis and reference-site adaptation into one Skill.
- Added `analyze`, `prototype`, `adapt`, and `full` modes.
- Made lightweight execution the default; full artifact/provenance workflow is opt-in for high-fidelity/production migrations.
- Kept existing detailed references/templates for full mode without forcing them on ordinary prototype tasks.