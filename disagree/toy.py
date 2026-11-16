"""A toy provision, written twice as a reference and as a second encoding, in plain Python and as Z3 terms.

Not a statute: a family benefit invented to test the enumerator, small enough that the differing cases are known by
hand. Facts: `children` under 20 (0 to 5) and `income` in hundreds of euros a month (0 to 32).

Reference:  yes when children >= 2 and income <= 30; not decided by the text when children >= 2 and 31 <= income <= 32
            (question: "is the ceiling inclusive of the first hundred above it?"); no otherwise.
Second:     the same, but from 3 children, and its question for the band is worded differently. Known to differ from
            the reference on every case with 2 children, and on the wording of the question where the band is reached.
Rewritten:  the reference's conditions written another way (a negated disjunction): equal to the reference everywhere.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from disagree import NO, YES, undecided  # noqa: E402

Q_REFERENCE = "is the ceiling inclusive of the first hundred above it?"
Q_SECOND = "does the ceiling of 3000 euros count after tax?"

GRID = {"children": range(0, 6), "income": range(0, 33)}
SMT_DOMAINS = {"children": ("int", 0, 5), "income": ("int", 0, 32)}
QUESTIONS = [Q_REFERENCE, Q_SECOND]


def reference(case):
    if case["children"] >= 2 and case["income"] <= 30:
        return YES
    if case["children"] >= 2 and case["income"] >= 31:
        return undecided(Q_REFERENCE)
    return NO


def second(case):
    if case["children"] >= 3 and case["income"] <= 30:
        return YES
    if case["children"] >= 3 and case["income"] >= 31:
        return undecided(Q_SECOND)
    return NO


def reference_rewritten(case):
    if not (case["children"] < 2 or case["income"] > 30):
        return YES
    if not (case["children"] < 2 or case["income"] < 31):
        return undecided(Q_REFERENCE)
    return NO


def _smt(children_at_least, question_code):
    import z3

    def encoding(t):
        return z3.If(z3.And(t["children"] >= children_at_least, t["income"] <= 30), 1,
                     z3.If(z3.And(t["children"] >= children_at_least, t["income"] >= 31), question_code, 0))
    return encoding


reference_smt = _smt(2, 2)   # code 2 is the first question
second_smt = _smt(3, 3)      # code 3 is the second question


def reference_rewritten_smt(t):
    import z3

    return z3.If(z3.Not(z3.Or(t["children"] < 2, t["income"] > 30)), 1,
                 z3.If(z3.Not(z3.Or(t["children"] < 2, t["income"] < 31)), 2, 0))
