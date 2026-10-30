# Integral Similarity: Compact Answers Are Not Expanded Witnesses

Date: 2026-10-30. Scope: an explicit output-size theorem, not a decision
lower bound, new quantum algorithm, or claim that all arithmetic reductions
fail. The proof below is independent of any finite test range.
An independent adversarial agent review checked completeness, negative
exponents, the minimum over all witnesses, and the ideal correspondence.
This is automatic mathematical review, not external peer review or Lean.

## Exact Family

For an integer m >= 2, set f=2^m and define

```
A_f = [[0,             2*f^2],
       [1,                 0]]
B_f = [[f^2,           2*f^2],
       [1-f^2/2,        -f^2]].
```

Both matrices have characteristic polynomial x^2-2*f^2, irreducible and
separable over Q. Their total binary input length is O(m). They are
integrally similar, but EVERY integral unimodular C with B_f C=C A_f has
an entry whose binary length is at least 2^(m-1). Conversely, a witness
with O(2^m) bits exists. Thus the minimum expanded witness has exponential
size in the input length, already in dimension two.

The input matrices themselves are not required to be unimodular. This is
the similarity problem for Mat_2(Z), not a statement restricted to GL_2(Z)
input matrices. The conjugating matrix is unimodular.

## Complete Parameterization

Write C=[[a,c],[d,e]]. The first row of B_f C=C A_f gives

```
c = f^2*(a+2*d),       e = a-c/2.
```

The second row imposes no additional condition. Since f is even, every
integral solution can therefore be written uniquely as

```
C(a,b) = [[a,                  2*f*b],
          [b/f-a/2,              a-f*b]],
a,b in Z,       b == f*a/2 (mod f).
det C(a,b) = a^2-2*b^2.
```

Conversely, these conditions give an integral intertwiner. No rational
solutions with half-integral b have been lost: b=f*(a+2*d)/2 is integral
because f is even.

Unimodularity implies a^2-2*b^2=+1 or -1. The units of Z[sqrt(2)] are
exactly +/- epsilon^k for k in Z, where epsilon=1+sqrt(2). Write
epsilon^k=a_k+b_k*sqrt(2). For all nonzero k,

```
v_2(b_k)=v_2(k),       a_k is odd.
```

Indeed b_k is odd for odd positive k, and
b_(2k)=2*a_k*b_k with a_k odd. Factoring k into an odd part times a power
of two proves the valuation formula. The inverse of epsilon^k is
(-1)^k*(a_k-b_k*sqrt(2)), so negative exponents have the same valuations.
For completeness, the elementary Pell-unit classification follows by
multiplying a positive real unit by a power of epsilon into [1,epsilon):
the norm +/-1 condition leaves only the unit 1 in that interval. Overall
sign and conjugation cover the remaining units.

Because a is odd, the congruence in the parameterization is equivalent to

```
b == f/2 (mod f),       v_2(b)=m-1.
```

The exponent k=0 is excluded. Hence all witnesses satisfy
k == f/2 (mod f), in particular |k| >= f/2. These k are even since m>=2,
so all witnesses in this family actually have determinant +1.

For even k, |a_k|=(epsilon^|k|+epsilon^(-|k|))/2. Since epsilon>2,
|a_k|>2^(|k|-1), giving bit_length(|a_k|)>=|k|>=2^(m-1).
Taking k=f/2 attains an upper bound O(f) on every entry's bit length,
including the f factors in C. This proves both bounds without floating
point estimates or an assumed regulator growth law.

For m=2, the exact witness is

```
A = [[0,32],[1,0]]
B = [[16,32],[-7,-16]]
C = [[3,16],[-1,-5]],       det C=1,       B*C=C*A.
```

## Ideal Interpretation And The Conductor

Let theta=f*sqrt(2), R_f=Z[theta], and

```
J_f = Z*(2+theta) + Z*(2*theta).
```

In the bases (1,theta) of R_f and (2+theta,2*theta) of J_f,
multiplication by theta has matrices A_f and B_f, respectively. For the
second assertion, the coefficients of theta*(2+theta) are
(f^2,1-f^2/2), and those of theta*(2*theta) are (2*f^2,-f^2).
Thus J_f is an R_f-ideal of index four.

For k=f/2 the element gamma=2*epsilon^k belongs to J_f: its coordinates
are (a_k, b_k/f-a_k/2), both integral. Its norm is four. Therefore the
contained principal ideal gamma*R_f has the same index as J_f, proving

```
J_f = 2*epsilon^(f/2)*R_f.
```

R_f is nonmaximal, of conductor f in O_K=Z[sqrt(2)] and discriminant
8*f^2. Extending J_f to O_K gives 2*O_K. The large exponent is a required
unit congruence on descending to the nonmaximal order; it is not a hard
maximal-order PIP instance. The units of R_f are +/-epsilon^(f*t).
Multiplying a witness by a stabilizer therefore changes k by a multiple
of f and cannot evade the minimum-output bound.

There is also the tiny rational similarity

```
Q = [[1,0],[-1/2,1]],       B_f=Q*A_f*Q^(-1).
```

It is not an integral witness. Rational similarity is a strictly weaker
output requirement here.

## Consequence For Reusing Published Algorithms

Bley--Hofmann--Johnston, arXiv:2202.03526v3, defines IsSimilar to return a
conjugator (p.2), uses input-bit complexity (Section5,p.9), and states a
polynomial quantum algorithm in Corollary9.16 (p.29). The family above
rules out reading this as polynomial time to PRINT arbitrary conjugators
in expanded binary coordinates. Algorithm8.3/Thm8.4 Step10 converts
finite-group exponent data into a number-field unit, a concrete place where
output representation must be charged. This observation does not refute
the decision result, finite-field arithmetic, or compact-output variants.
[Versioned primary source](https://arxiv.org/pdf/2202.03526v3).

A compact witness exists here: store epsilon and the binary exponent
2^(m-1), then the formulas for C. Repeated squaring gives a straight-line
arithmetic circuit of O(m) operations. Its operation count is NOT the bit
cost of expanding its values. Norm and integrality can be verified for
this structured family by the identities above and modular arithmetic.
General verification and consumption of arbitrary compact arithmetic
witnesses need their own algorithms; this family supplies neither for free.

The local snapshot is `literature_cache/bhj_2022_integral_matrix_similarity.pdf`,
37 pages, arXiv v3 dated 2022-08-31, SHA-256
`25d34d6a2138bf07e8dc1003113f084edaedf33f2b29e3896e96def7bc012ec5`.

## Research Decision

- Preserve known quantum arithmetic decision primitives. Do not revive the
  false arbitrary-degree regulator barrier corrected in
  ARBITRARY_DEGREE_NUMBER_FIELD_REGULATOR_BARRIER.md.
- Every downstream reduction must say whether it consumes a Boolean,
  residues modulo a polynomial-bit modulus, a compact expression, or all
  expanded coordinates. These are different interfaces.
- Charge exact expansion when the application really needs the integer
  entries. Changing their name to a matrix oracle does not remove that cost.
- All instances in this family are explicit YES instances. No classical
  hardness, quantum advantage, or general impossibility follows.
- A potential repair is an output-sensitive or compact-output theorem
  with proved downstream operations. Do not advertise it as a new quantum
  primitive without first checking existing representation-aware literature.

Bounded exact controls are in `tests/test_integral_similarity_output_size.py`.
They support the algebra and protect against regression; the asymptotic
minimum-witness statement is proved above, not inferred from finite cases.
