# Surse, feedback și fiabilitate estimată

## Ideea centrală

Informația nu este evaluată independent de sursa ei. Oamenii pot folosi indicii despre expertiză, încredere, istoricul de performanță și rolul instituțional pentru a decide câtă greutate să acorde unei afirmații. M0 reprezintă o versiune minimală a acestei idei: agentul menține o estimare a fiabilității sursei și o actualizează după feedback.

[[VAR:T]] · [[VAR:B]] · [[MECH:source]] · [[MODULE:MOD.20]] · [[VAL:VAL.M0.003]] · [[CODE:m0.update_reliability]] · [[VIEW:runs:source:6]]

## Trei lucruri trebuie păstrate distincte

Primul este performanța reală a sursei în mediul experimental. Al doilea este ceea ce agentul crede despre sursă. Al treilea este adevărul afirmației curente. În CEM, [[VAR:T]] reprezintă numai fiabilitatea estimată de agent. T nu este adevăr și nu este un scor obiectiv și universal de reputație.

Această separare evită circularitatea: o sursă nu trebuie considerată „bună” doar pentru că agentul are încredere în ea, iar o afirmație nu devine adevărată doar pentru că provine de la o sursă evaluată pozitiv.

## Regula de învățare de referință

M0 folosește o regulă delta simplă:

T' = clamp01(T + alpha_t × (outcome - T)),

unde outcome este 1 pentru feedback corect și 0 pentru feedback incorect în sarcina sintetică. Implementarea poate fi inspectată în [[CODE:m0.update_reliability]].

Când un semnal de dovadă intră în calculul convingerii, M0 transformă T din intervalul [0,1] într-o pondere a sursei din [-1,1], folosind 2T - 1. Astfel, același semnal poate avea efecte diferite în funcție de fiabilitatea estimată.

Este o alegere de modelare deliberat simplă. Nu presupune că oamenii actualizează bayesian optim, că rata alpha_t are o valoare psihologică fixă sau că încrederea este unidimensională.

## Credibilitatea are mai multe dimensiuni

Cercetarea asupra credibilității surselor distinge frecvent între dimensiuni precum expertiza și caracterul demn de încredere. Alte indicii pot include transparența, independența, istoricul de performanță, consensul dintre experți relevanți și existența unor stimulente care pot distorsiona raportarea. Aceste dimensiuni nu se reduc natural la o singură scală universală.

CEM le comprimă momentan în T pentru mecanismul executabil de referință. Compresia este utilă pentru un test minimal, dar reprezintă o limită a modelului, nu o afirmație despre natura reală a încrederii.

Evaluarea sursei depinde și de domeniu. O sursă poate fi foarte fiabilă într-un domeniu și slabă în altul. Modelele viitoare ar trebui, prin urmare, să evite tratarea reputației drept proprietate independentă de context a unei persoane, instituții sau platforme.

## Instituții, autoritate și cunoaștere distribuită

În societățile moderne, oamenii se bazează frecvent pe informații pe care nu le pot verifica personal. Revistele științifice, instituțiile de sănătate publică, institutele de statistică, instanțele, redacțiile, universitățile și organizațiile profesionale pot funcționa ca instituții epistemice: organizează expertiză, proceduri, evidențe și mecanisme de responsabilizare astfel încât cunoașterea să poată fi produsă și verificată la o scară care depășește capacitatea unui singur individ.

[[MODULE:MOD.20]] rezervă acest nivel instituțional în CEM. Autoritatea instituțională nu trebuie reprezentată ca un semnal magic de adevăr. Valoarea ei epistemică poate depinde de proceduri precum transparența, reproductibilitatea, gestionarea conflictelor de interese, mecanismele de corecție, independența și calitatea expertizei de specialitate.

Este la fel de important să evităm eroarea opusă: faptul că instituțiile pot greși nu înseamnă că toate sursele devin epistemic echivalente. Un model util trebuie să poată reprezenta simultan eroarea instituțională și diferențele reale de fiabilitate.

CEM separă, prin urmare, cel puțin trei niveluri care ar putea fi modelate independent în viitor: încrederea agentului într-o instituție, caracteristicile observabile ale instituției sau ale procedurilor sale și performanța empirică a afirmațiilor produse prin acele proceduri.

## Feedbackul poate crea bucle

Dacă evaluarea sursei influențează interpretarea dovezii, iar rezultatul interpretat influențează ulterior evaluarea sursei, poate apărea o buclă de feedback. Cercetarea sugerează că astfel de dinamici pot depinde de credibilitatea inițială. M0 nu modelează toate aceste bucle sociale, dar mecanismul de învățare a fiabilității sursei oferă o bază pentru versiuni mai bogate.

În cazul instituțiilor apar bucle suplimentare. Corecțiile, retractările, auditurile și explicațiile publice pot reduce încrederea pe termen scurt și totuși pot îmbunătăți fiabilitatea pe termen lung. În sens invers, prestigiul poate menține încrederea chiar atunci când feedbackul direct este rar. Astfel de posibilități nu trebuie ascunse în T fără ipoteze explicite.

## Patternul M0

[[VAL:VAL.M0.003]] verifică dacă feedbackul despre sursă poate modifica T și dacă, ulterior, dovezi comparabile primesc ponderi diferite. Deschide [[VIEW:runs:source:6]] pentru scenariul de referință.

## Ce nu afirmă acest capitol

Nu afirmă că încrederea este fixă, unidimensională sau independentă de identitate și context. Nu afirmă că sursele verificate sau instituțiile sunt infailibile. Nu tratează T ca adevăr, nu transformă reputația socială într-o proprietate intrinsecă și nu deduce fiabilitatea doar din statut. De asemenea, nu presupune că neîncrederea este irațională prin definiție; întrebarea relevantă este dacă nivelul de încredere este calibrat la dovezile privind performanța și procedurile sursei.

## Statut epistemic

Mecanismul M0 pentru surse este EXECUTABLE/CANDIDATE. Literatura oferă BACKGROUND_THEORY și suport la nivel de fenomen pentru efectele credibilității; regula delta și transformarea 2T - 1 rămân REFERENCE_CANDIDATE până la calibrare și comparație cu alternative. [[MODULE:MOD.20]] rămâne CONCEPTUAL până când caracteristicile instituționale, observabilele și predicțiile diferențiale vor fi definite explicit.