# Coverage classes

Each record (an item, a display, or a proof step) has one key relation: for an item, the
strongest relation of its key links; for a display or a step, its own relation. The relation is
the record's claim about the Lean ends it names (subject: the text; object: the Lean), with
`broadMatch` meaning the Lean is more general and `narrowMatch` that the text is.

| Class | Relations | Meaning |
|---|---|---|
| **1-to-1** | `exactMatch` | [L] states or establishes exactly this |
| **Faithful** | `closeMatch`, `broadMatch` | the same up to a named difference, or [L] proves more |
| **Partial** | `hasPart` | [L] carries part of it |
| **Deviates** | `narrowMatch`; a confirmed finding or erratum; `relatedMatch` where [L] argues differently | [L] proves less, or something else, or the text is wrong |
| **Absent** | `noMatch` | searched for, not in [L] |
| **Unjudged** | none | no completed verdict |

**Formalized** means 1-to-1 + Faithful. Every percentage is reported with its count, as
"41/52 (79%)".

The display and step mappings are in `data/<overlay>-steps-mapping.json` and
`data/<overlay>-displays-mapping.json`; each record carries its `class` and a `verification`
field saying which checks ran and whether they agreed.
