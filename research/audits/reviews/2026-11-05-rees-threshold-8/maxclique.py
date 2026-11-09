"""Clique number of the cyclotomic graph Cay(F_p, Q_0) (Q_0 = kappa-th powers, -1 in Q_0).
By vertex- and Q_0-transitivity a maximum clique may contain 0 and 1, so we search the
common neighbourhood N = Q_0 cap (Q_0 + 1). Usage: python maxclique.py K p [p ...]"""
import sys, math
import networkx as nx
k = int(sys.argv[1])
for p in map(int, sys.argv[2:]):
    h = (p-1)//k
    Q = set(pow(x, k, p) for x in range(1, p))
    assert len(Q) == h and (p-1) in Q
    N = [x for x in Q if (x-1) % p in Q]
    G = nx.Graph(); G.add_nodes_from(N)
    for i, x in enumerate(N):
        for y in N[i+1:]:
            if (x-y) % p in Q: G.add_edge(x, y)
    om = max(len(c) for c in nx.find_cliques(G)) + 2 if N else 2
    nmax = sum(1 for c in nx.find_cliques(G) if len(c) + 2 == om)
    # random-graph expectation of #om-cliques through {0,1} up to Q_0 scaling, density 1/k
    print(f"k={k} p={p} h={h} |N(0,1)|={len(N)} clique_number={om} maximal_cliques_of_that_size_through_0_1={nmax} 2log_k(p)={2*math.log(p)/math.log(k):.2f}", flush=True)
