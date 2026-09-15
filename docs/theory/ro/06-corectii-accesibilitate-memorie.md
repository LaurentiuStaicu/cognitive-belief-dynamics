# Corecții, accesibilitate și memorie

## Ideea centrală

O corecție poate reduce influența informației greșite fără să o „șteargă” din memorie. Literatura despre continued influence effect arată că informația retractată poate continua să afecteze raționamentul, iar eficiența corecției depinde în parte de cât de bine este integrată și recuperată informația corectivă.

[[VAR:C]] · [[VAR:B]] · [[MECH:correction]] · [[VAL:VAL.M0.002]] · [[CODE:m0.decay_correction]] · [[VIEW:runs:correction:5]]

## Ce spune cercetarea

Sinteza realizată de Ecker și colaboratorii în Nature Reviews Psychology sintetizează mecanismele propuse pentru rezistența dezinformării la corecție și diferențiază probleme de integrare, recuperare și coerență mentală. Meta-analizele citate în acea sinteză arată că fenomenul continued influence este robust, deși corecțiile sunt în general utile și pot reduce substanțial influența informației greșite.

O sinteză din 2024 dedicat memoriei subliniază că durabilitatea corecției poate scădea în timp și că amintirea sursei și a corecției contează. Aceasta susține ideea de accesibilitate dinamică, dar nu identifică ecuația CEM.

## Cum este implementat în M0

O corecție encodează accesibilitatea contextului corectiv prin:

C' = clamp01(C + alpha_c × (1 - C)).

Între evenimente, M0 folosește o scădere exponențială:

C(t + dt) = clamp01(C(t) × exp(-lambda_c × dt)).

Poți inspecta funcția de decădere în [[CODE:m0.decay_correction]]. În calculul convingerii, contribuția corecției este beta_correction × C × direction, unde direction poate fi negativă pentru o corecție care reduce susținerea afirmației sau pozitivă pentru un context corectiv care o susține.

Această reprezentare separă două lucruri: existența istorică a corecției și accesibilitatea ei curentă. O corecție poate fi „primită” în scenariu, dar influența ei asupra unei judecăți ulterioare poate scădea.

## De ce C nu este „memorie”

[[VAR:C]] nu este o măsură completă a memoriei episodice sau semantice. Nu are interferență, reconsolidare, surse multiple, indicii de recuperare ori reprezentări narative. Este o stare simplificată de accesibilitate a contextului corectiv, introdusă pentru a testa un tipar.

Această limită împiedică afirmații de tip „după X pași persoana uită corecția”. Pașii sunt abstracți, iar lambda_c este demonstrativ, nu o constantă psihologică estimată.

## Tiparul M0

[[VAL:VAL.M0.002]] urmărește două componente: corecția reduce convingerea în condiția de referință, iar o recuperare parțială a convingerii poate apărea pe măsură ce accesibilitatea corecției scade. [[VIEW:runs:correction:5]] arată traiectoria, nu o prognoză temporală reală.

## Ce nu afirmă acest capitol

Nu afirmă că o corecție repetă inevitabil mitul și îl întărește; literatura contemporană arată că astfel de efecte inverse sunt mult mai puțin generale decât se presupunea uneori. Nu afirmă nici că toate corecțiile funcționează egal. Credibilitatea sursei, formularea, explicația alternativă, momentul și atingerea audienței pot conta.

## Implicație pentru intervenții

În CEM, „context corectiv” este o intervenție demonstrativă asupra unei stări specifice. În lumea reală, o strategie de corectare trebuie evaluată și pentru acoperirea audienței, ușurința de înțelegere, sursă, repetare și persistență. Capitolul 12 separă aceste niveluri.