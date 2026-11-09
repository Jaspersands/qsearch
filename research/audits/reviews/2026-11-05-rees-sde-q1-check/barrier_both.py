"""When can BOTH fallbacks of the code's ALG-Q1 (Y- and U-recursion) fail at a case-4 stall?
Pure counting, independent of the absorption rule.  At a stall (q >= 3, b >= q-1, eps >= 1,
r = q+b+eps, M >= f(r)), with R = |Rcols| <= D_3(r)-D_3(q), Rout = round columns outside U, |T| <= q:
  cols(Y) >= b + pi,  cols(U) = b + pi + (R - Rout),  pi = M - r - R - |T|.
  Y fails  =>  R + |T| >= f(r) - r + b - f(b) + 1
  U fails  =>  Rout + |T| >= f(r) - r + b - f(r-q) + 1,   Rout <= R.
(crude: Rout <= R <= D_3(r)-D_3(q)).  For q = 3 also the structural bound: load >= 3 forces all of
Rout into one round l*, so Rout <= |S_l*| <= r+1."""
from myq1 import D3, f

first_crude = first_q3 = None
for r in range(3, 200):
    crude, q3 = [], []
    for q in range(3, r // 2 + 1):
        for b in range(q - 1, r - q):
            eps = r - q - b
            if eps < 1:
                continue
            Rmax = D3(r) - D3(q)
            NY = f(r) - r + b - f(b) + 1
            NU = f(r) - r + b - f(r - q) + 1
            if Rmax + q >= NY and Rmax + q >= NU:
                crude.append((q, b, eps))
                if q == 3 and (r + 1) + 3 >= NU:
                    q3.append((q, b, eps))
    if crude and first_crude is None:
        first_crude = r
        print("crude: first r =", r, crude[:5])
    if q3 and first_q3 is None:
        first_q3 = r
        print("q=3 structural: first r =", r, q3[:5])
    if first_crude and first_q3:
        break
print("first r (crude, any q):", first_crude, " first r with a q=3 shape:", first_q3)

# first r with a crude both-fail shape having q >= 4 (q = 3 shapes are excluded below r = 39 by the
# structural bound, under minimum-load absorption)
for r in range(3, 200):
    sh = []
    for q in range(4, r // 2 + 1):
        for b in range(q - 1, r - q):
            eps = r - q - b
            if eps < 1:
                continue
            Rmax = D3(r) - D3(q)
            if Rmax + q >= f(r) - r + b - f(b) + 1 and Rmax + q >= f(r) - r + b - f(r - q) + 1:
                sh.append((q, b, eps))
    if sh:
        print("crude, q >= 4: first r =", r, sh[:5])
        break
