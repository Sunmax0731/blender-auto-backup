# Backlog Triage

Generated for Issue 0008 / 0009 closure on 2026-05-14.

Updated on 2026-05-14 so `TODO.md`, local Issues, and Codex session records all expose explicit phase metadata. Issue 0010 was completed in the 04-implementation phase after adding the selectable backup destination layout. Issue 0013 was completed by adding Backup Preview / Dry Run and synchronizing post-MVP documentation. Issue 0014 tracks the v0.1.1 release publication.

## Phase Taxonomy

| Phase | Meaning |
| --- | --- |
| 00-inbox | Newly captured work that still needs routing. |
| 01-requirements | Outcome, constraints, and acceptance criteria. |
| 02-specification | User-facing behavior and non-goals. |
| 03-design | Architecture, module boundaries, and trade-off decisions. |
| 04-implementation | Code and package changes. |
| 05-test | Automated tests, runtime gate, and manual validation. |
| 06-release | Release checklist, QCDS, and distribution artifacts. |

## Phase TODO Source

`TODO.md` is organized into phase sections, and every checkbox line includes a `phase=...` token that matches the Codex Starter phase ids. Local Issues use a `Phase:` metadata line. Codex session history uses `phase` and `done` values so historical handoff records do not reappear as open untriaged work.

## Current Classification

| Phase | Items | Status |
| --- | --- | --- |
| 00-inbox | None | Done. No work item remains in the uncategorized phase. |
| 01-requirements | Repo creation, public remote setup, work branch, `README.md`, `AGENTS.md`, `SKILL.md`, Issue 0008, Issue 0009 | Done. No open requirement gaps remain. Issue 0009 is an exact duplicate of Issue 0008 and was closed through duplicate consolidation. |
| 02-specification | `docs/specification.md` | Done. MVP scope, non-goals, and error handling are documented. |
| 03-design | `docs/architecture.md` | Done. Module boundaries and the selected timer plus optional worker design are documented. |
| 04-implementation | Issues 0002, 0003, 0004, 0010, 0013 | Done. Background worker, glob rules, global default folder, selectable backup destination layout, and Backup Preview / Dry Run are implemented. |
| 05-test | Issues 0001, 0005, 0006, `docs/test-plan.md`, `docs/manual-test.md`, `dist/runtime-gate.json` | Done. Automated test flow, runtime gate diagnostics, Steam Blender detection, and Blender 5.1.1 runtime gate evidence are present. |
| 06-release | Issues 0007, 0011, 0012, 0014, `docs/release-checklist.md`, `docs/qcds-evaluation.md`, `docs/qcds-strict-metrics.json`, `dist/` artifacts | Done. Manifest validation, release evidence, screenshot documentation, and v0.1.1 package publication are synchronized. |

## Duplicate And Granularity Review

- Issue 0008 and Issue 0009 have the same title, context, acceptance criteria, priority, and QCDS scope.
- Issue 0008 is the retained primary issue for the triage work.
- Issue 0009 is resolved as a duplicate of Issue 0008.
- Issues 0001-0008, 0010, and 0013 are already issue-sized and do not need to be split or merged.

## Next Work

No open TODO or local Issue remains after Issue 0014 release publication. Future post-MVP candidates are documented in `docs/specification.md` with explicit priority and deferred status.
