# Native RLWE: Exact Metric, Nonprincipal Quaternion Ideal

2026-10-05. LOCAL DERIVATION / REVIEW PENDING. No independent theorem review,
novelty, speedup, quantum generator, or security claim. This is a deliberate
attempt to falsify the preceding quaternion audit's proposed bottleneck.

FOLLOW-UP: [the native ideal-class orbit audit](NATIVE_RLWE_IDEAL_CLASS_ORBIT_AUDIT.md)
classifies generic native equivalence by a public dihedral action with cheap
signed isometries. Class labeling in that family is already classical and
cannot improve geometry. Nonnative short-element/class-transport methods are
not ruled out; their geometric output and cost remain open.

## 1. The Metric Obstruction Is Not Universal

The [positive-lift audit](NATIVE_RLWE_QUATERNION_KERNEL_AUDIT.md) covers the
specific order R+Rj with j^2=-rho in the original graph coordinates. A different
order DOES preserve the physical metric exactly. Put

```
A=K+Kj, j^2=-1, ja=bar(a)j,
O_0=R+Rj, O_q=R+qRj,
Lambda_M={(g,f):g=Mf modq} subset O_0.
```

O_q is an order in the fixed definite quaternion algebra A. Lambda_M is a
fractional LEFT O_q ideal: left R multiplication preserves the graph and left
qj sends every pair into qO_0, which is contained in the graph. The original
reduced-norm trace is exactly ||g||^2+||f||^2. No weighted metric is introduced.
The square of the left qj action is -q^2 I, not -I; hence the earlier
Hamilton-isometry gate does not apply. Its operator norm is q, not one.

If an integral ideal is required, use q*Lambda_M subset O_q. This charges a
global scalar q in the presentation and lengths, not a relative distortion.
Lambda_M itself is generally NOT contained in O_q; dropping the word
fractional would misstate the input. This is algebraic encoding, not progress
on the quantum short-element primitive by itself.

## 2. Locally Principal Does Not Mean Globally Principal

Both O_q and Lambda_M have coefficient covolume q^d in O_0. The known element
alpha=M+j belongs to Lambda_M. Its norm beta=1+M*bar(M) is totally positive.
Right multiplication gives the contained lattice

```
O_q*alpha, column basis [C_M,-qI;I,qC_M^T],
[Lambda_M:O_q*alpha]=Norm_K(beta)=det(I+C_M*C_M^T).
```

This index is not generally one. If it is coprime to q, the contained lattice
equals Lambda_M after localization at every prime dividing q. Away from q,
Lambda_M and O_q both become O_0 and the local generator is 1. This gives an
actual locally principal certificate, without claiming global principality.

For prime q3mod8,d>=4, beta is a unit modq unless M*bar(M)=-1 modq. Thus
the local certificate covers probability 1-(q^(d/2)-1)/q^d on the full IID
source. Its failure is NOT proof of local nonprincipality. The saved native
d64 kernel passes the certificate. No native LLL or quantum solver is rerun.

## 3. Global Principality Gate: Only The Zero Ratio

For d power-two and odd q>=3:

```
Lambda_M is principal over THIS O_q if and only if M=0 modq.
```

The proof uses a published unit-signature theorem; it does not assume Weber's
class-number-one conjecture. [Dummit, Dummit and Kisilevsky, Proposition3,
journal page291](https://msp.org/pjm/2019/298-2/pjm-v298-n2-p03-s.pdf) state
that real 2-power cyclotomic fields have full circular-unit signature rank.
Consequently their full unit signature rank is also maximal. Since the
unit group modulo squares has size 2^[F:Q], the signature map is an
isomorphism there: every totally positive unit of O_F is a square of a unit.

Now suppose Lambda_M=O_q*alpha. Because 1 is in O_q, alpha belongs to
Lambda_M subset O_0. Equal covolumes force |Norm_K(nrd(alpha))|=1. Its norm
epsilon is integral and totally positive, hence a totally positive O_F unit.
Choose v in O_F^* with v^2=epsilon. Then alpha/v is integral in O_0 and has
reduced norm one. The coefficient trace forces alpha/v to be a signed
monomial in R, or that monomial times j, with no mixed blocks. Therefore
alpha itself is a pure R unit or a pure R unit times j.

A pure first-block unit cannot belong to Lambda_M: g divisible by q cannot
be a unit. A pure second-block unit belongs only if M=0, since f is invertible
modq. Conversely Lambda_0=qR+Rj=O_q*j, with known generator j and norm one.
This proves the gate. For q*Lambda the same conclusion holds after dividing
a purported generator by q. All statements retain local-review debt.

Uniform-source principal probability is exactly q^(-d), and is zero when
conditioning on a unit ratio. Thus a promised quaternion-PIP solver for this
encoding would reject almost all native inputs, even though the inputs are
usually locally principal and their metric is correct.

Central units MUST NOT be confused with norm-one units. At d4,
v=1+sqrt(2)=(1,1,0,-1) has physical norm squared3, and reduced norm
3+2sqrt(2), whose field norm is one. It is an ambient quaternion unit despite
not having reduced norm one. Its central square root supplies the above
normalization; the proof does not discard it through bounded enumeration.

## 4. What Survives The Critique

Enlarging the order is not a free rescue. For the same beta-unit instances,
O_0*Lambda_M=Lambda_M+j*Lambda_M contains qO_0 and the column basis
[C_M,-I;I,C_M^T]. Its determinant is Norm_K(beta), coprime to q. Hence the
sum is the WHOLE O_0. Every overorder containing O_0 likewise extends the
native ideal to that whole chosen overorder. At any FIXED overorder the ideal
no longer carries M. A deliberately M-dependent overorder choice is not ruled
out: its presentation would be additional source-bearing data whose cost and
information must be tracked. Keeping level data or intersecting an output back
into Lambda is likewise an extra obligation, not a supplied PIP solver.

This kills a direct PRINCIPAL-ideal-oracle interpretation over O_q, not
quaternion geometry itself. Native short relations are still elements of a
definite, usually locally principal but globally nonprincipal ideal. An
algorithm could search short nongenerators, transport ideal classes with
fully charged geometry, or use another order/presentation. None is supplied.

Highest-value next questions:

1. Does a costed quantum algorithm exploit this conductor-order ideal-class
   structure beyond classical native lattice reduction? Specify the actual
   quantum state, group action and output; no abelian HSP is granted merely
   by saying "ideal class" in a noncommutative algebra.
2. Could a different ideal-class representative yield a short native element
   with controlled transport norm? Charge the transport map and original
   relation's completion/index/reciprocal energy, not just ideal equivalence.
3. A larger order containing O_0 erases the graph on the beta-unit source.
   Preserve costed extra level data or find a genuinely different construction;
   simply running PIP on the saturated ideal in a fixed overorder returns an
   M-independent input. M-dependent order choice needs a separate reduction.
4. Attempt classical ideal-class, unit and lattice attacks before attributing
   a signal to quantum structure. The loose d64 geometry already has a
   classical cover; this encoding does not undo that negative result.

Scope excludes arbitrary quaternion orders, arbitrary field degrees,
fractional-coefficient maximal overorders and all short-element algorithms.
No cryptographic hardness or novel algorithm follows from the obstruction.

## 5. Executable Evidence

`theorems/native_rlwe_conductor_order.py` constructs the graph and contained
local-principal basis, computes exact determinant indices, checks left action
and audits the same adjoint-mapped saved d64 kernel. `--save` writes
`research/reductions/native_rlwe_conductor_order.json`. Bounded d4 calibration
checks all6561 {-1,0,1} coefficient pairs:48 ambient units, zero mixed units.
This is not a fast unit search or an exhaustive proof about unbounded units.

Tests: `tests/test_native_rlwe_conductor_order.py`. Independent BigInt checker:
`research/certificates/native_rlwe_conductor_order_crosscheck.js`. Published
theorem dependence and global proof still require independent mathematical
review. Gemini owns CLI/registry integration and full production validation.
