# Hermitian Qutrit Pilot: Actual Readout And Source-As-Solution Test

2026-10-17. Local derivations, review pending; no novelty claim.

## Scientific Question

Can the known low-bond qudit pilot construction yield a noncommuting
Hamiltonian optimization algorithm that escapes the independent-qubit
radius solver and the existing classical OPI/polar competitors?

We first considered dependent-qubit wrappers. For H0 anticommuting with Q,
(H0+gQ)^2=H0^2+g^2 I; a wrapper alone transforms an existing spectrum, not
a new decoder. No dependent-code decoder was implemented or assumed here.
We instead changed the involution assumption: order-three Weyl generators
do not obey the preceding qubit square-root recurrence.

[Wocjan's pilot MPS](https://arxiv.org/abs/2604.01022) applies to uniformly
twisted generators, including qudits.
[General-Pauli HDQI](https://arxiv.org/abs/2601.18773)
separately charges source and decoding.
Neither supplies a ready Hermitian qutrit optimizer for the family below.
Do not substitute a non-Hermitian free-parafermion spectrum for this task;
[Fendley's model](https://arxiv.org/abs/1310.6049) explicitly distinguishes
the non-Hermitian setting. These references motivate a test, not a novelty
or hardness claim for our family.

## Explicit Problem And Proposed Mechanism

On m qutrits define X|b>=|b+1 mod3>, Z|b>=omega^b|b>, omega^2+omega+1=0,

    U_j = Z_0 ... Z_(j-1) X_j,
    H = sum_j c_j (U_j + U_j^dagger),       c_j explicit signed integers.

This is an explicit physical many-body family, not a hidden oracle. X
pivots make the U_j labels independent over F3. Ordered products E_r
(r in F3^m) are Hilbert-Schmidt orthogonal. Decoding their labels is linear:
x_j=r_j, z_j=sum_(l>j)r_l; no unknown low-weight decoder is supplied.

Proposed algorithm: prepare coefficients alpha_r(P(H)) as a pilot state,
apply public label SUMs and a tensor-product qutrit Bell transform, then
discard the reference half. For Hermitian real P this gives P(H)^2/Tr(P(H)^2).
Use P=(t-H)^k, t=2 sum|c_j|, rather than H^(2k) which need not favor low
energies. A major advantage would require a polynomial source AND a charged
degree/gap/overlap argument beyond the best classical baseline. None is
assumed. The native source uses exponential exact coefficient enumeration
and charged TT-SVD; those are calibration tools, NOT the proposed algorithm.

## Result 1: Hermitian Completion Breaks The Direct Pilot Transfer

For A=sum c_j U_j, the one-directional relation gives A^3=(sum c_j^3)I.
The small source has low-degree algebra, but A is non-Hermitian. Adding
U_j^dagger introduces both omega and omega^-1 commutations and a commuting
inverse partner for each generator. With at least two noncommuting pairs,
no generator is uniform against all remaining predecessors: there is no
valid last vertex for that theorem's ordering.

The degree-two Hermitian coefficient tensor on c=[2,3,5,7], cut2, has a4x4
minor with EXACT determinant -4200-8400*omega, nonzero in Z[omega]. Thus the
bond bound degree+1=3 cannot be copied to this natural grouped-site pilot.
The corresponding one-directional power has rank3. This rejects a precise
transfer claim, not all polynomial bonds, site reorderings, gauge changes
or efficient non-MPS quantum source circuits.

Higher controls retain all initial six/eight-site exploratory inputs through
degree10, including saturation. They are exact modular lower-bound witnesses
(omega maps to5 mod31), not fitted exponents or rank upper bounds. All56
records retain coefficients, degree, cut, selected rows/columns, the minor
and its nonzero determinant. No asymptotic rank fit or hardness inference
is performed. The degree-two determinant is additionally evaluated directly
in characteristic zero, independently of numerical SVD.

## Result 2: Readout Actually Works

Exact coefficient multiplication uses

    E_r U_j^s = omega^(s*sum_(l>j)r_l) E_(r+s e_j),   s=+1,-1.

No floating phase is used by this expansion. The native readout starts from
the pilot and zero ancillas, computes the public z labels, applies one
qutrit Fourier per reference coordinate, and then coordinatewise SUM. It
does NOT use one cyclic Fourier over dimension3^m. It uses
m(m-1)/2+2m ideal logical qutrit Clifford gates; no fault-tolerant compilation
is claimed. Three full-state controls compare the prepared purification to
vec(P(H))/norm(P(H)) and its energy to dense physical matrices. All sources
and exponential transition counts are retained. Merely getting the label
law right would not pass these checks.

## Result 3: The Source Is Already The Filtered Seed State

E_r|0>=|r>. Therefore alpha(P(H))=P(H)|0>, not a freely supplied string of
coefficients. Since <0|E_r|0>=Tr(E_r)/3^m, this seed is a trace vector for
the generated algebra. More strongly, left multiplication obeys

    U_j E_r = omega^(sum_(i<j)r_i) E_(r+e_j),

exactly the SAME prefix-Weyl action on the pilot coordinates. The Bell
isometry intertwines H on the pilot and H on the physical output. Thus for
ANY normalized pilot, input and output have identical energy expectations.
Native tests check this for actual filters AND arbitrary entangled pilots.
Constructing a high-quality quantum pilot could still be an algorithm, but
the decoder/readout has not removed its hard preparation step. This is not
a general assertion that all HDQI or quantum state preparation is circular.

## Result 4: A Matched Classical MPS Competitor

Given an actual supplied pilot MPS A_j[r] of bondD, pair the output a_j and
reference b_j at each site. Track s=sum_(i<j)b_i mod3 and use

    T_j[(alpha,s),(a,b),(beta,s+b)]
      = A_j[alpha,a-b,beta] * omega^((a-b)*s) / sqrt(3).

Start at charge0 and sum the final charge. This is the ACTUAL output
purification with bond at most3D, not an assumed tensor-network truncation.
Its product-Weyl energy is contractible classically. Even more directly,
contract the same H in the pilot MPS: the intertwiner identity gives the
same mean without any output construction. Hence a constructible polynomial-
bond controlled-precision pilot cannot support an ENERGY-estimation
separation here. This does not claim the unknown optimum energy is easy.

A live64-site product-pilot control executes the charge construction and
both energy contractions, checked by an independent scalar product formula.
No3^64 source, Hamiltonian, state or density matrix is built. It is a
calibration of the universal map, explicitly NOT an efficiently constructed
Hamiltonian-filter pilot. Small arbitrary entangled sources check the map
against full arrays. Floating contractions/SVDs are not interval certificates;
controlled precision and constructibility remain premises of the asymptotic
classical comparison. No general measurement or non-MPS dequantization follows.

## Decision And Next Experiment

Run `python theorems/hermitian_qutrit_pilot.py --write` and
`python -m pytest tests/test_hermitian_qutrit_pilot.py -q`.

Do not implement the known one-directional pilot formula as if it already
prepared a physical Hermitian optimizer. Do not declare growing finite
ranks a quantum advantage. Do not compile a low-bond pilot to claim an
energy speedup already matched by these contractions.

The surviving scientific question is an explicit efficiently constructible
NON-MPS source or a code-aware, dependent-label mechanism whose actual
readout is not this finite-charge contraction. Any proposal must name that
source/decoder and its polynomial filter/gap guarantee before a new
subsystem. Further degree/site-size scans do not resolve this blocker.
No central candidate, general negative, proof promotion or novelty claim.
