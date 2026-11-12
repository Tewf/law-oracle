# Review: six strands

Step 2 of the review, read on 12 Nov. 2026. It groups the 46 sources by strand and answers Q1 to Q5 of
[frame](frame.md). Surveys first in each strand.

**Shape:** [review](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/review.md)

- Each key is in the [bibliography](../bibliography.md).
- Grades are the standard's four.
- A figure read in an abstract is marked (secondary).

## Strand 0: existing reviews

- Legal applications of logic have moved from deduction over rules to argument about rules: applying a statute to an
  unforeseen case and interpreting it are modelled as argument, not proof (Prakken 2015, abstract, secondary). Supported with caveat.
- Programming languages and law is a research agenda with ten avenues; legal logic programming adds defeasibility, and
  the French tax code ran on a language of its own, M (Grimmelmann 2022, abstract and search summary, secondary). Convention.
- The COHUBICOL study places rules as code on a spectrum: the more the code replaces the text, the more it changes the
  law's effect and its contestability (McBride 2024, chapter summary, secondary). Convention.
- A survey of LLMs in law maps legal roles to NLP tasks; it names hallucination and explainability as open (Shao 2025, abstract, secondary). Convention.
- No review of models translating statutes into an executed formal language, with fidelity measured, was found
  (protocol, strings F3, F7, F8). Not found, in these searches.

## Strand 1: writing a statute as code (Q1)

- The seminal work: a large part of the British Nationality Act 1981 written as an extended Prolog program, executed to
  decide citizenship (Sergot 1986, search summary, secondary). Measured, descriptive.
- **Catala** writes a statute as literate code beside its text, with default logic as a first-class feature for
  exceptions; its compiler's core steps are proved in F*; on French family benefits it found a bug in the official
  implementation (Merigoux 2021, abstract, secondary). Measured, descriptive.
- Catala's repository holds a proof backend that sends Z3 one verification condition per definition, absence of empty and of conflict errors
  (`compiler/verification/`),
  a Rocq mechanisation of its default calculus (Catala 2026c), a trace explainer (Catala 2026b), and French encodings:
  housing aids, family allowances, income tax, minimum wage, inheritance (Catala 2026a, file tree read 12 Nov.). 2,444 stars,
  pushed on 12 Nov. 2026; the README calls the compiler unstable. Measured, descriptive.
- `catleg` reads French statutes through the Légifrance API for Catala work (Catala 2026d, README). Measured, descriptive.
- Statutory reasoning is better modelled by default logic than by deduction: default rules and priority rules (Lawsky 2017,
  search summary, secondary). Convention, argued; contested for provisions that are standards (Abreu, in the same summary).
- LegalRuleML is the OASIS standard for legal norms in XML, with defeasible rules, strengths and an override relation
  (OASIS 2021, specification module read). Convention.
- Logical English is a controlled English that runs as Prolog (Kowalski 2021, search summary, secondary); its repositories
  are active, 52 and 15 stars (LogicalEnglish 2026). Measured, descriptive.
- Blawx is a visual editor over s(CASP), goal-directed answer set programming, with explanations and hypotheticals
  (Morris 2023, search summary, secondary); last pushed November 2024. Measured, descriptive.
- OpenFisca runs French public simulators (Mes Aides) and other countries' (OpenFisca 2026, page and repository: 252 stars).
  The DGFiP published its income-tax code in M (Merigoux 2021b). Measured, descriptive.
- That an administration runs Catala in production was not confirmed (protocol, G15). Not found, in these searches.

## Strand 2: is a legal question yes/no? (Q2)

- COLIEE Task 4 asks yes/no entailment from Japanese Civil Code articles supplied with the question; the 2024 winner voted
  three prompts of flan-T5, among 8 teams and 24 runs (Kano 2024, slides, secondary). The winning accuracy was not read. Measured.
- LegalBench has 162 tasks in six kinds, including rule application, rule conclusion and interpretation, built by legal
  professionals; 20 models evaluated (Guha 2023, abstract, secondary). Measured.
- When facts are missing, models fail to abstain: frontier models give the right verdict 89 to 92% of the time on
  complete paths, and 22 to 40% when the right answer is "not enough information" (Kouteili 2026, abstract, secondary). Measured.
- A re-annotation of ContractNLI finds a measurable gap between pragmatic legal reading and strict formal entailment:
  many legally sound inferences need unstated assumptions (Wang 2026b, abstract, secondary). Measured.
- The judge is a variable: on 18,937 French custody rulings, models per judge reach F1 92.85 against 82.63 for one model
  for all (Zambrano 2025, abstract, secondary). Measured.
- Judges' philosophy of law changes how the same statute is read (Zheng 2026, abstract, secondary). Convention, a benchmark.

## Strand 3: a model translating a statute into logic (Q3)

- On SARA (9 tax sections, 376 cases), a hand-written Prolog program solves the task; neural readers do not
  (Holzenberger 2020, abstract, secondary). GPT-4 gets 67% of the true/false cases (Blair-Stanek 2023, search summary, secondary). Measured.
- A model translating the statute into Prolog once, ahead of time, then each case with retrieved exemplars, improves SARA and
  costs less than the real average of tax errors (Jurayj 2025, abstract, secondary). Measured.
- DeonticBench, 6,232 tasks over tax, airline, immigration and housing, with reference Prolog for each; best hard-subset
  score 44.4% on SARA numeric and 46.6 macro-F1 on housing; RL improves Prolog quality but does not solve the tasks
  (Dou 2026a, abstract, secondary). Its reference programs were audited on 26 May 2026 and those with "flawed legal
  reasoning, trivially true logic, or hardcoded outputs" rewritten (DeonticBench 2026, README). Measured.
- Code and data: `guangyaodou/DeonticBench`, 17 stars and pushed 8 Nov. 2026 (GitHub metadata, read 12 Nov.), with hard and smoke splits (DeonticBench 2026, repository metadata and README). Measured, descriptive.
- Generating Catala from French tax law: a benchmark and a training set; few-shot and fine-tuned models make it look
  feasible (Lorenzo 2025, abstract); GPT-4.1 few-shot gave 88.8% syntactically valid Catala (cited by Heydari 2026, secondary).
  Syntax only; no data link found. Measured, secondary.
- L4L: models formalise provisions into SMT constraints, validated by case-level tests, then two adversarial agents
  extract facts and Z3 checks admissibility (Chen 2025b, abstract, secondary). Measured.
- Comparing formalisations by the decisions they encode: nine frontier models formalised ten EU provisions; a SAT solver
  enumerates the edge cases on which two encodings disagree, verbalised for an expert; behavioural divergence is
  uncorrelated with structural agreement (Vernie 2026, abstract, secondary). Measured.
- Defeasible deontic logic from an Australian code, with a refinement step (Horner 2025, abstract, secondary); the Highway
  Code through Logical English, three of four rules right (Dal Pont 2025, search summary, secondary). Measured, small.
- Neuro-symbolic systems generalise better than monolithic models on unseen tax variations, and contamination inflates the
  monolithic scores (Kordjamshidi 2026, abstract, secondary). Measured.
- Two extractors of the same statutes disagree on numeric thresholds at a false-negative rate of 0.43 (Saka 2026, abstract, secondary). Measured.
- The relation that fidelity asks for has a name since 1992: **isomorphism**, one well-defined correspondence between the
  knowledge base and the source texts (Bench-Capon 1992, search summary, secondary). Convention.

## Strand 4: saying the verdict back (Q4)

- Catala ships `catala-explain`, explanations from the trace of a run, and a prototype that writes individual
  explanations for the French state's design system (Catala 2026b, README). Measured, descriptive.
- Edge cases where two encodings disagree are verbalised into concrete scenarios for an expert (Vernie 2026). Measured.
- An architecture extends Catala, has a model autoformalise, a kernel verify, and writes the explanation from the proof
  trace; for open-textured analysis it guarantees structure, not outcome (Heydari 2026, abstract, secondary). Convention, a design with demonstrations.
- ASP models of the Italian criminal code explain through the supportedness of stable models (Dovier 2026, abstract, secondary). Measured, descriptive.
- Models report solver-inconsistent answers as if the solver had decided, "scope laundering", in all five models tested
  (Wang 2026b, abstract, secondary). Measured.

## Strand 5: Lean and other proof assistants on law (Q5)

- A Microsoft Research talk (18 Oct. 2022) used Lean to formalise and find bugs in French family benefits and Washington
  State's legal financial obligations, and to find a path through US civil procedure's pleading phase (MSR 2022, page read; no code or paper linked). Measured, descriptive.
- lawlib was described as a Lean 4 library of law, a verified twin of PolicyEngine US for the EITC, differentially tested (snippets, secondary)
  each night, with a Catala encoding of §32 compared to the administered version (lawlib 2026, search snippets only).
  The repository returned "could not resolve" on 12 Nov. 2026. Unverifiable.
- Isabelle with LogiKEy modelled value-oriented legal balancing on property cases (Benzmuller 2020, abstract, secondary). Measured, descriptive.
- Lean 4 for patent claims as DAGs with kernel-checked certificates, conditional on ML scores (Koomullil 2026a, abstract, secondary);
  Lean 4 guardrails for financial compliance, a roadmap with no measurement (Rashie 2026, abstract, secondary). Convention.
- A library of mathematical finance in Lean 4 records 804 results with an audit of what each formalisation leaves out
  (Coelho 2026, abstract, secondary). Measured, descriptive; it is the closest model of a faithfulness audit outside mathematics proper.
- No Lean library of statutes with released code was found (protocol, G5, G8, F4, F10). Not found, in these searches.
