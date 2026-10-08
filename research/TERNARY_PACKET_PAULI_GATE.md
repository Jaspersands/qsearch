# Conditional Pauli Visibility In Correlated Native Packets

LOCAL DERIVATION / REVIEW PENDING. A scoped measurement obstruction, not a
general quantum lower bound or a proof that correlated packets are useless.
This follows the charged source composition in
`TERNARY_CORRELATED_PACKET_ACQUISITION.md`.

## Exact Source Law, Not A Fitted Signal

At odd native level L=2r-1>=3, let q=3^r, q'=q/3. Conditional on its residue
matrix C, the K odd inputs have independent uniform high frequency lifts:

    a_i = ell_i + 3*alpha_i,
    c_i = (2*ell_i mod3) + 3*gamma_i,
    alpha_i,gamma_i uniform in Z_q'^n.

The ell rows agree with C up to the known nonzero native unit. For the actual
Gaussian syndrome y, write physical assignments t(z)=t0+D*z mod3, where D
is the full K-by-h kernel generator, h=K-rank(C). The retained state is
flat with phases chi_q'(<s,Q(z)>). Assume s is NONZERO modulo q': the zero
residual secret is a secret-independent flat state, an explicit exception.

For v!=0,w in F3^h define the known logical Pauli overlap

    A(v,w) = <psi|Z^w X^(-v)|psi>
           = 3^-h sum_z chi_3(w*z) chi_q'(<s,Q(z+v)-Q(z)>).

Let d=D*v, S=supp(d), and b=rank(D_S), the rank of the rows of D on S.
The exact conditional high-lift moment is

    E_high |A(v,w)|^2 = 3^-b, if w lies in row_span(D_S),
                       0,    otherwise.

In the second case A is identically zero for EACH high-label instance, not
just on average. The conditional law holds for every fixed C, syndrome y
and nonzero residual secret, at every odd level>=3. Neither the physical
support weight |S| nor h alone is the correct exponent.

### Proof

At a changed site, the two one-hot frequency coefficients for the local
transition t_i -> t_i+d_i take three distinct values as t_i ranges over F3.
Their differences remain distinct modulo3. Since some secret component is
nonzero modulo q', averaging its independent uniform alpha/gamma lifts kills
a pair of terms unless their starting digits agree at EVERY changed site.
Unchanged sites impose no constraint. Thus the surviving z,z' pairs satisfy

    D_S*(z-z')=0.

On these pairs the entire local transition coefficients agree, including
their low parts, so no unknown low-phase factor remains. The second moment
is the character average of chi_3(w*(z-z')) over this kernel, multiplied by
3^-b. Orthogonality gives the stated formula. Independently, the derivative
phase depends only on D_S*z; summing over each fiber proves the exact zero
when w is outside the row span. This also shows why one cannot substitute
support weight for projection rank.

The probe v,w must be fixed from LOW data, including C,y and the original
measured pointer, before averaging high lifts. The code computes its exact
conditional formula, not a proof that an arbitrary caller obeyed that policy.

## Uniform Rank Bound From Two Code Distances

Let d_primal be the minimum nonzero weight of ker(C), and d_dual the minimum
nonzero weight of row_span(C). For the zero dual code set d_dual=K+1.
For EVERY nonzero logical translation, even one chosen adaptively from C,

    rank(D_supp(D*v)) >= min(d_primal, d_dual-1).

Indeed, |supp(D*v)|>=d_primal. A dependency among any selected rows of D
is exactly a nonzero dual word supported on those selected coordinates.
Every subset of fewer than d_dual rows is therefore independent. Taking
min(|S|,d_dual-1) rows proves the bound. No source/frame independence,
full-rank conditioning, saturation or distance-solving algorithm is assumed.
Finite controls enumerate code distances only at bounded dimension.

For an UNCONDITIONED IID C in F3^(n by K), set

    U(K,d) = sum_(j=1..d-1) binomial(K,j)*2^(j-1).
    Pr[d_primal<d] <= U(K,d)/3^n.
    Pr[d_dual<d]   <= (3^n-1)*U(K,d)/3^K.

The first union is over projective physical words x, each satisfying C*x=0
with probability3^-n. The second is over projective nonzero coefficient
vectors u; u*C is uniform in F3^K, with exactly2*U nonzero words of weight<d.
Zero u*C is not a nonzero dual word. Dependence/duplicate coefficient images
only makes the union bound looser. Both bounds are unconditional in rank.

At K=2n and d=floor(n/8), both distance failure bounds decrease exponentially.
For example, bound U by d*(4*e*n/(d-1))^(d-1): its exponential rate is smaller
than3^n. On the remaining matrices every nonzero translation has b>=d-1.

## Polynomial Menus And One-Packet Tests

A menu of T probes can be defined from C,y and then inspected/selected using
all HIGH public labels. It must still consist of at most T probes fixed
before those high labels are used to define the family. Since max<=sum,

    E_high max_menu |A|^2 <= min(1,T*3^-(d-1))

on good low matrices. Charge the bad-matrix probability delta rather than
discard it. The raw population bound is

    R = min(1, delta + min(1,T*3^-(d-1))).

A single controlled-Pauli real/imaginary test on a fresh packet has binary
outcome bias no greater than |A|. Its mean total variation to an unbiased
coin with the SAME public labels/pointer/syndrome is at most sqrt(R)/2.
For B independent fresh packets, with adaptive past transcripts and current
high-label selection inside low-defined menus, a hybrid argument bounds TV
by min(1,B*sqrt(R)/2). The bound holds for each fixed NONZERO residual secret;
two such secrets have transcript TV at most min(1,B*sqrt(R)).

The reference does not supply a simulated quantum input, and the bound does
not cover reusing/disturbing the same packet with several noncommuting tests,
joint measurements across packets, measurements of untouched original states,
or a probe family implicitly containing exponentially many directions or
diagonal characters. High labels may define a new receiver outside the menu
premise. Efficient implicit high-informed construction remains OPEN.

This differs from the original small-copy blind product-readout gates:
at K=2n the packet can cost2n*(n+1)^2 original samples, yet these particular
low-defined Pauli tests remain exponentially weak. Polynomial sample surplus
does not automatically rescue every proposed measurement primitive.

## Controls And Revised Decision

Complete level3 censuses cover729 high-lift assignments each:

1. C=(1,1,1), v=(1,0), w=0 has support2, restricted rank2 and exact moment1/9.
2. C=(1,1,0), v=(1,0), w=0 has support2 but rank1 and moment1/3. A Hamming-
   weight exponent would incorrectly predict1/9.
3. The second frame with w=(0,1) has overlap0 on EVERY high lift because w
   is outside the restricted row span.

Exact F3 character-difference histograms verify the moments without a fitted
floating exponent. An independent JS implementation rebuilds the native
chart, all high-lift phase tables, Gaussian frames, code distances, every
nonzero translation in all27 small low matrices, and rational scaling bounds.
The censuses are conditional algebra controls, NOT a matched-packet factory.

The T=n^2 scaling envelope is deliberately VACUOUS at n32 and n64 after
clipping to1. It becomes nontrivial on the larger prespecified sizes; those
numbers are exact population bounds, not experiments on a large quantum
state. Tests and the independent verifier explicitly preserve the clipping.

Do not spend the next pass estimating low-defined translation expectations
more accurately. Seek a high-informed implicit observable, branch interference,
or a costed noncommuting/collective decoder that genuinely violates a premise.
An informative joint packet may still be useful; this gate identifies one
natural but weak readout family, not the missing general decoder.

```
python theorems/ternary_packet_pauli_gate.py --write
node research/certificates/ternary_packet_pauli_gate_crosscheck.js
python -m pytest -q tests/test_ternary_packet_pauli_gate.py
```

External proof review remains necessary. Gemini/Antigravity owns routine
CLI/registry integration and full production validation. No new candidate or
generic quantum complexity lower bound is accepted by this report.
