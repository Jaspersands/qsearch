# Independent Adversarial Review: Unknown-Rank Orthogonal Recovery

2026-10-27. Mathematical review of [RESULT.md](/Users/jaspersands/Developer/qsearch-research-work/orthogonal-general-rank-2026-10-27/RESULT.md), including the containment certificate, extension-field sampling, unknown-rank controller, success probability, resource schedule and reflection comparator.

## Verdict

**No mathematical counterexample or required proof correction found under the stated contract.** The certificate proves containment, the dimension rules turn containment into equality, and the stronger soundness statement for ideal undersampling is valid. Coefficient-1 elementary matrices suffice over extension fields. No SO(M) generators or maximal-parabolic classification are needed.

I reconstructed these arguments rather than treating the parent's controls as premises. The proofs below justify acceptance of this narrow construction. This is not a code audit, quantum implementation, novelty determination or natural-input advantage claim.

Essential hypotheses, already present in the proposed contract:
- U is a NONZERO, totally singular **F_q-linear** subspace, with 3<=k<=n for the recovery algorithm.
- The certificate tests all ordered elementary pairs i!=j, or a separately justified generating list giving the same invariance. Upper-triangular transvections alone would not suffice.
- The oracle hides the FULL setwise stabilizer in the stated O or SO domain; all actual test matrices lie in SO.
- The controller checks singularity of R itself and its dimension r=d+1. Singularity of the three neighbors is not a substitute for checking their intersection sum.
- The one-sided undersampling claim concerns exact Fourier outcomes and exact subsequent arithmetic, not arbitrary erroneous learner outputs.

## 1. Coefficient-1 Levi Tests Over F_q

Let T be an F_q-linear subspace of F_q^r invariant under every I+E_ij, i!=j. If v in T has v_j!=0, then

    (I+E_ij)v-v = v_j e_i in T, for every i!=j.

F_q-linearity, not availability of further group elements, gives e_i in T. Applying E_ji to one such e_i also gives e_j in T. Hence T=F_q^r. The only invariant F_q-subspaces are zero and the whole space. The same argument applies to the dual matrices I-E_ji.

There is no need to claim these matrices generate SL_r(F_q): they generally generate only SL_r(F_p), and that does not invalidate the argument. Nor is a semisimplicity assertion in defining characteristic being used.

The F_q-linearity qualification is essential. For q=p^2, the additive subset F_p^r inside F_q^r is invariant under these matrices but is not an F_q-subspace. Taking that subset inside R would defeat an overbroad certificate for merely prime-field-linear hidden sets. It is not a counterexample to the stated theorem.

## 2. Complete Containment Proof

Write V=R direct-sum M direct-sum R*, with coordinates (x,m,y),

    Q(x,m,y)=x.y+Q_M(m),  dim(R)=r,

and nondegenerate B_M. Let A=U intersect R and let Y be the projection of U to R*. Passing the Levi tests makes A and Y invariant natural/dual modules. By Section 1, A is zero or R, and Y is zero or R*.

Suppose Y=R*. For a in A, isotropy gives a.y=0 for every y in Y; hence A=0. Choose y with D y!=0 for the tested nonzero alternating matrix D. There is u=(x,m,y) in U. The central test gives

    c_D u-u = (D y,0,0) in U intersect R=A,

a contradiction. Therefore Y=0 and U is contained in R direct-sum M.

If A=0, for each u=(x,m,0) in U every elementary difference (E_ij x,0,0) lies in A and is zero. Consequently x=0 and U is contained in M. For every tested basis vector w of M,

    E_e1(w)u-u = -B_M(u,w)e1 in A=0.

Nondegeneracy of B_M now gives u=0. This contradicts U!=0, including when M=0, where U contained in M is already impossible. Thus A=R, proving R contained in U.

Conversely, if R is contained in U, isotropy gives U contained in R-perp=R direct-sum M. The Levi tests change any vector only within R; the central test fixes it; each cross test changes it by a multiple of e1. Each therefore preserves U. This proves the exact equivalence

    all certificate tests pass  iff  R is contained in U.

All tests preserve Q and have determinant one: Levi determinants cancel, the alternating D gives y.Dy=0, and E_e1(w) is the stated orthogonal unipotent. An arbitrary public Witt-frame change is harmless because conjugation preserves SO, even if the frame has determinant -1.

In particular, no action of SO(M) was used. A nonzero M-component is detected by its pairings with a basis of M, rather than by irreducibility of an orthogonal action on M.

## 3. All Probe Kernels And The Useful Dimension Inequality

Put N_W=2n-2. I independently obtain the three claimed kernels:

| Probe | Exact kernel | Dimension |
| --- | --- | --- |
| e in U | W | N_W |
| e in U-perp minus U | (pi U)-perp in W | N_W-k |
| e outside U-perp | pi(U intersect e-perp) | k-1 |

For the middle case, E_e(w)u-u=-B(u,w)e. Since e is not in U, stabilizing U is equivalent to all these differences vanishing. Projection is injective on U and the pairing on W is nondegenerate.

For the good case, choose u0 in U with B(e,u0)=1. Necessity follows because E_e(w)u0-u0 belongs to U intersect e-perp and projects to w. Conversely, if h=w+a e belongs to that intersection, singularity gives Q(w)=0 and B(u0,w)=-a. The transformation fixes U intersect e-perp and maps u0 to u0+h. These vectors span U, giving sufficiency. The kernel is therefore F_q-linear, not just additive.

The middle case can occur only for k<=n-1: pi U is a k-dimensional singular subspace of W, whose Witt index is n-1. It follows that

    dim(K_e) >= k-1 for EVERY probe;
    dim(K_e) >= k for EVERY nongood probe.

For the middle case, the second inequality is N_W-k>=k when k<=n-1. For e in U it follows from N_W>=k. This is the short invariant that makes the unknown-rank argument work.

## 4. Extension Fields And Ideal Undersampling

The additive characters are chi_y(w)=exp(2*pi*i*Tr(y.w)/p), with trace-dual coordinates interpreted using the supplied field presentation. If K is F_q-linear, its trace-annihilator equals its F_q dot-product annihilator: Tr(y.k)=0 for every k in K also holds with k replaced by a k for every a in F_q. Nondegeneracy of the trace pairing forces y.k=0 in F_q.

Thus every exact Fourier outcome lies in K-perp as an F_q-linear space. If Y_sample is the F_q-span of any number of these outcomes, the estimated kernel is

    K_hat = Y_sample-perp,  so K_hat contains K.

This remains true with no samples, repeated samples, or insufficient sampled rank. Taking only prime-field spans without the specified conversion would not justify the same F_q rank calculation; RESULT.md correctly requires F_q-linear recovery.

Suppose the controller returns a singular R after three estimates of common dimension d, with r=d+1. The preceding inequality gives r>=k. The containment certificate gives R contained in U and therefore r<=k. Hence

    r=k,  d=k-1,  R=U.

Moreover, each accepted probe must have been good, because any nongood probe has true kernel dimension at least k and its estimate cannot be smaller. Each accepted estimate must equal its true good kernel, since it contains that kernel and has the same dimension.

This proves **one-sided correctness of every return under ideal Fourier sampling**, without assuming full sampled rank in advance. Rank deficiency can only cause additional rejection or failure to return. Independence of the three restricted functionals is needed for the success guarantee, not for sound acceptance.

The troublesome k=n-1 bad probe has true dimension n-1, so any such dimension-gated candidate has r>=n>k and cannot pass containment. No testing of maximal extensions and no claim that P_R is maximal is necessary. The proof is identical for O and SO inputs.

Arbitrary malformed estimates can violate K_hat containing K. For example, a fabricated smaller-rank candidate inside U passes the containment certificate. Consequently the stated global approximation/error qualification must remain; the certificate is not an unconditional equality verifier for noisy arbitrary outputs.

## 5. Three-Probe Success And The 52/125 Bound

For good e_i define lambda_i=B(e_i,.) restricted to U. Independence of these functionals implies independence of e_i modulo U, since B(U,U)=0. Equating two expressions u_i+a_i e_i=u_j+a_j e_j forces a_i=a_j=0. Therefore the pairwise neighbor intersections are exactly the simultaneous kernels inside U. In a basis dual to three independent lambda_i, their pairwise kernels span every basis vector of U, including their common kernel. This proves reconstruction for all k>=3.

In adapted coordinates U=<e1,...,ek>, fix nonzero (y1,...,yk)=lambda. There are q^(n-k) choices of the remaining y coordinates and q^(n-1) solutions of x.y=0. Thus each nonzero lambda has exactly q^(2n-k-1) singular lifts, proving both the stated a_k and conditional uniformity. With fresh independent probes, the claimed success probability follows.

The proposed constants are valid:

    a_k = (1-q^(-k))/[(1-q^(-n))(1+q^(-(n-1)))] >= 13/15,
    (q^k-q)/(q^k-1) >= 12/13,
    (q^k-q^2)/(q^k-1) >= 9/13,
    (13/15)^3*(12/13)*(9/13) = 52/125 > 1/3.

The last two factors are minimized at q=3,k=3: the first follows from 1-1/(1+q+...+q^(k-1)); for the second, reduce to k=3 and use q^2/(q^2+q+1)>=9/13. No large-field or fixed-rank asymptotic assumption enters.

## 6. Resource And Failure Accounting

The certificate uses T(r)=r(r-1)+1+2(n-r) queries. For 3<=r<=n,

    [n(n-1)+1]-T(r)=(n-r)(n+r-3)>=0.

Hence the advertised query cap, caching f(I) once, is correct. A supplied singular R has a Witt decomposition obtainable by finite-field linear algebra and division by 2; the residual form does not need a further hyperbolic decomposition.

For an annihilator of F_q-dimension a<=N_W, m=N_W+s independent uniform samples fail to span it with probability at most

    [(q^a-1)/(q-1)] q^(-m) <= 1/[(q-1)q^s].

The union bound over at most 3B learners is valid. This failure budget ensures returning an answer, rather than being needed to prevent wrong ideal returns. With (2/3)^B<=epsilon/4, the geometric failure budget is valid because the actual one-trial success probability is at least 52/125.

The four stated budgets are compatible: geometry epsilon/4, sampled-rank failure epsilon/4, complete Fourier-instrument error totaling epsilon/4, and capped classical sampling error epsilon/4. The hybrid must include records and aborts as stated, without conditioning on a rare branch. Polynomial arithmetic and the standard approximate additive Fourier primitive give the claimed polynomial-time schedule, not a claim about the dense reference simulator.

## 7. Corrected Reflection Comparator

For Q(v)!=0 the reflection is r_v(z)=z-B(z,v)v/Q(v). If it stabilizes U and some u in U has B(u,v)!=0, then r_v(u)-u is a nonzero multiple of v in U, contradicting singularity of U. Thus r_v belongs to P_U exactly when v belongs to U-perp.

For k<n, U-perp has radical U and split nondegenerate quotient of dimension 2a with a=n-k. Multiplying its nonsingular-vector count by q^k and dividing by the ambient nonsingular count gives exactly

    Pr[r_v in P_U | Q(v)!=0] = (q^(n-k)-1)/(q^n-1).

This is at least (2/3)q^(-k). Conditional accepted vectors are uniform among nonsingular vectors in U-perp. For any proper subspace, choose a containing hyperplane. If its defining functional is nonzero on the radical, the zero probability is 1/q. Otherwise it descends to the quotient; for a>=2 the hyperplane-size bound gives at most 9/16, and for a=1 at most 1/(q-1)<=1/2. The claimed probability at least 1/3 of enlarging the current span is therefore conservative. O(n q^k) expected queries follows.

For k=n the accepted set is empty. Every nonsingular reflection has determinant -1, so the single-reflection test is unavailable to an SO-only oracle. RESULT.md states these limitations correctly. This is only an O-oracle classical upper bound; it neither transfers the maximal-only lower bound nor establishes optimality or an SO lower bound.

## 8. Independent Exact Controls And Review Boundary

I ran standalone standard-library arithmetic controls, without importing parent code or modifying its files:
- F_9=F_3[i]/(i^2+1), r=3: exhausted all 91 projective lines and all 91 planes. None is invariant under all coefficient-1 elementary tests. The F_3^3 additive subset is invariant but not F_9-linear, confirming the necessary distinction.
- Actual E_e(w) stabilization enumeration over F_3, with U the first k coordinate singular axes: (n,k)=(4,3) gives kernel sizes 9,27,729 in the good, bad, and e-in-U branches. The bad branches (5,3) and (5,4) give 243 and 81 respectively, matching all formulas.
- Checked the three proposed probability-factor bounds in 275 exact rational cases, q in {3,5,7,9,27}, 3<=k<=n<=12. The smallest tested full success probability is 19683/42250 at q=n=k=3. These checks are supplementary, not the proof of the uniform bound.
- Exhausted nonsingular vectors in F_3^8: the reflection acceptance counts are 108/4320=1/40 for k=3 and 0/4320 for k=4.

These scratch computations are not a retained regression suite, a code audit, a simulated quantum receiver, or evidence for novelty. The universal conclusions above rest on the reconstructed proofs.

I reread the parent's updated historical-comparator attribution before closing; the earlier withdrawals are not claimed as a new result in this review.
Reviewed source SHA-256 after that reread: `dac3c1c3e8e5c30d265b34cb9f47d5ba5b373b3bd66503077fc1157c7e440046`.
Only this new REVIEW.md was written. No parent artifact, Git, UI or dependency state was changed; no external contact or literature search was performed.
