import Lake
open Lake DSL

-- Results of H. A. Helfgott, *The ternary Goldbach problem* (arXiv:1501.05438v2), stated as
-- printed, each with its relation to calr3/ternary-goldbach proved where it holds.
package TGCompanionStatements

require TernaryGoldbach from git "https://github.com/calr3/ternary-goldbach" @ "192ca57362fa3ee737cd83205cb9ea99526c4553"

@[default_target] lean_lib Companion where
  -- an unknown name is an error, not a new variable
  leanOptions := #[⟨`autoImplicit, false⟩]
