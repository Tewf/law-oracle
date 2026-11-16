# The disagreement enumerator

Lists the input cases where two encodings of one provision decide differently. It is the measure that scores a second
encoding against a reference (Vernie 2026). The sibling [ai-augmented-law-oracle](https://github.com/Tewf/ai-augmented-law-oracle)
needs it to accept or refuse a translation by decisions.

**Shape:** [folder](https://github.com/Tewf/reader-ergonomics/blob/65e42472e2d4cbfd994c2a86e95a47e5dc7301ca/shapes/readme-and-folder.md).

## Contents

| File | What it is |
|---|---|
| [disagree.py](disagree.py) | the two engines and the report |
| [toy.py](toy.py) | an invented provision, written twice and rewritten once, in Python and as Z3 terms |
| [test_disagree.py](test_disagree.py) | the 13 tests |

## Example

```sh
conda activate law-oracle            # z3-solver and pytest are in this env
python3 -m pytest disagree -q
python3 disagree/disagree.py         # smoke check on the toy pair
```
```console
.............                                                            [100%]
13 passed in 0.15s
known-different pair: 39 cases, complete=True
equal pair: 0 cases, complete=True
```

From Python, with a verdict that is `YES`, `NO` or `undecided(question)` (decision 0002):

```python
from disagree import grid, smt
report = grid(domains, reference, second)                       # run both encodings on every case of a finite grid
report = smt(domains, reference_z3, second_z3, questions=[...])  # ask Z3 for the differing cases
report.disagreements    # [Disagreement(case, first, second), ...]
report.agree, report.complete   # no disagreement; and the listing is whole
```

## Two engines

| Engine | Takes | Says | Limit |
|---|---|---|---|
| `grid` | two Python functions, a Catala encoding compiled to Python included, and a finite grid of facts | every case of the grid where they differ, and the cases where an encoding raised (`errors`) | silent outside the grid |
| `smt` | two encodings written as Z3 terms over facts in a range, and a `limit` | every case of the domain where they differ; `agree` and `complete` together mean equal on the whole domain, not on a grid | the encodings must be written as Z3 terms; a `limit` met early gives `complete = False` |

Both compare the question that a "not decided by the text" verdict carries, unless told not to
(`compare_questions=False`): two encodings that leave the same case open for different reasons differ by default.

## What it does not do

- **It does not translate Catala to Z3.** Catala 1.3.0's proof backend reads only part of an encoding.
  It solved 75 of 100 conditions of the family allowances and 4 of 32 of the withdrawal right (`evidence/baseline-runs.md`, branch `law-6-proof`).
  So the `smt` engine takes encodings written as Z3 terms, and the `grid` engine takes the compiled Python.
- **It does not say which encoding is right.** A disagreement is a case for a jurist, with both verdicts and, where one
  is "not decided", its question.

## What the tests show

The toy provision is small enough that the differing cases are known by hand. The known-different pair differs on 39 of
198 cases, the equal pair on none, and a pair that differs everywhere on all 198. The two engines return the same set.
Three mutations of the enumerator each fail the suite: comparing nothing, asking for equal verdicts, and blocking a case
by a conjunction.

## See also

[The repository's README](../README.md), section Next; [decision 0004](../decisions/0004-two-engines-for-the-disagreement-enumerator.md).
