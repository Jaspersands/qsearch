# Theta norm and stable discriminant: primary-source bridge

2026-11-12. Focused source check against current `STATE.md` and
`SURFACE_UNIFORM_ARITHMETIC_HEIGHT.md`. No native torsion-support or
coordinate-height conclusion is made. No Git, network, API, archive, or
numerical experiment was used. Relevant PDF pages were rendered and read
to resolve extraction defects in signs and constants.

**Disposition.** Javanpeykar Lemma 2.4.2 controls exactly the normalized
theta-supremum sum in the book's Theorem 9.2.5. Substitution of the
established stable Faltings-height bound gives a uniform polynomial bound
on that AVERAGE OF LOGARITHMS, with growing genus charged. The same
existing point-height/Wronskian budget also gives a polynomial stable
discriminant bound by the source's Theorem 2.4.1.

## 1. Exact normalization and averaging

All three sources use

    ||theta||(z;tau) = det(Im tau)^(1/4)
       * exp(-pi (Im z)^T (Im tau)^(-1) (Im z)) * |theta(z;tau)|.

This is the determinant-normalized theta norm, not the unnormalized
theta series, its square, or its L2-normalization to norm one.

- Javanpeykar: `audits/sources/classical_surface_2026/javanpeykar.txt`,
  physical lines 260--281, formula (1), including the Faltings determinant
  metric; lines 414--419 define its global maximum norm as the geometric
  mean over ALL embeddings K->C.
- Couveignes--Edixhoven book:
  `audits/sources/surface_module_2026/couveignes_edixhoven_book.txt`,
  lines 4440--4487, formula (4.4.5); the same inner product
  `(i/2) integral omega wedge conjugate(eta)` defines the Faltings metric.
  Formula (4.4.5) was visually checked on PDF page 103, printed page 91:
  its Gaussian exponent has a MINUS sign and determinant exponent 1/4.
- Wilms: `audits/sources/surface_module_2026/wilms_delta.txt`, lines
  280--320, especially 296--298, gives exactly the same norm. Its
  `H(X)=integral log||theta|| nu^g/g!` uses Haar probability measure.
  Its delta convention uses the same orthonormal inner product and
  Faltings factor, lines 456--474. Genus one is explicitly included.

Put m_K=[K:Q] and

    Theta_av(C) = (1/m_K) sum_(sigma:K->C)
                    log sup_(Pic^(g-1)(C_sigma)) ||theta||_sigma.

Javanpeykar's `log||theta||_max(C)` is EXACTLY Theta_av(C). Both members
of every nonreal pair of embeddings occur; no factor of two is missing.
The book's Theorem 9.2.5 uses the unnormalized sum m_K*Theta_av(C), with
coefficient +1; lines 9538--9559 and PDF page 211, printed page 199,
were checked. The Pic^(g-1) supremum is the same one in both sources.
Any translations implicit in a choice of theta characteristic do not
alter a supremum over the whole Picard variety.

In particular, a normalized book integral
`(1/m_K)sum_sigma integral log||theta||(D_x^sigma-Q) mu_sigma(Q)` is
at most Theta_av(C), since each canonical measure has mass one.
This is an upper-bound use of the norm, with no change of sign.

## 2. Direct bound from the established Faltings height

Javanpeykar Lemma 2.4.2, physical lines 518--573 and PDF page 10, states
for every smooth projective geometrically connected curve over Qbar of
genus g>=1:

    Theta_av(C) <= (g/4) log max(1,h_Fal(C))
                  +(4g^3+5g+1) log 2.                    (1)

This is a source theorem, not a new period-matrix estimate. Retain its
`max(1,h_Fal)` even when the Faltings height is negative.

Under the already established cover hypotheses, let d be the cover degree,
r>=3 the fixed bound on the TOTAL Galois orbit of branch points, and h_B
their maximum absolute LOGARITHMIC height. Set

    S=d+1+h_B,  H_F=C_r d^5 S.

Then h_Fal(C)<=H_F, and Riemann--Hurwitz gives
`g<=(r-2)(d-1)/2<=rd`. Since x->log max(1,x) is nondecreasing, (1) gives
the precise admitted inequality

    Theta_av(C) <= (g/4) log max(1,C_r d^5 S)
                  +(4g^3+5g+1) log 2
                <= C'_r [d^3+d log(d+1+h_B)].             (2)

After enlarging C_r to at least one, all constants depend only on r.
The last expression is polynomially bounded in d and h_B, including
growing g. This controls the logarithmic term that the arithmetic
intersection theorem needs. It does not say that the theta norm itself
is polynomial, and it does not bound every individual embedding by (2).
Finite extension of K repeats embeddings and leaves the normalized
average unchanged; no uncharged extension degree appears in (2).

## 3. Source-stated discriminant and delta bounds

Javanpeykar's definition, physical lines 404--449, is the STABLE quantity

    Delta_st(C)=(1/m_K) sum_s delta_s log #k(s),

on a semistable RELATIVELY MINIMAL regular model, where delta_s counts
geometric nodes. It is not a polynomial discriminant or the discriminant
of the number field K. Its delta invariant is the embedding average
`delta_Fal(C)=(1/m_K)sum_sigma delta(C_sigma)`.

For a non-Weierstrass geometric point b_0, source Theorem 2.4.1 gives
exactly (physical lines 506--514; PDF page 10 checked):

    Delta_st(C) <= 2g(g+1)(4g+1) h(b_0)
                   +12 log||Wr||_Ar(b_0)+93g^3,           (3)
    delta_Fal(C) <= 6g(g+1) h(b_0)
                   +12 log||Wr||_Ar(b_0)+4g log(2pi).     (4)

Here h(b_0) is the source's normalized stable Arakelov point height,
and the logarithmic Wronskian norm is averaged over embeddings. The
Wronskian uses factorial-normalized derivatives, as already checked in
the Faltings-transfer review. Neither term is a naive coordinate height.

Use the EXISTING auxiliary non-Weierstrass point of that review. It
need not be the common base point used to encode torsion divisors. With
one enlarged constant put H=C_r d^3 S. Its proved budgets are

    h(b_0)<=H,  Lambda_bar<=H,
    log||Wr||_Ar(b_0)<=A_g H+W_0,
    A_g=g(g+1)/2,
    W_0=[g(g-1)/2]log4+(g/2)log(2g^2 d^2).

Substitution in (3)--(4) gives, without a sign reversal,

    Delta_st(C) <= 8g(g+1)^2 H+12W_0+93g^3
                <= C''_r d^6(d+1+h_B),                  (5)
    delta_Fal(C) <= 12g(g+1)H+12W_0+4g log(2pi)
                 <= C'''_r d^5(d+1+h_B).                (6)

Consequently the normalized node term `2g^2 Delta_st` in book 9.2.5
is at most `C''''_r d^8(d+1+h_B)` on that relatively minimal
semistable model (and after a split semistable base change with the
same normalized stable meaning). Arbitrary blowups add nodes; (5)
does NOT bound their node sums without charging those additions.
Minimal resolution alone is not the relative-minimality hypothesis.
No effective construction of a semistable extension/model follows.

## 4. Optional independent theta route through Wilms

The direct source inequality (1) is sufficient and sharper here. As an
independent check, Wilms Theorem 1.1 and Corollary 5.7 imply the proposed
alternative with the stated sign. Namely, with
`H_theta=integral log||theta|| nu^g/g!`,

    delta=-24H_theta+2phi-8g log(2pi),
    log||theta||(z)+H_theta<=log c_g             (r=1).

Thus

    log thetaSup <= log c_g+delta/24-phi/12+(g/3)log(2pi)
                 <= log c_g+delta/24+(g/3)log(2pi).       (7)

The sign of phi is NEGATIVE after solving for -H_theta. The source has
phi=0 in genus one and phi>0 in higher genus (lines 542--549), so (7)
holds for every g>=1. Its constants, visually checked on PDF page 38,
are

    c_g=(g+2)/2                                      for g<=3,
    c_g=((g+2)/2)*((g+2)/(pi*sqrt(3)))^(g/2)          for g>=4.

Hence `log c_g=O(g log(g+2))`, not an unspecified genus-dependent
constant. Corollary 5.7 was visually checked on PDF page 39: at r=1
its extra term is `(g/2)log1=0`. Averaging (7) and using (6) gives
another polynomial bound for Theta_av(C). This route needs no new
period-geometry argument and no pointwise-from-average inference.

**Scope.** The averaged theta term and stable node/discriminant budget
are now supplied by actual source theorems with matched metrics and
the established height budgets. Book 9.2.5's remaining model hypotheses,
divisor/intersection terms and every conversion to a native closed
torsion-divisor encoding remain separate. No torsion-support height,
coordinate bound, reconstruction precision, or full native surface
algorithm is established by this bridge alone.
