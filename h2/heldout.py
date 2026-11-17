"""Score the modules of a loop run on a grid the loop never showed the model: other dates, pays and ages.

  python3 h2/heldout.py TREE K...        TREE is a loop run's clerk tree; K are the runs (S1, S2, ...); scores rounds 0 and 1 and the last.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "h1"))
import score  # noqa: E402

score.DATES = [dt.date(2020, 4, 1), dt.date(2022, 10, 1), dt.date(2024, 3, 1), dt.date(2026, 2, 1)]
score.PAYS = [250, 650, 850, 950, 1100, 1300, 1450, 2000]
score.AGES_YEARS = [1, 5, 12, 14, 16, 17, 19, 20, 22, 24]

if __name__ == "__main__":
    tree = Path(sys.argv[1])
    out = {}
    for k in sys.argv[2:]:
        out[k] = {}
        for rnd in (0, 1, 4):
            r = score.compare(tree, "Ouverture_Ref", f"Ouverture_{k}_R{rnd}")
            out[k][rnd] = {"agree": r["agree"], "cases": r["cases"], "share": round(r["share"], 4)}
        print(k, out[k], flush=True)
    (tree.parent / "heldout.json").write_text(json.dumps(out, indent=1))
