\\ PARI/GP check of the six kappa = 9 witnesses above 20000 (AI-written 10 Nov 2026).
\\ C = matrix(k,k,i,j, z^(i-1) z^(j-1) (alpha_j + beta_i)); require: isprime(p), p = 1 mod k,
\\ znorder(Mod(g,p)^((p-1)/k)) == k, C[1,1] != 0, every nonzero C[i,j] a k-th power (ispower),
\\ and B~ * C * B == 0 for a basis B of W = ker(z^0..z^(k-1)) from matker.
chk(k,p,g,be,al)={my(h=(p-1)/k,z=Mod(g,p),C,v,B,ok=1);
 if(!isprime(p)||(p-1)%k,return("p"));
 if(znorder(z^h)!=k,return("generator"));
 C=matrix(k,k,i,j,z^(i-1)*z^(j-1)*(al[j]+be[i]));
 if(C[1,1]==0,return("C00"));
 for(i=1,k,for(j=1,k,if(C[i,j]!=0 && !ispower(C[i,j],k),ok=0)));
 if(!ok,return("not k-th power"));
 v=matrix(1,k,i,j,z^(j-1)); B=matker(v);
 if(matsize(B)[2]!=k-1,return("dim W"));
 if(B~*C*B!=0,return("W(x)W"));
 "ok"};
print("k=9 p=21187 g=2: ", chk(9,21187,2,[0, 33, 15892, 17438, 14704, 4111, 20146, 17675, 10315],[1, 4165, 9735, 15268, 6053, 2638, 21015, 20027, 17942]), "  znorder(g)=", znorder(Mod(2,21187)), " p-1=", factor(21187-1));
print("k=9 p=21871 g=6: ", chk(9,21871,6,[0, 21870, 4632, 8033, 10042, 18797, 1894, 19830, 18608],[1, 19716, 2784, 20487, 12367, 3888, 6610, 388, 13251]), "  znorder(g)=", znorder(Mod(6,21871)), " p-1=", factor(21871-1));
print("k=9 p=22051 g=3: ", chk(9,22051,3,[0, 15, 5481, 1154, 15045, 15660, 455, 7683, 2764],[1, 1336, 12405, 10579, 11073, 5962, 12268, 18459, 18714]), "  znorder(g)=", znorder(Mod(3,22051)), " p-1=", factor(22051-1));
print("k=9 p=22303 g=6: ", chk(9,22303,6,[0, 3, 4400, 4797, 4506, 9036, 13944, 9456, 17636],[1, 16695, 8707, 11734, 10298, 810, 9610, 2094, 3472]), "  znorder(g)=", znorder(Mod(6,22303)), " p-1=", factor(22303-1));
print("k=9 p=23671 g=3: ", chk(9,23671,3,[0, 12, 269, 3597, 15465, 14685, 6781, 9464, 20133],[1, 9539, 19912, 5537, 9638, 20920, 4866, 9841, 13604]), "  znorder(g)=", znorder(Mod(3,23671)), " p-1=", factor(23671-1));
print("k=9 p=24841 g=14: ", chk(9,24841,14,[0, 318, 17020, 22333, 14848, 14237, 3446, 15718, 1160],[1, 15091, 11309, 4063, 3806, 12499, 23972, 7766, 2340]), "  znorder(g)=", znorder(Mod(14,24841)), " p-1=", factor(24841-1));
print("negative control: ", chk(9,21871,6,[0, 21870, 4632, 8033, 10042, 18797, 1894, 19830, 18608],[1, 19717, 2784, 20487, 12367, 3888, 6610, 388, 13251]));
