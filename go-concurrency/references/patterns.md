# Cancellation and bounded work

These are generic function examples. Add the standard-library imports they use;
the worker-pool example additionally uses `golang.org/x/sync/errgroup`. Match
dependencies and APIs to the module's supported Go version.

## Bounded worker pool with an owned producer

Keep the producer and consumers in the same cancellation scope. An externally
created producer does not automatically receive a group's derived context.

```go
func ProcessAll(ctx context.Context, items []string, workers int,
    process func(context.Context, string) error) error {
    if workers < 1 {
        return errors.New("workers must be positive")
    }
    if process == nil {
        return errors.New("process is required")
    }
    g, workCtx := errgroup.WithContext(ctx)
    jobs := make(chan string)

    g.Go(func() error {
        defer close(jobs) // sole sender owns closure
        for _, item := range items {
            select {
            case <-workCtx.Done():
                return workCtx.Err()
            case jobs <- item:
            }
        }
        return nil
    })

    for i := 0; i < workers; i++ {
        g.Go(func() error {
            for {
                select {
                case <-workCtx.Done():
                    return workCtx.Err()
                case item, ok := <-jobs:
                    if !ok {
                        return nil
                    }
                    if err := workCtx.Err(); err != nil {
                        return err
                    }
                    if err := process(workCtx, item); err != nil {
                        return fmt.Errorf("process %q: %w", item, err)
                    }
                }
            }
        })
    }
    if err := g.Wait(); err != nil {
        return err
    }
    return ctx.Err()
}
```

There are `workers + 1` goroutines and no unbounded queue. The callback must honor
context during blocking operations. Cancellation can race with selection of a
ready job; do not promise transactional prevention of all work after cancel.
The group's context is canceled by `Wait` even on success, so the final check
uses the original parent context. See the
[errgroup contract](https://pkg.go.dev/golang.org/x/sync/errgroup#WithContext).

## Channel transform

Run a stage inside its owner's group; the stage closes its output on all paths.
Both receiving and sending observe cancellation.

```go
func transform(ctx context.Context, in <-chan string, out chan<- string,
    convert func(string) string) error {
    defer close(out)
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case value, ok := <-in:
            if !ok {
                return nil
            }
            result := convert(value)
            select {
            case <-ctx.Done():
                return ctx.Err()
            case out <- result:
            }
        }
    }
}
```

`convert` is assumed to be bounded, nonblocking work. The owner must ensure this
stage is the only sender and that a consumer either drains `out` or cancels the
shared context. Never close `in` here.

## Polling with fixed delay

A timer started after each operation avoids overlapping calls and guarantees a
delay after completion. For adaptive backoff, cap the delay and add jitter when
many clients might retry together. Retrying is an application policy: distinguish
transient from permanent errors instead of swallowing every failure.

```go
func poll(ctx context.Context, interval time.Duration,
    once func(context.Context) error) error {
    if interval <= 0 {
        return errors.New("interval must be positive")
    }
    if once == nil {
        return errors.New("poll function is required")
    }
    timer := time.NewTimer(interval)
    defer timer.Stop()
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-timer.C:
        }
        if err := ctx.Err(); err != nil {
            return err
        }
        if err := once(ctx); err != nil {
            return fmt.Errorf("poll: %w", err)
        }
        timer.Reset(interval) // timer has fired and its channel was consumed
    }
}
```

Use a ticker when fixed cadence is intended; slow consumers can miss ticks.
Stopping a ticker does not close its channel, so cancellation needs its own
select branch. Use timeouts on underlying I/O; a context cannot interrupt a
function that ignores it.
