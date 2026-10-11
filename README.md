# Kyle's skills

Portable, opinionated agent skills for software design, implementation, investigation,
and review. Each skill is a standalone directory with a `SKILL.md` entrypoint and
supporting references where useful.

The collection combines personal skills
with adaptations of [poteto's](https://github.com/poteto) skills from
[pstack](https://github.com/cursor/plugins/tree/main/pstack). The versions here remove
project-specific paths, fixed model choices, and required agent tooling while
retaining the design opinions and evidence standards.

## Skills and provenance

“Personal” identifies original skills generalized for use across projects.
“Poteto / pstack” identifies adapted upstream guidance, not an unchanged copy.

| Skill                                                   | Purpose                                                                 | Origin          | Original source                                                                                          |
| ------------------------------------------------------- | ----------------------------------------------------------------------- | --------------- | -------------------------------------------------------------------------------------------------------- |
| [go-architecture](go-architecture/SKILL.md)             | Package boundaries, dependency direction, adapters, and wiring          | Personal        | Original skill                                                                                           |
| [go-idioms](go-idioms/SKILL.md)                         | Small interfaces, composition, useful zero values, and deliberate APIs  | Personal        | Original skill                                                                                           |
| [go-errors](go-errors/SKILL.md)                         | Error contracts, wrapping, inspection, and reporting ownership          | Personal        | Original skill                                                                                           |
| [go-concurrency](go-concurrency/SKILL.md)               | Bounded work, cancellation, shared state, and explicit shutdown         | Personal        | Original skill                                                                                           |
| [message-driven-design](message-driven-design/SKILL.md) | Intent-bearing operations, encapsulation, and consumer contracts        | Personal        | Original skill                                                                                           |
| [tdd-workflow](tdd-workflow/SKILL.md)                   | Small test-first cycles that shape behavior and APIs                    | Personal        | Original skill                                                                                           |
| [verify-workflow](verify-workflow/SKILL.md)             | Repository checks and behavioral evidence proportional to risk          | Personal        | Original skill                                                                                           |
| [blast-radius](blast-radius/SKILL.md)                   | Consequences beyond the diff and evidence for safety assumptions        | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/blast-radius/SKILL.md)        |
| [interrogate](interrogate/SKILL.md)                     | Adversarial review with investigated findings and a prioritized verdict | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/SKILL.md)         |
| [how](how/SKILL.md)                                     | Code walkthroughs covering runtime flow, ownership, and boundaries      | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/how/SKILL.md)                 |
| [why](why/SKILL.md)                                     | Historical design rationale with facts separated from inference         | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md)                 |
| [benchmark-checklist](benchmark-checklist/SKILL.md)     | Correctness, repeatability, and relevance of performance measurements   | Poteto / pstack | [Upstream skill](https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md) |

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

Install [pre-commit](https://pre-commit.com/) and enable the hooks in each checkout:

```sh
uv tool install pre-commit
pre-commit install
pre-commit run --all-files
```

The hooks format Markdown, YAML, and JSON with Prettier; lint Markdown; check
YAML/JSON syntax, whitespace, and merge-conflict markers; and validate skill
frontmatter against the [Agent Skills specification](https://agentskills.io/specification).
The skill validator also checks local Markdown links and images across tracked
and new, non-ignored files on every run, so deleting a referenced file is caught.
It checks file existence, not heading anchors or external URLs.

Pre-commit manages isolated tool environments and downloads dependencies on the
first run. If a formatter changes files, review and stage those changes before
committing again.
