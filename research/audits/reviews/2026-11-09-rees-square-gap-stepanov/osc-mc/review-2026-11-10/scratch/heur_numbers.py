"""Referee scratch: HEURISTIC.md numbers, with the even-kappa correction (non-split involutions contribute 0)."""
import math
Ninv = lambda k: math.comb(k, 2) * math.comb(k - 2, 2) // 2
logT = {7: 5.57, 8: 6.18, 9: 6.78, 10: 7.36, 6: 5.14}          # group (0.5, 1.6) row of the 11.8 table
for k in range(6, 11):
    e = 2 if k % 2 == 0 else 1
    A_doc = Ninv(k) ** 2 * e * k ** 4; A_cor = Ninv(k) ** 2 * k ** 4
    T = k ** logT[k]
    print('k=%d N_inv=%d  R22*p^2: HEURISTIC %.4g  corrected %.4g   at T=%.3g: %.3g -> %.3g' % (k, Ninv(k), A_doc, A_cor, T, A_doc / T ** 2, A_cor / T ** 2))
k = 6; A = Ninv(6) ** 2 * 6 ** 4
print('k=6 corrected R22: ' + '  '.join('%d:%.3f' % (p, A / p ** 2) for p in (1597, 1621, 1657, 1933, 2347, 3877)) + '   =1 at p=%.0f' % math.sqrt(A))
print('k=6 R_full*p^4 = %.4g (HEURISTIC 4.9e11; split-only with e=2 would be %.4g)' % (math.prod(range(1, 6, 2)) ** 2 * 6 ** 12, 2 * math.prod(range(1, 6, 2)) ** 2 * 6 ** 12))
# F = measured structured rate / corrected R22, using exact shares
data = {1621: ((0.724, 0.789), 0.423), 1597: ((0.860, 0.875), 4.360), 1657: ((0.830, 0.833), 4.468), 1933: ((0.700, 0.762), 2.632), 2347: ((0.444, 0.444), 0.759), 3877: ((0.167, 0.167), 0.853)}
for p, (sh, n1) in data.items():
    R = A / p ** 2
    print('  F(%d) = %.2f-%.2f  (uns rate N1/mu1 %.3f-%.3f)' % (p, sh[0] * n1 / R, sh[1] * n1 / R, (1 - sh[1]) * n1, (1 - sh[0]) * n1))
A7 = Ninv(7) ** 2 * 7 ** 4
for p, sh, n1, ns in ((35281, 0.043, 0.88, 19), (35099, 0.011, 0.93, 5)):
    R = A7 / p ** 2
    print('  k=7 p=%d: R22 %.4f, expected share %.3f, measured %.3f (%d structured conf), F = %.2f' % (p, R, R / n1, sh, ns, sh * n1 / R))
