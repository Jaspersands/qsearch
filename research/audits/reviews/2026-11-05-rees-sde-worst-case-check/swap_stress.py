"""Forward-pass stress test of Theorem 2(b),(d) on general-position (moment-curve) banks at small p,
where columns landing in U are frequent.  With swaps: no stall and pi = 0 must hold for every bank.
Without swaps (control): the would-be swaps are discarded and stalls may occur."""
import random
from mysss import F, D, forward
from run_check import moment_bank, is_gp
rng = random.Random(31337)
tot = {"banks": 0, "swaps": 0, "pi": 0, "stall": 0, "ns_stall": 0, "ns_disc": 0, "gp_checked": 0}
for k, p, a in ((2, 11, 3), (2, 13, 4), (2, 17, 4), (2, 23, 5), (2, 29, 5), (2, 31, 5), (2, 37, 6),
                (3, 13, 3), (3, 19, 4), (3, 31, 5), (3, 37, 5), (3, 43, 6), (3, 67, 6), (3, 79, 7)):
    Fd = F(p, k)
    M = D(3, a) + a
    if M > p + 1:
        continue
    loc = dict(swaps=0, pi=0, stall=0, ns_stall=0, ns_disc=0)
    for t in range(300):
        cols = moment_bank(p, a, M, rng, rng.choice(["random", "one", "nr"]), Fd)
        if t < 30 and a <= 5:
            assert is_gp(cols, p)
            tot["gp_checked"] += 1
        order = list(range(M))
        rng.shuffle(order)
        run = forward(Fd, cols, 3, order=order)
        loc["swaps"] += run.get("swaps", 0)
        loc["pi"] += run.get("pi", 0)
        loc["stall"] += run["status"] == "stall"
        run0 = forward(Fd, cols, 3, swap=False, order=order)
        loc["ns_stall"] += run0["status"] == "stall"
        loc["ns_disc"] += len(run0.get("discarded", []))
        tot["banks"] += 1
    for key in loc:
        tot[key] += loc[key]
    print(f"kappa={k} p={p} a={a} M={M} banks=300: {loc}", flush=True)
print("TOTAL", tot)
print("Theorem 2(d) consistent:", tot["pi"] == 0 and tot["stall"] == 0)
