# 0004: Two engines for the disagreement enumerator, a grid and Z3, over one report

**Decision:** the disagreement enumerator has two engines, one report. `grid` runs two Python functions on every
case of a finite grid. `smt` asks Z3 for the differing cases of two encodings written as Z3 terms.

**Status:** accepted, 2026-11-17 (task law-7 of the DAG; to read by Mohamed). **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics-software-design/blob/8896e91b1a354a565bb0266a26b314329d82db98/shapes/decision-record.md). **Proposed in:** no proposal; the README's section Next, item 2.

## Context

- Decision 0001 puts Z3 on what a bounded check settles, and the README's Next section asks for a Z3 enumerator.
- Catala 1.3.0's own proof backend (built on 16 Nov., task law-6) reads 75 of 100 conditions of the family allowances and 4 of 32 of the withdrawal right.
- It has no command that compares two programs.
- The withdrawal-right encoding was compared with a second program by a grid of 148,256 cases (`retractation/enumerate.py`, branch `law-5-retractation`, 33 minutes).

## Decision

Both engines, behind one `Report`. The grid engine takes anything callable, so it scores a Catala encoding compiled to Python today. The
smt engine, where the encodings can be written as Z3 terms, proves an equal pair equal on the whole domain, which a grid cannot.

## Options

| Option | Consequences | Outcome |
|---|---|---|
| Grid and Z3, one report | the compiled Catala is scored now; an equal pair is proved equal where Z3 terms exist; two things to keep in step | chosen |
| Z3 only, through Catala's proof backend | one engine, a proof; the backend cannot compare two programs and reads only a part of the encodings | rejected until the backend does |
| Grid only | one engine; never says "equal on every case" | rejected: the sibling needs the stronger claim where it can be had |

## Consequences

- Good: the same cases come out of both engines on the toy pair (tested), so one can check the other.
- Bad: the `smt` engine needs the encodings rewritten as Z3 terms by hand; a translation from Catala is open work.
- To keep it true: the toy pair's tests, three mutations of the enumerator that each fail them, and a cross-check of the two engines on every new pair.

## See also

- [decisions/](README.md); [disagree/README.md](../disagree/README.md); [0001](0001-catala-for-the-statute-z3-for-bounded-checks-lean-for-theorems.md).
