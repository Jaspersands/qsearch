# Gaussian-channel mixture: convention and actual-source closure

2026-11-07. STATE/TRAPS read; `/opt/anaconda3/bin/python`; no network/Git/API
or new tests. This closes the source/convention interface, not the proposed
polynomial full-diamond learner. Source snapshots are under
`audits/sources/mixed_gaussian_pair/` and `gaussian_channel_selection/`.

## Reference first: accepted without global W

Define the FULL ordinary qubit channel by
`E(rho)=Tr_ENV U_G(rho tensor |vac><vac|)U_G^dagger`, in the fixed ordering
SYSTEM,ENV, with U_G an even Gaussian unitary. In the enlarged ordering
REF,SYSTEM,ENV, a last-register Majorana is `P_REF tensor c_SE`. Therefore
each quadratic SE generator has two P_REF factors, which cancel:
`I_REF tensor U_G` is a Gaussian unitary in the GLOBAL Majoranas.
For a fixed Gaussian maximally entangled Omega on REF,SYSTEM, its product
with vacuum ENV is Gaussian, remains Gaussian under this unitary, and stays
Gaussian after ordinary partial trace of the LAST environment modes.
This proves Gaussianity of `(Id_REF tensor E)(Omega)` directly. No fermionic
tensor-product identification or global parity correction is being omitted.
The channel is defined on ALL qubit inputs, including parity coherences.

One particularly convenient fixed Omega is the even BCS state

`|Omega_n> = 2^(-n/2) product_j(1+a_Rj^dagger a_Sj^dagger)|vac>`
`          = 2^(-n/2) sum_x (-1)^(binom(|x|,2)) |x>_R |x>_S`.

Creation operators are in the order REF then SYSTEM. The sign counts the
selected S_j/R_k crossings. Consequently
`|Omega_n>=(V_REF tensor I)|Bell_n>`, where
`V_REF=product_(j<k) CZ_Rj,Rk=V_REF^dagger` is a known reference-ONLY
Clifford of O(n^2) gates. Ordinary channel use commutes with V_REF, so the
corrected Choi state is exactly reference-unitarily conjugate to the
ordinary normalized Choi state. Reference marginal remains I/2^n.
The initial state and correction are exact Clifford preparations in this
model, not approximate noisy copies or supplied purification access.

With Bravyi's `c_(2j-1)=Zprefix X, c_(2j)=-Zprefix Y` and plus-i covariance,
put `K=direct_sum_j sigma_x`. Omega has covariance `[[0,K],[-K^T,0]]`.
For source channel `M -> A M A^T+B`, corrected reference-first Choi covariance
is `[[0,K A^T],[-A K^T,B]]`. In the learner's minus-i convention and
`Gamma -> L Gamma L^T+Z`, it is `[[0,-K L^T],[L K^T,Z]]`.
The source's alternative cross-I maximally entangled state also works;
its reference Clifford includes known X/S factors. Do not mix these states'
cross-covariance conventions.

## Actual source maps and the alternative first-half route

`mixed_gaussian_pair/gaussian_channels.txt`43–66 defines its Majorana/CM
signs;72–88 Eq2 supplies Gaussian Schmidt pairs with K blocks sigma_x.
Its channel action and Gaussian CJ/CP conditions are89–128:
`I-AA^T-iB >= 0`, equivalently its complex conjugate with +iB.
The Gaussian dilation and purification are196–235, Eqs7–8. These use a
possibly MIXED Gaussian environment, not a free vacuum environment.
Purifying that environment costs O(n) modes; if its pure Gaussian
purification has odd parity, append a parity-balancing mode. The resulting
even pure Gaussian environment is Gaussian-unitarily preparable from vacuum.
Thus the fixed vacuum/even-unitary native promise can cover these channels
with O(n) environment modes, without granting access to those modes.

Conversely a physical Gaussian corrected Choi state with reference covariance
zero gives the stated CP inequality by Schur complementation. The source
dilation builds the channel with those A,B; the reference-first argument
gives that same corrected Choi covariance. Gaussian-state uniqueness and
ordinary Choi injectivity identify the FULL ordinary channels. Merely saying
“maps even Gaussian inputs to Gaussian outputs” would be insufficient:
parity conjugation leaves their covariances unchanged but changes the action
on odd operators. The full Stinespring/corrected-CJ definition removes this
ambiguity.

For comparison, `mixed_gaussian_pair/bravyi_maps.txt`552–589 defines Gaussian
maps on arbitrary input operators;634–642 proves parity preservation;
666–704 gives CP/TP. Its first-half fermionic tensor convention is703–742,
and its identity dual state is752–770. In output/reference order its ordinary
realization uses `J=Ad_W`, `W=(-1)^(N_output N_reference)`: prepare J(rho_I),
query E on the first register, then apply W^dagger to recover the Gaussian
fermionic dual. That route is also polynomial, but its W is unnecessary in
the reference-FIRST native convention proved above. Do not apply ordinary E
to the first half of rho_I and silently identify it with the fermionic dual.

## Opened prior learners and lower bound: exact scope

- `few_nongaussian.txt`181–224/Theorem1 promises black-box UNITARY
  `U_t=G_t K_t ... G_0`, with constantly many bounded-weight nonGaussian
  unitaries. It learns that unitary channel in diamond distance. The
  constant-core channel tomography at620–660 is an internal step, not an
  arbitrary noisy-channel input theorem. Existence of a hidden Stinespring
  dilation does not grant the learner unitary/environment access.
- `flo_learning.txt`134–161 explicitly treats pure states and UNITARY
  channels; Theorem1.1 learns active FLOs, and1.3 at201–210 passive FLOs.
  Its query model permits coherent/interleaved repeated unitary calls.
  Lines169–190 explain the parity-relative phase and distinguish full diamond
  from the weaker guarantee on parity-eigenstate inputs. Neither opened
  theorem establishes arbitrary mixtures of TWO noisy Gaussian CPTP maps.
- `limited_parallel.txt`5988–5990 and6034–6058/TheoremC.2 is BOSONIC. Its
  channels output two known Gaussian states with weights depending on a
  measurement of the input, as EqC38 explicitly shows. It does not promise
  a fixed convex mixture of two Gaussian maps. Its transfer-function lower
  bound is not a lower bound for this fermionic/full-diamond native family.

## Obligations not supplied by these sources

A memoryless ordinary channel gives exact IID corrected Choi-state copies,
one ordinary use per copy, using n reference modes and known Clifford gates.
The earlier two-Gaussian STATE learner therefore has the correct input
access, but its trace-error guarantee alone does not pay full diamond error:
generic normalized-Choi conversion loses 2^n. A uniform restricted-family
conversion still needs proof. Physical output also needs payment: learned
Gaussian-state components need not be TP Choi components, and total
approximate reference marginal is not by itself an efficient CPTP projection.
Full-input Bell postselection succeeds only with 4^(-n); the previous
constant-input-core channel argument cannot remove this cost here. No
full learner, novelty, separation or applicable lower bound is certified by
this source/convention review.
