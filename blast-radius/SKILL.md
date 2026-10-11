---
name: blast-radius
description: >-
  Investigate what a proposed code change could break beyond its diff, and test
  the assumptions that make it safe. Use for change-impact analysis, compatibility
  concerns, or a small diff with hidden consequences. Not a substitute for the
  repository's ordinary verification checks.
---

# Blast radius

Find consequences that searching for callers misses. Treat safety as a claim
requiring evidence, not a convincing narrative.

1. Establish the exact change, intended behavior, and comparison base. Inspect
   relevant callers and dependencies, including pinned versions and local patches.
2. Identify the critical assumptions: ownership, ordering, lifetime, compatibility,
   or failure behavior. There may be several; do not force one universal explanation.
3. Follow indirect contracts: serialized data, database schemas, configuration,
   generated clients, other languages, deployment order, caches, and teardown.
   Investigate plausible paths rather than listing every hypothetical hazard.
4. Test the most consequential assumptions through actual affected code, using
   existing tests or a disposable local reproducer. Preserve user data and stay
   within the review's scope. Mark blocked checks as unresolved.
5. Report confirmed breakage, cleared concerns, and remaining uncertainty separately.
   Attach locations, triggering conditions, consequences, and executed evidence.

Distinguish source inspection, execution-path reasoning, a passing reproducer,
and observed application behavior. Each establishes different limits. A clean
search does not prove absence across external consumers.

Finish with the cheapest useful regression check. This review does not authorize
fixes, migrations, or deployment. Other skills are optional.

Adapted from poteto's [pstack blast-radius](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md).
