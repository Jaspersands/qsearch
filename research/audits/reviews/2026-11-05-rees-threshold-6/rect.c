/* rect.c -- rectangular contractions RC(D, m) for the tower schedule.
 * RC(D,m): rows R = {0, m, 2m, ..., D-m} (a subgroup of Z_D of size r = D/m),
 * columns Z_D.  Find alpha in F_p^{Z_D}, beta in F_p^R with
 *     alpha_j + beta_i in Q^{(D)}_{-(i+j)} u {0}   (i in R, j in Z_D),
 *     alpha_0 + beta_0 != 0,
 * where Q^{(D)}_c = g^c (F_p^x)^D, g a primitive root.  m = 1 is the full
 * two-level contraction (E_2(D)).  Normal form beta_0 = 0, alpha_0 = 1.
 * Usage: rect D m plo phi mode [zeros] [seed] [tries]
 *   mode 0 = randomized witness search (reports FEASIBLE or NOTFOUND)
 *   mode 1 = complete search (FEASIBLE or INFEASIBLE)
 *   zeros = 1 allows zero cells off (0,0) (definition of E_2); 0 = strict.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef long long ll;
static ll pw(ll b, ll e, ll p){ ll r=1; b%=p; if(b<0)b+=p; while(e){ if(e&1) r=r*b%p; b=b*b%p; e>>=1;} return r; }
static int isprime(ll n){ if(n<2) return 0; for(ll d=2; d*d<=n; d++) if(n%d==0) return 0; return 1; }
static ll primroot(ll p){ ll f[64]; int nf=0; ll n=p-1; for(ll d=2; d*d<=n; d++) if(n%d==0){ f[nf++]=d; while(n%d==0) n/=d; } if(n>1) f[nf++]=n;
  for(ll g=2; g<p; g++){ int ok=1; for(int k=0;k<nf;k++) if(pw(g,(p-1)/f[k],p)==1){ok=0;break;} if(ok) return g; } return -1; }
static uint64_t rs=88172645463325252ULL; static uint64_t xr(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }

static int D, m, r, zeros; static ll p; static unsigned char *ind; /* ind[x] in [0,D), ind[0]=255 */
static inline int ok(ll v, int c){ /* v in Q_c u {0}? */
  if(v==0) return zeros; return ind[v]==c; }
static ll beta[64], alpha[64];
/* complete search state */
static ll *cand[64]; static int ncand[64][64]; /* per depth, per column */
static ll **lists; static long long nodes;
static int R_(int k){ return k*m; } /* k-th row index */

static int colfeas_full(int j){ /* find x for column j given all rows; return 1 and set alpha */
  ll st = xr()%p;
  for(ll t=0;t<p;t++){ ll x=(st+t)%p; int good=1;
    for(int k=0;k<r;k++){ int i=R_(k); int c=((-(i+j))%D+D)%D; ll v=(x+beta[k])%p; if(!ok(v,c)){good=0;break;} }
    if(good){ alpha[j]=x; return 1; } }
  return 0; }

/* DFS: depth k (rows 1..r-1 to choose); lists[k*D + j] candidate arrays */
static ll *L[65][64]; static int Ln[65][64];
static int dfs(int k){
  nodes++;
  if(k==r){ for(int j=1;j<D;j++) alpha[j]=L[k][j][0]; return 1; }
  int i=R_(k);
  /* beta_k must satisfy cell (i,0): 1+beta in Q_{-i} u0, beta distinct from earlier beta's (Lemma: distinct needed? not required, skip) */
  for(ll b=0;b<p;b++){
    int c0=((-i)%D+D)%D; if(!ok((1+b)%p,c0)) continue;
    int dup=0; for(int kk=0;kk<k;kk++) if(beta[kk]==b) dup=1; if(dup) continue;
    beta[k]=b; int alive=1;
    for(int j=1;j<D && alive;j++){ int c=((-(i+j))%D+D)%D; int n=0;
      for(int t=0;t<Ln[k][j];t++){ ll x=L[k][j][t]; if(ok((x+b)%p,c)) L[k+1][j][n++]=x; }
      Ln[k+1][j]=n; if(n==0) alive=0; }
    if(alive && dfs(k+1)) return 1;
  }
  return 0; }

int main(int argc, char**argv){
  if(argc<6){ fprintf(stderr,"usage\n"); return 1; }
  D=atoi(argv[1]); m=atoi(argv[2]); ll plo=atoll(argv[3]), phi=atoll(argv[4]); int mode=atoi(argv[5]);
  zeros = argc>6? atoi(argv[6]) : 1; if(argc>7) rs ^= (uint64_t)atoll(argv[7])*2654435761ULL; int tries = argc>8? atoi(argv[8]) : 200;
  if(D%m){ fprintf(stderr,"m must divide D\n"); return 1; } r=D/m;
  for(p=plo; p<=phi; p++){
    if(p%D!=1 || !isprime(p)) continue;
    ll g=primroot(p); ind=malloc(p); ind[0]=255; ll x=1; for(ll e=0;e<p-1;e++){ ind[x]=(unsigned char)(e%D); x=x*g%p; }
    beta[0]=0; alpha[0]=1; int found=0;
    if(mode==0){
      for(int tr=0; tr<tries && !found; tr++){
        int okb=1;
        for(int k=1;k<r;k++){ int i=R_(k); int c0=((-i)%D+D)%D; ll st=xr()%p; int got=0;
          for(ll t=0;t<p;t++){ ll b=(st+t)%p; if(!ok((1+b)%p,c0)) continue; int dup=0; for(int kk=0;kk<k;kk++) if(beta[kk]==b) dup=1; if(dup) continue; beta[k]=b; got=1; break; }
          if(!got){okb=0;break;} }
        if(!okb) continue;
        int all=1; for(int j=1;j<D;j++) if(!colfeas_full(j)){ all=0; break; }
        if(all) found=1;
      }
      if(found){ printf("%lld FEASIBLE g=%lld beta",p,g); for(int k=0;k<r;k++) printf(" %lld",beta[k]); printf(" alpha"); for(int j=0;j<D;j++) printf(" %lld",alpha[j]); printf("\n"); }
      else printf("%lld NOTFOUND\n",p);
    } else {
      for(int j=1;j<D;j++){ L[0][j]=malloc(sizeof(ll)*p); int n=0; int c=((-j)%D+D)%D;
        for(ll xx=0;xx<p;xx++) if(ok(xx,c)) L[0][j][n++]=xx; Ln[0][j]=n; }
      for(int k=1;k<=r;k++) for(int j=1;j<D;j++) L[k][j]=malloc(sizeof(ll)*(Ln[0][j]+1));
      /* depth index: L[k] = lists after rows 0..k-1 are fixed; row 0 (beta=0) already applied in L[0]; so start at k=1 with L[1]=L[0] */
      for(int j=1;j<D;j++){ memcpy(L[1][j],L[0][j],sizeof(ll)*Ln[0][j]); Ln[1][j]=Ln[0][j]; }
      nodes=0; int alive=1; for(int j=1;j<D;j++) if(Ln[1][j]==0) alive=0;
      found = alive && dfs(1);
      if(found){ printf("%lld FEASIBLE g=%lld beta",p,g); for(int k=0;k<r;k++) printf(" %lld",beta[k]); printf(" alpha"); for(int j=0;j<D;j++) printf(" %lld",alpha[j]); printf(" nodes=%lld\n",nodes); }
      else printf("%lld INFEASIBLE nodes=%lld\n",p,nodes);
      for(int k=0;k<=r;k++) for(int j=1;j<D;j++) free(L[k][j]);
    }
    fflush(stdout); free(ind);
  }
  return 0; }
