# Surse, feedback și fiabilitate estimată

## Ideea centrală

Informația nu este evaluată independent de sursa ei. Oamenii pot folosi indicii despre expertiză, încredere și experiența anterioară pentru a decide câtă greutate să acorde unei afirmații. M0 reprezintă o versiune minimală a acestei idei: agentul menține o estimare a fiabilității sursei și o actualizează după feedback.

[[VAR:T]] · [[VAR:B]] · [[MECH:source]] · [[VAL:VAL.M0.003]] · [[CODE:m0.update_reliability]] · [[VIEW:runs:source:6]]

## Trei lucruri care trebuie separate

Prima este calitatea reală a sursei în mediul experimental. A doua este ceea ce agentul crede despre sursă. A treia este adevărul afirmației curente. În CEM, [[VAR:T]] reprezintă numai estimarea agentului despre fiabilitate. T nu este truth și nu este o reputație obiectivă universală.

Această distincție evită circularitatea: o sursă nu trebuie considerată „bună” doar pentru că agentul o crede, iar o afirmație nu devine adevărată doar pentru că vine de la o sursă evaluată pozitiv.

## Învățarea de referință

M0 folosește un delta rule simplu:

T' = clamp01(T + alpha_t × (outcome - T)),

unde outcome este 1 pentru feedback corect și 0 pentru feedback incorect în sarcina sintetică. [[CODE:m0.update_reliability]] arată implementarea.

Când un semnal de dovadă este integrat în convingere, M0 mapează T din intervalul [0,1] la o pondere a sursei în [-1,1] prin 2T - 1. Astfel, aceeași dovadă poate avea efect diferit în funcție de fiabilitatea estimată.

Aceasta este o alegere de modelare foarte simplă. Nu presupune că oamenii actualizează bayesian optim, că folosesc exact o rată alpha_t sau că încrederea este unidimensională.

## Ce arată literatura

Experimente asupra credibilității arată că sursele percepute ca mai credibile pot influența preluarea și menținerea convingerilor. Cercetări recente asupra actualizării în fața dezinformării găsesc că oamenii pot integra informația despre fiabilitatea sursei și își pot modifica evaluarea sursei după feedback contradictoriu.

Literatura distinge frecvent componente precum expertiza și trustworthiness. CEM le comprimă momentan într-o singură stare T doar pentru mecanismul de referință; această compresie este o limită, nu o afirmație ontologică.

## Feedbackul poate crea bucle

Dacă evaluarea sursei influențează interpretarea dovezii, iar rezultatul interpretat influențează ulterior evaluarea sursei, poate apărea o buclă de feedback. Cercetarea arată că astfel de dinamici pot fi sensibile la credibilitatea inițială. M0 nu modelează toate aceste bucle sociale, dar mecanismul de învățare al sursei este o bază pentru testarea lor ulterioară.

## Patternul M0

[[VAL:VAL.M0.003]] verifică dacă feedbackul despre sursă poate modifica T și dacă, apoi, dovezi comparabile primesc o greutate diferită. Deschide [[VIEW:runs:source:6]] pentru scenariul de referință.

## Ce nu afirmă acest capitol

Nu afirmă că încrederea într-o sursă este fixă, unidimensională sau independentă de identitate și context. Nu afirmă că „surse verificate” sunt infailibile. Nu folosește T ca adevăr și nu transformă reputația socială într-o proprietate intrinsecă a unei persoane sau instituții.

## Statut epistemic

Mecanismul este EXECUTABLE/CANDIDATE. Literatura oferă BACKGROUND_THEORY și fenomen-level support pentru rolul credibilității; ecuația delta și maparea 2T - 1 rămân REFERENCE_CANDIDATE până la calibrare și comparație cu alternative.