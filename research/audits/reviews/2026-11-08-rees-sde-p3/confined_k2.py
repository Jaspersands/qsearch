"""Which pattern sets T in F_3^2 \ 0 (two dependencies) admit a class-union realization
of a 2-dim subgroup?  Uses the defect formulation: local assignment y: F_3^2 -> {0,1},
y(0)=0, defect e(y) = (y(a) - a1 y(e1) - a2 y(e2))_{a not in {0,e1,e2}} in F_3^6.
Realization with patterns T: a linear C: F_3^2 -> F_3^6 with C(pi) in E for pi in T, rank C = 2
(rank <= 1 gives at most one dimension), plus per-class local y's with every y_alpha != 0.
Two variants: 'multi' (a class may hold several columns with different local y's) and
'single' (exactly one column per pattern class)."""
import itertools
from generic_piece import defect_set
others, E = defect_set(2)
alphas = [a for a in itertools.product(range(3), repeat=2) if any(a)]
units = [(1,0),(0,1)]
# local assignments by defect: Y[e] = list of bit-tuples (indexed by alphas)
Y = E  # dict defect -> list of bits
Es = set(E); zero6 = (0,)*6
def lin(u, v, a, b): return tuple((a*x + b*y) % 3 for x, y in zip(u, v))
pats = alphas  # nonzero patterns in F_3^2
vecs = [v for v in itertools.product(range(3), repeat=6)]
# candidate images for e1, e2 must themselves be in E u {0} only if e1, e2 in T; enumerate all pairs (u,v) independent
results = {}
Eu0 = Es | {zero6}
for u in vecs:
    for v in vecs:
        if u == zero6 and v == zero6: continue
        if v in (u, lin(u,u,2,0)) or u == zero6 or v == zero6: continue  # need rank 2
        # patterns pi=(a,b) with C pi = a u + b v in E u {0}
        good = frozenset(pi for pi in pats if lin(u, v, pi[0], pi[1]) in Eu0)
        if len(good) < 4: continue
        # realizability of y_alpha != 0 (multi variant): union over pi in good of supports of Y[Cpi]
        cov_multi = set(); cov_single_possible = None
        choices = []
        for pi in good:
            e = lin(u, v, pi[0], pi[1])
            ys = Y.get(e, [()]) if e != zero6 else [tuple([0]*8)]
            choices.append(ys)
            for y in ys:
                for j, bit in enumerate(y):
                    if bit: cov_multi.add(alphas[j])
        if len(cov_multi) < 8: continue
        results.setdefault(good, 0); results[good] += 1
# maximal feasible T (multi variant)
feas = set(results)
# all subsets of feasible are feasible (dropping patterns keeps C valid, may lose coverage) -> report maximal ones
maximal = [T for T in feas if not any(T < S for S in feas)]
print("number of feasible pattern sets T (multi variant, rank-2 C, all y_alpha != 0 coverable):", len(feas))
print("max |T| feasible:", max(len(T) for T in feas))
print("maximal feasible T's:")
for T in sorted(maximal, key=lambda T: (-len(T), sorted(T))):
    print("  |T|=%d:" % len(T), sorted(T))
# check: does any feasible T contain both (a,b) and all three of {(a,0),(a,1),(a,2)} for a nonzero (a full 'cylinder')?
def has_cyl(T):
    for a in (1,2):
        if all((a,b) in T for b in range(3)): return True
    for b in (1,2):
        if all((a,b) in T for a in range(3)): return True
    return False
print("feasible T containing a full cylinder {a}xF_3 or F_3x{b}:", sum(has_cyl(T) for T in feas))
