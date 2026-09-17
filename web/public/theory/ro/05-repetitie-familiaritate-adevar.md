# Repetiție, familiaritate și adevăr perceput

## Ideea centrală

Repetiția poate crește probabilitatea ca o afirmație să fie evaluată drept adevărată chiar dacă repetarea nu adaugă dovezi noi. Fenomenul este cunoscut drept efectul de adevăr iluzoriu. În M0, CEM îl reprezintă printr-un traseu minimal: expunerile cresc o stare de familiaritate, iar familiaritatea contribuie pozitiv la log-odds-ul convingerii.

[[VAR:Nexp]] · [[VAR:F]] · [[VAR:B]] · [[MECH:repetition]] · [[VAL:VAL.M0.001]] · [[REF:REF.DECHENE.2010]] · [[CODE:m0.update_familiarity]] · [[VIEW:runs:repetition:4]]

## Ce spune cercetarea

Meta-analiza lui Dechêne și colaboratorii a sintetizat 51 de studii și a confirmat că repetarea poate crește evaluările subiective de adevăr. Literatura ulterioară arată că efectul poate apărea chiar și atunci când participanții dețin cunoștințe relevante, dar nu este nelimitat și depinde de tipul afirmației, de instrucțiuni, de indicii privind veridicitatea și de context.

O meta-analiză publicată în 2026, bazată pe 182 de studii și 366 de mărimi ale efectului, estimează un efect mediu mic după corecția pentru efectele studiilor mici, cu eterogenitate importantă între studii. Tocmai această variație împiedică transformarea formulei „repetiția crește adevărul perceput” într-o lege universală.

Un studiu publicat în 2026 asupra afirmațiilor evaluative social-politice a găsit efecte neglijabile ale repetării în condițiile testate. CEM tratează această limită ca motiv pentru a nu extrapola automat mecanismul M0 de la afirmații factuale la opinii normative sau identitare.

## Cum este implementat în M0

[[VAR:Nexp]] numără expunerile din scenariu. [[VAR:F]] este familiaritatea latentă a agentului cu afirmația. Actualizarea de referință este saturantă:

F' = clamp01(F + alpha_f × (1 - F)).

Aceasta înseamnă că fiecare expunere suplimentară poate crește F, dar câștigul marginal scade pe măsură ce familiaritatea se apropie de 1. Funcția poate fi inspectată în [[CODE:m0.update_familiarity]].

În calculul convingerii, familiaritatea contribuie prin termenul beta_f × F la log-odds. Convingerea [[VAR:B]] rezultă după transformarea logistică, împreună cu priorul, semnalul ponderat de sursă și contextul corectiv. Adevărul cunoscut de mediul simulat nu intră direct în această funcție.

Forma saturantă este o alegere de modelare REFERENCE_CANDIDATE. Literatura susține fenomenul de repetiție și familiaritate, nu parametrul alpha_f sau forma exactă a saturației.

## De ce familiaritatea nu este adevăr

F este o stare internă care descrie cât de familiară este afirmația. Nu reprezintă adevărul ei, cantitatea de dovezi, frecvența reală a evenimentului sau fiabilitatea sursei. O afirmație adevărată și una falsă pot deveni ambele familiare dacă sunt repetate.

Această separare este una dintre regulile epistemice importante ale CEM: un mecanism care influențează judecata nu trebuie reinterpretat drept proprietate a lumii.

## Testul de tipar

[[VAL:VAL.M0.001]] cere ca, în condiții comparabile, expunerea repetată să poată crește evaluarea de adevăr. Testul verifică un tipar calitativ, nu reproduce mărimea unui efect populațional. Deschide [[VIEW:runs:repetition:4]] pentru traiectoria publicată.

## Ce nu afirmă acest capitol

Nu afirmă că orice repetiție convinge, că efectul este identic pentru fapte și opinii sau că familiaritatea anulează cunoașterea. Nu spune că mass-media ori algoritmii produc automat convingeri prin simplă repetare; pentru o asemenea concluzie ar trebui modelate separat expunerea, selecția, atenția și contextul.

## Dovezi și statut epistemic

[[REF:REF.DECHENE.2010]] este MODEL_EVIDENCE pentru fenomenul de adevăr iluzoriu. Hasher și colaboratorii oferă fundalul istoric al cercetării privind familiaritatea. Studiile și meta-analizele ulterioare sunt BACKGROUND_THEORY și delimitează domeniul de generalizare; ele nu calibrează coeficienții M0.