"""H2: the loop returns each disagreement as a case, and a model repairs its own translation.

Each round: a translation is compiled with Catala, scored against the reference on the grid of h1/score.py, and, if it
disagrees, up to FEEDBACK of its disagreeing cases go back to the model as plain cases (the date, the child, what the
official reading decides, what the translation decides), and the model returns a corrected module. The model sees cases,
never the reference's rules. Agreement per round is the measure; the loop stops when it reaches 1, when it stops rising for
a round, or after ROUNDS rounds.

  python3 h2/loop.py OUTDIR STARTS_DIR [MODEL]     STARTS_DIR holds runs/rules_K.catala_fr (h1/translate.py's output)

It needs the Catala environment (opam switch `catala`, tooling.md) and `ask-mistral`. Writes OUTDIR/loop.json.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "h1"))
import pipeline  # noqa: E402
import score  # noqa: E402

EXAMPLES = Path.home() / ".cache/dag-workers/law-8/catala-examples"
FEEDBACK = 6          # PROVISIONAL: disagreeing cases shown to the model each round
ROUNDS = 4            # PROVISIONAL: repair rounds after the first translation
MAX_SHOWN = 20        # score.compare keeps this many first disagreements


def build(tree: Path, variants: dict[str, str]) -> set[str]:
    """Compile every variant; return the names that do not compile. One bad module breaks a batch, so on failure each
    variant is built alone with the reference, and the ones that fail alone are left out."""
    pipeline.build_tree(tree, EXAMPLES, variants)
    if subprocess.run(["clerk", "build"], cwd=tree, capture_output=True, text=True).returncode == 0:
        return set()
    failed = set()
    for name in variants:
        if name == "Ouverture_Ref":
            continue
        pipeline.build_tree(tree, EXAMPLES, {"Ouverture_Ref": variants["Ouverture_Ref"], name: variants[name]})
        if subprocess.run(["clerk", "build"], cwd=tree, capture_output=True, text=True).returncode != 0:
            failed.add(name)
    pipeline.build_tree(tree, EXAMPLES, {n: r for n, r in variants.items() if n not in failed})
    done = subprocess.run(["clerk", "build"], cwd=tree, capture_output=True, text=True)
    if done.returncode != 0:
        raise RuntimeError(done.stderr[-600:] + done.stdout[-300:])
    return failed


def spread(diffs: list[dict], k: int) -> list[dict]:
    """k cases spread over the list, so the model sees different kinds of disagreement, not the first k in grid order."""
    if len(diffs) <= k:
        return diffs
    step = len(diffs) / k
    return [diffs[int(i * step)] for i in range(k)]


def case_text(d: dict) -> str:
    c = d["case"]
    ref, mod = d["reference"][0], d["model"][0]
    word = {"yes": "le droit est ouvert", "no": "le droit n'est pas ouvert", "raises": "le module produit une erreur"}
    return (f"- au {c['date']}, résidence {c['residence']}, enfant âgé de {c['years']} ans et {int(c['offset']):+d} jour(s) autour de son "
            f"anniversaire, situation scolaire « {c['situation']} », rémunération {c['pay']} € par mois: la lecture officielle: "
            f"{word[ref]}; votre module: {word[mod]}.")


def repair_prompt(prompt: str, rules: str, diffs: list[dict]) -> str:
    cases = "\n".join(case_text(d) for d in spread(diffs, FEEDBACK))
    return (f"{prompt}\n\n---\n\nVotre traduction précédente:\n\n```catala\n{rules}\n```\n\nEn comparant ses décisions à la lecture "
            f"officielle de ces deux articles sur une grille d'enfants et de dates, un programme a trouvé des cas où elles diffèrent. "
            f"Voici {min(FEEDBACK, len(diffs))} de ces cas (il y en a d'autres du même genre):\n\n{cases}\n\n"
            f"Corrige votre traduction pour que ses décisions suivent la loi. Réponds par le module de règles complet corrigé, "
            f"dans un seul bloc ```catala, sans commentaire autour.")


def ask(prompt: str, model: str) -> str | None:
    done = subprocess.run(["ask-mistral", "Réponds à la demande qui suit, dans les conditions qu'elle fixe."], input=prompt,
                          capture_output=True, text=True, env=dict(os.environ, MISTRAL_MODEL=model), timeout=200)
    return done.stdout if done.returncode == 0 and done.stdout.strip() else None


def main(out: Path, starts: Path, model: str) -> int:
    prompt = (starts / "prompt.md").read_text(encoding="utf-8")
    ref_rules = pipeline.read("reference_rules.catala_fr")
    current = {}
    for p in sorted((starts / "runs").glob("rules_*.catala_fr"), key=lambda q: int(q.stem.split("_")[1])):
        current[f"S{int(p.stem.split('_')[1])}"] = p.read_text(encoding="utf-8")
    history: dict[str, list[dict]] = {k: [] for k in current}
    previous = dict(current)
    tree = out / "tree"
    shutil.rmtree(tree, ignore_errors=True)
    for rnd in range(ROUNDS + 1):
        variants = {"Ref": ref_rules} | {f"{k}_R{rnd}": r for k, r in current.items()}
        failed = build(tree, {f"Ouverture_{n}": r for n, r in variants.items()})
        for k, rules in list(current.items()):
            if f"Ouverture_{k}_R{rnd}" in failed:         # a repair that does not compile: the previous module stands
                history[k].append({"round": rnd, "compiles": False, "share": history[k][-1]["share"] if history[k] else 0.0})
                print(f"{k} round {rnd}: does not compile", flush=True)
                current[k] = previous[k]
                if rnd < ROUNDS:
                    continue
                continue
            previous[k] = rules
            res = score.compare(tree, "Ouverture_Ref", f"Ouverture_{k}_R{rnd}")
            history[k].append({"round": rnd, "agree": res["agree"], "cases": res["cases"], "share": res["share"],
                               "raises": res["model_raises"], "shown": len(res["first_disagreements"])})
            print(f"{k} round {rnd}: {res['share']:.4f}", flush=True)
            if res["share"] < 1.0 and rnd < ROUNDS:
                answer = ask(repair_prompt(prompt, rules, res["first_disagreements"]), model)
                new = pipeline.answer_rules(answer) if answer else None
                history[k][-1]["repair_answered"] = bool(new)
                if new:
                    current[k] = new
        (out / "loop.json").write_text(json.dumps(history, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    sys.exit(main(out, Path(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "mistral-medium-latest"))
