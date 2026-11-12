## Verdict

**The two-control encoding can be proved under the contract’s stated native-pulse interfaces.** The prime construction needs an explicit repair, supplied below. Moreover, the entangler can be simplified:

> An isolated, normalized **\(\pi\)-pulse** on the cross-sum interaction implements CZ exactly on the code. No commutator limit is needed.

I also give an operator-norm bound validating the parent’s original commutator construction.

For a standard \(n\)-qubit, \(G\)-gate \(\{H,T,\mathrm{CZ}\}\) circuit and \(0<\epsilon\le1\), the simpler construction has
\[
D=O((n+1)^5),\qquad
m=O\!\left(\frac{(G+1)^2D^6}{\epsilon}\right)
 =O\!\left(\frac{(G+1)^2(n+1)^{30}}{\epsilon}\right).
\]
All pulse times can lie on **one explicitly specified dyadic clock**, with polynomially bounded inverse tick size. Initial occupation, complete pulse list, output tolerance, and decoder are explicit.

This is a worst-case BQP encoding, not an unconditional classical lower bound, novelty claim, or practical-speedup result.

---

## 1. Dequantization checks first

### The standard free-fermion shortcut fails

In the usual boson–fermion correspondence, write
\[
\alpha_{-k}=\sqrt{k}\,a_k^\dagger,\qquad
\alpha_k=\sqrt{k}\,a_k.
\]
Although \(S\) is quadratic in the standard fermionic description,
\[
N=\sum_{k\ge1} k\,\alpha_{-k}\alpha_k
\]
is a density–density operator and contains genuine quartic fermionic terms.

There is a small exact witness. In the orthonormal Schur basis at \(D=4\),
\[
\langle (4)|N|(2,2)\rangle
 =\frac13+2-\frac{10}{3}=-1.
\]
The associated occupied fermion positions are
\[
(4):\quad \{7/2,-3/2,-5/2,\ldots\},
\]
\[
(2,2):\quad \{3/2,1/2,-5/2,\ldots\}.
\]
These differ by two occupied-position substitutions. A quadratic fermionic operator cannot connect them. Thus \(N\) is not Gaussian in the standard representation making \(S\) free fermionic.

This finite witness **only rejects that Gaussian shortcut**. It is not hardness evidence by itself. Also, calling \(S\) free fermionic does not, without further work, make the specified bosonic occupation input and output free classical preprocessing.

### The obvious symmetries do not provide a dequantization

Momentum is conserved, as required. Boson-number parity satisfies
\[
P S P=-S,\qquad PNP=N,
\]
so it is not a common conserved symmetry of both controls. Integrability of a fixed \(S+\varepsilon_{\rm disp}N\) does not imply a common efficiently sampled representation for arbitrary alternating pulses.

I do not claim to have excluded every possible classical representation. The constructive reduction below supplies the complexity consequence; failed dequantization attempts do not.

---

## 2. Actual normalization and global norm bounds

At \(\hbar=1\), substituting
\[
V_k=\sqrt{k}\,a_k^\dagger,\qquad V_{-k}=\sqrt{k}\,a_k
\]
into the supplied Eq. (2.1) gives
\[
T_3=S+\varepsilon_{\rm disp}N.
\]
In particular, the displayed \(S\) has **no missing factor \(1/2\)**.

For distinct \(u,v\), let
\[
C_{uv}=a_u^\dagger a_v^\dagger a_{u+v}.
\]
The ordered pairs \((u,v)\) and \((v,u)\) together contribute
\[
\gamma_{uv}(C_{uv}+C_{uv}^\dagger),
\qquad
\gamma_{uv}=2\sqrt{uv(u+v)}.
\]
The ordered-pair factor \(2\) must therefore be included. For comparison, at \(D=2\), the matrix element between \(|n_2=1\rangle\) and \(|n_1=2\rangle\) is \(2\), not \(1\).

On the momentum-\(D\) sector, the stated cut-and-join spectrum gives
\[
\|S\|=D(D-1)\le D^2.
\]
Also,
\[
N=\sum_k k^2n_k\le D\sum_k kn_k=D^2,
\]
with equality on the one-boson mode-\(D\) state. Hence
\[
\boxed{\|S\|\le D^2,\qquad \|N\|=D^2.}
\]

Finally,
\[
[N,C_{uv}]=-2uv\,C_{uv}.
\]

The supplied excerpt supports the normalization. It does not itself prove the driven universality or the admitted clean native-pulse implementation.

---

## 3. An explicit polynomial Sidon-prime construction

Take \(n\ge1\) and define
\[
\boxed{R=2^{20}(n+1)^4.}
\]
We will greedily select \(2n\) primes from \((R,2R]\), requiring all unordered pair sums, **including repeated pairs**, to be distinct.

### 3.1 An elementary prime-count bound

For every integer \(R\ge2^{20}\),
\[
\boxed{\pi(2R)-\pi(R)\ge \frac{R}{4\log(2R)}.}
\]

Here is a proof, rather than a prime-distribution promise.

Let
\[
P(x)=\prod_{p\le x}p.
\]
The elementary bound \(P(x)\le4^x\) follows by induction. For odd \(m=2a+1\),
\[
P(m)\le P(a+1)\binom{2a+1}{a}
       \le 4^{a+1}2^{2a}=4^m;
\]
even \(m>2\) reduces to \(m-1\).

Now
\[
\binom{2R}{R}\ge \frac{4^R}{2R+1}.
\]
For primes \(p\le\sqrt{2R}\), the total power of each \(p\) dividing this binomial coefficient is at most \(2R\). Primes in \((2R/3,R]\) do not divide it. Consequently,
\[
\binom{2R}{R}
\le
(2R)^{\sqrt{2R}}\,4^{2R/3}
\prod_{R<p\le2R}p.
\]
Taking logarithms,
\[
\sum_{R<p\le2R}\log p
\ge
\frac{R}{3}\log4
-\sqrt{2R}\log(2R)-\log(2R+1)
\ge \frac R4.
\]
The last inequality holds for \(R\ge2^{20}\): the two error terms divided by \(R\) decrease there, their sum is below \(1/12\) at \(2^{20}\), and \(\log4\ge1\). Dividing by \(\log(2R)\) proves the bound.

For our chosen \(R\),
\[
\log(2R)\le21+4n\le25(n+1),
\]
so the interval contains more than
\[
\frac{2^{20}}{100}(n+1)^3>24n^3
\]
primes.

### 3.2 Greedy Sidon selection

Suppose \(A\) contains \(t\) already selected primes. A new value \(x\) can create a pair-sum collision only through
\[
x+a=b+c,\qquad 2x=b+c,\qquad x=a,
\]
with \(a,b,c\in A\).

Thus at most
\[
t^3+t^2+t\le24n^3
\]
values are forbidden while selecting the first \(2n\) elements. The interval contains more candidates than this.

A uniform algorithm therefore:

1. sieves all integers through \(2R\);
2. enumerates the forbidden values at each step;
3. selects the first remaining prime.

This takes polynomial time in \(n\), with no prime oracle.

Name the selected primes
\[
p_1,q_1,\ldots,p_n,q_n,
\qquad c_i=p_i+q_i,
\]
and set
\[
\boxed{D=\sum_{i=1}^n c_i\le4nR.}
\]

All primes are odd. All relevant sum modes are even, and the Sidon property makes the local \(c_i\) and cross sums \(p_i+p_j\) distinct.

### 3.3 Semiprime aliases are absent

Every selected distinct-prime product satisfies
\[
uv>R^2>4nR\ge D.
\]
The only unordered factor pairs of \(uv\) are
\[
\{u,v\},\qquad \{1,uv\}.
\]
The second is absent from \(S\), because \(1+uv>D\).

For a cross interaction, \(n\ge2\) and
\[
p_i+p_j\le4R<D,
\]
so its intended sum mode does exist. This repairs the parent’s critical cutoff defect.

---

## 4. Exact Fourier identities, implemented only by \(S,N\) pulses

Choose a power-of-two grid
\[
\boxed{
M=2^{\lceil\log_2(4D^2+1)\rceil},
\qquad 4D^2<M\le8D^2.
}
\]
Define
\[
\theta_s=\frac{2\pi s}{M},\qquad
S_s=e^{i\theta_sN}Se^{-i\theta_sN},
\quad 0\le s<M.
\]

For a selected pair \(u,v\), put \(z=uv\) and
\[
X_{uv}=C_{uv}+C_{uv}^\dagger,\qquad
Y_{uv}=i(C_{uv}^\dagger-C_{uv}).
\]
Then
\[
X_{uv}
=\sum_{s=0}^{M-1}
 \frac{2\cos(2z\theta_s)}{M\gamma_{uv}}\,S_s,
\]
\[
Y_{uv}
=\sum_{s=0}^{M-1}
 \frac{2\sin(2z\theta_s)}{M\gamma_{uv}}\,S_s.
\]

These identities are exact. All native frequencies are \(\pm2ij\), with \(i+j\le D\). Every nonzero frequency difference or sum relevant to the projection has magnitude below \(M\). The semiprime cutoff leaves exactly the intended ordered pair and its reverse.

Write either identity as \(H=\sum_s w_sS_s\). Since \(\gamma_{uv}>1\),
\[
\sum_s\|w_sS_s\|
\le \frac{2\|S\|}{\gamma_{uv}}
\le 2D^2.
\]
Use the uniform bound
\[
\boxed{\Lambda=2D^2.}
\]

Crucially, the weighted sum is **not** an available Hamiltonian. Each exponential of a summand is implemented by three actual pulses:
\[
e^{-iaS_s}
=
e^{i\theta_sN}e^{-iaS}e^{-i\theta_sN}.
\]
Signed weights merely produce signed \(S\)-pulse times, which the contract permits.

---

## 5. Logical gates and an exact finite-angle entangler

### 5.1 Local qubits

For qubit \(i\),
\[
|0_i\rangle=|n_{c_i}=1,n_{p_i}=n_{q_i}=0\rangle,
\]
\[
|1_i\rangle=|n_{c_i}=0,n_{p_i}=n_{q_i}=1\rangle.
\]
Both have momentum \(c_i\).

The triples are disjoint. On this two-dimensional space,
\[
C_{p_iq_i}|0_i\rangle=|1_i\rangle,\qquad
C_{p_iq_i}^\dagger|1_i\rangle=|0_i\rangle,
\]
and the other two actions vanish. All matrix elements are exactly \(1\).

Therefore the local code is exactly invariant under the isolated quadratures. In the ordered basis \((|0_i\rangle,|1_i\rangle)\),
\[
X_i=\sigma_x,\qquad Y_i=-\sigma_y.
\]
The sign of \(Y_i\) is worth making explicit.

Up to global phase,
\[
H_i\doteq e^{-i\pi Y_i/4}e^{-i\pi X_i/2},
\]
\[
T_i\doteq
e^{-i\pi Y_i/4}e^{-i\pi X_i/8}e^{i\pi Y_i/4}.
\]
Thus \(H\) needs two normalized primitive exponentials and \(T\) needs three.

### 5.2 Exact CZ by a return pulse

For qubits \(i\ne j\), let
\[
r=p_i+p_j,\qquad C=a_{p_i}^\dagger a_{p_j}^\dagger a_r,
\qquad X=C+C^\dagger.
\]
The mode \(r\) is empty throughout the code.

On logical \(00,01,10\), both \(C\) and \(C^\dagger\) vanish. On logical \(11\),
\[
C^\dagger|11\rangle=|a_{ij}\rangle,
\]
where \(|a_{ij}\rangle\) replaces the two bosons in \(p_i,p_j\) by one boson in \(r\), leaving \(q_i,q_j\) and all spectator qubits unchanged. Conversely,
\[
C|a_{ij}\rangle=|11\rangle.
\]
There are no further transitions from this two-state block.

Hence \(X\) is exactly \(\sigma_x\) on
\(\operatorname{span}\{|11\rangle,|a_{ij}\rangle\}\), and
\[
\boxed{
e^{-i\pi X}\big|_{\rm code}=\mathrm{CZ}_{ij}.
}
\]
The ancillary sum mode returns exactly to vacuum in the ideal gate. This is a finite-angle identity, not a limiting argument, and it uses no postselection or prepared auxiliary state.

A \(\{H,T,\mathrm{CZ}\}\) circuit consequently requires at most \(3G\) normalized primitive exponentials, all with \(|t|\le\pi<4\).

The initial occupation is explicitly
\[
\boxed{\mu=(c_1,\ldots,c_n)}
\]
sorted as a partition if required.

---

## 6. The parent’s commutator is also valid

For the same cross interaction,
\[
CC^\dagger=n_{p_i}n_{p_j}(n_r+1),
\]
\[
C^\dagger C=(n_{p_i}+1)(n_{p_j}+1)n_r.
\]
Thus
\[
K=[C,C^\dagger]
=n_{p_i}n_{p_j}-n_r(n_{p_i}+n_{p_j}+1).
\]
With \(X=C+C^\dagger\) and \(Y=i(C^\dagger-C)\),
\[
[X,Y]=2iK.
\]
On the code, \(K=|11\rangle\langle11|\). For unnormalized isolated quadratures, the commutator carries the additional factor \(\gamma_{p_ip_j}^{\,2}\); normalization cannot be omitted.

There is a direct polynomial error bound. Set
\[
W(h)=e^{-ihX}e^{-ihY}e^{ihX}e^{ihY}.
\]
For \(\Lambda h\le1/4\),
\[
\boxed{
\|W(h)-e^{-2ih^2K}\|\le32\Lambda^3h^3.
}
\]
For example, expand the four exponentials through total degree two. The remaining product tail is bounded by
\[
\frac{(4x)^3e^{4x}}6,\qquad x=\Lambda h,
\]
and the tail of the target exponential by \(2x^4e^{2x^2}\). Their sum is below \(32x^3\) for \(x\le1/4\).

For desired commutator-gate error \(\eta\), choose
\[
\ell=\left\lceil(128\Lambda^3/\eta)^2\right\rceil,
\qquad h=\sqrt{\frac{\pi}{2\ell}}.
\]
Then
\[
\left\|W(h)^\ell-e^{-i\pi K}\right\|
\le
\frac{32\Lambda^3(\pi/2)^{3/2}}{\sqrt{\ell}}
<\eta.
\]
This uses \(4\ell\) normalized primitive exponentials: polynomial, not exponential commutator depth.

The exact return pulse above is simply cheaper.

---

## 7. A complete finite-word, finite-clock compiler

Here are explicit parameters for the simpler return-pulse construction:
\[
g=G+1,\qquad Q=3g,
\]
\[
\boxed{
L=\left\lceil\frac{64Q\Lambda^2}{\epsilon}\right\rceil,
\qquad
J=QML,
}
\]
\[
\boxed{
B=\left\lceil\log_2\!\left(\frac{32D^2J}{\epsilon}\right)\right\rceil,
\qquad
b=\left\lceil\log_2(4/\epsilon)\right\rceil.
}
\]
Here \(Q\) bounds the normalized primitive count; \(J\) bounds the number of \(S\) pulses.

### 7.1 Product-formula error

For a normalized primitive \(e^{-itH}\), with \(H=\sum_s w_sS_s\), use
\[
F_H(t)=
\left(
\prod_{s=0}^{M-1}
e^{-i(t/L)w_sS_s}
\right)^L.
\]
Every factor becomes three native pulses.

The unitary first-order product-formula estimate gives
\[
\|F_H(t)-e^{-itH}\|
\le
\frac{t^2}{2L}\sum_{s<s'}\|[w_sS_s,w_{s'}S_{s'}]\|
\le \frac{t^2\Lambda^2}{L}.
\]
Since \(|t|<4\), the error per primitive is at most
\[
\frac{16\Lambda^2}{L}\le\frac{\epsilon}{4Q}.
\]
Telescoping over the circuit gives total product-formula error at most \(\epsilon/4\).

This is a global operator-norm bound on the whole momentum-\(D\) sector. It does not assume that intermediate product-formula states remain in the code.

### 7.2 Finite time precision

An ideal \(S\)-pulse duration is
\[
\tau=\frac{t\,w_s}{L}.
\]
Compute and round \(\tau/(2\pi)\) to a dyadic \(a/2^B\) with error at most \(2^{-B}\). The emitted pulse is
\[
U_S\!\left(2\pi a/2^B\right).
\]
For each such pulse,
\[
\|e^{-i\tau S}-e^{-i\widetilde\tau S}\|
\le D^2|\tau-\widetilde\tau|.
\]
Across at most \(J\) \(S\) pulses,
\[
\text{rounding error}
\le 2\pi D^2J\,2^{-B}
\le\frac{\epsilon}{4}.
\]

The \(N\)-pulse times \(2\pi s/M\) are exact dyadic clock values. Moreover, \(B\ge\log_2M\), so **every pulse can use the same clock**
\[
\boxed{\Delta=2\pi\,2^{-B}.}
\]

The square roots, \(\pi\), sine and cosine values are computable to certified accuracy by polynomial-time arithmetic: bisection and range-reduced convergent series suffice. Trigonometric arguments can first be reduced modulo \(M\) by integer arithmetic. All coupling coefficients are explicit functions of the selected integers; no coupling oracle is present.

### 7.3 Pulse count, precision, and total time

The native pulse count obeys
\[
m\le3J.
\]
Using \(M\le8D^2\), \(\Lambda^2=4D^4\), and
\(L\le65Q\Lambda^2/\epsilon\),
\[
\boxed{
m\le56160\,\frac{(G+1)^2D^6}{\epsilon}.
}
\]
Also,
\[
B=O\!\left(\log D+\log(G+1)+\log(1/\epsilon)\right).
\]
Thus the explicit pulse-list bit length is
\[
O(mB),
\]
not a logarithmic-size description of a repeated word.

All pulse magnitudes can be kept below \(2\pi\), so
\[
\sum_{\text{pulses}}|t_{\text{pulse}}|\le2\pi m.
\]
No exponentially long evolution is hidden behind binary times. The inverse clock spacing is polynomial in the charged parameters.

The compiler performs the polynomial-size sieve, finite forbidden-set tests, certified arithmetic, and emits all \(m\) pulses. It is therefore a uniform polynomial-time compiler, not merely a controllability proof.

### 7.4 Explicit bound for the original commutator version

To retain the parent’s entangler unchanged, take
\[
\eta=\frac{\epsilon}{4g},\qquad
\ell=\left\lceil(128\Lambda^3/\eta)^2\right\rceil,
\]
replace \(Q\) above by
\[
Q_{\rm comm}=g(4\ell+3),
\]
and use the same formulas for \(L,J,B,b\).

The three error contributions are then:

- commutator approximation: at most \(\epsilon/4\);
- Fourier product formulas: at most \(\epsilon/4\);
- rational-clock rounding: at most \(\epsilon/4\).

Its pulse count is
\[
m_{\rm comm}
=O\!\left((G+1)^6D^{30}\epsilon^{-5}\right).
\]
Thus the parent’s original mechanism is also polynomial after the prime repair, though substantially worse.

---

## 8. Measured output and all access costs

For the return-pulse compiler, the emitted exact native word differs from the ideal encoded circuit by at most
\[
\delta\le\epsilon/2
\]
in operator norm, up to the circuit’s irrelevant global phase.

Define the decoder on **every** measured occupation:

1. Check that every local triple is one of its two code patterns.
2. Check that all other modes are empty.
3. If valid, return the corresponding \(n\)-bit string.
4. Otherwise return a fixed string, such as \(0^n\).

There is no postselection.

The ideal circuit stays in the code. Hence bad-code probability is at most \(\delta^2\), and, more generally, measurement followed by deterministic decoding changes the output distribution by at most \(\delta\) in TV distance.

A native sampler with the emitted tolerance
\[
2^{-b}\le\epsilon/4
\]
therefore produces decoded samples within \(3\epsilon/4<\epsilon\) of the target circuit distribution. For the original commutator version, the corresponding bound is \(\epsilon\).

### Charged costs

- **Input:** the circuit, primes, occupation, and every pulse are explicit. Reading/writing the pulse list costs at least \(O(mB)\).
- **Initial state:** only the allowed explicit Fock basis input is used. In an occupation-register simulation, basis initialization costs at most \(O(D\log D)\), not arbitrary amplitude loading.
- **Quantum pulse implementation:** using the admitted interface, implement each of the \(m\) pulses to error \(O(2^{-b}/m)\). Total cost is
  \[
  m\,\operatorname{poly}(D,B,b+\log m)+O(D\log D).
  \]
  The clean native-pulse algorithms are admitted here, not proved by the supplied primary excerpt.
- **Output:** reading the full occupation and decoding costs \(O(D\,\operatorname{polylog}D)\) with a straightforward representation.
- **Numerical \(D\):** this is a polynomial-\(D\) statement, not a poly-\(\log D\) statement for arbitrary succinct inputs. On the reduced family, \(D\) is polynomial in the source circuit size.

For \(n=0\), use a trivial fixed occupation, no pulses, and the empty-string decoder.

---

## 9. What is proved, assumed, and not established

### Proved within the mathematical contract

- An elementary, uniform polynomial Sidon-prime construction.
- Elimination of the \((1,uv)\) semiprime alias.
- Exact Fourier isolation with the actual ordered-pair normalization.
- Exact local two-level invariance.
- An exact finite-angle CZ with vacuum return.
- The parent’s commutator identity and a polynomial operator-norm synthesis bound.
- A finite native pulse list, common finite clock, full error budget, and unconditional decoder.

No Lie-rank claim, finite simulation, or general bosonic-universality theorem is used.

### Admitted interfaces

The contract’s efficient native \(S/N\) pulse implementations and canonical occupation input/output access remain assumptions of the access model. A physical implementation with different normalization, inaccessible signed times, or additional uncontrolled errors would require a new analysis.

### Complexity consequence

A classical randomized sampler efficient in the charged parameters for all these constructed instances would simulate arbitrary BQP circuit output distributions to bounded error. Therefore
\[
\boxed{\text{such a classical sampler would imply }\mathrm{BPP}=\mathrm{BQP}.}
\]

That is a BQP-hard sampling consequence. It is **not** an unconditional statement that classical sampling is hard. A genuinely efficient classical representation with efficient initialization and output sampling would instead yield that complexity collapse; its existence is not logically excluded by a failed Gaussian attack.

The construction also establishes no priority, practical advantage, generic-drive hardness, or Shor-level discovery. Its large polynomial overhead is a universality certificate, not an engineering proposal.