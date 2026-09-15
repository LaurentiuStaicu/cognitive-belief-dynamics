# Algoritmi, ranking și feedback social

## Ideea centrală

Un algoritm de ranking poate influența ce informație este văzută, cât de des este văzută și în ce ordine, dar acesta este un alt nivel cauzal decât formarea directă a unei convingeri. CEM separă deliberat ranking → expunere de expunere → procesare → convingere → acțiune.

[[CONCEPT:algorithm-stage]] · [[VAR:Nexp]] · [[MECH:repetition]] · [[MODULE:MOD.18]] · [[VIEW:structure]]

## De ce „algoritmul m-a făcut să cred” este prea scurt

Sistemele de recomandare selectează și ordonează conținut pe baza unor obiective, semnale și constrângeri. Această selecție poate modifica distribuția expunerilor. Dar efectul asupra credințelor depinde apoi de conținut, atenție, cunoaștere anterioară, sursă, repetiție, congruență și context social.

Prin urmare, o săgeată directă algorithm → belief ar ascunde mai multe etape observabile. În CEM, viitorul mecanism de ranking trebuie să producă mai întâi o schimbare explicită în informația observată sau în [[VAR:Nexp]], după care mecanismele cognitive existente pot procesa acea intrare.

## Ce spune cercetarea platformelor

Dovezile experimentale nu susțin o singură poveste universală. Studiile Facebook/Instagram din 2023 au arătat că modificări mari ale feedului pot schimba expunerea și engagementul fără să producă efecte detectabile asupra polarizării ori multor atitudini politice în perioada studiată. Acest rezultat avertizează împotriva deducției automate de la „feed diferit” la „opinie diferită”.

În schimb, un experiment de teren publicat în Nature în 2026 pe platforma X, cu randomizare între feed algoritmic și cronologic timp de șapte săptămâni, a găsit că activarea feedului algoritmic a crescut engagementul și a deplasat unele atitudini politice în direcția conținutului promovat. Autorii au observat și modificări ale conturilor urmărite, oferind o cale intermediară plauzibilă. Efectele nu au fost însă universale: nu s-au găsit schimbări semnificative în partizanat sau polarizare afectivă.

Luate împreună, aceste rezultate susțin exact arhitectura etapizată: algoritmii pot schimba expunerea și uneori pot avea efecte downstream, dar magnitudinea și direcția depind de platformă, intervenție, populație și outcome.

## Feedbackul social ca buclă

Un utilizator vede conținut, reacționează, sistemul observă reacția și poate modifica selecția ulterioară. În paralel, reacțiile altor persoane pot deveni indicii sociale. Astfel apare o buclă:

ranking → exposure → action → platform signal → ranking.

O altă buclă posibilă este:

source/content exposure → familiarity or appraisal → action → social feedback → future exposure.

MOD.18 rezervă acest nivel în harta conceptuală, dar Alpha 0.4.1a1 nu execută încă un recommender system sau o rețea socială.

## Legătura cu repetarea

Dacă rankingul crește frecvența unui conținut, poate modifica [[VAR:Nexp]], iar mecanismul [[MECH:repetition]] poate apoi schimba familiaritatea. Acest lucru nu înseamnă că orice amplificare algoritmică produce adevăr iluzoriu: conținutul trebuie văzut, procesat și să se afle în domeniul în care efectul de repetiție este relevant.

## Ce nu afirmă acest capitol

Nu afirmă că algoritmii sunt neutri, dar nici că sunt cauza unică a polarizării. Nu extrapolează rezultatele de pe X la Facebook, TikTok sau orice altă platformă. Nu atribuie intenții politice unui algoritm doar din distribuția conținutului și nu tratează engagementul ca sinonim cu convingerea.

## Implicație pentru M1 viitor

[[CONCEPT:algorithm-stage]] rămâne CONCEPTUAL. Pentru a deveni executabil, trebuie să aibă o politică de ranking explicită, o intrare observabilă, un output de expunere, un nested null și un pattern diferențial care nu poate fi produs de modelul fără ranking.