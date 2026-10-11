# Boundary smells and focused refactors

Read when reviewing a component's message surface or fixing one of these smells.

## Inherited internals

Smell: a base class or embedded implementation exposes state that subclasses or callers must manipulate to change behavior. Swapping an implementation requires reproducing its internal layout or lifecycle.

Prefer independent implementations of a behavior contract. Share implementation through composed collaborators or private helpers. In Go, embedding is composition, but promoted fields and methods can still leak a contract; do not embed merely to imitate a subtype tree. Respect an existing framework's inheritance requirements without spreading that coupling into application logic.

## Overgrown components

Smell: one component coordinates unrelated workflows, knows several external systems, and owns unrelated mutable state. Changes to one capability repeatedly disturb the others.

Split around coherent responsibilities and invariant ownership. External systems often justify separate adapters; independent workflows can justify separate coordinators. Separating reads and writes is useful when their needs differ, but a component may reasonably own both operations on the same state. Do not prescribe CQRS or extra package layers solely because both exist.

## Callers operating another component's parts

Smell:

```go
publisher.Pending = batch
publisher.Validate()
publisher.Transport.Send(publisher.Pending)
publisher.MarkSent()
```

The caller must know the owner's state machine and failure rules. Move the invariant-sensitive sequence behind an operation such as `Publish(ctx, batch)` with explicit input and documented results. Decide whether retries can send duplicates and how partial failure is reported; hiding the sequence does not solve those semantics automatically.

Returning data is not inherently a leak. A copied `Status` value or immutable snapshot supports legitimate queries. Returning an internal map or writable buffer gives the caller access to component-owned mutable state even if the field itself is private. Shallow copies do not protect mutable nested values.

## Chatty calls with ambiguous intent

Smell: a caller makes many fine-grained calls to complete a single logical operation, leaving invariants or partial failure handling distributed across the boundary.

Choose a coarse operation only after preserving the intended semantics:

| Caller intent                                            | Suitable operation     | Contract to specify                                                  |
| -------------------------------------------------------- | ---------------------- | -------------------------------------------------------------------- |
| Add several new entries while retaining existing entries | `AddBatch(entries)`    | Duplicate handling and all-or-nothing versus per-item results        |
| Insert or update several entries by identity             | `UpsertBatch(entries)` | Identity, update rules, conflict handling, and failure results       |
| Set the complete snapshot to exactly these entries       | `ReplaceAll(entries)`  | Removal of absent entries, empty input, atomicity, and failure state |

Replacing an `Add` loop with `ReplaceAll` can silently delete existing entries. A single batch call may still apply partially; document and test the actual guarantee. Repeated small calls are acceptable when each is an independent action, streaming is necessary, or the caller intentionally needs per-item control.

## False interchangeability

Smell: adapters satisfy the same signature but require callers to inspect concrete types, handle different transport errors, or depend on undocumented consistency and ordering behavior.

Define the behavior callers rely on and normalize implementation details at the adapter boundary. Keep genuinely different capabilities explicit rather than promising a uniform contract that implementations cannot honor. Validate replacement implementations against meaningful observable contract behavior, including important failure cases.
