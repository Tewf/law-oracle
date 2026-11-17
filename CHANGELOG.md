# Changelog

The releases this repository pins, newest first, in the form of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
A pin move is recorded here, not in decisions/.

## Unreleased

### Changed

- The licence of new code: AGPL-3.0-or-later from decision 0004; what is published stays Apache-2.0.
- Pinned reader-ergonomics v1.24.3 (`722cfa4`), from v1.24.2 (`65e4247`): a server error is a warning in the online
  reference run, so a site that is down no longer fails the weekly job.

### Added

- The site: Quarto renders the README and every page, with the standard's stylesheet at its pin, and `pages.yml`
  publishes it to https://tewf.github.io/law-oracle/ on every push to master, as the family's other members do.

- Pinned reader-ergonomics v1.24.2 (`65e4247`), at the repository's start: the standard's pin, link, changelog and
  decision-record checks, which this skeleton is written to pass.
- B1's first run: Catala 1.3.0 on catala-examples `9e251b9`, in evidence/baseline-runs.md.
- The review of statutes as code, in the shapes of reader-ergonomics-review v0.1.1 (`39d3b25`), and decisions 0001 to 0003.
