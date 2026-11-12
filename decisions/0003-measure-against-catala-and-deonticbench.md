# 0003: Measure against Catala and DeonticBench, with the model in a sibling repository

**Decision:** this repository is measured against Catala on its French encodings (B1), and the model's translation lives in
a sibling repository, ai-augmented-law-oracle, measured against DeonticBench (B2) and judged by this one's checks.

**Status:** accepted, 2026-11-12. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics-software-design/blob/8896e91b1a354a565bb0266a26b314329d82db98/shapes/decision-record.md). **Proposed in:** no proposal; argued in [evidence/statutes-as-code/baseline.md](../evidence/statutes-as-code/baseline.md).

## Context

The family's pattern is a repository for the method and a sibling where a model does part of the work, the second judged
by the first. The review named one baseline for each: Catala with its French encodings, where a person writes the
encoding, and DeonticBench's symbolic setting, where a model writes Prolog and a solver decides (Dou 2026a).

## Decision

Two public repositories. This one holds the method: the three-valued verdict, the encodings, the checks, the Lean
claims and the review. ai-augmented-law-oracle holds the model's translation in both directions, statute to code and
verdict to words. It accepts an encoding only when it disagrees with a reference encoding on no enumerated case. The
first step runs both baselines as they are, before any code of our own, and records the numbers here.

## Options

| Option | Consequences | Outcome |
|---|---|---|
| Two repositories, B1 and B2 | the method stands without a model; the model is judged by a program it cannot change | chosen |
| A strand inside reader-ergonomics-blueprint | no new repository; widens a repository whose own review left law out, and Catala has no place there | rejected |
| Names after the field, rules-as-code | easier to find; promises law as code in general and is crowded by government repositories | rejected; the field's name is in the description |
| B1 only, the model later | nothing paid runs; the model side waits with no measure | rejected: B2 runs on the local model at no cost |

## Consequences

- Good: the two baselines are other people's code, so the comparison is not of our own making.
- Bad: two repositories to keep in step; the sibling pins this one by commit.
- Bad: B2 is United States law; the French comparison waits for a model run on B1's encodings.
- To keep it true: the baseline numbers are produced by a script and stored with the command that made them.

## See also

- [decisions/](README.md); [evidence/statutes-as-code/baseline.md](../evidence/statutes-as-code/baseline.md).
- [Tewf/ai-augmented-law-oracle](https://github.com/Tewf/ai-augmented-law-oracle).
