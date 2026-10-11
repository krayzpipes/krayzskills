# Composition without simulated inheritance

## Named collaborators

Named fields express a dependency without promoting all its methods into a
public API. Define the interface in the package consuming it.

```go
type Reader interface {
    ReadRecord() (Record, error)
}

type Importer struct {
    Source Reader
    Store  *Store
}
```

`Record` and `Store` stand for application types. Keep each collaborator useful
on its own; do not create a shared base solely to collect fields.

## Deliberate method promotion

Embedding can adapt an independently useful interface:

```go
type countingReader struct {
    io.Reader
    n int64
}

func (c *countingReader) Read(p []byte) (int, error) {
    n, err := c.Reader.Read(p)
    c.n += int64(n)
    return n, err
}
```

This adapter requires a non-nil `Reader` and is not safe for concurrent calls
without additional synchronization. Named fields would be preferable if other
promoted methods were unwanted. Avoid embedding a mutex in an exported type
merely for convenience: it exposes `Lock`/`Unlock` to callers, and values with
mutexes must not be copied after first use.

## Shared behavior

When unrelated types must be handled together, describe the consumer's needed
behavior in an interface. Do not unify their storage shapes just because some
fields overlap. Use exported methods for an interface that implementations in
other packages must satisfy.

Treat `Base*`/`Abstract*` names, superclass-style callbacks, and deep embedding
chains as prompts to reconsider the design. A named shared value representing
a real concept is still valid composition; a common field alone does not imply
inheritance.
