# 0004: New code under AGPL-3.0, what is published stays Apache-2.0

**Decision:** code added after this record is merged is licensed AGPL-3.0-or-later; every file published before it, on
any branch, stays under Apache-2.0, edits included. Prose stays under CC BY 4.0.

**Status:** accepted, 2026-11-17; the cut is the commit that merges this record. **Shape:** [decision record](https://github.com/Tewf/reader-ergonomics-software-design/blob/8896e91b1a354a565bb0266a26b314329d82db98/shapes/decision-record.md).
**Proposed in:** an audit of what the public repositories give away, read by the maintainer.

## Context

This repository is the open part of an offer sold as a subscription: the encodings stay public, and the subscription
sells their updates, reviewed by a jurist, with hosting and support. Under Apache-2.0 anyone may take the code, close a
copy and sell it as a service. Red Hat publishes under licences of the GPL family; MongoDB and Elastic changed their
licences for this case. A licence already granted cannot be taken back from copies made under it.

## Decision

- A file added after the cut opens with `SPDX-License-Identifier: AGPL-3.0-or-later`; the licence text is
  [LICENSES/AGPL-3.0-or-later.txt](../LICENSES/AGPL-3.0-or-later.txt).
- A file published before the cut keeps Apache-2.0 ([LICENSE](../LICENSE)), whoever edits it later.
- Section 13 of the AGPL is the reason for the choice: whoever runs a modified version as a network service must offer
  its users the source.

## Options

| Option | Consequences | Outcome |
|---|---|---|
| Apache-2.0 for everything | one licence, the widest reuse; a competitor may close a copy and sell it | rejected |
| AGPL-3.0 for new code, Apache-2.0 kept | a service built on new code must open its changes; two licences in one tree, by file | chosen |
| Relicense everything under AGPL-3.0 | copies already taken stay Apache-2.0 anyway; one file would carry two histories | rejected |
| A source-available licence (SSPL, BSL) | stronger protection; not open source, which the offer promises | rejected |

## Consequences

- Good: a competitor offering a modified service must publish its changes to the new code.
- Bad: two licences in one tree, read file by file; some firms refuse AGPL code.
- To keep it true: every new code file carries its SPDX line; the legal agent follows the same cut.

## See also

[decisions/](README.md) · [README, Licence](../README.md#licence).
