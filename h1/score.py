"""Score a model's module against the reference by decisions, on a grid of children and dates.

Both modules are compiled to Python by Catala (`clerk build`); the grid runs `prestations_familiales(...).droit_ouvert`
on each case of a grid and compares the verdicts, the way `disagree/disagree.py`'s grid engine does. A case where one side
raises (an empty or a conflict error of Catala, or a missing value) counts as a disagreement unless both raise.

  python3 h1/score.py TREE REFERENCE_MODULE MODEL_MODULE...     TREE is the clerk tree whose _targets/python holds the builds
"""
from __future__ import annotations

import datetime as dt
import importlib
import itertools
import sys
import types
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from disagree import disagree  # noqa: E402

DATES = [dt.date(y, m, 1) for y in (2019, 2021, 2023, 2025) for m in (1, 7)] + [dt.date(2026, 11, 17)]
RESIDENCES = ["Metropole", "Mayotte", "Guadeloupe"]
SITUATIONS = ["Avant", "Pendant", "Apres"]
PAYS = [0, 400, 700, 800, 900, 1000, 1200, 1500]       # euros a month; the ceiling is near 55 % of the SMIC times 169
AGES_YEARS = [3, 10, 15, 16, 17, 18, 19, 20, 21, 25]    # the age the child has on the date, to the day: birthday = date - age
AGE_OFFSETS = [-1, 0, 1]                                # days either side of the birthday, for the boundary


def load(tree: Path, module: str):
    """The compiled module `module`, with the runtime and the Smic and France modules on its path."""
    py = tree / "_targets" / "python"
    pkg = types.ModuleType(f"catala_build_{module}")
    pkg.__path__ = [str(py / "libcatala"), str(py / "smic"), str(py / module.lower().replace("_", "-"))]
    sys.modules[pkg.__name__] = pkg
    sys.path.insert(0, str(py / "libcatala"))
    return importlib.import_module(f"{pkg.__name__}.{module}")


def birthday(date: dt.date, years: int, offset: int) -> dt.date:
    try:
        born = date.replace(year=date.year - years)
    except ValueError:
        born = dt.date(date.year - years, 2, 28)
    return born + dt.timedelta(days=offset)


def decide(mod, france, rt, case: dict) -> tuple:
    d = case["date"]
    kid = mod.Enfant(identifiant=rt.Integer(1), obligation_scolaire=mod.SituationObligationScolaire(
                         getattr(mod.SituationObligationScolaire.Code, case["situation"]), rt.Unit()),
                     remuneration_mensuelle=rt.Money(str(case["pay"])), date_de_naissance=rt.Date(*(lambda b: (b.year, b.month, b.day))(case["born"])),
                     prise_en_charge=mod.PriseEnCharge(mod.PriseEnCharge.Code.EffectiveEtPermanente, rt.Unit()),
                     a_deja_ouvert_droit_aux_allocations_familiales=True,
                     beneficie_titre_personnel_aide_personnelle_logement=False)
    inputs = mod.PrestationsFamilialesIn(date_courante_in=rt.Date(d.year, d.month, d.day),
                                         residence_in=france.Collectivite(getattr(france.Collectivite.Code, case["residence"]), rt.Unit()))
    out = mod.prestations_familiales(inputs)
    return ("yes",) if out.droit_ouvert(kid) else ("no",)


def grid():
    for d, res, sit, pay, years, off in itertools.product(DATES, RESIDENCES, SITUATIONS, PAYS, AGES_YEARS, AGE_OFFSETS):
        yield {"date": d, "residence": res, "situation": sit, "pay": pay, "born": birthday(d, years, off), "years": years, "offset": off}


def compare(tree: Path, reference: str, model: str, sample: int | None = None) -> dict:
    """Run both modules over the grid; return the agreement and the first disagreements."""
    refm, modm = load(tree, reference), load(tree, model)
    rt = sys.modules[refm.__name__.split(".")[0]].__dict__.get("rt") or importlib.import_module("catala_runtime")
    france_r = importlib.import_module(refm.__name__.rsplit(".", 1)[0] + ".France")
    france_m = importlib.import_module(modm.__name__.rsplit(".", 1)[0] + ".France")
    total = agree = errors = 0
    diffs = []
    for case in grid():
        total += 1
        verdicts = []
        for mod, france in ((refm, france_r), (modm, france_m)):
            try:
                verdicts.append(decide(mod, france, rt, case))
            except Exception as exc:                      # empty or conflict error, or an unsupported value
                verdicts.append(("raises", type(exc).__name__))
        if verdicts[0] == verdicts[1]:
            agree += 1
        else:
            errors += verdicts[1][0] == "raises"
            if len(diffs) < 20:
                diffs.append({"case": {k: str(v) for k, v in case.items()}, "reference": verdicts[0], "model": verdicts[1]})
    return {"cases": total, "agree": agree, "share": agree / total, "model_raises": errors, "first_disagreements": diffs}


if __name__ == "__main__":
    import json
    import statistics
    tree, results = Path(sys.argv[1]), {}
    for m in sys.argv[3:]:
        results[m] = compare(tree, sys.argv[2], m)
        r = results[m]
        print(f"{m}: {r['agree']} of {r['cases']} cases agree ({r['share']:.4f}); the model raised on {r['model_raises']}")
    shares = [r["share"] for m, r in results.items() if not m.rsplit("_", 1)[-1].startswith("X")]   # X* are mutant controls
    if len(shares) > 1:
        print(f"{len(shares)} model runs: mean {statistics.mean(shares):.4f}, sd {statistics.stdev(shares):.4f}, "
              f"min {min(shares):.4f}, max {max(shares):.4f}")
    out = Path(__file__).resolve().parent / "scores.json"
    out.write_text(json.dumps(results, indent=1, default=str), encoding="utf-8")
