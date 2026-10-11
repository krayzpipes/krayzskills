# Confidence in historical explanations

Read before reporting a design rationale.

| Evidence                                           | Appropriate claim                                                |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| A contemporaneous source explicitly gives a reason | Report that recorded reason with its citation                    |
| Several independent records converge               | Describe the supported interpretation and its evidence           |
| Context suggests a reason without documenting it   | Label the inference and explain the reasoning                    |
| Several explanations fit sparse records            | Present useful hypotheses without choosing an unsupported winner |
| Relevant searches cannot establish a reason        | Say it remains unknown and identify the search limits            |

Working code establishes behavior, not its author's motivation. A regression test
can reveal a protected case without explaining the original requirement. Several
documents repeating one assertion are not independent corroboration.

Keep conflicting records visible. An introduction-time constraint may have expired;
a recent change may not explain the original design. Failure to find a rationale
does not establish that none existed.

Do not assign numerical confidence without a basis or require an invented gap when
the record answers a narrow question completely.

Adapted from pstack's [epistemics guidance](https://github.com/cursor/plugins/blob/main/pstack/skills/why/references/epistemics.md).
