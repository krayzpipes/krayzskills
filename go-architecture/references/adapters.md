# Adapter patterns

Use separate decode, conversion, and I/O functions when that makes contracts
easier to test. They may share a file in a small adapter; `wire.go`, `map.go`,
and `client.go` are optional organizational names.

## Input conversion

Keep external field names, optionality, and encoding in private wire types.
Decode the upstream format, reject malformed required input, and map to core
values. Return contextual errors that identify the failing item or operation
without including secrets or entire payloads.

Expose a parse function when file imports or focused tests need it. Otherwise
test through the adapter's public behavior without widening its API for tests.
Use representative, sanitized fixtures for meaningful upstream cases: valid
input, missing required fields, and an unsupported or malformed value. Keep
unknown-field handling compatible with the upstream contract rather than
rejecting every additive change.

Business validity belongs in core constructors or rules. For example, decoding
a timestamp is adapter work; deciding whether an item has expired is a business
rule. Avoid implementing the same business rule independently in each adapter.

## Consumer contract

An application package might declare:

```go
type CatalogFetcher interface {
    Fetch(ctx context.Context) ([]Item, error)
}

type CatalogReplacer interface {
    ReplaceAll(ctx context.Context, items []Item) error
}
```

Concrete HTTP and database adapters satisfy these contracts without requiring
the application to import them. Locate shared core values in an appropriate
core package if separate packages need them. Wiring creates the adapters and
passes them to the application operation.

Specify what `ReplaceAll` means: whether failure leaves old data intact, how
concurrent readers observe the change, and who owns the passed values. Do not
claim two adapters are substitutable merely because their signatures match.

## Ownership and lifecycle

Copy mutable slices, maps, and nested values when ownership crosses a boundary
that promises isolation. A shallow struct copy is insufficient for nested
mutable data. Avoid unnecessary copies where ownership is explicitly transferred.

Make timeouts and cancellation configurable at the I/O boundary. Let the
composition boundary own shared client and database lifetimes; an adapter
should not close a dependency it merely borrows.

Test conversion without network access, HTTP behavior with a local test server,
and database semantics with an appropriate isolated backend when needed. A fake
is useful for orchestration but cannot prove a real adapter's transaction or
protocol behavior.
