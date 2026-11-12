# Against

The evidence against what the idea assumes, and the disagreements. Sources are in [review](review.md). None is deleted
to make the idea look stronger.

**Shape:** [against](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/against.md)

## Against "law is a yes/no question"

- **Open texture.** A general term has a core of settled cases and a penumbra where the rule does not decide; there the
  official exercises discretion ("no vehicles in the park") (Hart 1961, chapter VII, read through a summary). Convention,
  argued; it is the standard position in jurisprudence.
- **Standards against rules.** Many provisions are standards ("reasonable", "proportionate"), which need weighing of
  values that priority rules cannot hold (Abreu, in the Lawsky 2017 summary). Convention.
- **Defeasibility.** A conclusion drawn from a statute can be withdrawn on new information; the answer is yes until an
  exception applies (Lawsky 2017; Prakken 2015). This does not make the question non-binary; it makes it non-monotonic.
- **Discretion is measured.** Who the judge is predicts the outcome (Zambrano 2025); a model per judge beats one model
  for all by ten points of F1. Measured.
- **Strict entailment is not legal reading.** Many legally sound inferences need unstated assumptions (Wang 2026b). Measured.
- **The facts are a question too.** Most disputes turn on what happened, not on what the rule says; a verdict over facts
  nobody established is a verdict over a hypothesis. Convention, the ordinary distinction of fact and law.
- **What survives.** Where the statute is "an algorithm in disguise" (tax, benefits, deadlines, thresholds), the
  question is decidable once the facts are given (Merigoux 2021). The honest form of the hypothesis is three-valued:
  yes, no, or **not decided by the text**, the last being a question for a jurist (Kouteili 2026 measures exactly how
  badly models do this third answer).

## Against "a model can map the law to logic"

- Translations are syntactically valid far more often than they are right: 88.8% valid Catala (Lorenzo 2025, via Heydari
  2026), against 44.4% right on SARA numeric hard cases with Prolog (Dou 2026a). The two numbers measure different things.
- Even the hand-written reference programs of a benchmark had flawed legal reasoning and were rewritten (DeonticBench 2026).
- Two encodings that look alike can decide differently; structural agreement does not predict agreement of decisions (Vernie 2026).
- A model can claim the solver's authority for an answer the solver did not give (Wang 2026b).
- Every formalisation makes interpretive choices; with a model as author they are hidden (Vernie 2026; McBride 2024).

## Against "Lean is the right tool"

- The verdict on a case is computed by running the encoding; Catala, Prolog and ASP already do that, with explanations.
  A proof assistant adds proofs of properties about the statute (no cliff, monotonicity, two encodings equal), not the verdict.
- No Lean library of statutes with public code was found; the two Lean projects seen have no code reachable (MSR 2022, lawlib 2026).
- Lean has no default logic built in; exceptions must be encoded, where Catala has them as a construct.

## Disagreements

| Point | One side | Other side |
|---|---|---|
| Is a model's encoding good enough? | 60% of model pathways rated as good as or better than manual ones (Janatian 2023) | best 44.4% on hard SARA numeric (Dou 2026a) |
| Does a solver make a model faithful? | neuro-symbolic generalises better on unseen variations (Kordjamshidi 2026) | formal structure raises accuracy without faithful reasoning (Wang 2026b) |
| Should law be code at all? | code finds bugs in the official implementation (Merigoux 2021) | code changes the law's effect and contestability (McBride 2024) |

- A possible reason for the first split: pathways for a lay decision aid are judged by people on readability, a SARA
  case on an exact number.

## Against the sources themselves

- Nearly every figure was read in an abstract or a search summary; none was checked in the paper.
- Most strand 3 papers are 2025 to 2026 preprints from a few groups (Johns Hopkins for SARA and DeonticBench).
- COLIEE's official tables were not read; its numbers here come from participants.
- lawlib could not be reached; it is recorded and not relied on.
- One reviewer, a model, with no second rater.
