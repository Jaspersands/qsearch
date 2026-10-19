# Quantum-advantage claim checker

Reads an abstract and flags the caveats that most often turn an advantage claim into a
negative result. Each flag quotes the sentence that raised it and maps to a failure mode
from `tools/audit/failure_modes.py`. The report also lists the nearest Q-Search negatives
and their lessons.

```bash
python tools/claim_checker/check.py 0811.3171                 # fetch from arXiv (paced, cached)
python tools/claim_checker/check.py 2408.08292 quant-ph/9508027
python tools/claim_checker/check.py --file abstract.txt --json
python tools/claim_checker/check.py --text "..." --no-corpus
```

| Flag | Raised by | Failure mode |
|---|---|---|
| `input_loading` | QRAM, data structures, copies of a state, block encodings; or a polylog or sqrt(N) runtime on classical data | state preparation |
| `readout` | Output is an expectation value, an estimate, a sample or a quantum state | readout |
| `oracle_model` | Oracle, black-box or query-model separation | hidden advice |
| `heuristic_assumption` | Correctness or hardness rests on a conjecture or heuristic | proof gap |
| `numerical_only` | Simulations, empirical results, a constructed instance | finite-size |
| `restricted_baseline` | Compared only with generic heuristics, or concedes a tailored classical solver wins | classical competitor |
| `parameter_dependence` | Condition number, sparsity, rank, gap or precision | resource blow-up |

The checker reads the abstract only, and only in English. A missing flag means the
abstract does not raise the issue, not that the paper is clear of it. It assumes the text
makes a quantum claim: a classical paper that mentions a data structure or precision still
gets flags.

**Ruled-out caveats.** A match counts as ruled out when a negation comes within six words
before it in the same clause ("does not require QRAM", "not an oracle separation",
"without relying on any conjecture", "independent of the condition number"), or "-free"
follows it ("oracle-free"). The negation carries along a list ("independent of the
condition number, sparsity and precision"). Ruled-out caveats are listed in their own
section with their quote, not dropped: "Without QRAM the speedup disappears" also counts
as ruled out, so read the quote. A plain mention elsewhere in the abstract still raises
the flag.

## Checks

Expected flags for ten well-known papers were written down before the rules were run.
Each paper has flags that must fire and flags that must not, from consensus caveats in
the literature. The fixtures are recorded arXiv abstracts, so the tests run offline.

| Set | Papers | Result |
|---|---|---|
| Development | Shor, Regev factoring, DQI, HHL, quantum recommendation systems, glued-trees walk | 6 of 6 |
| Held out until the rules were frozen | QPCA, Grover, shallow circuits (Bravyi-Gosset-König), Yamakawa-Zhandry | 3 of 4 |

The held-out miss was "a non-oracular version" firing the oracle flag. The checker now
recognises that form, and the paper is a regression test. Twelve sentences that rule a
caveat out, and one that negates a caveat in an earlier clause only, are regression
tests too. A planned LLM extraction pass that quotes the full paper was not built. The
rule layer plus the corpus lookup is the tool.
