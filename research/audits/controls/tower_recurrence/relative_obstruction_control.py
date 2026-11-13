from sage.all import *
proof.all(True)
Qx = PolynomialRing(QQ, 'x'); x = Qx.gen()
F = NumberField(x*x+14, 'a'); a = F.gen()
S = F.primes_above(2)+F.primes_above(7)
E = F.primes_above(3); T = S+E
RF = PolynomialRing(F, 'z'); z = RF.gen()
L = F.extension(z*z-2, 'b'); b = L.gen()
A = L.absolute_field('t'); fromA, toA = A.structure()
SA = A.primes_above(2)+A.primes_above(7)
FS, fg, ff, ft = F.selmer_space(S, ZZ(2), proof=True)
FT, tg, tf, tt = F.selmer_space(T, ZZ(2), proof=True)
LS, lg, lf, lt = A.selmer_space(SA, ZZ(2), proof=True)
base = [F(-1), F(2), a, (a-2)/9]
betas = [3*(b-1), b+2, (a/4-1)*b-F(1)/2,
         (-(a+10)*b+2*(a+7))/12]
def parity_column(beta):
    xx, yy = map(F, beta.list())
    return vector(GF(2), [ZZ(min(xx.valuation(P),
        yy.valuation(P)+F(2).valuation(P)/2)) % 2 for P in E])
J = matrix(GF(2), [parity_column(t) for t in betas]).transpose()
W = matrix(GF(2), [[ZZ(t.valuation(P)) % 2 for t in tg] for P in E])
O = W.left_kernel().basis_matrix()*J
out = [L(-1), L(a), L((a-2)/9), F(3)*betas[0], betas[1], betas[2]]
outcoords = matrix(GF(2), [lt(toA(t)) for t in out])
normcols = matrix(GF(2), [ft(F(fromA(t).relative_norm()))
                        for t in lg]).transpose()
assert F.class_group(proof=True).invariants() == (4,)
assert F.S_class_group(S=S, proof=True).invariants() == (2,)
assert FS.dimension() == 4 and FT.dimension() == 5
assert matrix(GF(2), [ft(t) for t in base]).rank() == 4
assert all(F.hilbert_symbol(t, F(2), P) == 1 for t in base for P in S)
assert W.rank() == O.rank() == 1 and O.right_kernel().dimension() == 3
assert list(O.row(0)) == [0, 0, 0, 1]
assert W*tt(F(3)) == J.column(0)
assert outcoords.rank() == LS.dimension() == 6 and normcols.rank() == 3
assert A.discriminant() == 3136 and L.relative_discriminant() == F.ideal(1)
assert [t.relative_norm() for t in betas] == [F(-9), F(2), a, base[3]]
assert all(not F.residue_field(P)(2).is_square() for P in E)
print('EXACT_CONTROL_PASS')
