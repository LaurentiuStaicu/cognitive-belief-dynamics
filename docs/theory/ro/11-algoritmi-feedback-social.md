# Ecosisteme informaționale: algoritmi, feedback social, AI și influență strategică

## Ideea centrală

În mediul digital, informația nu ajunge la o persoană printr-un singur mecanism. Conținutul poate fi produs strategic, selectat editorial, ordonat de platforme, redistribuit de alți utilizatori, rezumat de motoare de căutare sau sisteme AI, întâlnit pe mai multe servicii și interpretat prin indicii sociale. De aceea, CEM tratează ecosistemul informațional ca pe o succesiune de etape separabile și evită să traseze o săgeată directă de la „algoritm”, „presă” sau „AI” la convingere.

Un schelet cauzal util este:

producere → disponibilitate editorială → ordonare pe platformă → expunere → atenție/procesare → reprezentare internă → judecată → acțiune → feedback social/de platformă → expuneri ulterioare.

Mecanisme diferite pot interveni în puncte diferite. Efectele lor se pot cumula, anula sau pot depinde de populația și rețeaua în care operează.

[[CONCEPT:algorithm-stage]] · [[VAR:Nexp]] · [[MECH:repetition]] · [[MODULE:MOD.08]] · [[MODULE:MOD.10]] · [[MODULE:MOD.11]] · [[MODULE:MOD.12]] · [[MODULE:MOD.13]] · [[MODULE:MOD.18]] · [[MODULE:MOD.19]] · [[VIEW:structure]]

## De ce „algoritmul m-a făcut să cred” este o explicație prea scurtă

Sistemele de recomandare selectează și ordonează conținut pe baza unor obiective, semnale și constrângeri. Astfel se modifică probabilitatea ca utilizatorul să întâlnească un anumit conținut, frecvența întâlnirii și ordinea în care apar mesajele. Schimbarea convingerii este însă un rezultat ulterior. Depinde de faptul că informația este observată, înțeleasă și integrată, precum și de cunoașterea anterioară, evaluarea sursei, repetiție, context corectiv, congruență și informație socială.

O săgeată directă algoritm → convingere ar ascunde toate aceste etape intermediare. În CEM, un viitor mecanism de ordonare ar trebui să producă mai întâi o schimbare observabilă în expunere sau în compoziția informației întâlnite. Abia apoi mecanismele cognitive existente sau viitoare ar procesa intrarea modificată.

Aceeași logică ne protejează de eroarea opusă. Dacă o intervenție asupra ordonării nu schimbă o atitudine măsurată, nu rezultă că ordonarea nu a avut niciun efect. Poate să fi schimbat expunerea, atenția sau interacțiunea fără să deplaseze judecata măsurată în intervalul studiului.

## Ce arată experimentele pe platforme

Dovezile experimentale nu susțin o poveste universală. Studiile ample realizate pe Facebook și Instagram și publicate în 2023 au arătat că modificări importante ale fluxului de conținut pot schimba expunerea și interacțiunea fără efecte detectabile asupra multor atitudini politice sau asupra polarizării afective în perioada analizată.

În schimb, un experiment de teren publicat în Nature în 2026 pe platforma X a repartizat aleatoriu utilizatorii între un flux algoritmic și unul cronologic timp de șapte săptămâni. Activarea fluxului algoritmic a crescut interacțiunea și a deplasat unele atitudini politice în direcția conținutului promovat disproporționat de acel flux. Studiul a observat și schimbări în conturile urmărite, ceea ce oferă o cale intermediară plauzibilă. Partizanatul declarat și polarizarea afectivă nu s-au modificat semnificativ.

Rezultatele nu sunt contradictorii. Ele arată de ce este necesară o arhitectură pe etape. Efectele depind de platformă, intervenția asupra ordonării, distribuția conținutului, populație, durată și rezultatul măsurat. CEM trebuie să păstreze acești moderatori vizibili în loc să trateze „expunerea algoritmică” drept un tratament universal.

## Eterogenitatea populației și a rețelelor

[[MODULE:MOD.08]] acoperă o limită majoră a demonstrațiilor cu un singur agent. Populațiile reale diferă prin convingeri anterioare, cunoaștere, atenție, repertoriul de surse, poziția în rețea, obiceiurile media și oportunitățile de expunere. Rețelele diferă, la rândul lor, prin grupare, punți între comunități, omofilie și concentrarea conturilor foarte conectate.

Din momentul în care modelăm difuzia socială, efectul mediu individual nu mai este suficient. Același mecanism poate produce rezultate populaționale diferite în funcție de cine este conectat cu cine și de nodurile care primesc sau transmit primele conținutul. Invers, un tipar observat la nivel de populație poate apărea din structura rețelei chiar dacă regulile de actualizare individuală sunt identice.

Alpha 0.4.1a1 nu simulează o rețea populațională. CEM nu trebuie, așadar, să deducă polarizarea de rețea, prevalența unei convingeri sau mărimea unei cascade din scenariile sale actuale de referință.

## Dovezile sociale sunt mai mult decât numărul de interacțiuni

[[MODULE:MOD.18]] privește normele sociale și dovezile colective. Aprecierile, redistribuirile, comentariile, susținerile, dezmințirile și asemănarea cu sursa pot funcționa ca indicii sociale, dar nu au un sens psihologic fix.

O serie de cinci experimente publicată în 2024, cu peste 20.000 de participanți, a arătat că indiciile sociale au influențat judecățile despre dezinformare atunci când au schimbat consensul social perceput; simplele numere mari sau mici de interacțiuni nu au funcționat universal ca semnale persuasive. Și sursele credibile din propriul grup au contat numai în anumite condiții. Acesta este exact tipul de dependență de context pe care CEM trebuie să îl păstreze.

Un viitor mecanism de dovadă socială ar trebui de aceea să separe indicatorul brut al platformei de interpretarea pe care i-o atribuie agentul. „10.000 de aprecieri” este un indiciu observabil. „Majoritatea oamenilor informați cred acest lucru” este o stare socială inferată. Nu trebuie să fie aceeași variabilă.

## Ecosisteme multiplatformă și expunere incidentală

[[MODULE:MOD.10]] reprezintă adaptarea și circulația între platforme. Un utilizator poate vedea o secvență la televiziune, poate căuta ulterior subiectul, poate întâlni un fragment pe o rețea socială, îl poate primi într-o aplicație de mesagerie și, mai târziu, poate întreba un asistent AI despre el. La fiecare tranziție se pot schimba contextul, vizibilitatea sursei, repetiția, audiența și forma prezentării.

O sinteză sistematică din 2023 asupra expunerii incidentale la știri a identificat 88 de studii și a subliniat că știrile digitale sunt întâlnite frecvent în timp ce oamenii folosesc internetul în alte scopuri. Literatura separă și simplul contact incidental de interacțiunea și procesarea ulterioară. Pentru CEM, distincția este centrală: **disponibilitatea nu este expunere, expunerea nu este atenție, iar atenția nu este convingere**.

Un model matur al ecosistemului ar trebui să reprezinte explicit trecerile dintre canale. Alpha 0.4.1a1 doar rezervă această arhitectură.

## Intermediere epistemică om–AI

[[MODULE:MOD.11]] acoperă o etapă informațională tot mai importantă: sistemele AI pot căuta, rezuma, recomanda, explica, traduce sau genera material înainte ca acesta să ajungă la utilizator. În acest rol, AI nu este doar încă o sursă și nici doar un algoritm de ordonare. Poate transforma reprezentarea informației.

O sinteză interdisciplinară publicată în 2024 despre sfaturile oferite de AI arată că folosirea lor depinde de sarcina de decizie, expertiza percepută, încredere, transparență, caracteristicile utilizatorului și mediul decizional. Literatura conține atât aversiune față de algoritmi, cât și preferință pentru recomandări algoritmice; niciuna nu trebuie tratată ca tendință umană universală.

Pentru CEM, întrebarea utilă nu este „au oamenii încredere în AI?”, ci: **în ce condiții un sistem AI schimbă informația disponibilă, modul de prezentare, incertitudinea, vizibilitatea sursei sau procesul propriu de decizie al utilizatorului?** Fiecare cale ar necesita un mecanism diferit.

CEM nu are în prezent un mecanism executabil de LLM sau de recomandare AI. O implementare viitoare trebuie să păstreze separat și corectitudinea rezultatului AI de acceptarea lui de către utilizator.

## Încrederea adecvată: nici maximă, nici minimă

[[MODULE:MOD.12]] privește delegarea și încrederea adecvată. În mod ideal, utilizatorul ar trebui să accepte ajutorul AI atunci când este fiabil și să îl respingă ori să îl verifice atunci când nu este. Dependența excesivă și refuzul nejustificat al ajutorului sunt două tipuri diferite de eroare.

Problema nu poate fi reprezentată corect printr-un singur control global de „încredere în AI”. Dependența poate varia cu sarcina, expertiza de domeniu, incertitudinea, calitatea explicației, consecințele erorii și capacitatea utilizatorului de a verifica rezultatul. Aceeași persoană se poate baza adecvat pe AI într-un domeniu și inadecvat în altul.

Un viitor mecanism CEM ar trebui să compare comportamentul de utilizare a recomandării cu performanța reală a sistemului în aceleași condiții, nu să considere că mai multă încredere este automat mai bună.

## Dobândirea competenței, pierderea competenței și supravegherea umană

[[MODULE:MOD.13]] extinde analiza pe termen mai lung. Delegarea repetată poate modifica ceea ce omul învață, exersează, își amintește sau monitorizează. Dovezile sunt încă în dezvoltare și depind puternic de sarcină.

Un studiu CHI din 2025, realizat cu 319 lucrători ai cunoașterii și 936 de exemple raportate de utilizare a GenAI, a găsit că o încredere mai mare în GenAI era asociată cu un efort auto-raportat mai mic de gândire critică, în timp ce gândirea critică se deplasa către verificare, integrare și supravegherea sarcinii. Fiind un studiu observațional bazat pe auto-raportare, rezultatul nu demonstrează că AI produce declin cognitiv.

O sinteză sistematică din 2026 în domeniul sănătății raportează, de asemenea, preocupări legate de tendința de a accepta automat recomandarea sistemului (automation bias) și de pierderea competențelor, dar descrie o bază de dovezi eterogenă, dominată de studii observaționale, simulări și lucrări conceptuale. Aceste rezultate justifică un modul conceptual, nu un coeficient numeric de „deskilling”.

Distincția importantă este între **substituire** și **realocare**. AI poate reduce efortul pentru o subsarcină și, în același timp, poate crește nevoia de verificare, supervizare sau integrare în altă parte. CEM trebuie să modeleze competența și sarcina concrete, nu o cantitate globală numită „gândire”.

## Influență strategică și producție adversarială

[[MODULE:MOD.19]] întreabă cine produce informația și cu ce obiectiv. Actorii strategici pot selecta teme, coordona repetarea, imita surse credibile, exploata stimulentele platformelor, genera conținut sintetic sau ținti anumite audiențe.

Influența strategică nu este sinonimă cu informația falsă. Comunicarea strategică poate folosi materiale adevărate, false, selectiv incomplete sau încărcate emoțional. Întrebarea cauzală este cum schimbă deciziile de producție informația care intră în etapele ulterioare.

Un viitor mecanism de producție adversarială ar avea nevoie de obiective, acțiuni și observabile explicite. CEM nu trebuie să deducă intenția ascunsă doar din faptul că un conținut este polarizant, popular sau aliniat politic.

## Trei bucle de feedback care trebuie păstrate distincte

Arhitectura extinsă a CEM conține cel puțin trei bucle conceptual diferite.

**Bucla familiarității:** ordonarea sau circulația socială crește expunerea repetată; repetiția poate crește familiaritatea; conținutul familiar poate deveni mai ușor de observat sau de abordat; ordonarea ulterioară poate produce noi expuneri.

**Bucla întăririi sociale:** acțiunea produce semnale sociale vizibile; acestea modifică consensul perceput sau ordonarea platformei; utilizatorii următori primesc un context schimbat.

**Bucla închiderii/angajării față de o concluzie:** o interpretare timpurie poate reduce căutarea ulterioară sau poate diminua impactul informației noi. În versiunea actuală, această buclă este conceptuală și nu trebuie confundată cu întărirea socială.

În realitate, buclele se pot combina. Separarea lor este însă ceea ce permite formularea unor modele falsificabile.

## Ce nu afirmă acest capitol

Nu afirmă că algoritmii sunt neutri sau că sunt cauza unică a polarizării. Nu extrapolează rezultatele de pe X la toate platformele. Nu tratează interacțiunea ca pe o convingere, structura rețelei ca pe psihologie individuală, utilizarea AI ca declin cognitiv sau consensul social ca adevăr. Nu atribuie intenție politică unui sistem de ordonare și nici intenție strategică unui producător de conținut fără dovezi independente.

Mai ales, acest capitol nu face executabile MOD.08, MOD.10–13, MOD.18 sau MOD.19. El explică locul lor în arhitectură și distincțiile empirice necesare înainte de implementare.

## Implicație pentru dezvoltarea viitoare

[[CONCEPT:algorithm-stage]] rămâne CONCEPTUAL. Mecanismele viitoare ale ecosistemului trebuie introduse unul câte unul prin criteriile de extindere ale proiectului: definirea etapei, precizarea observabilelor, formularea predicției diferențiale, păstrarea modelelor nule ale versiunilor mai simple acolo unde este posibil și precizarea rezultatului care ar conta împotriva noului mecanism.
