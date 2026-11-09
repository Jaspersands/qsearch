# Brief for Claude on the other machine: dfs2b runs for E_2(9) and cross-checks

Copy this whole file to the other machine and tell Claude: "Follow this brief exactly."

---

You are running a long, pure-compute job for a research paper. The job decides whether
certain primes belong to the exceptional sets E_2(8) and E_2(9). You only compile and run
a C program that is given below, and collect its output.

**Rules**
- Do not use git, push, upload, email, or post anything. Work only in `~/dfs2b-run`.
- Results go into files that the owner copies back by hand.
- Do not edit the C source.
- Spend few tokens. Start the run once in the background and check on it rarely, at
  most every 1-2 hours.
- There is no deadline. Some jobs take many hours. Never kill a running `dfs2b`.
- Needs macOS or Linux (64-bit, where `long` is 64 bits), or WSL on Windows.
  Native Windows will not work.

## 1. Set up and compile

```sh
mkdir -p ~/dfs2b-run/out && cd ~/dfs2b-run
# write the source at the end of this brief, verbatim, to dfs2b.c
cc -O2 -o dfs2b dfs2b.c      # or gcc -O2 -o dfs2b dfs2b.c
md5sum dfs2b.c 2>/dev/null || md5 -q dfs2b.c
```

The md5 of `dfs2b.c` must be `244a31ed79c5cb95b294a35c75cc0137`. If it differs, the paste
changed the file (for example a trailing newline or tab). Fix the file so it matches; do
not change the code.

## 2. Test vectors

Every value must match exactly. Ignore the `secs=` field.

- `./dfs2b 8 2473 2521 4000000000 plain` prints `INFEASIBLE k=8 p=2473 nodes=200138`,
  then `INFEASIBLE k=8 p=2521 nodes=209412`, then
  `DONE ... feasible=0 infeasible=2 limit=0 mode=plain`.
- `./dfs2b 9 3637 3637 4000000000 plain` prints `INFEASIBLE k=9 p=3637 nodes=244064`.
- `./dfs2b 8 3089 3089 4000000000 print` prints
  `FEASIBLE k=8 p=3089 g=3 nodes=60394 ... beta=0,3088,2976,321,1,91,538,1304 alpha=1,113,2768,2215,614,2185,1785,2466`.
- `./dfs2b 9 6067 6067 4000000000 print` prints `INFEASIBLE k=9 p=6067 nodes=318496`.

If anything differs, stop and report the mismatch.

## 3. The queue (one job per line: K P MODE), in this exact order

`MODE` is `print` (the normal pruned search) or `plain` (the unpruned cross-check).
Write `queue.txt` with the script below. Do not reorder it: earlier jobs matter more.

```sh
cd ~/dfs2b-run
{
# Phase 2: kappa=9 exception primes in (20000, 25000] still undecided. 58 jobs, ~3 h
# (at 21313) rising to ~8 h (at 25000) each.
for p in 21313 21493 21529 21601 21673 21727 21799 21817 21871 21943 21961 21997 22051 \
  22159 22303 22447 22483 22501 22573 22699 22717 22807 23041 23059 23131 23167 23203 \
  23293 23311 23473 23509 23563 23581 23671 23689 23743 23761 23833 23869 23887 23977 \
  24049 24103 24121 24229 24247 24337 24373 24391 24481 24499 24517 24697 24733 24841 \
  24859 24877 24967; do echo "9 $p print"; done
# Phase 3a: plain-mode cross-check of kappa=8 members (expected INFEASIBLE). 47 jobs, ~1 h each.
for p in 7649 7673 7681 7753 7817 7873 7937 7993 8009 8017 8081 8089 8209 8233 8297 8329 \
  8353 8377 8513 8537 8641 8681 8713 8761 8969 9001 9041 9049 9209 9241 9257 9433 9473 \
  9689 9721 9769 9817 9833 9857 9929 10009 10169 10321 10457 10601 10729 10753; do echo "8 $p plain"; done
# Phase 3b: plain-mode cross-check of kappa=9 members (expected INFEASIBLE). 38 jobs, ~1.5-3 h each.
for p in 11701 11719 11827 12007 12043 12097 12241 12277 12421 12457 12511 12547 12583 \
  12601 12619 12637 12763 12781 12799 12853 12889 12907 13033 13159 13177 13249 13267 \
  13339 13411 13537 13591 13627 13681 13789 13807 13879 13933 14149; do echo "9 $p plain"; done
} > queue.txt
wc -l queue.txt    # must be 143
```

## 4. Runner (resumable, no time limit)

```sh
cat > run.sh <<'SH'
#!/bin/bash
cd ~/dfs2b-run
N=${JOBS:-$(getconf _NPROCESSORS_ONLN)}
one() { k=$1; p=$2; m=$3; f=out/${k}_${p}_${m}.out
  grep -q '^DONE' "$f" 2>/dev/null && return      # finished earlier: skip
  if [ "$m" = plain ]; then ./dfs2b $k $p $p 1000000000000000 plain print > "$f" 2>&1
  else ./dfs2b $k $p $p 1000000000000000 print > "$f" 2>&1; fi; }
export -f one
xargs -P "$N" -L 1 bash -c 'one "$@"' _ < queue.txt
echo ALL_DONE > out/ALL_DONE
SH
chmod +x run.sh
nohup nice -n 10 ./run.sh > run.log 2>&1 &
```

- By default it uses every core. To leave cores free, start it as `JOBS=6 nohup nice -n 10 ./run.sh ...`.
- The node limit of 10^15 means no job ends with LIMIT; jobs just take as long as they take.
- If the machine reboots or the run stops, start the same command again. Jobs with a
  `DONE` line are skipped. A job that was cut off restarts from scratch.
- Record `getconf _NPROCESSORS_ONLN`, the CPU model, and the OS. Use
  `sysctl -n machdep.cpu.brand_string` on a Mac, or `lscpu | grep 'Model name'` on Linux.

## 5. Results to hand back

Whenever the owner asks, and when `out/ALL_DONE` exists:

```sh
cd ~/dfs2b-run
cat out/*.out | grep -E '^(INFEASIBLE|FEASIBLE|LIMIT|DONE|BUG)' | sort -t= -k3 -n > results.txt
tar czf dfs2b-results-$(date +%Y%m%d-%H%M).tgz out results.txt queue.txt run.log
```

Then write `RESULTS.md` with:
- the machine (cores, CPU model, OS) and the test-vector results;
- per phase (phase 1 was dropped: the main machine finished it): jobs finished, how many INFEASIBLE and how many FEASIBLE, and jobs still running;
- **prominently**, any FEASIBLE line in phase 3 (a contradiction), any BUG line, and any
  job whose output has no DONE line;
- for phase 2, the largest P such that every phase-2 prime ≤ P has finished.

The owner copies `dfs2b-results-*.tgz` and `RESULTS.md` back to the main machine.
Partial results are useful: hand them back at any time without stopping the run.

## Background (for your understanding only)

- `INFEASIBLE` means p is in E_2(K) (no two-level contraction exists).
- `FEASIBLE` means p is not in E_2(K), and the line carries a witness (g, beta, alpha) that
  the owner re-verifies independently.
- `plain` mode drops both pruning rules. It reproduces the unpruned search tree exactly, so it
  independently checks the pruning proofs. It is about 10× slower.
- Cost grows roughly like p^5.6, so primes above ~25000 take more than a day each and are
  deliberately not in the queue.

## Source: dfs2b.c (comment-stripped; md5 244a31ed79c5cb95b294a35c75cc0137)

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef uint64_t u64;
typedef uint32_t u32;
static u64 P, K, W;
static unsigned char *idx;
static u32 *inv;
static u64 **D;
static u64 *S;
static u32 *cands;
static u32 *tmplist, *xs;
static u64 *E, *T;
static long nodes, limit;
static u64 beta[64], V;
static int assigned[64];
static int opt_plain = 0, opt_sym = 1, opt_fc = 1, opt_print = 0;
static long unexpected_empty = 0;
static inline u64 mulm(u64 a, u64 b) { return a * b % P; }
static u64 powm(u64 a, u64 e) { u64 r = 1; a %= P; while (e) { if (e & 1) r = mulm(r, a); a = mulm(a, a); e >>= 1; } return r; }
static u64 primroot(u64 p) {
    u64 n = p - 1, f[64]; int nf = 0;
    for (u64 q = 2; q * q <= n; q++) if (n % q == 0) { f[nf++] = q; while (n % q == 0) n /= q; }
    if (n > 1) f[nf++] = n;
    for (u64 g = 2;; g++) { int ok = 1; for (int i = 0; i < nf; i++) if (powm(g, (p - 1) / f[i]) == 1) { ok = 0; break; } if (ok) return g; }
}
static inline long md(long m) { m %= (long)K; if (m < 0) m += K; return m; }
static inline int inA(u64 y, long m) { return y == 0 || idx[y] == (unsigned char)md(m); }
static inline u64 *SET(long level, long j) { return S + ((u64)level * K + (u64)j) * W; }
static inline void extract(u64 *out, const u64 *d, u64 off) {
    for (u64 w = 0; w < W; w++) {
        u64 pos = off + 64 * w, q = pos >> 6, r = pos & 63;
        u64 v = d[q] >> r;
        if (r) v |= d[q + 1] << (64 - r);
        out[w] = v;
    }
    if (P & 63) out[W - 1] &= (1ULL << (P & 63)) - 1;
}
static inline int and_rot(u64 *out, const u64 *in, long m, u64 b) {
    const u64 *d = D[md(m)];
    u64 any = 0;
    for (u64 w = 0; w < W; w++) {
        u64 pos = b + 64 * w, q = pos >> 6, r = pos & 63;
        u64 v = d[q] >> r;
        if (r) v |= d[q + 1] << (64 - r);
        if (w == W - 1 && (P & 63)) v &= (1ULL << (P & 63)) - 1;
        out[w] = in[w] & v;
        any |= out[w];
    }
    return any != 0;
}
static inline u64 popc(const u64 *a) { u64 n = 0; for (u64 w = 0; w < W; w++) n += (u64)__builtin_popcountll(a[w]); return n; }
static inline u64 listof(const u64 *a, u32 *out) {
    u64 n = 0;
    for (u64 w = 0; w < W; w++) { u64 x = a[w]; while (x) { out[n++] = (u32)(64 * w + (u64)__builtin_ctzll(x)); x &= x - 1; } }
    return n;
}
static inline void clearbit(u64 *a, u64 x) { a[x >> 6] &= ~(1ULL << (x & 63)); }
static u64 compute_candidates(long level, long r, u32 *out) {
    extract(E, D[md(-r)], 1);
    long order[64]; u64 cnt[64];
    long nj = 0;
    for (long j = 1; j < (long)K; j++) { order[nj] = j; cnt[nj] = popc(SET(level, j)); nj++; }
    for (long a = 1; a < nj; a++) {
        long oj = order[a]; u64 oc = cnt[a]; long b = a - 1;
        while (b >= 0 && cnt[b] > oc) { order[b + 1] = order[b]; cnt[b + 1] = cnt[b]; b--; }
        order[b + 1] = oj; cnt[b + 1] = oc;
    }
    int lookup = 0;
    u64 ne = popc(E);
    for (long a = 0; a < nj; a++) {
        long j = order[a], m = md(-(r + j));
        const u64 *Sj = SET(level, j);
        u64 cj = cnt[a];
        if (!lookup) {
            if (ne == 0) return 0;
            u64 small = cj < 2 * K ? cj : 2 * K;
            if (ne * small <= cj * W) lookup = 1;
            else {
                u64 nx = listof(Sj, xs);
                memset(T, 0, W * sizeof(u64));
                for (u64 q = 0; q < nx; q++) {
                    u64 x = xs[q];
                    const u64 *d = D[m];
                    for (u64 w = 0; w < W; w++) {
                        u64 pos = x + 64 * w, qq = pos >> 6, rr = pos & 63;
                        u64 v = d[qq] >> rr;
                        if (rr) v |= d[qq + 1] << (64 - rr);
                        T[w] |= v;
                    }
                }
                if (P & 63) T[W - 1] &= (1ULL << (P & 63)) - 1;
                for (u64 w = 0; w < W; w++) E[w] &= T[w];
                ne = popc(E);
                continue;
            }
        }
        u64 nx = listof(Sj, xs);
        for (u64 w = 0; w < W; w++) {
            u64 word = E[w];
            while (word) {
                u64 b = 64 * w + (u64)__builtin_ctzll(word); word &= word - 1;
                u64 q;
                for (q = 0; q < nx; q++) { u64 v = xs[q] + b; if (v >= P) v -= P; if (inA(v, m)) break; }
                if (q == nx) E[w] &= ~(1ULL << (b & 63));
            }
        }
    }
    u64 n = listof(E, out);
    if (opt_sym && !opt_plain && assigned[1] && V != 0) {
        u64 k = 0;
        long rm = md(r - 1), rp = md(r + 1);
        for (u64 q = 0; q < n; q++) {
            u64 b = out[q], c = b + 1; if (c >= P) c -= P;
            if (c == 0) continue;
            if (assigned[rm]) { u64 cm = beta[rm] + 1; if (cm >= P) cm -= P; if (mulm(c, inv[cm]) < V) continue; }
            if (assigned[rp]) { u64 cp = beta[rp] + 1; if (cp >= P) cp -= P; if (mulm(cp, inv[c]) < V) continue; }
            out[k++] = b;
        }
        n = k;
    }
    return n;
}
static void filt_row(long level, long s) {
    u64 bs = beta[s], z = (P - bs) % P, cs = bs + 1; if (cs >= P) cs -= P;
    for (long t = 1; t < (long)K; t++) clearbit(SET(level, t), z);
    u64 *S1 = SET(level, 1);
    u64 nx = listof(S1, xs);
    for (u64 q = 0; q < nx; q++) {
        u64 x = xs[q], v = x + bs; if (v >= P) v -= P;
        if (mulm(v, inv[cs]) < V) clearbit(S1, x);
    }
}
static void filt_pair(long level, long s) {
    long s1 = md(s + 1);
    u64 bs = beta[s], bs1 = beta[s1];
    for (long t = 1; t < (long)K; t++) {
        u64 *St = SET(level, t);
        u64 nx = listof(St, xs);
        for (u64 q = 0; q < nx; q++) {
            u64 x = xs[q], lo = x + bs, hi = x + bs1;
            if (lo >= P) lo -= P;
            if (hi >= P) hi -= P;
            if (lo == 0) { clearbit(St, x); continue; }
            if (mulm(hi, inv[lo]) < V) clearbit(St, x);
        }
    }
}
static int dfs(long level) {
    if (level == (long)K - 1) return 1;
    if (++nodes > limit) return -1;
    long best = -1; u64 bestn = 0;
    u32 *cl = cands + (u64)level * (P + 1);
    if (level == 0 || opt_plain || !opt_fc) {
        for (long r = 1; r < (long)K; r++) if (!assigned[r]) { best = r; break; }
        bestn = compute_candidates(level, best, cl);
        if (bestn == 0) return 0;
    } else {
        for (long r = 1; r < (long)K; r++) {
            if (assigned[r]) continue;
            u64 n = compute_candidates(level, r, tmplist);
            if (n == 0) return 0;
            if (best < 0 || n < bestn) { best = r; bestn = n; memcpy(cl, tmplist, n * sizeof(u32)); }
        }
    }
    for (u64 q = 0; q < bestn; q++) {
        u64 b = cl[q];
        beta[best] = b;
        int ok = 1;
        for (long j = 1; j < (long)K && ok; j++) ok = and_rot(SET(level + 1, j), SET(level, j), -(best + j), b);
        if (!ok) { unexpected_empty++; continue; }
        assigned[best] = 1;
        if (best == 1) { V = b + 1; if (V >= P) V -= P; }
        if (opt_sym && !opt_plain && V != 0) {
            filt_row(level + 1, best);
            if (level == 0) filt_row(level + 1, 0);
            long bm = md(best - 1), bp = md(best + 1);
            if (assigned[bm]) filt_pair(level + 1, bm);
            if (assigned[bp]) filt_pair(level + 1, best);
            for (long t = 1; t < (long)K && ok; t++) ok = popc(SET(level + 1, t)) != 0;
        }
        int r = ok ? dfs(level + 1) : 0;
        assigned[best] = 0;
        if (r) return r;
    }
    return 0;
}
static double now(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec + 1e-9 * ts.tv_nsec; }
int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: dfs2b K P0 P1 node_limit [plain] [nosym] [nofc] [print]\n"); return 1; }
    K = strtoull(argv[1], 0, 10);
    u64 P0 = strtoull(argv[2], 0, 10), P1 = strtoull(argv[3], 0, 10);
    limit = atol(argv[4]);
    for (int a = 5; a < argc; a++) {
        if (!strcmp(argv[a], "plain")) opt_plain = 1;
        else if (!strcmp(argv[a], "nosym")) opt_sym = 0;
        else if (!strcmp(argv[a], "nofc")) opt_fc = 0;
        else if (!strcmp(argv[a], "print")) opt_print = 1;
        else { fprintf(stderr, "unknown flag %s\n", argv[a]); return 1; }
    }
    if (K < 2 || K > 62 || P1 >= (1ULL << 32)) { fprintf(stderr, "bad K or P1\n"); return 1; }
    char *comp = calloc(P1 + 1, 1);
    for (u64 i = 2; i * i <= P1; i++) if (!comp[i]) for (u64 j = i * i; j <= P1; j += i) comp[j] = 1;
    idx = malloc(P1 + 1);
    inv = malloc((P1 + 1) * sizeof(u32));
    u64 Wmax = (P1 >> 6) + 2;
    D = malloc(K * sizeof(u64 *));
    for (u64 m = 0; m < K; m++) D[m] = malloc((2 * Wmax + 2) * sizeof(u64));
    S = malloc((K + 1) * K * Wmax * sizeof(u64));
    cands = malloc((K + 1) * (P1 + 2) * sizeof(u32));
    tmplist = malloc((P1 + 2) * sizeof(u32));
    xs = malloc((P1 + 2) * sizeof(u32));
    E = malloc(Wmax * sizeof(u64)); T = malloc(Wmax * sizeof(u64));
    long nf = 0, ni = 0, nl = 0;
    for (u64 p = (P0 < 3 ? 3 : P0); p <= P1; p++) {
        if (comp[p] || (p - 1) % K) continue;
        double t0 = now();
        P = p; W = (p >> 6) + 1;
        u64 g = primroot(p), x = 1;
        idx[0] = 255;
        for (u64 e = 0; e < p - 1; e++) { idx[x] = (unsigned char)(e % K); x = mulm(x, g); }
        inv[1] = 1;
        for (u64 i = 2; i < p; i++) inv[i] = (u32)((p - (p / i) * (u64)inv[p % i] % p) % p);
        for (u64 m = 0; m < K; m++) {
            memset(D[m], 0, (2 * W + 2) * sizeof(u64));
            for (u64 y = 0; y < 2 * p; y++) {
                u64 yy = y % p;
                if (yy == 0 || idx[yy] == m) D[m][y >> 6] |= 1ULL << (y & 63);
            }
        }
        for (u64 j = 1; j < K; j++) {
            u64 m = md(-(long)j);
            memcpy(SET(0, j), D[m], W * sizeof(u64));
            if (P & 63) SET(0, j)[W - 1] &= (1ULL << (P & 63)) - 1;
        }
        memset(assigned, 0, sizeof assigned); assigned[0] = 1;
        nodes = 0; beta[0] = 0; V = 0; unexpected_empty = 0;
        int r = dfs(0);
        double dt = now() - t0;
        if (r == 1) {
            u64 alpha[64]; alpha[0] = 1;
            for (u64 j = 1; j < K; j++) {
                u64 n = listof(SET((long)K - 1, (long)j), xs);
                if (n == 0) { printf("BUG p=%llu empty S_%llu at leaf\n", (unsigned long long)p, (unsigned long long)j); return 2; }
                alpha[j] = xs[0];
            }
            if ((alpha[0] + beta[0]) % P == 0) { printf("BUG0 p=%llu\n", (unsigned long long)p); return 2; }
            for (u64 i = 0; i < K; i++) for (u64 j = 0; j < K; j++)
                if (!inA((alpha[j] + beta[i]) % P, -(long)(i + j))) { printf("BUG2 p=%llu\n", (unsigned long long)p); return 2; }
            nf++;
            if (opt_print) {
                printf("FEASIBLE k=%llu p=%llu g=%llu nodes=%ld secs=%.3f beta=", (unsigned long long)K, (unsigned long long)p, (unsigned long long)g, nodes, dt);
                for (u64 i = 0; i < K; i++) printf("%llu%s", (unsigned long long)beta[i], i + 1 < K ? "," : "");
                printf(" alpha=");
                for (u64 j = 0; j < K; j++) printf("%llu%s", (unsigned long long)alpha[j], j + 1 < K ? "," : "");
                printf("\n");
            }
        } else if (r == 0) {
            ni++;
            printf("INFEASIBLE k=%llu p=%llu nodes=%ld secs=%.3f%s\n", (unsigned long long)K, (unsigned long long)p, nodes, dt,
                   unexpected_empty ? " UNEXPECTED_EMPTY" : "");
        } else { nl++; printf("LIMIT k=%llu p=%llu nodes=%ld secs=%.3f\n", (unsigned long long)K, (unsigned long long)p, nodes, dt); }
        fflush(stdout);
    }
    printf("DONE k=%llu range=[%llu,%llu] feasible=%ld infeasible=%ld limit=%ld mode=%s%s%s\n",
           (unsigned long long)K, (unsigned long long)P0, (unsigned long long)P1, nf, ni, nl,
           opt_plain ? "plain" : "full", (!opt_plain && !opt_sym) ? "+nosym" : "", (!opt_plain && !opt_fc) ? "+nofc" : "");
    return 0;
}
```
