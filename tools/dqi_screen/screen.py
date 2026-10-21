"""Screen a DQI candidate against the Mazumder-Niroula soundness rules (arXiv:2610.06753).

    python tools/dqi_screen/screen.py --params tools/dqi_screen/examples/opi_prime_character_r19.json
    python tools/dqi_screen/screen.py --objective count --q 7 --m 100 --n 30 --rho 0.5 --radius 5 --min-distance 20 --decoder-known
    python tools/dqi_screen/screen.py --params cand.json --json --out screen.json

A candidate is a max-LINSAT family: m constraints over n variables in F_q, accepted density
rho, the objective ("count" of satisfied constraints, or "cosine"), and the claimed decoding
radius. The screen computes the closed-form quantities, runs each rule and gives a verdict:
"not viable" when a hard rule fails, "unknown" when an input is missing or a soft rule
flags, else "viable". It is a soundness screen, not a proof.

Exit codes: 0 viable or unknown, 1 not viable, 2 bad input.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import MISSING, asdict, dataclass, fields
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.dqi_screen import rules as R  # noqa: E402

OBJECTIVES = ("count", "cosine")
HARD = ("R1", "reach", "R2", "R3-encoder", "R4")
WITNESS_GAP = 0.01
NOT_APPLICABLE = "not applicable"


@dataclass(frozen=True)
class Candidate:
    name: str
    objective: str
    q: int
    m: int
    n: int
    rho: float
    radius: int | None = None
    min_distance: int | None = None
    decoder_known: bool = False
    encoder_known: bool = False
    p: int | None = None
    b: int | None = None
    c: int | None = None
    classical_witness: float | None = None
    finite_dqi_mean: float | None = None


@dataclass(frozen=True)
class Check:
    rule: str
    passed: bool | None
    detail: str


@dataclass
class Screen:
    candidate: Candidate
    quantities: dict[str, float | int | None]
    checks: list[Check]
    verdict: str
    reasons: list[str]


_INTS = {"q", "m", "n", "radius", "min_distance", "p", "b", "c"}
_FLOATS = {"rho", "classical_witness", "finite_dqi_mean"}
_BOOLS = {"decoder_known", "encoder_known"}
_EXACT_FLOAT = 2**53  # from here on a float cannot tell neighbouring integers apart


def _coerce(key: str, value):
    if value is None:
        return None
    if key in _BOOLS:
        if not isinstance(value, bool):
            raise ValueError(f"{key} must be true or false, got {value!r}")
        return value
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        if key in _INTS | _FLOATS:
            raise ValueError(f"{key} must be a number, got {value!r}")
        return str(value)
    if key in _INTS:
        if isinstance(value, float) and not value.is_integer():
            raise ValueError(f"{key} must be an integer, got {value!r}")
        if isinstance(value, float) and abs(value) >= _EXACT_FLOAT:
            raise ValueError(f"{key} = {value!r} is a float beyond 2^53, which cannot hold every integer: "
                             "give it as an exact integer")
        return int(value)
    if key in _FLOATS:
        return float(value)
    return str(value)


def candidate_from_dict(data: dict) -> Candidate:
    """A Candidate from a JSON-style dict; ValueError on unknown or missing keys, wrong types
    or an objective other than "count" or "cosine"."""
    if not isinstance(data, dict):
        raise ValueError(f"candidate must be a JSON object, got {type(data).__name__}")
    names = [f.name for f in fields(Candidate)]
    unknown = sorted(set(data) - set(names))
    if unknown:
        raise ValueError(f"unknown keys: {', '.join(unknown)}")
    required = [f.name for f in fields(Candidate) if f.default is MISSING]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"missing keys: {', '.join(missing)}")
    nulls = [key for key in required if data[key] is None]
    if nulls:
        raise ValueError(f"{', '.join(nulls)} must not be null")
    if data["objective"] not in OBJECTIVES:
        raise ValueError(f"objective must be one of {', '.join(OBJECTIVES)}, got {data['objective']!r}")
    return Candidate(**{key: _coerce(key, value) for key, value in data.items()})


def load_candidate(path: Path) -> Candidate:
    return candidate_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def _isprime(q: int) -> bool:
    import sympy  # deterministic below 2^64; imported lazily (slow import)

    return bool(sympy.isprime(q))


def _validate(c: Candidate) -> None:
    if not 0 < c.n < c.m:
        raise ValueError(f"need 0 < n < m, got n={c.n}, m={c.m}")
    if not 0 < c.rho < 1:
        raise ValueError(f"rho must lie strictly between 0 and 1, got {c.rho}")
    if c.radius is not None and not 0 <= c.radius <= c.m:
        raise ValueError(f"radius must lie in [0, m], got {c.radius}")
    if c.min_distance is not None and not 1 <= c.min_distance <= c.m:
        raise ValueError(f"min_distance must lie in [1, m], got {c.min_distance}")
    low = 0.0 if c.objective == "count" else -1.0  # satisfied fraction, or mean of cos(2 pi v / q)
    for key in ("finite_dqi_mean", "classical_witness"):
        value = getattr(c, key)
        if value is not None and not low <= value <= 1:  # also rejects NaN and inf
            raise ValueError(f"{key} must be a finite number in [{low:g}, 1] for the {c.objective} objective, got {value}")
    root = _prime_power(c.q) if c.q >= 2 else None
    if root is None:
        raise ValueError(f"q must be a prime power, got {c.q}")
    p, b = root
    field = f"q = {c.q} = {p}^{b}"
    if c.p is not None and c.p != p:
        raise ValueError(f"p = {c.p} does not match {field}: p is the prime with q = p^b")
    if c.b is not None and c.b != b:
        raise ValueError(f"b = {c.b} does not match {field}: b is the degree of F_q over F_p")
    if c.c is not None and (c.c < 1 or b % c.c):
        raise ValueError(f"c = {c.c} does not divide b = {b} ({field}): F_(p^c) is a subfield of F_q only when c | b")


def _prime_power(q: int) -> tuple[int, int] | None:
    """(p, b) with q = p^b and p prime, or None when q is not a prime power."""
    import sympy

    if _isprime(q):
        return q, 1
    power = sympy.perfect_power(q)
    if power and _isprime(int(power[0])):
        return int(power[0]), int(power[1])
    return None


def _fmt(x: float | None) -> str:
    return "none" if x is None else f"{x:.4g}"


def _quantities(c: Candidate) -> dict[str, float | int | None]:
    count = c.objective == "count"
    alpha = c.n / c.m
    lam = c.radius / c.m if c.radius is not None else None
    delta = c.min_distance / c.m if c.min_distance is not None else None
    q_pr = R.q_prange(alpha, c.rho) if count else None
    q_dqi = R.q_dqi(lam, c.rho) if count and lam is not None else None
    cos_obj = R.cosine_objective(lam) if not count and lam is not None else None
    baseline = q_pr if count else alpha  # Prange's value: satisfied fraction, or alpha for the cosine
    asymptotic = q_dqi if count else cos_obj
    margin = asymptotic - baseline if asymptotic is not None else None
    margin_finite = c.finite_dqi_mean - baseline if c.finite_dqi_mean is not None else None
    threshold = R.lambda_crit(alpha, c.rho) if count else R.lambda_crit_cos(alpha)
    kappa = R.margin_cap(alpha) if count else None
    mu = margin_finite if margin_finite is not None else margin
    subfield = c.p is not None and c.b is not None and c.c is not None
    alpha_sub = R.subfield_rate(alpha, c.b, c.c) if subfield else None
    return {
        "alpha": alpha,
        "lam": lam,
        "delta": delta,
        "q_prange": q_pr,
        "q_dqi": q_dqi,
        "q_dqi_finite": c.finite_dqi_mean,
        "margin": margin,
        "margin_finite": margin_finite,
        "lambda_crit": threshold if count else None,
        "radius_crit": threshold * c.m if threshold is not None else None,
        "licensed_radius": R.licensed_radius(c.min_distance) if c.min_distance is not None else None,
        "signed_packing_radius": None if count else R.packing_radius(c.m, c.n, c.q, 2),
        "singleton_reach": R.singleton_reach(alpha),
        "distance_reach": R.distance_reach(delta) if delta is not None else None,
        "sphere_packing_reach": R.sphere_packing_reach(alpha, c.q),
        "plotkin_reach": R.plotkin_reach(alpha, c.q),
        "signed_packing_reach": None if count else R.signed_packing_reach(alpha, c.q),
        "kappa": kappa,
        "q_cap": q_pr + kappa if count else None,
        "cosine_objective": cos_obj,
        "lambda_crit_cos": None if count else threshold,
        "restart_length": R.restart_length(alpha, mu, 1 if count else 2) if mu is not None else None,
        "existential_line": R.existential_line(alpha, c.rho, c.q) if count else None,
        "rho_crit": R.rho_crit(alpha) if count else None,
        "alpha_sub": alpha_sub,
        "subfield_baseline": R.subfield_baseline(c.rho, alpha_sub, c.m) if count and subfield else None,
    }


def _reach_bounds(c: Candidate, qn: dict) -> dict[str, float]:
    """Asymptotic upper bounds on lam. The cosine needs only signed {0, +-1} error patterns, which
    the Hamming bounds do not limit (Proposition 13): its bound is signed-pattern packing."""
    if c.objective == "cosine":
        return {"signed packing": qn["signed_packing_reach"]}
    names = {"Singleton": "singleton_reach", "distance": "distance_reach",
             "sphere-packing": "sphere_packing_reach", "Plotkin": "plotkin_reach"}
    return {name: qn[key] for name, key in names.items() if qn[key] is not None}


def _check_r1(c: Candidate, qn: dict) -> Check:
    threshold = qn["lambda_crit"] if c.objective == "count" else qn["lambda_crit_cos"]
    if threshold is None:
        return Check("R1", False, f"alpha = {_fmt(qn['alpha'])} >= 1/sqrt(2): no radius beats Prange on the cosine objective")
    name = "lambda_crit" if c.objective == "count" else "lambda_crit_cos"
    bounds = _reach_bounds(c, qn)
    low = [f"{bound} {_fmt(value)}" for bound, value in bounds.items() if value <= threshold]
    if low:
        return Check("R1", False, f"reach bound {', '.join(low)} <= {name} = {_fmt(threshold)}: "
                     "even an ideal decoder at the reach limit cannot beat Prange")
    tight = min(bounds, key=bounds.get)
    return Check("R1", True, f"every reach bound exceeds {name} = {_fmt(threshold)} (tightest: {tight} {_fmt(bounds[tight])})")


def _check_reach_signed(c: Candidate, qn: dict) -> Check:
    """The cosine: the radius must fit signed-pattern packing at this (m, n, q). A Hamming licence
    (d - 2) // 2 covers signed patterns, but a radius beyond it is not refuted by it."""
    limit = qn["signed_packing_radius"]
    if c.radius > limit:
        return Check("reach", False, f"outside licensed signed-pattern reach: radius {c.radius} > signed packing radius "
                     f"{limit}: C(m, l) 2^l > q^n, so the {{+-1}} patterns of weight l cannot have distinct syndromes "
                     "(Proposition 13(i))")
    inside = f"radius {c.radius} (lam = {_fmt(qn['lam'])}) is inside signed packing radius {limit}"
    if qn["licensed_radius"] is not None:
        licence = qn["licensed_radius"]
        inside += (f", within the Hamming licence (d - 2) // 2 = {licence}, which covers signed patterns"
                   if c.radius <= licence else
                   f", beyond the Hamming licence (d - 2) // 2 = {licence}: it needs a decoder licensed for "
                   "{+-1} patterns (Definition 11)")
    if not c.decoder_known:
        return Check("reach", None, inside + ", but no decoder is known to reach it; give decoder_known")
    return Check("reach", True, inside)


def _check_reach(c: Candidate, qn: dict) -> Check:
    lam = qn["lam"]
    if lam is None:
        return Check("reach", None, "give radius")
    if c.objective == "cosine":
        return _check_reach_signed(c, qn)
    problems = []
    if qn["licensed_radius"] is not None and c.radius > qn["licensed_radius"]:
        problems.append(f"radius {c.radius} > licensed radius {qn['licensed_radius']} = (d - 2) // 2")
    bounds = _reach_bounds(c, qn)
    over = [f"{bound} {_fmt(value)}" for bound, value in bounds.items() if lam > value]
    if over:
        problems.append(f"lam = {_fmt(lam)} exceeds the reach bound {', '.join(over)}")
    saturated = None
    if c.objective == "count" and lam > 1 - c.rho:
        saturated = (f"saturated: lam = {_fmt(lam)} > 1 - rho = {_fmt(1 - c.rho)}, where the semicircle law pins "
                     "Q_DQI at 1 and says nothing about this radius")
    if problems:
        detail = "outside licensed Hamming reach: " + "; ".join(problems)
        return Check("reach", False, detail + (f"; also {saturated}" if saturated else ""))
    tight = min(bounds, key=bounds.get)
    if saturated:
        return Check("reach", False, f"{saturated} (radius {c.radius} is within every reach bound; tightest: "
                     f"{tight} {_fmt(bounds[tight])})")
    inside = f"radius {c.radius} (lam = {_fmt(lam)}) is inside licensed Hamming reach (tightest: {tight} {_fmt(bounds[tight])})"
    if not c.decoder_known:
        return Check("reach", None, inside + ", but no decoder is known to reach it; give decoder_known")
    return Check("reach", True, inside)


def _check_r2(c: Candidate, qn: dict) -> Check:
    threshold = qn["lambda_crit"] if c.objective == "count" else qn["lambda_crit_cos"]
    if qn["lam"] is None:
        return Check("R2", None, "give radius")
    if threshold is None:
        return Check("R2", False, "no threshold radius exists (alpha >= 1/sqrt(2))")
    name = "lambda_crit" if c.objective == "count" else "lambda_crit_cos"
    passed = qn["lam"] > threshold
    relation = ">" if passed else "<="
    return Check("R2", passed, f"lam = {_fmt(qn['lam'])} {relation} {name} = {_fmt(threshold)} "
                 f"(radius {c.radius} against {_fmt(qn['radius_crit'])})")


def _claimed(c: Candidate, qn: dict) -> tuple[float | None, str]:
    if c.finite_dqi_mean is not None:
        return c.finite_dqi_mean, "finite DQI mean"
    return qn["q_dqi"], "Q_DQI"


def _check_r3(c: Candidate, qn: dict) -> Check:
    if c.objective != "count":
        return Check("R3", None, f"{NOT_APPLICABLE} (count objective only)")
    value, label = _claimed(c, qn)
    if value is None:
        return Check("R3", None, "give radius or finite_dqi_mean")
    line = qn["existential_line"]
    if value <= line + 1e-12:
        return Check("R3", True, f"{label} {_fmt(value)} <= existential line {_fmt(line)}")
    return Check("R3", False, f"{label} {_fmt(value)} > existential line {_fmt(line)}: "
                 "a typical instance has no assignment that good")


def _check_encoder(c: Candidate) -> Check:
    if c.encoder_known:
        return Check("R3-encoder", False, "the encoder is known, so the margin over Prange is <= 0")
    return Check("R3-encoder", True, "encoder not known")


def _check_r4(c: Candidate, qn: dict) -> Check:
    if _isprime(c.q):
        return Check("R4", None, f"{NOT_APPLICABLE} (prime field)")
    if qn["alpha_sub"] is None:
        return Check("R4", None, f"q = {c.q} is a prime power: give p, b, c for the subfield rule")
    if c.objective != "count":
        return Check("R4", None, "the subfield baseline is stated for the count objective; compare by hand")
    value, label = _claimed(c, qn)
    if value is None:
        return Check("R4", None, "give radius or finite_dqi_mean")
    baseline = qn["subfield_baseline"]
    blocks = c.rho == 0.5 and R.subfield_blocks_at_half(qn["alpha"], c.b, c.c)
    detail = f"{label} {_fmt(value)} against subfield baseline {_fmt(baseline)} (alpha_sub = {_fmt(qn['alpha_sub'])})"
    if blocks:
        return Check("R4", False, detail + "; at rho = 1/2, alpha >= 2c^2/(b^2+c^2) blocks every licensed radius")
    if value <= baseline:
        return Check("R4", False, detail + ": the subfield baseline is at least as good")
    return Check("R4", True, detail)


def _check_cap(c: Candidate, qn: dict) -> Check:
    if c.objective != "count":
        return Check("cap", None, f"{NOT_APPLICABLE} (count objective only)")
    if qn["q_dqi"] is None:
        return Check("cap", None, "give radius")
    passed = qn["q_dqi"] <= qn["q_cap"] + 1e-12
    relation = "<=" if passed else ">"
    return Check("cap", passed, f"Q_DQI {_fmt(qn['q_dqi'])} {relation} q_cap = Q_Pr + kappa = {_fmt(qn['q_cap'])}")


def _check_witness(c: Candidate, qn: dict) -> Check:
    if c.classical_witness is None:
        return Check("witness", None, f"{NOT_APPLICABLE} (no classical witness given)")
    if qn["q_cap"] is None:
        return Check("witness", None, f"{NOT_APPLICABLE} (the cap is for the count objective)")
    limit = qn["q_cap"] - WITNESS_GAP
    if c.classical_witness < limit:
        return Check("witness", True, f"classical witness {_fmt(c.classical_witness)} < q_cap - {WITNESS_GAP} = {_fmt(limit)}")
    return Check("witness", False, f"classical witness {_fmt(c.classical_witness)} >= q_cap - {WITNESS_GAP} = {_fmt(limit)}: "
                 f"no licensed radius beats it by more than {WITNESS_GAP}")


def _check_restarts(c: Candidate, qn: dict) -> Check:
    which = "finite" if qn["margin_finite"] is not None else "asymptotic"
    mu = qn["margin_finite"] if which == "finite" else qn["margin"]
    if mu is None:
        return Check("restarts", None, "give radius or finite_dqi_mean")
    length = qn["restart_length"]
    if length is None:
        return Check("restarts", False, f"{which} margin {_fmt(mu)} <= 0: no length outruns Prange restarts")
    passed = length <= c.m
    relation = ">=" if passed else "<"
    return Check("restarts", passed, f"m = {c.m} {relation} {length:.1f}, the length at which 2^40 Prange restarts "
                 f"stop closing the {which} margin {_fmt(mu)} (eta = 0.05)")


def _verdict(checks: list[Check]) -> tuple[str, list[str]]:
    failed = [f"{ch.rule}: {ch.detail}" for ch in checks if ch.rule in HARD and ch.passed is False]
    if failed:
        return "not viable", failed
    open_ = [f"{ch.rule}: {ch.detail}" for ch in checks
             if ch.passed is False or (ch.passed is None and not ch.detail.startswith(NOT_APPLICABLE))]
    if open_:
        return "unknown", open_
    return "viable", []


def screen(c: Candidate) -> Screen:
    _validate(c)
    qn = _quantities(c)
    checks = [
        _check_r1(c, qn),
        _check_reach(c, qn),
        _check_r2(c, qn),
        _check_r3(c, qn),
        _check_encoder(c),
        _check_r4(c, qn),
        _check_cap(c, qn),
        _check_witness(c, qn),
        _check_restarts(c, qn),
    ]
    verdict, reasons = _verdict(checks)
    return Screen(c, qn, checks, verdict, reasons)


def _cell(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.6g}"
    return str(value)


def _status(check: Check) -> str:
    if check.passed is None:
        return "n/a" if check.detail.startswith(NOT_APPLICABLE) else "open"
    return "pass" if check.passed else "FAIL"


def render(s: Screen) -> str:
    c = s.candidate
    lines = [
        f"# DQI screen: {c.name}",
        "",
        f"Objective {c.objective}, q = {c.q}, m = {c.m}, n = {c.n}, rho = {_cell(c.rho)}, radius = {_cell(c.radius)}, "
        f"min_distance = {_cell(c.min_distance)}, decoder known: {'yes' if c.decoder_known else 'no'}, "
        f"encoder known: {'yes' if c.encoder_known else 'no'}.",
        "",
        "## Quantities",
        "",
        "| Quantity | Value |",
        "|---|---|",
        *[f"| {key} | {_cell(value)} |" for key, value in s.quantities.items()],
        "",
        "## Checks",
        "",
        *[f"- {ch.rule} ({'hard' if ch.rule in HARD else 'soft'}): {_status(ch)}. {ch.detail}" for ch in s.checks],
        "",
        f"**Verdict: {s.verdict}**",
    ]
    if s.reasons:
        lines += ["", "Reasons:", "", *[f"- {reason}" for reason in s.reasons]]
    errors = "Hamming errors" if c.objective == "count" else "signed {+-1} error patterns"
    lines += ["", f"Asymptotic rules for worst-case decoding of {errors}; a screen, not a proof."]
    return "\n".join(lines) + "\n"


_FLAGS = ("name", "objective", "q", "m", "n", "rho", "radius", "min_distance", "decoder_known", "encoder_known",
          "p", "b", "c", "classical_witness", "finite_dqi_mean")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--params", type=Path, help="JSON file with the candidate's fields (see examples/); flags override it.")
    parser.add_argument("--name")
    parser.add_argument("--objective", choices=OBJECTIVES)
    for flag in ("q", "m", "n", "radius", "min-distance", "p", "b", "c"):
        parser.add_argument(f"--{flag}", type=int)
    for flag in ("rho", "classical-witness", "finite-dqi-mean"):
        parser.add_argument(f"--{flag}", type=float)
    parser.add_argument("--decoder-known", action="store_true", help="An efficient decoder reaches the radius.")
    parser.add_argument("--encoder-known", action="store_true", help="The planted encoder is known (R3: margin <= 0).")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out", type=Path, help="Write the report here instead of printing it.")
    args = parser.parse_args(argv)

    try:
        data = json.loads(args.params.read_text(encoding="utf-8")) if args.params else {}
        if not isinstance(data, dict):
            raise ValueError(f"{args.params} must hold a JSON object")
        # A value flag counts when given, even as 0; a boolean flag only when set, so it never clears the file's true.
        data.update({key: getattr(args, key) for key in _FLAGS
                     if getattr(args, key) is True or (key not in _BOOLS and getattr(args, key) is not None)})
        data.setdefault("name", "candidate")
        result = screen(candidate_from_dict(data))
    except (OSError, TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    text = json.dumps(asdict(result), indent=1) + "\n" if args.json else render(result)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"{result.verdict}: {args.out}")
    else:
        print(text, end="")
    return 1 if result.verdict == "not viable" else 0


if __name__ == "__main__":
    raise SystemExit(main())
