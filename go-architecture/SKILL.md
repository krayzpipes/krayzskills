---
name: go-architecture
description: >-
  Design and review Go package boundaries, dependency direction, adapters, and
  application wiring. Use when deciding where a feature belongs, introducing an
  integration, or untangling package coupling. Not for routine Go syntax or
  naming, and not a mandate to reorganize an existing application.
---

# Go Architecture

Prefer a small core of application behavior with infrastructure at its edges.
Make dependency direction clear enough that a change in transport, persistence,
or upstream format does not require rewriting business rules.

## Choose boundaries before directories

1. Inspect the existing package graph, entrypoints, and conventions. Work with
   sound boundaries already present. Do not scaffold an entire layer hierarchy
   for a small feature or rename packages merely to match this skill.
2. Identify the business capability, its inputs and outputs, and the systems it
   touches. Group code by capability when unrelated features would otherwise
   share a large generic `service`, `data`, or `utils` package.
3. Put stable business values and rules inward; put HTTP, SQL, file formats, and
   vendor SDKs outward. Keep I/O out of pure rules. Prefer standard-library
   dependencies in the core, but evaluate useful libraries by coupling rather
   than imposing a blanket ban.
4. Define small interfaces where behavior is consumed when substitution or
   dependency inversion is useful. Application code should not need a concrete
   vendor client to express its work. Construct implementations at the
   composition boundary and inject them. Do not add an interface to every type.
5. Keep entrypoints focused on configuration, lifecycle, wiring, and delivery.
   Put reusable behavior in packages. Keep `internal/` for implementation code;
   expose public packages only when there is a real external consumer.

## Placement guide

These are responsibilities, not required package names. Combine them when
separate packages would add ceremony without protecting a boundary.

| Responsibility | Holds | Dependency direction |
|---|---|---|
| Business core | Values, invariants, pure decisions | No adapters or entrypoints |
| Application operations | Use cases, orchestration, transaction boundaries | Core and contracts it consumes |
| Integration adapters | Network, storage, vendor formats, conversion | Core values; implement consumed contracts |
| Delivery adapters | CLI, HTTP handlers, jobs, request/response mapping | Application operations and core values |
| Composition boundary | Configuration, concrete construction, lifecycle | Wires the above |

Separate read queries from write operations when their responsibilities,
performance, or consistency needs diverge. A read-only query does not by itself
justify a separate selector layer, event bus, or CQRS architecture.

## Boundary opinions

- Keep upstream wire shapes private to their adapter by default. Convert them
  into application values before they reach business code. Introduce distinct
  transport types when versioning, validation, or serialization would otherwise
  distort the core; serialization tags alone do not justify duplicating every
  struct.
- Validate format and decoding requirements at the input edge; enforce business
  invariants in the core so every input path receives the same rules.
- Persistence belongs behind the contract the application needs. Avoid a
  universal repository interface that exposes every backend capability.
- Keep adapters independent of each other unless one is deliberately composed
  from another. Break import cycles by correcting responsibilities, not by
  creating an unstructured shared package.
- Group a new business capability beside existing capabilities. Share code only
  when the semantics are actually shared, not because two structs look alike.
- Let transaction and consistency needs shape contracts. A method that promises
  atomic replacement must keep that promise across implementations.

Read [references/adapters.md](references/adapters.md) when implementing an
integration or reviewing its conversion and test boundaries.

## Review a change

Trace one use case from delivery through application behavior to its adapters.
Check that core rules remain testable without external systems, transport
details stop at their boundary, and wiring selects concrete dependencies. Run
the relevant package tests and build affected entrypoints. Report any deliberate
coupling and its reason; avoid proposing a wholesale rewrite for a local issue.
