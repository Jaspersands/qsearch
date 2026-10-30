# Quaternion Norm Slices And Public Local Flags

Date: 2026-10-30. Status: independently reviewed mathematical interfaces and
bounded exact controls, NOT an implemented quantum algorithm or novelty claim.
Five agents divided the primary-source audit, rational classical baseline,
local-orbit audit, exact controls, and adversarial review. Their reviews are
automated, not external human peer review or Lean certification.

## Decision

The useful unresolved problem is growing-degree, norm-constrained quaternion
principalization with the correct positive metric. Rational definite PIP is
already classically polynomial. A Borel HSP built from the orbit of an
explicit local ideal image recovers a flag already available by elimination.
Neither route is a new quantum mechanism.

There is a precise constructive target: for real power-of-two cyclotomic
centers, a length approximation strictly better than sqrt(2) in the weighted
norm below recovers an exact norm target. For general totally real centers,
sqrt(7/4) suffices with explicit central-unit corrections. These are
sufficient interfaces, not algorithms achieving those approximation factors.
Exact weighted SVP principalization is already prior art.

## 1. Native Input And Prior Art

Let F be totally real of degree d, B/F a totally definite quaternion algebra,
and O an explicit O_F-order. Supply a full ideal I by a Z-basis, a totally
positive q in F, and a verified equality nrd(I)=q O_F. All field structure,
order action, basis conversion and bit lengths are charged inputs. We use
LEFT ideals I=O alpha in our fixtures. The Hawk paper uses RIGHT ideals
I=g O; conjugation translates conventions, but multiplication order must
not be silently exchanged.

The target is a nonzero x in I with nrd(x)=q. For locally principal ideals,
equality of norm ideals then proves x generates I. Alternatively verify
the generated lattice equals I directly. Without either condition, do not
infer principality solely from a norm-ideal equality.

[Hawk/module-LIP, ePrint 2025/287](https://eprint.iacr.org/2025/287), the
2025-02-19 version, Definition 2.18 p12, specifies this exact norm problem,
not unrestricted ordinary PIP. Its solution ambiguity is the norm-one unit
group, not all units. Corollary 3.9 p21 gives the general nonuniform reduction;
Corollary 4.4 p27 gives the uniform cyclotomic case. The growing lattice rank
is 4d. A fixed quaternion presentation does not make that rank constant.

[Kirschmer--Voight's corrected Algorithm 6.3](https://jvoight.github.io/articles/quatideal-fixed-errata-111614.pdf),
p22, already searches shortest vectors in exactly this kind of weighted
trace form, over appropriate positive-unit square classes. See also their
[addendum](https://jvoight.github.io/articles/quatideal-errata-102320.pdf), p3.
Do not relabel that reduction as a new discovery. Their fixed-field
complexity statement is not uniform polynomial time in growing degree.

The cached full Hawk paper supersedes the earlier abstract-only audit:
`literature_cache/eprint_2025_287_20250219.pdf`, 47 pages, 908323 bytes,
SHA-256 `785b9a5b6f33074fb08a1959226976c64c45aa9e795445ed067b3435a1347577`.

## 2. Rational Definite PIP Is An Easy Baseline

For an arbitrary explicit unital order O in a definite quaternion algebra
over Q and a full integral left ideal I, every nonzero alpha in I satisfies

```text
O alpha subset I,
[O:I] [I:O alpha] = det(right multiplication by alpha) = nrd(alpha)^2.
```

Reduced norms of elements of O are positive integers. If [O:I] is not a
square, I is not principal. If [O:I]=r^2, all nonzero norms in I are at least
r, and equality holds precisely for a generator. Exact positive-definite
SVP in dimension four is polynomial in the expanded input bit length.
This argument requires neither a maximal order nor an ideal-class
enumeration or factorization of the index. Clear explicit denominators for
fractional ideals. It does not solve arbitrary prescribed norms,
congruence-constrained generators, or another metric's short-vector problem.

Exact matched controls use B=(-1,-11)_Q and
O=Z[1,i,(1+j)/2,(i+ij)/2]. With coordinates (a,b,c,e),

```text
nrd = a^2+a*c+3*c^2 + b^2+b*e+3*e^2
    = (a+c/2)^2+(b+e/2)^2+(11/4)(c^2+e^2).
```

The left ideal O(1+i) has index 4 and minimum norm 2. The left ideal
defined by a+e=0 and b+c=0 modulo 2 also has index 4 and norm ideal 2Z,
but minimum norm 4. The square completion excludes c or e nonzero at norm
2; the remaining vectors violate parity. Witness norms 4 and 6 certify
the norm ideal. Thus norm-ideal information alone does not find a generator.

Even a fixed quadratic slice can miss an existing generator: intersecting
O(1+i) with Q(j) gives 2Z+2Z(1+j)/2, whose minimum norm is 4, not 2.
This only refutes that slice, not an adaptive choice of subfield.

## 3. Exact Weighted Norm And Output Size

For nonzero x in I, set zeta=nrd(x)/q. This is a totally positive algebraic
integer, by the norm-ideal contract. Define

```text
Q_q(x) = Tr_(F/Q)(nrd(x)/q),
G_ij = (1/2) Tr_(F/Q)(q^-1 trd(b_i conjugate(b_j))).
```

Then Q_q(x)=z^T G z for ideal-basis coordinates z. G is rational positive
definite and computable using exact multiplication and trace matrices;
floating-point embeddings are unnecessary. Its construction has polynomial
bit cost in the expanded field, basis and q data. Diagonal entries and
twice the off-diagonal entries are integral.

AM--GM gives Q_q(x)>=d Norm(zeta)^(1/d)>=d. Equality implies all conjugates
of zeta equal one, and hence nrd(x)=q. On an attainable exact-q instance,
the squared shortest-vector length is therefore d. Attainability must not
be inferred merely from ordinary principality.

Every exact-q witness has coordinate bound
`|z_i|^2 <= d*(G^-1)_ii`, by Cauchy--Schwarz in G. Exact rational inverse
entries have polynomial bit length. Thus an expanded exact-q witness has
polynomial size in these inputs even when d grows. This does not bound
arbitrary ordinary-PIP generators, compactly represented q, or the time to
find a bounded witness.

## 4. A Quantitative Approximation Interface

The length guarantee is `Q_q(x) <= gamma^2*lambda_1^2`; gamma is NOT a
squared-length factor. On an exact-q YES input, lambda_1^2=d.

[Smyth's primary theorem](https://www.numdam.org/article/AIF_1984__34_3_1_0.pdf),
printed p2, classifies the exceptional totally positive algebraic integers
of normalized trace below 1.7719. Below 7/4 only 1, the roots of
`Z^2-3Z+1`, and the roots of `P(Z)=Z^3-5Z^2+6Z-1` remain. Normalized trace
is unchanged on extending from Q(zeta) to F. Consequently gamma<sqrt(7/4)
permits the following exact correction:

```text
zeta=1:                  return x.
zeta^2-3*zeta+1=0:       u=zeta-1,       u^-1=zeta-2.
P(zeta)=0:               u=zeta^2-3*zeta+1,
                        u^-1=zeta^2-4*zeta+3.
Return u^-1*x in the latter two cases.
```

The polynomial identities `u^2=zeta` and `u*u^-1=1` show that these are
integral central units. Scalar correction preserves I and divides the
reduced norm by zeta. Direct polynomial evaluation suffices; no unknown
generator, unit-group search or minimal-polynomial computation is required.
On a NO input, an exact norm check prevents a false YES. The reduction's
completeness still depends on the promised SVP algorithm.

Do not assert the original sqrt(3/2) boundary is an impossibility: over
Q(sqrt(5)), the scalar golden-ratio unit has trace-normalized norm 3/2 and
is corrected as above. Nor extend the universal correction through 7/4:
one exceptional quartic, `Z^4-7Z^3+14Z^2-8Z+1`, has roots that are not
squares in their own degree-four field. This is a limitation of the stated
central correction, not a lower bound for other algorithms. The primary
Smyth paper has the correct quadratic middle terms; the cached 2008 survey
excerpt has typographical cubic exponents in those two quartics.

### Stronger Power-Of-Two Center

Let F=Q(xi+xi^-1), xi a primitive 2^k root, k>=3, and d=2^(k-2).
The full integral basis is
`1, t_j=xi^j+xi^-j (1<=j<d)`.
Indeed, in the integral basis `1,xi,...,xi^(2d-1)` of Q(xi), conjugation
sends xi^j to -xi^(2d-j). Its fixed integral vectors have zero xi^d
coefficient and opposite coefficients at those paired positions. This
proves completeness, not just independence of the displayed real basis.

For 1<=j<d, summing odd powers of xi gives Tr_F(t_j)=0, whereas Tr_F(1)=d.
Thus `Tr(O_F)=d Z`. Every Q_q(x)/d is a positive integer; AM--GM makes
value 1 equivalent to the exact norm target. Any other value is >=2.
Therefore **gamma<sqrt(2) suffices without a unit correction**. At equality,
the Hamilton element 1+i of norm 2 is already an off-target control for
q=1, I=O. No universal guarantee at equality follows. This is not unique-SVP;
the shortest shell can contain many independent vectors.

In these fields all totally positive units are squares: full unit
signature rank is [Dummit--Dummit--Kisilevsky, Proposition 3](https://msp.org/pjm/2019/298-2/pjm-v298-n2-p03-p.pdf),
printed p291. Thus if an ordinary generator h is already explicitly found,
epsilon=nrd(h)/q is a positive unit and a field square root s gives h/s
of exact norm q. This does not find h or justify cheaply expanding a compact
h. The real missing operation is quaternion principalization, not a newly
postulated unit-sign barrier.

### Essential Countercontrols

For F=Q(sqrt(3)), the Hamilton Lipschitz order I=O is principal and
q=2+sqrt(3) is a positive unit, so nrd(I)=q O_F. But every norm in O is a
sum of four squares in Z[sqrt(3)] and has even sqrt(3) coefficient. No norm
equals q. This disproves ordinary principality implying attainability for
general centers/orders.

For F=Q(sqrt(2)), x=(1+sqrt(2))/2+i/2 has norm 1+sqrt(2)/2, of trace 2
but not equal to 1. It lies in (1/2)O whose norm ideal is (1/4)O_F, not
O_F. The failed hypothesis is norm normalization, not fractionality itself.

## 5. The Public Local-Flag Construction Is Classically Solved

Assume an explicit computable split chart rho:O/pO -> M_2(k). Reduce the
public ideal basis to its AMBIENT image L=rho(I), not the abstract I/pI.
Every left ideal of M_2(k) consists of matrices whose rows lie in a public
row space W. If I=O alpha and A=rho(alpha), then L=M_2(k)A and W=rowspan(A).
Stacking rows of the given image generators finds W and its annihilator
K by classical Gaussian elimination, without finding alpha.

```text
K = intersection of right kernels of public image generators,
K(Lg) = g^-1 K,
Stab_right(L) = {g in GL_2(k): gK=K},
Stab_left(L) = GL_2(k).
```

Rank one gives a Borel subgroup with its flag already known. Rank zero or
two gives the whole group and no hidden line. For A=diag(1,0), K=<e_2>
and the right stabilizer is LOWER triangular. Canonical(Lg) labels right
cosets H g; invert g to convert to the usual left-coset convention.

Prime-power precision does not change the public-information conclusion,
but it changes the group. In Smith coordinates over R=D/pi^e,

```text
W=pi^a R e_1^T + pi^b R e_2^T, 0<=a<=b<=e,
Stab(W)={[[x,y],[z,w]] in GL_2(R): y in pi^(b-a) R}.
```

This is the full group at a=b, triangular at (a,b)=(0,e), and otherwise
a congruence stabilizer. Use the full row module, not a fraction-field
kernel. Example diag(1,2) over Z/4 has nonfree kernel {(0,0),(0,2)} and
allows upper-right entry 2. Over Q its kernel is zero although its integral
row lattice still has a proper stabilizer.

Other controls: I=pO has zero ambient image but four-dimensional abstract
I/pI; individual rank-one module generators can generate the full ideal;
rebasing must not change the recovered flag. Matrices [[1,0],[0,15]] and
[[1,3],[0,15]] give different M_2(Z) left ideals with the same mod-3 flag
and determinant 15. This last example concerns one local flag, not complete
local data or a hardness theorem.

[Chen et al., arXiv:2305.19897](https://arxiv.org/pdf/2305.19897), Sections
2.4--2.5 and 3, instead give a hiding oracle for secret submodule data in
their relevant input models. Public ideal generators are not automatically
available there. The public-row attack does not break that encoded-isogeny
problem. Likewise, the [Dagstuhl report, Section 4.1](https://drops.dagstuhl.de/storage/04dagstuhl-reports/volume15/issue10/25431/html/DagRep.15.10.105/DagRep.15.10.105.html)
describes a partial Hawk/Borel approach without enough construction detail
to identify it with this wrapper. No refutation of that unpublished
construction is claimed.

## 6. Next Constructive Gate

The recent HSVP and QuaILLL papers are assessed separately in
[the version-scoped source audit](QUATERNION_HSVP_PREPRINT_AUDIT.md).
No quantum speedup candidate passes admission on the evidence here.

Two meaningful ways to reopen the route are:

1. Give a coherent, efficiently evaluable orbit function that retains
   generator-frame information NOT already public in a row module. State
   unit ambiguity, prove exact fibers, reconstruct an exact-q generator,
   and charge chart and query costs. Reject a function that needs the
   unknown generator to evaluate, or reduces to the public flag above.
2. Give an actual weighted short-vector method and compare against
   structure-aware classical reduction on the SAME I,q metric. Charge
   module-basis construction, all embeddings/precision, and matched real
   lattice block sizes. A finite improvement or a missed witness is not
   asymptotic advantage or a hardness certificate.

Number-field PIP, S-units, splitting a rational algebra, and restricting to
a fixed CM subfield do not by themselves do either job. A quaternion ideal
is generally rank two over that subfield; effective integral descent and
the norm target remain to be solved. Do not build another wrapper until
one of these specific mechanisms is supplied.

## Verification

`test_quaternion_pip_scope.py`: 23 controls; `test_quaternion_norm_slice.py`:
24 controls; `test_quaternion_local_flags.py`: 16 controls. They use exact
rational, number-field fixture and finite-field arithmetic with bounded
enumeration. They do not prove the quoted general theorems or implement
SVP, hidden-subgroup sampling, or a native Hawk attack.
