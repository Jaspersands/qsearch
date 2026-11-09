# Two-cluster Gaudin gap: accepted-source and BCS scope

Status: CLOSED source/normalization review. The proposed native finite-site counterfamily's fusion, perturbation and min–max estimates are separate parent/core proofs; this source review does not certify them from numerical controls. No controls, Git, network or API calls were used. Actual primary snapshots are `research/audits/sources/gaudin_gap_geometry/lutz_v3.txt`/PDF and `two_level_bcs.txt`/PDF with their manifests. The first is the accepted v3 text, not the previously read v2.

## What Lutz v3 does and does not claim

Equation(12), `lutz_v3.txt`280–298, is the quadratic charge-eigenvalue system. The target parent Hamiltonian at350–359 has spectrum ||q_v−q_w||_2². Therefore the relevant quantity discussed here is SQUARED joint-charge distance, not its square root or the gap of an arbitrary linear combination of charges.

The accepted main text is explicit about its qualifications. Lines365–391 prove/discuss the different-magnetization bound Eq(13), cite a sufficiently weak-coupling regime and the fixed-N strong-coupling limit, and then state that no rigorous scaling bound was obtained within the same magnetization sector away from those regimes. Lines315–326 describe the tested numerical families (central spin, equally spaced sites and uniform random sites) as evidence for1/N behavior and an overall lower bound along g; Figure1's caption334–344 describes minimization over tested eigenstates and g in[0,10]. This is not a theorem with an absolute constant uniform over every N-dependent rational site family. The source nevertheless proposes the1/N behavior in that broader physical discussion. An explicit same-sector native o(1/N) family would refute its unrestricted uniform extension; it should not be described as contradicting a proved all-site theorem or disproving the behavior of the three numerical families.

The accepted version also retains the classical-input condition:328–349 explicitly lacks a polynomial root-tracking guarantee, discusses step size and conditioning, and takes efficient target-charge computation as an assumption. This is independent of the joint-gap issue. The parent's previously closed label-free randomized channel avoids that input assumption but still needs a quantitative gap/resource promise.

AppendixE1053–1065 explicitly calls a full lower-bound proof elusive. Its sufficient weak-coupling condition in the main text378–384 is of order min_(i!=j)|eps_i−eps_j|/N². For the proposed final delta=n^-8 sites, this scale is of order n^-10, whereas g_n=1/(2n). Thus g_n tending to0 with n does NOT put the family inside that proved perturbative regime. AppendixF1103–1132 concerns g tending to infinity for each fixed finite site instance and uses different-magnetization Gaudin-magnet degeneracies/Dicke states to obtain the global minimum1/N. The proposed g_n, shrinking site separations and growing N are a different limit. No source weak/strong limit is falsified by that construction.

The source's magnetization is the sum of sigma_z operators, while the parent's M=n denotes the excitation count among2n spins. The latter is total Sz=0. Equation(13)'s cross-sector bound has zero right-hand side for the pair considered in the proposed construction and cannot constrain it. A smaller same-sector separation would also bound the global minimum from above, but does not imply a superpolynomial gap or an obstruction to polynomial preparation.

## Exact two-level BCS identification

Dusuel–Vidal, cond-mat/0501282v2, *Finite-size scaling exponents of the two-level BCS model*, `two_level_bcs.txt`35–65, Eq(3), gives

    H_BCS = −h(S1z−S2z) − (Sx²+Sy²)/N,
    S = S1+S2.

The microscopic pairing strength has been set to unity; the paper restricts to paired occupations, half filling Sz=0, and the maximal collective-spin sector S1=S2=N/4 (48–58). Its thermodynamic critical point is h=1 (62–65). With the parent's N=2n, each cluster has spin S0=n/2=N/4. Exchange the level labels so S1=S_B and S2=S_A. On total Sz=0,

    Sx²+Sy² = S_A²+S_B²+2 S_A dot S_B
             = 2 S0(S0+1) I + 2 S_A dot S_B.

Consequently, at h=1,

    H_BCS = 2 S_Az − (1/n) S_A dot S_B − S0(S0+1)/n I
          = 2 H − (n+2)/4 I,
    H = S_Az − (1/(2n)) S_A dot S_B.

This is an exact finite-dimensional operator identity on the specified spin/half-filling sector; no asymptotic approximation is involved in the normalization. Thus Delta_BCS=2(h1−h0). The parent's fused squared charge separation2(h1−h0)²/n equals Delta_BCS²/N. The additive constant is also consistent with the BCS critical ground-energy subtraction shown in Fig1: its energy per spin tends to−1/2 with the displayed−1/N correction.

## Known exponent versus the parent's independent bound

The BCS source's TableI,78–95, assigns the critical energy GAP exponent1/3. Its1/N expansion and scaling ansatz,146–176, and Fig1/204–207 give Delta_BCS proportional to N^-1/3 in the critical finite-size analysis. The argument combines continuous unitary transformations, cancellation of singular expansions and finite-size scaling; the text explicitly checks the prediction by diagonalization up to N=2^17 (244–249). This is prior physical knowledge of the critical mechanism. It is not an explicit all-n theorem with certified constants that can replace the parent's elementary variational estimate.

Under the exact mapping, that known exponent predicts fused SQUARED joint separation of order N^-5/3. The parent's proved-if-accepted O(n^-1/3) bound on h1−h0 is only an upper bound, not a matching Theta statement. Its path-Laplacian/tent min–max proof supplies its own constants and all-family quantifiers. The BCS source has coincident two-level energies and collective spins; it does not supply the parent's final delta=n^-8, distinct rational native Gaudin sites, commuting spectral projector, finite-delta compression, anchor-label comparison or exact finite-n certificate. Those are indispensable separate steps. Conversely, identifying this with the known BCS critical point prevents any novelty claim based merely on observing the1/3 exponent or two-cluster criticality.

Disposition: if the independent core accepts the native fusion and all-family variational estimates, the scientifically correct result is an explicit same-excitation finite-distinct-site family refuting a UNIFORM Omega(1/N) squared-joint-gap claim over all native rational site families. It leaves a potentially weaker inverse-polynomial all-path gap, fixed equally spaced/random-family behavior, general efficient preparation, classical hardness and quantum advantage OPEN. No result is promoted from the n64 Sturm control or the BCS numerical scaling plot.
