# Selecție editorială, presă și lumea observată

## Ideea centrală

Două relatări pot fi ambele compatibile cu faptele și totuși să construiască mostre foarte diferite din aceeași realitate disponibilă. M1.E1 testează o parte îngustă a acestei probleme: păstrează fix un set de informații compatibile cu faptele, modifică politica de selecție și observă cum se schimbă balanța informației văzute și evaluarea ulterioară.

Problema media este însă mai largă. Organizațiile de presă selectează evenimente, stabilesc importanța relativă a subiectelor, aleg surse, construiesc titluri, ordonează materialele și decid ce este repetat. Televiziunile, ziarele, publicațiile online și jurnalismul distribuit prin platforme funcționează și sub constrângeri tehnice, economice și temporale diferite. CEM trebuie de aceea să separe **selecția editorială**, **stabilirea agendei**, **încadrarea și prezentarea**, **repetarea** și **ordonarea algoritmică**, nu să le comprime într-un singur „bias media”.

[[CONCEPT:m1-e1]] · [[VAR:Eedit]] · [[VAR:Sobs]] · [[VAR:Aissue]] · [[MECH:editorial]] · [[MODULE:MOD.16]] · [[VAL:VAL.M1.001]] · [[REF:REF.TOHIDI.2025]] · [[CODE:m1e1.editorial_select]] · [[VIEW:learning]]

## De la realitatea disponibilă la mostra observată

Setul de referință conține obiecte InformationUnit cu valențe între -1 și 1, toate marcate ca fiind compatibile cu faptele. Politica editorială are [[VAR:Eedit]], un accent de referință între -1 și 1, împreună cu un buget fix de selecție.

Accentul negativ favorizează unitățile cu valență negativă; accentul pozitiv, pe cele pozitive; accentul neutru, pe cele apropiate de zero. [[CODE:m1e1.editorial_select]] implementează regula în mod transparent. [[VAR:Sobs]] este media valențelor elementelor selectate.

Eedit nu este un scor măsurat al unei redacții reale. Este o manipulare experimentală sintetică. Sobs nu este „adevărul despre eveniment”, ci balanța mostrei observate.

## Gatekeeping, stabilirea agendei și încadrarea sunt procese distincte

În cercetarea comunicării, **gatekeeping** desemnează procesele prin care se decide ce fragmente de informație trec prin diferite puncte de selecție și ajung la public. Teoria contemporană nu se limitează la un singur editor: rutinele organizaționale, valorile jurnalistice, economia, tehnologia, sursele și distribuția prin platforme pot influența vizibilitatea informației.

**Stabilirea agendei** (agenda setting) privește importanța relativă acordată subiectelor. Dacă un subiect primește în mod repetat o parte mare din atenția disponibilă, iar altul aproape deloc, publicul întâlnește o distribuție diferită a importanței chiar și atunci când materialele individuale sunt corecte factual.

**Încadrarea** (framing) privește felul în care o problemă este organizată și prezentată: ce aspecte sunt puse în prim-plan, ce structură cauzală sau morală este sugerată, ce exemple și imagini sunt alese, cum este formulat titlul și cum sunt legate faptele într-o narațiune. Capitolul 10 izolează o manipulare de prezentare mult mai restrânsă, cu semnificația semantică păstrată constantă; aceasta nu trebuie confundată cu sensul mai larg al framingului din teoria comunicării.

Distincțiile sunt importante deoarece același material observat poate reflecta simultan mai multe mecanisme. Strategia științifică a CEM este să le separe experimental ori de câte ori este posibil.

## Televiziunea și presa online nu sunt canale interschimbabile

Știrile de televiziune combină selecția cu ordinea temporală, saliența audiovizuală, timpul de emisie limitat și un flux în mare măsură liniar. Publicațiile online pot păstra arhive extinse, actualiza continuu articolele, modifica titluri, lega materiale între ele și ordona conținutul pe pagina principală. Platformele sociale pot redistribui apoi același material jurnalistic prin sisteme de recomandare și semnale sociale.

Literatura despre televiziune identifică mai multe funcții decât simpla transmitere a faptelor, printre care supravegherea mediului, interpretarea, socializarea și competiția pentru atenție. Cercetarea știrilor digitale arată, la rândul ei, că oamenii întâlnesc frecvent informații de presă în mod incidental, în timp ce folosesc servicii online în alte scopuri, iar simplul contact trebuie deosebit de procesarea mai profundă a conținutului.

CEM nu presupune că un efect estimat într-un canal se transferă neschimbat în altul. Tipul de mediu, formatul și traseul expunerii sunt moderatori candidați, nu detalii cosmetice.

## De la mostră la evaluare

M1.E1 actualizează [[VAR:Aissue]] prin:

Aissue' = clip(Aissue + g × Sobs, -1, 1),

cu g = 0.25 în experimentul de referință. Ecuația este deliberat necalibrată. Aissue reprezintă evaluarea unei probleme sau a unui eveniment în M1.E1 și nu este convingerea M0 [[VAR:B]] despre adevărul unei afirmații.

Ecuația trebuie citită ca o legătură candidată transparentă: o mostră observată cu altă balanță poate deplasa evaluarea. Nu este o ecuație generală a „influenței media”.

## Ancora empirică

[[REF:REF.TOHIDI.2025]] descrie un experiment preregistrat cu 2.141 de participanți și șapte evenimente, în care articole sintetice pozitive, neutre și negative au selectat diferit informații factuale. Condiția negativă a produs sentimente și opinii mai negative decât condiția neutră.

CEM folosește rezultatul ca țintă direcțională la nivel de fenomen. Studiul nu măsoară Eedit, Sobs sau Aissue și nu poate separa în mod unic efectul selecției informației de tonul prezentării. De aceea mecanismul exact rămâne CANDIDATE.

Limita este esențială. Chiar dacă modelul reproduce tiparul Tohidi, aceasta nu demonstrează că selecția editorială este cauza unică a efectului uman; arată doar că mecanismul candidat poate reproduce o direcție constrânsă respectând invariantele modelului.

## Sistemul editorial are instituții și stimulente

[[MODULE:MOD.16]] este mai larg decât M1.E1. Redacțiile reale funcționează sub norme profesionale, reguli juridice, structuri de proprietate, termene-limită, concurență, cerere din partea publicului și presiuni comerciale. Toate acestea pot influența ce este selectat și cum este prezentat.

CEM nu ar trebui să le reducă la un singur scor ideologic. Dacă o versiune viitoare modelează un stimulent, trebuie să precizeze consecința observabilă: de exemplu, o schimbare a probabilității de selecție, a importanței acordate unui subiect, a alegerii titlului, a efortului de verificare sau a momentului publicării.

Aceeași regulă se aplică presei online și televiziunilor. Modelul trebuie să reprezinte mecanismul testat, nu să deducă mecanismul dintr-o etichetă politică atribuită instituției media.

## Modelul nul imbricat: testul esențial

Când selecția editorială este dezactivată, toate condițiile trebuie să primească același set complet. Diferența dintre condiții trebuie să dispară. Constrângerea împiedică modelul să „fabrice” efectul prin schimbări ascunse ale faptelor, setului informațional sau stării agentului.

[[VAL:VAL.M1.001]] verifică tiparul cu selecția activă. Modelul nul asociat verifică dispariția diferenței când selecția este eliminată.

## Relația cu ordonarea algoritmică

Selecția editorială și ordonarea algoritmică pot apărea succesiv. O redacție decide mai întâi ce publică; site-ul poate ordona materialele publicate; apoi o platformă socială poate decide care dintre ele ajunge la un anumit utilizator. Etapele se pot influența reciproc, dar nu sunt identice.

Capitolul 11 tratează separat ordonarea, fluxurile dintre platforme și feedbackul social. Un efect al platformei nu trebuie atribuit redacției fără dovezi, iar un efect editorial nu trebuie atribuit automat „algoritmului”.

## Ce nu afirmă acest capitol

Nu afirmă că negativ înseamnă fals, că jurnalismul poate fi rezumat printr-o singură axă de bias, că stabilirea agendei sau încadrarea determină opinia ori că toate canalele media produc aceleași efecte. Nu atribuie efectul Tohidi algoritmilor platformelor și nu îl extrapolează cantitativ la populații reale sau la anumite instituții media din România.

## În aplicație

Deschide [[VIEW:learning]] și [[MECH:editorial]] pentru a urmări setul disponibil → selecție → Sobs → Aissue. Folosește [[VIEW:reference]] pentru a verifica ce înseamnă și ce nu înseamnă fiecare variabilă. Apoi compară manipularea de prezentare din Capitolul 10 și nivelul de platformă/ecosistem din Capitolul 11.
