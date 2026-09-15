# Formularea mesajului, congruența atitudinală și contextul identitar

## Ideea centrală

Aceeași semnificație factuală poate fi exprimată prin forme lingvistice diferite. M1.E2 întreabă dacă formularea de confirmare, comparativ cu cea de infirmare, modifică propensiunea pentru interacțiune activă și dacă diferența depinde de relația dintre poziția anterioară a participantului și sensul mesajului.

Întrebarea este deliberat îngustă. Congruența cu atitudinea anterioară poate fi asociată cu identitatea, partizanatul sau raționamentul motivat în anumite contexte reale, dar nu este identică cu niciunul dintre aceste constructe. CEM păstrează relația experimentală locală înainte de a introduce mecanisme mai largi de identitate socială.

[[CONCEPT:m1-e2]] · [[VAR:Fpres]] · [[VAR:Gatt]] · [[VAR:Pengage]] · [[VAR:EngageIntent]] · [[MECH:presentation]] · [[MODULE:MOD.05]] · [[VAL:VAL.M1.003]] · [[REF:REF.ALVARADO.2026]] · [[CODE:m1e2.active_engagement_probability]] · [[VIEW:learning]]

## Invarianța semantică

M1.E2 construiește o SemanticProposition și două obiecte PresentedMessage care au aceeași semantic_signature. O condiție exprimă „TRUE că p”, cealaltă „FALSE că nu-p”. [[VAR:Fpres]] codifică forma de prezentare, nu adevărul și nu selecția editorială.

Invarianța este esențială. Dacă semnificația s-ar schimba între condiții, diferența observată nu ar mai putea fi atribuită curat formei de prezentare.

Manipularea trebuie citită, așadar, ca un contrast lingvistic controlat, nu ca un model general al încadrării jurnalistice. Capitolul 9 folosește noțiunea de încadrare într-un sens mai larg, în care se pot schimba selecția, accentul, exemplele, titlurile și organizarea narațiunii.

## Congruența este relațională și specifică sarcinii

[[VAR:Gatt]] este calculată ca prior_stance × message_stance și rămâne în intervalul [-1,1]. Nu este ideologie, identitate de partid, personalitate sau un scor global al tendinței de confirmare. Spune numai dacă, în această sarcină, poziția anterioară și sensul mesajului sunt aliniate sau opuse.

Designul permite testarea unei interacțiuni fără să transforme o relație experimentală locală într-o identitate psihologică stabilă. Aceeași persoană poate fi congruentă cu un mesaj, incongruentă cu altul și neutră față de un al treilea.

## Trei modele imbricate

NULL: logit(Pengage) = b0. Variația de formulare este neutralizată, iar confirmarea și infirmarea trebuie să convergă.

FRAME_ONLY: logit(Pengage) = b0 + beta_frame × Fpres. Confirmarea are un avantaj uniform.

FRAME_CONGRUENCE adaugă beta_congruence × Gatt și beta_interaction × Fpres × Gatt. Avantajul confirmării poate fi mai mare pentru mesajele congruente și se poate apropia de zero pentru mesajele contrare atitudinii inițiale.

[[CODE:m1e2.active_engagement_probability]] conține aceste forme exacte. Coeficienții sunt demonstrativi și nu sunt estimați din regresiile publicate.

Succesiunea modelelor imbricate este utilă științific deoarece întreabă dacă relația mai complexă explică un tipar pe care modelul mai simplu nu îl poate reproduce. Ea nu demonstrează că termenul de interacțiune dezvăluie un singur mecanism psihologic.

## Dovezile empirice

Aruguete și colaboratorii (2024) au găsit un avantaj agregat al confirmării față de infirmare pentru interacțiunea activă în patru țări latino-americane, folosind conținut corect factual și semantic echivalent. Distribuirea, luată separat, nu a fost un rezultat robust în toate condițiile.

[[REF:REF.ALVARADO.2026]] raportează o interacțiune între formularea de confirmare și congruența partizană într-un experiment de sondaj reprezentativ național în Argentina. CEM generalizează prudent numai tiparul relațional necesar discriminării între modele.

Prin urmare, [[VAL:VAL.M1.003]] cere ca diferența confirmare–infirmare să fie mai mare pentru mesajele congruente decât pentru cele contrare atitudinii inițiale.

## Congruența, identitatea și raționamentul motivat nu sunt sinonime

Cercetarea din psihologia politică documentează favoritism partizan în numeroase tipuri de judecăți, dar mecanismele sunt încă dezbătute. Explicațiile motivaționale pun accent pe scopuri precum protejarea unei identități importante sau a unei concluzii dorite. Explicațiile cognitive pun accent pe convingeri anterioare, medii informaționale, expunere selectivă, memorie și procese de inferență. Sintezele contemporane avertizează tot mai clar împotriva tratării tuturor diferențelor partizane ca efect al unui singur mecanism universal de raționament motivat.

În CEM, [[MODULE:MOD.05]] rezervă stratul mai larg al identității sociale și polarizării. Dacă identitatea va deveni executabilă, modelul trebuie să precizeze ce variabilă identitară este măsurată, când este activată, ce rezultat modifică și ce predicție o separă de simpla congruență cu o convingere anterioară.

M1.E2 **nu** face încă acest pas. [[VAR:Gatt]] este o relație între o poziție anterioară specifică sarcinii și poziția semantică a mesajului. A o numi „forță a identității” sau „partizanat” ar însemna reinterpretarea nejustificată a variabilei.

## De ce distincția contează pentru explicația cauzală

Să presupunem că formularea de confirmare produce mai multă interacțiune pentru conținut congruent. Sunt posibile mai multe explicații: formularea poate fi mai ușor de procesat; poate părea mai puțin confruntațională; poate corespunde mai bine așteptărilor; poate proteja o identitate; sau rezultatul poate depinde de norme și de contextul platformei. Interacțiunea observată nu identifică singură mediatorul.

CEM modelează de aceea mai întâi **tiparul** și lasă mediatorii neexecutați până când dovezile și designul experimental pot discrimina între ei. Astfel, afirmația computațională rămâne mai restrânsă decât povestea psihologică posibilă.

## Pengage și EngageIntent nu sunt Share

[[VAR:Pengage]] este probabilitatea latentă pentru rezultatul M1.E2. [[VAR:EngageIntent]] este observabilul obținut prin compararea probabilității cu o extragere aleatorie explicită. Niciuna dintre ele nu este [[VAR:Share]] din M0. Menținerea rezultatelor separate împiedică folosirea unui efect despre interacțiune agregată drept dovadă nejustificată pentru distribuirea comportamentală.

Distincția este importantă și deoarece „interacțiunea” poate combina comportamente cu sensuri diferite: aprecierea, comentarea, accesarea sau intenția de a interacționa nu reflectă neapărat aceeași convingere sau motivație.

## Ce nu afirmă acest capitol

Nu afirmă că formularea de confirmare este întotdeauna mai eficientă, că efectul se generalizează universal între culturi, că Gatt măsoară identitatea politică sau că identitatea distorsionează întotdeauna raționamentul. Nu impune dificultatea cognitivă, afectul negativ sau raționamentul motivat ca mediatori, deoarece studiile de ancorare nu identifică în mod unic aceste căi.

## În aplicație

Folosește [[VIEW:learning]] pentru comparația NULL → FRAME_ONLY → FRAME_CONGRUENCE și inspectorul [[MECH:presentation]] pentru a vedea exact ce rămâne invariant și ce se schimbă. Folosește [[VIEW:reference]] pentru a păstra [[VAR:Gatt]] distinctă de constructele conceptuale mai largi din [[MODULE:MOD.05]].
