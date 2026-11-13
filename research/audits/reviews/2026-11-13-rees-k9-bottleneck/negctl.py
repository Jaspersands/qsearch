#!/opt/anaconda3/bin/python
"""Negative controls for chain_exec.py: (1) perturb one alpha of the 37 stage witness; (2) claim the stage is a
{0,5}-node instead of {0,4}; (3) drop the finish class check by using a K-node whose classes are not in Tn.
Each must be caught (assertion or failed verification)."""
import random, chain_exec as CE
rng = random.Random(5)
p, kap, plan = CE.PLANS['p37']
orig = CE.rc_witness.__wrapped__
def bad(p_, D, R, K):
    al, be = orig(p_, D, R, K)
    if D == 9 and R == (0, 3, 6):
        al = list(al); al[2] = (al[2] + 1) % p_; al = tuple(al)
    return al, be
def trial(pl, wit=None):
    caught = 0
    for t in range(20):
        if wit: CE.rc_witness = wit
        try:
            L = [[rng.randrange(p) for _ in range(2)] for _ in range(CE.plan_arity(p, kap, pl, 2))]
            x = CE.run(p, kap, pl, L, 2)
            caught += not CE.verify(x, L, p, kap, 2)
        except (AssertionError, KeyError, StopIteration) as e:
            caught += 1
        finally:
            CE.rc_witness = CE.functools.lru_cache(None)(orig)
    return caught
print('perturbed stage alpha: caught', trial(plan, bad), '/ 20')
print('stage declared {0,5}:  caught', trial((('ch', 5, [(3, (0,)), (9, (0, 4))]), plan[1])), '/ 20')
print('finish K={0,1,2,3} (not a shift-subset of Tn classes {0,2,3,5}): caught', trial((plan[0], ('F3', [(9, (0, 1, 2, 3))]))), '/ 20')
