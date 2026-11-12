# 0001: Catala for the statute, Z3 for bounded checks, Lean for theorems about it

**Decision:** a statute is encoded in Catala; what can be checked over a bounded domain is checked by Z3; Lean holds
only the claims about a statute that quantify over all cases.

**Status:** accepted, 2026-11-12. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics-software-design/blob/8896e91b1a354a565bb0266a26b314329d82db98/shapes/decision-record.md). **Proposed in:** no proposal; argued in [evidence/statutes-as-code](../evidence/statutes-as-code/position.md).

## Context

The repository was proposed as a law oracle in Lean. The review found three facts that bear on the language:

- The verdict on a case is computed by running an encoding of the statute. Catala does that, with default logic as a
  construct for exceptions, French encodings already written, and explanations from the trace (Merigoux 2021; Catala 2026a; Catala 2026b).
- Catala already sends Z3 one condition per definition: no empty error and no conflict error (Catala 2026a). Whether two
  encodings decide alike can be checked by enumerating the cases where they differ (Vernie 2026).
- No Lean library of statutes with public code was found, and Lean has no default logic built in. What Lean adds is a
  proof of a property for every input: monotonicity, no cliff, two encodings equal (position, Q5).

## Decision

Three layers, each holding the job its tool does best ([README](../README.md#what-a-verdict-is)):

- The statute and its verdicts are Catala.
- A check over a bounded domain (consistency, coverage, disagreement between two encodings) is Z3, through Catala's
  proof backend or a solver query of our own.
- A claim that quantifies over every case is a Lean theorem, written as a claim in the shape of
  reader-ergonomics-blueprint. It is stated over a Lean model of the same provision, tied to the Catala encoding by
  differential testing on the cases Z3 enumerates.

## Options

| Option | Consequences | Outcome |
|---|---|---|
| Catala, Z3, then Lean | reuses the French encodings and the Z3 backend; Lean is kept for what only it does; two languages to keep in step | chosen |
| Lean for everything | one language and one kernel; every statute re-encoded by hand, exceptions encoded without default logic, no baseline to compare with | rejected: rebuilds B1 before adding anything, and the review found no prior Lean encoding to start from |
| Catala and Z3 only | the least work; no claim about all cases can be proved, only tested | rejected: the properties a reader of a statute cares about are of that kind |
| Prolog or ASP for the statute | the language of B2 and of most model papers; no French encodings, no proof backend | rejected for the method; kept for runs against B2 |

## Consequences

- Good: the first encodings exist; the comparison with B1 is direct, since B1 is the same language.
- Good: the order matches the family's tooling rule, a solver first and a proof assistant only for an unbounded claim.
- Bad: a Lean model can drift from the Catala encoding; only the differential tests tie them, and they are as good as
  the cases enumerated.
- Bad: Catala's compiler calls itself unstable; a version is pinned, and moving it is a changelog line.
- To keep it true: every Lean claim names the Catala scope it models, and the tests between the two run in CI.

## See also

- [decisions/](README.md), and [0002](0002-a-verdict-has-three-values.md) for what a verdict returns.
- [evidence/statutes-as-code/baseline.md](../evidence/statutes-as-code/baseline.md), B1 and B2.
- The claim shape: [reader-ergonomics-blueprint, shapes/claim.md](https://github.com/Tewf/reader-ergonomics-blueprint/blob/cab095257656b1bde1b202a433decf821b8876f9/shapes/claim.md).
