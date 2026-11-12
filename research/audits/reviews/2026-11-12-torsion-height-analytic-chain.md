# Canonical torsion support heights: analytic-chain review

2026-11-12. Independent review of the ANALYTIC identity, moment estimate,
principal-divisor restriction and support-height assembly in
`SURFACE_TORSION_HEIGHT_CHAIN.md`. Read current `STATE.md`, the established
global Green lower-bound addendum in the Merkl review, and
`2026-11-12-surface-theta-delta.md`. The finite contraction/graph argument
is assigned to a different reviewer and remains an explicit premise here.
No Git, network, API, archive, or numerical experiment was used.

**Disposition.** The analytic signs and the moment estimate are correct.
Regular semistable principal-divisor restriction removes the support-etale
assumption needed by the book's particular resolution proof. With the
stated finite-model premises, the claimed sum of geometric pi-value
heights is bounded by `C_r d^9(d+1+h_B+log(N+1))` when only poles are
forbidden. Extra arbitrary chart exceptions require their count to be
charged as below. This is not a closed-divisor encoding-height theorem.

Two repairs are explicit: pi(Q)=0 must be handled separately because a
principal divisor cannot be restricted to a section on which its function
vanishes identically; and the actual book constants are log(2*pi), not
log 2. The zero case is harmless and does not require excluding zeros.

## 1. Green identity, including its sign and polar multiplicities

Work first on one complex fibre. Let mu be the canonical probability
measure and G the symmetric normalized Green function with local
singularity log|z-w| and integral `integral G(P,Q)mu(Q)=0`. Normalize
dd^c by `dd^c log|z|=delta_0`. Then

    dd^c_Q G(P,Q)=delta_P-mu.

Let F=pi^*FS, with FS the Fubini--Study probability form on P^1. Its
mass is d. Write the polar divisor as `P_inf=sum_j e_j P_j`, where
`sum_j e_j=d`, including ramification over infinity. Put

    ell(Q)=0.5 log(1+|pi(Q)|^2),
    H_pi=integral_C ell mu,
    u(Q)=ell(Q)+G(P_inf,Q).

At a pole of order e, ell has singular part -e log|z| and G(P_inf,.)
has singular part +e log|z|. They cancel, leaving a smooth function.
As currents,

    dd^c ell = F-delta_(P_inf),
    dd^c u = F-d mu.                                      (1)

The function `v(Q)=integral_C G(Q,R)F(R)` has the same dd^c and mean
zero. The logarithmic kernel is integrable, so the mean computation and
Fubini are valid. The difference u-v is constant; integrating against mu
identifies the constant as H_pi. Thus

    u(Q)=integral_C G(Q,R)F(R)+H_pi.                       (2)

This is also the EXACT final identity in book Proposition 9.1.4,
`couveignes_edixhoven_book.txt` physical lines 9181--9233. Its PDF page
204, printed page 192, was rendered and visually checked. The book writes
the differential operator `1/(pi*i) partial bar-partial`, which has the
opposite sign to the dd^c convention fixed above, and puts a minus sign
in its initial Green representation. Its final identity (2) has PLUS
the Green integral and PLUS the mean. Do not copy one of these operator
signs without the other.

Let `M=sup_(P!=Q) G(P,Q)`. Since F is positive of mass d, (2) yields

    u(Q)<=d M+H_pi.                                       (3)

All statements include genus one. The existence of a nontrivial
canonical probability measure and normalized Green kernel is all that
is used; no argument divides by g-1.

## 2. Exact spherical moment and the upper bound for H_pi

Use a point b with pi(b)=a, where a is the chosen nonzero integer, and
the established lower bound

    G(b,R)>=log dist_ch(a,pi(R))-L,
    L=log(Cd)+Lambda'.                                    (4)

The excluded equal-image fibre is finite and has F-measure zero. The
right side is integrable: logarithmic singularities at ramified points
remain integrable against the smooth pulled-back form F. For every
integrable function h on P^1,
`integral_C h(pi(R))pi^*FS(R)=d integral_(P^1) h FS`, with local
degrees counted. SU(2)-invariance reduces the chordal integral to a=inf:

    integral_(P^1) log dist_ch(a,t) FS(t)
      = -0.5 integral_1^infinity (log v)/v^2 dv = -1/2.

Consequently

    integral_C log dist_ch(a,pi(R)) F(R)=-d/2.             (5)

Evaluate (2) at b. Since `G(P_inf,b)<=dM`, (4)--(5) give

    H_pi<=dM+0.5log(1+a^2)+dL+d/2.                        (6)

This uses the lower Green bound to bound the SUBTRACTED integral in
`H_pi=u(b)-integral G(b,R)F(R)`. Reversing that sign would be wrong.
Ramification or a branch point at infinity changes neither (5) nor the
polar multiplicity count d.

## 3. Local valuation proof without etale horizontal supports

On a regular semistable arithmetic model Y over O_K, write

    div_Y(pi)=Z_0-P_inf+sum_C v_C C,
    m_s=max(0,-min_(C over s) v_C).

Here Z_0 and P_inf mean the horizontal closures, with their positive
multiplicities. They are effective Cartier divisors because Y is regular.
They may collide in special fibres, and neither their union nor the
individual supports need be etale over O_K.

A section Q meets a smooth point of a regular semistable fibre and
exactly one component C_Q with intersection multiplicity one. Locally at
a node, xy=varpi and a section would give nonnegative integral valuations
whose sum is one, so it cannot meet both branches at the node. For
pi(Q) nonzero and finite, restriction of the principal divisor therefore
gives the exact local identity

    v_s(pi(Q))=I_s(Q,Z_0)-I_s(Q,P_inf)+v_(C_Q).

All finite horizontal intersections here are nonnegative, regardless
of collisions between zero and pole supports. Hence

    max(0,-v_s(pi(Q)))<=I_s(Q,P_inf)+m_s.                 (7)

This establishes the needed finite inequality directly. The book's
etale-union hypothesis at physical lines 9003--9011 is used by its
chosen sequence of resolution blowups at lines 9099--9110; it is not
required by (7). Regularity, a section, and the charged vertical
negative-part bound remain substantive hypotheses.

If pi(Q)=0 identically, do NOT invoke the displayed restriction identity.
Its finite height contribution is zero, and (7) holds trivially because
its right side is nonnegative. At infinity the horizontal self/support
intersection would require different treatment; the chosen D_t avoid
the polar support, so that case is excluded.

Let `m_K=[K:Q]` and `V_pi=m_K^-1 sum_s m_s log Norm(s)`. The Arakelov
intersection convention is

    (Q,P_inf)=I_fin(Q,P_inf)-sum_sigma G(P_inf^sigma,Q^sigma).

Combine (7) with `log max(1,|pi(Q)|)<=ell(Q)` and (3). This proves

    h(pi(Q)) <= (Q,P_inf)/m_K+V_pi+d M_bar+H_pi_bar.        (8)

For a zero Q this remains valid: `(Q,P_inf)/m_K+u_bar(Q)` equals its
nonnegative finite pole intersection, since ell(Q)=0. Thus the same
right side in (8) bounds zero, even if `(Q,P_inf)` alone is negative.
The proof pays collisions rather than assuming them absent.

## 4. Finite avoidance and the size of the chosen integer

The proposed avoidance Wronskian is correct, conditional on uniqueness
already imposed. For a forbidden geometric point P,

    P in D_t  iff h^0(t(gb-P))>0
              iff h^0(K_C tensor t^-1(P-gb))>0.

The middle bundle has degree g-1, so RR has Euler characteristic zero.
The complete space `H^0(K_C tensor t^-1(P))` has dimension g and its
line bundle has degree 2g-1. Its Wronskian is nonzero in characteristic
zero (also if char>2g-1). A section of order >=g has positive weight;
the total Wronskian weight is

    g(2g-1)+g(g-1)^2=g^3.

Thus at most g^3 base points are forbidden for each pair (t,P),
including genus one. Poles contribute at most d geometric forbidden
points. Together with the Ng^3 uniqueness bound and <=r branch values,
one may choose a in

    {1,...,r+1+Ng^3(1+d+A)},

where A counts any ADDITIONAL specified geometric chart exceptions.
Every b over the resulting a is good. Therefore

    log a=O_r(log(d+1)+log(N+1)+log(A+1)).

For A=0 this is paid by `S_N=d+1+h_B+log(N+1)`. With arbitrary extra
exceptions use `S_(N,A)=d+1+h_B+log(N(A+1)+1)` instead, until a
polynomial bound on A in the charged presentation parameters is given.
This is an existence/counting argument, not an algorithm for constructing
the complete forbidden set. Small point heights and field-normalized
Arakelov bounds are not being inferred from uniqueness alone.

## 5. Conditional arithmetic assembly

Take Y relatively minimal, regular and split semistable, as required
by the corrected use of book 9.2.5. The separately audited finite-model
premises used here are

    h_Y(b)<=h_Z(b),
    I_fin,Y(b,P_inf)/m_K<=d h_Z(b),
    V_pi<=d[h_Z(b)+Delta_st(C)].                          (9)

Their construction, nonnegativity inputs and contraction/graph proof are
NOT certified by this review. They must hold on the common model/field
used for the following calculation.

Set `A_inf=0.5log(1+a^2)` and `J_b=h_Z(b)+A_inf+L_bar`. For a pole P,
the global lower bound gives
`G(b,P)>=-A_inf-L`, since `dist_ch(a,infinity)=1/sqrt(1+a^2)`.
Sum this with polar multiplicities and combine with (9). It gives
`(b,P_inf)/m_K<=d J_b`, and therefore
`(gb,P_inf)/m_K<=gd J_b`. No individual finite-intersection bound is
needed beyond the displayed aggregate premise.

Arakelov adjunction gives `b^2=-(b,omega_Y)`, so for D=gb,

    -(D,D-omega_Y)/(2m_K)=g(g+1)h_Y(b)/2.

Use the ACTUAL book 9.2.5, with its minus intersection sign and log(2*pi)
constants; drop its nonnegative log-cardinality term. Sum over the
degree-d polar divisor with multiplicities. Writing

    B_*=[g(g+1)/2]h_Y(b)+2g^2 Delta_st+Theta_av
                          +(g/2)log(2*pi)+0.5h_Fal,

we obtain

    (D_t,P_inf)/m_K <= d B_*+gd J_b.                     (10)

Finally sum (8) over the effective degree-g D_t, preserving every
multiplicity:

    sum_(Q in D_t) h(pi(Q))
       <= d B_*+gd J_b+g[V_pi+d M_bar+H_pi_bar].         (11)

Put S=S_N for pole avoidance alone, or S=S_(N,A) with extra exceptions.
The established budgets and (6),(9) give

    g=O_r(d),  h_Z(b), M_bar, Lambda'_bar <= C_r d^3 S,
    H_pi_bar<=C_r d^4 S,
    Delta_st<=C_r d^6 S,  V_pi<=C_r d^7 S,
    Theta_av<=C_r[d^3+d log(d+1+h_B)],
    h_Fal<=C_r d^5 S,  J_b<=C_r d^3 S.

Thus B_*<=C_r d^8 S. The dominant term in (11) is
`2d g^2 Delta_st`, of size `C_r d^9 S`; the vertical term is at most
`C_r d^8 S`, and all remaining terms are smaller. This proves the
claimed deliberately loose exponent, CONDITIONAL on (9) and the exact
minimal-model/book premises.

## 6. Averaging, fields, and the output boundary

One may choose a finite field extension containing b, all relevant
divisor classes and all geometric support points to justify section-wise
intersection calculations. Every estimate above is divided by [K:Q],
and every archimedean sum runs over ALL embeddings. Absolute logarithmic
heights and the stable intrinsic invariants are unchanged by extension;
the resulting geometric sum has total multiplicity g. The finite-model
premises must be applied on the compatible extended model, not silently
transported from an unrelated one. This existential use of a large
field supplies no polynomial common splitting-field algorithm.

All analytic arguments include genus one, repeated points in D_t,
ramified polar points, and a branch point at infinity. Torsion is used
by book 9.2.5, not by the Green or local valuation identities.

**Exact admitted output:** a bound for the sum of absolute heights of
the GEOMETRIC pi-values in each canonical D_t. Those values can coincide
on different branches and do not identify the points, their local jets,
or an ideal/closed-divisor encoding. A controlled supplied plane equation
can support a separate coordinate-height argument, but exceptional
charts, branch labels, primitive coordinates and repeated-point jets
still require explicit treatment. No reconstruction or full native
surface-comparison claim follows from (11) alone.
