/* dfs2r.c -- RANDOMIZED-RESTART variant of dfs2b.c (round 5, 2026-11-04): flag 'rand R S'
 * shuffles every candidate list and restarts up to R times (seed S) with the node limit
 * per restart; it then only ever reports FEASIBLE (witness re-checked) or LIMIT, never
 * INFEASIBLE.  Use with nosym.  Original header follows.
 * dfs2b.c -- complete DFS for the universal two-level contraction, with
 * sound pruning.  SAME DECISION PROBLEM AS dfs2.c (this folder):
 *
 *   p prime, p = 1 (mod K).  A_m = Q_m U {0}, Q_m = {y != 0 : log_g(y) = m (mod K)}.
 *   Decide whether alpha, beta in F_p^K exist with alpha_0 = 1, beta_0 = 0 and
 *   alpha_j + beta_i in A_{-(i+j)} for all i, j in Z_K.
 *   (The general form alpha_0 + beta_0 != 0 of the notes normalises to this by
 *   translating beta_0 to 0 and scaling by (alpha_0 + beta_0)^{-1} in H = Q_0.)
 *
 * Output per prime, same format as dfs2: INFEASIBLE (search complete; also
 * prints nodes and seconds), LIMIT (node budget exhausted; no conclusion),
 * FEASIBLE (printed only with the "print" flag; the witness is re-checked on all
 * K^2 cells against the ORIGINAL definition before being counted).
 *
 * Build: cc -O2 -o dfs2b dfs2b.c
 * Usage: ./dfs2b K P0 P1 node_limit [plain] [nosym] [nofc] [print]
 *   plain : static row order 1..K-1, no forward checking, no symmetry breaking.
 *           This explores exactly dfs2's tree (same node counts on INFEASIBLE
 *           primes) and serves as the independent cross-check mode.
 *   nosym : keep forward checking and MRV, drop the symmetry prune.
 *   nofc  : no forward checking over the other rows (only the branching row).
 *
 * ---------------------------------------------------------------------------
 * Terminology.  M_{ij} = alpha_j + beta_i is the "sum matrix", indexed by Z_K
 * (the constraint depends on i+j mod K only).  Column 0 is c_i = M_{i0} =
 * 1 + beta_i in A_{-i} with c_0 = 1.  The DFS assigns rows (beta_i) and keeps,
 * for each column j >= 1, the set S_j of alpha_j values compatible with every
 * assigned row:  S_j = A_{-j}  cap_i (A_{-(i+j)} - beta_i).  A leaf (all rows
 * assigned, all S_j nonempty) is a solution: pick any alpha_j in S_j.
 *
 * PRUNE 1 (row viability / forward checking / most-constrained row first).
 *   A value b for an unassigned row r is viable iff 1 + b in A_{-r} and, for
 *   every j >= 1, S_j cap (A_{-(r+j)} - b) is nonempty.  Soundness: these are
 *   exactly the conditions dfs2 tests before descending, and every completed
 *   solution extending the current partial assignment satisfies them, so a
 *   row with no viable value proves the node dead, and restricting the branch
 *   to viable values loses nothing.  Rows may be assigned in any order
 *   (the constraints are symmetric across rows, the search over the remaining
 *   rows is still exhaustive), so we branch on the row with the fewest viable
 *   values.  The viable set is computed as a bitset intersection of the
 *   "difference sets" A_m - S_j = U_{x in S_j} (A_m - x) (cost |S_j| words
 *   times W) or, when the running intersection is already small, by direct
 *   table look-ups; both compute the same set.
 *
 * PRUNE 2 (symmetry breaking: a canonical corner).  Let M be a normalised
 *   solution.  For every cell (s,t) with M_{st} != 0 the recentred matrix
 *       M'_{ij} = M_{i+s, j+t} / M_{st}
 *   is again a normalised solution:  it is a sum matrix (alpha'_j =
 *   (alpha_{j+t} + beta_s)/M_{st}, beta'_i = (beta_{i+s} - beta_s)/M_{st}),
 *   M'_{00} = 1, and M'_{ij} lies in M_{st}^{-1} A_{-(i+s+j+t)} = A_{-(i+j)}
 *   because M_{st} in Q_{-(s+t)} and Q_a Q_b = Q_{a+b}.  The transpose M^T
 *   is also a normalised solution (alpha' = 1 + beta, beta' = alpha - 1).
 *   Define the ratio set
 *       R(M) = { M_{s+1,t} / M_{s,t} : M_{st} != 0 }  U  { M_{s,t+1} / M_{s,t} : M_{st} != 0 }
 *   (vertical and horizontal ratios, values in F_p read as integers in [0,p)).
 *   Recentring at (s,t) and transposing permute the cells, so R(M') = R(M)
 *   and R(M^T) = R(M).  Pick the cell (s*,t*) (possibly after transposing)
 *   achieving min R(M); recentring there gives a normalised solution M* with
 *   c*_1 = M*_{10}/M*_{00} = min R(M*).  Hence:
 *       the problem is feasible  iff  a normalised solution M exists with
 *       c_1 = 1 + beta_1 = min R(M).
 *   The search is therefore restricted to such M ("canonical"), i.e. with
 *   v := c_1 every ratio in R(M) is >= v.  We only enforce the subset of these
 *   necessary conditions that is decidable from the current partial
 *   assignment (enforcing fewer conditions is still sound):
 *   (2a) rows: for consecutive assigned rows s, s+1 (mod K) with c_s != 0,
 *        c_{s+1} / c_s >= v  (these are the ratios in column 0);
 *   (2b) columns: for consecutive assigned rows s, s+1 and any x in S_t,
 *        x survives only if x + beta_s = 0 or (x + beta_{s+1})/(x + beta_s) >= v
 *        (ratio of cells (s+1,t) and (s,t) when alpha_t = x);
 *   (2c) column pair (0,1) in row s: x in S_1 survives only if
 *        (x + beta_s)/c_s >= v  (c_s != 0);
 *   (2d) zeros: if v != 0 then M has NO zero cell.  Proof: all beta_i are
 *        distinct in a normalised solution (equal rows i != i' would be zero
 *        rows, since A_{-(i+j)} cap A_{-(i'+j)} = {0}; then alpha_j = -beta_i
 *        for all j, so all alpha_j are equal to alpha_0 = 1, but 1 in A_{-1}
 *        is false for K >= 2).  So each column has at most one zero; if
 *        M_{ut} = 0 then M_{u-1,t} != 0 and 0 = M_{ut}/M_{u-1,t} in R(M),
 *        forcing v = min R = 0.  Hence for v != 0 we delete x = -beta_s from
 *        every S_t for every assigned row s (including s = 0: x = 0) and
 *        reject b with 1 + b = 0; this also makes every inverse in (2a)-(2c)
 *        exist.  For v = 0 (beta_1 = -1) nothing in (2a)-(2d) binds.
 *   Soundness of PRUNE 2 as a whole: if the restricted search finds no leaf,
 *   no canonical normalised solution exists, hence by the displayed
 *   equivalence no normalised solution exists, which is dfs2's INFEASIBLE.
 *   If it finds a leaf, the leaf is a solution of the ORIGINAL constraints
 *   (the filters only delete elements), and it is re-checked.
 *   Row 1 is always assigned first (at level 0 all rows have equal domain
 *   size), so v is known from level 1 on.
 * --------------------------------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

typedef uint64_t u64;
typedef uint32_t u32;

static u64 P, K, W;              /* prime, kappa, words per bitset */
static unsigned char *idx;       /* idx[y] = log_g(y) mod K, idx[0] = 255 */
static u32 *inv;                 /* modular inverses, inv[0] unused */
static u64 **D;                  /* doubled bitsets of A_m, 2p bits */
static u64 *S;                   /* S[level][j] bitsets: (K+1) x K x W words */
static u32 *cands;               /* cands[level]: chosen row's viable values, (K+1) x Pmax */
static u32 *tmplist, *xs;        /* scratch lists */
static u64 *E, *T;               /* scratch bitsets */
static long nodes, limit;
static u64 beta[64], V;          /* V = c_1 = 1 + beta_1, valid from level 1 */
static int assigned[64];
static int opt_plain = 0, opt_sym = 1, opt_fc = 1, opt_print = 0;
static long unexpected_empty = 0;
static long opt_rand = 0; static u64 rstate = 1;
static inline u64 xr(void) { rstate ^= rstate << 13; rstate ^= rstate >> 7; rstate ^= rstate << 17; return rstate; }

static inline u64 mulm(u64 a, u64 b) { return a * b % P; }           /* P < 2^32 */
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

/* out = bits [off, off + 64W) of the doubled bitset d, masked to p bits:
 * out = {b in [0,p) : (b + off) mod p in A_m} = (A_m - off) for 0 <= off < p. */
static inline void extract(u64 *out, const u64 *d, u64 off) {
    for (u64 w = 0; w < W; w++) {
        u64 pos = off + 64 * w, q = pos >> 6, r = pos & 63;
        u64 v = d[q] >> r;
        if (r) v |= d[q + 1] << (64 - r);
        out[w] = v;
    }
    if (P & 63) out[W - 1] &= (1ULL << (P & 63)) - 1;
}
/* out = in & (A_m - b); returns nonzero iff nonempty */
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

/* PRUNE 1: viable values for unassigned row r at this level, into out; returns count. */
static u64 compute_candidates(long level, long r, u32 *out) {
    extract(E, D[md(-r)], 1);                       /* 1 + b in A_{-r} */
    long order[64]; u64 cnt[64];
    long nj = 0;
    for (long j = 1; j < (long)K; j++) { order[nj] = j; cnt[nj] = popc(SET(level, j)); nj++; }
    for (long a = 1; a < nj; a++) {                   /* smallest S_j first */
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
            u64 small = cj < 2 * K ? cj : 2 * K;        /* cost model: look-ups per b until first hit */
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
        /* look-up mode: keep b iff some x in S_j has x + b in A_m */
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
    /* PRUNE 2a/2d on the row value itself (only when v is known and nonzero) */
    u64 n = listof(E, out);
    if (opt_sym && !opt_plain && assigned[1] && V != 0) {
        u64 k = 0;
        long rm = md(r - 1), rp = md(r + 1);
        for (u64 q = 0; q < n; q++) {
            u64 b = out[q], c = b + 1; if (c >= P) c -= P;
            if (c == 0) continue;                                    /* 2d */
            if (assigned[rm]) { u64 cm = beta[rm] + 1; if (cm >= P) cm -= P; if (mulm(c, inv[cm]) < V) continue; }   /* 2a */
            if (assigned[rp]) { u64 cp = beta[rp] + 1; if (cp >= P) cp -= P; if (mulm(cp, inv[c]) < V) continue; }   /* 2a */
            out[k++] = b;
        }
        n = k;
    }
    return n;
}

/* PRUNE 2b/2c/2d filters on the child's column sets after row s is assigned. */
static void filt_row(long level, long s) {               /* 2d for row s, 2c for column 1 */
    u64 bs = beta[s], z = (P - bs) % P, cs = bs + 1; if (cs >= P) cs -= P;
    for (long t = 1; t < (long)K; t++) clearbit(SET(level, t), z);
    u64 *S1 = SET(level, 1);
    u64 nx = listof(S1, xs);
    for (u64 q = 0; q < nx; q++) {
        u64 x = xs[q], v = x + bs; if (v >= P) v -= P;
        if (mulm(v, inv[cs]) < V) clearbit(S1, x);
    }
}
static void filt_pair(long level, long s) {              /* 2b for consecutive rows s, s+1 */
    long s1 = md(s + 1);
    u64 bs = beta[s], bs1 = beta[s1];
    for (long t = 1; t < (long)K; t++) {
        u64 *St = SET(level, t);
        u64 nx = listof(St, xs);
        for (u64 q = 0; q < nx; q++) {
            u64 x = xs[q], lo = x + bs, hi = x + bs1;
            if (lo >= P) lo -= P;
            if (hi >= P) hi -= P;
            if (lo == 0) { clearbit(St, x); continue; }   /* zero cell, excluded under v != 0 */
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
            if (n == 0) return 0;                          /* forward check */
            if (best < 0 || n < bestn) { best = r; bestn = n; memcpy(cl, tmplist, n * sizeof(u32)); }
        }
    }
    if (opt_rand) for (u64 q = bestn; q > 1; q--) { u64 w = xr() % q; u32 t = cl[q-1]; cl[q-1] = cl[w]; cl[w] = t; }
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
        else if (!strcmp(argv[a], "rand") && a + 2 < argc) { opt_rand = atol(argv[a+1]); rstate = strtoull(argv[a+2], 0, 10) * 0x9E3779B97F4A7C15ULL + 1; a += 2; }
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
        /* level 0: S_j = A_{-j} (row 0, beta_0 = 0, alpha_0 = 1) */
        for (u64 j = 1; j < K; j++) {
            u64 m = md(-(long)j);
            memcpy(SET(0, j), D[m], W * sizeof(u64));
            if (P & 63) SET(0, j)[W - 1] &= (1ULL << (P & 63)) - 1;
        }
        memset(assigned, 0, sizeof assigned); assigned[0] = 1;
        nodes = 0; beta[0] = 0; V = 0; unexpected_empty = 0;
        int r = dfs(0);
        for (long rr = 1; opt_rand && r == -1 && rr < opt_rand; rr++) {
            memset(assigned, 0, sizeof assigned); assigned[0] = 1; nodes = 0; V = 0; r = dfs(0);
        }
        if (opt_rand && r == 0) r = -1;   /* a randomized run never claims INFEASIBLE */
        double dt = now() - t0;
        if (r == 1) {
            /* witness: alpha_j = any element of the final S_j; re-check all K^2 cells of the ORIGINAL definition */
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
