# Framing de prezentare și congruență atitudinală

## Ideea centrală

Aceeași semnificație factuală poate fi prezentată prin forme lingvistice diferite. M1.E2 întreabă dacă o formulare de confirmare față de una de infirmare poate modifica propensiunea de engagement și dacă această diferență depinde de relația dintre poziția anterioară a participantului și poziția semantică a mesajului.

[[CONCEPT:m1-e2]] · [[VAR:Fpres]] · [[VAR:Gatt]] · [[VAR:Pengage]] · [[VAR:EngageIntent]] · [[MECH:presentation]] · [[VAL:VAL.M1.003]] · [[REF:REF.ALVARADO.2026]] · [[CODE:m1e2.active_engagement_probability]] · [[VIEW:learning]]

## Invarianța semantică

M1.E2 construiește o SemanticProposition și două PresentedMessage care împart aceeași semantic_signature. O condiție exprimă „TRUE că p”, cealaltă „FALSE că nu-p”. [[VAR:Fpres]] codifică forma de prezentare, nu adevărul și nu selecția editorială.

Această invarianță este esențială: dacă semnificația s-ar schimba între condiții, nu am mai putea atribui diferența frame-ului.

## Congruența este relațională și task-specific

[[VAR:Gatt]] este calculată ca prior_stance × message_stance și rămâne în [-1,1]. Nu este ideologie, partid, personalitate ori „confirmation bias” global. Ea spune doar dacă, în această sarcină, poziția anterioară și sensul mesajului sunt aliniate sau opuse.

Acest design permite testarea unei interacțiuni fără a transforma o relație experimentală locală într-o identitate psihologică stabilă.

## Trei modele nested

NULL: logit(Pengage) = b0. Frame-ul este normalizat și confirmarea/infirmarea trebuie să convergă.

FRAME_ONLY: logit(Pengage) = b0 + beta_frame × Fpres. Confirmarea are un avantaj uniform.

FRAME_CONGRUENCE: se adaugă beta_congruence × Gatt și beta_interaction × Fpres × Gatt. Avantajul confirmării poate fi mai mare în condiția congruentă și se poate apropia de zero în condiția counter-attitudinal.

[[CODE:m1e2.active_engagement_probability]] conține exact aceste forme. Coeficienții sunt demonstrativi, nu fit la regresiile publicate.

## Dovezile empirice

Aruguete și colaboratorii (2024) au găsit un avantaj agregat de engagement pentru confirmation versus refutation în patru țări latino-americane, cu conținut factually accurate și semantic echivalent. Share luat separat nu a fost un outcome universal robust.

[[REF:REF.ALVARADO.2026]] arată o interacțiune între confirmation frame și partisan congruence într-un experiment reprezentativ național în Argentina. CEM generalizează prudent numai patternul relațional necesar pentru discriminarea modelelor.

[[VAL:VAL.M1.003]] cere ca diferența confirmation-refutation să fie mai mare pentru mesajele congruente decât pentru cele counter-attitudinal.

## Pengage și EngageIntent nu sunt Share

[[VAR:Pengage]] este o probabilitate latentă pentru outcome-ul M1.E2. [[VAR:EngageIntent]] este observabilul obținut prin compararea probabilității cu un draw explicit. Niciunul nu este [[VAR:Share]] din M0. Menținerea outcome-urilor separate previne folosirea nejustificată a unui rezultat despre engagement agregat ca dovadă pentru sharing comportamental.

## Ce nu afirmă acest capitol

Nu afirmă că formularea de confirmare este întotdeauna mai eficientă, că efectul este universal între culturi sau că Gatt măsoară identitatea politică. Nu cere un mediator de dificultate cognitivă sau afect negativ, deoarece studiile ancoră nu justifică obligativitatea acestor căi.

## În aplicație

Folosește [[VIEW:learning]] pentru comparația NULL → FRAME_ONLY → FRAME_CONGRUENCE și inspectorul [[MECH:presentation]] pentru a vedea exact ce este invariant și ce se schimbă.