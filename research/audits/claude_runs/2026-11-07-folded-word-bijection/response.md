# Review: bond-token bijection and block conjugacy (brief.md, lemma only)

**Verdict.** I could not falsify the lemma. Cheapest attacks (odd 1-runs, trailing D, string start, B-type zeros, double-counted triples, diagonal terms) all fail. Below is a complete local-case proof. Everything else in the brief (circuit, costs, comparator) is out of scope and remains unproved here.

## 0. Setup (proved deductions from the stated H)

- $(X_{j+1}X_{j+2}+Y_{j+1}Y_{j+2})$ has no diagonal entries and maps $|01\rangle\mapsto 2|10\rangle$ on sites $(j+1,j+2)$; $(1+Z_jZ_{j+3})$ equals $2$ iff $s_j=s_{j+3}$, else $0$. Hence $H_N$ in the computational basis is purely off-diagonal with entry exactly $-\tfrac18\cdot2\cdot2=-\tfrac12$ on each pair $a01a\leftrightarrow a10a$ at sites $j..j+3$, $j=0..N-2$, and nothing else. A given basis transition flips exactly sites $(j+1,j+2)$, so $j$ is unique: **no transition multiplicity at the physical level.**
- Bonds $b_i=s_i\oplus s_{i+1}$, $i=0..N$. Direct check: $a01a\mapsto$ bonds $(a,1,\bar a)$ wait, explicitly $0010\to011$, $0100\to110$, $1011\to110$, $1101\to011$ on bonds $(b_j,b_{j+1},b_{j+2})$. So every physical transition is $011\leftrightarrow110$ on bond triple $(j,j+1,j+2)$, and $j=0..N-2$ ranges over **all** consecutive triples of the length-$(N+1)$ bond string. $(s_0,b)\leftrightarrow s$ is a bijection (CNOT ladder); $s_{N+1}=s_0\oplus(\#1\text{s of }b \bmod 2)$.

## 1. Bijection (parse)

$\{A=11,\ B=10,\ C=0\}$ is a complete prefix code; the only string with no codeword prefix is a lone final $1$, named $D$. Hence every binary string decodes uniquely into a token word $T\in\{A,B,C\}^*D^{d}$, and conversely every such word (with $D$ only last) encodes to a string whose greedy parse returns the same word. "Ambiguous 1-runs" are not ambiguous: every run start is a token boundary (the preceding $0$ is either $C$ or the tail of a $B$), so an odd run of length $2a+1$ followed by $0$ is forced to $A^aB$, an even run $A^aC$, and the final run $A^aD^d$. Given the label $(s_0,w,d,m)$ and $q$, reinsertion is the inverse. Dimension check: token-sequence counts satisfy $a_L=a_{L-1}+2a_{L-2}$, $a_1=2$ ($C$ or $D$), $a_2=4$, giving $2^L$; so blocks exhaust the space with $\sum_{\text{labels}}\binom{\ell}{m}=2^{N+1}$. Length constraint $L=2m+2\#B+\#C+d$ is forced, not an extra assumption.

## 2. Label invariance under $011\leftrightarrow110$

A rewrite moves one $0$ by two positions; the 1-run to its left changes length by $\pm2$ and the run to its right by $\mp2$. Run-length **parities are preserved**, the number and order of zeros are preserved, and the final run's parity is preserved. Token identity of each zero ($C$ iff preceding run length even, $B$ iff odd) and $d$ are therefore invariant; $m=(\#1\text{s}-\#B-d)/2$ is invariant; $s_0$ is untouched. So $(s_0,w,d,m)$ is conserved and only $q$ moves. (Trailing $D$ can never move: $110$ needs a zero after two 1s, absent at the end; $011$ before a lone final $1$ is impossible.)

## 3. Transition correspondence (exhaustive local cases)

Every physical rewrite is identified by the zero that moves. Let the zero be at bond position $p$.

(i) $011\to110$ at $(p,p+1,p+2)$: zero followed by run of length $r\ge2$, whose first token is $A$. If the zero is $C$: $CA\to AC$ ($011\to110$). If the zero is the tail of $B$: $BA=1011\to1110=AB$ (triple $(p,p+1,p+2)$, i.e. the last three bits). Right-hand run becomes $r-2\ge0$, same parity ($A^{a'}X\to A^{a'-1}X$).

(ii) $110\to011$ at $(p-2,p-1,p)$: zero preceded by run of length $r\ge2$. If $r$ even, zero is $C$ and $(p-2,p-1)$ is the last $A$: $AC\to CA$. If $r$ odd, zero is in $B=(p-1,p)$ and the last $A$ is $(p-3,p-2)$: $AB=1110\to1011=BA$ on triple $(p-2,p-1,p)$. Left run becomes $r-2$, same parity.

(iii) Non-transitions agree: in $q$, $10\to01$ needs an $A$ immediately before the zero-token, physically two 1s before the zero ($a\ge1$ in $A^aB$ or $A^aC$); $B$ alone ("010"/"10" at start), $C$ followed by $B$, $C$, or $D$, give no $011/110$, matching $q$ patterns $00$ or $0$ at the end.

Completeness: every $011$/$110$ triple is case (i)/(ii). Uniqueness: the physical triple is a function of the zero's position and direction; the zero corresponds to a unique $0$ in $q$; direction gives left/right hop. So **each adjacent $10\leftrightarrow01$ in $q$ corresponds to exactly one physical triple, and vice versa.** Boundary of the string: a zero at position $0$ has empty left run, hence is $C$; case (i) applies with the triple $(0,1,2)$. Empty ($m=0$) and full ($h=0$, string $1^{2m}D^d$) blocks have no transitions, consistent with $\binom{\ell}{0}=\binom{\ell}{\ell}=1$ and energy $0$ (also $\sum_{k=1}^{\ell}\cos\frac{\pi k}{\ell+1}=0$).

## 4. Amplitudes and conjugacy

By §0 every matrix element is $-\tfrac12$ with no diagonal terms, no boundary terms, no phases. Hence the block of $H_N$ on a fixed label is, up to the permutation of §1, the adjacency operator $\times(-\tfrac12)$ of adjacent hard-core hops on $\{0,1\}^\ell$ with $m$ ones, which is exactly $H_{\rm free}=-\tfrac14\sum_{r=1}^{\ell-1}(X_rX_{r+1}+Y_rY_{r+1})$ in its $m$-particle sector (check: $-\tfrac14\cdot2=-\tfrac12$). On an open path, Jordan–Wigner carries no boundary sign, so the block is $m$ free fermions with one-body tridiagonal hopping $-\tfrac12$, spectrum $-\cos\frac{\pi k}{\ell+1}$. The conjugating map is a label-dependent permutation of computational-basis states. Consistency with the source: for $s_0=s_{N+1}=0$, $M=m$, $D=\#B+d$ gives $\ell=N+1-M-D=N_0$; this is a control, not an input to the proof.

## 5. Finite controls (not proof)

Hand checks at $N=2,3,4$ (e.g. $00100$: path of 3, spectrum $0,\pm1/\sqrt2$; $0\,1110$: $CAB$–$ACB$–$CBA$ path of 3; $0101$: $AD$, energy $0$ since $s_0\ne s_3$) agree with §3–4.

## 6. Residual obligations and falsifiers (outside the lemma)

Not established here: reversible parse/encode and its clean uncompute; label-controlled sine-transform Gaussian unitary on variable $\ell$ with padding; fermionic phase gadget precision; total gate count. **Falsifiers for the lemma** would be: a bond pair related by $011\leftrightarrow110$ whose parses differ by other than one adjacent $A\leftrightarrow B/C$ swap; a block with a diagonal or non-$(-\tfrac12)$ entry; two physical triples realizing one $q$-hop. §0–§3 exclude all three for every $N\ge2$.