"""Tests of the disagreement enumerator: it lists the differing cases of a known-different pair, finds none for an
equal pair, and lists every case of a pair that differs everywhere; both engines say the same."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import toy  # noqa: E402
from disagree import NO, YES, Report, grid, smt, undecided  # noqa: E402

pytest.importorskip("z3")


def by_case(report: Report) -> dict:
    return {(d.case["children"], d.case["income"]): (d.first, d.second) for d in report.disagreements}


def test_the_known_different_pair_lists_exactly_the_cases_it_differs_on():
    # reference and second differ on every case with 2 children and income <= 30 (yes against no), with 2 children
    # and income 31 or 32 (not decided against no): 33 cases. From 3 children both decide alike except for the
    # question of the band, 3 to 5 children by income 31 and 32: 6 cases.
    report = grid(toy.GRID, toy.reference, toy.second)
    cases = by_case(report)
    assert report.compared == 6 * 33
    assert len(cases) == 33 + 6
    assert cases[(2, 10)] == (YES, NO)
    assert cases[(2, 31)] == (undecided(toy.Q_REFERENCE), NO)
    assert cases[(4, 32)] == (undecided(toy.Q_REFERENCE), undecided(toy.Q_SECOND))
    assert (1, 10) not in cases and (3, 10) not in cases


def test_the_equal_pair_has_no_disagreement_on_the_grid():
    report = grid(toy.GRID, toy.reference, toy.reference_rewritten)
    assert report.agree and report.compared == 198 and report.errors == 0


def test_a_pair_that_differs_everywhere_lists_every_case():
    report = grid(toy.GRID, toy.reference, lambda case: NO if toy.reference(case) != NO else YES)
    assert len(report.disagreements) == report.compared == 198


def test_the_smt_engine_agrees_with_the_grid_on_the_known_different_pair():
    from_grid = by_case(grid(toy.GRID, toy.reference, toy.second))
    from_smt = smt(toy.SMT_DOMAINS, toy.reference_smt, toy.second_smt, questions=toy.QUESTIONS)
    assert from_smt.complete
    assert by_case(from_smt) == from_grid


def test_the_smt_engine_proves_an_equal_pair_equal_on_the_whole_domain():
    report = smt(toy.SMT_DOMAINS, toy.reference_smt, toy.reference_rewritten_smt, questions=toy.QUESTIONS)
    assert report.agree and report.complete


def test_the_smt_engine_lists_every_case_of_a_pair_that_differs_everywhere():
    import z3

    flipped = lambda t: z3.If(toy.reference_smt(t) == 0, 1, 0)  # noqa: E731
    report = smt(toy.SMT_DOMAINS, toy.reference_smt, flipped, questions=toy.QUESTIONS)
    assert report.complete and len(report.disagreements) == 6 * 33


def test_a_limit_stops_the_listing_and_says_it_is_not_complete():
    report = smt(toy.SMT_DOMAINS, toy.reference_smt, toy.second_smt, questions=toy.QUESTIONS, limit=5)
    assert len(report.disagreements) == 5 and not report.complete


def test_a_limit_met_exactly_at_the_last_case_is_complete():
    report = smt(toy.SMT_DOMAINS, toy.reference_smt, toy.second_smt, questions=toy.QUESTIONS, limit=39)
    assert len(report.disagreements) == 39 and report.complete


def test_two_different_questions_are_one_verdict_when_questions_are_not_compared():
    only_the_question = smt(toy.SMT_DOMAINS, toy.reference_smt, toy.second_smt, questions=toy.QUESTIONS, compare_questions=False)
    on_the_grid = grid(toy.GRID, toy.reference, toy.second, compare_questions=False)
    assert len(only_the_question.disagreements) == len(on_the_grid.disagreements) == 33  # the band of 3 to 5 children agrees
    assert by_case(only_the_question) == by_case(on_the_grid)


def test_an_encoding_that_raises_is_listed_and_counted_apart():
    def conflict(case):
        if case["children"] == 2 and case["income"] == 20:
            raise RuntimeError("conflict")
        return toy.reference(case)
    report = grid(toy.GRID, toy.reference, conflict)
    assert report.errors == 1
    assert by_case(report) == {(2, 20): (YES, "raises: RuntimeError")}


def test_both_encodings_raising_alike_is_counted_and_not_a_disagreement():
    def conflict(case):
        raise RuntimeError("conflict")
    report = grid({"children": range(2)}, conflict, conflict)
    assert report.errors == 2 and report.agree


def test_a_fact_domain_that_is_not_int_bool_or_enum_is_refused():
    with pytest.raises(ValueError):
        smt({"x": ("real", 0, 1)}, lambda t: 0, lambda t: 1)


def test_bool_and_enum_facts_are_decoded_in_the_cases():
    import z3

    def reference(t):
        return z3.If(t["resident"], 1, 0)

    def second(t):
        return z3.If(z3.And(t["resident"], t["status"] == 1), 1, 0)
    report = smt({"resident": ("bool",), "status": ("enum", ["single", "married", "widowed"])}, reference, second)
    cases = {(d.case["resident"], d.case["status"]) for d in report.disagreements}
    assert cases == {(True, "single"), (True, "widowed")}
