# Approximate Coherent Access From A Fixed Classical Noisy Phase Bank

Status: LOCAL DERIVATION / EXTERNAL REVIEW PENDING. This extends, rather than
changes, the copy-only input bridge. No efficient receiver or hardware
synthesis is supplied. The inverse of a noisy known preparation is NOT the
exact inverse of the ideal unknown state; approximate access is separately
budgeted below. Restricting every classical-source investigation to copy-only
access would miss this legitimate, conditional stronger interface.

## Fixed Bank, Not Chosen Queries

Take2M independent classical noisy-linear records in the same source model.
Their original IID labels form a FIXED PUBLIC BANK of pairs a_i,c_i.
Known masked values b_i,d_i allow the controlled phase operation

    V_C=sum_i |i><i| tensor diag(1,omega^b_i,omega^d_i).

Its known inverse negates both phases. Invalid padded indices act as identity.
The corresponding ideal V_s uses <a_i,s>,<c_i,s> in place of the noisy values.
F3 followed by these phases prepares the previous native qutrit. A noisy
preparation inverse is F3^dagger V_C^dagger, not V_C^dagger F3^dagger.

Implementation uses an explicit sequence of reversible index-equality
controls and two known phase gates per bank entry. It costs O(M) such
controls per query with O(log M) address bits, plus angle/bit costs.
No free QRAM, hidden-state inverse, or group table is assumed. A polynomial
bank and polynomial query count give polynomial-description access in the
stated qutrit gate model. It supplies ONLY these indexed labels. A caller
cannot request an arbitrary unseen a or choose new source equations.

## Errors Are Fixed Across Every Query

Let E_j be the2M source errors, each with true E[E_j^2]<=V. For the exact
known phase and its ideal counterpart,

    delta=||V_C-V_s||
      =max_j |exp(2*pi*i*E_j/q)-1|,
    delta^2 <= (4*pi^2/q^2)*sum_j E_j^2,
    E[delta^2] <=80M*V/q^2.

The equality uses block-diagonal operator norm. The bound needs the moment
promise, but not symmetry for this phase-access comparison. Uniform IID
labels and the full source law are still needed to compose the upstream
problem reduction. We do NOT resample errors at each oracle invocation.

For an integer power k, reduce k modulo q to its canonical signed residue,
since both ideal and noisy phase operations have period q. The telescoping
power identity gives ||V_C^k-V_s^k||<=|k|*delta; inverses have the same bound.
For any committed exposure schedule or adaptive schedule with pathwise cap
W=sum |k_t| and T nonidentity calls, the complete query hybrid and CPTP
contraction give expected receiver correctness loss at most

    min(1,W*sqrt(80M*V/q^2)),

before physical gate and source-rounding errors. Jensen is applied AFTER a
pointwise bound on the whole circuit, so shared source errors across calls
are legal. The compiler returns an exact rational square-root upper interval
whose precision scales with W and confidence. Gate/F3 allowances add
2*T*2^-P with P=kappa+ceil(log2(2T)), bounded by2^-kappa.
This covers a receiver using preparations and their inverses on arbitrary
workspace via V and known F3. All such phase invocations must be counted.
Caller gates outside these primitives have their OWN error budget. Reflection
about a bank state uses V F3(2|0><0|-I)F3^dagger V^dagger and consumes TWO
phase calls. It is not a free exact ideal reflection.

The noise error scales as sqrt(V)/q rather than V/q^2. The earlier smaller
averaged copy-only loss CANNOT be reused for a coherent adaptive circuit:
the ideal/noisy preparation descriptions can themselves be queried. This
is a different approximation theorem and a different access contract.

## Fast Forwarding Is Not Free Noise Suppression

Known classical phase values let the reduction compute k*b_i modulo q and
synthesize the actual k-th diagonal power cheaply in bit complexity. That
does NOT make its comparison to an ideal k-th power free. Its phase error is
k*E_i modulo q, and exposure is |canonical(k)|, not one just because a gate
description is short. Exponentially large canonical powers generally make
the transfer bound vacuous. A multiple of q is exactly identity for BOTH
operations and correctly has zero exposure. Inverses and powers q+1 reduce
to -1 and1 as appropriate; they are not rejected by a needless raw-exponent
charge.

Repeated known-bank preparation also does NOT provide fresh independent
frequency rows or errors. Source originals remain2M, while receiver phase
queries are T and weighted exposure W. That reuse is legal in this theorem,
unlike the false assertion that it manufactures IID native source states.

## Conditional Consequence And Research Priority

For rounded continuous Gaussian source, V<=q^2*alpha^2/3+1/2, so the generic
coherent noise loss is at most W*sqrt((80/3)*M*alpha^2+40M/q^2), capped at1.
For polynomial M,W and inverse-polynomial receiver success, sufficiently
small inverse-polynomial alpha and large q can make this loss small while
retaining a polynomial upstream lattice approximation factor. Concrete
receiver M,W/success and source theorem guards must be fixed first.
Source-rounding aborts, source interval promises, caller/gate errors,
composition review and novelty still prevent automatic hardness admission.

This restores a potentially useful RESEARCH interface: costed label-indexed
coherent processing and approximate state reflections from classical records.
It does not solve fiber erasure or amplify an exponentially small branch in
polynomial queries. Nor does it offer an unseen-label phase oracle or claim
a generic coherent-input LWE algorithm. The original classical-data Bayes
ceiling STILL holds because every actual oracle is computed from those data;
any quantum advantage would be computational, not additional information.

## Controls And Falsifiers

Exact scalar controls check normal, inverse, high-power and modular-identity
exposure, large roots, and scaling of square-root/gate precision. Four literal
fixed-bank recipe plans replay six original records at q9 and powers1,-1,3,9.
Their phases are known, originals do not get cloned into independent IDs,
and zero-power branches are identity. Gaussian moment controls compare
T128 andT1024 unit-power calls with a single2^20-power call. The latter has
short description but a vacuous noise comparison.

Falsifiers: wrong preparation-inverse order; arbitrary new labels; noise
refresh on reuse; uncharged powers/inverses; exponent counted only as one
gate; missing multiplexor/angle costs; a moment bound inferred from samples;
copy-only loss used for a coherent receiver; or a vacuous sufficient ledger
advertised as either success or an impossibility theorem.

NEXT: a genuinely constructive fixed-bank coherent receiver with polynomial
weighted exposure and full-secret recovery, compared against matched
original-data classical attacks. The old source-copy-only barriers must be
rechecked for this access model, but their general normalization/search
obstructions are not automatically removed.
