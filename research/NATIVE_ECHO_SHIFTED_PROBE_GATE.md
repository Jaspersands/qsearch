# Shifted-Probe Weak-Trit Gate For One Phase Echo

LOCAL DERIVATION / REVIEW PENDING. Exact finite identities are independently
replayed; the asymptotic argument below still requires external mathematical
review. This is not an unrestricted quantum lower bound or a novelty claim.

## Scope

Use the original even-level IID source in
[the receiver derivation](NATIVE_PARTIAL_PHASE_ECHO.md). Let G=q^n=3^N, N=nr,
M=m+w, W=3^w. The target is the LEAST secret trit s_1 mod3, not full recovery.
Full-secret bounds alone do not rule out useful weak inference.

Fix B labels. A public K and all phase settings may depend on B, but NOT on
A labels. A precommitted menu of L such policies is allowed; its selector
may inspect the full A labels. Unlimited unknown-secret classical processing
of the final outcomes is covered. A full-A inverse calibration taking values
outside a precommitted small menu is explicitly outside this cut.

## The Exact Gram Identity

For one pair y,y' set delta=K F_B(y), delta'=K F_B(y'). Under uniform A-word
output a and the full IID A labels define

    X_s = 3^m A(a,s+delta) conjugate(A(a,s+delta')),
    C = E_(a uniform) X_s
      = product_i [1+chi_q((delta-delta').a_i)
                      +chi_q((delta-delta').c_i)]/3,
    Z_s = X_s-C.

C depends on the public A labels but NOT on s. Outside the exceptional set
{-delta,-delta'}, the Z_s are exactly orthogonal for distinct s. Their
squared norm is (5/3)^m-1 if delta=delta', and 1-3^(-m) otherwise; both are
at most D=(5/3)^m-1. This includes arbitrary FIXED A phase settings.

For one source copy, put e_0=(0,0), e_1=(1,0), e_2=(0,1). Expand the four
amplitude factors. Of 81 quartets (j,k,l,h), the uniform measured Fourier
word cancels 54 through k-j+l-h !=0 mod3. Nine diagonal terms are the common
background. Six identical ordered-root terms require s=t. The remaining
12 have nonparallel roots e_j-e_k, e_l-e_h with determinant +/-1. Solving
the two character equations forces (s,t)=(-delta,-delta') or its reverse.
There are no nonunit determinant exceptions at growing ternary roots.
For the surviving nonexceptional terms, all fixed-setting phase factors
cancel. Independent copies tensor this identity and its background.

The complete rational Gram controls cover q9 diagonal and off-diagonal shifts,
q27 and dimension2 at q3. Separate tests enumerate the actual IID public rows
and measured outcomes with nonzero fixed phase settings; they do not just
replay the quartet classification.

## Background And Weak Target

Use density relative to UNIFORM measured (a,b). The clean echo density is

    u_s(a,b) = W^(-1) sum_(y,y') X_s
      chi_q(s.(F_B(y)-F_B(y')))
      chi_q(-F_A(a)^T K(F_B(y)-F_B(y')))
      chi_q(-eta_B(y)+eta_B(y')) omega_3^(-b.(y-y')).

The second phase depends on A labels AND the output a. It is common to all
secrets and has modulus1, so multiplication by it preserves the L2 norm of
one centered-pair contrast. It must NOT be dropped or called a constant.

Replacing X_s by C is precisely the positive normalized receiver channel
obtained by dephasing the A input word before its Fourier transform. B then
has a known shift K^T(F_A(x)-F_A(a)), averaged over the dephased A words x.
This channel remains outcome-dependent, but is positive and normalized for
every secret and public label record.

Let w_t(s)=(3/G)1[s_1 mod3=t]-1/G. Its squared sum is 2/G. The C contribution
to its contrast vanishes unless a nonzero B difference is one of the two
target-dual characters +/- (q/3)e_1. Zero frequency collisions are harmless.
For each distinct y,y', their B-frequency difference is uniform in Z_q^n:
at least one independent full B row has coefficient +/-1. A union over
unordered pairs bounds the bad-B mass by W(W-1)/G.

For good B records, replace the at most W exceptional secret channels by
their positive C channels. This changes prior-weighted decision success by
at most W/G. Away from these secrets, orthogonality gives centered-pair
contrast norm at most sqrt(2D/G). The common outcome phase preserves this
norm, and Minkowski over W^2 pairs with coefficient1/W gives
W sqrt(2D/G). Each contrast integrates to zero because both channels are
normalized; replacing a classifier indicator h_t by h_t-1/2 bounds its
contribution. Hence one fixed policy obeys

    E[Pr(correct least trit)] - 1/3
      <= min(2/3, W^2/G + W sqrt(D/(2G))).

The expectation includes the ORIGINAL full IID public source. It is not a
pointwise bound for arbitrary chosen public cohorts.

## Label-Based Selection From A Fixed Menu

For L policies conditional on B, the exceptional-secret union has size at
most LW. Disjoint A-label selector masks give an L2 bound sqrt(L) times the
one-policy bound, rather than L. Good-B background contrasts still vanish.
All exceptional and bad-B channels are retained in the raw failure ledger:

    advantage <= min(2/3,
        [W(W-1)+LW]/G + sqrt(L) W sqrt(((5/3)^m-1)/(2G))).

The full-label selector cannot introduce previously uncommitted K values or
settings. An inverse calibration generally has exponentially many possible
full-label values and is therefore not covered by a polynomial menu ledger.

At M=N+c, c=O(log N), w=O(log N), L=poly(N), the bound is exponentially small
in N even with unlimited decoding. A directed rational envelope uses
sqrt(5)/3 <= 3/4 (80<=81), sqrt(L)<=L and
(5/3)^(c/2)<=(5/3)^ceil(max(c,0)/2):

    advantage <= min(2/3,
        [W(W-1)+LW]/3^N
        + L W (5/3)^ceil(max(c,0)/2) (3/4)^N).

This does NOT rule out a large copy surplus, a wide mediator, multiple
noncommuting echoes, arbitrary collective receivers, or a full-A-adaptive
coupling. It does not prove a classical simulation of the clean echo.

This adaptive escape is backed by an exact counterexample, not just a missing
proof. For every q=3^r with r>=2 and one A copy, take delta=0 and
delta'=inverse(a) when a is a unit, otherwise0. Keep every original IID (a,c)
row and every Fourier digit. The secrets s=q/3 and t=2q/3 are never
exceptional, yet their centered inner product is exactly4/27 instead of0.

For unit a, averaging c forces all four second-coordinate simplex indicators
to agree: the inverse term is a unit while s,t are divisible by3. Seven
quartets survive the output Fourier average: six binary-index quartets and
the all2 quartet. Put zeta=chi_q(1). Their X inner product is
(2+zeta+conjugate(zeta))/9; the C norm is
(3+zeta+conjugate(zeta))/9. Their centered difference is -1/9.
For nonunit a the zero fallback gives C=1 and the first source phase is1 for
both secrets. Fifteen quartets survive the c/output averages, giving
15/9-1=2/3. Unit and nonunit source probabilities are2/3 and1/3, so the raw
unconditional entry is (2/3)(-1/9)+(1/3)(2/3)=4/27. No rank failures or
exceptional-secret records were removed.

An independent cyclotomic replay checks all22,113 source/outcome records at
q9,q27,q81, including both conditional source partitions. The growing-root
derivation remains review pending. Extending fixed-probe orthogonality to
full-A inverse calibration is false. This does not establish weak-trit
advantage or an efficient decoder for that calibration.

## Falsifiers And Verification

Reject the derivation if a nonexceptional off-diagonal Gram entry is nonzero,
fixed settings alter its claimed norm, a common-phase step changes an L2
norm, the C channel is not normalized/positive, the target-dual background
condition is wrong, or selection from L policies violates the masked bound.
Do not extend the full-IID source result to odd-level or correlated rows.

The independent rational checker replays all81 quartet classes and 836 full
Gram entries, plus growing parameter ledgers. This verifies finite algebra
and ledger encoding, not the entire asymptotic proof by machine.

```
python theorems/native_echo_shifted_probe_gate.py --write
node research/certificates/native_echo_shifted_probe_gate_crosscheck.js
python -m pytest -q tests/test_native_echo_shifted_probe_gate.py
```
