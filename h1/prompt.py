"""The prompt of one translation: the primer, the declarations, the statute, and what to return."""
from __future__ import annotations

from pathlib import Path

import pipeline
import statute

HERE = Path(__file__).resolve().parent


def build(examples: Path) -> str:
    return f"""Tu traduis du droit français en Catala (syntaxe française). Voici d'abord une aide-mémoire de la syntaxe sur un exemple sans rapport.

{(HERE / "primer.md").read_text(encoding="utf-8")}

## Les déclarations de la vraie tâche (déjà écrites, tu ne les récris pas)

```catala
{pipeline.read("declarations.catala_fr").rstrip()}
```

`smic.brut_horaire` est le SMIC horaire brut, en euros, à la date courante et pour la résidence donnée.

## Le texte à traduire (Code de la sécurité sociale, Légifrance)

{statute.statute(examples)}

## Ce que tu rends

Les règles Catala, en un seul bloc ```catala, qui définissent, pour le champ d'application `PrestationsFamiliales`, exactement trois choses :
`droit_ouvert` (la condition « cet enfant ouvre droit aux prestations familiales »), `âge_l512_3_2` (l'âge limite) et `plafond_l512_3_2` (le plafond de rémunération mensuelle). Rien d'autre : pas de déclarations, pas de test. Un seul bloc, sans explication autour.
"""


if __name__ == "__main__":
    import sys
    print(build(Path(sys.argv[1])))
