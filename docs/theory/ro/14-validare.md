# Cum validăm un model epistemic

## Ideea centrală

Un model poate fi implementat corect și totuși să fie științific slab. Validarea CEM separă verificarea software, reproducerea unor tipare empirice, legătura cu dovezile externe, discriminarea între modele, calibrarea și analiza limitelor.

[[CONCEPT:odd]] · [[CONCEPT:model-validation]] · [[VAL:VAL.M0.001]] · [[VAL:VAL.M1.003]] · [[CODE:registry.validate_model_dir]] · [[VIEW:process]] · [[VIEW:reference]]

## Verificare software versus test științific

Testele software răspund la întrebări precum: funcția produce valori în intervalul declarat? aceeași sămânță aleatoare reproduce aceeași rulare? registrul are referințe valide? aplicația web se compilează? Aceste verificări sunt necesare, dar nu demonstrează că mecanismul psihologic este corect.

Testele științifice întreabă dacă modelul reproduce un tipar extern relevant în condiții care împiedică soluțiile triviale. De exemplu, [[VAL:VAL.M0.001]] testează tiparul asociat repetării, iar [[VAL:VAL.M1.003]] testează heterogenitatea interacțiunii dintre formă și congruență.

## Țintă empirică versus parametru

Un rezultat publicat poate fi stocat drept țintă empirică fără să devină automat coeficient al simulatorului. Separarea este esențială. Dacă un studiu raportează o diferență de 18 puncte procentuale, CEM nu poate introduce pur și simplu valoarea 0,18 într-un coeficient intern care are altă scară și altă semnificație.

Calibrarea ar necesita o funcție de observație care să lege stările modelului de măsura experimentală, un set de date, o procedură de estimare și o verificare pe date care nu au fost folosite la ajustare. Alpha 0.4.1a1 nu este calibrat în acest sens.

## Modele nule incluse și discriminarea între modele

Un mecanism nou devine mai credibil atunci când produce o predicție pe care modelul mai simplu nu o poate reproduce fără modificări ascunse. De aceea M1.E1 are un model nul în care selecția editorială este oprită și toate condițiile primesc același set factual. M1.E2 compară modelele NULL, FRAME_ONLY și FRAME_CONGRUENCE.

Un astfel de model nul inclus nu dovedește mecanismul; arată doar că efectul din simulare depinde de componenta declarată. Discriminarea între modele cere apoi date care pot favoriza o variantă în raport cu alta.

## Identificabilitate și sensibilitate

CEM are diagnostice locale de sensibilitate și de identificabilitate practică. Acestea pot arăta dacă parametri diferiți produc răspunsuri similare în jurul unei configurații de referință. Nu demonstrează identificabilitatea structurală, nu oferă distribuții posterioare ale parametrilor și nu înlocuiesc calibrarea.

Un model poate reproduce un tipar din motive greșite. De aceea trebuie inspectate și traiectoriile intermediare, nu doar rezultatul final.

## ODD, TRACE și proveniență

[[CONCEPT:odd]] oferă o descriere standardizată a scopului, entităților, proceselor, conceptelor de proiectare, inițializării și submodelelor. Protocolul ODD este folosit pentru claritate și replicare. TRACE documentează deciziile de modelare și alternativele respinse.

[[VIEW:process]] arată ODD vizual. [[VIEW:reference]] expune variabilele, dovezile, limitările și starea documentată a surselor. Rulările publicate și hash-urile de proveniență permit verificarea faptului că aplicația afișează rezultate produse de modelul declarat.

## Adecvarea la scop

Validitatea nu este absolută; depinde de scopul pentru care este folosit modelul. M0 poate fi adecvat pentru demonstrarea mecanismelor și testarea de regresie a unor tipare, dar nu pentru estimarea prevalenței unei convingeri într-o țară. M1 poate discrimina mecanisme în sarcini sintetice fără să fie potrivit pentru recomandări de politică privind platformele.

Fiecare versiune trebuie să declare explicit pentru ce este și pentru ce nu este adecvată.

## Ce ar crește încrederea

Încrederea ar crește prin validare externă preregistrată, seturi de date independente, măsurarea directă a constructelor, calibrare care include incertitudinea, predicție pe date noi și comparații cu modele rivale mai simple. Rezultatele negative trebuie să poată elimina mecanisme, nu doar să conducă la introducerea unor parametri noi.

## Ce nu afirmă acest capitol

„Toate testele sunt verzi” nu înseamnă „teoria este adevărată”. Un CI verde certifică integritatea tehnică și reproductibilitatea definită de suita de teste; statutul științific depinde de dovezi, de teste discriminative și de domeniul de aplicare.