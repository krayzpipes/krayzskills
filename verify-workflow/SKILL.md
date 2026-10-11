---
name: verify-workflow
description: Verify a code change using the repository's own checks and a risk-based behavioral validation plan. Use after implementation, before a requested commit, or when asked to confirm a change works. Discover existing tooling, diagnose failures honestly, and report executed checks and limits. Does not implement CI infrastructure or mandate a particular test runner.
---

# Verify Workflow

Verification should establish that the changed behavior works and the surrounding project still meets its requirements. A green command is evidence only for what it actually checks.

## Discover the project contract

Read applicable repository instructions and inspect the changed files. Find the established commands in contribution docs, task files, package manifests, test configuration, hooks, and CI. Prefer those commands over inventing a parallel workflow. Do not assume any particular language, task runner, hook manager, or directory layout.

Understand what aggregate commands do before running them: some format files, fetch dependencies, launch services, or deploy. Use local, bounded checks for verification; running a deployment is not an implied verification step. Protect unrelated edits when a formatter or generator writes files.

Choose checks proportional to the change while honoring explicit project requirements. Documentation or a mechanical low-risk edit does not need an invented test suite. A behavior change needs evidence that can distinguish the old behavior from the requested behavior.

## Execute a useful validation plan

Start with targeted feedback, then run the required broader checks once the implementation is ready:

- **Formatting and static checks:** Use established formatting, linting, type checking, and static analysis for the affected code. Inspect any automatic rewrites and rerun affected checks.
- **Tests:** Run the relevant test suite, including a regression for the changed behavior when useful, then the required project suite or aggregate check. Confirm filters selected actual tests rather than yielding an empty successful run.
- **Build:** Build affected deliverables when compilation, bundling, generated interfaces, or packaging are not covered by the other checks.
- **Behavior:** Exercise changed public behavior at the appropriate level: command output and exit status, application interaction, service response, or library contract. Prefer local fixtures and controlled dependencies. Verify the result, not just process success.
- **Risk-specific checks:** For concurrency changes, use the ecosystem's supported race or thread tooling and tests that exercise relevant interleavings. For persistence changes, test migration and compatibility against disposable data. For UI changes, inspect rendering and interaction. For performance claims, use representative repeatable measurements.

Run existing hooks when the project requires them for the requested workflow, using its installed tooling. Do not install a hook manager or rewrite configuration merely because another repository used one. Note unavailable required checks and what existing checks do or do not cover.

Use live dependencies only when needed to validate the changed integration and within the authorized scope. A local stub can prove handling of a response; it cannot prove that a live service still accepts the request. Avoid presenting one as evidence for the other.

## Handle failures without hiding them

Fix failures introduced by the change and rerun the failed check plus any checks invalidated by the fix. Use the formatter for formatting errors; investigate diagnostic and test failures in their source context.

Do not skip tests, remove useful assertions, suppress diagnostics, or narrow a required check simply to obtain green. Correct an outdated expectation when the intended behavior truly changed, explaining why it is now wrong and preserving meaningful coverage.

For suspected pre-existing failures, gather evidence with safe comparison or isolated reproduction. Preserve the user's work. Clearly distinguish an observed baseline failure from an unproven suspicion.

When a dependency, permission, environment, or flaky failure blocks a check, exhaust reasonable local alternatives and report the remaining limit. Do not repeatedly rerun until a lucky pass or label the change fully verified when a material required check remains unresolved.

## Finish with evidence

Review the final diff for unintended files, generated churn, debug output, and whitespace problems. If verification changed files, ensure the results apply to the final state. Avoid repeating successful checks unless subsequent edits or unresolved concerns invalidate their evidence.

Report what changed, the significant commands or behavioral checks that ran, their outcomes, and any remaining limits. Keep optional omitted checks distinct from required blocked checks. A requested commit or publication remains a separate action whose authorization comes from the user, not this skill.
