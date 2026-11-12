# Position

Step 4 of the review. What is known, what was not found, and what the proposed repositories ask. Each "not found" is
a statement about these searches, not about the world. Terms are in [frame](frame.md).

**Shape:** [position](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/position.md)

## Known

- Writing a statute as executable code is a forty-year field with running tools: Prolog (Sergot 1986), Catala
  (Merigoux 2021; Catala 2026a), Logical English (Kowalski 2021), Blawx on s(CASP) (Morris 2023), OpenFisca (OpenFisca 2026).
- Catala already holds French encodings, an SMT check of its exceptions, a mechanised core and trace explanations (Catala 2026a to 2026c).
- A model writing Prolog from a statute, executed by a solver, beats a model answering alone, and still fails more than
  half of the hard cases (Jurayj 2025; Dou 2026a; Kordjamshidi 2026).
- Fidelity can be measured by decisions, not by form: enumerate the cases where two encodings disagree (Vernie 2026).
- The answer must have three values ([decision 0002](../../decisions/0002-a-verdict-has-three-values.md); [README](../../README.md#what-a-verdict-is)); "not decided by the text" is the one models get wrong (Kouteili 2026).
- Explanations from the trace exist without a model (Catala 2026b); a model's own explanation can launder a solver's
  authority (Wang 2026b).

## Not found in these searches

- A Lean library of statutes with public code (G5, G8, F4, F10). Two projects were described, neither reachable (MSR 2022; lawlib 2026).
- A study comparing Lean with Catala or Prolog on the same statute (F4, F10).
- A model translating French statutes read at their source (LEGI) into Catala, scored on decisions rather than syntax
  (F5, G14). Lorenzo 2025 scores French tax law on syntax and code metrics; its data was not located.
- A round trip measured: statute to formal to prose, the prose re-formalised and compared by decisions (F9).
- Proof of production use of Catala by an administration (G15).

## The questions

| Question | Answer from the evidence | Grade |
|---|---|---|
| Q1 What exists to write a statute as code? | Catala is the best-evidenced, OpenFisca the most adopted; both are open source | measured, descriptive |
| Q2 Is a legal question yes/no? | For rules that are algorithms in disguise, yes once facts are fixed; in general three-valued, with open texture and discretion outside | measured for the third value; convention for open texture |
| Q3 Can a model translate faithfully? | Not reliably: at best under half of hard cases; fidelity is measurable by decisional disagreement | measured, secondary |
| Q4 Can the verdict be said back? | Yes from the trace, without a model; a model's prose needs a check | measured, descriptive |
| Q5 What does Lean add? | Theorems about a statute (properties, equality of two encodings), not the verdict, which execution already gives | convention; no comparison found |

## What this repository asks

- For one French provision read at its source, can a Lean statement of a property (monotonicity, no cliff, two
  encodings equal) be proved where Catala can only test it, and does the proof find what the tests missed?
- Does accepting a model's encoding only when it agrees with a reference encoding on every edge case a solver
  enumerates catch the errors that syntax and test cases miss?
- Is a three-valued verdict, whose third value becomes the question for a jurist, answered better by solver plus
  model than by the model alone?
- Does an explanation that survives a round trip (re-formalised by a second model and compared by decisions) mislead less than one that does not?

## What the shapes must decide

- The encoding language: Catala for the statute, Lean for theorems about it, or Lean for both. The evidence favours
  Catala for the statute (default logic built in, French encodings exist) and Lean only where a property is claimed.
- The verdict contract: three values, and what each carries (the article read, the facts assumed, the trace).
- The unit of work: one legal point as one claim topic (reader-ergonomics-blueprint, `shapes/claim.md`), whose Lean
  line names a declaration and whose audit has two columns.
- Where the facts come from: given by the person, never extracted by a model without a check.
