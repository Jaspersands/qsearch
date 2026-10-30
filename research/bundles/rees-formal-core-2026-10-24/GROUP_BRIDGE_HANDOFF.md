# Bounded Integration Handoff

The main Developer checkout is still absent. Do not edit the moving
Desktop source, staging, registry, CLI, UI or Git until migration is
verified. All new work here is local outside iCloud.

After verification:

1. Port ReesGroupBridge.lean beside the four existing checked modules.
   It depends on ReesDilation and constructs group maps from a supplied
   base PolynomialGroupLaw; it does not prove Lazard/BCH existence.
2. Preserve all 26 new audit declarations, including groupCover,
   evaluationGroupHom, dilationGroupEquiv, PolynomialGroupLaw and
   actual_tuple_hides. Rebuild source files before accepting an axiom report.
3. Keep the old 99-declaration receipt as historical evidence. The new
   verifier rebuilds that base and requires exact agreement, then audits
   the new module. Do not relabel the old receipt as evidence for new code.
4. Record only the constructed group bridge as checked relative to its
   explicit base law. Keep base BCH, graded quotient chain, efficient SDE
   construction, full quantum execution and natural applications unresolved.
5. Run the actual Lean verification, Python verifier tests and the existing
   Rees physical controls, followed by normal repository validation after
   integration. Do not infer compilation from Python manifest tests alone.

No dashboard change, new search campaign, extra reviewer or frequent commit
is requested. The next high-reasoning task is the actual central certificate
construction, not more finite BCH fixtures or routine wiring.
