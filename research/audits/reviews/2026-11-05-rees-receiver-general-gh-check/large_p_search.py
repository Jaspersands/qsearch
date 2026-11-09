"""Does the module's constant search refuse primes OUTSIDE E_2(kappa) above 2*10^6 (alpha-scan cap)?
Also: the cost of G.Config's Encoding tables in p. Referee script, AI-written, pending human review."""
import json, sys, time, math
sys.path.insert(0, "/Users/jaspersands/Developer/qsearch")
from theorems.rees_coherent_sde_kappa import _kappa_constants, contraction_valid, coset_generator
from theorems.rees_coherent_sde import is_prime
from theorems.rees_circuit_general import Encoding

out = {"search": [], "encoding": []}
for kappa in (3, 4, 5, 6, 7):
    found = 0
    p = 2*10**6+1
    while found < 4:
        p += 1
        if (p-1) % kappa or not is_prime(p):
            continue
        found += 1
        t0 = time.time()
        try:
            C = _kappa_constants(p, kappa)
            ok = contraction_valid(p, kappa, C["g"], C["alpha"], C["beta"])
            r = {"kappa": kappa, "p": p, "result": "constructed", "valid": ok}
        except RuntimeError as e:
            r = {"kappa": kappa, "p": p, "result": f"RuntimeError: {e}"}
        except ValueError as e:
            r = {"kappa": kappa, "p": p, "result": f"ValueError: {e}"}
        r["seconds"] = round(time.time()-t0, 1)
        print(json.dumps(r), flush=True)
        out["search"].append(r)
        if time.time()-t0 > 120:
            break
for p in (61, 127, 251, 509):
    t0 = time.time()
    Encoding(p)
    r = {"p": p, "encoding_seconds": round(time.time()-t0, 2)}
    print(json.dumps(r), flush=True)
    out["encoding"].append(r)
json.dump(out, open("large_p_search.json", "w"), indent=1)
