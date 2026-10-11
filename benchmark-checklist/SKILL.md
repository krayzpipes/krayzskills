---
name: benchmark-checklist
description: >-
  Validate measured performance claims and comparisons by checking executed work,
  correctness, representative conditions, repeatability, and bottlenecks. Use
  before reporting a speedup, regression, or benchmark-based recommendation.
  Not a requirement to benchmark ordinary changes with no performance claim.
---

# Benchmark checklist

Measure the claim the user needs, with units and workload specified.

1. Inspect the measurement: timing boundaries, awaited completion, consumed results,
   and verified output. Count failures and retries; fast rejection is not throughput.
2. Compare representative conditions: optimized builds, versions, data, configuration,
   cache state, concurrency, and equivalent correctness guarantees. Distinguish
   default-configuration comparisons from tuned implementations.
3. Check system noise and load-generator saturation using available platform tools.
   Profile separately from reported timings to identify the limiting resource.
4. Repeat and interleave comparisons to reduce drift. Five runs per side is a
   useful starting point, not statistical proof. Report variation and use suitable
   analysis for close results; disclose inconclusive differences.
5. Sanity-check physical limits and the maximum benefit of the changed fraction.
   Relate microbenchmarks to the end-to-end workload before claiming user benefit.

A requested rough estimate may use one run if correctness and executed work are
checked and the limitation is stated. Adoption recommendations require stronger
evidence. Do not tune production systems or terminate unrelated processes merely
to improve measurement conditions.

Report the observed result, workload, units, run count, variability, and relevant
limitations. An unexplained bottleneck limits causal claims; it need not erase a
repeatable observation. Preserve commands and raw results when useful.

Adapted from poteto's [pstack benchmark-checklist](https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md).
