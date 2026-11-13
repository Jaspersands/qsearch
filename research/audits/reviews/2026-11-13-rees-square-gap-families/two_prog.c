/* Two-progression family F3 (open torus orbits), fixed chart.
 * alpha_j = rho^j, beta_i = -t rho^i  (j,i = 0..kappa-1), rho, t in F_p^*.
 * cell(j,i) = rho^i (rho^{j-i} - t);  ind = i*ind(rho) + H(j-i),  H(d) = ind(rho^d - t),
 * d in [-(kappa-1), kappa-1].  The configuration (after the affine relabelling
 * sigma(j) = -(theta j + const), pi(i) = -(i(ind rho - theta) + const)) is a two-level
 * contraction iff H is affine in d on that interval with slope theta, theta != 0 and
 * theta != ind(rho) (bijectivity), and no cell is zero (t != rho^d) -- zero cells are
 * skipped here, so the family is slightly undercounted.
 * Usage: two_prog kappa pmin pmax [stride]   (stride: only every stride-th admissible prime)
 * Output: p  p mod kappa^2  nsol  [rho t]
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
static int64_t pw(int64_t b,int64_t e,int64_t m){int64_t r=1;b%=m;if(b<0)b+=m;while(e){if(e&1)r=r*b%m;b=b*b%m;e>>=1;}return r;}
static int isprime(int64_t n){if(n<2)return 0;for(int64_t d=2;d*d<=n;d++)if(n%d==0)return 0;return 1;}
static int64_t primroot(int64_t p){int64_t f[64];int nf=0;int64_t n=p-1;for(int64_t d=2;d*d<=n;d++)if(n%d==0){f[nf++]=d;while(n%d==0)n/=d;}if(n>1)f[nf++]=n;
  for(int64_t g=2;;g++){int ok=1;for(int i=0;i<nf;i++)if(pw(g,(p-1)/f[i],p)==1){ok=0;break;}if(ok)return g;}}
int main(int argc,char**argv){
  int K=atoi(argv[1]); int64_t pmin=atoll(argv[2]),pmax=atoll(argv[3]); int stride=argc>4?atoi(argv[4]):1; int cnt=0;
  for(int64_t p=pmin;p<=pmax;p++){
    if(p%K!=1||!isprime(p)) continue;
    if((cnt++)%stride) continue;
    int64_t g=primroot(p);
    unsigned char *I=malloc(p); {int64_t x=1; for(int64_t e=0;e<p-1;e++){I[x]=e%K; x=x*g%p;}}
    long nsol=0; int64_t wr=-1,wt=-1;
    int64_t rp[64]; int L=2*K-1;
    for(int64_t rho=2;rho<p;rho++){
      /* powers rho^d, d = -(K-1)..K-1 stored at index d+K-1 */
      int64_t ri=pw(rho,p-2,p); rp[K-1]=1;
      for(int d=1;d<K;d++){rp[K-1+d]=rp[K-2+d]*rho%p; rp[K-1-d]=rp[K-d]*ri%p;}
      int dup=0; for(int d=1;d<K;d++) if(rp[K-1+d]==1){dup=1;break;}
      if(dup) continue; /* rho of order < K: alpha's not distinct */
      int ir=I[rho];
      for(int64_t t=1;t<p;t++){
        int64_t x0=(rp[K-1]-t+p)%p, x1=(rp[K]-t+p)%p; if(!x0||!x1) continue;
        int h0=I[x0], th=(I[x1]-h0+K)%K;
        if(th==0||th==ir) continue;
        int ok=1;
        for(int d=2;d<K&&ok;d++){int64_t x=(rp[K-1+d]-t+p)%p; if(!x||I[x]!=(h0+d*th)%K) ok=0;}
        for(int d=1;d<K&&ok;d++){int64_t x=(rp[K-1-d]-t+p)%p; if(!x||I[x]!=((h0-d*th)%K+K)%K) ok=0;}
        if(ok){nsol++; if(wr<0){wr=rho;wt=t;}}
      }
    }
    printf("%lld %lld %ld",(long long)p,(long long)(p%(K*K)),nsol);
    if(wr>=0) printf(" %lld %lld",(long long)wr,(long long)wt);
    printf("\n"); fflush(stdout); free(I);
  }
  return 0;
}
