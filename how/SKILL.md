---
name: how
description: >-
  Explain how an existing code subsystem works by tracing its runtime flow,
  state ownership, and boundaries. Use for code walkthroughs, onboarding, or
  understanding where a change fits. Historical motivation requires separate
  evidence; explanation alone does not authorize implementation or a redesign.
---

# How

Build an explanation someone can use to work in the subsystem. Organize around
behavior, not a narrated inventory of files.

## Investigate

State the question and scope. Begin with a concrete trigger, then follow calls,
data transformations, state changes, and results. Inspect both sides of important
boundaries; distinguish a declared interface from the implementation actually wired.

Identify the owners of mutable state, lifecycle, and error handling. Check tests
and configuration for behavior that source alone leaves ambiguous. Separate normal
operation from relevant failure, cancellation, and cleanup paths.

Handle narrow questions directly. For a broad investigation, divide exploration
into distinct angles when useful; use agents only when available and authorized.
Give them a shared question and request evidence with locations. Resolve conflicting
findings against the implementation before presenting them.

## Explain

Lead with what the subsystem does. Introduce only the concepts needed to follow
one representative flow. Cite important functions and files. Add a small diagram
when it clarifies ordering or ownership, and mention practical surprises and gaps.

For placement questions, explain existing responsibility and dependency direction.
Distinguish observed conventions from proposed improvements. Do not invent historical
intent, present unexecuted behavior as tested, or turn a walkthrough into a critique
unless requested. Related skills are optional.

Adapted from poteto's [pstack how](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md).
