# Uniform Algorithm And Paid Error Budget

## Claim And Scope

This is a **review-pending mathematical algorithm argument**, not a quantum
execution, compiled circuit, kernel-checked proof, novelty claim or speedup.
It closes a particular gap in INTEGER_CHARACTER_INTERPOLATION.md: the
924-bit native decoder control alone did not establish a uniform, paid
end-to-end quantum procedure.

For every m>=20000, put cap=floor(7m/200) and t=1/20. Take any m distinct
public primes other than 3, including 2, and construct M=3^k with
M>2*B^(2cap+1), where B is the largest prime. Include the actual verified
labels a_i=log_2(p_i) modulo N=2*3^(k-1) in the public input. For EVERY
public center vector c in Z_N^m, the argument below gives a bounded-error
quantum procedure producing x with

```
(1/m)*sum_i cos(2*pi*(a_i*x-c_i)/N) >= 3/10.
```

Its bit complexity is polynomial in the public description length and
log(1/failure_probability). This is not an optimality approximation ratio.
There is no demonstrated advantage over classical algorithms on this task.
The separate m=1024 native certificate is covered by its own exact mean
and source-mass bounds, not by pretending that it satisfies m>=20000.

The integer lattice and rational decoder are known from
[Ducas--Pierrot (2018)](https://doi.org/10.1007/s10623-018-0573-3).
The radix-d Fourier circuit is also standard; see
[Camps, Van Beeumen and Yang](https://arxiv.org/abs/2003.03011).
The composition, constants and error bookkeeping here need independent
review, including comparison with existing DQI and quantum transference.

## A Uniform Source Bound

Start from independent signed coordinates with probabilities
(1-t,t/2,t/2)=(19/20,1/40,1/40). Let P and Q be the positive and negative
counts. They are NOT independent, but each has the stated binomial marginal.
Only the union bound is used.

For a length-m word, the variance of either count is 39m/1600.
Since cap+1>7m/200, the gap above its mean m/40 is greater than m/100.
Chebyshev and the union bound give

```
Z = Pr[P,Q<=cap] >= 1 - 975/(2m) >= 1561/1600 > 1/4.
```

For a length-(m-1) word, define R=Pr[P<=cap-1,Q<=cap].
The smaller bad-event gap is

```
cap - (m-1)/40 >= m/100 - 39/40 >= 199m/20000,
```

where the last inequality holds for every m>=20000. Consequently,

```
1-R <= 19500000/(39601*m) <= 975/39601 < 1/40.
```

The already established signed-box/readout identity therefore gives

```
mu = sqrt(19/200)*R/Z > sqrt(19/200)*(39/40) > 601/2000.
```

The last comparison is exact: square the two positive quantities.
The producer checks these rational constants and their monotone endpoint
conditions. It does not prove the written probabilistic argument by
running a finite parameter sweep.

## Actual Source Preparation

Prepare m local qutrit states with amplitudes

```
sqrt(19/20)|0> +
sqrt(1/40)*exp(-2*pi*i*c_i/N)|+1> +
sqrt(1/40)*exp(+2*pi*i*c_i/N)|-1>.
```

Compute P,Q reversibly, compute only the Boolean box-membership flag, and
uncompute the count registers. Measure the FLAG, not the counts or word.
On rejection discard the registers and charge a new trial. On success the
word is precisely the conditioned product source. No exponentially large
amplitude table, QRAM, uniform-superposition oracle or free postselection
is used. Counts cost O(m log m) elementary reversible operations.
With two-qubit qutrit encodings, the herald also rejects invalid symbols.
Extend every arithmetic permutation and Fourier block unitarily to the
unused encoding states; reject invalid measured outputs. Approximation
leakage is included in the same norm/TV budget, not silently renormalized.

Add the public signed labels into an initially zero syndrome register.
Reversibly compute D(s) from s alone, XOR its fixed two-bit-per-coordinate
encoding into the word register, and uncompute the decoder workspace.
On the licensed support D(s)=y, so the word register is erased.
Define D(s)=0 on invalid syndromes to make this a total classical function
before reversible compilation. Do not assume a decoder is already unitary.

D computes 2^s modulo M, bounded rational reconstruction, and trial
division by the PUBLIC primes. There is no arbitrary integer factoring
oracle or secret error word. The height/readout guard covers both norm
and score identities, including magnitude-two transitions.

## Fourier Transform And Bit Costs

Let q=3^(k-1). Convert the syndrome exactly to (s mod2,s modq).
Apply F_2 tensor F_q, then relabel the output (e,v) as

```
x = q*e + 2*v mod 2q.
```

Indeed exp(2*pi*i*s*x/(2q)) equals the product of the two CRT characters.
This is the required cyclic Fourier transform; using the input CRT
inverse as an unexamined output map would be an indexing error.
The radix-three circuit for F_q has k-1 single-qutrit Fourier blocks,
(k-1)(k-2)/2 controlled-phase blocks, and digit reversal. Each qutrit can
be encoded in two qubits. Exact digit conversion and reversible arithmetic
are polynomial in L=bit_length(M). No array of length N is allocated.

Using conservative schoolbook integer arithmetic:

- Public label construction/verification costs O(m L^3) bit operations.
- One syndrome uses O(m) controlled constant additions, costing O(m L)
  bit gates. Counting the word costs O(m log m).
- Modular exponentiation and Euclidean reconstruction cost O(L^3).
- Trial division uses O(m+L) divisions on O(L)-bit integers: there are at
  most O(L) successful prime-factor removals across both integers.
  Thus this part costs O((m+L)L^2), including failed divisibility checks.
- A saved-history reversible simulation has polynomial circuit size and
  space; the exact workspace/T counts have NOT been compiled.
- There are O(L^2) constant-dimensional Fourier blocks. Their synthesis
  adds polylog((m+L)/epsilon) overhead per block with a fixed universal
  gate set. These block counts are not fault-tolerant gate estimates.

For b=bit_length(B), minimal k has L=O(m b). The public table itself has
O(m L) bits. Prime validation/generation must be charged classically;
native primes are obtained by a sieve, not by a quantum subroutine.
These polynomial bounds are deliberately not claims of practical economy.

## Error And Repetition Accounting

Let epsilon=1/10000. Bound the entire pre-herald source-state norm error
by delta=epsilon/8, for example by giving each of its m local unitary
blocks operator error at most epsilon/(8m). All counting/arithmetic
permutations are exact at the logical level.

If P is the herald projection, ||P psi||=sqrt(Z). For a normalized
approximation phi with ||phi-psi||<=delta, normalization gives

```
|| P phi/||P phi|| - P psi/sqrt(Z) || <= 2*delta/sqrt(Z) <= 4*delta.
```

The approximate herald probability is at least
(sqrt(Z)-delta)^2 >= (1/2-delta)^2 > 1/8.
Give the full QFT operator error at most epsilon/2. Telescoping errors
through its compiled blocks and contractivity under measurement imply
conditional output total variation at most 4delta+epsilon/2=epsilon.
There is no assertion that a floating state-vector check establishes this
operator-norm budget.

Compute every score from EXACT modular integer residues. An interval
implementation and fail-closed verifier are supplied in the producer.
The verifier checks its enclosure width and accepts only a rigorous lower
bound of at least 3/10. Equivalently, choose an estimate with
absolute error eta=1/100000 and accept only if estimate-eta>=3/10.
No false positive is then possible; a true score at least 3/10+2eta
is accepted. Since scores lie in [-1,1], the ideal mean lower bound yields

```
Pr[robust acceptance | herald]
 >= (601/2000 - (3/10+2eta))/(1-(3/10+2eta)) - epsilon
 > 1/2000.
```

Each FULL trial, including a possible source rejection, succeeds with
probability greater than 1/16000. Fresh trials are independent for the
fixed public input. A block of 16000 trials fails with probability below
1/2: (1-p)^r <= 1/(1+r*p). Therefore 16000*b trials suffice for failure
probability at most 2^-b. Score verification and failed trials are charged.
The constants are loose but remove an unpriced amplification assumption.

## What Could Invalidate The Direction

1. An error in the height/readout identity or reversible source erasure
   invalidates the algorithm. The tests check identities and rational
   certificates, not the whole proof in a theorem prover.
2. A compiler exceeding these stated primitive errors invalidates the
   claimed output guarantee for that implementation. This is an error
   specification, not an already compiled circuit.
3. A classical p-adic, lattice or other algorithm reaching score 0.3
   efficiently removes the proposed advantage. The smooth modulus is
   an obvious attack surface; huge N is not a hardness argument.
4. A known equivalent quantum algorithm removes any novelty. The core
   decoder and Fourier technique are already known.
5. Failure to connect this search task to a meaningful external problem
   limits research impact even if the mathematics is correct.

The next decisive work remains structural classical attacks and a useful
reduction, not tightening these conservative constants or a pilot sweep.
The result is kept outside central claim admission and the UI.

## Reproduction

```
python theorems/integer_character_uniform.py
python -m pytest -q tests/test_integer_character_uniform.py -W error::RuntimeWarning
```

The report is `research/phase_workbench/integer_character_uniform.json`.
The native source artifact is hashed, and the producer fails closed if
that artifact no longer matches its own source producer.
