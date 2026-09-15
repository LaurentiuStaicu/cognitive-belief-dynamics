# Cum validăm un model epistemic

## Ideea centrală

Un model poate fi implementat corect și totuși să fie slab din punct de vedere științific. De aceea, CEM separă mai multe întrebări care sunt adesea amestecate: software-ul execută ceea ce spune specificația? modelul reproduce tipare empirice relevante? un mecanism nou explică ceva ce modelul mai simplu nu poate explica? parametrii pot fi identificați din date? rezultatele se generalizează dincolo de cazurile folosite la construire? modelul este adecvat scopului pentru care cineva vrea să îl folosească?

[[CONCEPT:odd]] · [[CONCEPT:model-validation]] · [[VAL:VAL.M0.001]] · [[VAL:VAL.M1.003]] · [[CODE:registry.validate_model_dir]] · [[VIEW:process]] · [[VIEW:reference]]

## Verificarea implementării nu este același lucru cu validarea științifică

Verificarea software răspunde la întrebări precum: funcția rămâne în domeniul declarat? aceeași sămânță aleatoare reproduce aceeași rulare? referințele din Registru se rezolvă corect? aplicația web se compilează? rulările de referință pot fi reproduse identic acolo unde acest lucru este cerut?

Aceste teste sunt indispensabile, deoarece un argument științific nu poate fi susținut de o implementare defectuoasă. Trecerea lor arată însă doar că modelul implementat respectă specificația. Nu demonstrează că specificația este o descriere bună a cogniției umane.

Validarea științifică pune alte întrebări: modelul reproduce observații importante pentru scopul declarat și o face sub constrângeri care împiedică soluțiile triviale?

## Teste de tipar și ținte empirice

CEM păstrează rezultatele publicate ca **ținte empirice**, nu le transformă automat în parametri. O țintă poate fi direcțională, ordinală, calitativă sau cantitativă. De exemplu, [[VAL:VAL.M0.001]] testează tiparul legat de repetare, iar [[VAL:VAL.M1.003]] testează heterogenitatea relației dintre formularea mesajului și congruența atitudinală.

Un model care reproduce o țintă a trecut un test. Nu a fost „dovedit adevărat”. Mecanisme diferite pot produce același rezultat agregat, iar un model flexibil poate uneori să reproducă tiparul din motive greșite.

De aceea, CEM expune și traiectoriile intermediare. Dacă familiaritatea, accesibilitatea corecției sau fiabilitatea sursei ar trebui să medieze un efect, lanțul intern trebuie să se comporte coerent, nu doar valoarea finală să semene cu rezultatul dorit.

## Ținta empirică nu este parametrul modelului

Mărimea unui efect publicat poate constrânge ceea ce modelul ar trebui să poată reproduce în viitor, dar numărul nu devine coeficient prin simplă copiere.

Dacă un studiu raportează o diferență de 18 puncte procentuale, introducerea valorii 0,18 într-un coeficient intern care are altă scară și altă semnificație ar fi nevalidă. Calibrarea necesită o funcție de observație care leagă stările latente ale simulatorului de măsurătorile reale, un set de date, o procedură de estimare, cuantificarea incertitudinii și o evaluare pe informații care nu au fost folosite pentru estimarea parametrilor.

Alpha 0.4.1a1 nu este calibrat în acest sens.

## Modele nule imbricate și discriminarea între modele

Un mecanism nou este mai informativ dacă produce o predicție pe care modelul mai simplu nu o poate reproduce, în timp ce celelalte condiții relevante rămân controlate.

M1.E1 include de aceea un model nul în care selecția editorială este dezactivată și toate condițiile primesc același set de informații. M1.E2 compară NULL, FRAME_ONLY și FRAME_CONGRUENCE. Sunt comparații imbricate: modelul mai complex trebuie să își justifice componenta suplimentară prin reproducerea unui tipar diferențial pe care modelul mai simplu îl ratează.

Un model nul imbricat nu dovedește că mecanismul adăugat este cauza unică. Arată doar că, în simulator, diferența declarată depinde de acea componentă. **Discriminarea între modele** cere apoi date empirice capabile să favorizeze o explicație candidată în raport cu alta.

## Calibrare, estimare și incertitudine

Calibrarea întreabă ce valori ale parametrilor sunt susținute de date. Este diferită de alegerea unor valori plauzibile pentru demonstrație.

Un proces de calibrare defensabil are nevoie cel puțin de:
- o legătură clară între stările modelului și măsurătorile observate;
- date cu proprietăți de măsurare cunoscute;
- o metodă de estimare;
- cuantificarea incertitudinii parametrilor;
- verificări pentru confundare și neidentificabilitate;
- evaluare predictivă pe date păstrate separat sau cu adevărat externe.

Coeficienții de referință ai CEM nu îndeplinesc aceste condiții ca estimări populaționale. Sunt utili pentru că fac mecanismele inspectabile, nu pentru că valorile lor numerice ar descrie o țară sau o persoană.

## Identificabilitate și sensibilitate

Un parametru este **practic identificabil** atunci când datele și designul disponibile îl constrâng suficient pentru inferența urmărită. **Identificabilitatea structurală** este o întrebare matematică mai puternică: pot două valori diferite ale parametrilor să producă, în principiu, observații indistincte chiar într-un design idealizat?

CEM are în prezent diagnostice locale de sensibilitate și identificabilitate practică. Ele pot arăta că mai multe combinații de parametri produc răspunsuri asemănătoare în jurul configurației de referință. Nu demonstrează identificabilitate structurală și nu oferă distribuții posterioare ale parametrilor.

Analiza de sensibilitate răspunde unei alte întrebări: dacă un parametru sau o ipoteză se modifică într-un interval justificat, cât de mult se schimbă concluzia? Un rezultat care își schimbă sensul după variații mici merită mai puțină încredere decât unul stabil într-un domeniu bine argumentat.

## Validitate externă și transfer

Un mecanism susținut într-o anumită sarcină, populație, țară sau platformă poate să nu se transfere neschimbat în alt context. Capitolele despre formularea mesajelor, algoritmi și intervenții insistă asupra acestei limite tocmai pentru că multe efecte depind de context.

Validarea externă ar trebui să păstreze moderatorii relevanți și să nu se reducă la întrebarea „s-a replicat efectul?”. O calibrare viitoare a CEM ar putea avea nevoie de parametri ierarhici sau specifici contextului, nu de un singur coeficient global.

Trebuie separat și **eșecul generalizării** de **eșecul mecanismului**. Un mecanism poate fi valid doar în condiții de activare mai restrânse decât s-a presupus inițial.

## Triangulare și explicații concurente

Încrederea crește atunci când surse diferite de dovezi converg: experimente controlate, experimente de teren, date longitudinale, urme comportamentale și replicări independente pot constrânge componente diferite ale modelului.

Triangularea nu înseamnă însă numărarea studiilor. Două cercetări care folosesc același indicator indirect și aceeași sursă de eroare nu devin dovezi independente doar pentru că sunt două.

CEM ar trebui să prefere dovezile care ajută la separarea mecanismelor. Un rezultat negativ este științific valoros dacă poate elimina, restrânge sau modifica un mecanism candidat, nu doar dacă duce la introducerea unui nou parametru liber.

## ODD, TRACE și proveniența rezultatelor

[[CONCEPT:odd]] oferă o structură standardizată pentru descrierea scopului, entităților, proceselor, programării evenimentelor, conceptelor de proiectare, inițializării, intrărilor și submodelelor. Actualizarea ODD din 2020 discută explicit necesitatea de a documenta rațiunea modelului și adecvarea sa la scop. TRACE completează această descriere prin documentarea deciziilor de modelare, alternativelor și etapelor de evaluare.

[[VIEW:process]] expune ODD-ul vizual. [[VIEW:reference]] prezintă variabilele, dovezile și limitările. Rulările publicate și hash-urile de proveniență ajută la verificarea faptului că interfața afișează rezultate generate de modelul declarat.

Documentarea crește reproductibilitatea, dar documentarea însăși nu este validare empirică.

## Adecvarea la scop

Validitatea nu este o etichetă universală de tip „valid / invalid”. Un model poate fi adecvat unei utilizări și complet nepotrivit alteia.

M0 poate fi util pentru demonstrarea interacțiunilor dintre mecanisme și pentru testarea regresivă a unor tipare calitative, dar total nepotrivit pentru estimarea prevalenței unei convingeri în România. M1 poate discrimina mecanisme candidate în sarcini sintetice controlate fără să fie apt pentru recomandarea unei politici reale de platformă.

Fiecare versiune ar trebui să declare:
- întrebările pentru care a fost proiectată;
- nivelul la care se aplică afirmațiile sale;
- datele care o constrâng;
- mecanismele importante pe care le omite;
- utilizările pentru care nu trebuie tratată drept validă.

## Ce ar crește încrederea

Încrederea în CEM ar crește prin validare externă preregistrată, seturi de date independente, măsurarea directă a constructelor-cheie, modele de observație calibrate, incertitudine explicită, predicții pe date nevăzute, comparații cu modele rivale și replicări reușite de către alte echipe.

Încrederea ar crește și mai mult dacă unele mecanisme plauzibile ar fi respinse. Un model care poate doar să crească și nu poate pierde niciodată o componentă este greu de falsificat.

## Ce nu afirmă acest capitol

„Toate testele sunt verzi” nu înseamnă „teoria este adevărată”. Un CI verde susține integritatea tehnică și reproductibilitatea definită de suita de teste. Statutul științific depinde de calitatea dovezilor, puterea testelor discriminative, calibrare, generalizare și adecvarea la scop.
