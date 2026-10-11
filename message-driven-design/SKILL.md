---
name: message-driven-design
description: Design or review component collaboration through intent-bearing operations, narrow consumer contracts, encapsulated state, and replaceable implementations. Use when adding or reshaping component boundaries, interfaces, or adapters, especially where callers manipulate another component's internals or coordinate many small calls. Covers synchronous collaboration as well as messaging; does not prescribe queues, actors, or inheritance hierarchies.
---

# Message-Driven Design

Design around the requests components exchange before choosing their implementation types. A message here is an operation such as `Reserve`, `Fetch`, or `Publish`; an ordinary function or method call qualifies. Introduce queues, events, actors, or asynchronous delivery only when the task requires their semantics.

Prefer composition over inheritance for implementation reuse. Each component owns its mutable state and invariants; callers ask for behavior through a deliberate contract. Bind external implementations at an application composition point so callers depend on capabilities rather than adapter details. Follow the host project's language and conventions instead of imposing a package layout.

## Design the collaboration

1. **State the caller's intent and name its requests.** Start with the behavior the caller needs, including observable results and failure cases. Prefer names that express that intent. A query such as `Snapshot` or `Find` is a valid message; a getter is a problem when it exposes internals the caller must manipulate, not merely because of its name.

2. **Define the smallest contract the caller needs.** Prefer consumer-owned interfaces at meaningful substitution boundaries. Do not add interfaces around every concrete helper or widen one caller's contract to accommodate another. Read [consumer-interfaces.md](references/consumer-interfaces.md) when defining or placing a contract, particularly in Go.

3. **Keep invariant-preserving behavior with the state owner.** If callers must set fields and invoke several methods in a particular order, consider one operation that owns that sequence. Pass explicit arguments and return useful values. Immutable domain data, request records, copied snapshots, and read-only views are legitimate contract values. Avoid returning mutable references that let callers change internal state, including references hidden inside slices, maps, or nested objects.

4. **Specify the semantics before making calls coarser.** Write down whether an operation appends, upserts, replaces, or deletes; its ordering, atomicity, failure, and cancellation behavior; and any relevant ownership or idempotency rules. A batch request can reduce chatter without changing intent, but repeated `Add` calls and `ReplaceAll` are not interchangeable. One call does not itself guarantee atomicity.

5. **Wire interchangeable implementations at the boundary.** Callers should not construct a particular external client or inspect its concrete type to make the operation work. Use application startup, constructors, factories, or the existing dependency mechanism to select implementations. Substitution must preserve behavior, not merely compile against the same signature. Keep concrete implementation details inside the adapter.

## Review and refactor

Read [anti-patterns.md](references/anti-patterns.md) when reviewing a boundary or correcting exposed state, inherited internals, overgrown components, or chatty calls. Refactor the smallest boundary that solves the task; these preferences do not authorize an application-wide architectural rewrite.

For each proposed boundary, check whether the caller can express its intent without knowing storage, transport, or mutable internal structure; whether a second implementation can honor the same semantics; and whether the contract has introduced machinery without a useful substitution or ownership boundary. Verify relevant invariants and failure behavior with the project's existing validation approach.
