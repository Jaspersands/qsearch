# Source-Preserving Native Descent And Reference Recovery

LOCAL DERIVATION / EXTERNAL REVIEW AND NOVELTY CHECK PENDING.
This is an actual source-driven reference execution of a known-style measured
descent mechanism, not a new Shor-level algorithm, an arbitrary StateHSP
receiver, or polynomial recovery at growing depth. The supplied source is the
existing native cyclotomic phase family, not a manufactured oracle problem.

## Input And Honest Scope

At native level L, let R_L=Z[zeta3]/(pi^L), pi=zeta3-1. Supplied inputs have
PUBLIC independent uniform labels a inR_L^n and UNKNOWN secret s inR_L^n:

    |psi_a^s>=1/sqrt3 sum_j chi_L(a.lambda_j.s)|j>,
    lambda=(0,1,1+zeta3).

This uses the existing exact pairing and mixed-characteristic carry backend.
It works for full ring-valued secrets; no integer-embedding/Galois assumption
is used. The physical source/independence/ideal-phase law is a PRECONDITION,
not established by viewing a few samples or supplied for free by this pass.
True secrets occur only in forward producer/test fixtures. The receiver takes
sample packets, public labels, measurement records and learned lower prefixes.

The numerical backend represents supplied quantum registers by statevectors.
Reading their amplitudes is simulator bookkeeping, not permitted classical
access in a speedup comparison. The actual merge recipe consists of qutrit
SUM-inverse gates, complement measurements and ONE retained pivot. The final
digit gates use only labels and already learned prefixes. Hardware compilation
and source/noise error composition remain open.

## Exact Measured Level Drop

Choose a NONEMPTY block using only public residue vectors a_i mod pi, with
sum_i a_i mod pi=0. The existing streaming F3 ZeroSumBuffer guarantees such
a subset inside W=(n+1)^2 inputs. Unused registers remain in its live buffer.

Use the existing cycle-basis recipe: pivot t=j_0, offsets v_i=j_i-j_0 mod3.
Measure all offsets except the pivot, accepting EVERY outcome. For ideal
inputs their joint probability is3^(1-B), independent of labels and secret.
The retained normalized vector has amplitudes proportional to

    prod_i chi_L(a_i.lambda_(t+v_i).s).

The cyclotomic identity lambda_(t+v)=lambda_v+zeta3^v*lambda_t holds modulo3
indices because1+zeta3+zeta3^2=0. Therefore, put

    A=sum_i zeta3^v_i*a_i,
    offset=sum_i lambda_v_i*a_i.

The state is exactly chi_L(offset.s)*|psi_A^s>. The zero-residue support
ensures A in piR_L. Divide its public label by pi using the existing ideal
chart, b=A/pi inR_(L-1). The pairing identity

    chi_L(pi*b*s)=chi_(L-1)(b*(s mod pi^(L-1)))

gives a genuine lower-level native phase sample. Its unknown global phase is
retained by the numerical instrument. Since the complement is MEASURED, this
global phase has no observable effect on the output source. A coherent-pointer
transfer is NOT claimed; omitting measurements would require preserving
relative phases across histories.

No ideal child is constructed from the true secret. merge_branch computes
the actual conditional vector from the supplied parent vectors. For large
blocks it rescales intermediate products, rather than mistaking floating
underflow for a zero-probability event. The ideal branch probability is also
retained as the exact compact power3^(1-B).

## Why The Child Source Is Uniform

Condition on the COARSE support-selection transcript and observed offsets.
Each original label is uniform in its fixed residue coset of piR_L^n.
Multiplication by zeta3^v is an automorphism preserving that residue. A
nonempty sum of independent uniform ideal-coset lifts is uniform in their
sum coset. Since the residues sum to zero, A is uniform in piR_L^n, and
division by pi makes b uniform inR_(L-1)^n.

Disjoint supports preserve independence of the unobserved higher lifts.
Offset probabilities are uniform and do not bias those lifts. This argument
survives streaming reuse of UNUSED registers, including coarse-label
correlations, provided selection never reads higher digits or quantum
outcomes to choose a desired child. The joint returned labelled densities are
IID for the native lower secret under this legal coarse filtration. Do not
condition this statement on arbitrary inspections of unused higher labels.

Small exact censuses cover every higher lift for residues(1,2) at L2 andL3
and all three complement outcomes. These controls illustrate the general
ideal-coset proof; they are not a finite experiment promoted to a theorem.
The construction reuses ternary_cyclic_extractor.py's cycle gates and
zero-sum mathematics. It extends its executable source contract to mixed-
characteristic levels, full ring secrets and recursive original-copy tracking;
novelty is NOT asserted.

## Actual Recursive Receiver

At L1 the native state is a ternary Fourier character. Measure it and solve
the public F3 linear equations. At L>1:

1. Construct a lower labelled-phase stream by the measured level drop.
2. Recover s mod pi^(L-1) by the SAME receiver on that stream.
3. Take fresh supplied samples at the current level, not measured ancestors
   or convenient leftover labels filtered for rank.
4. Correct phases using the learned canonical lower representative. The
   residual lies in pi^(L-1)R_L, has order3, and Fourier measurement yields
   a public central-character row times the unknown last digit.
5. Solve only a full-rank system, then reconstruct the native ring value with
   its actual carries. Rank deficiency or finite-source exhaustion returns
   NO RECOVERY, not guessed digits or extra unbudgeted samples.

Each original input has a unique physical lineage. Merges account for all
consumed ancestors; final digit measurements have disjoint lineages; all
leftovers remain accounted. There is no cloning or secret assignment.
Unlike the retracted nil3 simulation, lower values here come from measured
original inputs. This still does not supply a general StateHSP decoder for
an arbitrary unknown density/representation interface.

## Conservative Scaling Contract

With K=n+h fresh digit samples per level, the stipulated recursion has

    C_1=K, C_L<=W*C_(L-1)+K,
    C_L<=K*(1+W+...+W^(L-1)).

This is an UPPER bound for this procedure, never a universal copy lower bound.
Each merge compresses to one qutrit, so the live unknown-register buffer is
at most(L-1)*W+L, rather than materializing full tensor histories. Metadata
and public ring arithmetic are separately charged and may use more memory.
All fixed L are polynomial in n; growing L makes this chosen upper ledger
large. No polynomial growing-depth algorithm or hardness theorem is supplied.

For independent uniform public central-character rows, the projective-line
union bound gives rank failure at most(3^n-1)/(2*3^K) per digit stage.
Union over L stages gives the reported ideal failure budget. This assumes
fresh IID inputs and the source-preserving coarse policy; arbitrary data or
noise cannot inherit it. Ancestor overdraw is capped, and leftovers are
charged as supplied originals. The actual execution records its copy count,
SUM gates, measurements, source indices, equations and learned prefixes.

## What Is And Is Not A Result

The report includes source-driven recoveries at levels2-4 with arbitrary
ring secrets, including vector dimension4 at level3, and scaling ledgers
without expanding their huge domains. Independent original labels and
provided qutrits drive the receiver; no probability law is evaluated from
the hidden secret inside it.

It remains a review-pending ideal-source algorithm specification and bounded
reference execution. Its source is a restricted quantum-data interface,
not free coherent access to a classical LWE evaluator. No classical hardness,
dequantization separation, physical quantum execution, cryptographic
reduction or new algorithmic speedup is claimed.

NEXT: attack this real baseline's growing-depth copy cost and source/noise
composition. Test larger admissible merge families without replacing the
full ring secret by an integer embedding or assuming free source regeneration.
Compare any improvement with original-data classical attacks and legitimate
single-copy measurement baselines. Do not resurrect the former secret-reading
nil3 implementation or interpret this recursion's cost as a no-go theorem.
