# Selecție editorială și lumea observată

## Ideea centrală

Două prezentări pot fi factuale și totuși pot construi mostre foarte diferite din aceeași realitate disponibilă. M1.E1 testează această idee fără a confunda negativitatea cu falsitatea: ține fix un pool de unități compatibile cu faptele, schimbă politica de selecție și observă cum se modifică balanța informației văzute și evaluarea ulterioară.

[[CONCEPT:m1-e1]] · [[VAR:Eedit]] · [[VAR:Sobs]] · [[VAR:Aissue]] · [[MECH:editorial]] · [[VAL:VAL.M1.001]] · [[REF:REF.TOHIDI.2025]] · [[CODE:m1e1.editorial_select]] · [[VIEW:learning]]

## De la lume disponibilă la mostră observată

Pool-ul de referință conține unități InformationUnit cu valențe între -1 și 1 și toate sunt marcate fact-compatible. Politica editorială are [[VAR:Eedit]], un accent de referință între -1 și 1, plus un buget fix de selecție.

Cu accent negativ sunt preferate unitățile cu valență negativă; cu accent pozitiv, cele pozitive; cu accent neutru, cele apropiate de zero. [[CODE:m1e1.editorial_select]] aplică regula transparentă. [[VAR:Sobs]] este media valențelor selectate.

Important: Eedit nu este un scor măsurat al unei redacții reale. Este o manipulare experimentală sintetică. Sobs nu este „adevărul evenimentului”, ci balanța mostrei observate.

## De la mostră la appraisal

M1.E1 actualizează [[VAR:Aissue]] prin forma simplă:

Aissue' = clip(Aissue + g × Sobs, -1, 1),

cu g = 0.25 în experimentul de referință. Această ecuație este deliberat necalibrată. [[VAR:Aissue]] reprezintă evaluarea unei probleme/eveniment în experimentul M1.E1 și nu este convingerea M0 [[VAR:B]] despre adevărul unei afirmații.

## Ancora empirică

[[REF:REF.TOHIDI.2025]] descrie un experiment preregistrat cu 2.141 participanți și șapte evenimente, în care articole sintetice pozitive, neutre și negative au selectat informații factuale în mod diferit. Framingul negativ a produs evaluări afective și opinii mai negative față de condiția neutră.

CEM folosește acest rezultat ca țintă direcțională la nivel de fenomen. Studiul nu măsoară Eedit, Sobs sau Aissue și nu poate identifica separat efectul selecției față de tonul prezentării. De aceea mecanismul exact rămâne CANDIDATE.

## Nested null: testul esențial

Când editorial selection este dezactivat, toate condițiile trebuie să primească același pool complet. Diferența dintre condiții trebuie să dispară. Această constrângere împiedică modelul să „fabrice” efectul schimbând faptele, pool-ul sau starea agentului pe ascuns.

[[VAL:VAL.M1.001]] verifică patternul cu selecția activă. Null-ul asociat verifică dispariția efectului când selecția este eliminată.

## Ce nu afirmă acest capitol

Nu afirmă că negativ înseamnă fals, că presa poate fi rezumată printr-o singură axă de bias sau că selectarea informației determină unic opinia. Nu spune că algoritmii platformelor produc efectul Tohidi și nu extrapolează numeric la populații reale.

## În aplicație

Deschide [[VIEW:learning]] și mecanismul [[MECH:editorial]] pentru a urmări pool → selecție → Sobs → Aissue. Distincția va fi importantă în capitolul 11, unde rankingul algoritmic este plasat într-o altă etapă a lanțului causal.