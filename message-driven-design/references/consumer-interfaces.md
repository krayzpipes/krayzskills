# Consumer-owned contracts

Read when defining an interface or deciding who owns it. Examples use Go's structural interfaces; apply the same principle through protocols, callable parameters, traits, or other language-appropriate contracts.

## Default ownership

The consumer knows what it needs. Declare its narrow interface near the code making the request instead of asking a producer to anticipate every caller. A second consumer with different needs can define its own interface without expanding the first one's dependency.

In Go, a producer can expose a concrete constructor and methods without importing its consumers' interfaces. Compose the components where implementations are selected:

```go
// In the package performing synchronization.
type Source interface {
    Fetch(ctx context.Context) ([]Entry, error)
}

type SnapshotWriter interface {
    // ReplaceAll replaces the complete snapshot atomically.
    // On error the previous snapshot remains available.
    ReplaceAll(ctx context.Context, entries []Entry) error
}

type Synchronizer struct {
    source Source
    writer SnapshotWriter
}

func New(source Source, writer SnapshotWriter) *Synchronizer {
    return &Synchronizer{source: source, writer: writer}
}

func (s *Synchronizer) Run(ctx context.Context) error {
    entries, err := s.source.Fetch(ctx)
    if err != nil {
        return err
    }
    return s.writer.ReplaceAll(ctx, entries)
}
```

`Entry` is a domain value shared through an appropriate contract location. It carries no HTTP response, database transaction, or adapter handle. A remote client, a fixture source, and a cache can satisfy `Source` if their behavior matches the consumer's needs. A memory writer and a database writer can satisfy `SnapshotWriter` only if they both provide its documented replacement and failure semantics.

The application composition point constructs the chosen source and writer and passes them to `New`. It may know their concrete types; the synchronizer does not need to. In languages that require explicit interface implementation, use a stable contract module or an adapter rather than creating dependency cycles to mimic Go's placement literally.

## Practical limits

- A standard ecosystem interface or deliberately shared public protocol can be the right owner. Keep it cohesive; do not duplicate it just to enforce physical consumer placement.
- Share domain values where dependency direction permits. Do not move all values into a global domain package by default.
- Carry cancellation or deadlines for operations that need them. In Go, use `context.Context` for cancellable work; do not add it reflexively to pure local queries.
- Expose only operations the consumer actually uses, but group methods that form one coherent contract. A separate interface for every method is not an end in itself.
- Return copies or immutable views where callers must not mutate component-owned state. Document ownership when copying is expensive; ensure nested references follow the same rule.
- An interface is useful when it expresses a stable boundary, permits substitution, or protects dependency direction. Concrete collaboration is reasonable for local helpers with no such need.
