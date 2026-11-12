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
- **Not run:** the proof backend (Z3: no empty error, no conflict error). Catala 1.3.0 as built from opam has no `proof`
  command; it needs Catala built with the Z3 bindings. That run is the next measurement of B1.

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
