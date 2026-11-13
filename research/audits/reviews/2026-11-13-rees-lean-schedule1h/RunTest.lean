import Formal.Schedule1H.Audit
open QSearch.Schedule1H QSearch.Schedule1H.Run
local instance : Fact (Nat.Prime 7) := ⟨by norm_num⟩
#eval (List.finRange 9).map (H prep7 ch7 2 2 9 cols7)
#eval (List.finRange 9).map (H prep7 ch7 2 2 9 (fun i => ![(i : ZMod 7), (i : ZMod 7) ^ 2]))
#eval let c := (fun i : Fin 9 => ![(i : ZMod 7), (i : ZMod 7) ^ 2]); let r := H prep7 ch7 2 2 9 c; (List.finRange 2).map (∑ i, r i ^ 2 • c i)
