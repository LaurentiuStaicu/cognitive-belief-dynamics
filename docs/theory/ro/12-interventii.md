# Intervenții: unde acționăm în lanțul cauzal

## Ideea centrală

O intervenție este mai ușor de înțeles atunci când este plasată exact în etapa pe care încearcă să o modifice. CEM separă intervențiile asupra ofertei informaționale, corecției, evaluării sursei și atenției acordate acurateții. În versiuni viitoare pot fi adăugate intervenții asupra atenției și consumului, dovezilor sociale, intermedierii AI sau ordonării algoritmice, dar numai după operaționalizare și testare.

[[VAR:C]] · [[VAR:W]] · [[MECH:correction]] · [[MECH:accuracy]] · [[VIEW:planning]]

## Intervențiile executabile în M0

Modulul actual de planificare compară patru măsuri: reducerea repetării, introducerea unui context corectiv, orientarea atenției către acuratețe și feedback verificat despre sursă. Fiecare intervine într-un punct diferit al mecanismului.

Reducerea repetării modifică expunerile programate și, indirect, familiaritatea. Contextul corectiv actualizează [[VAR:C]]. Indiciul de orientare către acuratețe modifică [[VAR:W]] în politica de acțiune. Feedbackul despre sursă actualizează estimarea fiabilității.

Separarea este mai informativă decât un singur scor „anti-dezinformare”, deoarece două intervenții pot produce același rezultat final prin căi diferite, iar combinațiile lor pot avea efecte neliniare.

## Corectare și inoculare informațională

Sintezele contemporane arată că dezmințirea și corectarea informației false pot reduce influența dezinformării, iar teama că o corecție produce în mod obișnuit un efect invers a fost exagerată. Corecțiile nu ajung însă întotdeauna la aceeași audiență ca informația inițială, iar o parte din influența acesteia poate persista.

Inocularea informațională, numită adesea *prebunking* în literatura internațională, încearcă să pregătească oamenii înainte de expunere, de exemplu prin explicarea tehnicilor de manipulare. Experimente și sinteze recente indică îmbunătățiri ale discernământului în anumite condiții. În CEM, aceste rezultate sunt deocamdată BACKGROUND_THEORY: nu există încă un mecanism executabil separat pentru inoculare.

Orientarea atenției către acuratețe are o legătură experimentală mai directă cu discernământul privind distribuirea și este de aceea reprezentată în M0 prin [[MECH:accuracy]].

## Fricțiune, verificare și educație informațională

Unele intervenții introduc o mică pauză sau un cost suplimentar înainte de distribuire: deschiderea articolului, confirmarea intenției, verificarea sursei ori un pas suplimentar. CEM nu are încă o variabilă generică pentru acest tip de fricțiune. O implementare viitoare trebuie să precizeze dacă intervenția modifică atenția, timpul de deliberare, probabilitatea acțiunii sau alt mecanism.

În mod similar, instruirea pentru evaluarea credibilității surselor, inclusiv verificarea laterală a unei surse prin consultarea independentă a altor resurse, are suport în literatura de educație informațională. Ea nu trebuie însă confundată cu regula delta simplificată prin care M0 actualizează T.

## Intervențiile asupra ecosistemului

Capitolul 11 arată că unele intervenții nu vizează direct procesarea individuală. Ele pot modifica producția conținutului, selecția editorială, politica de recomandare, vizibilitatea dovezilor sociale, proiectarea interfeței sau felul în care un sistem AI prezintă incertitudinea și sursele.

Această diferență este importantă pentru politici publice. O intervenție asupra platformei și una asupra utilizatorului pot avea același obiectiv final, dar costuri, mecanisme, efecte adverse și distribuții ale beneficiilor foarte diferite.

CEM nu le compară încă numeric. Ele trebuie mai întâi să primească un loc cauzal clar și un rezultat observabil.

## Ce optimizează modulul actual de planificare

Modulul de planificare evaluează toate combinațiile fezabile ale celor patru măsuri executabile pe un orizont sintetic de 13 pași. Obiectivul ponderat încearcă să reducă probabilitatea distribuirii unei afirmații false fără să reducă excesiv distribuirea unei afirmații adevărate. Costurile de efort sunt introduse de utilizator.

Profilurile scăzut/referință/ridicat sunt analize de sensibilitate, nu intervale de încredere. [[VIEW:planning]] nu estimează raporturi cost–beneficiu reale, efecte populaționale, acoperirea audienței, fezabilitatea implementării sau echitatea distribuirii costurilor și beneficiilor.

„Cea mai bună combinație” înseamnă numai cea mai bună dintre opțiunile finite evaluate, sub ipotezele și ponderile alese.

## Principiul localizării cauzale

Pentru orice intervenție nouă trebuie puse cel puțin cinci întrebări:

1. Ce etapă a lanțului modifică?
2. Care este variabila observabilă sau latentă afectată?
3. Ce tipar trebuie să se schimbe față de modelul nul?
4. Ce efect advers, compromis sau efect distributiv trebuie urmărit?
5. Ce date ar putea contrazice mecanismul propus?

Această disciplină împiedică introducerea unor măsuri în model doar pentru că „sună utile”.

## Efect cumulativ nu înseamnă simplă adunare

Două intervenții pot acționa asupra aceleiași etape, asupra unor etape succesive sau asupra unor ramuri diferite. Efectul lor combinat poate fi subaditiv, aproximativ aditiv sau supra-aditiv. De aceea, obiectivul de a obține un impact cumulat mare nu justifică însumarea directă a efectelor estimate în studii diferite.

CEM poate explora interacțiuni în interiorul propriului model, dar pentru recomandări reale sunt necesare dovezi despre implementare, context, costuri, efecte adverse și generalizare.

## Ce nu afirmă acest capitol

Nu afirmă că o intervenție demonstrativă CEM este o recomandare de politică. Nu presupune că efectele se adună liniar în lumea reală și nu tratează rezultate experimentale obținute în populații diferite ca și cum ar fi parametri direct comparabili.

## În aplicație

Folosește [[VIEW:planning]] numai după ce ai inspectat mecanismele și dovezile. Modulul de planificare trebuie citit ca un laborator de scenarii: arată dependențe și compromisuri și ajută la formularea întrebărilor pentru o evaluare reală; nu substituie acea evaluare.
