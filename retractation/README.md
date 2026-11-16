# Retractation: the right of withdrawal from a distance sale

The first encoding of our own: the French consumer's right to withdraw from a contract concluded at a distance,
written in Catala from the articles of the Code de la consommation. For one case it answers three questions: does
the right exist, on which day does the period end, and was a withdrawal sent on a given day in time.

> **Status (2026-11-16):** it compiles, and its 35 tests pass (`clerk test`). A grid of 148,256 cases raises no empty
> and no conflict error, and agrees with a second reading written in Python on the right, the end of the period and
> 2,075,584 verdicts on a withdrawal. Catala's proof backend has not run on it: Catala 1.3.0, as built here, has no
> Z3 bindings. Nothing here is legal advice.

## What it encodes

| Article | What it decides | In the code |
|---|---|---|
| L. 221-18 | 14 days, from the conclusion (services, L. 221-4) or the reception (goods); last item, or first for regular delivery; an order not fully received has not started the period | `jour_de_départ`, `délai_commencé`, input `réception_complète` |
| L. 221-19 | the start day is not counted; an end on a Saturday, Sunday or holiday moves to the next working day | `fin_du_délai_initial`, scope `JourOuvrable` |
| L. 221-20 | no information on the right: 12 more months; information supplied during them: 14 days from its reception | `fin_du_délai` |
| L. 221-21, al. 1 | a withdrawal is sent before the period, as extended, expires | `dans_le_délai` |
| L. 221-28 | eight kinds of contract with no right (2°-4°, 7°, 8°, 10°-12°); five events that end it on their date (1°, 5°, 6°, 9°, 13°) | `cas_l221_28` |

The twelve months are counted by regulation 1182/71, art. 3(2)(c): the same day number twelve months later, or the
last day of the month when it has none. Catala calls that `date arrondi inférieur`.

## Readings chosen

| Question | Reading | Why |
|---|---|---|
| Do the 12 months start from the initial end before or after it moves to a working day? | after | L. 221-19 is how the L. 221-18 period is computed; the regulation applies to the directive's art. 9(2) (recital 41). To confirm by the legal agent |
| Does the directive's 12-month window move to a working day? | yes | it is a period under the same regulation, art. 3(4) |
| Does L. 221-20 compare the day the information is supplied, or received? | supplied, for the window; received, for the 14 days | « lorsque la fourniture de ces informations intervient pendant cette prolongation », then « à compter du jour où le consommateur a reçu ces informations » |
| Is a withdrawal sent on the start day in time, though the period runs from the next day (L. 221-19, 2°)? | yes, for goods and services | L. 221-21 sets only an upper bound, « avant l'expiration »; the a contrario of L. 221-18, 2°, reaches only a sending before the reception, and only for goods |
| Do the 12 months end on the day number of the initial end, or of the day after? | of the initial end | regulation art. 3(2)(c) counts from « le jour de départ », the day of the event, as L. 221-19 does for the 14 days (from the 5th, the 19th) |
| One order, several goods, one of them unsealed (5°): is the whole order excluded? | yes, the verdict is for the contract as given | the text names « biens » without saying whether per item; to judge item by item, run the encoding on each part of the order |
| Is information supplied on the start day inside the directive's window? | no: both texts give the full extension | regulation 1182/71, art. 3(1): the day of the event is not counted, so the window opens the next day |

## What the text does not decide

In four cases the encoding returns `NonDécidé` with the question, never a yes or a no.

- When the question is which of two ends applies, the end is a `Fourchette` holding both.
- A withdrawal sent by the earlier end is `Oui` under both readings; one sent after the later end is `Non` under both.
- Only the days between stay undecided.
- When several questions are open for one withdrawal, the first in the order of the checks is returned. Two come from L. 221-20 counting
differently from the directive it transposes, which allows no difference (directive 2011/83, art. 4).

| Case | What each text says |
|---|---|
| information supplied after the start day, no later than the end of the initial period | L. 221-20: not "during the extension", so 12 months; directive art. 10(2): 14 days from its reception |
| information supplied during the extension, after the 12 months counted from the start day | L. 221-20: 14 days from its reception; directive art. 10(1): the end of the extension |
| goods: withdrawal sent after the conclusion and before the reception, the start day | L. 221-18, 2°, allows exercise from the conclusion only « pour les contrats conclus hors établissement », which suggests a contrario that it is too early; L. 221-21 sets only an upper bound, « avant l'expiration » |
| the event of L. 221-28, 1°, 5°, 6°, 9° or 13° falls on the day the withdrawal is sent | the texts count in days; which came first that day is a fact of the hour |

Information supplied after the conclusion and no later than the start day is decided: neither text shortens the 12 months.

## Out of scope

- Off-premises contracts and telephone canvassing: the same article, with other start rules.
- The effects of withdrawal (L. 221-23 to L. 221-27).
- Establishing the facts of the case. Whether a perfume is "nettement personnalisé" (L. 221-28, 3°) is a fact the
  caller gives, as are the conditions of 1° and 13° (express consent, acknowledged loss of the right and, for 13°, the
  trader's confirmation). The encoding asserts that the dates come in order: receptions and events after the
  conclusion; 1° on a service, 13° on digital content, 5°, 6° and 9° on goods after a reception.
- Regulation 1182/71, art. 3(5), at least two working days in any period of two days or more: L. 221-19 does not
  take it, and it matters only if 13 of the 14 days are holidays.
- Holidays: they are an input, since they depend on the place (Alsace-Moselle has two more).

## Layout

- [Retractation_distance.catala_fr](Retractation_distance.catala_fr): the articles and their code, in one literate file.
- [tests/](tests/tests_retractation.catala_fr): 35 cases computed by hand from the articles, with the edge of each
  L. 221-20 branch, in the folder `clerk.toml` names for them.
- [enumerate.py](enumerate.py): the grid of cases, compared with a second reading in plain Python.
- [sources/](sources/): the texts as read, each with its identifier and the date it was read.

## To run it

From the repository root, in the `law-oracle` environment of [the baseline runs](../evidence/baseline-runs.md):

```sh
clerk test
clerk build && python3 retractation/enumerate.py
```

The second command takes about 35 minutes. Both readings were written by the same author and share every reading
chosen above, so their agreement shows that the code does what that reading says, not that the reading is right.
