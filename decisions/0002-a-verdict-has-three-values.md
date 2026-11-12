# 0002: A verdict has three values

**Decision:** the oracle answers yes, no, or not decided by the text; the third answer carries the question that only a
jurist can settle.

**Status:** accepted, 2026-11-12. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics-software-design/blob/8896e91b1a354a565bb0266a26b314329d82db98/shapes/decision-record.md). **Proposed in:** no proposal; argued in [evidence/statutes-as-code/against.md](../evidence/statutes-as-code/against.md).

## Context

The repository started from the hypothesis that a legal question is a yes/no question. The review keeps it only in
part. For a provision that is an algorithm in disguise the verdict is computable once the facts are fixed (Merigoux 2021).
Outside that core, open texture and discretion leave cases the text does not settle (Hart 1961; Zambrano 2025).

- Models answer those worst: 22 to 40% right where the answer is "not enough information" (Kouteili 2026).
- Catala already marks the place: where no rule applies it raises an empty error, and where two exceptions apply a
  conflict error ([baseline](../evidence/statutes-as-code/baseline.md)).

## Decision

A verdict is one of three values, as the [README](../README.md#what-a-verdict-is) draws it. Yes and no come with the trace of the encoding that computed them. Not decided by the
text comes with what made it so: no rule applied (Catala's empty error), two rules applied (a conflict error), or a term
the encoding left open on purpose. Each carries the article, the facts assumed and one question for a jurist that a
yes or no would close.

## Options

| Option | Consequences | Outcome |
|---|---|---|
| Three values | honest about open texture; the third value is the bridge to a person; a little more to encode | chosen |
| Two values, yes or no | the original hypothesis; forces a guess where the text is silent, which is where models fail most | rejected: the evidence against it is measured |
| A probability | a score per answer; no source of calibration for law, and a number reads as more certain than it is | rejected |

## Consequences

- Good: a client of the oracle, a person or an agent, never receives a guess dressed as a verdict.
- Good: the third value maps onto Catala's two errors, so B1 gives it for free on encoded scopes.
- Bad: an encoding can hide open texture by choosing a reading; only a reviewer of the encoding catches that.
- To keep it true: a test case for each encoded provision whose expected verdict is the third value.

## See also

- [decisions/](README.md); [0001](0001-catala-for-the-statute-z3-for-bounded-checks-lean-for-theorems.md) for the layers.
- [evidence/statutes-as-code/against.md](../evidence/statutes-as-code/against.md), against "law is a yes/no question".
