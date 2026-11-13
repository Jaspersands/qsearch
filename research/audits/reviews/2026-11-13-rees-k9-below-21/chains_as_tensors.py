#!/opt/anaconda3/bin/python
"""Route 2 for the K_L != {0} chain corollary: every chain witness of witness_dump.out, composed by Lemma P,
is verified as an (L+1)-level lift(K_L)-contraction (exact, all cells).  usage: chains_as_tensors.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ell_common as E, compose as C
T = C.two_level
W = {
 37: [T(3,(0,1,2),(0,),[1,0,12],{0:0,1:2,2:1}), T(9,(0,3,6),(0,4),[1,0,17,10,36,34,0,10,32],{0:0,3:1,6:27})],
 73: [T(3,(0,1,2),(0,),[1,14,26],{0:0,1:1,2:3}), T(9,(0,3,6),(0,1),[1,0,0,43,67,28,45,48,34],{0:0,3:6,6:25})],
 19: [T(3,(0,1,2),(0,),[1,0,5],{0:0,1:3,2:1}), T(9,(0,3,6),(0,1),[1,9,9,7,0,0,16,15,15],{0:0,3:4,6:10})],
 '19b': [T(9,tuple(range(9)),(0,1,4,7),[1,0,9,16,0,9,16,0,9],{0:0,1:10,2:3,3:1,4:10,5:3,6:1,7:10,8:3}),
         T(9,(0,1,4,7),(0,3,8),[1,4,5,1,0,11,11,13,1],{0:0,1:8,4:18,7:14})],
 '37f': [T(9,tuple(range(9)),(0,2,5),[1,35,8,24,20,21,30,0,26],{0:0,1:11,2:36,3:2,4:29,5:13,6:17,7:16,8:7})],
 181: [T(3,(0,1,2),(0,),[1,0,17],{0:0,1:2,2:1}), T(9,(0,3,6),(0,1),[1,1,72,80,7,87,129,152,138],{0:0,3:6,6:4}),
       T(9,(0,1),(0,),[1,75,54,68,0,16,95,138,97],{0:0,1:10})],
 433: [T(3,(0,1,2),(0,),[1,0,26],{0:0,1:6,2:2}), T(9,(0,3,6),(0,1),[1,143,12,103,131,242,0,0,22],{0:0,3:1,6:2}),
       T(9,(0,1),(0,),[1,9,81,302,55,19,84,14,0],{0:0,1:8})],
}
for key, st in W.items():
    p = int(str(key).rstrip('bf'))
    B, l = C.compose(p, 9, st)
    K = st[-1][2]
    ok, info = E.verify(B, p, 9, K, l, sample=20)
    print(f'{key}: chain of length {len(st)} -> {l}-level {K}-contraction', 'VERIFIED' if ok else 'FAILED', info)
