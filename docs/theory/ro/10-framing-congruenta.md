# Încadrare de prezentare, congruență atitudinală și identitate

## Ideea centrală

Aceeași semnificație factuală poate fi exprimată prin forme lingvistice diferite. M1.E2 testează dacă prezentarea prin confirmare, față de prezentarea prin infirmare, modifică propensiunea către interacțiune și dacă această diferență depinde de relația dintre poziția anterioară a participantului și poziția semantică a mesajului.

[[CONCEPT:m1-e2]] · [[VAR:Fpres]] · [[VAR:Gatt]] · [[VAR:Pengage]] · [[VAR:EngageIntent]] · [[MECH:presentation]] · [[MODULE:MOD.05]] · [[VAL:VAL.M1.003]] · [[REF:REF.ALVARADO.2026]] · [[CODE:m1e2.active_engagement_probability]] · [[VIEW:learning]]

## Invarianța semantică

M1.E2 construiește o singură SemanticProposition și două obiecte PresentedMessage care au aceeași semantic_signature. O condiție exprimă „este adevărat că p”, iar cealaltă „este fals că non-p”. [[VAR:Fpres]] codifică forma de prezentare, nu adevărul afirmației și nici selecția editorială.

Această invarianță este esențială: dacă semnificația s-ar schimba între condiții, diferența observată nu ar mai putea fi atribuită formei de prezentare.

## Congruența este relațională și specifică sarcinii

[[VAR:Gatt]] este calculată ca prior_stance × message_stance și rămâne în intervalul [-1,1]. Nu reprezintă ideologia, identitatea de partid, personalitatea sau un scor global de „confirmation bias”. Arată doar dacă, în această sarcină, poziția anterioară și sensul mesajului sunt aliniate sau opuse.

Acest design permite testarea unei interacțiuni fără a transforma o relație experimentală locală într-o identitate psihologică stabilă.

## Identitatea și procesarea motivată sunt mai largi decât Gatt

Identitatea socială poate modifica modul în care este interpretată informația deoarece o afirmație poate semnala apartenență de grup, statut, loialitate sau amenințare, pe lângă conținutul ei factual. Cercetările asupra raționamentului motivat și procesării congruente cu identitatea sugerează că angajamentele anterioare pot influența uneori căutarea, interpretarea și acceptarea informației. Aceste efecte nu sunt universale și nu se reduc la o singură axă politică.

[[MODULE:MOD.05]] rezervă acest domeniu mai larg în CEM. M1.E2 nu implementează identitatea socială. El conține doar o relație locală de congruență atitudinală. Un viitor mecanism al identității ar avea nevoie de reprezentarea explicită a grupului, de context, de variabile observabile și de predicții diferite de cele produse de un model mai simplu bazat pe convingeri anterioare sau congruență.

Distincția este importantă deoarece „participantul este de acord cu mesajul” și „mesajul protejează o identitate socială importantă” nu sunt aceeași afirmație psihologică.

## Polarizarea nu este o singură variabilă

Termenul polarizare poate desemna rezultate diferite: depărtarea pozițiilor asupra unor politici, sortarea ideologică, ostilitatea afectivă dintre grupuri, separarea rețelelor informaționale sau extremizarea atitudinilor exprimate. Aceste dimensiuni se pot modifica în direcții diferite.

CEM nu trebuie, prin urmare, să deducă o creștere generică a „polarizării” dintr-o schimbare a interacțiunii sau dintr-un singur efect de congruență. Un viitor modul executabil dedicat polarizării trebuie să precizeze ce rezultat măsoară și la ce nivel: individual, interpersonal, de rețea sau populațional.

## Trei modele incluse unul în altul

NULL: logit(Pengage) = b0. Variația formei este neutralizată, iar condițiile de confirmare și infirmare trebuie să convergă.

FRAME_ONLY: logit(Pengage) = b0 + beta_frame × Fpres. Confirmarea are un avantaj uniform.

FRAME_CONGRUENCE adaugă beta_congruence × Gatt și beta_interaction × Fpres × Gatt. Avantajul confirmării poate fi mai mare pentru mesajele congruente și se poate apropia de zero pentru mesajele care contrazic atitudinea anterioară.

[[CODE:m1e2.active_engagement_probability]] conține aceste forme exacte. Coeficienții sunt demonstrativi și nu sunt ajustați pe regresiile publicate.

## Dovezile empirice

Aruguete și colaboratorii (2024) au găsit, în patru țări latino-americane, un avantaj agregat al confirmării față de infirmare pentru interacțiunea activă cu mesaje factuale și semantic echivalente. Distribuirea luată separat nu a fost un rezultat robust în toate condițiile.

[[REF:REF.ALVARADO.2026]] raportează o interacțiune între forma de confirmare și congruența partizană într-un experiment de tip survey, pe un eșantion reprezentativ național din Argentina. CEM generalizează prudent doar patternul relațional necesar pentru discriminarea modelelor.

[[VAL:VAL.M1.003]] cere ca diferența confirmare–infirmare să fie mai mare pentru mesajele congruente decât pentru cele care contrazic atitudinea anterioară.

## Pengage și EngageIntent nu sunt Share

[[VAR:Pengage]] este o probabilitate latentă pentru rezultatul M1.E2. [[VAR:EngageIntent]] este observabilul obținut prin compararea probabilității cu o extragere aleatorie explicită. Niciunul nu este [[VAR:Share]] din M0. Menținerea acestor rezultate separate împiedică folosirea nejustificată a unui efect asupra interacțiunii agregate ca dovadă pentru comportamentul de distribuire.

## Ce nu afirmă acest capitol

Nu afirmă că formularea prin confirmare este întotdeauna mai eficientă, că efectul se generalizează universal între culturi sau că Gatt măsoară identitatea politică. Nu tratează identitatea drept o cauză fixă a iraționalității și nu deduce polarizarea unei populații dintr-o singură interacțiune specifică sarcinii. De asemenea, nu impune drept mediatori dificultatea cognitivă sau afectul negativ, deoarece studiile de ancorare nu fac necesară niciuna dintre aceste căi.

## În aplicație

Folosește [[VIEW:learning]] pentru comparația NULL → FRAME_ONLY → FRAME_CONGRUENCE și inspectorul [[MECH:presentation]] pentru a vedea exact ce rămâne invariant și ce se schimbă. [[MODULE:MOD.05]] trebuie tratat ca extensie conceptuală până când identitatea și polarizarea vor primi definiții operaționale explicite și teste care să discrimineze între mecanisme.