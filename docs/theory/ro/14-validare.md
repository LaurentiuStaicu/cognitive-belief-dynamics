# Cum validăm un model epistemic

## Ideea centrală

Un model poate fi corect implementat și totuși să fie științific slab. Validarea CEM separă verificarea software, reproducerea tiparelor, legătura cu dovezile empirice, discriminarea între modele, calibrarea și analiza limitelor.

[[CONCEPT:odd]] · [[CONCEPT:model-validation]] · [[VAL:VAL.M0.001]] · [[VAL:VAL.M1.003]] · [[CODE:registry.validate_model_dir]] · [[VIEW:process]] · [[VIEW:reference]]

## Verificare software versus test științific

Testele software răspund la întrebări precum: funcția produce valori în intervalul declarat? seed-ul reproduce aceeași rulare? registrul are referințe valide? build-ul web compilează? Acestea sunt necesare, dar nu demonstrează că mecanismul psihologic este corect.

Testele științifice întreabă dacă modelul reproduce un tipar extern relevant sub constrângeri care împiedică soluții triviale. De exemplu, [[VAL:VAL.M0.001]] testează tiparul de repetare; [[VAL:VAL.M1.003]] testează heterogenitatea framing × congruență.

## Empirical target versus parametru

Un rezultat publicat poate fi stocat ca țintă empirică fără să devină coeficient de simulator. Această separare este esențială. Dacă un studiu raportează o diferență de 18 puncte procentuale, CEM nu are voie să introducă automat 0.18 într-un coeficient intern cu altă scară și altă semnificație.

Calibrarea ar necesita o funcție de observație care leagă stările modelului de măsura experimentală, un set de date, o procedură de estimare și verificare în afara eșantionului. Alpha 0.4.1a1 nu este calibrat în acest sens.

## Nested null și discriminarea între modele

Un mecanism nou este mai credibil dacă produce o predicție pe care modelul mai simplu nu o poate produce fără schimbări ascunse. De aceea M1.E1 are un null în care selecția editorială este oprită și toate condițiile primesc același set de informații. M1.E2 compară NULL, frame-only și frame × congruence.

Nested null nu dovedește mecanismul; arată că efectul din simulare depinde de componenta declarată. Model discrimination cere apoi date care pot favoriza o variantă față de alta.

## Identificabilitate și sensibilitate

CEM are diagnostice locale de sensibilitate și identificabilitate practică. Acestea pot arăta că parametri diferiți produc răspunsuri similare în jurul unei configurații. Ele nu demonstrează identificabilitate structurală, nu oferă distribuții posterioare ale parametrilor și nu înlocuiesc calibrarea.

Un model poate reproduce un tipar din motive greșite. De aceea trebuie inspectate traiectoriile intermediare, nu doar rezultatul final.

## ODD, TRACE și proveniență

[[CONCEPT:odd]] oferă o descriere standardizată a scopului, entităților, proceselor, concepte de proiectare, inițializării și submodelelor. Protocolul ODD este folosit tocmai pentru claritate și replicare. TRACE documentează deciziile de modelare și alternativele respinse.

[[VIEW:process]] arată ODD vizual. [[VIEW:reference]] expune variabilele, dovezile, limitările și instantaneul dovezilor. Rulările publicate și hash-urile de proveniență permit verificarea faptului că aplicația afișează rezultate produse de modelul declarat.

## Fitness for purpose

Validitatea nu este absolută; depinde de scop. M0 poate fi adecvat pentru demonstrarea mecanismelor și teste de regresie ale tiparelor, dar nu pentru estimarea prevalenței unei credințe într-o țară. M1 poate discrimina mecanisme în sarcini sintetice fără a fi apt pentru recomandări de platform policy.

Fiecare versiune trebuie să declare explicit pentru ce este și pentru ce nu este potrivit.

## Ce ar crește încrederea

Încrederea ar crește prin preregistered external validation, seturi de date independente, măsurarea directă a constructelor, calibrare cu incertitudine, predicție în afara eșantionului și comparații cu modele rivale mai simple. Rezultatele negative trebuie să poată elimina mecanisme, nu doar să producă noi parametri.

## Ce nu afirmă acest capitol

„Toate testele sunt verzi” nu înseamnă „teoria este adevărată”. Un CI verde certifică integritatea tehnică și reproducibilitatea definită de suită de teste; statutul științific depinde de dovezi, teste discriminative și domeniul de aplicare.