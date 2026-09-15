# Convingere, atenție la acuratețe și acțiune

## Ideea centrală

A crede o afirmație și a decide să o distribui sunt rezultate diferite. Distribuirea poate depinde de acuratețe, dar și de recompense sociale, relevanță, identitate, divertisment sau alte motive. M0 separă explicit convingerea [[VAR:B]], ponderea acurateții [[VAR:W]], probabilitatea latentă de distribuire și acțiunea eșantionată [[VAR:Share]].

[[VAR:B]] · [[VAR:W]] · [[VAR:Share]] · [[MECH:accuracy]] · [[VAL:VAL.M0.N01]] · [[REF:REF.PENNYCOOK.2021]] · [[CODE:m0.share_probability]] · [[VIEW:runs:accuracy:5]]

## De la convingere la probabilitatea de acțiune

M0 calculează mai întâi B fără acces direct la ground truth. Apoi un accuracy cue poate deplasa ponderea W printr-o transformare logistică a baseline-ului de acuratețe.

Probabilitatea de distribuire este:

P(Share) = logistic(sharing_bias + W × (2B - 1) + beta_reward × (1 - W) × reward_context).

Inspectează [[CODE:m0.share_probability]].

Ecuația arată de ce B și Share nu sunt sinonime. Când W este mare, acuratețea/convingerea cântărește mai mult în utilitatea acțiunii. Când W este mai mic, reward_context poate avea pondere mai mare. În final, Share este o realizare stocastică din probabilitate; două rulări pot avea aceeași probabilitate latentă și acțiuni observate diferite dacă seed-ul diferă.

## Ce spune literatura despre accuracy prompts

Pennycook și colaboratorii au arătat experimental că mutarea atenției către acuratețe poate îmbunătăți discernământul în intenția de distribuire. O meta-analiză internă ulterioară a 20 de experimente, cu N total 26.863, a găsit o creștere a sharing discernment, în principal prin reducerea intenției de a distribui titluri false.

Această literatură sprijină ideea că acuratețea poate fi subponderată în momentul deciziei de sharing și că un cue poate modifica alegerea. Nu identifică însă W ca stare latentă literală și nu estimează ecuația M0.

## De ce separarea este epistemic importantă

Dacă observăm că cineva distribuie un conținut, nu putem deduce în mod sigur că îl crede. Sharingul poate fi o acțiune socială cu utilități multiple. Invers, cineva poate crede o afirmație și să nu o distribuie. Această disociere limitează inferențele făcute din comportamentul platformei către credințe private.

[[VAL:VAL.M0.N01]] păstrează o frontieră de tip nested-null/ground-truth isolation: decizia trebuie să decurgă din stările agentului și contextul acțiunii, nu din adevărul ascuns al simulatorului.

## Atenție, nu „inteligență”

[[VAR:W]] nu este IQ, System 2, moralitate sau capacitate generală de gândire critică. Este o pondere contextuală a acurateții în politica M0. Accuracy cue nu „face persoana mai inteligentă”; în model, schimbă ce criteriu primește greutate în acel moment.

## Ce nu afirmă acest capitol

Nu afirmă că toate distribuirile de misinformation sunt produse de neatenție și nici că accuracy prompts rezolvă dezinformarea. Efectele reale depind de design, populație, conținut și platformă. De asemenea, intențiile de sharing din experimente nu sunt identice cu comportamentul observat pe platforme.

## În aplicație

Folosește [[VIEW:runs:accuracy:5]] pentru scenariul M0 și [[VIEW:planning]] pentru combinațiile demonstrative de intervenții. Capitolul 10 va introduce un alt outcome, EngageIntent, care trebuie păstrat separat de Share.