# Exact three-site Gaudin generator falsifier: parent derivation

2026-11-13. Exact control code fully parent-read; independent scope review
pending. Native N4,M2, sites(0,1,3,7),g=1/3 and charges from
GAUDIN_JOINT_CHARGE_TRAVERSAL.md. No quantum implementation.

For a universal joint eigenbasis transport generator A=iK with K real
antisymmetric, necessary equations are
[Q_j,V_i-[K,Q_i]]=0 for all i,j, V_i=dQ_i/dg. The exact rational control
has rank12/13 for the at-most3site current span, with an explicit13term
left-null certificate yA=0,yb=1. The unrestricted antisymmetric problem
has rank15/15 and a verified unique solution in the six-dimensional
sector. In ordered basis0011,0101,0110,1001,1010,1100 its corner is

  K[0011,1100]=355248848800449/125250068977266446 !=0.

These bitstrings differ at all four sites. Every operator supported on
at most3sites has this matrix element ZERO. Therefore a unique necessary
K with this nonzero corner refutes a universal3site formula at this
native instance. All exact commutators vanish and sum_i Q_i=2I.

Proposed scope extension, independently under check: for arbitrary
Hermitian A=S+iK, S real symmetric and K real antisymmetric, real and
imaginary parts of the generator equations separate, so S cannot repair
this K obstruction. Since all Q_i preserve the fixed-M sector, projecting
an arbitrary number-nonconserving A to that sector still obeys the same
necessary equations; a3site operator cannot acquire a Hamming4 entry
under projection. Commuting gauge/branch phases do not repair it.

Boundary: universal simultaneous joint-eigenbasis generator ONLY. This
is not a lower bound on a chosen individual branch, approximate control,
growing-locality formula, integrated transport cost or general preparation.
The complete finite example disproves a universal assertion; it establishes
no asymptotic impossibility. Stop this ansatz, no N6 or nearby sweep.
Artifacts: audits/controls/gaudin_local_agp/control.sage,result.json,
certificate.json. The full matrix solution is a positive algebraic control,
not an efficient many-body algorithm. Paid constructive and analytic
reports remain separate and advisory.
