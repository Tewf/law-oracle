"""Ask the model N times for the translation; keep each raw answer, extract its rules, record the spend.

  python3 h1/translate.py OUTDIR N [MODEL]     answers go to OUTDIR/runs/answer_K.txt, the rules to OUTDIR/runs/rules_K.catala_fr

The prompt is OUTDIR/prompt.md (built by prompt.py). The call is `ask-mistral`, whose temperature is fixed at 0.2, so the runs
differ only by the model's own sampling. A spend row per call goes to OUTDIR/depenses.csv, `when,account,what,amount,unit`, the
tokens counted as four characters each and priced at 0.4 and 2 dollars the million (an estimate, stated as one).
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pipeline

IN_RATE, OUT_RATE = 0.4e-6, 2.0e-6


def main(out: Path, n: int, model: str) -> int:
    runs = out / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    prompt = (out / "prompt.md").read_text(encoding="utf-8")
    spend = out / "depenses.csv"
    if not spend.exists():
        spend.write_text("when,account,what,amount,unit\n", encoding="utf-8")
    for k in range(1, n + 1):
        answer_file = runs / f"answer_{k}.txt"
        if answer_file.exists() and answer_file.stat().st_size:
            continue                                   # a resumed run keeps what it already has
        done = subprocess.run(["ask-mistral", "Réponds à la demande qui suit, dans les conditions qu'elle fixe."], input=prompt,
                              capture_output=True, text=True, env=dict(os.environ, MISTRAL_MODEL=model))
        if done.returncode != 0 or not done.stdout.strip():
            (runs / f"err_{k}.txt").write_text(done.stderr, encoding="utf-8")
            print(f"run {k}: no answer ({done.stderr.strip()[-80:]})")
            continue
        answer_file.write_text(done.stdout, encoding="utf-8")
        rules = pipeline.answer_rules(done.stdout)
        if rules:
            (runs / f"rules_{k}.catala_fr").write_text(rules + "\n", encoding="utf-8")
        cost = len(prompt) / 4 * IN_RATE + len(done.stdout) / 4 * OUT_RATE
        with spend.open("a", encoding="utf-8") as f:
            f.write(f'{time.strftime("%Y-%m-%dT%H:%M:%S")},mistral-api,"law-8 H1 run {k}, {model}",{cost:.6f},usd (estimate)\n')
        print(f"run {k}: {'rules kept' if rules else 'no catala block'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "mistral-medium-latest"))
