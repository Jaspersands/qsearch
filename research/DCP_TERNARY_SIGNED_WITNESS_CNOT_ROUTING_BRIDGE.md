# DCP Ternary Signed-Support Witness Extraction and CNOT-Syndrome Routing Bridge

## 1. Bijection Between Signed Ternary Witnesses and CNOT Syndrome Branches
For any ternary witness $\delta \in \{-1, 0, +1\}^K \setminus \{0^K\}$ with support $S = \{r_0 < r_1 < \dots < r_{w-1}\}$ and $\delta_{r_0} = +1$, the $w$-wire CNOT star on $S$ realizes $\tilde{A}(S, d) \equiv A\delta \pmod q$ on the unique canonical syndrome branch $d^*(\delta)_j = (1 - \delta_{r_j})/2 \in \{0, 1\}$ with Born probability $2^{-(w-1)}$.

## 2. Pigeonhole Threshold Separation ($2^K > q^n$)
Whenever $2^K > q^n$, Pigeonhole Principle on $\{0, 1\}^K$ guarantees at least one non-trivial ternary zero-sum witness $\delta = x - y \in \{-1, 0, +1\}^K \setminus \{0^K\}$ with $A\delta \equiv 0 \pmod q$, even on instances where the binary zero-sum witness set $\{v \in \{0, 1\}^K \setminus \{0^K\} : A v \equiv 0 \pmod q\}$ is empty.
