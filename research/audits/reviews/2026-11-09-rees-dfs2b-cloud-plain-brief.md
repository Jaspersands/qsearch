# Cloud brief (9 Nov 2026): plain-mode dfs2b cross-checks, shards S1-S3

AI-only compute job. Each cloud session runs ONE shard and reports its result lines in its
final message; the owner's main session copies them back. Plain mode re-runs the unpruned
search for primes already found to be members of E_2(K) (expected INFEASIBLE); any FEASIBLE,
BUG or LIMIT line is a contradiction and must be reported prominently.

**Rules**
- No git commit, push, branch, PR, upload, email or post. Read the repository only.
- Do not edit the C source. Work in `~/dfs2b-run`.
- Stop by 5 h 30 min wall clock (the runner below enforces it) and report whatever finished.
- Spend few tokens: start the run in the background, check rarely.

## 1. Compile and check

```sh
mkdir -p ~/dfs2b-run/out && cd ~/dfs2b-run
cp "$REPO/research/audits/reviews/2026-11-02-rees-schedules/small-prime/dfs2b.c" .   # REPO = the repo checkout
md5sum dfs2b.c        # must be 26407094f71ccb5366c3fe3a4d41e395 (full commented source)
cc -O2 -o dfs2b dfs2b.c
```

## 2. Test vectors (ignore `secs=`; every other value must match, else stop and report)

- `./dfs2b 8 2473 2521 4000000000 plain` -> `INFEASIBLE k=8 p=2473 nodes=200138`,
  `INFEASIBLE k=8 p=2521 nodes=209412`, `DONE ... feasible=0 infeasible=2 limit=0 mode=plain`.
- `./dfs2b 9 3637 3637 4000000000 plain` -> `INFEASIBLE k=9 p=3637 nodes=244064`.
- `./dfs2b 8 3089 3089 4000000000 print` -> `FEASIBLE k=8 p=3089 g=3 nodes=60394 ...
  beta=0,3088,2976,321,1,91,538,1304 alpha=1,113,2768,2215,614,2185,1785,2466`.
- `./dfs2b 9 6067 6067 4000000000 print` -> `INFEASIBLE k=9 p=6067 nodes=318496`.

## 3. Shards (one line per job: K P), run in this order

- **S1:** `9 13807`, `9 14149`, then K=8: 7649 7673 7681 7753 7817 7873 7937 7993 8009 8017
  8081 8089 8209 8233 8297 8329
- **S2:** K=8: 8353 8377 8513 8537 8641 8681 8713 8761 8969 9001 9041 9049 9209 9241 9257 9433
- **S3:** K=8: 9473 9689 9721 9769 9817 9833 9857 9929 10009 10169 10321 10457 10601 10729 10753

Write your shard's lines to `queue.txt` as `K P` pairs, one per line.

## 4. Runner

```sh
cat > run.sh <<'SH'
#!/bin/bash
cd ~/dfs2b-run
N=$(getconf _NPROCESSORS_ONLN)
one() { k=$1; p=$2; f=out/${k}_${p}_plain.out
  grep -q '^DONE' "$f" 2>/dev/null && return
  ./dfs2b $k $p $p 1000000000000000 plain print > "$f" 2>&1; }
export -f one
timeout 19800 xargs -P "$N" -L 1 bash -c 'one "$@"' _ < queue.txt
echo FINISHED > out/FINISHED
SH
chmod +x run.sh; nohup ./run.sh > run.log 2>&1 &
```

## 5. Report (final message)

Machine: `getconf _NPROCESSORS_ONLN`, CPU model, OS; md5; test-vector result. Then, verbatim:

```sh
grep -hE '^(INFEASIBLE|FEASIBLE|LIMIT|BUG|DONE)' out/*.out | sort -t= -k3 -n
```

and the list of shard jobs with no DONE line (unfinished). Put any FEASIBLE/BUG/LIMIT first.
