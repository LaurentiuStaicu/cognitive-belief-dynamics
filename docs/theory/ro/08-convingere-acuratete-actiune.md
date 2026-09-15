# Convingere, atenție la acuratețe și acțiune

## Ideea centrală

A considera o afirmație adevărată și a decide să o distribui sunt două rezultate diferite. Distribuirea poate depinde de acuratețe, dar și de recompense sociale, relevanță, identitate, divertisment sau alte motive. M0 separă explicit convingerea [[VAR:B]], ponderea contextuală a acurateții [[VAR:W]], probabilitatea latentă de distribuire și acțiunea eșantionată [[VAR:Share]].

[[VAR:B]] · [[VAR:W]] · [[VAR:Share]] · [[MECH:accuracy]] · [[VAL:VAL.M0.N01]] · [[REF:REF.PENNYCOOK.2021]] · [[CODE:m0.share_probability]] · [[VIEW:runs:accuracy:5]]

## De la convingere la probabilitatea de acțiune

M0 calculează mai întâi B fără acces direct la adevărul de referință al simulării. Apoi, un indiciu care mută atenția către acuratețe poate modifica ponderea W printr-o transformare logistică a valorii sale de referință.

Probabilitatea de distribuire este:

P(Share) = logistic(sharing_bias + W × (2B - 1) + beta_reward × (1 - W) × reward_context).

Identificatorii din ecuație sunt păstrați în forma folosită de cod. Implementarea poate fi inspectată în [[CODE:m0.share_probability]].

Ecuația arată de ce B și Share nu sunt sinonime. Când W este mare, acuratețea și convingerea au o pondere mai mare în utilitatea acțiunii. Când W este mai mic, reward_context poate conta mai mult. În final, Share este rezultatul unei extrageri stocastice din probabilitatea calculată; două rulări pot avea aceeași probabilitate latentă și acțiuni observate diferite dacă folosesc semințe aleatoare diferite.

## Ce spune literatura despre orientarea atenției către acuratețe

Pennycook și colaboratorii au arătat experimental că orientarea momentană a atenției către acuratețe poate îmbunătăți discernământul privind ceea ce oamenii declară că ar distribui. O meta-analiză ulterioară a 20 de experimente, cu un total de 26.863 de participanți, a găsit o îmbunătățire a discernământului la distribuire, produsă în principal prin reducerea intenției de a distribui titluri false.

Literatura susține ideea că acuratețea poate primi o pondere prea mică în momentul deciziei de distribuire și că un indiciu contextual poate schimba alegerea. Ea nu identifică însă W drept o stare latentă literală și nu estimează ecuația M0.

## De ce separarea este importantă epistemic

Dacă observăm că o persoană distribuie un conținut, nu putem deduce cu certitudine că îl consideră adevărat. Distribuirea este o acțiune socială care poate avea mai multe utilități. Invers, o persoană poate considera o afirmație adevărată și totuși să nu o distribuie. Această disociere limitează inferențele care pot fi făcute de la comportamentul vizibil pe platformă la convingerile private.

[[VAL:VAL.M0.N01]] păstrează și o frontieră importantă de izolare a adevărului de referință: decizia trebuie să rezulte din stările agentului și din contextul acțiunii, nu din adevărul ascuns al simulatorului.

## Atenție, nu „inteligență”

[[VAR:W]] nu este IQ, „System 2”, moralitate sau capacitate generală de gândire critică. Este o pondere contextuală acordată acurateții în politica de acțiune M0. Indiciul de acuratețe nu „face persoana mai inteligentă”; în model, schimbă doar criteriul care primește mai multă greutate în acel moment.

Această limită este esențială. Un efect asupra W nu poate fi folosit drept dovadă că o persoană a devenit global mai rațională, mai atentă sau mai competentă.

## De la intenție la comportament real

O parte importantă a literaturii folosește intenții declarate de distribuire sau alegeri în sarcini experimentale. Aceste rezultate sunt informative, dar nu sunt identice cu distribuirea observată pe o platformă reală, unde intervin interfața, publicul perceput, normele, reputația, costurile sociale și consecințele reale.

De aceea, CEM trebuie să păstreze explicit nivelul observabilului. Un mecanism valid pentru intenția de distribuire nu devine automat un model valid al comportamentului de distribuire în toate platformele.

## Ce nu afirmă acest capitol

Nu afirmă că toate distribuirile de dezinformare sunt produse de neatenție și nici că orientarea către acuratețe rezolvă problema dezinformării. Efectele reale depind de designul intervenției, populație, conținut și platformă. Nu afirmă nici că distribuirea unei informații dovedește acceptarea ei ca adevărată.

## În aplicație

Folosește [[VIEW:runs:accuracy:5]] pentru scenariul M0 și [[VIEW:planning]] pentru combinațiile demonstrative de intervenții. Capitolul 10 introduce un rezultat diferit, EngageIntent, care trebuie păstrat separat de Share.
