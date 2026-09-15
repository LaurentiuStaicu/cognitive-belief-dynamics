# Convingere, atenție la acuratețe și acțiune

## Ideea centrală

A crede o afirmație și a decide să o distribui sunt rezultate diferite. Distribuirea poate depinde de acuratețe, dar și de recompense sociale, relevanță, identitate, divertisment sau alte motive. M0 separă explicit convingerea [[VAR:B]], ponderea acurateții [[VAR:W]], probabilitatea latentă de distribuire și acțiunea eșantionată [[VAR:Share]].

[[VAR:B]] · [[VAR:W]] · [[VAR:Share]] · [[MECH:accuracy]] · [[VAL:VAL.M0.N01]] · [[REF:REF.PENNYCOOK.2021]] · [[CODE:m0.share_probability]] · [[VIEW:runs:accuracy:5]]

## De la convingere la probabilitatea de acțiune

M0 calculează mai întâi B fără acces direct la adevărul cunoscut de mediul simulat. Apoi, un indiciu care atrage atenția asupra acurateții poate modifica ponderea W printr-o transformare logistică a nivelului de referință al acurateții.

Probabilitatea de distribuire este:

P(Share) = logistic(sharing_bias + W × (2B - 1) + beta_reward × (1 - W) × reward_context).

Formula poate fi inspectată în [[CODE:m0.share_probability]]. Numele precum sharing_bias sau reward_context sunt identificatori ai implementării și sunt păstrați ca atare.

Ecuația arată de ce B și Share nu sunt sinonime. Când W este mare, acuratețea și convingerea au o pondere mai mare în utilitatea acțiunii. Când W este mai mic, contextul de recompensă poate conta mai mult. În final, Share este o realizare stocastică a probabilității: două rulări pot avea aceeași probabilitate latentă și acțiuni observate diferite dacă folosesc semințe aleatoare diferite.

## Ce spune literatura despre indiciile de acuratețe

Pennycook și colaboratorii au arătat experimental că readucerea atenției către acuratețe poate îmbunătăți discernământul în intenția de distribuire. O meta-analiză internă ulterioară a 20 de experimente, cu un total de 26.863 de participanți, a găsit o îmbunătățire a diferențierii dintre conținutul adevărat și cel fals în intențiile de distribuire, în principal prin reducerea intenției de a distribui titluri false.

Această literatură sprijină ideea că acuratețea poate primi o pondere prea mică în momentul deciziei de distribuire și că un indiciu contextual poate modifica alegerea. Nu identifică însă W drept stare latentă literală și nu estimează ecuația M0.

## De ce separarea este importantă epistemic

Dacă observăm că cineva distribuie un conținut, nu putem deduce în mod sigur că îl crede. Distribuirea poate fi o acțiune socială cu mai multe utilități. Invers, cineva poate crede o afirmație și totuși să nu o distribuie. Această disociere limitează inferențele făcute din comportamentul observabil pe platforme către convingeri private.

[[VAL:VAL.M0.N01]] păstrează o frontieră de tip model nul inclus și izolare a adevărului din simulare: decizia trebuie să rezulte din stările agentului și din contextul acțiunii, nu din adevărul ascuns al simulatorului.

## Atenție, nu „inteligență”

[[VAR:W]] nu este IQ, „Sistem 2”, moralitate sau capacitate generală de gândire critică. Este o pondere contextuală a acurateții în politica M0. Un indiciu de acuratețe nu „face persoana mai inteligentă”; în model, el schimbă criteriul care primește mai multă greutate în acel moment.

## Ce nu afirmă acest capitol

Nu afirmă că toate distribuirile de dezinformare sunt produse de neatenție și nici că indiciile de acuratețe rezolvă problema dezinformării. Efectele reale depind de design, populație, conținut și platformă. De asemenea, intențiile de distribuire măsurate în experimente nu sunt identice cu comportamentul observat pe platforme.

## În aplicație

Folosește [[VIEW:runs:accuracy:5]] pentru scenariul M0 și [[VIEW:planning]] pentru combinațiile demonstrative de intervenții. Capitolul 10 introduce un alt rezultat, EngageIntent, care trebuie păstrat separat de Share.