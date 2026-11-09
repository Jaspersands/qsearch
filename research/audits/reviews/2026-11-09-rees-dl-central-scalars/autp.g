# Usage: gap -q -c "p := 5;;" autp.g   (after: python -I mkpc.py 5 > pc5.g)
LoadPackage("autpgrp");
Read(Concatenation("pc", String(p), ".g"));

Print("p=", p, " confluent=", IsConfluent(rws), " size=", Size(G) = p^8, " class=", NilpotencyClassOfGroup(G), " centre=", Size(Centre(G)), "\n");
pc := Pcgs(G);; t0 := Runtime();;
A := AutomorphismGroupPGroup(G);;
gens := Concatenation(A.glAutos, A.agAutos);;
mats := List(gens, a -> List([pc[7], pc[8]], z -> ExponentsOfPcElement(pc, Image(a, z)){[7,8]} * One(GF(p))));;
Gz := Group(mats);;
sc := Filtered([1..p-1], x -> x*IdentityMat(2, GF(p)) in Gz);;
Print("p=", p, " |Aut|=", A.size, " |image on Z|=", Size(Gz), " scalars=", sc, " dets=", Set(List(Elements(Gz), m -> IntFFE(DeterminantMat(m)))), " ", StructureDescription(Gz), " time=", Runtime()-t0, "ms\n");
QUIT;
