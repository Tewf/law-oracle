# Baseline runs

B1 run as it is, before any encoding of our own, so later work is compared with numbers measured here and not only
read in a paper. The baseline and its measure are named in [statutes-as-code/baseline.md](statutes-as-code/baseline.md).

## B1: Catala on its French encodings, 2026-11-12

| Item | Value |
|---|---|
| Catala | 1.3.0, from opam, OCaml 5.2.1, in a conda environment with opam 2.6.1 from conda-forge |
| Encodings | [CatalaLang/catala-examples](https://github.com/CatalaLang/catala-examples) at `9e251b9` |
| Machine | i5-12450H, Ubuntu 24.04 |

| Run | Tests passed | Time |
|---|---|---|
| `clerk test allocations_familiales/tests` | 31 of 31, interpreted | 1.7 s |
| `clerk test`, the whole repository (12 folders, French and US law) | 189 of 189, interpreted | 5.1 s |

- The tests are the encodings' own: each a case written by their authors with its expected result. They show that the
  encodings run as their authors meant; they say nothing about fidelity to the text beyond those cases.
- The proof backend was run on 2026-11-16: see [the proof runs](#b1-the-proof-backend-2026-11-16).

## B1: the proof backend, 2026-11-16

The plugin `catala-proof` 1.3.0 (`catala proof FILE`, Z3 through its OCaml bindings) turns each variable of a scope into two conditions: it never returns an empty error, and no two exceptions overlap.
It prints a warning for a variable that fails one, and "No errors found" for a program with nothing to report.

| Item | Value |
|---|---|
| Plugin | `catala-proof` 1.3.0, built from the tag 1.3.0 of [CatalaLang/catala](https://github.com/CatalaLang/catala), beside Catala 1.3.0 in the same opam switch |
| Solver | opam `z3` 5.1.0 (OCaml bindings, built from source in 8 min 22 s); the Ubuntu package z3 4.8.12 is not used |
| Encodings | family allowances at `9e251b9` (`allocations_familiales/Allocations_familiales.catala_fr`, with the include folders of its `clerk.toml`); the withdrawal right from a distance sale at `64f3aad` (branch `law-5-retractation`, `retractation/Retractation_distance.catala_fr`) |

| Run | Conditions | Solved, no empty or conflict case found | Solved, a case found | Not translated to Z3 |
|---|---|---|---|---|
| family allowances, `catala proof` | 100 (50 variables, 2 each) | 75 | 0 | 25 |
| withdrawal right, `catala proof` | 32 (16 variables, 2 each) | 4 | 0 | 28 |

- **Empty and conflict cases reported: none, in either run.** The backend found no case; it also could not look at 25 and 28 conditions, so the result is not a proof of the encodings.
- Not translated, family allowances (25 conditions, 16 variables): `ErrorOnEmpty unsupported` for 17, `TArrow type not supported` for 7 (a function value, in the variables `droit_ouvert_complément`, `montant_initial_base` and
  `montant_initial_base_premier_enfant`, `montant_initial_majoration`), and one duration with years or months (`âge_minimum_alinéa_1_l521_3`). The two `PrestationsFamiliales` variables `droit_ouvert` and `conditions_hors_âge` are among them.
- Not translated, withdrawal right (28 conditions, 14 variables): all `Ill-formed operator application: is_Absent`, for `après_une_réception`, `dans_le_délai`, `droit_de_rétractation`, `délai_commencé`, `exclu_par_son_type`, `fin_après_information`,
  `fin_douze_mois_du_départ`, `fin_du_délai`, `fin_du_délai_initial`, `fin_initiale`, `fin_prolongation`, `jour_de_départ`, `perdu_avant` and `perdu_le_jour`. The four solved conditions are those of `fin` and `est_ouvrable`.
- With `-O` the family-allowances run stops on an internal error of the condition generator (`this expression does not have the structure expected`, in `prologue.catala_fr` line 143); a run with `--avoid-exceptions -O` did not finish in 900 s.
- **Does the backend flag a real case?** It does, on Catala's own proof tests (`tests-extra/proof` at the tag). 18 of 19 good files give "No errors found". 25 of 28 bad files are flagged ("This variable might return an empty error", or an overlap).
  The other three bad files stop before the prover: two are compile errors in the source as written, and one hits the same translation limit. So "none found" on the encodings is a result of a solver that flags cases when it can read them.
- Time: 0.64 s for the family allowances, 0.23 s for the withdrawal right, no counterexample search disabled.

What this means for the next step: the backend cannot read an encoding written with exceptions that may be empty, with functions as values or with optional values, which is most of both. To get a verdict on them, either the encodings are rewritten into the
fragment the backend supports, or the backend is extended; the first costs fidelity to the text, the second is work on Catala.

## To run it again

```sh
conda create -n law-oracle -c conda-forge opam=2.6.1 python=3.12 gmp pkg-config
conda activate law-oracle
export OPAMROOT=$CONDA_PREFIX/opam OPAMSWITCH=catala C_INCLUDE_PATH=$CONDA_PREFIX/include LIBRARY_PATH=$CONDA_PREFIX/lib
opam init --bare --disable-sandboxing -n
opam switch create catala ocaml-base-compiler.5.2.1
opam install catala
eval $(opam env)
git clone https://github.com/CatalaLang/catala-examples && cd catala-examples && git checkout 9e251b9
clerk test allocations_familiales/tests && clerk test
```

The conda compiler does not search the system's headers, hence `gmp` from conda-forge and the two include variables;
without them zarith fails on `gmp.h`.

The proof backend, in the same switch:

```sh
opam install z3
git clone --branch 1.3.0 --depth 1 https://github.com/CatalaLang/catala && cd catala && opam install ./catala-proof.opam
cd ../catala-examples && clerk start
catala proof -I "$(python3 -c "import tomllib; print(':'.join(tomllib.load(open('clerk.toml','rb'))['project']['include_dirs']))")" allocations_familiales/Allocations_familiales.catala_fr
```
