# Surse, autoritate epistemică și fiabilitate estimată

## Ideea centrală

Informația nu este evaluată independent de sursa ei. Oamenii pot folosi indicii despre expertiză, încredere, rol instituțional și experiența anterioară pentru a decide câtă greutate să acorde unei afirmații. M0 reprezintă doar o parte minimală a acestei probleme: agentul păstrează o estimare a fiabilității sursei și o actualizează după feedback.

[[VAR:T]] · [[VAR:B]] · [[MECH:source]] · [[VAL:VAL.M0.003]] · [[CODE:m0.update_reliability]] · [[MODULE:MOD.20]] · [[VIEW:runs:source:6]]

## Trei lucruri care trebuie păstrate separat

Primul este performanța sau calitatea reală a sursei în mediul experimental. Al doilea este ceea ce agentul crede despre acea sursă. Al treilea este adevărul afirmației curente. În CEM, [[VAR:T]] reprezintă numai fiabilitatea estimată de agent. T nu este adevăr și nu este un scor universal și obiectiv de reputație.

Separarea evită circularitatea. O sursă nu trebuie considerată „bună” doar pentru că agentul are încredere în ea, iar o afirmație nu devine adevărată doar pentru că provine de la o sursă evaluată pozitiv. Invers, o sursă poate fi fiabilă în medie și totuși să greșească într-un caz particular.

## Regula de învățare de referință

M0 folosește o regulă delta simplă:

T' = clamp01(T + alpha_t × (outcome - T)),

unde outcome este 1 pentru feedback corect și 0 pentru feedback incorect în sarcina sintetică. Implementarea poate fi inspectată în [[CODE:m0.update_reliability]].

Când dovada intră în calculul convingerii, M0 transformă T din intervalul [0,1] într-o pondere a sursei în [-1,1] prin 2T - 1. Astfel, dovezi comparabile pot avea un efect diferit în funcție de fiabilitatea estimată.

Aceasta este o alegere de modelare intenționat simplă. Nu presupune actualizare bayesiană optimă, o valoare alpha_t fixată empiric sau o încredere unidimensională.

## Ce adaugă literatura empirică

Experimentele asupra credibilității sursei arată că oamenii pot folosi informația despre fiabilitate atunci când își actualizează convingerile. Experimentele publicate de Sanna și Lagnado în 2025 sunt deosebit de utile pentru CEM deoarece separă feedbackul despre sursă de adevărul afirmației și arată că atât încrederea în buna-credință a sursei, cât și expertiza pot contribui la evaluarea fiabilității.

Literatura arată și de ce CEM nu ar trebui să comprime întreaga evaluare a sursei într-o esență psihologică numită simplu „încredere”. Expertiza privește competența într-un domeniu relevant. Încrederea în buna-credință privește așteptarea că sursa comunică onest și fidel. Familiaritatea, apartenența la un grup, reputația instituțională și performanța anterioară pot oferi alte indicii. Uneori aceste indicii converg; alteori nu.

M0 comprimă problema multidimensională într-o singură stare T pentru a putea testa un mecanism de referință controlat. Compresia este o limită a modelului, nu o afirmație despre natura reală a încrederii.

## Fiabilitatea unei surse nu este același lucru cu autoritatea epistemică

[[MODULE:MOD.20]] păstrează o întrebare mai largă: cum se bazează oamenii și societățile pe instituții și autorități epistemice?

O instituție epistemică poate organiza expertiză, verificare, corectare, responsabilitate și păstrarea evidențelor prin cooperarea mai multor persoane. Revistele științifice, institutele de statistică, instanțele, organizațiile profesionale, redacțiile și organizațiile de verificare a faptelor sunt foarte diferite între ele, dar ilustrează de ce credibilitatea instituțională nu poate fi redusă la onestitatea unui singur vorbitor.

Autoritatea instituțională poate funcționa ca o scurtătură rezonabilă atunci când verificarea directă este prea costisitoare. Poate însă eșua prin conflicte de interese, proceduri slabe, opacitate sau pierderea istorică a încrederii. Un model mai complet ar trebui să separe cel puțin **autoritatea revendicată**, **garanțiile procedurale**, **expertiza de domeniu**, **performanța observată în timp** și **estimarea de fiabilitate a agentului**.

Alpha 0.4.1a1 nu execută aceste niveluri instituționale. T nu trebuie prezentat niciodată ca un scor numeric pentru „știință”, „presă”, „guvern” sau o altă instituție.

## Feedback, dezacord și revizuire

Evaluarea unei surse se poate schimba atunci când predicțiile îi sunt confirmate, afirmațiile îi sunt corectate sau surse independente intră în dezacord. Învățarea poate deveni bidirecțională: convingerile despre sursă influențează interpretarea dovezii, iar rezultatele interpretate modifică ulterior convingerile despre sursă.

Astfel poate apărea o buclă de feedback. Un model mai bogat trebuie să evite circularitatea păstrând observațiile externe distincte de interpretarea lor și separând performanța sursei de felul în care agentul o percepe.

M0 modelează numai o versiune controlată a acestei bucle. Nu modelează coaliții de surse, validare instituțională, atacuri coordonate asupra reputației, cascade de prestigiu sau încercări strategice de a imita autoritatea.

## Identitate socială și indicii de credibilitate

Asemănarea cu o sursă poate conta în anumite condiții, dar asemănarea nu este echivalentă cu credibilitatea. Experimente ample asupra indiciilor sociale și de sursă arată efecte condiționate de context: consensul social perceput și sursele credibile din propriul grup pot influența judecățile, în timp ce simplele numere de interacțiuni nu funcționează ca semnale universale de persuasiune.

Pentru CEM, aceasta este o avertizare împotriva unei reguli directe de tip „sursă din grupul meu → convingere”. Identitatea, credibilitatea și consensul social aparțin unor etape cauzale separabile și ar trebui măsurate independent ori de câte ori este posibil.

## Tiparul M0

[[VAL:VAL.M0.003]] verifică dacă feedbackul despre sursă poate modifica T și dacă dovezi comparabile primesc apoi ponderi diferite. Deschide [[VIEW:runs:source:6]] pentru scenariul de referință.

Testul confirmă o dependență internă a modelului candidat. Nu demonstrează că regula delta este singura regulă psihologică posibilă de învățare.

## Ce nu afirmă acest capitol

Nu afirmă că încrederea este fixă, unidimensională sau independentă de identitate și context. Nu afirmă că experții ori „sursele verificate” sunt infailibile. Nu tratează T ca adevăr și nu deduce legitimitatea instituțională din popularitate. Nici neîncrederea nu este declarată automat irațională: uneori poate reflecta dovezi relevante, iar alteori poate fi produsă de semnale înșelătoare.

## Statut epistemic

Mecanismul M0 de învățare a fiabilității este EXECUTABLE/CANDIDATE. Efectele credibilității sursei au suport empiric. Regula delta exactă și transformarea 2T - 1 rămân REFERENCE_CANDIDATE. Stratul instituțional mai larg din [[MODULE:MOD.20]] este CONCEPTUAL și necesită o operaționalizare și o validare separate.
