# Kyle's skills

Portable, opinionated agent skills for software design, implementation, investigation,
and review. Each skill is a standalone directory with a `SKILL.md` entrypoint and
supporting references where useful.

The collection combines personal skills originally developed for the `vdr` project
with adaptations of [poteto's](https://github.com/poteto) skills from
[pstack](https://github.com/cursor/plugins/tree/main/pstack). The versions here remove
project-specific paths, fixed model choices, and required agent tooling while
retaining the design opinions and evidence standards.

## Skills and provenance

“Personal” identifies the original VDR collection, generalized for use elsewhere.
“Poteto / pstack” identifies adapted upstream guidance, not an unchanged copy.

| Skill | Purpose | Origin | Original source |
| --- | --- | --- | --- |
| [go-architecture](go-architecture/SKILL.md) | Package boundaries, dependency direction, adapters, and wiring | Personal | VDR's `vdr-architecture` |
| [go-idioms](go-idioms/SKILL.md) | Small interfaces, composition, useful zero values, and deliberate APIs | Personal | VDR's `go-idioms` |
| [go-errors](go-errors/SKILL.md) | Error contracts, wrapping, inspection, and reporting ownership | Personal | VDR's `go-errors` |
| [go-concurrency](go-concurrency/SKILL.md) | Bounded work, cancellation, shared state, and explicit shutdown | Personal | VDR's `go-concurrency` |
| [message-driven-design](message-driven-design/SKILL.md) | Intent-bearing operations, encapsulation, and consumer contracts | Personal | VDR's `message-driven-design` |
| [tdd-workflow](tdd-workflow/SKILL.md) | Small test-first cycles that shape behavior and APIs | Personal | VDR's `tdd-workflow` |
| [verify-workflow](verify-workflow/SKILL.md) | Repository checks and behavioral evidence proportional to risk | Personal | VDR's `verify-workflow` |
| [blast-radius](blast-radius/SKILL.md) | Consequences beyond the diff and evidence for safety assumptions | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md) |
| [interrogate](interrogate/SKILL.md) | Adversarial review with investigated findings and a prioritized verdict | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md) |
| [how](how/SKILL.md) | Code walkthroughs covering runtime flow, ownership, and boundaries | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md) |
| [why](why/SKILL.md) | Historical design rationale with facts separated from inference | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md) |
| [benchmark-checklist](benchmark-checklist/SKILL.md) | Correctness, repeatability, and relevance of performance measurements | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md) |

## Use

Copy the complete directory for each desired skill into your agent's supported
skills location, keeping any references alongside `SKILL.md`. Installation paths
and invocation syntax depend on the agent.

Skills can be used independently. Related skills and delegation are optional;
the instructions adapt to the repository's conventions and available tools.

## Maintain

See the [changelog](CHANGELOG.md) for notable changes to the collection.

Keep descriptions specific enough for accurate discovery. Preserve source attribution
when adapting upstream material, and distinguish required constraints from preferred
defaults. Update this table when adding, removing, or renaming a skill.
