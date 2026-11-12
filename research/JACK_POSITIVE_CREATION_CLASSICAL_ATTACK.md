# Positive row creation: an exact mixed-row falsifier

13 November 2026. One exact Sage control, lambda=(2,1), alpha=3. The direct
replacement of signed creation histories by their positive weights does
NOT preserve the fixed-shape Jack Born law. This is a scoped falsifier,
not a hardness result or a rejection of every positive-formula algorithm.
General polynomial classical Born sampling remains OPEN.

The actual Ben Dali--Dolega source 2305.07966v1 was read at equations
(23)--(26), Corollary 5.3, and Theorem 8.2. Local source:
audits/sources/jack_transform/bendali_dolega_positive.txt. Formal positivity
is in NEGATIVE row variables. At native positive row length r, the signed
operator uses u=-3r; changing to u=+3r is an absolute-history operation,
not a positive evaluation of the original native Jack formula.

## 1. Source operators and the two candidate constructions

Set alpha=3 and b=2. In the source's catalytic variables,

    Y_+ = sum_(i>=0) y_(i+1) partial_(y_i),
    Gamma_Y = 3 sum_(i,j>=1) i y_(i+j) partial_(p_i)partial_(y_(j-1))
              + sum_(i,j>=1) y_i p_j partial_(y_(i+j-1))
              + 2 sum_(i>=1) i y_(i+1) partial_(y_i),
    Theta_Y = sum_(i>=1) p_i partial_(y_i),
    B_n(p,u) f = Theta_Y (Gamma_Y+u Y_+)^n (y_0 f/3),
    B_infty(t,p,u)=sum_(n>=1) t^n B_n(p,u)/n.

Theorem 8.2's FIRST equality defines row creation as

    R_r=(-1)^r [t^r] exp(B_infty(t,p,-3r)).

Starting at 1 and applying rows in increasing size gives J_lambda.
Because Gamma_Y, Y_+, and Theta_Y have nonnegative coefficients at b=2,
the corresponding absolute-history operator is

    A_r=[t^r] exp(B_infty(t,p,+3r)).

This takes the absolute value of each expanded history weight BEFORE
histories are collected by final power-sum monomial. It is not the
coefficientwise absolute value of R_r after cancellation.

The row-only warning is essential. Corollary 5.3, with q_k=1 for all k,
leaves only a one-row Jack in the Cauchy expansion and gives

    [t^D] exp(B_infty(t,p,u)) 1
       = J_(D)(p) prod_(j=0)^(D-1)(u+3j)/(3^D D!).

Consequently A_D 1=binom(2D-1,D) J_(D). Its normalized Born law is
identical to the target. The exponential scalar ratio alone is therefore
not a sampling falsifier.

## 2. The single exact mixed-row control

For degree two in the exponential set

    C_2(u)=(B_2(p,u)+B_1(p,u)^2)/2.

Direct catalytic differentiation, independently executed in Sage, gives

    B_1(p,u)1=(u/3)p_1,
    C_2(u)p_1 = [u(u+3)/18] p_1^3
                 + [1+u(u+5)/6] p_1 p_2 + (u+3)p_3.

Thus R_1 1=A_1 1=p_1, but the next row yields

    R_2 R_1 1 = p_1^3+2p_1p_2-3p_3 = J_(2,1),
    A_2 A_1 1 = 3p_1^3+12p_1p_2+9p_3.

The signed result was also compared exactly with Sage's INDEPENDENT
integral-Jack basis at alpha=3. Relative to coefficientwise |J_(2,1)|,
the positive coefficients have ratios (3,6,3), in the order (111,21,3).
In particular, removing the product of the vacuum row factors, which is
3 here, still leaves coefficients (1,4,3), not (1,2,3).

The Hall weights of these three power sums are (162,18,9). Hence

    ||J_(2,1)||^2=315,
    ||A_2 A_1 1||^2=4779,
    pi_J=(18,8,9)/35,
    pi_A=(18,32,9)/59,
    TV(pi_J,pi_A)=648/2065.

So even granting an exact sampler for the normalized positive polynomial's
BORN law, it samples the wrong distribution. Merely sampling one positive
creation history is weaker still: its boundary marginal is generally
linear in the positive coefficients, whereas the Born law needs their
squares and the Hall factors.

This ONE example is easy to correct: rejection from pi_A with acceptance
probabilities (1,1/4,1) has success 35/59 and returns pi_J exactly. Thus
the control supplies neither an exponential rejection lower bound nor a
general positive-sampling obstruction.

## 3. Exact implementation boundary and disposition

Artifact: audits/controls/jack_positive_creation/check_lambda21.py.
Receipt: audits/controls/jack_positive_creation/result.json.
Reproduce with:

    /opt/anaconda3/envs/qsearch-cas/bin/sage research/audits/controls/jack_positive_creation/check_lambda21.py

The script uses Sage rational polynomial differentiation and Sage's Jack
basis, not custom polynomial arithmetic. It retains only p_1,...,p_3 and
y_0,...,y_3. This is exact for this control: Gamma_Y and Y_+ increase the
weight deg(p_i)=deg(y_i)=i by one, and Theta_Y preserves it; no intermediate
has weight above three. There is no shape sweep or numerical extrapolation.
The source text hash is in the receipt. No network, API, or Git action
was taken. The Sage wrapper accepts the script directly, not the -python
option; the successful invocation above is the one to reuse.

Refuted: coefficientwise proportionality

    A_lambda 1 = constant(lambda) * |J_lambda|

for every native partition, and the resulting direct normalized-Born-law
replacement. The sign correction is shape-and-output dependent already
at lambda=(2,1).

Still open: a genuinely efficient paired-history contraction for the
signed squared coefficients/conditional derivative norms, or a complete
positive proposal plus a COMPUTABLE correction with polynomial acceptance
after permissible global rescaling. For the latter, if a_mu denotes the
absolute-history coefficient, the required relative correction is
(theta_mu/a_mu)^2; neither those ratios nor proposal sampling/normalization
are supplied by formal positivity alone. A global scalar cancellation
ratio must not be counted as unavoidable sampling cost, as the one-row
identity demonstrates. No additional control or nearby shape sweep is
recommended from this result.

## 4. First paid report: Lax moment closure

Completed Claude jack-lax-norm-closure report fully parent-read. Accepted:
for derivative multiset nu=(1^n1 2^n2...), normalized squared derivative
norm is E_pi[prod_k(3k)^nk (m_k)_nk]. At total removed degreeD this
recovers the individual Born probability times prod(3k)^nk nk!. Thus exact
all-word norms are stronger than merely approximate sampling. Hierarchy
moments of the CORNER measure are not these occupation factorial moments.

Formal diagonal-plus-commutator elimination is automatic by finite-dimensional
interpolation because the full hierarchy separates shapes, but its size and
evaluation cost are unpaid. Parent checked a narrow all-degree falsifier:
F(a)=||3 partial_p1 J_(a,1)||²/H_(a,1), a>=2, equals

  3(a-1)(3a-4)(3a+1)/[(3a-5)(3a-1)(3a-2)]
  +9a(3a-1)/[(3a+1)(3a-2)].

Derive from the two removable corners: top Pieri weight
(3a-4)/[(3a-5)(3a-1)] and bottom weight3a/(3a+1), and actual hook-norm
ratios. F(2)=186/35 and F(a)->4, so it is bounded and nonconstant. Each
FIXED T_l eigenvalue is polynomial in a by the box-product resolvent
expansion/Faulhaber. Therefore no FIXED polynomial P(T_1,...,T_L), with
L and coefficients independent of D, gives this single norm. This does
NOT exclude polynomial-size D-dependent/rational recursions and is not
a reason for another closure-barrier pass.

Also checked directly: p2 J1=(1/28)J3+(4/35)J21-(3/20)J111, so
Schur ribbon-only support does not transfer to alpha3. No general support
lower bound follows. Repairs: at alpha1 integral-Jack power coefficients
are hook(lambda)*chi_lambda(mu)/z_mu, not literally chi; all conversion
factors are explicit. The report's OPEN general hook-ratio computation
is already paid by the hook product (polynomial bits). No claim about
typical history depth or impossibility of all polynomial methods is adopted.
The report did not receive creation-source definitions and correctly left
the one-row absolute-creation identity unverified; parent verified it above.
No new all-degree sampler, hardness result, or STATE status move follows.

## 5. Creation-contraction report disposition

Completed OpenAI jack-creation-contraction report (410lines) fully parent-
read. No unrestricted polynomial contraction. Accepted structural identity,
derived directly by comparing Jack coefficients in actual sourceThm5.2:
for generic real u, T_u J_nu=J_nu(u)J_nu and

  B_m(u)=(1/3) T_u p_m T_u^-1,
  exp B_infty(t,u)=T_u G(t)T_u^-1,
  G(t)=exp(sum_k t^k p_k/(3k)).

Adjoint contraction contains T_u^-1 S(s) T_u² G(t) T_u^-1, with
S(s)=G(s)^*=exp(sum_k s^k partial_pk). The intermediate shape diagonal
T_u² prevents replacing this with the scalar Hall kernel(1-st)^(-1/3).
At native u=-3r, zero eigenvalues make an unrestricted inverse illegal;
only the original polynomial operators may be specialized. No diagonal
Jack oracle or matrix-element access is paid by this identity.

Parent also checked report's scalar/degree-only commutator falsifiers:
[R1*,R1]=3+2degree; on degree2 basis(p1²,p2), [R2*,R2] has matrix
[[160,16],[48,192]], with Jack eigenvalues208 and144. The degree211
example has a genuine probability9/16 history(1,1) on which absolute
replacement gives forbidden next-part2 with probability1/4. These agree
with exact polynomial/Gram calculations; no new CAS control is needed
after the stronger-than-needed lambda21 falsifier. Rank>=p(d) for a
universal LINEAR cross-contraction boundary follows from orthogonal Jack
Gram rank, but does not constrain arbitrary nonlinear matched-norm methods.

Accepted all-degree leading-coefficient calculation: if
G_lambda=A_lambda1...A_lambdal 1 and c_lambda=prod_i binom(2lambda_i-1,lambda_i),
then coefficients of p1^D are1,c_lambda, and of p2 p1^(D-2) are
3n(lambda')-n(lambda), c_lambda[3n(lambda')+n(lambda)]. Retaining only
defect0/1 in the catalytic formula gives per-row beta update
beta -> beta+3binom(r,2)+3rd/u, for input degree d. Thus rectangle
(r^(3r-2)) has zero target coefficient and positive absolute coefficient.
The all-ones derivative history can be exponentially rare, so this supplies
NO asymptotic TV/acceptance lower bound. It strengthens the same already
closed shortcut; no follow-up family or barrier is queued.

An explicit expansion has polynomial coefficient BIT lengths (D catalytic
steps, denominator dividing lcm(1,...,3D)^(3D), exp(O(DlogD)) weight/path
bounds) but exp(O(sqrtD)) coefficient count. This is a complete coarse
classical baseline, not a polynomial contraction. General nonlinear,
determinantal and uniformly controlled approximate sampling remain OPEN.
The separate paired-map request truncated with zero response bytes; it
establishes nothing and is not retried.

## 6. BGL prefix-amplitude report disposition

Completed OpenAI jack-prefix-amplitude-sampler report(483lines) fully
parent-read/checked. Accepted ideal block-boundary identity: remaining
removal-content history h determines a unique subshape nu, with amplitude
sqrt(Q(h))*a_nu(mu) for occupation mu. All path/hook factors have polynomial
bits; the unresolved factor is the actual Jack coefficient a_nu(mu).
Within one fixed-history ideal block, O(D²) abstract corner coordinates
suffice, but conversion to occupation coordinates contains the same Jack
problem already at marker0. No coefficient oracle is supplied.

Parent checked the exact termwise-closure falsifier in degree2. In basis
a=|11,0>, b=|2,0>, c=|1,1>, d=|empty,2>, L edges are
a-c sqrt6, c-d sqrt3, b-d sqrt6, with diagonal(0,0,2,4).
u=(a+sqrt3*b)/2 and Lu=(sqrt6*c+3sqrt2*d)/2 span the Jack(2)
cyclic space, with L²u=5Lu+6u. The mode2 matching sends u solely to
3sqrt2*d/2, outside that space. Thus exact corner-only tracking does not
hold for every native product-formula prefix. This is not a lower bound
on other contractions or approximate-prefix algorithms.

Actual BGL Algorithm2 requires all bounded-support compiled PREFIX
amplitudes. Its robustness lemma charges a SUM of prefix vector errors,
not endpoint error or arbitrary rare-history conditional error. A sufficient
interface is uniform coefficient accuracy2^-b with
b>=nqubits/2+log2(128*ngates/epsilon). This is polynomially many precision
BITS, but an efficient evaluator is still missing. One must resample each
fiber from G_t times the approximate preceding vector, as in the actual
lemma; no lower bound on individual fiber probability is assumed.
Ground-state alternative additionally owes a unique ground state, local
flip graph, gap, amplitude ratios, initial mass and sensitivity. Corner
gaps do not supply these for arbitrary excited Jack states. Report's
conditional sampler is accepted only with these explicit unpaid routines.
No new unconditional classical improvement or exact gate-exponent claim.

Four-job classical round now TERMINAL: three substantive completed reports,
one truncated EMPTY. No failed call was retried. Their combined outcome
is scoped failed contractions plus a sharper list of unpaid quantities;
general classical Born sampling remains OPEN, never hard by default.
