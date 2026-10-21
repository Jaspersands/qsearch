"""Screen a DQI candidate against the Mazumder-Niroula soundness rules (arXiv:2610.06753).

A candidate is a max-LINSAT family: m constraints over n variables in F_q, accepted density
rho, the objective ("count" of satisfied constraints, or "cosine"), and the claimed decoding
radius. The screen computes the closed-form quantities, runs each rule and gives a verdict:
"not viable" when a hard rule fails, "unknown" when an input is missing or a soft rule
flags, else "viable". It is a soundness screen, not a proof.
"""

from __future__ import annotations

import json
from dataclasses import MISSING, dataclass, fields
from pathlib import Path

from tools.dqi_screen import rules as R

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
    if c.q < 2 or not _is_prime_power(c.q):
        raise ValueError(f"q must be a prime power, got {c.q}")
    for key in ("p", "b", "c"):
        value = getattr(c, key)
        if value is not None and value < (2 if key == "p" else 1):
            raise ValueError(f"{key} is too small: {value}")


def _is_prime_power(q: int) -> bool:
    import sympy

    if _isprime(q):
        return True
    power = sympy.perfect_power(q)
    return bool(power) and _isprime(int(power[0]))


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
        "singleton_reach": R.singleton_reach(alpha),
        "distance_reach": R.distance_reach(delta) if delta is not None else None,
        "sphere_packing_reach": R.sphere_packing_reach(alpha, c.q),
        "plotkin_reach": R.plotkin_reach(alpha, c.q),
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


def _reach_bounds(qn: dict) -> dict[str, float]:
    names = {"Singleton": "singleton_reach", "distance": "distance_reach",
             "sphere-packing": "sphere_packing_reach", "Plotkin": "plotkin_reach"}
    return {name: qn[key] for name, key in names.items() if qn[key] is not None}


def _check_r1(c: Candidate, qn: dict) -> Check:
    threshold = qn["lambda_crit"] if c.objective == "count" else qn["lambda_crit_cos"]
    if threshold is None:
        return Check("R1", False, f"alpha = {_fmt(qn['alpha'])} >= 1/sqrt(2): no radius beats Prange on the cosine objective")
    name = "lambda_crit" if c.objective == "count" else "lambda_crit_cos"
    bounds = _reach_bounds(qn)
    low = [f"{bound} {_fmt(value)}" for bound, value in bounds.items() if value <= threshold]
    if low:
        return Check("R1", False, f"reach bound {', '.join(low)} <= {name} = {_fmt(threshold)}: "
                     "even an ideal decoder at the reach limit cannot beat Prange")
    tight = min(bounds, key=bounds.get)
    return Check("R1", True, f"every reach bound exceeds {name} = {_fmt(threshold)} (tightest: {tight} {_fmt(bounds[tight])})")


def _check_reach(c: Candidate, qn: dict) -> Check:
    lam = qn["lam"]
    if lam is None:
        return Check("reach", None, "give radius")
    problems = []
    if c.objective == "count" and lam > 1 - c.rho:
        problems.append(f"saturated: lam = {_fmt(lam)} > 1 - rho = {_fmt(1 - c.rho)}, where the semicircle value is pinned at 1")
    if qn["licensed_radius"] is not None and c.radius > qn["licensed_radius"]:
        problems.append(f"radius {c.radius} > licensed radius {qn['licensed_radius']} = (d - 2) // 2")
    bounds = _reach_bounds(qn)
    over = [f"{bound} {_fmt(value)}" for bound, value in bounds.items() if lam > value]
    if over:
        problems.append(f"lam = {_fmt(lam)} exceeds the reach bound {', '.join(over)}")
    if problems:
        return Check("reach", False, "outside licensed Hamming reach: " + "; ".join(problems))
    tight = min(bounds, key=bounds.get)
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
