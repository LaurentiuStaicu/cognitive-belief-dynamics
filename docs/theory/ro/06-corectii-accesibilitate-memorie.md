# Corecții, accesibilitate și memorie

## Ideea centrală

O corecție poate reduce influența informației greșite fără să o „șteargă” din memorie. Literatura despre continued influence effect arată că informația retractată poate continua să afecteze raționamentul, iar eficiența corecției depinde, printre altele, de cât de bine este integrată și cât de ușor poate fi recuperată informația corectivă.

[[VAR:C]] · [[VAR:B]] · [[MECH:correction]] · [[VAL:VAL.M0.002]] · [[CODE:m0.decay_correction]] · [[VIEW:runs:correction:5]]

## Ce spune cercetarea

Sinteza lui Ecker și colaboratorii din Nature Reviews Psychology trece în revistă mecanismele propuse pentru persistența influenței dezinformării după corectare și distinge între probleme de integrare, recuperare și coerență a reprezentării mentale. Literatura arată că fenomenul este robust, dar și că mesajele de corectare sunt, în general, utile și pot reduce substanțial influența informației greșite.

Cercetările asupra memoriei arată și că efectul corecțiilor poate scădea în timp și că recuperarea sursei și a informației corective contează. Aceste rezultate susțin ideea unei accesibilități dinamice, dar nu identifică ecuația folosită de CEM.

## Cum este implementat în M0

O corecție crește accesibilitatea contextului corectiv prin:

C' = clamp01(C + alpha_c × (1 - C)).

Între evenimente, M0 folosește o scădere exponențială:

C(t + dt) = clamp01(C(t) × exp(-lambda_c × dt)).

Funcția de scădere poate fi inspectată în [[CODE:m0.decay_correction]]. În calculul convingerii, contribuția corecției este beta_correction × C × direction, unde direction poate fi negativă pentru o corecție care reduce susținerea afirmației sau pozitivă pentru un context corectiv care o susține.

Reprezentarea separă două lucruri: faptul că o corecție a fost întâlnită și accesibilitatea ei în momentul unei judecăți ulterioare. O corecție poate fi prezentă în istoricul scenariului, dar influența ei poate scădea dacă informația devine mai puțin accesibilă.

## De ce C nu este „memorie”

[[VAR:C]] nu este o măsură completă a memoriei episodice sau semantice. Nu modelează interferența, reconsolidarea, surse multiple, indicii de recuperare ori reprezentări narative. Este o stare simplificată care descrie accesibilitatea contextului corectiv și a fost introdusă pentru testarea unui tipar precis.

Această limită împiedică afirmații de tipul „după X pași persoana uită corecția”. Pașii sunt abstracți, iar lambda_c este demonstrativ, nu o constantă psihologică estimată.

## Tiparul M0

[[VAL:VAL.M0.002]] urmărește două componente: corecția trebuie să reducă convingerea în condiția de referință, iar o revenire parțială a convingerii poate apărea pe măsură ce accesibilitatea corecției scade. [[VIEW:runs:correction:5]] arată această traiectorie, nu o prognoză temporală pentru o persoană reală.

## Ce nu afirmă acest capitol

Nu afirmă că repetarea unei informații false într-o corecție întărește inevitabil mitul; literatura contemporană arată că efectele de tip backfire sunt mult mai puțin generale decât se presupunea uneori. Nu afirmă nici că toate corecțiile funcționează la fel. Credibilitatea sursei, formularea, explicația alternativă, momentul și audiența la care ajunge mesajul pot conta.

## Implicație pentru intervenții

În CEM, „corrective context” este o intervenție demonstrativă asupra unei stări specifice. În lumea reală, o strategie de corectare trebuie evaluată și prin acoperirea audienței, claritatea mesajului, sursă, repetare și persistență. Capitolul 12 separă aceste niveluri.