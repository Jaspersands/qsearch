/* Joint law of the column indicators (1[n_j(y) > 0])_j for uniform y = (0, y_1..y_{K-1}).
   n_j(y) = #{x : x + y_i in Q_{-(i+j)} for all i in Z_K}  (strict cosets, as in WT Lemma A).
   Exact mode: enumerates y up to the free action y -> lambda*y, lambda in Q_0 (which maps
   X_j(y) onto lambda*X_j(y)): y_1 = 0 (weight 1) or y_1 = g^r, r < K (weight h).
   Sample mode: S uniform y.
   Output per prime: q = P(n_0>0); P(all>0); prod_j P(n_j>0); max over (K-1)-sets S of the
   total-variation distance between the law of the indicators on S and the product law;
   flag q<=1/2.
   Usage: jointlaw K P0 P1 [S seed]      (S = 0 or absent: exact) */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>

static int isprime(long n){ if(n<2) return 0; for(long d=2; d*d<=n; d++) if(n%d==0) return 0; return 1; }
static long pw(long a,long e,long m){ long r=1; a%=m; while(e){ if(e&1) r=r*a%m; a=a*a%m; e>>=1;} return r; }
static long primroot(long p){ long n=p-1, f[64], nf=0, t=n; for(long q=2;q*q<=t;q++) if(t%q==0){f[nf++]=q; while(t%q==0) t/=q;} if(t>1) f[nf++]=t;
  for(long g=2;;g++){ int ok=1; for(int i=0;i<nf;i++) if(pw(g,n/f[i],p)==1){ok=0;break;} if(ok) return g; } }
static uint64_t rs=88172645463325252ULL; static uint64_t xr(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }

int main(int argc,char**argv){
  int K=atoi(argv[1]); long P0=atol(argv[2]), P1=atol(argv[3]); long S = argc>4? atol(argv[4]):0; if(argc>5) rs=strtoull(argv[5],0,10);
  for(long p=P0;p<=P1;p++){ if(!isprime(p) || (p-1)%K) continue;
    long h=(p-1)/K, g=primroot(p);
    int *ind=malloc(sizeof(int)*p); ind[0]=-1; long x=1; for(long e=0;e<p-1;e++){ ind[x]=(int)(e%K); x=x*g%p; }
    int NP=1<<K; double *hist=calloc(NP,sizeof(double)); double tot=0;
    long y[32]; y[0]=0; long cnt[32];
    long nouter;  /* number of y vectors to process */
    long free_vars = K-2; /* y_2..y_{K-1} enumerated fully in exact mode */
    long inner=1; for(int i=0;i<free_vars;i++) inner*=p;
    nouter = S? S : (long)(K+1)*inner;
    for(long it=0; it<nouter; it++){
      double wgt=1;
      if(S){ for(int i=1;i<K;i++) y[i]=(long)(xr()%p); }
      else { long a=it/inner, b=it%inner; if(a==0){ y[1]=0; wgt=1;} else { y[1]=pw(g,a-1,p); wgt=(double)h; }
             for(int i=2;i<K;i++){ y[i]=b%p; b/=p; } }
      for(int j=0;j<K;j++) cnt[j]=0;
      for(long xx=1; xx<p; xx++){ int ix=ind[xx]; int ok=1;
        for(int i=1;i<K;i++){ long z=xx+y[i]; if(z>=p) z-=p; if(z==0){ok=0;break;} int want=((ix-i)%K+K)%K; if(ind[z]!=want){ok=0;break;} }
        if(ok) cnt[(K-ix)%K]++; }
      int pat=0; for(int j=0;j<K;j++) if(cnt[j]>0) pat|=1<<j;
      hist[pat]+=wgt; tot+=wgt; }
    double qj[32]; for(int j=0;j<K;j++){ qj[j]=0; for(int s=0;s<NP;s++) if(s>>j&1) qj[j]+=hist[s]; qj[j]/=tot; }
    double pall=hist[NP-1]/tot, prodq=1; for(int j=0;j<K;j++) prodq*=qj[j];
    double maxtv=0, minr=1e300, maxr=0;
    for(int omit=0; omit<K; omit++){ /* law on S = Z_K \ {omit} */
      double tv=0;
      for(int a=0;a<NP;a++){ if(a>>omit&1) continue; double pa=0; for(int s=0;s<NP;s++) if((s & ~(1<<omit))==a) pa+=hist[s]; pa/=tot;
        double pr=1; for(int j=0;j<K;j++){ if(j==omit) continue; pr*= (a>>j&1)? qj[j] : 1-qj[j]; } tv+=fabs(pa-pr); }
      tv/=2; if(tv>maxtv) maxtv=tv;
      { int full=(NP-1)&~(1<<omit); double pa=0; for(int s=0;s<NP;s++) if((s&full)==full) pa+=hist[s]; pa/=tot;
        double pr=1; for(int j=0;j<K;j++) if(j!=omit) pr*=qj[j]; double r= pr>0? pa/pr:0; if(r<minr) minr=r; if(r>maxr) maxr=r; } }
    printf("K=%d p=%ld %s q=%.6g P(all)=%.6g prod_q=%.6g ratio=%.4g maxTV_(K-1)=%.4g AND_(K-1)/prod in [%.4g,%.4g] q<=1/2:%s lambda=%.4g\n",K,p,S?"sample":"exact",qj[0],pall,prodq,prodq>0?pall/prodq:0,maxtv,minr,maxr,qj[0]<=0.5?"yes":"no",(double)(p-1)/pow(K,K));
    fflush(stdout); free(ind); free(hist); }
  return 0; }
