# Local Issues

This folder stores local Markdown issues that are linked from `TODO.md`.

## Status Values

- `open`: Work is not started.
- `in_progress`: Work is currently being implemented.
- `done`: Code, docs, tests, and QCDS evidence are synchronized.
- `blocked`: Work cannot be closed in the current environment.

## Phase Values

- `00-inbox`: Newly captured work that still needs routing.
- `01-requirements`: Outcome, constraints, and acceptance criteria.
- `02-specification`: User-facing behavior and non-goals.
- `03-design`: Architecture, module boundaries, and trade-off decisions.
- `04-implementation`: Code and package changes.
- `05-test-validation`: Automated tests, runtime gate, and manual validation.
- `06-release`: Release checklist, QCDS, and distribution artifacts.

If a local issue is an exact duplicate, keep the issue file for traceability, mark it `done`, and record which issue absorbed the work.

## Issue Template

When creating a real issue, replace `status-value` with one of the status values above and convert `todo:` checklist placeholders into normal Markdown checkboxes.

```markdown
# 0000 Title

- Priority: P3
- Status: status-value
- Phase: 00-inbox
- Linked TODO: ../TODO.md

## Contract

Describe the expected outcome.

## Checklist

- todo: Implementation
- todo: Tests
- todo: Docs
- todo: QCDS evidence

## Evidence

- Pending.
```
