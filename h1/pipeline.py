"""H1: a model translates two articles into Catala; its decisions are scored against the reference's.

The slice is the right a child opens to the family benefits: article L. 512-3 (the child, the age limit and the ceiling
of pay it names) and article R. 512-2 (twenty years, 55 % of the SMIC times 169). The reference is the three rules of
catala-examples at 9e251b9 (`reference_rules.catala_fr`, copied from its files and tested to occur there). A module is the
declarations, a set of rules, and the reference's helper `conditions_hors_âge`; the reference module and each model module
differ in the rules only. The model sees the statute's prose and the declarations, never the reference's rules.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FENCE = "```"


def read(name: str) -> str:
    return (HERE / name).read_text(encoding="utf-8")


def module_text(name: str, rules: str) -> str:
    """A Catala module `name`: the declarations, the given rules and the reference's helper."""
    return (f"> Usage de France\n> Usage de Smic\n\n> Module {name}\n\n# {name}\n\n"
            f"{FENCE}catala-metadata\n{read('declarations.catala_fr').rstrip()}\n{FENCE}\n\n"
            f"{FENCE}catala\n{rules.rstrip()}\n{FENCE}\n\n"
            f"{FENCE}catala\n{read('helper.catala_fr').rstrip()}\n{FENCE}\n")


def answer_rules(answer: str) -> str | None:
    """The Catala code the model returned: its first catala block, or None when it returned none."""
    found = re.search(r"```(?:catala|catala_fr)?\n(.*?)```", answer, re.S)
    return found.group(1).strip() if found else None


def build_tree(tree: Path, examples: Path, variants: dict[str, str]) -> None:
    """A clerk tree holding Smic and France (from catala-examples) and one module per variant, each its own target."""
    import shutil
    (tree / "ouverture").mkdir(parents=True, exist_ok=True)
    for sub in ("smic", "prologue_france"):
        shutil.copytree(examples / sub, tree / sub, dirs_exist_ok=True)
    targets = ['[project]\nname = "h1"\ninclude_dirs = ["smic", "prologue_france", "ouverture"]\n',
               '[[target]]\nname = "smic"\nmodules = ["Smic", "France"]\nbackends = ["python"]\n']
    for name, rules in variants.items():
        (tree / "ouverture" / f"{name}.catala_fr").write_text(module_text(name, rules), encoding="utf-8")
        targets.append(f'[[target]]\nname = "{name.lower().replace("_", "-")}"\nmodules = ["{name}"]\n'
                       f'backends = ["python"]\ndependencies = ["smic"]\n')
    (tree / "clerk.toml").write_text("\n".join(targets), encoding="utf-8")
