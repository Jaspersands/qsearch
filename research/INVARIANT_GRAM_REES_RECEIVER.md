# Invariant-Gram Rees Receiver

30 October 2026. Constructive ideal channel argument, implemented classical
controller, and exact arithmetic controls. No compiled quantum receiver,
new asymptotic HSP regime, novelty clearance, or speedup claim.

## Question And Answer

The [four-copy obstruction](COHERENT_GRADE_SELECTOR.md) showed that a
simultaneous cancellation witness at every character label does NOT imply
a complete coherence-preserving selector. Can a larger bank avoid that
normalization failure without reading individual noncentral characters?

For the class-three filiform family below, YES: construct an invariant
three-dimensional scale frame from central records, measure its six Gram
entries, and solve one ternary quadratic. The ideal instrument has no
label-dependent failure sector. Its bounded classical implementation has
explicit arithmetic ABORT probability at most 2^-b under fresh fair bits.
Every successful complete record produces the same exact quotient source.

The sufficient bank size is 14 if p=2 mod 3, otherwise 16. A stronger
verified sequential sufficient bound is 12/18: this construction is WORSE
in the first regime and uses two fewer copies in the second. Neither bound
is known optimal here. There is NO uniform source improvement or new
general-rank regime. The earlier 18/36 comparison was too weak and has
been withdrawn after checking the published quadratic solver directly.

## Actual Source And Access

Let p>3 be prime and L have basis X,Y1,Y2,Y3 with [X,Y1]=Y2,
[X,Y2]=Y3. Its genuine positive Rees cover A has dimension seven:

    A1 = tL, A2 = span(t^2 Y2,t^2 Y3), A3 = span(t^3 Y3).
    G = exp(A), N = exp(A2 + A3), Z = exp(span(t^2 Y3,t^3 Y3)).

N is abelian normal; Z is central. The ordinary hiding-function tuple
at three distinct nonzero evaluation points supplies mixed K-coset sources,
where K=exp(direct_sum t^j(h intersect gamma_j(L))). This is the actual
homogeneous lift of an arbitrary hidden Lie subalgebra h, not an invented
label oracle. No normality or transversality of K is assumed or required.
Each fresh lifted source costs three original coherent oracle queries and
paid reversible evaluation, with all evaluation workspace cleaned.

Use R_g|x>=|x g^-1>. Public N-character labels are (alpha,beta,ell),
on (t^2 Y2,t^2 Y3,t^3 Y3), respectively. Measure beta and ell, but keep
alpha and every multiplicity/group register COHERENT. The independent
sources need not have uniform character labels. Conjugation changes alpha
by +/-x(g)*ell and fixes beta,ell; x(g) is the tX coefficient.
For V_s(g)=tensor_i R_(Delta_si(g)), the change is

    alpha_i -> alpha_i +/- x(g)*ell_i*s_i.

A zero s_i means the identity action on that consumed slot, not inversion
of a zero dilation. At least one scale must be nonzero.

## Public Frame Construction

Put g3=gcd(3,p-1), M=13+g3. On the measured central bank define

    T(u,v,w) = sum_i ell_i*u_i*v_i*w_i,
    B(u,v) = sum_i beta_i*u_i*v_i.

1. Each zero ell_i supplies its coordinate vector. Classify nonzero ell_i
   by cubic residue class and pair within each class. A pair (i,j)
   supplies a vector with entries 1 and c, where ell_i+ell_j*c^3=0.
   There are at most g3 unpaired nonzero entries. With z zero entries and
   o odd-sized classes, the number of disjoint directions is
   z+(M-z-o)/2=(M+z-o)/2 >= (M-g3)/2 >= 7.
2. Retain seven directions and their span V. Disjoint supports and the
   cubic equations imply T vanishes on ALL of V x V x V, not only
   T(v,v,v) at the seven generators.
3. Find a three-dimensional totally singular subspace W of B restricted
   to V. Over F_p every quadratic in at least three variables has a
   nonzero isotropic vector. After selecting v, restrict to a complement
   of v inside v-perp. A radical v removes one dimension; otherwise two.
   The three selections therefore have dimensions at least 7,5,3.
   Preserve radicals; do not discard zero diagonal coefficients.

For a basis w1,w2,w3 of W, compute coherently and measure ONLY

    Q_jk = sum_i alpha_i*w_j,i*w_k,i,  1 <= j <= k <= 3.

These are six commuting linear functions of the N-character labels.
Uncompute the arithmetic workspace. For each symmetric Q choose any
nonzero t with t^T Q t=0, and set s=sum_j t_j w_j. The frame has rank
three, so s is nonzero. On this entire measured Gram fiber,

    sum_i ell_i*s_i^3 = 0,
    sum_i beta_i*s_i^2 = 0,
    sum_i alpha_i*s_i^2 = t^T Q t = 0.

The Gram fiber is invariant under V_s(G): its (j,k) change is
+/-x(g)*T(w_j,w_k,s)=0. Thus its projector A_Q commutes with V_s(g)
for EVERY g, not just an unknown generator of K. Classical randomness
choosing the frame or isotropic vector is part of the complete record.
For each fixed such record the same commutation statement holds.

## Full Quotient Channel, Including Hidden Intersections

This argument does not replace a conditioned source by an ordinary KZ
coset state. That would erase its potentially nontrivial central twist.
Let C=K intersect Z. For a central character mu,

    Pr(mu) = |C|/|Z| if mu|C=1, and zero otherwise;
    tau_mu = (1/(|G|*|C|)) sum_(k in K,z in Z) conjugate(mu(z))*R_(kz).

Only positive-probability outcomes are normalized. In particular tau_mu
belongs to C[KZ], is positive, and R_k*tau_mu=tau_mu for every k in K.
The public compiler never needs C or its order; they enter the proof only.

Condition on the complete central record and independent classical frame
randomness. Let rho be the tensor product of the normalized tau_mu.
For a Gram outcome and subsequent successful isotropic choice s, write
B=A rho A^dagger and b0=Tr(B). A is its Gram-fiber projector, with a
scalar square-root probability if additional random records are included.
The three facts needed for every g in G are:

1. A acts as a scalar on each FULL joint N-character block, hence
   A belongs to C[N^M]. Since rho belongs to C[(KZ)^M], B belongs to
   C[(KN)^M]. If g is outside KN, any active Delta_si(g) is outside KN,
   since dilations preserve K and N. Orthogonality of regular group
   matrices therefore gives Tr(B V_s(g))=0.
2. For k in K, homogeneity gives V_s(k)rho=rho. Gram invariance gives
   [A,V_s(k)]=0, so V_s(k)B=B. This is LEFT invariance, stronger than
   merely V_s(k)B V_s(k)^dagger=B.
3. The three moment equations make V_s(n) the identity on the entire
   supported character fiber for every n in N. Thus V_s(n)B=B.

Together, since V_s is a representation (identity on zero slots),

    Tr(B V_s(g)) = b0 * 1[g in KN].

Prepare a uniform register on G/N, use ANY public representative section
sigma, apply literal controlled V_s(sigma(q)), and trace ALL targets.
The (q,r) entry is b0/|G/N| times the indicator that
sigma(r)^-1 sigma(q) belongs to KN. This is exactly b0 times the mixed
KN/N-coset state. The section need not be a homomorphism. Successful
normalized output is independent of every measurement/randomness record.
Summing successful records preserves that state, with the separately
recorded abort mass. Impossible Gram fibers are zero operators, not failures
requiring normalization. G/N=tL additively; the lifted subgroup image is th.

IMPORTANT: all Fourier and arithmetic work registers must be restored or
cleaned before literal right actions. A residual alpha register, leaked
multiplicity information, or approximate transform cannot be ignored.
The proof uses ideal transformations; it is not a compiled circuit test.

## Why Weight Invariance Alone Is Insufficient

Take ell=(1,-1), beta=0 and s=(1,1) over F5. On the moment hyperplane
alpha1+alpha2=0, the scalar amplitude a(alpha)=omega^alpha1 has constant
absolute value. Under alpha -> alpha+a*s*ell it picks up omega^a.
Consequently the hidden K correlation picks up a nontrivial phase despite
invariant weights and valid moments. The operator proof needs invariant
AMPLITUDES. Positive Gram-fiber projectors have this property automatically.

## Implemented Arithmetic And Failure Budget

`theorems/invariant_gram_selector.py` accepts central ell,beta and then ONE
3x3 Gram matrix. It has no API that accepts individual noncentral alpha
labels. Its six measurement rows describe the required quantum measurement;
the implementation does not perform it. Tests/report calculate Gram
outcomes from classical alpha fixtures explicitly labelled as references.

Cube roots use the existing bounded Cantor--Zassenhaus backend when
needed, or an inverse power when cubing is bijective. Symmetric congruence
diagonalization is exact. A nondegenerate ternary conic is solved by
sampling x and testing y^2=(-c-a*x^2)/b. At least (p-1)/2 of the p choices
work, so per-trial failure is at most 3/5 for p>=5. A radical is used
directly without random trials. Found roots and final witnesses are verified.

For requested b>=1 set Kcap=3(b+6). There are at most seven cubic root
calls, four square-root calls, and four conic searches. Root splitting
uses at most 5Kcap field draws per cubic and 2Kcap per square root;
conic sampling uses at most Kcap each. Thus at most 47Kcap field draws
are needed, below the allocated 50Kcap. The algebraic union abort bound is
22*(2/3)^Kcap. Set the per-integer bit-rejection cap to
b+2+ceil(log2(50Kcap)); integer abort contributes at most
50Kcap*2^-cap. Their sum is less than 2^-b for all b>=1.

This assumes fresh independent fair bits, not a test seed. ABORT is
explicit, never silently retried or counted as a valid witness. After
selection starts the controller is one-shot even on stochastic abort.
Malformed inputs/backend errors propagate as errors, not successful branches.
Primality validation and deterministic library runtime are separate from
the capped randomness guarantee. Fixed-size field arithmetic is polynomial
in log p; there is no p-sized label table or enumeration in the controller.

The ideal N transform and inverse use 6M single-field Fourier transforms.
Quotient-register preparation and terminal Fourier readout are ADDITIONAL
costs. An implementation must budget all their approximation errors and
all source errors, including conditioning; the current module does NOT
provide that circuit or a full physical error budget. In an unconditional
instrument comparison, transform errors accumulate by channel composition;
one must not claim the same conditional bound on arbitrarily rare records.

## Matched Comparison, Prior Art, And Falsifiers

The stronger comparator uses six inputs for two diagonal quadratic
equations, from [Ivanyos--Sanselme--Santha, Section 5, Claim 1, manuscript
page 13](https://www.irif.fr/~santha/Papers/iss12.pdf#page=13). Its general
arity is (r+1)(r+2)/2. This is the QUADRATIC-only claim, not the larger
quadratic-plus-linear schedule. The algorithm permits arbitrary coefficients;
zero columns and deficient rank give simpler cases. Random nonresidue
selection and polynomial-time scalar solving are paid classical ingredients.

A scalar cubic requires only two inputs when cubing is bijective. Otherwise
three suffice: a zero coefficient gives a singleton, repeated cube classes
give a pair, and three distinct classes use the existing ternary cubic curve
solver. For coefficients (a,b,c), call `ternary_cubic_scales(p,(a,(-b)%p,c))`;
its result (1,y,z) gives the original witness (z,y,1). The helper's existing
Hasse--Weil argument gives sampling success at least 1/9 for eligible p>=7.

Six disjoint cubic blocks therefore give a sequential bank of 12/18.
Apply the quadratic witness to their output characters; the original cubic
moments remain zero. Original query counts are 36/54 per bank. This is a
known-ingredient sufficient construction, not a verified integrated quantum
implementation or an optimality claim. Rejection/root costs and quantum
precision must still be charged. The 14/16-source Gram mechanism survives
the correctness checks, but the previous uniform improvement claim does not.

Finite-field solving ingredients are known. Ivanyos--Santha give the
quadratic construction and input-relative power-class classification;
their Fact 2 states deterministic scalar solving via van de Woestijne.
Those ingredients should not be advertised as new. Input-relative cubic
classes and deterministic conic solving could remove arithmetic randomness,
but are not implemented here. See [the primary paper, Sections 2.1 and
3.1](https://arxiv.org/html/1503.09016v2). Novelty of this exact Gram-channel
composition remains unestablished; automated review is not peer review.

The principal failure of the hoped-for extrapolation is vector-valued
top characters. For uniform nonzero vectors in F_p^r, a second vector
has a cube-scalable proportional relation to a fixed one with probability
(p-1)/(g3*(p^r-1)). A polynomial bank can contain no such pairs. General
SDE disjoint-block constructions reproduce existing coverage; extending a
frame with overlapping supports introduces mixed, non-diagonal equations.
No efficient high-rank frame construction or better exponent follows.

Even for a scalar diagonal cubic with z zero coefficients, a totally
singular subspace has dimension at most z+floor((M-z)/2). Over an algebraic
closure, choose a vector nonzero on every coordinate used by that subspace.
The induced bilinear form T(u,-,-) is nondegenerate on those coordinates,
so a totally isotropic subspace has at most half their dimension. Project
off zero-coefficient coordinates to obtain the stated bound. Pairing misses
this scalar limit by at most one dimension; scalar overlap is not an
asymptotic escape route. This is a bound on THIS frame method, not all
collective measurements.

NEXT: either construct a genuinely better vector-valued invariant frame
with complete channel and polynomial-time construction, or pivot to a
motivated application with a surviving matched classical competitor test.
Do not spend another pass optimizing scalar constants or source calculators.

## Verification And Replay

    python qsearch.py power-sde --coherent-gram --write
    python -m pytest -q tests/test_invariant_gram_selector.py tests/test_invariant_gram_budget.py

The report writes `research/reductions/invariant_gram_selector.json` only;
it does not promote a candidate or proof-registry status. Source hashes
cover the listed files, not the complete transitive dependency closure.
Popper independently reviewed the full channel and matched comparator.
Nietzsche independently reviewed the public controller, degenerate forms,
large-prime arithmetic and worst-case randomness bound. These are automated
reviews; the complete channel is analytical, not formally verified or
simulated by the arithmetic tests.
