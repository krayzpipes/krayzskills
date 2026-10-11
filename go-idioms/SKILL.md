---
name: go-idioms
description: Write and review idiomatic Go types, interfaces, APIs, and package names, favoring consumer-defined interfaces, composition, useful zero values, and a small exported surface. Use when adding or refactoring Go types or reviewing their design.
---

# Go Idioms

Prefer concrete, readable Go over speculative abstractions. Apply these defaults
to the code being changed while respecting established public contracts.

## Interfaces and APIs

- Start with concrete types. Introduce an interface for a real consumer need:
  substitutable implementations, an isolation seam in tests, or a meaningful
  boundary. Do not generate an interface for every struct.
- Define small interfaces beside the consumer, describing only the behavior it
  uses. Prefer one to three methods; name a single-method interface for its
  behavior, often with an `-er` suffix. Avoid `I` prefixes and `Interface` suffixes.
- Accept interfaces where callers need substitution; return concrete types by
  default. Returning an interface is appropriate when hiding implementations is
  part of the API contract. Do not replace useful standard interfaces such as
  `io.Reader` with an application-specific duplicate.
- Keep exports deliberate. Do not export implementation details merely to make
  tests convenient.

## Composition

Use fields for collaborators and small interfaces for shared behavior. Do not
simulate inheritance with base structs, superclass hooks, or deep embedding
chains. A few repeated fields are cheaper than a speculative type hierarchy.

Prefer named fields; embedding deliberately promotes a method set and changes
the containing type's API. Use it only when that promotion is intended. Read
[references/composition.md](references/composition.md) when choosing between
embedding, delegation, and a shared interface.

## Everyday defaults

- Avoid getter/setter ceremony for plain data. Export a field when direct access
  is safe; use methods when they protect invariants, synchronize access, compute
  a value, or form a stable API. Do not export mutable state solely to avoid a
  method.
- Make the zero value useful where practical. If initialization is required,
  make that contract clear and return a useful error for invalid use rather
  than an accidental nil dereference. Constructors should establish real
  invariants, not exist out of habit.
- Return early for invalid inputs and errors; keep the happy path un-nested.
- Choose short, lowercase package names that explain a responsibility. Avoid
  junk-drawer names such as `util`, `common`, `helpers`, and `misc`, and avoid
  package/type stutter. Choose vocabulary from the current application's
  concepts and use one term consistently for each concept.

## Validate

Format changed Go files with `gofmt`. Use the repository's equivalent checks
when present; otherwise run `go vet ./...` and tests for affected packages from
the relevant module root. Apply
[references/checklist.md](references/checklist.md) for a type/API review. Report
checks that could not run and the reason; do not claim unperformed validation.
