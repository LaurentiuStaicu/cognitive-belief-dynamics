# Cum validăm un model epistemic

## Ideea centrală

Un model poate fi corect implementat și totuși să fie științific slab. Validarea CEM separă verificarea software, reproducerea patternurilor, legătura cu dovezile empirice, discriminarea între modele, calibrarea și analiza limitelor.

[[CONCEPT:odd]] · [[CONCEPT:model-validation]] · [[VAL:VAL.M0.001]] · [[VAL:VAL.M1.003]] · [[CODE:registry.validate_model_dir]] · [[VIEW:process]] · [[VIEW:reference]]

## Verificare software versus test științific

Testele software răspund la întrebări precum: funcția produce valori în intervalul declarat? seed-ul reproduce aceeași rulare? registrul are referințe valide? build-ul web compilează? Acestea sunt necesare, dar nu demonstrează că mecanismul psihologic este corect.

Testele științifice întreabă dacă modelul reproduce un pattern extern relevant sub constrângeri care împiedică soluții triviale. De exemplu, [[VAL:VAL.M0.001]] testează patternul de repetare; [[VAL:VAL.M1.003]] testează heterogenitatea framing × congruență.

## Empirical target versus parametru

Un rezultat publicat poate fi stocat ca empirical target fără să devină coeficient de simulator. Această separare este esențială. Dacă un studiu raportează o diferență de 18 puncte procentuale, CEM nu are voie să introducă automat 0.18 într-un coeficient intern cu altă scară și altă semnificație.

Calibrarea ar necesita o funcție de observație care leagă stările modelului de măsura experimentală, un set de date, o procedură de estimare și verificare out-of-sample. Alpha 0.4.1a1 nu este calibrat în acest sens.

## Nested null și model discrimination

Un mecanism nou este mai credibil dacă produce o predicție pe care modelul mai simplu nu o poate produce fără schimbări ascunse. De aceea M1.E1 are un null în care selecția editorială este oprită și toate condițiile primesc același pool. M1.E2 compară NULL, frame-only și frame × congruence.

Nested null nu dovedește mecanismul; arată că efectul din simulare depinde de componenta declarată. Model discrimination cere apoi date care pot favoriza o variantă față de alta.

## Identificabilitate și sensibilitate

CEM are diagnostice locale de sensibilitate și practical identifiability. Acestea pot arăta că parametri diferiți produc răspunsuri similare în jurul unei configurații. Ele nu demonstrează structural identifiability, nu oferă distribuții posterioare ale parametrilor și nu înlocuiesc calibrarea.

Un model poate reproduce un pattern din motive greșite. De aceea trebuie inspectate traiectoriile intermediare, nu doar outcome-ul final.

## ODD, TRACE și proveniență

[[CONCEPT:odd]] oferă o descriere standardizată a scopului, entităților, proceselor, design concepts, inițializării și submodelelor. Protocolul ODD este folosit tocmai pentru claritate și replicare. TRACE documentează deciziile de modelare și alternativele respinse.

[[VIEW:process]] arată ODD vizual. [[VIEW:reference]] expune variabilele, dovezile, limitările și snapshotul de evidence. Rulările publicate și hash-urile de proveniență permit verificarea faptului că aplicația afișează outputuri produse de modelul declarat.

## Fitness for purpose

Validitatea nu este absolută; depinde de scop. M0 poate fi adecvat pentru demonstrarea mecanismelor și teste de regresie ale patternurilor, dar nu pentru estimarea prevalenței unei credințe într-o țară. M1 poate discrimina mecanisme în sarcini sintetice fără a fi apt pentru recomandări de platform policy.

Fiecare release trebuie să declare explicit pentru ce este și pentru ce nu este potrivit.

## Ce ar crește încrederea

Încrederea ar crește prin preregistered external validation, datasets independente, măsurarea directă a constructelor, calibration cu uncertainty, prediction out-of-sample și comparații cu modele rivale mai simple. Rezultatele negative trebuie să poată elimina mecanisme, nu doar să producă noi parametri.

## Ce nu afirmă acest capitol

„Toate testele sunt verzi” nu înseamnă „teoria este adevărată”. Un CI verde certifică integritatea tehnică și reproducibilitatea definită de suite; statutul științific depinde de dovezi, teste discriminative și domeniul de aplicare.