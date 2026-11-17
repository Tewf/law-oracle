Catala (French syntax) in four lines of grammar, shown on an unrelated toy provision, a library's free membership.

Declarations (already written for you in the real task, so you only write the rules):

```catala
déclaration énumération Statut:
  -- Étudiant
  -- Salarié
  -- Retraité

déclaration structure Adhérent:
  donnée statut contenu Statut
  donnée revenu_mensuel contenu argent
  donnée date_de_naissance contenu date

déclaration champ d'application Bibliothèque:
  résultat gratuité condition dépend de adhérent contenu Adhérent
  résultat âge_minimum contenu durée
  interne seuil contenu argent
  entrée date_courante contenu date
```

Rules, for the same toy: « a student is free; a worker is free if the monthly pay is at most the threshold and the member is old enough; the minimum age is sixty years; the threshold is 40 % of 3 000 euros ».

```catala
champ d'application Bibliothèque:
  définition âge_minimum égal à 60 an

champ d'application Bibliothèque:
  définition seuil égal à 3000€ * 40%

champ d'application Bibliothèque:
  règle gratuité de adhérent
  sous condition adhérent.statut sous forme Statut.Étudiant
  conséquence rempli

champ d'application Bibliothèque:
  règle gratuité de adhérent
  sous condition
    adhérent.statut sous forme Statut.Salarié
    et (adhérent.revenu_mensuel <= seuil)
    et (adhérent.date_de_naissance + âge_minimum <= date_courante)
  conséquence rempli
```

Grammar to keep in mind: a block opens with `champ d'application <Scope>:`; a value is given by `définition <nom> égal à <expression>`; a condition that holds in some cases is given by `règle <nom> de <paramètre> sous condition <test> conséquence rempli` (one rule per case; where no rule holds, the condition is false); an enumeration case is tested with `<valeur> sous forme <Enum>.<Cas>`; tests combine with `et`, `ou`, `non`; money is written `1000€`, a rate `55%`, a duration `20 an`, a decimal `169,0`; a date plus a duration is a date, and dates compare with `<`, `<=`, `>`.
