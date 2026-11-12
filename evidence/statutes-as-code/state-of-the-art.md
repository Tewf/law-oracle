# State of the art

Step 3 of the review. For each question, the best evidence, kept apart from the practice most adopted. Upper bounds
(what was achieved) are kept apart from limits (what was shown not to work). Sources are in [review](review.md).

**Shape:** [state of the art](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/state-of-the-art.md)

## Q1 What exists to write a statute as code, and who uses it?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Merigoux 2021 | Catala: literate code beside the text, default logic, a proved compiler core, a bug found in an official implementation | measured, descriptive |
| Upper bound | Catala 2026a | French housing aids, family allowances, income tax and more encoded, with a Z3 check that no definition is empty or in conflict, and trace explanations | measured, descriptive |
| Limit | Catala 2026a | the compiler is called unstable by its own README | measured, descriptive |
| Most adopted | OpenFisca 2026 | the engine under French and other public simulators | measured, descriptive |

## Q2 Is a legal question a yes/no question?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Kouteili 2026 | three answers are needed: yes, no, not enough information; models fail the third (22 to 40%) | measured, secondary |
| Upper bound | Merigoux 2021 | for statutes that are algorithms in disguise, the verdict is computable once facts are fixed | measured, descriptive |
| Limit | Zambrano 2025; Hart 1961 | outcomes depend on the judge; open texture leaves a penumbra | measured; convention |
| Most adopted | Kano 2024 | COLIEE Task 4 asks yes/no entailment from given articles | measured |

## Q3 Can a model translate a statute into logic faithfully, and how is that measured?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Dou 2026a | DeonticBench: model to Prolog, executed, scored against audited reference programs; best 44.4% on hard SARA numeric | measured, secondary |
| Upper bound | Jurayj 2025 | translating the statute once, ahead of time, then cases with retrieved exemplars, improves SARA markedly | measured, secondary |
| Limit | Wang 2026b; Vernie 2026 | scope laundering; structural likeness does not predict decisional agreement | measured, secondary |
| Most adopted | none found | no production system has a model write the encoding | not found |

## Q4 Can the verdict be translated back into language?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Vernie 2026 | disagreements between encodings verbalised into scenarios an expert can act on | measured, secondary |
| Upper bound | Catala 2026b | explanations generated from the execution trace, no model in the loop | measured, descriptive |
| Limit | Wang 2026b | a model's explanation can claim a solver result that does not exist | measured, secondary |
| Most adopted | Catala 2026b | trace-based explanation, as a prototype for public forms | measured, descriptive |

## Q5 Has Lean, or another proof assistant, been used on law, and what does it add?

| Record | Holder | What it says | Grade |
|---|---|---|---|
| Best evidence | Merigoux 2021; Catala 2026c | proofs about the language (F*, Rocq) and checks about an encoding (Z3), not theorems about a statute | measured, descriptive |
| Upper bound | MSR 2022 | Lean used on French family benefits and US civil procedure; no code reachable | measured, descriptive |
| Limit | none found | no study compares Lean with Catala or Prolog on the same statute | not found |
| Most adopted | none found | no Lean library of statutes is in use | not found |
