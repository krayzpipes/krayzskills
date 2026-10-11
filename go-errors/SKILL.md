---
name: go-errors
description: Design, wrap, inspect, and surface Go errors with meaningful context, errors.Is/errors.As, deliberate error contracts, and one reporting owner. Use when adding or reviewing error returns, validation guards, sentinels, typed errors, or error reporting paths.
---

# Go Errors

Make error chains useful to people and callers. Prefer short messages, preserved
causes, and explicit ownership of reporting.

## Construct and wrap

- Validate required inputs early. Name the problem directly: `errors.New("store
is required")` or `fmt.Errorf("invalid interval %s", interval)`.
- Wrap with `%w` when adding useful operation context and callers should retain
  access to the cause: `fmt.Errorf("load configuration: %w", err)`. Return an
  error unchanged when another wrapper adds no information. Do not wrap at
  every function boundary merely to repeat the call stack.
- Add distinct context once. Avoid chains such as `load: load: load` and prose
  such as `failed to ...: failed to ...`. Include useful identifiers where safe,
  but do not put credentials or sensitive payloads in errors.
- Wrapping exposes an error contract. If callers should not depend on a
  lower-level cause, translate it to your own documented error or deliberately
  format without `%w`. Do not hide causes by accident.
- Error messages normally start lowercase and omit trailing punctuation,
  preserving proper names and acronyms where appropriate.

## Choose the contract

- Default to plain descriptive errors for failures that only need reporting.
- Use a sentinel when callers need to identify a condition. Match with
  `errors.Is`, never by comparing message strings.
- Use a typed error when callers need structured details. Implement `Error()`
  and, if it wraps a cause, `Unwrap() error`; extract it with `errors.As`.
- Do not create sentinels or typed errors speculatively. Document public errors
  that consumers are expected to inspect. Preserve an established contract
  during refactoring.
- Avoid typed-nil errors: return literal `nil` on success rather than a nil
  pointer placed in an `error` interface.

## Report once and clean up

Return errors from inner layers. Assign reporting to the layer that owns the
outcome: a CLI entry point, request handler, job supervisor, or application
boundary. Avoid logging an error and returning it to a caller that logs it
again. A worker that handles a failure and continues can report it locally.
Keep process exit decisions at the executable boundary; return first so deferred
cleanup runs before `os.Exit`.

Recoverable failures return errors. Reserve panic for programmer invariants or
explicit must-style APIs, not invalid input or ordinary I/O failure.

Handle returned errors, including cleanup failures when they affect durability
or successful completion. Intentionally ignored errors need a nearby explanation
of why they cannot affect the result. A deferred `Close` is not automatically
safe to ignore for writes; preserve the primary error and propagate a relevant
cleanup failure if no earlier error occurred.

## Validate

Format changed Go files and run the repository's checks or `go vet ./...` from
the module root. Exercise affected failure paths, including wrapped matching,
invalid input, and cleanup where relevant. Inspect the diff for duplicate
reporting, lost causes, repeated prefixes, and accidental contract changes.
Report any validation that could not run.
