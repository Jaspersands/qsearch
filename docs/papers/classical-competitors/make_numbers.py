"""Generate numbers.tex from numbers_map.json: every number in the paper comes from a committed report.

    python docs/papers/classical-competitors/make_numbers.py          # write numbers.tex
    python docs/papers/classical-competitors/make_numbers.py --check  # also list undefined macros in main.tex

Each entry names a LaTeX macro, a report (path relative to the repository root), a dotted
path into its JSON (list indices are numbers) and a Python format string. A path that no
longer resolves is an error, so a report that moved or dropped a value stops this script.
An entry may set "absent" (for example "--"): then, and only then, a missing last key under
a parent that does resolve prints that text, for counts the report omits when they are zero.
A value that merely changes is not an error here: numbers.tex stays stale until this script
is rerun, and tests/tools/test_paper_numbers.py fails while the committed numbers.tex differs
from what the script would write.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
_MACRO = re.compile(r"^[A-Za-z]+$")
# LaTeX commands the paper may use without defining them here.
KNOWN = frozenset("""
documentclass usepackage begin end title author date maketitle section subsection subsubsection paragraph
label ref eqref cite citep citet emph textbf textit texttt url href footnote item caption centering
hline toprule midrule bottomrule multicolumn tabular table figure le ge leq geq ne neq approx sim cdot times
equiv frac tfrac sqrt sum prod log ln exp sin cos theta gamma Gamma alpha beta delta Delta epsilon varepsilon lambda Lambda
mu nu pi rho sigma tau phi Phi psi Psi omega Omega chi mathbb mathcal mathrm mathbf operatorname left right
langle rangle lvert rvert lVert rVert ldots cdots dots quad qquad in notin subset subseteq cup cap to mapsto
infty pm mp otimes oplus dagger top perp partial nabla forall exists neg land lor implies iff text textsc
bibliographystyle bibliography newcommand renewcommand input include appendix abstract keywords noindent
small footnotesize large Large tiny normalsize vspace hspace bigskip medskip smallskip newline linewidth
textwidth includegraphics resizebox tableofcontents enumerate itemize description verb bm boldsymbol
lfloor rfloor lceil rceil binom choose bmod pmod mod det tr Tr rank deg gcd max min arg sup inf lim
hat tilde bar overline underline widehat widetilde vec mid colon star ast circ bullet setminus emptyset
varphi vartheta kappa eta zeta xi Xi upsilon Upsilon iota ell hbar Re Im wp aleph square checkmark
rightarrow leftarrow Rightarrow Leftarrow leftrightarrow longrightarrow hookrightarrow
""".split())


def resolve(data, path: str):
    node = data
    walked = []
    for part in path.split("."):
        walked.append(part)
        try:
            node = node[int(part)] if isinstance(node, list) else node[part]
        except (KeyError, IndexError, ValueError, TypeError):
            raise KeyError(".".join(walked)) from None
    return node


def convert(value, kind: str) -> str:
    """Exact conversions applied before formatting.

    up:N / down:N    decimal with N places, rounded toward +inf / -inf (for upper / lower bounds)
    bits             bit length of an integer (or of a decimal string)
    bits_ge          least b such that every b-bit integer is >= the value (a sufficient size)
    pi               an angle as a small rational multiple of pi, in LaTeX
    sci              one-digit-mantissa scientific notation, in LaTeX, rounded to nearest
    sci:up/sci:down  the same, rounded toward +inf / -inf
    """
    if kind.startswith(("up:", "down:")):
        direction, places = kind.split(":")
        scaled = _exact(value) * 10 ** int(places)
        whole = math.ceil(scaled) if direction == "up" else math.floor(scaled)
        sign, digits = ("-" if whole < 0 else ""), str(abs(whole)).rjust(int(places) + 1, "0")
        return f"{sign}{digits[:-int(places)]}.{digits[-int(places):]}" if int(places) else f"{sign}{digits}"
    if kind == "bits":
        return str(int(str(value)).bit_length())
    if kind == "bits_ge":
        threshold = int(str(value))
        if threshold < 1:
            raise ValueError(f"bits_ge needs a positive integer, got {value}")
        return str((threshold - 1).bit_length() + 1)
    if kind == "pi":
        ratio = Fraction(float(value) / math.pi).limit_denominator(64)
        if abs(float(ratio) * math.pi - float(value)) > 1e-12:
            raise ValueError(f"{value} is not a small rational multiple of pi")
        num = "" if abs(ratio.numerator) == 1 else str(abs(ratio.numerator))
        sign = "-" if ratio < 0 else ""
        return f"{sign}{num}\\pi" + ("" if ratio.denominator == 1 else f"/{ratio.denominator}")
    if kind == "sci":
        mantissa, exponent = f"{float(value):.1e}".split("e")
        return f"{mantissa}\\times 10^{{{int(exponent)}}}"
    if kind in ("sci:up", "sci:down"):
        return _directed_sci(_exact(value), kind == "sci:up")
    raise ValueError(f"unknown kind {kind!r}")


def _exact(value) -> Fraction:
    return Fraction(value) if isinstance(value, float) else Fraction(str(value))


def _directed_sci(exact: Fraction, up: bool) -> str:
    """m.d x 10^e with the mantissa rounded toward +inf (up) or -inf (down), computed exactly."""
    if exact == 0:
        return "0.0\\times 10^{0}"
    magnitude, toward_larger = abs(exact), up == (exact > 0)
    exponent = math.floor(math.log10(magnitude))
    while magnitude >= Fraction(10) ** (exponent + 1):
        exponent += 1
    while magnitude < Fraction(10) ** exponent:
        exponent -= 1
    tenths = magnitude / Fraction(10) ** exponent * 10
    tenths = math.ceil(tenths) if toward_larger else math.floor(tenths)
    if tenths == 100:
        tenths, exponent = 10, exponent + 1
    sign = "-" if exact < 0 else ""
    return f"{sign}{tenths // 10}.{tenths % 10}\\times 10^{{{exponent}}}"


def _value(entry: dict, data) -> str:
    try:
        value = resolve(data, entry["path"])
    except KeyError:
        parent, _, last = entry["path"].rpartition(".")
        node = resolve(data, parent) if parent else data
        if "absent" in entry and isinstance(node, dict) and last not in node:
            return entry["absent"]
        raise
    if entry.get("kind"):
        value = convert(value, entry["kind"])
    return entry.get("format", "{}").format(value)


def render(entries: list[dict], root: Path) -> str:
    cache: dict[str, object] = {}
    lines = ["% Generated by make_numbers.py from numbers_map.json; do not edit."]
    for entry in entries:
        macro = entry["macro"]
        if not _MACRO.match(macro):
            raise ValueError(f"macro {macro!r} must be letters only")
        source = entry["source"]
        if source not in cache:
            cache[source] = json.loads((root / source).read_text(encoding="utf-8"))
        lines.append(f"\\newcommand{{\\{macro}}}{{{_value(entry, cache[source])}}}")
    return "\n".join(lines) + "\n"


def compare(entries: list[dict], committed: Path, fresh: Path) -> list[dict]:
    """Format each number from the committed reports and from a fresh regeneration, and compare."""
    rows = []
    for entry in entries:
        old = _value(entry, json.loads((committed / entry["source"]).read_text(encoding="utf-8")))
        path = fresh / entry["source"]
        if not path.exists():
            rows.append({"macro": entry["macro"], "status": "not regenerated", "committed": old, "fresh": None})
            continue
        try:
            new = _value(entry, json.loads(path.read_text(encoding="utf-8")))
        except KeyError:
            new = None
        rows.append({"macro": entry["macro"], "status": "same" if new == old else "DIFFERENT", "committed": old, "fresh": new})
    return rows


def undefined(tex: str, defined: set[str], known_commands=KNOWN) -> list[str]:
    body = re.sub(r"(?<!\\)%.*", "", tex)
    used = set(re.findall(r"\\([A-Za-z]+)", body))
    local = set(re.findall(r"\\(?:re)?newcommand\{\\([A-Za-z]+)\}", body))
    return sorted(used - defined - set(known_commands) - local)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--compare", type=Path, help="root of a fresh regeneration (see reproduce.sh)")
    args = parser.parse_args(argv)
    entries = json.loads((HERE / "numbers_map.json").read_text(encoding="utf-8"))["numbers"]
    if args.compare:
        rows = compare(entries, REPO, args.compare)
        for row in rows:
            print(f"{row['status']:>15}  \\{row['macro']}  committed={row['committed']}  fresh={row['fresh']}")
        counts = {s: sum(r["status"] == s for r in rows) for s in ("same", "DIFFERENT", "not regenerated")}
        print(counts)
        return 1 if counts["DIFFERENT"] else 0
    text = render(entries, REPO)
    (HERE / "numbers.tex").write_text(text, encoding="utf-8")
    print(f"wrote {len(entries)} numbers")
    if args.check:
        missing = undefined((HERE / "main.tex").read_text(encoding="utf-8"), {e["macro"] for e in entries})
        for name in missing:
            print(f"main.tex uses \\{name}, which is neither a number nor a known command")
        return 1 if missing else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
