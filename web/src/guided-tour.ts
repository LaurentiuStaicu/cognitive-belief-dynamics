type Lang='ro'|'en';

type Copy={ro:string;en:string};
type TourAction={kind:'hash'|'view';target:string;label:Copy};
type TourStep={
 slug:string;
 title:Copy;
 purpose:Copy;
 observe:Copy[];
 checkpoint:Copy;
 boundary:Copy;
 status:Copy;
 action:TourAction;
};

const steps:TourStep[]=[
 {
  slug:'orientation',
  title:{ro:'1. Începe cu întrebarea modelului',en:'1. Start with the model question'},
  purpose:{ro:'Înțelege ce încearcă CEM să explice și, la fel de important, ce nu pretinde că măsoară.',en:'Understand what CEM is trying to explain and, equally importantly, what it does not claim to measure.'},
  observe:[
   {ro:'Diferența dintre fenomen empiric, mecanism executabil, arhitectură conceptuală și interpretare.',en:'The distinction between empirical phenomenon, executable mechanism, conceptual architecture and interpretation.'},
   {ro:'Ordinea obiectivelor: mecanisme → compararea factorilor → planificarea intervențiilor.',en:'The goal order: mechanisms → factor comparison → intervention planning.'}
  ],
  checkpoint:{ro:'Poți spune de ce un coeficient demonstrativ nu este o estimare populațională?',en:'Can you explain why a demonstrative coefficient is not a population estimate?'},
  boundary:{ro:'CEM nu diagnostichează persoane și nu estimează prevalențe sau rezultate electorale.',en:'CEM does not diagnose individuals or estimate prevalence or election outcomes.'},
  status:{ro:'CONCEPTUAL + EXECUTABLE',en:'CONCEPTUAL + EXECUTABLE'},
  action:{kind:'hash',target:'#understanding/theory/what-is-cem',label:{ro:'Deschide capitolul 0',en:'Open chapter 0'}}
 },
 {
  slug:'causal-chain',
  title:{ro:'2. Separă lumea de informația observată',en:'2. Separate the world from observed information'},
  purpose:{ro:'Urmărește lanțul lume → informație disponibilă → selecție/prezentare → observație → reprezentare → judecată → acțiune.',en:'Trace world → available information → selection/presentation → observation → representation → judgment → action.'},
  observe:[
   {ro:'O schimbare în informația observată nu este încă o schimbare de convingere.',en:'A change in observed information is not yet a change in belief.'},
   {ro:'Selecția editorială, prezentarea și ordonarea algoritmică apar în etape cauzale diferite.',en:'Editorial selection, presentation and algorithmic ranking occupy different causal stages.'}
  ],
  checkpoint:{ro:'Poți identifica unde ar trebui introdus un mecanism nou fără a sări direct la convingere?',en:'Can you identify where a new mechanism belongs without jumping directly to belief?'},
  boundary:{ro:'CEM folosește predictive processing doar ca fundal; nu implementează predictive coding neuronal.',en:'CEM uses predictive processing as background only; it does not implement neural predictive coding.'},
  status:{ro:'CONCEPTUAL',en:'CONCEPTUAL'},
  action:{kind:'hash',target:'#understanding/theory/world-information-representation',label:{ro:'Deschide lanțul conceptual',en:'Open the causal chain'}}
 },
 {
  slug:'mechanism',
  title:{ro:'3. Urmărește un mecanism executabil',en:'3. Follow an executable mechanism'},
  purpose:{ro:'Folosește repetarea ca exemplu complet: expunerea modifică familiaritatea, iar familiaritatea poate contribui la judecata de adevăr.',en:'Use repetition as a complete example: exposure changes familiarity, and familiarity can contribute to judged truth.'},
  observe:[
   {ro:'Variabilele Nexp, F și B rămân distincte.',en:'Nexp, F and B remain distinct variables.'},
   {ro:'Forma saturantă este o alegere de modelare, nu ecuația demonstrată de meta-analiză.',en:'The saturating form is a modelling choice, not an equation established by the meta-analysis.'}
  ],
  checkpoint:{ro:'Poți explica de ce familiaritatea nu este adevăr și nici dovadă?',en:'Can you explain why familiarity is neither truth nor evidence?'},
  boundary:{ro:'Efectul de adevăr iluzoriu este eterogen și nu trebuie generalizat automat la opinii normative sau identitare.',en:'The illusory-truth effect is heterogeneous and should not be automatically generalized to normative or identity-laden opinions.'},
  status:{ro:'EMPIRICAL + EXECUTABLE',en:'EMPIRICAL + EXECUTABLE'},
  action:{kind:'hash',target:'#understanding/mechanisms/repetition',label:{ro:'Deschide mecanismul Repetiție',en:'Open the Repetition mechanism'}}
 },
 {
  slug:'state-equation',
  title:{ro:'4. Leagă variabila de ecuație și de cod',en:'4. Connect state, equation and code'},
  purpose:{ro:'Revino la capitolul de repetiție și inspectează F: definiția, domeniul, actualizarea și locul în calculul convingerii.',en:'Return to the repetition chapter and inspect F: its definition, range, update and role in belief computation.'},
  observe:[
   {ro:'F este o stare internă latentă; Nexp este numărul expunerilor.',en:'F is a latent internal state; Nexp is the exposure count.'},
   {ro:'Inspectorul leagă termenii din teorie de Registru și de implementarea canonică.',en:'The inspector connects theory terms to the Registry and canonical implementation.'}
  ],
  checkpoint:{ro:'Dacă ai schimba forma de actualizare a lui F, ce predicție ar trebui să rămână și ce ar trebui retestat?',en:'If you changed the F update form, which prediction should remain and what would need retesting?'},
  boundary:{ro:'Parametrii alpha_f și beta_f sunt valori de referință demonstrative, nu estimări psihologice calibrate.',en:'alpha_f and beta_f are demonstrative reference values, not calibrated psychological estimates.'},
  status:{ro:'EXECUTABLE · REFERENCE_CANDIDATE',en:'EXECUTABLE · REFERENCE_CANDIDATE'},
  action:{kind:'hash',target:'#understanding/theory/repetition-familiarity-truth',label:{ro:'Inspectează F în capitolul 5',en:'Inspect F in chapter 5'}}
 },
 {
  slug:'scenario',
  title:{ro:'5. Verifică mecanismul într-un scenariu',en:'5. Check the mechanism in a scenario'},
  purpose:{ro:'Deschide rularea de referință și urmărește traiectoria, nu doar rezultatul final.',en:'Open the reference run and inspect the trajectory, not only the final outcome.'},
  observe:[
   {ro:'Expunerile apar la pași expliciți, iar familiaritatea se modifică gradual.',en:'Exposures occur at explicit steps and familiarity changes gradually.'},
   {ro:'Convingerea și probabilitatea de distribuire sunt rezultate diferite.',en:'Belief and sharing probability are different outcomes.'}
  ],
  checkpoint:{ro:'Poți identifica starea intermediară care explică schimbarea rezultatului?',en:'Can you identify the intermediate state that explains the outcome change?'},
  boundary:{ro:'Pașii sunt unități sintetice; curba nu este o prognoză temporală pentru o populație reală.',en:'Steps are synthetic units; the curve is not a time forecast for a real population.'},
  status:{ro:'EXECUTABLE · PATTERN TEST',en:'EXECUTABLE · PATTERN TEST'},
  action:{kind:'view',target:'runs:repetition:4',label:{ro:'Deschide rularea Repetiție',en:'Open the Repetition run'}}
 },
 {
  slug:'information-environment',
  title:{ro:'6. Compară selecția cu prezentarea',en:'6. Compare selection with presentation'},
  purpose:{ro:'M1 separă două mecanisme care în lumea reală apar adesea împreună: ce informație este selectată și cum este formulată.',en:'M1 separates two mechanisms that often co-occur in the real world: which information is selected and how it is phrased.'},
  observe:[
   {ro:'M1.E1 ține setul factual fix și schimbă selecția editorială.',en:'M1.E1 keeps the factual set fixed and changes editorial selection.'},
   {ro:'M1.E2 ține semnificația semantică fixă și schimbă forma confirmare/infirmare.',en:'M1.E2 keeps semantic meaning fixed and changes confirmation/refutation form.'}
  ],
  checkpoint:{ro:'Poți spune ce trebuie păstrat invariant pentru a atribui un efect fiecărui mecanism?',en:'Can you state what must remain invariant to attribute an effect to each mechanism?'},
  boundary:{ro:'Nici selecția editorială, nici congruența locală nu sunt scoruri generale de ideologie, identitate sau bias al unei instituții.',en:'Neither editorial selection nor local congruence is a general score of ideology, identity or institutional bias.'},
  status:{ro:'EMPIRICAL + EXECUTABLE',en:'EMPIRICAL + EXECUTABLE'},
  action:{kind:'hash',target:'#understanding/mechanisms/editorial',label:{ro:'Deschide mecanismul editorial',en:'Open the editorial mechanism'}}
 },
 {
  slug:'evidence',
  title:{ro:'7. Verifică dovada și limita ei',en:'7. Inspect evidence and its limit'},
  purpose:{ro:'Folosește Registrul pentru a separa definiția variabilei, statutul mecanismului, sursa empirică și ceea ce sursa nu validează.',en:'Use the Registry to separate variable definition, mechanism status, empirical source and what that source does not validate.'},
  observe:[
   {ro:'MODEL_EVIDENCE nu înseamnă calibrarea automată a ecuației.',en:'MODEL_EVIDENCE does not mean automatic calibration of the equation.'},
   {ro:'BACKGROUND_THEORY poate justifica arhitectura fără a valida numeric mecanismul.',en:'BACKGROUND_THEORY can motivate architecture without numerically validating the mechanism.'}
  ],
  checkpoint:{ro:'Poți distinge „fenomen observat” de „formă funcțională estimată”?',en:'Can you distinguish an observed phenomenon from an estimated functional form?'},
  boundary:{ro:'Un CI verde dovedește integritatea tehnică definită de teste, nu adevărul teoriei.',en:'A green CI establishes the technical integrity defined by tests, not the truth of the theory.'},
  status:{ro:'EVIDENCE AUDIT',en:'EVIDENCE AUDIT'},
  action:{kind:'view',target:'reference:VAR.FAMILIARITY.CLAIM',label:{ro:'Deschide F în Registru',en:'Open F in the Registry'}}
 },
 {
  slug:'validation',
  title:{ro:'8. Întreabă ce ar respinge mecanismul',en:'8. Ask what would reject the mechanism'},
  purpose:{ro:'În Visual ODD și capitolul de validare, urmărește modelele nule, testele diferențiale, identificabilitatea și proveniența.',en:'In Visual ODD and the validation chapter, inspect null models, differential tests, identifiability and provenance.'},
  observe:[
   {ro:'Un mecanism nou trebuie să producă o predicție pe care modelul mai simplu nu o reproduce trivial.',en:'A new mechanism should produce a prediction that the simpler model cannot reproduce trivially.'},
   {ro:'Reproducerea unui tipar nu demonstrează unicitatea mecanismului.',en:'Reproducing a pattern does not establish that the mechanism is unique.'}
  ],
  checkpoint:{ro:'Ce rezultat negativ te-ar face să elimini sau să simplifici o componentă?',en:'Which negative result would make you remove or simplify a component?'},
  boundary:{ro:'Sensibilitatea locală și identificabilitatea practică nu înlocuiesc validarea externă și calibrarea.',en:'Local sensitivity and practical identifiability do not replace external validation and calibration.'},
  status:{ro:'VALIDATION',en:'VALIDATION'},
  action:{kind:'view',target:'process',label:{ro:'Deschide Visual ODD',en:'Open Visual ODD'}}
 },
 {
  slug:'planning',
  title:{ro:'9. Planifică numai după ce ai înțeles mecanismele',en:'9. Plan only after understanding mechanisms'},
  purpose:{ro:'Planificatorul compară combinații în modelul demonstrativ. Folosește-l pentru dependențe și compromisuri, nu pentru recomandări directe de politică.',en:'The planner compares bundles inside the demonstrative model. Use it to inspect dependencies and trade-offs, not as a direct policy recommender.'},
  observe:[
   {ro:'Clasamentul depinde de obiectiv, buget, momentul activării și ipoteza de răspuns.',en:'Ranking depends on objective, budget, activation time and response assumption.'},
   {ro:'Contribuțiile factorilor sunt condiționate de celelalte măsuri și pot fi neaditive.',en:'Factor contributions are conditional on other measures and can be non-additive.'}
  ],
  checkpoint:{ro:'Se schimbă alegerea când modifici ipoteza sau costurile? Dacă da, ce spune asta despre robustețe?',en:'Does the choice change when assumptions or costs change? If so, what does that imply about robustness?'},
  boundary:{ro:'„Cea mai bună combinație” înseamnă doar cea mai bună dintre opțiunile simulate sub ipotezele selectate.',en:'“Best bundle” means only the best among simulated options under the selected assumptions.'},
  status:{ro:'EXPLORATORY',en:'EXPLORATORY'},
  action:{kind:'view',target:'planning',label:{ro:'Deschide Planificatorul',en:'Open the Planner'}}
 },
 {
  slug:'finish',
  title:{ro:'10. Încheie prin a verifica harta și limitele',en:'10. Finish by checking the map and its limits'},
  purpose:{ro:'Reunește traseul: înțelegere → mecanism → dovadă → test → comparație → planificare.',en:'Reconnect the journey: understanding → mechanism → evidence → test → comparison → planning.'},
  observe:[
   {ro:'Întreabă permanent dacă privești un fapt empiric, o implementare, o ipoteză conceptuală sau o interpretare.',en:'Keep asking whether you are looking at an empirical fact, an implementation, a conceptual hypothesis or an interpretation.'},
   {ro:'Revino la teorie sau Registru ori de câte ori statutul unei afirmații nu este clar.',en:'Return to Theory or the Registry whenever a claim status is unclear.'}
  ],
  checkpoint:{ro:'Poți explica traseul unui rezultat din interfață până la variabilă, ecuație, sursă și limită?',en:'Can you trace an interface result back to its variable, equation, source and limitation?'},
  boundary:{ro:'Modelul este o hartă pentru explicare și testare; nu este teritoriul social însuși.',en:'The model is a map for explanation and testing; it is not the social territory itself.'},
  status:{ro:'TOUR COMPLETE',en:'TOUR COMPLETE'},
  action:{kind:'hash',target:'#understanding/theory/using-cem',label:{ro:'Deschide capitolul final',en:'Open the final chapter'}}
 }
];

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({
 '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
}[char]!));

export function mountGuidedTour(
 host:HTMLElement,
 lang:Lang,
 requestedSlug:string|undefined,
 navigate:(target:string)=>void
){
 const t=(copy:Copy)=>copy[lang];
 let current=steps.find(step=>step.slug===requestedSlug)??steps[0];
 let storedVisited:string[]=[];
 try{storedVisited=JSON.parse(localStorage.getItem('cem-guided-tour-visited')??'[]');}catch{storedVisited=[];}
 const visited=new Set<string>(Array.isArray(storedVisited)?storedVisited:[]);
 visited.add(current.slug);

 const persist=()=>{
  localStorage.setItem('cem-guided-tour-visited',JSON.stringify([...visited]));
  localStorage.setItem('cem-guided-tour-step',current.slug);
 };

 const render=()=>{
  persist();
  const index=steps.indexOf(current);
  const progress=Math.round(((index+1)/steps.length)*100);
  host.innerHTML=`<div class="guided-tour-layout">
   <nav class="panel guided-tour-steps" aria-label="${lang==='ro'?'Pașii turului ghidat':'Guided tour steps'}">
    <p class="eyebrow">${lang==='ro'?'TRASEU':'JOURNEY'}</p>
    <ol>${steps.map((step,i)=>`<li><button type="button" data-tour-step="${esc(step.slug)}" aria-current="${step.slug===current.slug?'step':'false'}"><span>${String(i+1).padStart(2,'0')}</span><span>${esc(t(step.title).replace(/^\d+\.\s*/,''))}</span>${visited.has(step.slug)?'<span class="tour-visited" aria-label="'+(lang==='ro'?'vizitat':'visited')+'">✓</span>':''}</button></li>`).join('')}</ol>
   </nav>
   <section class="panel guided-tour-stage" aria-labelledby="guidedTourTitle">
    <div class="tour-progress"><span>${lang==='ro'?'Pas':'Step'} ${index+1} / ${steps.length}</span><progress value="${index+1}" max="${steps.length}" aria-label="${lang==='ro'?'Progresul turului':'Tour progress'}"></progress><span>${progress}%</span></div>
    <p class="eyebrow">${esc(t(current.status))}</p>
    <h2 id="guidedTourTitle" tabindex="-1">${esc(t(current.title))}</h2>
    <p class="tour-purpose">${esc(t(current.purpose))}</p>
    <div class="tour-observe"><h3>${lang==='ro'?'Ce să urmărești':'What to look for'}</h3><ul>${current.observe.map(item=>`<li>${esc(t(item))}</li>`).join('')}</ul></div>
    <div class="tour-checkpoint"><h3>${lang==='ro'?'Întrebarea de control':'Checkpoint question'}</h3><p>${esc(t(current.checkpoint))}</p></div>
    <div class="boundary"><strong>${lang==='ro'?'Limită epistemică':'Epistemic boundary'}</strong><p>${esc(t(current.boundary))}</p></div>
    <div class="tour-actions">
     <button type="button" class="tour-open" data-tour-open>${esc(t(current.action.label))}</button>
     <div class="tour-pagination">
      <button type="button" data-tour-prev ${index===0?'disabled':''}>← ${lang==='ro'?'Înapoi':'Back'}</button>
      <button type="button" data-tour-next ${index===steps.length-1?'disabled':''}>${lang==='ro'?'Următorul':'Next'} →</button>
     </div>
    </div>
    <p class="note">${lang==='ro'?'Când deschizi o suprafață a aplicației, butonul Back al browserului te readuce la acest pas.':'When you open an application surface, the browser Back button returns you to this step.'}</p>
   </section>
  </div>`;

  host.querySelectorAll<HTMLButtonElement>('[data-tour-step]').forEach(button=>button.onclick=()=>{
   location.hash=`#understanding/tour/${encodeURIComponent(button.dataset.tourStep!)}`;
  });
  host.querySelector<HTMLButtonElement>('[data-tour-prev]')!.onclick=()=>{
   if(index>0) location.hash=`#understanding/tour/${encodeURIComponent(steps[index-1].slug)}`;
  };
  host.querySelector<HTMLButtonElement>('[data-tour-next]')!.onclick=()=>{
   if(index<steps.length-1) location.hash=`#understanding/tour/${encodeURIComponent(steps[index+1].slug)}`;
  };
  host.querySelector<HTMLButtonElement>('[data-tour-open]')!.onclick=()=>{
   visited.add(current.slug);persist();
   if(current.action.kind==='hash') location.hash=current.action.target;
   else navigate(current.action.target);
  };
  requestAnimationFrame(()=>host.querySelector<HTMLElement>('#guidedTourTitle')?.focus({preventScroll:true}));
 };

 render();
}

export const guidedTourStepCount=steps.length;
