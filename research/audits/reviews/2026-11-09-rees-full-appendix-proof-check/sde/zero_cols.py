"""Finding 3: rem:sde-worst-case-q1(i) says U_L != 0 whenever the bank has at least D_3(r)+r
columns.  Counterexample with zero columns: e1, e2 and D_3(2) = 4 zero columns (6 = D_3(2)+2
columns).  Every zero column is a true-pool event at U = 0, so the forward pass of
rem:sde-worst-case(b) stalls with U_L = 0.  Control: the same count of nonzero columns."""
import random, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from steer import Field, reserved_forward

F = Field(7, 2)
bank = [(1, 0), (0, 1), (0, 0), (0, 0), (0, 0), (0, 0)]
status, rounds, B, U, pi = reserved_forward(F, bank, J=3)
print("bank", bank, "->", status, "dim U_L =", len(U), "true-pool events =", pi, "rounds =", len(rounds))
rng = random.Random(3)
bad = 0
for trial in range(2000):
    p = rng.choice([7, 11, 13, 31])
    F = Field(p, 2)
    while True:
        bank = [tuple(rng.randrange(p) for _ in range(2)) for _ in range(6)]
        if all(v != (0, 0) for v in bank) and any((u[0] * v[1] - u[1] * v[0]) % p for u in bank for v in bank):
            break
    status, rounds, B, U, pi = reserved_forward(F, bank, J=3)
    if status == 'stall' and len(U) == 0:
        bad += 1
print("control: 2000 random rank-2 banks of 6 nonzero columns, stalls with U_L = 0:", bad)
