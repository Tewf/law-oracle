"""The statute text the model translates: the prose of two articles, with the Catala of the reference left out.

Article L. 512-3 and article R. 512-2 of the Code de la sécurité sociale, as the catala-examples tree carries them
(the Légifrance text, with its LEGIARTI id). The reference's code blocks are removed, so the model reads the law and
never the reference's rules. Run as a script it prints the text.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ARTICLES = [("securite_sociale_L.catala_fr", "Article L512-3"), ("securite_sociale_R.catala_fr", "Article R512-2")]
CODE = re.compile(r"```catala.*?```\n?", re.S)


def article(source: Path, heading: str) -> str:
    """The prose of one article: from its heading to the next heading of the same or a higher level, no code block."""
    text = CODE.sub("", source.read_text(encoding="utf-8"))   # no code first: a comment in a block looks like a heading
    start = text.index(f"###### {heading}")
    end = re.search(r"^#{1,6} ", text[start + 8:], re.M)
    body = text[start: start + 8 + end.start()] if end else text[start:]
    return re.sub(r"\n{3,}", "\n\n", body).strip()


def statute(tree: Path) -> str:
    return "\n\n".join(article(tree / "allocations_familiales" / f, h) for f, h in ARTICLES)


if __name__ == "__main__":
    print(statute(Path(sys.argv[1])))
