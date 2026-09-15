# Procesare rapidă, euristici, deliberare și metacontrol

## Ideea centrală

Cercetarea asupra raționamentului distinge procese relativ autonome de procese deliberative care solicită mai mult memoria de lucru. O literatură complementară studiază euristicile: proceduri eficiente de decizie care folosesc intenționat numai o parte din informația disponibilă. CEM folosește prudent ambele perspective. Nici „rapid”, nici „euristic” nu înseamnă automat irațional, iar „lent” sau „deliberativ” nu garantează un răspuns corect.

[[CONCEPT:type1-type2]] · [[MODULE:MOD.02]] · [[MODULE:MOD.09]] · [[MODULE:MOD.15]] · [[VAR:W]] · [[VIEW:reference]]

## Type 1 și Type 2 sunt familii de procese, nu două creiere

Evans și Stanovich susțin că o distincție centrală este autonomia relativă a procesării Type 1 și dependența procesării Type 2 de memoria de lucru și de gândirea ipotetică. Clasificarea este influentă, dar proprietățile asociate în limbajul popular nu se suprapun perfect. Rapid nu înseamnă neapărat irațional, lent nu înseamnă neapărat corect, iar automat nu este sinonim cu emoțional.

De aceea, CEM evită schema simplă „Sistem 1 rău / Sistem 2 bun”. Procesele automate pot încorpora expertiză bine învățată. Deliberarea poate raționaliza o concluzie dorită, poate opera pe dovezi slabe sau poate consuma resurse fără să îmbunătățească decizia. Criticile teoriilor dual-process avertizează și asupra tendinței de a interpreta orice diferență de comportament ca dovadă pentru două arhitecturi psihologice clar separate.

## Euristicile sunt strategii, nu etichete pentru eroare

Literatura despre euristici corectează la rândul ei opoziția simplistă dintre „rațional” și „irațional”. Gigerenzer și Gaissmaier descriu euristicile ca procese cognitive eficiente, conștiente sau inconștiente, care ignoră o parte din informația disponibilă. Performanța unei euristici depinde de sarcină și de structura mediului în care este folosită.

O euristică poate economisi efort și poate rămâne precisă, mai ales când informația este zgomotoasă, eșantioanele sunt mici, timpul este limitat sau câteva indicii conțin cea mai mare parte a informației utile. Aceeași regulă poate funcționa slab într-un alt mediu. Această idee este descrisă adesea prin termenul **raționalitate ecologică**: calitatea unei strategii depinde de potrivirea dintre strategie și mediu, nu doar de strategie privită separat.

În CEM, [[MODULE:MOD.15]] reprezintă de aceea **selecția strategiilor euristice**, nu un modul generic de „biasuri”. O versiune executabilă viitoare ar trebui să precizeze strategiile candidate, indiciile folosite de fiecare strategie, mediul în care este aplicată, costul obținerii informației și tiparul care ar permite discriminarea între strategii. Modelul ar trebui să permită și situații în care o euristică depășește o strategie care folosește mai multă informație.

Alpha 0.4.1a1 nu execută un asemenea selector. Modulul rămâne în arhitectură deoarece alegerea euristicii este importantă pentru teoria generală, dar introducerea acum a unei simple „tendințe euristice” numerice ar amesteca strategii diferite într-o trăsătură greu de interpretat.

## Ce înseamnă metacontrolul

Metacontrolul este folosit aici ca termen-umbrelă pentru alegerea și reglarea procesării: detectarea conflictului, alocarea atenției, verificarea unei intuiții, căutarea de informații suplimentare, alegerea unei strategii sau oprirea căutării. Aceste procese fac legătura cu metacogniția, adică monitorizarea și reglarea propriilor procese cognitive.

Nu există însă motive suficiente pentru a le comprima automat într-o singură „resursă” latentă. Un model viitor ar putea fi nevoit să separe alegerea strategiei, detectarea conflictului, alocarea resurselor și regulile de oprire. Întrebarea empirică este ce distincții produc diferențe observabile pe care un model mai simplu nu le poate explica.

## De ce W nu este „System 2”

[[VAR:W]] este ponderea contextuală acordată acurateții în politica de acțiune M0. Un indiciu care mută atenția către acuratețe poate crește W într-un scenariu. W nu măsoară capacitatea cognitivă generală, IQ-ul, funcția executivă, nevoia de cogniție sau „cât System 2” folosește o persoană. O valoare mai mare a lui W înseamnă doar că acuratețea primește o pondere mai mare în acea decizie simulată.

Limita este importantă. Dacă orice efect al unui indiciu de acuratețe ar fi descris drept „activare a Sistemului 2”, o variabilă specifică unei sarcini ar fi transformată într-un construct psihologic mult mai larg decât permite operaționalizarea ei.

## Conflict, monitorizare și resurse

Un model viitor ar putea separa cel puțin patru întrebări. A apărut un răspuns inițial? A fost detectat un conflict sau un motiv de îndoială? Au existat și au fost mobilizate resurse pentru reconsiderare? Ce strategie a fost aleasă după această monitorizare? Etapele pot varia independent. O persoană poate detecta incertitudinea, dar poate decide că o căutare suplimentară costă prea mult; alta poate delibera mult și totuși să folosească dovezi slabe.

CEM păstrează loc conceptual pentru aceste distincții tocmai pentru a explica variația dependentă de context fără să transforme oamenii în tipuri cognitive fixe.

## Legătura cu următoarele capitole

Capitolul 3 examinează o motivație care poate influența căutarea informației și angajarea față de o concluzie: nevoia de închidere cognitivă. Capitolul 4 tratează separat stresul și resursele executive. Capitolul 8 arată rolul mult mai îngust și executabil al lui [[VAR:W]]. Ordinea este deliberată: o teorie cognitivă largă nu trebuie dedusă retrospectiv dintr-un singur parametru al unei ecuații de decizie.

## Ce nu afirmă acest capitol

Nu afirmă existența a două sisteme neuronale discrete, nu echivalează procesarea rapidă cu eroarea, deliberarea cu adevărul sau euristicile cu biasurile. Nu folosește Type 1/Type 2 sau utilizarea euristicilor pentru a clasifica persoane ori populații. Nu transformă W într-o măsură a raționalității generale. [[MODULE:MOD.15]] rămâne conceptual până când o strategie euristică precisă poate trece criteriile de extindere ale proiectului.

## În aplicație

Inspectează [[VAR:W]] în [[VIEW:reference]] pentru definiția operațională. Folosește harta modulelor pentru [[MODULE:MOD.15]] și separă viitoarea selecție a strategiilor euristice de regula de acțiune M0, care este deja executabilă.
