"""Run the compiled encoding on a grid of cases and compare it with a second program.

Catala's proof backend (Z3) proves that no input reaches an empty or a conflict error. Until Catala is built with
it, this script checks the same two errors on a bounded grid. It also checks three outputs against `reference`,
a second program written by the same author, branch for branch, from the same reading: the right, the end of the
period, and the verdict on a withdrawal sent on each of 14 days. It checks a property of this encoding that
does not depend on the second program: from the conclusion on, a later sending day never turns a lost right back
into one in time (`monotone`). A
case where the two disagree, where the property fails, or where Catala raises, is printed; the exit status is 1 if
there is one, else 0.

  python3 retractation/enumerate.py [STEP]     from the repository root, after `clerk build`; STEP days
                                               between conclusion dates, 3 by default
"""
import datetime as dt
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "_targets/python/libcatala"), str(ROOT / "_targets/python")]

import importlib  # noqa: E402
import types  # noqa: E402

import catala_runtime as rt  # noqa: E402

# The generated module imports the standard library relatively, and the generated __init__.py files do not run, so
# one package is made by hand whose path holds both folders.
_pkg = types.ModuleType("catala_build")
_pkg.__path__ = [str(ROOT / "_targets/python/libcatala"), str(ROOT / "_targets/python/retractation")]
sys.modules["catala_build"] = _pkg
R = importlib.import_module("catala_build.Retractation_distance")

HOLIDAYS = [dt.date(2027, 12, 25), dt.date(2028, 1, 1), dt.date(2028, 4, 17), dt.date(2028, 5, 1),
            dt.date(2028, 12, 25), dt.date(2029, 1, 1), dt.date(2029, 4, 2), dt.date(2029, 5, 1)]
CONTRACTS = ["PrestationDeServices", "FournitureArticleL2214", "VenteDeBiens"]
DELIVERIES = ["UnSeulBien", "PlusieursBiensLivresSeparement", "BienEnLotsOuPiecesEchelonnes",
              "LivraisonRegulierePendantUnePeriode"]
RECEPTIONS = [(), (3,), (3, 10), (10, 3)]
# Information: before the conclusion, never, or (days after the conclusion it is supplied, days later it is received).
INFOS = ["avant", "jamais"] + [(k, lag) for k in (1, 3, 5, 10, 14, 16, 17, 20, 100, 360, 368, 372, 380, 400, 500)
                               for lag in (0, 2)]
# L. 221-28: none; a case of type (3°); dated cases inside the period (day 6) and after it (day 30, a probe day);
# a case of type with a dated one.
EXCLUSIONS = [(), (("Al3BienPersonnalise", None),), (("Al5BienDescelleHygiene", 6),),
              (("Al13ContenuNumeriqueCommence", 30),),
              (("Al9EnregistrementOuLogicielDescelle", 6), ("Al6BienMelangeIndissociablement", 30)),
              (("Al3BienPersonnalise", None), ("Al5BienDescelleHygiene", 6))]
# Days after the conclusion on which a withdrawal is sent, to probe `dans_le_delai`.
PROBES = [-1, 0, 2, 3, 5, 6, 7, 16, 17, 18, 19, 30, 380, 400]


# --- the second reading, in plain Python -------------------------------------------------------------------------
def next_working_day(day):
    """L. 221-19, 3°, and regulation 1182/71, art. 3(4)."""
    while day.weekday() >= 5 or day in HOLIDAYS:
        day += dt.timedelta(days=1)
    return day


def plus_twelve_months(day):
    """Regulation 1182/71, art. 3(2)(c): same day number, or the month's last day."""
    year = day.year + 1
    for d in (day.day, 30, 29, 28):
        try:
            return dt.date(year, day.month, d)
        except ValueError:
            continue


def reference(contract, delivery, conclusion, receptions, complete, info, exclusions):
    """Return (right, started, end) where end is ('none',) | ('notstarted',) | ('date', d) | ('open', question)."""
    by_type = any(d is None for _, d in exclusions)
    started = contract != "VenteDeBiens" or (len(receptions) > 0 and (
        complete or delivery in ("UnSeulBien", "LivraisonRegulierePendantUnePeriode")))
    if contract == "VenteDeBiens" and receptions:
        start = min(receptions) if delivery == "LivraisonRegulierePendantUnePeriode" else max(receptions)
    else:
        start = conclusion
    initial = next_working_day(start + dt.timedelta(days=14))
    if by_type:
        return False, started, ("none",)
    if not started:
        return True, started, ("notstarted",)
    if info == "avant":
        return True, started, ("date", initial)
    extended = next_working_day(plus_twelve_months(initial))
    if info == "jamais":
        return True, started, ("date", extended)
    supplied, received = info
    window = next_working_day(plus_twelve_months(start))
    if supplied <= start:
        return True, started, ("date", extended)
    after_info = next_working_day(received + dt.timedelta(days=14))
    bounds = (min(after_info, extended), max(after_info, extended))
    if supplied <= initial:
        return True, started, ("open", "InformationFournieAvantLaProlongation", *bounds)
    if supplied > extended:
        return True, started, ("date", extended)
    if supplied <= window:
        return True, started, ("date", after_info)
    return True, started, ("open", "InformationFournieApresDouzeMoisDuDepart", *bounds)


def reference_sent(sent, conclusion, receptions, contract, delivery, exclusions, end):
    """The verdict on a withdrawal sent on `sent`: ('Oui',) | ('Non',) | ('NonDecide', question)."""
    if any(d is None for _, d in exclusions) or sent < conclusion:
        return ("Non",)
    if end[0] == "date" and sent > end[1]:
        return ("Non",)
    if end[0] == "open" and sent > end[3]:
        return ("Non",)
    events = [d for _, d in exclusions if d is not None]
    if any(d < sent for d in events):
        return ("Non",)
    if any(d == sent for d in events):
        return ("NonDecide", "PerteDuDroitLeJourDeLEnvoi")
    if end[0] == "notstarted":
        return ("NonDecide", "EnvoiAvantLOuvertureDuDelai")
    start = conclusion
    if contract == "VenteDeBiens":
        start = min(receptions) if delivery == "LivraisonRegulierePendantUnePeriode" else max(receptions)
    if contract == "VenteDeBiens" and sent < start:
        return ("NonDecide", "EnvoiAvantLOuvertureDuDelai")
    if end[0] == "open":
        return ("Oui",) if sent <= end[2] else ("NonDecide", end[1])
    return ("Oui",) if sent <= end[1] else ("Non",)


# --- the Catala encoding ------------------------------------------------------------------------------------------
def cdate(d):
    return rt.Date(d.year, d.month, d.day)


def to_py(d):
    return dt.date(*map(int, str(d).strip("|").split("-")))


def run_catala(contract, delivery, conclusion, receptions, complete, info, exclusions):
    code = R.InformationSurLeDroit.Code
    if info == "avant":
        information = R.InformationSurLeDroit(code.FournieAvantLaConclusion, rt.Unit())
    elif info == "jamais":
        information = R.InformationSurLeDroit(code.JamaisFournie, rt.Unit())
    else:
        information = R.InformationSurLeDroit(code.FournieApresLaConclusion, R.InformationTardive(
            fournie_le=cdate(info[0]), recue_le=cdate(info[1])))
    cases = [R.CasL22128(getattr(R.CasL22128.Code, c), rt.Unit() if d is None else cdate(d))
             for c, d in exclusions]
    result = R.delai_de_retractation(R.DelaiDeRetractationIn(
        type_de_contrat_in=R.TypeDeContrat(getattr(R.TypeDeContrat.Code, contract), rt.Unit()),
        date_de_conclusion_in=cdate(conclusion),
        modalite_de_livraison_in=R.ModaliteDeLivraison(getattr(R.ModaliteDeLivraison.Code, delivery), rt.Unit()),
        dates_de_reception_in=rt.Array([cdate(d) for d in receptions]),
        reception_complete_in=rt.Bool(complete) if hasattr(rt, "Bool") else complete,
        information_in=information,
        cas_l221_28_in=rt.Array(cases),
        jours_feries_ou_chomes_in=rt.Array([cdate(d) for d in HOLIDAYS]),
    ))
    end = result.fin_du_delai
    name = end.code.name
    decoded = {"PasDeDroit": ("none",), "PasEncoreCommence": ("notstarted",)}.get(name)
    if decoded is None:
        if name == "Le":
            decoded = ("date", to_py(end.payload))
        else:
            f = end.payload
            decoded = ("open", f.question.code.name, to_py(f.au_plus_tot), to_py(f.au_plus_tard))
    return bool(result.droit_de_retractation), result.dans_le_delai, decoded


def decode_verdict(v):
    return (v.code.name,) if v.code.name != "NonDecide" else ("NonDecide", v.payload.code.name)


RANK = {"before": 0, "Oui": 1, "after": 2, "Non": 3}


def monotone(verdicts):
    """From the conclusion on, the verdicts run: undecided, in time, undecided, late; none goes back.

    A property of this encoding: a later sending day can lose the right, never regain it. It holds because the one
    question about a sending day that is too early is rendered undecided; a strict a contrario reading of L. 221-18,
    2°, would give `Non` then `Oui`, a right not yet open rather than one regained. Undecided before the first `Oui`
    ranks 0, after it 2.
    """
    ranks, seen_yes = [], False
    for v in verdicts:
        if v[0] == "Oui":
            seen_yes = True
        ranks.append(RANK[v[0]] if v[0] != "NonDecide" else RANK["after" if seen_yes else "before"])
    return all(a <= b for a, b in zip(ranks, ranks[1:]))


def main():
    step = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    conclusions = [dt.date(2027, 12, 1) + dt.timedelta(days=k) for k in range(0, 122, step)]
    counts = {"cases": 0, "verdicts": 0, "errors": 0, "disagreements": 0, "not monotone": 0}
    errors = {}
    for conclusion, contract, delivery, rec, complete, info_kind, excl in itertools.product(
            conclusions, CONTRACTS, DELIVERIES, RECEPTIONS, (True, False), INFOS, EXCLUSIONS):
        if not complete and (contract != "VenteDeBiens" or not rec):
            continue  # completeness only matters for goods already partly received
        if contract != "VenteDeBiens" and (delivery != "UnSeulBien" or rec != (3,)):
            continue  # delivery does not enter a service contract
        if delivery == "UnSeulBien" and len(rec) > 1:
            continue
        if contract != "VenteDeBiens":
            rec = ()
        receptions = [conclusion + dt.timedelta(days=k) for k in rec]
        info = info_kind if isinstance(info_kind, str) else (
            conclusion + dt.timedelta(days=info_kind[0]), conclusion + dt.timedelta(days=info_kind[0] + info_kind[1]))
        after_delivery = {"Al5BienDescelleHygiene", "Al6BienMelangeIndissociablement",
                          "Al9EnregistrementOuLogicielDescelle"}
        if any(c in after_delivery for c, _ in excl) and not rec:
            continue  # the encoding asserts that these events follow a reception
        if any(c == "Al13ContenuNumeriqueCommence" for c, _ in excl) and contract != "FournitureArticleL2214":
            continue  # 13° is asserted for digital content only
        exclusions = tuple((c, None if k is None else conclusion + dt.timedelta(days=k)) for c, k in excl)
        args = (contract, delivery, conclusion, receptions, complete, info, exclusions)
        counts["cases"] += 1
        try:
            right, sent_fn, end = run_catala(*args)
            got_sent = [decode_verdict(sent_fn(cdate(conclusion + dt.timedelta(days=k)))) for k in PROBES]
        except rt.CatalaError as e:
            counts["errors"] += 1
            errors.setdefault(type(e).__name__, []).append(args)
            continue
        want_right, _, want_end = reference(*args)
        want_sent = [reference_sent(conclusion + dt.timedelta(days=k), conclusion, receptions, contract, delivery,
                                    exclusions, want_end) for k in PROBES]
        counts["verdicts"] += len(PROBES)
        if not monotone([v for k, v in zip(PROBES, got_sent) if k >= 0]):
            counts["not monotone"] += 1
            if counts["not monotone"] <= 5:
                print("not monotone:", args, got_sent)
        if (right, end, got_sent) != (want_right, want_end, want_sent):
            counts["disagreements"] += 1
            if counts["disagreements"] <= 10:
                print("disagree:", args, "catala", right, end, got_sent, "reference", want_right, want_end, want_sent)
    for name, cases in errors.items():
        print(f"{name}: {len(cases)} cases, first {cases[0]}")
    print(counts)
    sys.exit(1 if counts["errors"] or counts["disagreements"] or counts["not monotone"] else 0)


if __name__ == "__main__":
    main()
