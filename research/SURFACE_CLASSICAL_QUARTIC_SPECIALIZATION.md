# Native classical quartic reconstruction

2026-11-14. Reviewed WRITTEN specialization of the already established
classical surface pipeline. For EVERY smooth quartic in P3/Fp, input only
binary p and its coefficients, compute exact degree22 P2 in randomized
poly(logp,log(1/eta)) BIT time. Fixed degree is essential. This matches the
same native quantum endpoint; no implementation, practicality, novelty,
human/formal verification, hardness, separation or quantum execution claim.

The full141-line independent dependency check in
audits/reviews/2026-11-14-positive-surface-selection.md was parent-read.
The parent checked the changed geometry/atlas/boundary calculations against
SURFACE_CLASSICAL_NATIVE_RECONSTRUCTION.md, SURFACE_NATIVE_COVER_CONSTRUCTION.md,
the normalized-frame proof, and the actual Pila2005 TheoremsD/E/F.
This reuses the closed native arithmetic/height/lifting/reconstruction
proofs, not the earlier refuted ordinary compact=parabolic source assertion.

## Changed fixed parameters and proof obligations

For the cubic pencil on a quartic, K_X=0,H^2=4. Its complete-intersection
(4,3) fibres have degree12, genus19; n=38. The36 basepoints give Euler60
after blowup and r=60-2(2-38)=132 nodes. One-node fibres are irreducible:
A+B=3H,A.B=1 gives A^2=3a-1>a^2/4 for1<=a=H.A<=6. The same verified
Lefschetz, integral torsion-free H1/H2 and finite-coefficient monodromy
proofs apply; odd surface degree is not a hypothesis. No rational point,
section, torsion basis, target Frobenius or monodromy advice is added.

The native atlas is explicitly specialized, not inferred from smaller genus:
a degree12 hyperplane pencil has at most60 ramified values. Among0..1725
choose1666 etale fibres. Five give degE=60 and h0(E)=42; the other1661
give closed evaluation length19932>(8*42-4)*60=19920. The (4,3) Koszul
shifts m-7,m-4,m-3 give h0(kE)=60k-18. Anderson's degE>=2g+1 holds
(60>=39); compression/radical/addition/family constructions retain fixed
format and polynomial coefficient-bit bounds. The actual Weil pairing
uses43 slots per point, closed degrees<=12, and common degree<=12^86
for two points. No unknown arithmetic scalar is substituted.

For Gamma=GSp38(Fell), |Gamma|<ell^742. The complete natural multiplicity
is (r-2)n=4940, fixed. Native module extraction, numerical lifting, explicit
heights, finite coordinate algebra and original-prime Frobenius use the
existing variable-cover degree/genus interfaces. No ambient full-torsion
enumeration is inserted. Auxiliary-prime selection and later saturated RR
retain the already proved order, with no circular extra exclusions.

Node normalizations have genus18 and bounded explicit models. Actual
Pila2005 D/E/F covers this bounded family over ANY field; a fixed-Q-family
theorem alone would not pay the boundary. The degree ledger is

    open4940 - boundary132*37 = parabolic56,
    surface degree = 56+2-36 = 22.

The boundary factors remain (1-epsilon_z*T^degz)*P_norm,z(T^degz), and

    P2_X=(1-pT)^2 * P_par / product_b(1-p^degb*T^degb).

Keep ell>53,ell!=p and CRT modulus>2^23*p^22. Largest ell isO(logp).
If p is below any required explicit fixed polynomial thresholdQ(ell),
direct counts through extension degree22 cost p^O(1)<=Q(ell)^O(1).
All finite clocks, completeness certificates and failure caps are retained.

## Consequence and next action

The old quartic note's native-classical OPEN statement is superseded.
The separate Kuga--Satake construction may remain open, but it is no longer
needed to match this endpoint. The quantum theorem is not refuted; an
unmatched-asymptotic interpretation is retired. No new quantum subsystem or
repeated G0 confirmation is warranted. Select a genuinely new constructive
output; current admission question is CASSELS_TATE_NATIVE_ADMISSION.md.
