# Baseline

Step 5 of the review: the baselines the two proposed repositories are compared against, one for the method and one
for the model. Evidence is in [review](review.md).

**Shape:** [baseline](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/baseline.md)

## B1: Catala on its French encodings

The baseline for the method repository, where a person writes the encoding.

1. The language and compiler: [CatalaLang/catala](https://github.com/CatalaLang/catala), Apache-2.0, pushed 12 Nov. 2026.
2. The encodings: [CatalaLang/catala-examples](https://github.com/CatalaLang/catala-examples), folders
   `allocations_familiales`, `aides_logement`, `impot_revenu`, with their tests.
3. The check of the encoding: the proof backend in `compiler/verification/`, which sends to Z3 one verification
   condition per definition: no **empty error** (no rule applies) and no **conflict error** (two exceptions apply).
4. The words back: [CatalaLang/catala-explain](https://github.com/CatalaLang/catala-explain), explanation from the trace.
5. The reading at source: [CatalaLang/catleg](https://github.com/CatalaLang/catleg), French statutes through Légifrance.

## B2: DeonticBench's symbolic setting

The baseline for the AI-augmented repository, where a model writes the encoding.

1. [guangyaodou/DeonticBench](https://github.com/guangyaodou/DeonticBench) (Dou 2026a): a model reads the statute and the
   facts, writes Prolog, SWI-Prolog runs it; the answer is compared with the label and the audited reference program.
2. Splits: smoke (5 cases a domain) and hard (35 SARA numeric, 30 SARA binary, 78 housing), scored with bootstrap
   confidence intervals; best published hard score 44.4% on SARA numeric.
3. Fidelity, added from Vernie 2026: a SAT solver enumerates the cases where the model's program and the reference
   decide differently; a count of zero is the bar.

## Compared with what the review found

| Item | In B1 | In B2 | Fit |
|---|---|---|---|
| executable encoding beside the text | yes, literate Catala | Prolog, apart from the text | B1 matches; B2 in part |
| exceptions as a construct (default logic) | yes | encoded by hand in Prolog | B1 matches |
| a check of the encoding itself | Z3 proof of no empty and no conflict error | comparison with a reference program | both, in part |
| three-valued verdict with "not decided" | as an error only: an empty or conflict error at run time | no; labels are two-valued or numeric | in part; lacks |
| French law read at its source | yes for the examples; catleg reads Légifrance | no, US law only | B1 matches; B2 lacks |
| explanation without a model | trace explainer | Prolog trace | both |
| theorems about the statute | no | no | lacks |
| fidelity measured by decisions | tests only | against a reference program | in part |

## What B1 lacks

- A third answer that is an answer: where no rule applies Catala raises an empty error, which its proof backend treats
  as a bug to rule out. Open texture has no place as a verdict (Kouteili 2026; Hart 1961). The empty error is the
  natural carrier of "not decided by the text".
- Theorems about the statute beyond the absence of empty and conflict errors: monotonicity, absence of a cliff, equality with another
  encoding (MSR 2022 and lawlib 2026 aimed at this; neither is reachable).
- A measure of fidelity by decisions against a second encoding, such as OpenFisca's (Vernie 2026).

## What B2 lacks

- French law, and a third answer; models fail it (Kouteili 2026).
- A check that the model's prose matches what the solver did (Wang 2026b).

## How it is measured

- Method repository against B1: on one French provision, the count of properties stated and proved in Lean that Catala
  tests do not cover, and the count of disagreements found between the Catala and the Lean encodings by enumeration.
- AI-augmented repository against B2: on DeonticBench's hard splits, accuracy with its bootstrap interval, run as B2
  runs it and then with the method repository's checks in the loop; on the French provision, the count of edge cases
  where the model's encoding disagrees with B1's, which must reach zero before the encoding is accepted.
- Both counts are produced by programs and can be rerun from the repositories.

## The review is finished

The baselines are named, B1 Catala on its French encodings and B2 DeonticBench's symbolic setting, with code at the
links above; what comes next is the maintainer's choice of the repositories and of the first build step.
