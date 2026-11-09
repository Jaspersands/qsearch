/* s2a: independent exhaustive search for two-level contractions at (p, kappa).
 * Normal form (Lemma lem:app-s2-normal and the paragraph after it): beta_0 = 0, alpha_0 = 1,
 * cell (i,j): alpha_j + beta_i in Q_{-(i+j)} u {0}   (mode 0, the definition of E_2)
 *             alpha_j + beta_i in Q_{-(i+j)}         (mode 1, every entry nonzero)
 * symmetric form (mode 2/3): alpha = beta = t, t_0 = 1/2, entries z_i z_j (t_i + t_j) in Q_0 u {0} (2) or Q_0 (3).
 * Exact DFS over beta_1..beta_{k-1} with running column intersections (an exact necessary
 * condition, so the pruning is sound); no symmetry breaking, no use of Lemma two-rows.
 * Coset labels: xi = least primitive root g, Q_m = g^m Q_0, i.e. ind(x) = dlog_g(x) mod k.
 * Usage: e2search kappa pmin pmax mode [xi_exponent]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int p, k, mode, h, W;
static int *ind;           /* ind[x] = dlog mod k, ind[0] = -1 */
static uint64_t **A;       /* A[(i*k+j)] bitset over x in F_p: allowed values of alpha_j+beta_i */
static uint64_t *col;      /* running intersections, (k) x (depth) x W */
static int beta[32], alpha_w[32];

static int isprime(int n){ if(n<2) return 0; for(int d=2; (long)d*d<=n; d++) if(n%d==0) return 0; return 1; }
static long pw(long b, long e, long m){ long r=1; b%=m; while(e){ if(e&1) r=r*b%m; b=b*b%m; e>>=1;} return r; }
static int primroot(int p){
  int f[32], nf=0, n=p-1;
  for(int d=2; (long)d*d<=n; d++) if(n%d==0){ f[nf++]=d; while(n%d==0) n/=d; }
  if(n>1) f[nf++]=n;
  for(int g=2; g<p; g++){ int ok=1; for(int i=0;i<nf;i++) if(pw(g,(p-1)/f[i],p)==1){ok=0;break;} if(ok) return g; }
  return -1;
}
static inline int getbit(const uint64_t *b, int x){ return (b[x>>6]>>(x&63))&1; }
static inline void setbit(uint64_t *b, int x){ b[x>>6] |= (1ULL<<(x&63)); }

/* shifted[x] = base[(x + s) mod p], intersect into dst; returns nonzero if dst nonempty */
static int and_shift(uint64_t *dst, const uint64_t *src_prev, const uint64_t *base, int s){
  int nonempty = 0;
  for(int w=0; w<W; w++){
    uint64_t v = 0;
    int x0 = w*64;
    for(int b=0; b<64; b++){
      int x = x0 + b; if(x>=p) break;
      int y = x + s; if(y>=p) y-=p;
      if(getbit(base,y)) v |= (1ULL<<b);
    }
    v &= src_prev[w];
    dst[w] = v; if(v) nonempty = 1;
  }
  return nonempty;
}

static long nodes;
/* depth r: choosing beta_r (r = 1..k-1); col[(r-1)][j] holds intersection over rows 0..r-1 */
static int dfs(int r){
  if(r == k){
    for(int j=1;j<k;j++){
      uint64_t *c = col + ((size_t)(r-1)*k + j)*W;
      int found=-1; for(int w=0;w<W && found<0;w++) if(c[w]) { for(int b=0;b<64;b++) if((c[w]>>b)&1){found=w*64+b;break;} }
      alpha_w[j]=found;
    }
    return 1;
  }
  /* beta_r must satisfy column 0: 1 + beta_r in A(r,0) */
  for(int b=0; b<p; b++){
    int y = (1 + b) % p;
    if(!getbit(A[r*k+0], y)) continue;
    nodes++;
    beta[r] = b;
    int ok = 1;
    for(int j=1;j<k && ok;j++){
      uint64_t *prev = col + ((size_t)(r-1)*k + j)*W;
      uint64_t *dst  = col + ((size_t)r*k + j)*W;
      ok = and_shift(dst, prev, A[r*k+j], b);
    }
    if(ok && dfs(r+1)) return 1;
  }
  return 0;
}

/* symmetric form: t_0 = 1/2; choose t_1..t_{k-1}; entries z_i z_j (t_i+t_j) */
static long zz[32];
static int tt[32];
static int okcell(long v){ v%=p; if(v<0) v+=p; if(v==0) return (mode==2); return ind[v]==0; }
static int dfs_sym(int j){
  if(j==k) return 1;
  for(int t=0;t<p;t++){
    if(!okcell(2*zz[j]%p*zz[j]%p*t)) continue;
    int ok=1; for(int i=0;i<j && ok;i++) ok = okcell(zz[i]*zz[j]%p*((t+tt[i])%p));
    if(!ok) continue;
    tt[j]=t; if(dfs_sym(j+1)) return 1;
  }
  return 0;
}

int main(int argc, char **argv){
  if(argc<5){ fprintf(stderr,"usage\n"); return 1; }
  k = atoi(argv[1]); int pmin = atoi(argv[2]), pmax = atoi(argv[3]); mode = atoi(argv[4]);
  int xe = argc>5 ? atoi(argv[5]) : 1;  /* xi = g^xe, need gcd(xe,k)=1 */
  for(p = pmin; p <= pmax; p++){
    if(!isprime(p) || (p-1)%k) continue;
    h = (p-1)/k; W = (p+63)/64;
    int g = primroot(p);
    ind = malloc(sizeof(int)*p); ind[0] = -1;
    long x=1; for(int n=0;n<p-1;n++){ ind[x] = n % k; x = x*g%p; }
    /* relabel for xi = g^xe: ind_xi = ind_g * xe^{-1} mod k */
    int einv=-1; for(int e=0;e<k;e++) if((e*xe)%k==1%k){einv=e;break;}
    if(einv<0){ fprintf(stderr,"bad xi exponent\n"); return 1; }
    for(int y=1;y<p;y++) ind[y] = (ind[y]*einv)%k;
    long xi = pw(g, xe, p);
    if(mode>=2){
      for(int m=0;m<k;m++) zz[m]=pw(xi,m,p);
      tt[0] = (int)((p+1)/2);
      int f = dfs_sym(1);
      printf("k=%d p=%d mode=%d xi=%ld %s", k, p, mode, xi, f?"FEASIBLE":"INFEASIBLE");
      if(f){ printf(" t="); for(int j=0;j<k;j++) printf("%d%s", tt[j], j<k-1?",":""); }
      printf("\n"); fflush(stdout); free(ind); continue;
    }
    A = malloc(sizeof(uint64_t*)*k*k);
    for(int i=0;i<k;i++) for(int j=0;j<k;j++){
      uint64_t *b = calloc(W, sizeof(uint64_t));
      int target = ((-(i+j)) % k + k) % k;
      for(int y=0;y<p;y++){
        if(y==0){ if(mode==0) setbit(b,0); continue; }
        if(ind[y]==target) setbit(b,y);
      }
      A[i*k+j]=b;
    }
    col = calloc((size_t)k*k*W, sizeof(uint64_t));
    /* row 0 (beta_0 = 0): alpha_j in A(0,j) */
    for(int j=1;j<k;j++) memcpy(col + ((size_t)0*k + j)*W, A[0*k+j], W*sizeof(uint64_t));
    beta[0]=0; nodes=0;
    /* check cell (0,0): alpha_0 + beta_0 = 1 in Q_0 : always */
    int f = (k==1) ? 1 : dfs(1);
    printf("k=%d p=%d mode=%d xi=%ld %s nodes=%ld", k, p, mode, xi, f?"FEASIBLE":"INFEASIBLE", nodes);
    if(f){ printf(" beta="); for(int i=0;i<k;i++) printf("%d%s", i?beta[i]:0, i<k-1?",":"");
           printf(" alpha=1"); for(int j=1;j<k;j++) printf(",%d", alpha_w[j]); }
    printf("\n"); fflush(stdout);
    for(int i=0;i<k*k;i++) free(A[i]); free(A); free(col); free(ind);
  }
  return 0;
}
