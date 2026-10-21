# Referee queue

Generated on 2026-10-22 from `research/audits/reviews/reviews.json` by `python tools/referee/referee.py render`.
Reviews come from in-session model judges that quote each claim from the note; they are a
triage, not peer review. The referee never edits `research/*.md`.

| Overall | Notes |
|---|---|
| unsound | 0 |
| needs-work | 29 |
| unclear | 0 |
| sound | 5 |
| stale | 0 |

## Flagged

Unsound and needs-work reviews of notes that have not changed since.

| Note | Overall | Reviewed | Worst claim |
|---|---|---|---|
| [AFFINE_CLUSTER_NATIVE_PROBE](reviews/AFFINE_CLUSTER_NATIVE_PROBE.md) | needs-work | 2026-10-22 | gap: "The BPQM tree certificate survives, but a classical separation is STILL UNESTABLISHED" Headline scope (both judges). Every experiment in this note is a classical sampler or exact contraction on finite graphs; none tests the tree certificate, so 'survives' reports no evidence. The dec... |
| [BPQM_GIBBS_FRONTIER](reviews/BPQM_GIBBS_FRONTIER.md) | needs-work | 2026-10-22 | gap: "It supplies a specified decoder family, public input, rigorous local test and known sampling reduction" Headline scope (both judges). The 'rigorous local test' rests on a degradation argument the note says 'remains review pending'; it certifies a beyond-ceiling tree condition only at (dv,dc)=(3,6), c... |
| [COHERENT_BPQM_ERASURE](reviews/COHERENT_BPQM_ERASURE.md) | needs-work | 2026-10-22 | gap: "The coherent erasure stage is now implemented and its phase/workspace composition is checked" As a headline this drops the scope stated in the body. The phase/workspace composition was executed only on the declared M5 code (checks 25,26,12; 12 qubits; gate-reference cap 10 data wires, state... |
| [CONJUGATE_CHIRP_REPAIR](reviews/CONJUGATE_CHIRP_REPAIR.md) | needs-work | 2026-10-22 | gap: "m=Theta(n), bounded list densities and p>=m+1, H<=exp(O(n)) but p^n grows as exp(Omega(n log n" The producer sets A^2=max(rho/(1-rho),(1-rho)/rho) (theorems/conjugate_chirp_repair.py, postselection_bound), so H<=(1+A^2)^m=exp(O(n)) needs list densities bounded away from 0 and 1. Every density... |
| [DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT](reviews/DCP_INTERLEAVED_TREE_MERGE_SYNDROME_PRUNING_AUDIT.md) | needs-work | 2026-10-22 | gap: "coincidence pruning strictly purifies the phase error" The sign statement is algebraically correct: the numerator p(1-p)(2-3p)(1-cos(2pi/q))/2 is positive for 0<p<2/3. It is, however, a statement about the conditional posterior of classical latent erro... |
| [EXPLICIT_CUBIC_OPI](reviews/EXPLICIT_CUBIC_OPI.md) | needs-work | 2026-10-22 | gap: "Explicit Cubic-Target OPI: A Structural Classical Falsifier" The headline drops the body's scope: the 'falsifier' is a finite, seeded, best-of-four classical score against a one-shot quantum mean at four sizes, with no matched tails or runtime, and the narro... |
| [EXPLICIT_QUADRATIC_OPI](reviews/EXPLICIT_QUADRATIC_OPI.md) | needs-work | 2026-10-22 | gap: "The high-rate quadratic family has a constructive classical explanation, not a remaining quantum-advantage candidate" The supporting perfect-solution argument holds only with high probability for independent uniform T_i in GL(t,2), only asymptotically for fixed R>1/2 as t grows, and is review pending. The note its... |
| [FOLDED_NORM_SOURCE](reviews/FOLDED_NORM_SOURCE.md) | needs-work | 2026-10-22 | gap: "Folded Norm Source: Phases, Scalar Rank And Matched Attacks" The norm-pencil section states that the budgets are 'deliberately EXPLICIT but NOT MATCHED' (96 full interpolations against 8192 scored line parameters), and that 'No matched quantum wall-clock/gat... |
| [INTERVAL_SOFT_DECODER](reviews/INTERVAL_SOFT_DECODER.md) | needs-work | 2026-10-22 | gap: "cut claims of a SUPERPOLYNOMIAL quantum-search separation at constant full-RS interval width" The classical argument behind this cut covers only the KV-certified window d/p<C<=L/p, which forces d<L. At constant L with growing codimension outside that window, the DP costs O(N*L*d*p^d) and is... |
| [JACOBI_KNOWN_NORM_REDUCTION](reviews/JACOBI_KNOWN_NORM_REDUCTION.md) | needs-work | 2026-10-22 | gap: "Known Relative Norm Removes The Prime-Conductor Quantum Opening" The title states the removal unconditionally. The status line and Next Research Action make it 'subject to independent review of the application', and the Lenstra-Silverberg recovery algorithm was ... |
| [JACOBI_SURFACE_RECONSTRUCTION](reviews/JACOBI_SURFACE_RECONSTRUCTION.md) | needs-work | 2026-10-22 | gap: "Under the stated Jacobi/primary identities this removes the prime-conductor asymptotic quantum opening" The headline paragraph states the removal as established, while it rests on JACOBI_KNOWN_NORM_REDUCTION's local application of Lenstra-Silverberg Theorem 1.3, which is review pending (artifact flag... |
| [NATIVE_RLWE_CONDUCTOR_ORDER_AUDIT](reviews/NATIVE_RLWE_CONDUCTOR_ORDER_AUDIT.md) | needs-work | 2026-10-22 | gap: "Native RLWE: Exact Metric, Nonprincipal Quaternion Ideal" The title asserts nonprincipality without conditions. Section 3 proves nonprincipality only for M!=0 mod q: the zero ratio gives Lambda_0=qR+Rj=O_q*j, which is principal and has source probability ... |
| [NATIVE_RLWE_IDEAL_CLASS_ORBIT_AUDIT](reviews/NATIVE_RLWE_IDEAL_CLASS_ORBIT_AUDIT.md) | needs-work | 2026-10-22 | gap: "Native Quaternion Ideal Classes: Public Dihedral Orbits" The title presents native quaternion ideal classes in general as public dihedral orbits. The classification in Sections 1-3 holds only on the generic source (M a unit and beta=1+M*bar(M) a unit mod... |
| [NATIVE_RLWE_PRIMAL_BABAI_CERTIFICATE](reviews/NATIVE_RLWE_PRIMAL_BABAI_CERTIFICATE.md) | needs-work | 2026-10-22 | gap: "Native Ring-LWE: Direct Classical Decoding At The Lower Modulus" Headline scope (both judges). Read alone, the title asserts classical decoding at the q-near-d^4 modulus in general. The note certifies only two seeded labels at d=64, q=16777259, under the exact d... |
| [NATIVE_RLWE_SPARSE_WITNESS_AUDIT](reviews/NATIVE_RLWE_SPARSE_WITNESS_AUDIT.md) | needs-work | 2026-10-22 | gap: "On typical native labels this does not produce a sufficiently short point" The certificate covers witnesses of norm <=R with R=2^40, 2^53, 2^66, which equals 2*sqrt(dq) at the three references; the note never shows R is the decoder's passing radius. The rotational decoder... |
| [NATIVE_RLWE_SUBFIELD_COVER_AUDIT](reviews/NATIVE_RLWE_SUBFIELD_COVER_AUDIT.md) | needs-work | 2026-10-22 | gap: "This independent source counting excludes typical successful AFFINE witnesses in the stated restricted output class" The restricted output class of Section 2 allows every divisor h, including h=d/2. The counting bound is vacuous at half degree in all six reference rows (artifact density_log2_strict_upper +221, +2... |
| [NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT](reviews/NATIVE_RLWE_UNIT_ORBIT_GENERATOR_AUDIT.md) | needs-work | 2026-10-22 | gap: "A quantum unit wrapper around the unmodified native generators would be solving the wrong search space" Units cannot leave a native line (Section 2 is general), but whether the two native lines are the wrong search space depends on both fixed-line lower bounds exceeding t^2/E^2. That is checked only ... |
| [OPI_FILTER_TAIL_CERTIFICATE](reviews/OPI_FILTER_TAIL_CERTIFICATE.md) | needs-work | 2026-10-22 | gap: "Thus classical105/127 and104/127 remain verified witnesses but do NOT kill the quantum tail" On seed 29 (classical_best_of_four=105), the certified lower tail at 105 is 0 for filter degrees 16/18/19. Nothing quantum is certified at that instance's classical score, and the only positive tai... |
| [OUTER_CODED_CHIRP_PROBE](reviews/OUTER_CODED_CHIRP_PROBE.md) | needs-work | 2026-10-22 | gap: "a deterministic classical construction below solves EVERY target in the entire proposed useful rate range, and beyond" The algebra behind it holds, but the decision sentence states no limit for 'and beyond'. The construction is proved only for full support N=p-1 with 1<=r<N/2 strictly, and it fails at r=N/2: the no... |
| [POLAR_CONDITIONAL_SAMPLER](reviews/POLAR_CONDITIONAL_SAMPLER.md) | needs-work | 2026-10-22 | gap: "It resolves the missing public-set premise below for that finite family" This note's premise is 'epsilon_F->0 with a polynomial construction' for a code family. The follow-up certifies a single half-rate length (N32768) at fixed TV 0.0102; half-rate is UNKNOWN at every ... |
| [POLAR_SOURCE_DESIGN](reviews/POLAR_SOURCE_DESIGN.md) | needs-work | 2026-10-22 | gap: "Largest set certified at average TV<=0.1" The rows shown match the artifact (16/64, 78/256=0.304688, 361/1024=0.352539, 1614/4096=0.394043, with TV uppers 0.0826, 0.0935, 0.0998, 0.0995). However, the artifact also has an N16 instance (max... |
| [PRIME_CHARACTER_CAPACITY_SOURCE](reviews/PRIME_CHARACTER_CAPACITY_SOURCE.md) | needs-work | 2026-10-22 | gap: "without randomizing input shifts? YES for the flat-spectrum primes below" The YES is unqualified by radius or instance. Non-trivial bounds are certified only at one large instance (N127,K39,p=2^61-1, both zero conventions) for ell24 and ell32. Recomputed: ell37 gives eps... |
| [PRIME_CHARACTER_EXTERIOR_BOUND](reviews/PRIME_CHARACTER_EXTERIOR_BOUND.md) | needs-work | 2026-10-22 | gap: "This is a genuinely enlarged fixed-input guarantee, not an empirical seed-success estimate" The guarantee rests on the imported compact-support trace formula, Hc0/Hc2 vanishing and the weight application. 'Attempts To Disprove It' item 4 says these 'still need independent review', and the... |
| [PRIME_CHARACTER_FINITE_READOUT](reviews/PRIME_CHARACTER_FINITE_READOUT.md) | needs-work | 2026-10-22 | gap: "radius32, the certified normalized mean is about 0.9028547353515506" The value matches the artifact (ell32 heralded mean lower bound) and recomputation (127*0.9028547=114.66). But the Result calls it 'certified' without saying that the Gram/readout application and t... |
| [PRIME_CHARACTER_INTERLEAVED_PROBE](reviews/PRIME_CHARACTER_INTERLEAVED_PROBE.md) | needs-work | 2026-10-22 | gap: "A Fast Interleaved Decoder Does Not Preserve This DQI Objective" The body says 'The decoder ingredient WORKS' and that the attempted quantum repair (shared support, separate QFTs, selection among original rows) fails, at the single parameter set N127, K39, ell32... |
| [PRIME_CHARACTER_MORSE_ATTACK](reviews/PRIME_CHARACTER_MORSE_ATTACK.md) | needs-work | 2026-10-22 | gap: "A sufficient condition for >=1/(2n) is p>=max(64G^2,4*R_branch*h" No derivation is given. p>=64G^2 gives 2G*sqrt(p)<=p/4, but the bound uses ceil(sqrt p), so 2G*ceil(sqrt p)<=p/4+2G. With R*h<=p/4 the numerator is then only at least p/2+1-2G, which is below p/2. ... |
| [PRIME_CHARACTER_NORM_ATTACK](reviews/PRIME_CHARACTER_NORM_ATTACK.md) | needs-work | 2026-10-22 | gap: "but left mixed high-rate controls at124/127 and122/127" The previous experiment's artifact also leaves N31,K16 mixed seed71 at 30/31 (r=2, rate 16/31>1/2) and the r=3/r=4 mixed controls below perfect. The norm attack was not run on N31, and its budget K... |
| [PRIME_CHARACTER_OPI](reviews/PRIME_CHARACTER_OPI.md) | needs-work | 2026-10-22 | gap: "all25 native polynomials fail perfect strict satisfaction" The coset orientation is not stated, and the claim depends on it. Exhaustive check: with the common square coset (orientation 0, the one tests/test_prime_character_opi.py uses), 0/25 polynomials ar... |
| [PRIME_CHARACTER_PHASE_FEEDBACK](reviews/PRIME_CHARACTER_PHASE_FEEDBACK.md) | needs-work | 2026-10-22 | gap: "There is a concrete interference-restoring action, verified on full native states and locally bounded without selecti..." Full native-state verification exists only for the four two-row controls at p7/11, N4, K2, ell1, plus one three-row test. At N127, K39, ell32 the restoration is an analytic certificate that 'additi... |

## Stale

Notes edited after their review; re-run the referee on them.

None.

## Next 30

Review-pending notes without a current review, newest first.

| Note | Date |
|---|---|
| NATIVE_RLWE_SINGLE_WITNESS_TARGET | 2026-10-04 |
| NATIVE_RLWE_ROTATIONAL_WITNESS_REDUCTION | 2026-10-04 |
| NATIVE_RLWE_PRELABEL_PIP_FALSIFIER | 2026-10-04 |
| NATIVE_RLWE_NORM_LIFT_AUDIT | 2026-10-04 |
| NATIVE_RLWE_NONUNIT_WITNESS_AUDIT | 2026-10-04 |
| NATIVE_RLWE_HOMOGENEOUS_DGS_REDUCTION | 2026-10-04 |
| NATIVE_RLWE_GAUSSIAN_COOLING_AUDIT | 2026-10-04 |
| NATIVE_RLWE_COHERENT_READOUT_AUDIT | 2026-10-04 |
| NATIVE_RLWE_CHOSEN_PREIMAGE_REDUCTION | 2026-10-04 |
| NATIVE_RLWE_SAMPLE_ACCESS_AUDIT | 2026-09-29 |
| NATIVE_RLWE_PHASE_DECODER_TARGET | 2026-09-29 |
| NATIVE_RLWE_GAUSSIAN_SAMPLER_AUDIT | 2026-09-29 |
| NATIVE_RLWE_COVARIANT_DECODER_TARGET | 2026-09-29 |
| KNOWN_PHASE_SIEVE_DEQUANTIZATION | 2026-09-29 |
| STRUCTURED_EDCP_SMALL_SECRET_TARGET | 2026-09-28 |
| STRUCTURED_EDCP_POLYNOMIAL_LIFT_AUDIT | 2026-09-28 |
| STRUCTURED_EDCP_GAUSSIAN_SUPERPOSITION_AUDIT | 2026-09-28 |
| STRUCTURED_EDCP_CONDITIONAL_METRIC_AUDIT | 2026-09-28 |
| STRUCTURED_EDCP_ARCHIMEDEAN_GAUSSIAN_AUDIT | 2026-09-28 |
| STRUCTURED_EDCP_SOURCE_HARDNESS_AUDIT | 2026-09-27 |
| STRUCTURED_EDCP_SHEAR_ALIAS_DECODER | 2026-09-27 |
| STRUCTURED_EDCP_NONLINEAR_CHIRP_AUDIT | 2026-09-27 |
| STRUCTURED_EDCP_MODULE_GLUING_AUDIT | 2026-09-27 |
| STRUCTURED_EDCP_IDEAL_COLLISION_CORE | 2026-09-27 |
| STRUCTURED_EDCP_FOURIER_ERASURE_AUDIT | 2026-09-27 |
| STRUCTURED_EDCP_WIDE_PHASE_INFORMATION | 2026-09-26 |
| STRUCTURED_EDCP_PHASE_SOURCE_MOMENTS | 2026-09-26 |
| STRUCTURED_EDCP_DIRECT_PHASE_SOURCE | 2026-09-26 |
| STRUCTURED_EDCP_UPSTREAM_MIXING_AUDIT | 2026-09-25 |
| STRUCTURED_EDCP_PROFILE_LIST_DECODER | 2026-09-25 |
