# Intervenții, intermediere om–AI și localizare cauzală

## Ideea centrală

O intervenție este mai ușor de interpretat atunci când este plasată la etapa pe care încearcă să o modifice. CEM separă intervențiile asupra ofertei informaționale, corecției, evaluării sursei și atenției acordate acurateții și rezervă, pentru versiuni viitoare, intervenții asupra atenției, ordonării conținutului, intermedierii om–AI și supravegherii umane.

[[VAR:C]] · [[VAR:W]] · [[MECH:correction]] · [[MECH:accuracy]] · [[MODULE:MOD.11]] · [[MODULE:MOD.12]] · [[MODULE:MOD.13]] · [[VIEW:planning]]

## Intervențiile executabile din M0

Planificatorul actual compară patru măsuri: reducerea repetării, introducerea unui context corectiv, indicii care atrag atenția asupra acurateții și feedback verificat despre sursă. Fiecare acționează într-un punct diferit al mecanismului.

Reducerea repetării modifică expunerile programate și, indirect, familiaritatea. Contextul corectiv actualizează [[VAR:C]]. Un indiciu privind acuratețea modifică [[VAR:W]] în politica de acțiune. Feedbackul despre sursă actualizează fiabilitatea estimată.

Această separare este mai informativă decât un singur scor generic „anti-dezinformare”, deoarece două intervenții pot ajunge la același rezultat final prin căi diferite și pot interacționa neliniar.

## Ce spune cercetarea despre corectare și prebunking

Sintezele contemporane arată că mesajele de corectare pot reduce influența dezinformării și că teama de un efect general de tip backfire a fost adesea exagerată. Totuși, corecțiile pot să nu ajungă la aceeași audiență, iar influența reziduală poate persista. Corecțiile detaliate și explicațiile alternative tind adesea să funcționeze mai bine decât o simplă negare, dar eficiența variază în funcție de subiect, populație și context.

Prebunkingul, numit și inoculare psihologică, încearcă să pregătească oamenii înaintea expunerii, de exemplu prin explicarea unor tehnici de manipulare. Experimentele de amploare au arătat îmbunătățiri în recunoașterea unor astfel de tehnici, dar cercetări mai recente arată și că aceste câștiguri nu se traduc automat într-un discernământ mai bun între adevărat și fals pentru orice tip de conținut. CEM tratează, prin urmare, prebunkingul ca BACKGROUND_THEORY relevant, nu ca pe un coeficient generic deja validat.

Indiciile care readuc atenția asupra acurateții au suport experimental și meta-analitic mai direct pentru discernământul privind distribuirea, motiv pentru care M0 conține [[MECH:accuracy]]. Nici aici nu trebuie dedusă o creștere generală a inteligenței sau raționalității.

## Fricțiune și verificare

Intervențiile de tip fricțiune introduc un cost sau o pauză înaintea distribuirii: deschiderea articolului, confirmarea intenției, verificarea sursei sau un pas suplimentar. CEM nu are încă o variabilă generică pentru fricțiune. O implementare viitoare trebuie să precizeze dacă intervenția schimbă atenția, probabilitatea acțiunii, timpul disponibil sau alt mecanism.

La fel, instruirea în evaluarea credibilității surselor, inclusiv tehnici precum verificarea laterală a surselor (lateral reading), are o bază empirică în educația informațională, dar nu trebuie confundată cu regula delta din M0.

## Intermedierea epistemică om–AI

Sistemele AI pot intra în lanțul informațional în roluri diferite: interfață de căutare sau recuperare a informației, instrument de rezumare, sistem de recomandare, asistent de redactare, suport decizional, tutor, consilier conversațional sau filtru autonom. Aceste roluri nu sunt echivalente. Ele pot modifica informația care este scoasă în evidență, modul în care sunt comprimate dovezile, felul în care este exprimată incertitudinea și cantitatea de efort de verificare care rămâne utilizatorului.

[[MODULE:MOD.11]] rezervă intermedierea epistemică om–AI. Un viitor mecanism executabil ar trebui să precizeze unde se află sistemul AI în lanțul cauzal: înaintea expunerii, în timpul integrării dovezilor, în etapa de judecată sau în cea de acțiune. Tratarea „influenței AI” ca un singur efect nediferențiat ar ascunde aceste căi distincte.

Modelul trebuie să separe și calitatea rezultatului produs de AI de gradul în care utilizatorul se bazează pe acel rezultat. Un sistem foarte precis poate fi folosit prost, iar un sistem imperfect poate fi util dacă recomandările lui sunt verificate adecvat.

## Încredere, utilizare și supraîncredere în automatizare

Literatura de factori umani distinge între încredere și utilizarea efectivă a recomandării, denumită frecvent reliance. Utilizarea adecvată înseamnă să te bazezi pe automatizare atunci când este probabil să ajute și să o verifici sau să o respingi atunci când limitele ei sunt relevante.

[[MODULE:MOD.12]] rezervă delegarea și utilizarea adecvată a automatizării. Cercetările asupra supraîncrederii în automatizare (automation bias) arată că oamenii se pot baza excesiv pe sisteme de suport decizional, mai ales atunci când verificarea este dificilă sau încărcarea cognitivă este mare. Experimente mai recente cu sisteme AI documentează și situații în care participanții urmează recomandări AI chiar dacă acestea intră în conflict cu informații contextuale disponibile. Aceste rezultate justifică modelarea utilizării recomandării ca rezultat distinct, fără a presupune că încrederea, acceptarea și corectitudinea sunt aceeași variabilă.

Un viitor mecanism CEM ar trebui să includă cel puțin fiabilitatea percepută, performanța reală a sistemului, costul verificării și decizia utilizatorului de a accepta, inspecta sau respinge recomandarea.

## Dobândirea competenței, pierderea ei și supravegherea umană

Delegarea repetată poate schimba ceea ce utilizatorul continuă să exerseze. În unele domenii, automatizarea poate sprijini învățarea sau poate elibera resurse pentru activități mai complexe; în altele, reducerea practicii poate slăbi capacitatea de a executa sau verifica independent o sarcină. Dovezile depind de domeniu, iar literatura recentă cea mai directă privind pierderea competenței este concentrată în contexte profesionale, inclusiv sănătate și alte forme de suport decizional.

[[MODULE:MOD.13]] rezervă dobândirea competenței, pierderea competenței și supravegherea umană. CEM nu trebuie să introducă o regulă generică de tip „AI produce pierderea competenței”. O versiune executabilă ar avea nevoie de o stare a competenței specifică sarcinii, de dinamica practicii și feedbackului, de teste ale performanței independente și de un model al modului în care calitatea supravegherii se schimbă în timp.

Supravegherea umană este semnificativă numai dacă persoana păstrează informația, timpul și competența necesare pentru a contesta sistemul. Simpla prezență formală a unui „om în buclă” (human in the loop) nu este echivalentă cu o verificare eficientă.

## Ce optimizează planificatorul actual

Planificatorul evaluează toate subseturile fezabile ale celor patru măsuri M0 pe un orizont sintetic de 13 pași și folosește un obiectiv ponderat între reducerea probabilității de distribuire a informației false și păstrarea distribuirii informației adevărate. Costurile de efort sunt introduse de utilizator. Profilurile scăzut/de referință/ridicat (low/reference/high) sunt verificări de sensibilitate, nu intervale de încredere.

[[VIEW:planning]] nu estimează raporturi reale cost–eficiență, efecte populaționale, acoperire, implementare sau echitate. „Cea mai bună combinație” (best bundle) înseamnă doar cea mai bună opțiune din setul finit analizat și în condițiile ipotezelor alese. Intervențiile om–AI nu fac încă parte din planificatorul executabil.

## Principiul localizării cauzale

Pentru orice intervenție nouă trebuie întrebat:
1. Ce etapă modifică?
2. Ce variabilă observabilă sau latentă se schimbă?
3. Ce tipar diferă față de modelul nul?
4. Ce efect advers sau compromis trebuie urmărit?
5. Ce date ar putea respinge mecanismul?
6. Intervenția modifică și competența viitoare, nu doar decizia imediată?

Această disciplină împiedică introducerea unor măsuri în model doar pentru că „sună utile”.

## Ce nu afirmă acest capitol

Nu transformă o intervenție demonstrativă CEM într-o recomandare de politică publică. Nu presupune că efectele din lumea reală se adună liniar și nu combină experimente din populații diferite ca și cum ar proveni din același set de parametri. Nu afirmă că recomandarea AI este prin definiție superioară sau inferioară judecății umane, că încrederea este identică cu utilizarea recomandării ori că automatizarea produce inevitabil pierderea competenței.

## În aplicație

Folosește [[VIEW:planning]] după ce ai inspectat mecanismele. Planificatorul este un laborator de scenarii: face vizibile dependențele și compromisurile înainte de a indica ce ar merita măsurat într-o evaluare reală. [[MODULE:MOD.11]], [[MODULE:MOD.12]] și [[MODULE:MOD.13]] rămân conceptuale până când rolurile AI, deciziile de utilizare și dinamica competenței vor fi operaționalizate și testate.