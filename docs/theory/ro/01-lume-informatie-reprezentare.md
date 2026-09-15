# Lume, informație și reprezentare internă

## Ideea centrală

CEM pornește de la o distincție simplă, dar decisivă: o stare a lumii nu este identică cu informația disponibilă despre ea, informația disponibilă nu este identică cu informația observată de un agent, iar informația observată nu este identică cu reprezentarea internă construită de acel agent.

Lanțul conceptual este:

lume → informație disponibilă → selecție și prezentare → informație observată → reprezentare internă → judecată → acțiune.

[[CONCEPT:world-model]] · [[MODULE:MOD.14]] · [[MECH:editorial]] · [[MECH:presentation]] · [[VIEW:learning]]

## De ce nu putem comprima etapele

Dacă o analiză sare direct de la „ce există în lume” la „ce crede persoana”, orice diferență intermediară riscă să fie atribuită greșit psihologiei individului. În practică, mediul informațional filtrează, ordonează și formatează informația înainte ca agentul să o proceseze. Apoi memoria, așteptările, cunoștințele și contextul contribuie la o reprezentare internă care poate fi incompletă.

Această separare permite întrebări cauzale diferite. M1.E1 întreabă ce se întâmplă când același set de informații factuale este selectat diferit. M1.E2 întreabă ce se întâmplă când aceeași propoziție semantică este formulată prin confirmare sau infirmare. Un viitor mecanism de ordonare algoritmică ar trebui să întrebe separat ce conținut ajunge în expunere. Niciuna dintre aceste intervenții asupra fluxului nu implică automat o schimbare de convingere.

## Relația cu teoriile despre procesarea predictivă

Procesarea predictivă (predictive processing) oferă un fundal teoretic util: percepția și interpretarea pot fi privite ca procese constructive în care așteptările și semnalele senzoriale se confruntă. Literatura neuroștiințifică descrie modele generative și semnale de eroare de predicție, în special în procesarea senzorială. Dar cadrul este larg, are mai multe variante și există dezbateri privind dovezile care îl disting de explicații alternative.

CEM nu implementează codare predictivă neuronală (predictive coding) și nu pretinde că MOD.14 este o instanțiere a unei teorii cerebrale complete. Folosește doar o distincție mai modestă și mai ușor de testat: informația externă și reprezentarea internă trebuie modelate separat.

Acesta este motivul pentru care [[CONCEPT:world-model]] este simultan conceptual și legat de componente executabile, fără a fi prezentat ca o „teorie unificată a creierului”.

## Adevărul de referință al simulării și ceea ce știe agentul

În M0, adevărul sintetic aparține mediului de simulare. El este folosit pentru a construi și verifica scenarii, dar nu este transmis direct actualizării convingerii. Aceasta este o frontieră epistemică importantă: un observator extern al simulării poate ști că o afirmație este adevărată sau falsă, în timp ce agentul trebuie să lucreze cu expuneri, dovezi, corecții și estimări de fiabilitate.

Dacă am trece adevărul de referință al simulării direct în actualizarea convingerii, am confunda evaluarea modelului cu informația disponibilă agentului și am elimina tocmai problema epistemică pe care modelul încearcă să o studieze.

## Selecția și prezentarea sunt mecanisme diferite

[[MECH:editorial]] schimbă subsetul factual observat dintr-un set de informații fix. [[MECH:presentation]] păstrează semnificația propoziției și compară forma de confirmare cu forma de infirmare. În realitate, selecția, tonul, titlul, ordinea și ordonarea algoritmică pot apărea împreună. CEM le separă intenționat pentru a putea testa ce predicție aparține fiecărei etape.

Aceasta este o regulă generală a proiectului: dacă două mecanisme pot fi confundate, modelul ar trebui să încerce să le separe prin condiții controlate și modele nule imbricate, nu să le ascundă într-un coeficient global.

## Ce nu afirmă acest capitol

Nu afirmă că oamenii „halucinează realitatea”, că percepția este arbitrară sau că orice interpretare este la fel de validă. Nu afirmă că procesarea predictivă este o teorie definitiv demonstrată a întregii cogniții. Nu afirmă că M1.E1 sau M1.E2 descriu toate filtrele informaționale existente.

## În aplicație

Folosește [[VIEW:learning]] pentru a compara M1.E1 și M1.E2. În capitolele 9 și 10, aceleași distincții sunt legate de variabilele executabile și de testele lor de discriminare.