# Review criteria and judgment

Read when reviewing a change. Select relevant concerns rather than mechanically
applying every category.

- Correctness: trace inputs through decisions to outcomes. Examine important
  boundaries, failed operations, retries, repeated execution, and partial completion.
- Shared state: identify ownership and synchronization. Check shutdown, stale data,
  and whether concurrent actors can violate the same invariant.
- Compatibility: examine stored and transmitted values, downstream consumers, and
  deployment sequencing beyond symbol references.
- Security: trace an actual untrusted input to its effect. Inspect authorization,
  unsafe execution, and secret disclosure where the change touches those boundaries.
- Design: assess whether the fix addresses the responsible contract and whether
  added coupling or machinery serves a demonstrated need.
- Verification: check observable behavior and important integration paths. A test
  that duplicates the implementation is weak evidence.

Separate a defect's severity from confidence that it exists. Show why the trigger
is reachable; investigate a suspected security or correctness issue even if only
one reviewer raises it. Do not inflate preferences into blockers.

Use the broader task context when interpreting temporary code, staged migrations,
and constraints. Distinguish introduced problems from baseline problems. Avoid
dismissing a finding simply because the questioned pattern already exists elsewhere.

A useful verdict prioritizes what matters and explains material rejected claims.
No finding quota is needed. If a concern cannot be resolved, state the missing fact
and the cheapest check that would settle it.

Adapted from pstack's [rubric](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/rubric.md)
and [lead judgment](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/lead-judgment.md).
