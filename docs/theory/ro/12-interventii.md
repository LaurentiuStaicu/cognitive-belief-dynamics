# Intervenții: unde acționăm în lanțul causal

## Ideea centrală

O intervenție este mai ușor de înțeles când este plasată la etapa pe care încearcă să o modifice. CEM separă intervenții asupra ofertei informaționale, corecției, evaluării sursei, atenției la acuratețe și, în versiuni viitoare, atenției/consumului sau ordonarea algoritmicăui.

[[VAR:C]] · [[VAR:W]] · [[MECH:correction]] · [[MECH:accuracy]] · [[VIEW:planning]]

## Intervențiile executabile M0

Modulul de planificare actual compară patru măsuri: reducerea repetării, context corectiv, indicii de orientare către acuratețe și feedback verificat despre sursă. Fiecare are un loc diferit în mecanism.

Reducerea repetării acționează asupra expunerilor programate și, indirect, asupra familiarității. Contextul corectiv encodează [[VAR:C]]. Accuracy cue modifică [[VAR:W]] în politica de acțiune. Feedbackul de sursă actualizează estimarea fiabilității.

Această separare este mai informativă decât un singur scor „anti-dezinformare”, deoarece două intervenții pot produce același rezultat final prin căi diferite și pot interacționa neliniar.

## Ce spune literatura despre corectarea informației false și inoculare informațională

Sintezele contemporane arată că corectarea informației false poate reduce influența dezinformării și că teama de backfire generalizat a fost adesea exagerată. Totuși, corecțiile nu ajung întotdeauna la aceeași audiență și influența reziduală poate persista.

Prebunkingul sau inocularea încearcă să pregătească oamenii înaintea expunerii, de exemplu explicând tehnici de manipulare. Experimente pe scară largă au găsit îmbunătățiri ale discernământului față de tehnici de dezinformare. Aceste intervenții sunt relevante ca BACKGROUND_THEORY, dar nu există încă un mecanism inoculare informațională executabil separat în CEM.

Indiciile de orientare către acuratețe au un suport experimental și meta-analitic mai direct pentru discernământul de distribuire, motiv pentru care M0 are un mecanism [[MECH:accuracy]].

## Fricțiune și verificare

Intervențiile de fricțiune pot introduce un cost sau o pauză înaintea distribuirii: citirea articolului, confirmarea intenției, verificarea sursei sau un pas suplimentar. CEM nu are încă o variabilă generică de fricțiune. O implementare viitoare trebuie să specifice dacă fricțiunea schimbă atenția, probabilitatea de acțiune, timpul disponibil sau alt mecanism.

La fel, instruirea în evaluarea credibilității surselor, inclusiv verificare laterală a surselor, are o bază empirică în educația informațională, dar nu trebuie confundată cu delta-rule-ul M0.

## Ce optimizează modulul de planificare actual

Modulul de planificare evaluează toate subseturile fezabile ale celor patru măsuri pe un orizont sintetic de 13 pași și un obiectiv ponderat între reducerea probabilității de distribuire fals și menținerea distribuirii adevărat. Costurile de efort sunt introduse de utilizator. Profilurile scăzut/referință/ridicat sunt analize de sensibilitate, nu intervale de încredere.

[[VIEW:planning]] nu estimează cost-beneficiu real, efecte populaționale, acoperirea audienței, implementare sau equity. „Best combinație” înseamnă doar cel mai bun în setul finit și sub ipotezele selectate.

## Principiul causal-location

Pentru orice intervenție nouă trebuie întrebat:
1. Ce etapă modifică?
2. Care este variabila observabilă sau latentă?
3. Ce tipar se schimbă față de null?
4. Ce efect advers sau compromis trebuie urmărit?
5. Ce date ar putea falsifica mecanismul?

Această disciplină împiedică introducerea măsurilor doar pentru că „sună utile”.

## Ce nu afirmă acest capitol

Nu afirmă că o intervenție demonstrativă CEM este recomandare de politică. Nu presupune că efectele se adună liniar în lumea reală și nu compară rezultate experimentale din populații diferite ca și cum ar fi aceiași parametri.

## În aplicație

Folosește [[VIEW:planning]] după ce ai inspectat mecanismele. Modulul de planificare trebuie citit ca un laborator de scenarii: explică dependențele și compromisurile înainte de a sugera ce ar merita măsurat într-o evaluare reală.