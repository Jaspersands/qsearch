# Open folded chain: closed all-N transform and classical endpoint review

2026-11-07. Read STATE/TRAPS and the exact proposed contract in
audits/claude_inputs/2026-11-07-folded-transform/brief.md. Read actual
folded.txt Sections3--4, especially equations3.6,3.30 and the clean ancillary
states in Section4.2. Interpreter /opt/anaconda3/bin/python. No network,
API, Git, implementation or finite control was used.

**Disposition: CLOSED for the following WRITTEN transform.** For every N>=2,
the specified open folded Hamiltonian on N+2 qubits has a uniform coherent
fragment/free-fermion transform and an approximate exp(-itH_N) circuit with
BIT/gate cost polynomial in N, the binary rational time's bit length, and
log(1/epsilon). No fragment, momenta, roots, input state description or
initial-state preparation is supplied. The circuit acts on arbitrary input,
including input entangled with an external reference. The error convention
and phase guards below are part of this verdict. No novelty, classical
separation, practicality or implementation claim follows.

## 1. Bond basis and exact matrix elements

Write the spin basis string as s_0,...,s_(N+1), put L=N+1 and
b_i=s_i XOR s_(i+1), 0<=i<N+1. Retain s_0. This is a reversible binary
linear transformation: s_(i+1)=s_i XOR b_i.

The term indexed j in the brief has a nonzero matrix element exactly when
s_(j+1)!=s_(j+2) and s_j=s_(j+3). The XX+YY factor gives amplitude2,
the diagonal factor1+Z_j Z_(j+3) gives2, and the prefactor is -1/8.
Thus its matrix element is -1/2. In bonds the same condition says
(b_j,b_(j+1),b_(j+2)) is 011 or110, and exchanging the two interior spins
replaces that triple by the other one. There are no diagonal contributions.
The j range covers every consecutive triple of the length-L bond string.

## 2. Token bijection, all sectors and transition multiplicity

Greedily parse each bond string from the left with A=11, B=10, C=0,
and a possible final D=1. Equivalently a run of 2a+b ones before a zero
contributes A^a followed by C if b=0 and B if b=1; the terminal run is
A^a D^d. This proves existence and uniqueness without any source-state
promise. Set m=#A, h=#B+#C, ell=m+h, and retain the ordered B/C word w.
The label is (s_0,w,d,m), and q is the length-ell occupancy string with
ones at A tokens and zeros at B/C tokens. Use fixed-size padded registers
and store the lengths as ordinary binary integers.

The image consists precisely of the valid records satisfying

    weight(q)=m, length(w)=h, L=2m+2#B+#C+d.

To invert, replace each one of q by A and its successive zeros by successive
letters of w, append D if d=1, expand the tokens, and use prefix XOR with
s_0. Every such expansion reparses into exactly the same tokens, so this
is a bijection, not an overcomplete encoding. For fixed label, ALL binary
q of length ell and weight m occur. No unused fragment-label advice remains.

Consider an occurrence of 011. Its initial zero is either a standalone C
or the final zero of B; the following two ones are an A token at that point
of the greedy parse. In the first case CA becomes AC, using 011<->110.
In the second case BA=1011 becomes AB=1110, using the final triple. The
rest of the parse is unchanged. For the reverse move110, inspect the run of
ones immediately preceding its zero: an even run gives AC, and an odd run
gives AB. Moving the final two ones across the zero changes the run lengths
by two and leaves every other token and the final-run parity unchanged.
This also proves that no move changes w, d or m.

Conversely each adjacent A/C or A/B pair has exactly the indicated physical
triple and hence exactly one Hamiltonian term. Distinct such pairs change
different adjacent positions of q and cannot yield the same q'. There is
therefore no transition multiplicity, hidden sign, potential or energy shift.
The q graph is the connected exclusion graph of m particles on an open
ell-site path; labels describe complete invariant blocks, not just subsets.

Trailing D never needs to hop: it is the unpaired last one of the final
run, whose parity is invariant under these moves. Both physical boundary
spins are covered. Explicitly,

    s_(N+1)=s_0 XOR (#B mod2) XOR d,

so their conservation is already represented by the label, without fixing
them to00 or using a boundary-sector isomorphism of a different chain size.
The m=0 and m=ell blocks are one-dimensional and jammed. The latter has
free energy zero because the sum of the open-path one-body eigenvalues is
zero. Small and empty-particle cases require no exceptional dynamics.

## 3. Coherent free-fermion reduction and phases

On each valid label block the exact Hamiltonian is

    -(1/4) sum_(r=1)^(ell-1) (X_r X_(r+1)+Y_r Y_(r+1)).

The Jordan-Wigner strings cancel on adjacent hopping, giving one-body matrix
h_(r,r+1)=h_(r+1,r)=-1/2 and no diagonal. Its normalized sine matrix is

    S_(r,k)=sqrt(2/(ell+1))*sin(pi*r*k/(ell+1)),
    S^T h S=diag(-cos(pi*k/(ell+1))).

Use the honest number-preserving second quantization Gamma(S), with vacuum
phase FIXED to1. Real mode rotations and signed/permutation modes give a
polynomial-size Gaussian circuit. A determinant-minus-one mode matrix is
allowed: a single-mode phase supplies it. Fermionic mode swaps include the
usual doubly occupied sign; a bare qubit SWAP is not a substitute.

The inverse sine transform, followed by the OCCUPATION phases

    diag(1, exp(+it*cos(pi*k/(ell+1)))),

and the forward sine transform gives exp(-itH) on that block. These are
occupation phases, not uncorrected Rz gates. Dropping an apparently global
phase in a sector-controlled compiler would create relative phases between
labels. There is no zero-point energy to add: the vacuum has energy0 and
the second-quantized representation is fixed accordingly.

Compute the classical encoding reversibly, then XOR its inverse into the
old spin register to clear it. Both classical directions run in polynomial
time. The label and padded q stay coherent; q's particle number is preserved.
After the mode transformation and phases, apply the inverse encoding to
return the physical qubits and uncompute workspace. Standard reversible
implementations are total permutations; define arbitrary checked behavior on
invalid work-register encodings. Only their action on the valid encoded
subspace is used by the exact proof.

One can implement the variable-length circuit by looping ell=1,...,L and
controlling each fixed-ell circuit on the label. This uses polynomially many
gates, rather than looping over exponentially many w. All labels w with the
same ell have the same free circuit. Keeping labels throughout is required;
measuring, forgetting or prematurely erasing them would break the endpoint.

## 4. Numerical and gate clocks, including arbitrary reference systems

The sine matrix has a stable polynomial-time orthogonal decomposition into
O(ell^2) two-mode rotations and permutations. For example, at each remaining
column choose a largest residual entry as pivot; its norm is at least
1/sqrt(ell) in the exact orthogonal matrix. Givens eliminations then keep
denominators bounded below polynomially, and sufficiently accurate arithmetic
preserves the same bound up to a constant. No exponentially small spectral
gap, Bethe root isolation or ill-conditioned eigensystem is being assumed.

There are polynomially many controlled gates, so approximate the resulting
mode-transform gates to error epsilon/poly(N). Sine and cosine values and
the time phases need only

    O(log N + log(1+|t|) + log(1/epsilon))

bits of accuracy, with the input rational numerator/denominator charged.
Argument reduction modulo2pi must retain the log(1+|t|) bits; computing
t*cos to fixed precision independent of t would be invalid. Ordinary
polynomial-time high-precision arithmetic and finite universal-gate synthesis
pay this precision. For example the phase error in a branch is bounded by
|t| times the sum of its at most L one-body energy errors. Allocate the
remaining error to gate synthesis and both mode transforms by telescoping
operator-norm differences. The total cost is polynomial in the stated bits.

The precise finite-gate guarantee is the clean-input isometry bound

    sup_(||psi||=1) || U_comp(psi tensor0)
                     - (exp(-itH)psi) tensor0 || <= epsilon.

It remains valid after tensoring an arbitrary reference. The resulting
physical channel, after discarding work qubits, is within 2epsilon in diamond
norm. Ideal gates reset the work registers exactly. Approximate finite-gate
synthesis can leave O(epsilon) leakage; it must not be advertised as exact
ancilla reset without an additional exact compilation convention. This
standard isometry-error formulation suffices for native fast-forwarding.

## 5. Strong classical match for the source's correlator endpoint

Actual folded.txt Eq3.6/3.30 writes its specified eigenbasis states as a
known open-XX Slater determinant followed by U_D. Lines434ff say the map
permutes coefficients. Sections4.2--4.3 implement it with reversible
classical gates and fixed/reset ancillary states; the Section4.2 final
auxiliary state is |0^M 1>, not necessarily its initial state. Forward and
inverse classical simulation therefore give samples and amplitudes with
polynomial work. This statement covers the specified fragment/momentum
basis states, not arbitrary coherent combinations in degenerate eigenspaces.

More explicitly, a Slater determinant with orthonormal orbital matrix V
has occupation probability |det(V_S)|^2. Its projection determinantal law
is sampled sequentially from diagonal leverage scores; after selecting i,
the projection updates by K-K e_i e_i^* K/K_ii. Cauchy--Binet proves the
successive rule. Push the sampled occupation set through U_D, or through
the token decoder proved above. To evaluate an arbitrary output amplitude,
invert the permutation, check the fixed padding and particle number, and
compute the corresponding determinant; outside the image the amplitude is0.

For an efficiently row-sparse observable O with known norm bound B, draw
x from |psi_x|^2 and form

    L(x) = sum_y O_(x,y) psi_y/psi_x.

Zero-amplitude x have probability zero. Direct calculation gives

    E L = <psi|O|psi>,
    E |L|^2 = sum_(psi_x!=0) |(O psi)_x|^2 <= B^2.

Median-of-means uses O(B^2 epsilon^-2 log(1/eta)) samples. A Pauli string of
ANY length is one-sparse with B=1. Polynomial Pauli sums have polynomial
row sparsity and the explicit coefficient-l1 norm bound. Thus arbitrary
string length alone supplies no additive-correlator advantage for these
specified folded eigenstates. This does not challenge statements about
general interacting XXZ eigenstates or exponentially precise relative error.

Finite precision is paid, rather than inferred from the formal ratio. The
open-chain sine orbitals lie in a cyclotomic field of degree O(N), with at
most a quadratic extension for a common normalization. Determinants, their
ratios and the conditional sampling probabilities have polynomial-size
algebraic representations: use minors/Schur complements of the original
matrix to bound heights rather than multiplying bounds through a recursive
division expression. Exact zeros can be checked; a nonzero denominator has
an effective 2^-poly(input) lower bound by the algebraic norm/height bound.

For approximate sampling, clip the complex estimator radially at
R=O(B^2/epsilon). Its clipping bias is at most E|L|^2/R<=B^2/R.
Total variation delta=O(epsilon/R) in the sampling law then changes the
clipped expectation by at most 2R*delta. Approximate the ratios to the
remaining additive error. All required precision is polynomial in N and
log(B/epsilon), with polynomial dependence on B/epsilon in sample count.
No unproved minimum-probability promise is used.

## 6. Computational-basis quenches and the unmatched unitary scope

For a known computational-basis input, the token label is known and its q
state is an occupation vector. Free evolution turns it into a Slater
determinant. The same determinant sampler and local estimator therefore
classically match computational-basis sampling and additive sparse-observable
estimation, including at binary long times. Inverse token encoding makes
amplitudes outside the fixed label exactly zero.

There is a useful finite-precision repair for long-time phases, where exact
transcendental zeros need not be decided. Keep the sine transform algebraic
and approximate each unit phase by an EXACT rational point on the unit
circle, using a bounded stereographic chart. This creates an exactly unitary
approximate one-body matrix over a polynomial-degree algebraic field, with
polynomial-bit height in N, bitlength(t), log(B/epsilon). Its M-particle
Slater state differs by at most M times the one-body error. Choose that error
so the observable bias is O(epsilon), then apply the preceding algebraic
sampler/estimator to this exact nearby state. This avoids an exact-zero
oracle for transcendental amplitudes and preserves the polynomial clock.

These matches do NOT produce a classical implementation of the arbitrary-
unknown-input unitary, especially when the input is entangled with a
reference. They also do not prove its classical hardness. The constructive
all-sector token transform is the extra operation beyond the source's
supplied-eigenstate preparation; its priority remains a separate literature
question. No conclusion here uses a finite control or an agent ACCEPT label.
