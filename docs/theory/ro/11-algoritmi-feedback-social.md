# Algoritmi, rețele, ecosistem multiplatformă și feedback social

## Ideea centrală

Un algoritm de ordonare și recomandare poate influența ce informație este văzută, cât de des și în ce ordine, dar aceasta este o etapă cauzală diferită de formarea directă a unei convingeri. CEM separă deliberat traseul ordonare → expunere de traseul expunere → procesare → convingere → acțiune.

[[CONCEPT:algorithm-stage]] · [[VAR:Nexp]] · [[MECH:repetition]] · [[MODULE:MOD.08]] · [[MODULE:MOD.10]] · [[MODULE:MOD.18]] · [[MODULE:MOD.19]] · [[VIEW:structure]]

## De ce afirmația „algoritmul m-a făcut să cred” comprimă prea mult lanțul cauzal

Sistemele de recomandare selectează și ordonează conținutul pe baza unor obiective, semnale și constrângeri. Această selecție poate modifica distribuția expunerilor. Efectul asupra convingerilor depinde apoi de conținut, atenție, cunoaștere anterioară, sursă, repetiție, congruență și context social.

O legătură directă algoritm → convingere ar ascunde, prin urmare, mai multe etape observabile. În CEM, un viitor mecanism de ordonare ar trebui să producă mai întâi o modificare explicită a informației observate sau a [[VAR:Nexp]], după care mecanismele cognitive existente să proceseze acea intrare.

## Ce arată experimentele pe platforme

Dovezile experimentale nu susțin o singură poveste universală. Studiile Facebook/Instagram publicate în 2023 au arătat că modificări importante ale fluxului de conținut pot schimba expunerea și interacțiunea fără efecte detectabile asupra polarizării sau asupra multor atitudini politice în intervalul studiat. Rezultatul avertizează împotriva deducției automate „flux diferit → opinie diferită”.

În schimb, un experiment de teren publicat în Nature în 2026 pe platforma X, cu randomizare între un flux algoritmic și unul cronologic timp de șapte săptămâni, a găsit că activarea fluxului algoritmic a crescut interacțiunea și a deplasat unele atitudini politice în direcția conținutului promovat. Autorii au observat și schimbări în conturile urmărite, ceea ce oferă o cale intermediară plauzibilă. Efectele nu au fost universale: nu au fost detectate schimbări semnificative în partizanatul declarat sau în polarizarea afectivă.

Împreună, aceste rezultate susțin o arhitectură etapizată: algoritmii pot modifica expunerea și uneori pot produce efecte ulterioare asupra atitudinilor, dar direcția și amploarea depind de platformă, intervenție, populație și rezultatul măsurat.

## Impresia titlului nu este același lucru cu accesarea conținutului complet

M1.E3 face executabilă o etapă intermediară fără să o reducă la termenul generic „atenție”. [[VAR:PreviewImpression]] înregistrează faptul că preview-ul unui titlu a fost randat sau disponibil. [[VAR:Access]] înregistrează dacă elementul complet a fost deschis sau accesat prin click. Între ele, [[VAR:Paccess]] este probabilitatea de acces calculată de model. Aceste mărimi sunt separate deliberat de atenție, encodare, convingere, [[VAR:EngageIntent]] și [[VAR:Share]].

Comparatorul de referință păstrează fixe povestea, sursa, imaginea, compatibilitatea factuală și impresia preview-ului. Se modifică numai indiciul binar precomputat [[VAR:Hneg]]: 0 pentru condiția de control cu negativitate mai redusă și 1 pentru condiția cu negativitate mai ridicată. Modelul NULL folosește `logit(Paccess) = b0`, iar modelul candidat [[MECH:access]] folosește `logit(Paccess) = b0 + beta_hneg × Hneg`. Coeficienții sunt demonstrativi și nu sunt ajustați la regresia publicată. [[CODE:m1e3.access_probability]] conține forma executabilă.

Ținta direcțională principală, [[REF:REF.ROBERTSON.2023.NEGATIVITY]], provine din experimente randomizate cu variante de titlu pe Upworthy. Eșantionul confirmator filtrat raportat în textul principal al rezultatelor conține 12.448 de experimente, 53.699 de variante de titlu, peste 205 milioane de impresii și 2.778.124 de clickuri. Modelul sursă folosea un predictor continuu standardizat pentru proporția cuvintelor negative într-o regresie binomială multilevel; CEM nu copiază acel predictor și nici coeficientul publicat în indiciul binar de referință.

Arhiva Upworthy a primit ulterior o corecție privind integritatea randomizării. [[REF:REF.MATIAS.2024.UPWORTHY_CORRECTION]] raportează că rezultatul Robertson rămâne aproape neschimbat atunci când analiza este restrânsă la testele considerate fiabile. Aceasta întărește proveniența, dar nu transformă efectul într-o lege universală. [[REF:REF.NICKL.2025.ATTENTION_ECONOMY]] este păstrată drept contra-dovadă preliminară dintr-un alt context experimental, în care efectul așteptat al negativității nu a fost observat.

[[VAL:VAL.M1.004]] cere ca un Hneg înregistrat mai mare să producă un Paccess mai mare. [[VAL:VAL.M1.N04]] cere convergență când indiciul este dezactivat. [[VAL:VAL.M1.N05]] împiedică Paccess să modifice direct procese cognitive ulterioare, iar [[VAL:VAL.M1.N06]] cere ca lipsa clickului să păstreze PreviewImpression. Folosește [[VIEW:learning]] și deschide [[MECH:access]] pentru a inspecta comparatorul delimitat NULL versus Hneg.

## Expunerea este eterogenă, nu distribuită uniform

Mediile populaționale pot ascunde cozi de distribuție foarte concentrate. Cercetările asupra dezinformării online arată că materialele problematice sunt adesea consumate disproporționat de un subset relativ restrâns de utilizatori, nu uniform de întreaga populație. Un model ajustat doar la o medie populațională poate rata tocmai utilizatorii și pozițiile de rețea în care expunerea repetată este cea mai mare.

[[MODULE:MOD.08]] rezervă eterogenitatea populațională și de rețea. Un model executabil viitor ar trebui să poată reprezenta diferențe de activitate, conectivitate, surse urmărite și oportunități de expunere, în loc să presupună agenți interschimbabili. Eterogenitatea trebuie măsurată sau definită explicit în scenariu, nu introdusă doar pentru a face simularea să pară realistă.

## Feedbackul social ca buclă

Un utilizator vede conținut, reacționează, sistemul observă reacția și poate modifica selecția ulterioară. În paralel, reacțiile altor persoane pot deveni indicii sociale. Astfel poate apărea o buclă:

ordonare → expunere → acțiune → semnal pentru platformă → ordonare.

O altă buclă posibilă este:

expunere la sursă/conținut → familiaritate sau evaluare → acțiune → feedback social → expunere viitoare.

[[MODULE:MOD.18]] rezervă normele sociale și dovezile colective. Numărul de aprecieri, distribuiri, comentarii sau aprobări poate funcționa ca indiciu, dar nu este o măsură directă a adevărului sau a unui consens autentic. Un viitor mecanism de „dovadă socială” trebuie să separe indiciul observat de starea populației care l-a generat.

## Ecosistemul multiplatformă

Informația rareori rămâne într-o singură platformă. O afirmație poate trece dintr-o emisiune de televiziune într-un ziar online, apoi într-o rețea socială, o aplicație de mesagerie, un motor de căutare, o platformă video sau un asistent AI, dobândind la fiecare trecere alte formulări și alte audiențe. Utilizatorii se deplasează și ei între servicii, iar conținutul creat într-un loc poate fi amplificat în altul.

[[MODULE:MOD.10]] rezervă acest ecosistem multiplatformă. Consecința pentru modelare este că platformele nu sunt containere independente de expunere. Transferul dintre platforme poate crea repetiție, poate modifica impresia de diversitate a surselor și poate schimba audiența la care ajung intervențiile. Un viitor mecanism are nevoie, prin urmare, de reguli explicite de transfer, nu de presupunerea că o expunere pe un serviciu este echivalentă cu o expunere oriunde.

## Influența strategică nu este același lucru cu difuzia obișnuită

Unele informații se răspândesc pentru că mulți utilizatori aleg independent să le distribuie. Alte informații sunt produse, țintite sau amplificate deliberat de actori coordonați. Literatura despre propaganda computațională separă actorii, producția de conținut, metodele de distribuție și amplificarea, inclusiv automatizarea, campaniile coordonate și microtargetarea.

[[MODULE:MOD.19]] rezervă influența strategică și producția adversarială. Acest nivel nu trebuie redus la „dezinformare”. Influența strategică poate folosi materiale false, înșelătoare, selectiv adevărate sau complet factuale. Elementul suplimentar relevant este intervenția intenționată sau coordonată asupra producției și distribuției, nu doar factualitatea conținutului.

Un viitor mecanism executabil ar trebui, prin urmare, să distingă difuzia organică de producția ori amplificarea coordonată și să se bazeze pe semnături observabile sau pe scenarii definite extern. CEM nu trebuie să deducă intenția ostilă doar din popularitatea sau distribuția unui conținut.

## Legătura cu repetarea

Dacă ordonarea algoritmică, feedbackul social, transferul între platforme sau amplificarea coordonată cresc frecvența unui conținut, ele pot modifica [[VAR:Nexp]], după care [[MECH:repetition]] poate influența familiaritatea. Aceasta nu înseamnă că orice amplificare produce adevăr iluzoriu: conținutul trebuie să fie efectiv observat și procesat, iar efectul de repetiție trebuie să fie relevant pentru acel tip de conținut.

## Ce nu afirmă acest capitol

Nu afirmă că algoritmii sunt neutri și nici că sunt cauza unică a polarizării. Nu extrapolează rezultatele de pe X la Facebook, TikTok sau la orice altă platformă. Nu presupune că media expunerii descrie fiecare utilizator, nu echivalează aprobarea socială cu adevărul, nu deduce intenția strategică din popularitate și nu tratează interacțiunea cu un conținut drept sinonimă cu convingerea.

## Implicație pentru viitorul modelului

Etapa de ordonare și modulele pentru eterogenitate de rețea, transmitere între platforme, feedback social și influență strategică rămân CONCEPTUAL. Pentru a deveni executabile, fiecare are nevoie de intrări și ieșiri explicite, un model nul, ipoteze măsurabile sau definite prin scenariu și un pattern diferențial pe care un model mai simplu nu îl poate reproduce.