---
name: tdd-workflow
description: Design new behavior and component APIs with small test-first Red → Green → Refactor cycles. Use when TDD is requested, an API is undecided, or behavior is hard to test. Focus on observable behavior through public boundaries rather than coverage targets or private implementation details. Does not describe the full repository verification process.
---

# TDD Workflow

Use the test as the first caller of a component. An awkward test is feedback about the API, dependencies, or responsibilities. Coverage is a side effect; the purpose is to design behavior that is easy to use and change.

## Choose the boundary

Test through a supported public surface: an exported function, module API, service operation, command, or UI interaction. Public here means available to the component's consumers, not necessarily published outside the application.

Do not bypass private access, expose test-only wrappers, or couple assertions to private helpers. When an internal rule feels hard to test, exercise it through its existing public surface or extract a cohesive component with an API useful to real callers. Do not expand production APIs solely to make a test possible.

Follow the project's test framework, placement, and naming conventions. In Go, prefer external test packages (`package foo_test`) that use exported identifiers. In other languages, use the corresponding module or component boundary.

## Run the cycle

Discover the smallest existing test command that exercises the behavior. Use that command for fast feedback during the cycle; broader verification follows when the change is ready.

1. **Red:** Write one test for one missing behavior before implementing it. Choose names, arguments, and outputs from the caller's perspective. Run it and observe failure for the intended reason. A missing API can be a valid first failure; an invalid import, unavailable dependency, or broken fixture is not evidence of missing behavior. Resolve setup problems and rerun.
2. **Green:** Write the least production code that makes the test pass. Avoid unused options, speculative abstractions, and features no test or requirement asks for. Run the test and the nearby suite.
3. **Refactor:** Improve names, remove duplication, and clarify responsibilities in code and tests while preserving behavior. Rerun the affected suite. If nothing needs improving, move on.
4. Repeat for the next behavior. Grow cases one at a time; each new case must demonstrate its own red step before its implementation.

For a bug, start with a regression that reproduces the observed failure. For existing untested behavior, characterization tests can establish a baseline, but describe that work accurately: tests written after implementation are not a completed test-first cycle.

When the user explicitly requests TDD, preserve the sequence and report the red and green evidence. If tests cannot run, resolve available setup issues or explain the limit; do not claim to have observed a cycle that was never executed.

## Keep tests informative

- Assert outputs, errors, and meaningful externally visible effects. Avoid reproducing the implementation or asserting incidental ordering and call counts.
- Prefer small concrete fakes at dependency boundaries over large mocking frameworks or mocks of every internal call. Keep established tooling when it serves the project well.
- Make time, randomness, I/O, and remote dependencies controllable when they affect the behavior. Use realistic minimal fixtures and seed state through supported APIs.
- Use parameterized or table-driven tests when cases share one behavior. Keep unrelated scenarios separate so failures explain what broke.
- Test relevant boundary and failure cases, not every line. Include the interaction level needed to catch integration mistakes that isolated tests cannot reveal.

Trivial forwarding, generated mappings, and assembly of already-tested pieces usually need no dedicated unit tests. Entry points still need behavioral coverage when argument parsing, exit status, output, or startup logic can fail. Base the choice on actual behavior and risk, not the filename or coverage percentage.

Read [references/worked-example.md](references/worked-example.md) when a concrete cycle or private-helper design decision would clarify the task. Use the project's verification workflow after the feature cycles; this skill does not require another skill to be installed.
