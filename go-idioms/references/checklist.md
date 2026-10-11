# Idiomatic Go review checklist

Use when reviewing a type or API change. Explain intentional departures where
they matter rather than treating these defaults as mechanical bans.

- Each interface has a current consumer need and lives with that consumer unless
  it is a shared public contract. Its methods match what consumers actually use.
- Constructors return concrete types unless hiding implementations is an
  intentional part of the contract.
- Composition uses independent collaborators. Embedded method promotion is
  intentional; there is no simulated superclass or speculative type hierarchy.
- Plain data avoids accessor ceremony, while invariants and concurrent state
  remain protected.
- The zero value works where practical, and required initialization is explicit.
- Guard clauses keep the happy path readable.
- Exports are needed by actual callers; names avoid stutter and junk-drawer
  packages.
- Terminology stays consistent across the change.
- Formatting, vet, and relevant tests were run or their limitations reported.
