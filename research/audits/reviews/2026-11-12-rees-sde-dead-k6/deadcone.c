/* Largest dead banks for the diagonal SDE in F_p^1 and F_p^2 via P-stable cones.
 *
 * P = (F_p^x)^kappa, P0 = P u {0}. A bank (multiset of nonzero columns) is dead if
 * sum x_i lambda_i = 0 has no solution x in P0^n \ {0}. Columns are taken up to
 * P-scaling ("classes" = P-orbits of nonzero vectors). Cone C(B) = {sum x_i lambda_i}
 * is P-stable, hence a set of classes (plus 0). Incremental rule (exact):
 *   B dead and lambda new:  B + lambda dead  <=>  class(-lambda) not in C(B);
 *   C(B + lambda) = C(B) u P lambda u (C(B) + P lambda).
 * We store D = -C (as a class bitset):  B + L dead <=> L not in D,
 *   D' = D | {M} | OR_{A in D} T[A][M],  M = class(-L),  T[A][B] = classes of a + u b, u in P.
 *
 * Modes:
 *   deadcone p kappa w2        : dead_w2.py-equivalent search (base e1,e2, multisets of
 *                                further classes in index order); prints m1, m2, #max_ext.
 *   deadcone p kappa tri       : canonical search: banks with >= 3 projective points, base
 *                                (g^c1 e1, g^c2 e2, (1,1)) for c1, c2 in Z/kappa; m2 = max(2 m1, tri).
 *   deadcone p kappa check     : read banks from stdin (n then 2n ints), print dead flag (0/1).
 * Class indexing is identical to dead_w2.py: point t<p is (1,t), point p is (0,1),
 * class = pt*kappa + e with representative g^e * point.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#ifndef W
#define W 5
#endif
#define MAXN (64 * W)
typedef struct { uint64_t w[W]; } bs;

static int p, K, g, NC, hneg;
static int dlog_[1000], pw[1000];
static int Pset[1000], nP;
static bs T[MAXN][MAXN];
static int negc[MAXN];
static int repu[MAXN], repv[MAXN];

static inline int tst(const bs *s, int i) { return (s->w[i >> 6] >> (i & 63)) & 1; }
static inline void setb(bs *s, int i) { s->w[i >> 6] |= (uint64_t)1 << (i & 63); }
static inline void orin(bs *a, const bs *b) { for (int k = 0; k < W; k++) a->w[k] |= b->w[k]; }

static int primroot(int q) {
    int m = q - 1, fac[32], nf = 0;
    for (int d = 2; d * d <= m; d++) if (m % d == 0) { fac[nf++] = d; while (m % d == 0) m /= d; }
    if (m > 1) fac[nf++] = m;
    for (int c = 2; c < q; c++) {
        int ok = 1;
        for (int i = 0; i < nf; i++) {
            long r = 1, b = c; int e = (q - 1) / fac[i];
            while (e) { if (e & 1) r = r * b % q; b = b * b % q; e >>= 1; }
            if (r == 1) { ok = 0; break; }
        }
        if (ok) return c;
    }
    return -1;
}

/* dimension-2 class of nonzero (u,v) */
static int cls2(int u, int v) {
    u %= p; v %= p; if (u < 0) u += p; if (v < 0) v += p;
    if (u) { int inv = pw[(p - 1 - dlog_[u]) % (p - 1)]; int t = (int)((long)v * inv % p); return t * K + dlog_[u] % K; }
    if (v) return p * K + dlog_[v] % K;
    return -1;
}

static void setup(int dim) {
    g = primroot(p);
    long v = 1;
    for (int e = 0; e < p - 1; e++) { pw[e] = (int)v; dlog_[v] = e; v = v * g % p; }
    nP = 0;
    for (int e = 0; e < p - 1; e += 1) if (e % K == 0) Pset[nP++] = pw[e];
    /* note: K | p-1 is required (kappa' = gcd(kappa,p-1) = kappa) */
    hneg = dlog_[p - 1] % K;
    if (dim == 1) {
        NC = K;
        for (int a = 0; a < K; a++) { repu[a] = pw[a]; repv[a] = 0; }
    } else {
        NC = (p + 1) * K;
        for (int L = 0; L < NC; L++) {
            int pt = L / K, e = L % K, s = pw[e];
            if (pt < p) { repu[L] = s; repv[L] = (int)((long)s * pt % p); }
            else { repu[L] = 0; repv[L] = s; }
        }
    }
    if (NC > MAXN) { fprintf(stderr, "too many classes\n"); exit(1); }
    for (int A = 0; A < NC; A++) {
        if (dim == 1) negc[A] = (A + hneg) % K; else negc[A] = cls2(p - repu[A], p - repv[A]);
        for (int B = 0; B < NC; B++) {
            memset(&T[A][B], 0, sizeof(bs));
            for (int i = 0; i < nP; i++) {
                int u = (int)((repu[A] + (long)Pset[i] * repu[B]) % p);
                int w = (int)((repv[A] + (long)Pset[i] * repv[B]) % p);
                int c;
                if (dim == 1) { if (u == 0) continue; c = dlog_[u] % K; }
                else { c = cls2(u, w); if (c < 0) continue; }
                setb(&T[A][B], c);
            }
        }
    }
}

/* add class L to state D (must have L not in D) */
static inline void addcls(const bs *D, int L, bs *out) {
    int M = negc[L];
    *out = *D;
    setb(out, M);
    for (int k = 0; k < W; k++) {
        uint64_t x = D->w[k];
        while (x) { int b = __builtin_ctzll(x); x &= x - 1; orin(out, &T[(k << 6) + b][M]); }
    }
}

static int best; static long long nbest, nodes; static int cur[64], ncur, bestbank[64], cap;

static void dfs(const bs *D, int start, int size) {
    nodes++;
    if (size > best) { best = size; nbest = 1; memcpy(bestbank, cur, sizeof(int) * ncur); }
    else if (size == best) nbest++;
    if (cap && size >= cap) return;
    for (int L = start; L < NC; L++) {
        if (tst(D, L)) continue;
        bs D2; addcls(D, L, &D2);
        cur[ncur++] = L;
        dfs(&D2, L, size + 1);
        ncur--;
    }
}

/* returns 1 and fills D if the base bank is dead */
static int build(const int *base, int nb, bs *D) {
    memset(D, 0, sizeof(bs));
    for (int i = 0; i < nb; i++) {
        if (tst(D, base[i])) return 0;
        bs t; addcls(D, base[i], &t); *D = t;
    }
    return 1;
}

static int m1_value(void) {
    /* separate 1-dim system */
    int save = p; (void)save;
    setup(1);
    bs D; memset(&D, 0, sizeof D);
    best = 0; nbest = 0; nodes = 0; ncur = 0; cap = 3 * K;
    dfs(&D, 0, 0);
    return best;
}

static void print_bank(int n, const int *b) {
    printf("[");
    for (int i = 0; i < n; i++) printf("%s[%d,%d]", i ? "," : "", repu[b[i]], repv[b[i]]);
    printf("]");
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: p kappa mode\n"); return 1; }
    p = atoi(argv[1]); K = atoi(argv[2]);
    if ((p - 1) % K) { fprintf(stderr, "need kappa | p-1\n"); return 1; }
    const char *mode = argv[3];
    clock_t t0 = clock();
    if (!strcmp(mode, "check")) {
        setup(2);
        int n;
        while (scanf("%d", &n) == 1) {
            int b[64], ok = 1;
            for (int i = 0; i < n; i++) { int u, v; scanf("%d %d", &u, &v); b[i] = cls2(u, v); if (b[i] < 0) ok = 0; }
            bs D;
            printf("%d\n", ok ? build(b, n, &D) : 0);
        }
        return 0;
    }
    int m1 = m1_value();
    long long n1 = nbest;
    setup(2);
    if (!strcmp(mode, "w2")) {
        int base[2] = {0, p * K};
        bs D; build(base, 2, &D);
        int ncand = 0; for (int L = 0; L < NC; L++) if (!tst(&D, L)) ncand++;
        best = 2; nbest = 0; nodes = 0; ncur = 0; cap = 0;
        memcpy(cur, base, sizeof base); ncur = 2;
        best = 1; /* so that the root (size 2) sets best = 2, nbest = 1 like dead_w2 */
        dfs(&D, 0, 2);
        /* dead_w2 counts the root as one bank of size 2 too; identical semantics */
        printf("w2 kappa=%d p=%d minus1inP=%d m1=%d m2=%d nmax_ext=%lld ncand3=%d nodes=%lld sec=%.1f example=",
               K, p, hneg == 0, m1, best, nbest, ncand, nodes, (double)(clock() - t0) / CLOCKS_PER_SEC);
        print_bank(best, bestbank); printf("\n");
    } else if (!strcmp(mode, "tri")) {
        int overall = 2 * m1; long long totnodes = 0; int ex[64], exn = 0;
        printf("tri kappa=%d p=%d m1=%d (#max 1-dim multisets %lld)\n", K, p, m1, n1);
        for (int c1 = 0; c1 < K; c1++) for (int c2 = 0; c2 < K; c2++) {
            int base[3] = {0 * K + c1, p * K + c2, 1 * K + 0};
            bs D;
            if (!build(base, 3, &D)) { printf("  base c1=%d c2=%d not dead\n", c1, c2); continue; }
            memcpy(cur, base, sizeof base); ncur = 3;
            best = 0; nbest = 0; nodes = 0; cap = 0;
            dfs(&D, 0, 3);
            totnodes += nodes;
            printf("  base c1=%d c2=%d max=%d #max=%lld nodes=%lld\n", c1, c2, best, nbest, nodes);
            if (best > overall || exn == 0) { if (best >= overall) { overall = best; exn = best; memcpy(ex, bestbank, sizeof(int) * best); } }
            fflush(stdout);
        }
        printf("tri kappa=%d p=%d minus1inP=%d m1=%d m2=%d nodes=%lld sec=%.1f example=", K, p, hneg == 0, m1,
               overall, totnodes, (double)(clock() - t0) / CLOCKS_PER_SEC);
        if (exn) print_bank(exn, ex); else printf("(two-line bank, 2*m1)");
        printf("\n");
    }
    return 0;
}
