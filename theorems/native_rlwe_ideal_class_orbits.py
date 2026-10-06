"""Native conductor-ideal class orbits, not a short-element algorithm.

LOCAL DERIVATION / REVIEW PENDING. Conditional source counts assume prime
q=3 mod8 and power-two d>=4. Global equivalence uses the published full
real unit-signature theorem, not an independently reviewed result here.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from functools import lru_cache
from pathlib import Path

import sympy as sp

from native_rlwe_quaternion_kernel import NATIVE, _input, conjugate, mul

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/native_rlwe_ideal_class_orbits.json"


@lru_cache(maxsize=32)
def _prime_screen(q):
    if not sp.isprime(q):
        raise ValueError("composite modulus rejected; independent prime certificate still required for source theorem")


def ring_inverse(a,q):
    a,d = _input(a,q)
    x = sp.Symbol("x")
    polynomial = sp.Poly.from_list(list(reversed(a)),x,modulus=q)
    modulus = sp.Poly(x**d+1,x,modulus=q)
    try:
        inverse = sp.invert(polynomial,modulus)
    except (sp.NotInvertible,ZeroDivisionError) as exc:
        raise ValueError("a ring unit is required") from exc
    result = tuple(int(inverse.nth(i)) % q for i in range(d))
    assert tuple(v % q for v in mul(a,result))==(1,)+(0,)*(d-1)
    return result


def rotate(a,e,q):
    """Multiply by X^e using the actual negacyclic signed permutation."""
    d = len(a)
    out = [0]*d
    for i,v in enumerate(a):
        j = i+e
        out[j % d] = ((-1 if (j//d)%2 else 1)*v) % q
    return tuple(out)


def generic_source_member(a,q):
    a,d = _input(a,q)
    if d<4 or q%8!=3:
        raise ValueError("conditional high-CRT source law requires d>=4, q=3 mod8 PRIME")
    _prime_screen(q)
    norm = tuple(v % q for v in mul(a,conjugate(a)))
    # In the stated prime CRT regime, the real residue subring is a field.
    return any(norm) and norm!=((q-1,)+(0,)*(d-1))


def class_orbit(a,q):
    a,d = _input(a,q)
    if not generic_source_member(a,q):
        raise ValueError("unit ratio and unit beta=1+M*bar(M) required")
    inverse = ring_inverse(a,q)
    reflected = tuple(-v % q for v in inverse)
    words = [("rotation",k,rotate(a,2*k,q)) for k in range(d)]
    words += [("reflection",k,rotate(reflected,2*k,q)) for k in range(d)]
    orbit = {word for _,_,word in words}
    canonical = min(orbit)
    transport = next((kind,k) for kind,k,word in words if word==canonical)
    assert len(orbit) in (d,2*d)
    return {"dimension":d,"modulus":str(q),"ratio":list(map(str,a)),
            "canonical_class_label":list(map(str,canonical)),"orbit_size":len(orbit),
            "canonicalizing_unit_word":{"kind":transport[0],"rotation_exponent":transport[1]},
            "all_orbit_ratios":orbit,
            "global_equivalence_within_generic_native_family_decided_classically":True,
            "new_short_relation_or_completion_supplied":False,
            "class_label_is_not_a_hidden_oracle":True,
            "classmates_have_an_explicit_signed_isometric_transport":True,
            "generic_source_assumption":"q independently certified prime, q=3 mod8, power-two d>=4",
            "independent_review":False,"novelty_claim":False,"speedup_claim_allowed":False}


def source_class_count(d,q):
    if type(d) is not int or d<4 or d&(d-1) or type(q) is not int or q<3 or q%8!=3:
        raise ValueError("conditional high-CRT regime required")
    _prime_screen(q)
    x = q**(d//2)
    generic = (x-1)*(x-2)
    assert generic % (2*d)==0
    classes = generic//(2*d)+1
    return {"dimension":d,"modulus":str(q),"assumption":"q independently certified prime; primality screen alone is not this certificate",
            "all_ratio_count_hex":format(x*x,"x"),
            "generic_ratio_count_hex":format(generic,"x"),
            "exact_generic_native_ideal_class_count_hex":format(classes,"x"),
            "short_orbit_count":2,"short_orbit_size":d,
            "all_other_orbit_size":2*d,
            "generic_classes_are_not_principal_ideal_classes":True,
            "counts_only_classes_represented_by_THIS_native_family":True}


def finite_classes(d,q):
    members = {a for a in itertools.product(range(q),repeat=d) if generic_source_member(a,q)}
    count = len(members)
    sizes = {}
    while members:
        a = min(members)
        orbit = class_orbit(a,q)["all_orbit_ratios"]
        assert orbit<=members
        members.difference_update(orbit)
        sizes[len(orbit)] = sizes.get(len(orbit),0)+1
    expected = source_class_count(d,q)
    assert count==int(expected["generic_ratio_count_hex"],16)
    assert sum(sizes.values())==int(expected["exact_generic_native_ideal_class_count_hex"],16)
    assert sizes[d]==2
    return {"d":d,"q":q,"all_ratios_checked":q**d,"generic_ratio_count":count,
            "exact_native_class_count":sum(sizes.values()),"orbit_size_histogram":{str(k):v for k,v in sorted(sizes.items())}}


def run_controls():
    finite = [finite_classes(d,q) for d,q in ((4,3),(8,3))]
    saved = json.loads(NATIVE.read_text())
    q = int(saved["q"])
    ratio = tuple(v % q for v in conjugate(tuple(map(int,saved["native_ratio"]))))
    native = class_orbit(ratio,q)
    orbit = native.pop("all_orbit_ratios")
    native["distinct_orbit_ratio_sha256"] = sorted(hashlib.sha256(json.dumps(a,separators=(",",":")).encode()).hexdigest() for a in orbit)
    return {"status":"NATIVE_CLASS_EQUIVALENCE_CLASSICAL_SHORT_ELEMENT_STILL_OPEN_REVIEW_PENDING",
            "complete_finite_source_orbits":finite,"same_saved_native_d64_kernel":native,
            "native_source_class_count":source_class_count(len(ratio),q),
            "mechanism":{"public_group":"D_d of order2d","rotation":"M->X^2*M","reflection":"M->-M^-1",
                         "right_unit_word":"X^k for R^k; j*X^k=X^-k*j for R^k*T",
                         "proof_dependencies":["ambient saturation equals O_0 on generic source","full real unit signatures","ambient units are central units times signed monomials or j multiples"],
                         "direct_ideal_class_identification_is_already_classical":True,
                         "general_nonprincipal_short_element_or_transport_algorithms_ruled_out":False},
            "claim_gate":{"efficient_short_element_algorithm":False,"independent_review":False,
                          "candidate_record_accepted":False,"novelty_claim":False,"speedup_claim_allowed":False},
            "dependency_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in (Path(__file__),ROOT/"theorems/native_rlwe_conductor_order.py",ROOT/"theorems/native_rlwe_quaternion_kernel.py",ROOT/"theorems/structured_edcp_upstream_mixing.py",NATIVE)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":report["status"],"finite":report["complete_finite_source_orbits"],
                      "native_orbit_size":report["same_saved_native_d64_kernel"]["orbit_size"],"claim_gate":report["claim_gate"]},indent=2))


if __name__=="__main__":
    main()
