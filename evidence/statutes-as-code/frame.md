# Frame: a law oracle, and what the field calls it

Step 1 of the review, read on 12 Nov. 2026. It states the problem, gives the field's names beside the practitioners',
and says whether the working name matches.

**Shape:** [frame](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/frame.md)

## The problem in one sentence

Given a statute and the facts of a case, return a verdict that a program has checked against a formal encoding of the
statute, and say in plain language why, with a model doing the translation both ways and never the deciding.

## What the field calls it

| Level | The field's name | First met in |
|---|---|---|
| the whole field | **computational law**; in AI, **AI and law** | Grimmelmann 2022; Prakken 2015 |
| writing a statute as an executable program | **rules as code**, RaC; earlier **legal knowledge-based systems**, LKBS | Merigoux 2021; Sergot 1986 |
| the formal languages for it | **legal DSL**: Catala, L4, Logical English, LegalRuleML, Blawx on s(CASP) | Merigoux 2021; Kowalski 2021 |
| the logic of exceptions | **default logic**, **defeasible logic**, **defeasible deontic logic**, DDL | Lawsky 2017; Horner 2025 |
| applying a statute to facts | **statutory reasoning**; with rules about duties, **deontic reasoning** | Holzenberger 2020; Dou 2026a |
| the yes/no question | **legal textual entailment** (COLIEE Task 4); **rule-conclusion** (LegalBench) | Kano 2024; Guha 2023 |
| a model writing the encoding | **autoformalization** of law, or **semantic parsing** of statutes | Chen 2025b; Jurayj 2025 |
| the encoding staying true to the text | **isomorphism** (one rule per provision, traceable); **faithfulness** | Bench-Capon 1992; Wang 2026b |
| saying the verdict back in words | **explanation from trace**; **verbalization** of edge cases | Catala 2026b; Vernie 2026 |
| why a rule cannot settle every case | **open texture**, **discretion**, **standards against rules** | Hart 1961; Lawsky 2017 |

- **Oracle**, here: a program that answers a question and whose answer is trusted because it was checked, as in
  testing; the field does not use the word for law.
- **Informalization**: the inverse of autoformalization, from the formal object back to prose. The legal literature
  says **explanation** or **verbalization**.

## What practice calls it

- **Rules as code**: governments' word (France's OpenFisca, New Zealand's Better Rules). The field's word is the same.
- **Legal engineering**, **compliance automation**: vendors' words for checking a plan against rules; the field says
  deontic reasoning or compliance checking.
- **Simulateur** (France): a public calculator of a benefit or a tax, often built on OpenFisca; the field calls it an
  executable encoding of the statute.

## Does the repository's name match?

- No repository exists yet. "Law oracle" is not the field's name; **rules as code** and **statutory reasoning** are.
  A name with "oracle" would be read as the testing sense, which is the intended sense. The maintainer decides.

## Sub-questions

| Question | Strand in review.md |
|---|---|
| Q1 What exists to write a statute as code, and who uses it? | Strand 1 |
| Q2 Is a legal question a yes/no question? | Strand 2 |
| Q3 Can a model translate a statute into logic faithfully, and how is that measured? | Strand 3 |
| Q4 Can the verdict be translated back into language? | Strand 4 |
| Q5 Has Lean, or another proof assistant, been used on law, and what does it add? | Strand 5 |

## Held elsewhere

- Autoformalization of mathematics into Lean, and its baseline (the audited blueprint):
  [reader-ergonomics-blueprint, evidence/autoformalization](https://github.com/Tewf/reader-ergonomics-blueprint/tree/master/evidence/autoformalization).
  That review left law out on purpose; this one picks it up.
- How to stop a search: [ai-augmented-data-gathering](https://github.com/Tewf/ai-augmented-data-gathering).
