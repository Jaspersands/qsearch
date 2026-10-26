# A useful refinement: balance is sufficient, not essential

Status: proved deduction from the Fourier algebra, independently derived.
This does not refute the balanced construction; it narrows the possible
novelty claim and identifies an exact failure outside the stated scope.

For any nonempty S in F_(2^n), put p=|S|/q and
a(u)=B(u)/sqrt(q|S|), B(u)=sum_(x in S) chi(ux). Then a(0)=sqrt(p),
and, for d!=0,

    sum_u a(u)a(u+d)=B(d)/|S|,
    a(0)a(d)=B(d)/q,
    sum_(u!=0,d) a(u)a(u+d)=(1-2p)B(d)/|S|.

The three nonempty zero-pattern cells have total absolute correlation

    c_p |B(d)|/|S|,   c_p=2p+|1-2p|.

The support-cell proof therefore works without exact cancellation, with
rho_i(d)=c_(p_i)|B_i(d)|/|S_i| in place of beta. In particular c_p=1 for
p<=1/2 and c_p=4p-1 for p>=1/2. With a common rho bound the excess is
sum_(d in D\0) rho^wt(d), or its minimum-distance bound.

For root densities bounded away from zero and one, uniformly small
nonzero normalized Fourier coefficients still give an exponentially small
coalescence excess. The error-weight distribution is now Poisson-binomial
with nonzero probabilities 1-p_i. Exact balance is especially convenient,
but is not necessary for a related polynomial-time theorem.

An exact counterexample to importing the *unchanged* beta bound above half
density: take q=4, N=1, D=F_4, S=F_4\{0}, p=3/4. The Fourier amplitudes
are a(0)=sqrt(3)/2 and a(u)=-1/(2sqrt(3)) for u!=0. Set the support-only
mask m(0)=1, m(u)=-1 for u!=0. The source norm squared is 1, whereas
||A(ma)||²=3. Here beta=max|B(d)|/|S|=1/3 and (|D|-1)beta=1, smaller
than the actual excess 2. The corrected c_p=2 bound is attained exactly.

Self-attack: the cell proof still requires the mask to depend only on
support. Absolute values of *individual amplitudes* cannot be substituted
before summing the both-nonzero cell. This refinement does not supply a
bound on arbitrary label-dependent arithmetic error, nor classical hardness.

Next use: compare this deterministic spectral condition directly against
existing general decoding-to-coset-sampling theorems. A balanced-specific
identity alone should not be presented as a new quantum framework.
