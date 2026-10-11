# Changelog

Notable changes to this skill collection are recorded here. Changes remain under
Unreleased until a release is published.

## Unreleased

### Added

- Pre-commit hooks for formatting, Markdown linting, YAML/JSON validation,
  whitespace, merge-conflict markers, skill metadata, and local Markdown links.

- Seven portable skills from the personal collection: `go-architecture`,
  `go-idioms`, `go-errors`, `go-concurrency`, `message-driven-design`,
  `tdd-workflow`, and `verify-workflow`.
- Five adaptations of [poteto's pstack skills](https://github.com/cursor/plugins/tree/main/pstack):
  `blast-radius`, `interrogate`, `how`, `why`, and `benchmark-checklist`, with
  upstream attribution in each skill.
- Supporting references for architecture, Go idioms and concurrency, component
  contracts, TDD, historical confidence, and adversarial review.
- [README](README.md) with a skill inventory, provenance table, upstream links,
  and usage and maintenance guidance.
- This changelog.

### Changed

- Generalized project-specific guidance into independently usable skills.
- Replaced fixed repository paths and required verification tooling with guidance
  that follows the host project's conventions and available checks.
- Adapted pstack workflows to remove Cursor-specific tooling and fixed model
  choices, and to make delegation optional.
- Clarified mutable-state ownership, batch-operation semantics, cancellation and
  shutdown, error contracts, and the limits of verification evidence.
