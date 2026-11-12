# Judging disagreements on step and display links

Two agents (a mapper and an independent verifier) linked each record of a batch to the Lean
formalization [L] by the instructions in `~/tg-companion/scratch/steps2/MAPPER.md`. Read
those instructions first: they define the records, the relations, the output fields, the
sources, and the `decl.py` helper. Do not run `lake` or `lean`.

Your prompt names one or more judge packets `scratch/steps/judge/<batch>.todo.json`; handle each, writing one output per packet. Each lists
- `disputed`: records where the two disagree on the relation's class (table below) or name
  disjoint sets of declarations, with both versions;
- `nomatch_sample`: records both called `noMatch`, with both searches.

| Class | Relations |
|---|---|
| 1-to-1 | exactMatch |
| Faithful | closeMatch, broadMatch |
| Partial | hasPart |
| Deviates | narrowMatch, relatedMatch |
| Absent | noMatch |

For each **disputed** record: read the record's TeX in context and the Lean lines both sides
cite, and search further if neither is right. Rule which side is right, or write your own
version. Never take a relation stronger than you verified by reading the lines.

For each **nomatch_sample** record: run your own search (key declarations, then greps for the
quantity, constants, equation or lemma numbers across `TernaryGoldbach/`). If you find lines
that carry the claim, overturn with a full record.

Write `scratch/steps/judge/<batch>.json`:

```json
{"batch": "<batch>", "rulings": [
  {"id": "<record id>", "kind": "disputed|nomatch_sample",
   "ruling": "mapper|verifier|own|confirmed|overturned",
   "reason": "one or two sentences",
   "record": { full record in the MAPPER.md output schema: the final verdict }}
]}
```

`record` is required in every ruling (copy the side you uphold, correcting any wrong line or
range; for `confirmed`, copy the mapper's record). Text-error claims: keep a side's
`text_error_claim` only if you think it may be right; it will go to skeptics.
Your final reply is at most two lines.

Do all the work yourself: do not launch subagents or tasks.
