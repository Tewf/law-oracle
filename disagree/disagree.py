"""List the input cases where two encodings of one provision decide differently.

An encoding is a function from the facts of a case to a verdict, and a verdict is one of three values (decision
0002): yes, no, or not decided by the text, which carries the question that would close it. Two encodings of one
provision, say a reference and a second, agree on a case when they return the same verdict. This module lists the
cases where they do not: the measure of Vernie 2026 for scoring a second encoding against a reference (README.md).

Two engines list the same thing, over the same inputs:

  grid  runs both encodings on every case of a finite grid, as Python functions, and lists the cases where the
        verdicts differ. It works on anything callable, a Catala encoding compiled to Python included (the grid
        of retractation/enumerate.py). It is exhaustive on the grid and silent outside it.
  smt   takes the two encodings as Z3 expressions over symbolic facts and asks the solver for a case where their
        verdicts differ, again and again, each time forbidding the case just found. When the solver says there
        is none, the pair agrees on every case of the domain, not only on a grid; the report says `complete`.
        If `limit` cases were listed first, it says it is not complete.

A case where one encoding raises (Catala's empty and conflict errors surface this way) is listed as a
disagreement when the other does not raise, and counted apart: the grid engine's `errors`. The smt engine has no
errors: an encoding there is total on its domain, by its form.

`python3 disagree/disagree.py` is a smoke check of the two engines on the toy pair: it exits 0 when the known-different
pair differs and the equal pair agrees, else 1.
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Mapping, Sequence

YES = ("yes",)
NO = ("no",)


def undecided(question: str) -> tuple:
    """Not decided by the text, with the question that would close it (decision 0002)."""
    return ("not decided", question)


Case = Mapping[str, Any]
Verdict = tuple


@dataclass
class Disagreement:
    case: dict
    first: Any   # a verdict, or "raises: <Exception>" for an encoding that raised
    second: Any


@dataclass
class Report:
    engine: str
    compared: int                 # cases run (grid) or the number of cases the solver listed (smt)
    disagreements: list[Disagreement] = field(default_factory=list)
    errors: int = 0               # grid: cases where at least one encoding raised
    complete: bool = True         # grid: always; smt: the solver ran out of disagreements before `limit`

    @property
    def agree(self) -> bool:
        return not self.disagreements


def _same(first: Verdict, second: Verdict, compare_questions: bool) -> bool:
    if not compare_questions and first[0] == "not decided" and second[0] == "not decided":
        return True
    return first == second


def grid(domains: Mapping[str, Sequence], first: Callable[[dict], Verdict], second: Callable[[dict], Verdict],
         compare_questions: bool = True) -> Report:
    """Every case of the product of the domains, in order, run through both encodings."""
    names = list(domains)
    report = Report(engine="grid", compared=0)
    for values in itertools.product(*(domains[name] for name in names)):
        case = dict(zip(names, values))
        report.compared += 1
        outcomes = []
        for encoding in (first, second):
            try:
                outcomes.append(encoding(dict(case)))
            except Exception as error:  # an empty or conflict error of the encoding: a finding, not a crash
                outcomes.append(f"raises: {type(error).__name__}")
        if any(isinstance(o, str) for o in outcomes):
            report.errors += 1
            if outcomes[0] != outcomes[1]:
                report.disagreements.append(Disagreement(case, outcomes[0], outcomes[1]))
        elif not _same(outcomes[0], outcomes[1], compare_questions):
            report.disagreements.append(Disagreement(case, outcomes[0], outcomes[1]))
    return report


# --- the smt engine ----------------------------------------------------------------------------------------------
NO_CODE, YES_CODE = 0, 1


def smt(domains: Mapping[str, tuple], first: Callable[[dict], Any], second: Callable[[dict], Any],
        questions: Sequence[str] = (), limit: int = 100_000, compare_questions: bool = True) -> Report:
    """Cases where two Z3 encodings differ, found by the solver and forbidden one by one.

    domains    name -> ("int", low, high) | ("bool",) | ("enum", [value, ...]); the facts, each in its range.
    first, second  take the dict of Z3 terms, one per fact, and return an integer term: 0 for no, 1 for yes, and
               2 + i for not decided by the text with the i-th of `questions`.
    """
    import z3

    terms: dict[str, Any] = {}
    solver = z3.Solver()
    for name, spec in domains.items():
        if spec[0] == "bool":
            terms[name] = z3.Bool(name)
        elif spec[0] == "int":
            terms[name] = z3.Int(name)
            solver.add(terms[name] >= spec[1], terms[name] <= spec[2])
        elif spec[0] == "enum":
            terms[name] = z3.Int(name)
            solver.add(terms[name] >= 0, terms[name] < len(spec[1]))
        else:
            raise ValueError(f"fact {name!r}: domain {spec!r} is not int, bool or enum")
    a, b = first(dict(terms)), second(dict(terms))
    if compare_questions or not questions:
        solver.add(a != b)
    else:  # two different questions are one verdict: fold every not-decided code to one
        fold = lambda t: z3.If(t >= 2, z3.IntVal(2), t)  # noqa: E731
        solver.add(fold(a) != fold(b))

    def label(code: int):
        if code == NO_CODE:
            return NO
        if code == YES_CODE:
            return YES
        return undecided(questions[code - 2] if 0 <= code - 2 < len(questions) else f"question {code - 2}")

    report = Report(engine="smt", compared=0)
    while report.compared < limit:
        if solver.check() != z3.sat:
            return report
        model = solver.model()
        case, block = {}, []
        for name, spec in domains.items():
            value = model.eval(terms[name], model_completion=True)
            if spec[0] == "bool":
                case[name] = z3.is_true(value)
            elif spec[0] == "int":
                case[name] = value.as_long()
            else:
                case[name] = spec[1][value.as_long()]
            block.append(terms[name] != value)
        va = model.eval(a, model_completion=True).as_long()
        vb = model.eval(b, model_completion=True).as_long()
        report.disagreements.append(Disagreement(case, label(va), label(vb)))
        report.compared += 1
        solver.add(z3.Or(block))
    report.complete = solver.check() != z3.sat  # `limit` reached: complete only if nothing is left
    return report


def main(argv: list[str] | None = None) -> int:
    """`python3 disagree/disagree.py` runs the toy pair of toy.py, as a smoke check of the engines."""
    import sys

    import toy

    different = smt(toy.SMT_DOMAINS, toy.reference_smt, toy.second_smt)
    equal = smt(toy.SMT_DOMAINS, toy.reference_smt, toy.reference_rewritten_smt)
    print(f"known-different pair: {len(different.disagreements)} cases, complete={different.complete}")
    print(f"equal pair: {len(equal.disagreements)} cases, complete={equal.complete}")
    return 1 if different.agree or not equal.agree else 0


if __name__ == "__main__":
    raise SystemExit(main())
