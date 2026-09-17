# Construirea modelului realității

> **Modul:** MOD.14 · **Statut:** mixt EMPIRICAL / EXECUTABLE / CONCEPTUAL / INTERPRETIVE

## Ce anume este „construit”?

În CEM, un model al realității este o **reprezentare relativă la agent, parțială și revizuibilă a unor stări de fapt**. Nu este realitatea externă însăși. Distincția este esențială: agentul nu primește direct „lumea”, ci informație disponibilă filtrată prin percepție și acces; numai o parte este observată sau codificată, memoria furnizează informație anterioară, afirmațiile comunicate au surse și proveniență, iar după actualizare rămâne incertitudine.

MOD.14 conectează, prin urmare, procese deja existente în CEM. Nu creează o a doua stare de familiaritate, o a doua variabilă de fiabilitate a sursei sau o a doua variabilă de convingere. `F`, `C`, `T`, `B`, `Sobs`, `Aissue`, variabilele de preview/acces și cele de prezentare își păstrează sensurile existente.

## Bucla mecanismului

Arhitectura explicativă este:

**informație disponibilă/observată → observare și selecție → recuperarea informației anterioare și a memoriei → evaluarea provenienței și a sursei → interpretarea contextului social → revizuirea propoziției acolo unde există dovadă diagnostică → incertitudine explicită → reevaluare declanșată de contradicție/corecție**.

Aceasta este o arhitectură de organizare, nu o ecuație cauzală liniară universală. Într-o sarcină concretă, unele etape pot lipsi, se pot repeta sau pot fi cuplate.

## Nivelul EMPIRICAL

Mai multe componente ale buclei sunt susținute ca fenomene. Experimente multisenzoriale controlate arată că oamenii pot integra indicii incerte în mod apropiat de integrarea statistică ponderată după fiabilitate în anumite sarcini. Cercetarea asupra situation models descrie reprezentări mentale integrate construite în timpul comprehensiunii. Schemele și cunoașterea anterioară pot influența interpretarea și memoria. Cercetarea asupra source monitoring arată că oamenii fac atribuiri de sursă și pot atribui greșit informația. Literatura despre dezinformare și corecție arată că informația anterioară, repetarea, factorii sociali și revizuirea memoriei pot conta.

Concluzia empirică nu este că o singură ecuație explică procesul. Concluzia mai bine susținută este că formarea reprezentării este selectivă, dependentă de istoric, sensibilă la sursă și purtătoare de incertitudine, iar efectele depind de sarcină și context.

## Nivelul EXECUTABLE: o referință normativă îngustă

MOD.14 execută numai o actualizare bayesiană de referință la nivel de propoziție atunci când sunt furnizate explicit două intrări: probabilitatea anterioară `Pprior` și un raport de verosimilitate diagnostic justificabil `LR`.

`Pwm = (Pprior × LR) / (Pprior × LR + 1 − Pprior)`

Dacă `LR > 1`, posteriorul se deplasează spre propoziție; dacă `0 < LR < 1`, se deplasează în sens opus; `LR = 1` nu produce schimbare. Operatorul refuză valori LR invalide sau absente. CEM nu transformă implicit în LR încrederea în sursă, familiaritatea, acordul social, saliența sau atenția.

A doua cantitate executabilă este entropia Shannon binară normalizată:

`Uwm = −p log2(p) − (1−p) log2(1−p)`

`Uwm` este maximă la `p = 0,5` și zero la `p = 0` sau `p = 1`. Ea descrie incertitudinea **din interiorul acestei stări normative binare înguste**. Nu măsoară necunoașterea legată de specificarea greșită a modelului, ontologii conflictuale sau necunoscute necunoscute.

## De ce `Pwm` nu este `B`

`B` este propensiunea latentă deja existentă în CEM de a judeca o afirmație ca adevărată la un moment dat. Aparține arhitecturii descriptive de simulare. `Pwm` este o probabilitate normativă de referință, transparentă, produsă numai din intrări probabilistice declarate. O persoană poate avea `B` mare în timp ce un model normativ specific domeniului produce `Pwm` mic sau invers. MOD.14 tratează diferența ca potențial informativă, nu o forțează să dispară.

## Percepție și atenție

CEM separă deja disponibilitatea informației de accesarea ei efectivă. O impresie de preview nu dovedește că mesajul a fost fixat vizual, citit, codificat sau înțeles. MOD.14 folosește de aceea **observarea/selecția** ca poartă conceptuală și nu introduce un „coeficient de atenție” continuu inventat. Cercetări viitoare, specifice sarcinii, pot introduce măsurători validate ale atenției, dar acestea trebuie să-și păstreze semantica de măsurare.

## Memorie, informație anterioară și scheme

Informația anterioară poate proveni din cunoaștere stocată, memorie episodică, regularități învățate sau instrucțiunile sarcinii. Cercetarea asupra schemelor indică faptul că structurile anterioare pot îmbunătăți unele forme de procesare, dar pot și distorsiona altele. Cum direcția depinde de sarcină, MOD.14 refuză un semn universal pozitiv sau negativ de la „puterea schemei” către actualizarea convingerii.

Un `Pprior` numeric este permis numai când sarcina sau domeniul îi oferă o interpretare probabilistică justificabilă. În rest, cunoașterea anterioară rămâne conceptuală sau este reprezentată prin constructele CEM specifice sarcinii.

## Surse, proveniență și vigilență epistemică

Source monitoring privește atribuirea informației către origini și contexte. Teoria vigilenței epistemice evidențiază evaluarea informației comunicate și a comunicatorilor. CEM are deja `T`, estimarea relativă la agent a fiabilității unei surse pentru sarcina curentă. MOD.14 păstrează separat trei lucruri:

1. **proveniența** — de unde provine o dovadă și în ce condiții a fost obținută;
2. **fiabilitatea estimată `T`** — o stare psihologică a agentului;
3. **raportul diagnostic `LR`** — o cantitate statistică specifică domeniului.

Niciuna nu este substituită automat celeilalte.

## Context social

Informația comunicată este interpretată social: cine o afirmă, câte surse aparent independente o susțin, ce norme sunt active și ce stimulente sunt percepute pot conta. Dar acordul social este vulnerabil la dependență: zece redistribuiri ale aceluiași raport original nu reprezintă zece observații independente. MOD.14 menține contextul social la nivel conceptual până când o punte de măsurare validată pentru o sarcină furnizează diagnosticitate fără dublă numărare.

## Contradicție, corecție și revizuire

Un model util al realității trebuie să rămână revizuibil. O nouă dovadă contrară poate readuce posteriorul normativ spre incertitudine sau îl poate muta spre propoziția opusă. Actualizarea descriptivă umană poate fi mai lentă sau asimetrică; mecanismele CEM existente privind accesibilitatea corecției și influența continuată sunt vecinătatea potrivită pentru reprezentarea acestor procese descriptive.

## Predictive coding și „creierul bayesian”

Cadrele predictive-coding și Bayesian-brain sunt modele interpretative utile: pun accent pe așteptări generative, erori de predicție și incertitudine. În MOD.14 rămân **INTERPRETIVE** dacă un experiment specific nu furnizează variabile și o formă funcțională validată. CEM nu transformă aceste cadre într-o ecuație universală a creierului numai pentru că pot fi formulate matematic.

## Falsificare și incertitudine

Afirmațiile empirice din MOD.14 au condiții care le-ar slăbi. Integrarea sensibilă la fiabilitate ar trebui să urmărească manipularea experimentală a diagnosticității în sarcinile care pretind acel mecanism. Efectele sursei/provenienței trebuie să se reproducă atunci când informația despre sursă este disponibilă și observată. Efectele informației anterioare/schemelor necesită direcție specifică sarcinii, măsurare și putere statistică adecvată. Un rezultat nul sau invers slăbește afirmația acelei sarcini și nu trebuie ascuns prin modificarea unui coeficient arbitrar.

Regula Bayes executabilă are alt statut: testele ei stabilesc corectitudinea software și algebrică, nu validitatea populațională. Afirmația că oamenii o urmează într-un domeniu concret ar necesita date umane și calibrare separate.

## Limite

MOD.14 nu reactivează M1.E4, Pencode, recrutarea umană sau calibrarea populațională. Phase M rămâne neschimbată. Modulul este complet ca arhitectură științifică și software pentru explicație și calcul normativ de referință, în timp ce punțile descriptive mai bogate către memorie și context social rămân intenționat conceptuale până când dovezile justifică operaționalizarea lor.
