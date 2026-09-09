"""Curated first proof-route contracts; pin only on explicit initialization.

These declarations are review-pending mathematical attestations, not extracted
proofs. Do not regenerate hashes to conceal a provenance failure.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from proof_provenance import MANIFEST_PATH


def build_initial_proof_routes(root: Path = Path(".")) -> dict:
    claims, evidence = [], []

    def claim(identifier, domain, model, conclusion, *, level="unresolved", quantifier="universal"):
        row = {"id": identifier, "scope": {"domain": domain, "input_model": model,
               "conclusion": conclusion, "quantifier": quantifier}, "asserted_level": level, "routes": []}
        claims.append(row)
        return row

    def attest(node, path, suffix, *, level="derived-review-pending", predicates=()):
        identifier = f"E-{node['id']}-{suffix}"
        evidence.append({"id": identifier, "path": path, "sha256": hashlib.sha256((root / path).read_bytes()).hexdigest(),
                         "claim_id": node["id"], "scope": node["scope"], "level": level, "predicates": list(predicates)})
        return identifier

    def route(node, identifier, reference, *premises, diagnostics=()):
        node["routes"].append({"id": identifier, "conclusion_evidence": [reference],
                               "premises": list(premises), "diagnostics": list(diagnostics)})

    baba = "single-base-fiber BABA marked presentations from binary codes of size 2^r and distance at least two"
    model = "explicit ordered codeword relators; n grows with code width"
    cubic = claim("CUBIC-LOCAL-LOSS", "all normalized proper binary face-color triples at growing check width", model,
                  "every nonempty cubic-overlap face has uniform symmetric-group solution-exponent loss at least one half")
    local = claim("LOCAL-SYSTEMATIC-BOUND", baba + " with a systematic information set", model,
                  "the local face/deviation/block proof gives a uniform one-half exponent loss")
    route(local, "local-face", attest(local, "theorems/self_dual_wreath_systematic_stopping_core_no_go.py", "local"), cubic["id"])

    suffix = claim("SUFFIX-ELIMINATION", baba, model, "suffix witnesses permit at least r triangular appended-generator eliminations",
                   level="derived-review-pending")
    route(suffix, "suffix-entropy", attest(suffix, "theorems/self_dual_wreath_frame_subword_entropy.py", "source"))
    surface = claim("SURFACE-ABSORPTION", "all coefficient words disjoint from the five surface generators", model,
                    "the invertible Nielsen substitution absorbs the coefficient into the fixed genus-two relation", level="derived-review-pending")
    route(surface, "nielsen", attest(surface, "theorems/self_dual_wreath_codimension_two_universal_no_go.py", "source"))
    global_bound = claim("GLOBAL-BABA-BOUND", baba, model, "solution exponent is at most d+4 by global suffix/surface elimination",
                         level="derived-review-pending")
    route(global_bound, "global", attest(global_bound, "theorems/self_dual_wreath_all_codimension_baba_no_go.py", "source"), suffix["id"], surface["id"])
    systematic = claim("SYSTEMATIC-BABA-BOUND", baba + " with a systematic information set", model,
                       "a uniform solution-exponent loss of at least one half holds", level="derived-review-pending")
    route(systematic, "old-local", attest(systematic, "theorems/self_dual_wreath_systematic_stopping_core_no_go.py", "local"), local["id"])
    route(systematic, "independent-global", attest(systematic, "theorems/self_dual_wreath_all_codimension_baba_no_go.py", "global"), global_bound["id"])

    access = claim("ENCODED-RESTRICTION", "known K=C2 wr S_m inside S_(2m)",
                   "real Young-basis physical Fourier column; efficient compatible group QFT primitives supplied",
                   "normalized carrier extraction with an implicit copy code costs two group QFTs plus polynomial reversible arithmetic",
                   level="derived-review-pending")
    check = attest(access, "research/representation/coset_hidden_involution_encoded_restriction.json", "diagnostic", level="observed",
                   predicates=[{"pointer": "/claim_gate/finite_encoded_isometry_verified", "equals": True},
                               {"pointer": "/claim_gate/physical_real_symmetric_column_convention_verified", "equals": True}])
    route(access, "two-qft", attest(access, "research/ENCODED_RESTRICTION.md", "derivation"), diagnostics=[check])
    access["routes"][0]["conclusion_evidence"].append(attest(access, "theorems/coset_hidden_involution_encoded_restriction.py", "source"))

    identification = claim("FIXED-REFERENCE-IDENTIFICATION-BOUND", "uniform fixed-point-free involutions in S_(2m)",
                           "any copy count; complete final POVM invariant under one known reference K",
                           "average exact identification success is at most p(m)/(2m-1)!!", level="derived-review-pending")
    route(identification, "orbit-likelihood", attest(identification, "research/ENCODED_RESTRICTION.md", "derivation"))
    claim("BINARY-DETECTION-IMPOSSIBLE", "identity versus uniform hidden-involution class mixture", "physical coset states",
          "efficient binary detection is impossible")
    claim("HIDDEN-INVOLUTION-DECODER", "full reduction-backed hidden-involution family", "physical coset-state samples",
          "a polynomial-time hidden-involution decoder with bounded error exists")
    twirl_doc = "research/REFERENCE_TWIRL_INFORMATION.md"
    twirl_source = "theorems/coset_hidden_involution_reference_twirl_information.py"
    purity = claim("REFERENCE-ORBIT-BLOCK-PURITY", "nonidentity involutions in one reference-conjugacy orbit O of S_(2m)",
                   "b physical coset copies of the same h, diagonally twirled within the block",
                   "|G|^b Tr(sigma_O,b^2)-1 = (2^b-1)/|O|", level="derived-review-pending")
    fixed = claim("PREDETERMINED-REFERENCE-TWIRL-INFORMATION", "uniform fixed-point-free involutions in S_(2m)",
                  "independent disjoint block twirls with outcome-independent known references; arbitrary later joint processing",
                  "squared half trace distance is at most min(1, p(m)/(2(2m-1)!!) sum_j(2^b_j-1))", level="derived-review-pending")
    adaptive = claim("ADAPTIVE-PREINTERACTION-REFERENCE-TWIRL", "uniform fixed-point-free involutions in S_(2m)",
                     "at most t classical adaptive reference rounds; fresh blocks twirled before quantum-memory interaction; no other h-dependent resource",
                     "squared half trace distance is at most min(1, t*p(m)/(2(2m-1)!!) sum_j(2^b_j-1))", level="derived-review-pending")
    for node, name, premises in ((purity, "regular-orthogonality", ()),
                                 (fixed, "entropy-additivity", (purity["id"],)),
                                 (adaptive, "null-prefix-hybrid", (purity["id"],))):
        route(node, name, attest(node, twirl_doc, "derivation"), *premises)
        node["routes"][0]["conclusion_evidence"].append(attest(node, twirl_source, "source"))
    return {"schema_version": 1, "scope": "Curated review-pending route attestations, not formal proofs or exhaustive repository coverage.",
            "claims": claims, "evidence": evidence}


def initialize_proof_routes(path: Path = MANIFEST_PATH, root: Path = Path(".")) -> dict:
    manifest = build_initial_proof_routes(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
    return manifest
