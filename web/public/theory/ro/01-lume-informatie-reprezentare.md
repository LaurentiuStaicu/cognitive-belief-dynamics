# Lume, informație și reprezentare internă

## Ideea centrală

CEM pornește de la o distincție simplă, dar decisivă: o stare a lumii nu este identică cu informația disponibilă despre ea, informația disponibilă nu este identică cu ceea ce observă un agent, iar informația observată nu este identică cu reprezentarea internă construită de acel agent.

Lanțul conceptual este:

lume → informație disponibilă → selecție și prezentare → informație observată → reprezentare internă → judecată → acțiune.

[[CONCEPT:world-model]] · [[MODULE:MOD.14]] · [[MECH:editorial]] · [[MECH:presentation]] · [[VIEW:learning]]

## De ce etapele nu trebuie comprimate

Dacă o analiză sare direct de la „ce există în lume” la „ce crede persoana”, diferențele apărute între aceste două niveluri riscă să fie atribuite greșit psihologiei individului. În realitate, mediul informațional filtrează, ordonează și formatează informația înainte ca agentul să o proceseze. Apoi memoria, așteptările, cunoștințele și contextul contribuie la construirea unei reprezentări interne care poate fi incompletă.

Separarea etapelor permite formularea unor întrebări cauzale diferite. M1.E1 întreabă ce se întâmplă când același set factual este selectat diferit. M1.E2 întreabă ce se întâmplă când aceeași propoziție semantică este formulată prin confirmare sau infirmare. Un viitor mecanism de ordonare algoritmică ar trebui să întrebe separat ce conținut ajunge efectiv la expunere. Niciuna dintre aceste intervenții asupra fluxului informațional nu implică automat o schimbare a convingerii.

## Relația cu teoriile despre procesarea predictivă

Predictive processing oferă un fundal teoretic util: percepția și interpretarea pot fi privite ca procese constructive în care așteptările interacționează cu semnalele primite. Literatura neuroștiințifică descrie modele generative și semnale de eroare de predicție, în special pentru procesarea senzorială. Cadrul este însă larg, are mai multe variante și există dezbateri privind măsura în care dovezile disponibile îl disting de explicații alternative.

CEM nu implementează un model neuronal complet de predictive coding și nu susține că MOD.14 reprezintă o teorie generală a creierului. Folosește o distincție mai modestă și mai ușor de testat: informația externă și reprezentarea internă trebuie modelate separat.

Din acest motiv, [[CONCEPT:world-model]] este o punte conceptuală legată de componente executabile, fără să fie prezentată drept o „teorie unificată a creierului”.

## Adevărul din simulare și ceea ce știe agentul

În M0, adevărul sintetic aparține mediului de simulare. Este folosit pentru construirea și evaluarea scenariilor, dar nu este transmis direct funcției care actualizează convingerea. Aceasta creează o frontieră epistemică importantă: evaluatorul extern al simulării poate ști dacă o afirmație sintetică este adevărată sau falsă, în timp ce agentul trebuie să lucreze cu expuneri, dovezi, corecții și estimări ale fiabilității surselor.

Dacă adevărul din simulare ar intra direct în actualizarea convingerii, am confunda evaluarea modelului cu informația disponibilă agentului și am elimina tocmai problema epistemică pe care CEM încearcă să o studieze.

## Selecția și prezentarea sunt mecanisme diferite

[[MECH:editorial]] modifică subsetul factual observat dintr-un set disponibil fix. [[MECH:presentation]] păstrează semnificația propoziției și compară forma de confirmare cu forma de infirmare. În lumea reală, selecția, tonul, titlul, ordinea și recomandarea algoritmică pot apărea împreună. CEM le separă intenționat pentru a putea testa ce predicție aparține fiecărei etape.

Aceasta este o regulă generală a proiectului: dacă două mecanisme se pot confunda, modelul trebuie să încerce să le separe prin condiții controlate și prin modele nule incluse unul în altul, nu să le ascundă într-un coeficient global.

## Ce nu afirmă acest capitol

Nu afirmă că oamenii „halucinează realitatea”, că percepția este arbitrară sau că orice interpretare este la fel de validă. Nu afirmă că predictive processing este o teorie definitiv demonstrată a întregii cogniții. Nu afirmă că M1.E1 sau M1.E2 descriu toate filtrele informaționale existente.

## În aplicație

Folosește [[VIEW:learning]] pentru a compara M1.E1 și M1.E2. Capitolele 9 și 10 leagă aceste distincții de variabile executabile și de testele folosite pentru discriminarea mecanismelor.