# Protocol: how the pool was built

A first pass, run on 12 Nov. 2026 by one reviewer, a model, in one session. Terms are in [frame](frame.md).

**Shape:** [protocol](https://github.com/Tewf/reader-ergonomics-review/blob/39d3b25cd822a20277ee39c37b9e0130439802f2/shapes/protocol.md)

## 1. Why grey literature

Garousi's questions, answered for this topic:

- Is the subject complex and not solvable by formal sources alone? Yes: the languages (Catala, Blawx, L4, Logical
  English, OpenFisca) live in repositories, and their adoption is in government pages, not papers.
- Is there a lack of volume or quality of formal evidence on practice? Yes: no paper counts who uses Catala in production.
- Is the context important? Yes: what an administration runs decides the baseline.
- Does practice run ahead of research? In part: OpenFisca has run French simulators for years; the LLM papers are from 2023 on.

## 2. Questions

- Q1 What exists to write a statute as code, and who uses it?
- Q2 Is a legal question a yes/no question?
- Q3 Can a model translate a statute into logic faithfully, and how is that measured?
- Q4 Can the verdict be translated back into language?
- Q5 Has Lean, or another proof assistant, been used on law, and what does it add?

## 3. Existing reviews

- Found: Prakken 2015 (law and logic, from argumentation); Grimmelmann 2022 (programming languages and law, a research
  agenda); Shao 2025 (LLMs in law, a taxonomy); the COHUBICOL study on computational law (McBride 2024).
- Not found: a review of LLMs translating statutes into a formal language that is executed, with fidelity measured.
  The nearest are the primary papers of strand 3.

## 4. Formal search

arXiv, through its API, title and abstract, no identity sent; counts on 12 Nov. 2026.

| Id | String as run | Count | New concept |
|---|---|---|---|
| F3 | "large language models" AND (statute OR legal) AND (formalization OR "logic programming" OR Prolog OR "answer set") | 20 | yyyyyyyyyynyyyyyynyy |
| F4 | (Lean OR Coq OR Isabelle OR "proof assistant") AND (legal OR law OR statute OR contract) | 20 | yynnnnynynnynynnnnnn |
| F5 | Catala AND ("large language model" OR LLM OR GPT OR translation) | 6 | nnnnyy |
| F6 | au:Jurayj OR au:Holzenberger OR ti:"statutory reasoning" | 12 | yyynyyynynnn |
| F7 | (autoformalization OR "semantic parsing" OR "natural language to logic") AND (legal OR law OR statute OR regulation) AND (SMT OR Z3 OR "first-order logic" OR Lean), from 2023 | 5 | nynny |
| F8 | (survey OR review) AND ("neuro-symbolic" OR "logic") AND ("legal reasoning" OR "legal AI") AND ("large language models"), from 2024 | 1 | n |
| F9 | (informalization OR "natural language generation" OR verbalization OR explanation) AND (legal OR statute OR "rules as code") AND (logic OR Prolog OR Catala OR proof) | 12 | nnnnynnnnnny |
| F10 | (Lean OR "proof assistant" OR "theorem prover" OR "dependent types") AND (legal OR law OR statute OR regulation OR compliance) AND ("language model" OR LLM OR autoformalization), from 2023 | 15 | ynnnnnnynyynnnn |

The letters are computed from the log of every result, with its concepts, in [search-log.csv](search-log.csv).

## 5. Grey search

A web engine (the session's search tool) and GitHub's search, through `gh`, no identity beyond the maintainer's token.

| Id | Producer or engine | String or what was read | Result | New concept |
|---|---|---|---|---|
| F1 | web | survey computational law rules as code formalization legislation programming languages | 10 screened, 4 kept | yyyy |
| F2 | web | Catala programming language law Merigoux Chataing Protzenko French tax code | 17 screened, 2 kept | yy |
| G1 | web | L4 legal DSL Logical English Kowalski Datoo Singapore Management University CCLAW | 10 screened, 1 kept | y |
| G2 | web | LegalRuleML OASIS standard defeasible deontic logic Governatori Palmirani | 10 screened, 1 kept | y |
| G3 | web | Blawx s(CASP) rules as code Jason Morris answer set programming legislation | 17 screened, 1 kept | y |
| G4 | web | COLIEE 2025 competition legal entailment task 4 statute law yes/no results | 10 screened, 1 kept | y |
| G5 | web | Lean 4 theorem prover formalization of law statute legal reasoning | 10 screened, 1 kept | y |
| G6 | web | SARA statutory reasoning assessment Holzenberger Blair-Stanek Van Durme Prolog tax GPT-4 fails | 10 screened, 1 kept | y |
| G7 | web | LegalBench Guha 2023 162 tasks legal reasoning benchmark rule-application yes/no | 10 screened, 1 kept | y |
| G8 | GitHub | `gh search repos` "lean4 law", "statute lean", "catala llm", "rules as code" | 0, 0, 0, 15 | y |
| G9 | web | "lawlib" Lean 4 policyengine EITC verified twin | 10 screened, 1 kept | y |
| G10 | web | Sergot Kowalski 1986 British Nationality Act as a logic program | 19 screened, 1 kept | y |
| G11 | web | Prakken Sartor "Law and logic: A review from an argumentation perspective" 2015 | 10 screened, 1 kept | y |
| G12 | web | Hart open texture of law computational law critique rules as code Diver Hildebrandt COHUBICOL | 20 screened, 1 kept | y |
| G13 | web | Lawsky "A logic for statutes" default logic tax law Florida Tax Review 2017 | 10 screened, 1 kept | y |
| G14 | web | large language model generate Catala code from statute translation evaluation 2025 | 20 screened, 1 kept | y |
| G15 | web | OpenFisca France rules as code adoption Catala DGFiP CNAF production use | 15 screened, 1 kept | y |
| G16 | GitHub | the trees of CatalaLang/catala and CatalaLang/catala-examples, and the org's repositories | 1 read | y |
| G17 | web | COLIEE 2024 overview task 4 legal textual entailment accuracy best team | 10 screened, 1 kept | n |
| G18 | web | Logical English large language models translate legislation Kowalski Davila 2024 LLM | 10 screened, 1 kept | y |
| G19 | GitHub | `gh search repos` for ten names of strand 3 (DeonticBench, SARA, LegalBench, COLIEE...) | 40 screened | n |
| G20 | GitHub | guangyaodou/DeonticBench README | 1 read | y |
| G21 | arXiv | 2605.16052 abstract, from G18 | 1 read | y |
| G22 | arXiv | 2605.25186 abstract, from G14 | 1 read | y |
| G23 | web | Bench-Capon Coenen isomorphism principle legal knowledge based systems | 10 screened, 1 kept | y |
| G24 | web | Hart "Concept of Law" 1961 open texture vehicles in the park Waismann | 10 screened, 1 kept | y |

The web engine returns a synthesis with its links, not a ranked list: one letter per row stands for the synthesis.

## 6. Stopping rule

- **Effort bounded**: one session, about 35 strings, set after the first batch rather than before it, which the shape
  does not allow; it is reported here as a departure.
- The stopping estimator of ai-augmented-data-gathering, run on the log: 121 results, 34 strings, 121 concepts;
  coverage 0.62 (abundance) and 0.52 (incidence) against a target of 0.95. Its verdict: keep searching. The family's
  rule (stop after 5 results with no new concept) fired at result 50. The two disagree.
- The search was stopped on the effort bound with coverage 0.62, because the five questions each have an answer and a
  baseline with code. The unseen mass, 0.38, is a limit of this pass (section 10).

## 7. Selection

- Include: a method, a benchmark, a tool or a critique that bears on Q1 to Q5, for statutes or regulations.
- Exclude: smart contracts on blockchains (verification of programs, not of law); legal judgment prediction from past
  cases with no rule encoded; retrieval of cases.

## 8. Quality of grey sources

The 20 criteria of Garousi 2019, Table 7, in eight groups (authority 4, methodology 6, objectivity 4, date 1,
position 1, novelty 2, impact 1, outlet 1). Threshold 10 of 20 to support a claim; below, an example of practice only.

## 9. Extraction and synthesis

- Formal sources read from the abstract; figures from an abstract are marked secondary. No PDF was read in full.
- Repositories read from their README and their file tree, through the GitHub API.
- Synthesis by strand, narrative, by the one reviewer.

## 10. Not searched, and limits

- Not searched: Google Scholar, DBLP, SSRN and HeinOnline (law reviews); the JURIX and ICAIL proceedings directly; French
  sources in French (Légifrance doctrine, Revue française d'administration publique); COLIEE's official results tables.
- Limits: one reviewer, a model; one day; abstracts only; the estimator says 38% of the concept mass is still unseen.
- No second rater.
- Not recorded: the web engine returns a synthesis, so its rows carry one letter for the synthesis, not one per result.
