---
name: go-concurrency
description: Build and review Go goroutines, channels, worker pools, cancellation, and shared-state coordination with bounded concurrency and explicit shutdown. Use for concurrent Go components or reviews for races, leaks, deadlocks, and missing backpressure.
---

# Go Concurrency

Start with the simplest sequential design. Add concurrency for overlapping I/O,
an independent blocking loop, or a demonstrated throughput need. Make ownership,
limits, and shutdown visible before adding goroutines.

## Build a concurrent component

- Give each goroutine an owner, a reachable exit path, and a way for its owner
  to wait for it. Returning from a parent while its workers still run is not
  cancellation or cleanup.
- Pass `ctx context.Context` first through operations scoped to a request or
  job. Usually pass contexts through calls rather than storing them in structs.
  Lifecycle objects may store a cancel function and completion signal.
- Make blocking sends, receives, waits, and I/O interruptible where cancellation
  is required. A `for range` over a channel cannot observe cancellation while
  waiting for the next item; use a `select` or prove the producer always closes.
- Assign one channel-closing owner on the sending side. With multiple senders,
  a coordinator closes only after all senders finish. Receivers do not close
  data channels. A receive-only channel expresses that boundary to callers.
- Use `errgroup.WithContext` for related tasks that fail together when that
  dependency fits the repository; use `sync.WaitGroup` for joining tasks without
  first-error cancellation. All workers must observe the cancellation, and the
  coordinator must still wait. Avoid sleeps as coordination.
- Bound work before spawning goroutines. Use a fixed worker pool, admission
  semaphore, or suitable group limit. Bound queues as well as active workers;
  choose backpressure, rejection, or dropping intentionally.
- Concurrency limits and request-rate limits solve different problems. For
  external services, apply rate limits at the scope of the actual quota, such
  as per host, account, or tenant. A pool size alone does not bound requests per
  second. Long-lived workers need fair scheduling if more sources exist than
  available slots.
- Protect shared mutable state with a mutex, atomic operations suited to the
  invariant, or one owning goroutine. Channels do not make referenced maps or
  slices safe if a sender continues mutating them after handoff.

Read [references/patterns.md](references/patterns.md) for a cancellation-safe
worker pool, channel transform, or polling loop.

## Review and validate

Trace normal completion, cancellation, first failure, and a stalled downstream
consumer. Check channel closure order, blocked senders/receivers, shared memory,
and whether every started task is joined. Avoid a tight `select` with `default`
that spins, and remember that closed channels remain ready until removed from
multi-channel selects.

Prefer a reused timer or ticker for hot or controlled polling loops, and stop it
on shutdown. Do not claim `time.After` always leaks: modern Go can collect
unreferenced timers. Timer reset/drain behavior depends on the module's Go
version and timer mode; consult the relevant
[time documentation](https://pkg.go.dev/time#NewTimer) when changing it.

Run relevant tests with `go test -race` on a supported platform, broadening to
`go test -race ./...` for shared infrastructure changes. A clean run only covers
executed paths; also review ownership and exercise cancellation, blocked
consumers, and failure propagation. Report environment limits or unrun checks.
