import TernaryGoldbach
open Lean Meta Elab Command

/-- Project constants reachable from `root` through types and values. -/
partial def coneOf (env : Environment) (root : Name) : NameSet := Id.run do
  let mut seen : NameSet := {}
  let mut todo := [root]
  while !todo.isEmpty do
    let n := todo.head!; todo := todo.tail!
    if seen.contains n then continue
    seen := seen.insert n
    if let some ci := env.find? n then
      let cs := ci.type.getUsedConstants ++ ((ci.value? (allowOpaque := true)).map (·.getUsedConstants)).getD #[]
      for c in cs do
        if (`TernaryGoldbach).isPrefixOf (privateToUserName? c |>.getD c) && !seen.contains c then todo := c :: todo
  return seen

elab "#dump_index " out:str : command => do
  let env ← getEnv
  let cone := coneOf env ``TernaryGoldbach.ternary_goldbach_of_hypotheses
  let mut arr : Array Json := #[]
  for (n, ci) in env.constants.toList do
    let user := privateToUserName? n |>.getD n
    unless (`TernaryGoldbach).isPrefixOf user do continue
    if n.isInternalDetail || isAuxRecursor env n || isNoConfusion env n then continue
    let last := match n with | .str _ s => s | _ => ""
    if last.startsWith "_proof" || last.startsWith "match_" || last.startsWith "proof_" || last.startsWith "eq_" then continue
    let some modIdx := env.getModuleIdxFor? n | continue
    let modName := env.header.moduleNames[modIdx.toNat]!
    let rng ← liftCoreM (findDeclarationRanges? n)
    let doc ← liftCoreM (findDocString? env n)
    let kind := match ci with
      | .thmInfo _ => "theorem" | .defnInfo _ => "def" | .axiomInfo _ => "axiom"
      | .opaqueInfo _ => "opaque" | .inductInfo _ => "inductive" | .ctorInfo _ => "constructor"
      | .recInfo _ => "recursor" | .quotInfo _ => "quot"
    let tyStr ← liftTermElabM do
      try pure (toString (← ppExpr ci.type)) catch _ => pure "<pp failed>"
    let valHash : Nat := match ci with
      | .defnInfo d => d.value.hash.toNat | _ => 0
    let facts := ci.type.getUsedConstants.filter (fun c => c == ``TernaryGoldbach.PlattGRH ||
      c == ``TernaryGoldbach.BinaryGoldbachInput || c == ``TernaryGoldbach.RamareMoebius ||
      c.toString == "TernaryGoldbach.RHUpTo" || c.toString == "TernaryGoldbach.ButhePsi")
    let isProj := fun (c : Name) => (`TernaryGoldbach).isPrefixOf (privateToUserName? c |>.getD c)
    let tyConsts := (ci.type.getUsedConstants.filter isProj).map toString
    let valConsts : Array String := match ci with
      | .defnInfo d => (d.value.getUsedConstants.filter isProj).map toString | _ => #[]
    arr := arr.push <| Json.mkObj [
      ("name", toString user), ("private", toJson (isPrivateName n)), ("kind", kind),
      ("module", toString modName),
      ("line", toJson (rng.map (·.range.pos.line) |>.getD 0)),
      ("end_line", toJson (rng.map (·.range.endPos.line) |>.getD 0)),
      ("in_cone", toJson (cone.contains n)),
      ("type_hash", toJson ci.type.hash.toNat),
      ("value_hash", toJson valHash),
      ("facts", toJson (facts.map toString)),
      ("type_consts", toJson tyConsts), ("value_consts", toJson valConsts),
      ("doc", toJson (doc.getD "")),
      ("type", tyStr)]
  IO.FS.writeFile out.getString (Json.compress (Json.arr arr))
  logInfo m!"wrote {arr.size} declarations; cone size {cone.size}"

#dump_index "lean_index.json"
