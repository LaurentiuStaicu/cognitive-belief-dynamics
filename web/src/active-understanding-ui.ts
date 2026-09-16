import {
 LearningHistoryStore,
 createActiveSession,
 reduceActiveSession,
 type ActiveConfidence,
 type ActiveSession
} from './active-understanding';

type Lang='ro'|'en';
type Copy={ro:string;en:string};
type Choice={id:string;label:Copy};
type Challenge={
 id:'AU-1'|'AU-2'|'AU-3';
 family:string;
 prediction_format:string;
 learning_target:Copy;
 worked_example_refs:string[];
 prompt:Copy;
 choices:Choice[];
 correct_choice_id:string;
 canonical_target_refs:string[];
 canonical_relation_refs:string[];
 explanation:Copy;
 epistemic_boundary:Copy;
};
type Contract={
 schema_version:'1';
 history_schema_version:'1';
 history_storage_key:string;
 max_history_records:number;
 confidence_scale:ActiveConfidence[];
 challenges:Challenge[];
};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({
 '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
}[char]!));

function local(copy:Copy,lang:Lang){return copy[lang];}
function stageLabel(stage:ActiveSession['stage'],lang:Lang):string{
 const labels:Record<ActiveSession['stage'],Copy>={
  WORKED_EXAMPLE:{ro:'Exemplu ghidat',en:'Worked example'},
  PREDICT:{ro:'Predicție',en:'Prediction'},
  REVEAL:{ro:'Rezultat',en:'Reveal'},
  EXPLAIN:{ro:'Explicație',en:'Explanation'},
  BOUNDARY:{ro:'Limită epistemică',en:'Epistemic boundary'},
  COMPLETE:{ro:'Complet',en:'Complete'}
 };
 return local(labels[stage],lang);
}
function confidenceLabel(value:ActiveConfidence,lang:Lang):string{
 const labels:Record<ActiveConfidence,Copy>={
  low:{ro:'scăzută',en:'low'},medium:{ro:'medie',en:'medium'},high:{ro:'ridicată',en:'high'}
 };
 return local(labels[value],lang);
}

async function loadContract():Promise<Contract>{
 const response=await fetch('./model/active_understanding.json',{cache:'no-store'});
 if(!response.ok)throw new Error(`Active Understanding contract HTTP ${response.status}`);
 const contract=await response.json() as Contract;
 if(contract.schema_version!=='1'||!Array.isArray(contract.challenges))throw new Error('unsupported Active Understanding contract');
 return contract;
}

export async function mountActiveUnderstanding(
 host:HTMLElement,
 lang:Lang,
 requestedId:string|undefined,
 navigate:(target:string)=>void
):Promise<void>{
 const contract=await loadContract();
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const challenge=contract.challenges.find(item=>item.id===requestedId)??contract.challenges[0];
 let session=createActiveSession(challenge.id,challenge.correct_choice_id);
 let selectedChoice='';
 let selectedConfidence='';
 const history=new LearningHistoryStore(localStorage,{maxRecords:contract.max_history_records,storageKey:contract.history_storage_key});

 host.innerHTML=`<section class="active-understanding" aria-labelledby="activeUnderstandingTitle">
  <div class="active-understanding-intro">
   <div>
    <p class="eyebrow">${t('OA-5 · ÎNVĂȚARE ACTIVĂ','OA-5 · ACTIVE LEARNING')}</p>
    <h2 id="activeUnderstandingTitle">${t('Înțelegere activă','Active Understanding')}</h2>
    <p>${t('Fă o predicție înainte să vezi rezultatul, apoi compară, explică și verifică limita epistemică. Acest mod nu modifică modelul și nu ascunde rezultate în celelalte suprafețe ale aplicației.','Make a prediction before seeing the result, then compare, explain and inspect the epistemic boundary. This mode does not modify the model or hide results elsewhere in the application.')}</p>
   </div>
   <span class="active-mode-badge">${t('MOD EXPLICIT','EXPLICIT MODE')}</span>
  </div>
  <div class="active-understanding-layout">
   <nav class="panel active-challenges" aria-label="${t('Provocări de înțelegere','Understanding challenges')}">
    <p class="eyebrow">${t('PROVOCĂRI','CHALLENGES')}</p>
    <ol>${contract.challenges.map(item=>`<li><button type="button" data-au-challenge="${esc(item.id)}" aria-current="${item.id===challenge.id?'step':'false'}"><strong>${esc(item.id)}</strong><span>${esc(local(item.learning_target,lang))}</span></button></li>`).join('')}</ol>
   </nav>
   <div class="active-understanding-main">
    <article id="activeChallengeStage" class="panel active-stage" aria-live="polite"></article>
    <section id="activeHistory" class="panel active-history" aria-labelledby="activeHistoryTitle"></section>
   </div>
  </div>
 </section>`;

 const stage=host.querySelector<HTMLElement>('#activeChallengeStage')!;
 const historyHost=host.querySelector<HTMLElement>('#activeHistory')!;

 host.querySelectorAll<HTMLButtonElement>('[data-au-challenge]').forEach(button=>button.onclick=()=>{
  const id=button.dataset.auChallenge;
  if(id)location.hash=`#understanding/active/${encodeURIComponent(id)}`;
 });

 const renderHistory=()=>{
  const records=[...history.all()].reverse().slice(0,6);
  historyHost.innerHTML=`<div class="active-history-heading"><div><p class="eyebrow">${t('LOCAL · PE DISPOZITIV','LOCAL · ON DEVICE')}</p><h3 id="activeHistoryTitle">${t('Istoricul predicțiilor','Prediction history')}</h3></div>${records.length?`<button type="button" data-au-clear-history>${t('Șterge istoricul','Clear history')}</button>`:''}</div>
   <p class="note">${t('Se păstrează local doar categoria predicției, încrederea opțională, rezultatul categoric, țintele canonice și momentul. Fără note libere, cont sau telemetrie.','Only the prediction category, optional confidence, categorical outcome, canonical targets and timestamp are kept locally. No free-form notes, account identity or telemetry.')}</p>
   ${records.length?`<ol class="active-history-list">${records.map(record=>`<li><div><strong>${esc(record.challenge_id)}</strong><span>${record.outcome_category==='correct'?t('predicția coincide','prediction matches'):t('predicția diferă','prediction differs')}</span></div><code>${esc(record.prediction_category)}</code>${record.confidence?`<span>${t('încredere','confidence')}: ${esc(confidenceLabel(record.confidence,lang))}</span>`:''}<time datetime="${esc(record.timestamp)}">${esc(new Date(record.timestamp).toLocaleString(lang==='ro'?'ro-RO':'en-GB',{dateStyle:'short',timeStyle:'short'}))}</time></li>`).join('')}</ol>`:`<p class="active-history-empty">${t('Nicio predicție salvată încă. Poți parcurge provocările și fără a salva o predicție, folosind „Sari peste”.','No saved prediction yet. You can also continue without saving a prediction by using “Skip”.')}</p>`}`;
  historyHost.querySelector<HTMLButtonElement>('[data-au-clear-history]')?.addEventListener('click',()=>{history.clear();renderHistory();});
 };

 const focusStage=()=>{
  const heading=stage.querySelector<HTMLElement>('[data-au-stage-title]');
  heading?.focus({preventScroll:true});
 };

 const choiceLabel=(id:string)=>local(challenge.choices.find(item=>item.id===id)?.label??{ro:id,en:id},lang);

 const refsMarkup=()=>`<div class="active-canonical-refs"><strong>${t('Ancore canonice','Canonical anchors')}</strong><div>${challenge.canonical_target_refs.map(id=>`<button type="button" data-au-open-ref="${esc(id)}"><code>${esc(id)}</code></button>`).join('')}</div></div>`;

 const wireRefs=()=>{
  stage.querySelectorAll<HTMLButtonElement>('[data-au-open-ref]').forEach(button=>button.onclick=()=>{
   const id=button.dataset.auOpenRef;
   if(id)navigate('reference:'+id);
  });
 };

 const renderStage=()=>{
  stage.dataset.auStage=session.stage;
  const progress={WORKED_EXAMPLE:1,PREDICT:2,REVEAL:3,EXPLAIN:4,BOUNDARY:5,COMPLETE:6}[session.stage];
  const stageHeader=`<div class="active-stage-progress"><span>${t('Pas','Step')} ${progress} / 6</span><progress value="${progress}" max="6" aria-label="${t('Progresul secvenței active','Active sequence progress')}"></progress><span>${esc(stageLabel(session.stage,lang))}</span></div>`;

  if(session.stage==='WORKED_EXAMPLE'){
   stage.innerHTML=stageHeader+`<p class="eyebrow">${esc(challenge.id)} · ${esc(challenge.family)}</p><h3 data-au-stage-title tabindex="-1">${t('Ce vei verifica','What you will check')}</h3><p class="active-learning-target">${esc(local(challenge.learning_target,lang))}</p>
    <div class="active-worked-example"><strong>${t('Pornește de la obiectele deja existente în CEM','Start from objects already present in CEM')}</strong><div>${challenge.worked_example_refs.map(id=>`<code>${esc(id)}</code>`).join('')}</div></div>
    ${refsMarkup()}
    <div class="active-actions"><button type="button" class="primary" data-au-start>${t('Începe predicția','Start prediction')}</button></div>`;
   stage.querySelector<HTMLButtonElement>('[data-au-start]')!.onclick=()=>{session=reduceActiveSession(session,{type:'START_PREDICTION'});renderStage();focusStage();};
   wireRefs();return;
  }

  if(session.stage==='PREDICT'){
   stage.innerHTML=stageHeader+`<p class="eyebrow">${esc(challenge.id)} · ${t('PREDICȚIE ÎNAINTE DE REZULTAT','PREDICT BEFORE RESULT')}</p><h3 data-au-stage-title tabindex="-1">${esc(local(challenge.prompt,lang))}</h3>
    <form id="activePredictionForm">
     <fieldset class="active-choice-fieldset"><legend>${t('Alege o predicție','Choose a prediction')}</legend>${challenge.choices.map(choice=>`<label><input type="radio" name="auPrediction" value="${esc(choice.id)}"><span>${esc(local(choice.label,lang))}</span></label>`).join('')}</fieldset>
     <label class="active-confidence" for="activeConfidence">${t('Câtă încredere ai? (opțional)','How confident are you? (optional)')}<select id="activeConfidence"><option value="">${t('Nu declar','Not stated')}</option>${contract.confidence_scale.map(value=>`<option value="${value}">${esc(confidenceLabel(value,lang))}</option>`).join('')}</select></label>
     <p class="note">${t('Încrederea este autoevaluarea ta metacognitivă. Nu este un scor științific și nu influențează rezultatul modelului.','Confidence is your own metacognitive judgment. It is not a scientific score and does not influence the model result.')}</p>
     <div class="active-actions"><button type="submit" class="primary" data-au-submit disabled>${t('Fixează predicția și arată rezultatul','Lock prediction and reveal result')}</button><button type="button" data-au-skip>${t('Sari peste predicție','Skip prediction')}</button></div>
    </form>`;
   const form=stage.querySelector<HTMLFormElement>('#activePredictionForm')!;
   const submit=stage.querySelector<HTMLButtonElement>('[data-au-submit]')!;
   form.querySelectorAll<HTMLInputElement>('input[name="auPrediction"]').forEach(input=>input.onchange=()=>{selectedChoice=input.value;submit.disabled=false;});
   stage.querySelector<HTMLSelectElement>('#activeConfidence')!.onchange=event=>{selectedConfidence=(event.currentTarget as HTMLSelectElement).value;};
   form.onsubmit=event=>{
    event.preventDefault();if(!selectedChoice)return;
    const confidence=selectedConfidence as ActiveConfidence|'';
    session=reduceActiveSession(session,{type:'SUBMIT_PREDICTION',predictionCategory:selectedChoice,...(confidence?{confidence}:{})});
    history.record({
     challenge_id:challenge.id,
     canonical_target_refs:[...challenge.canonical_target_refs],
     prediction_category:selectedChoice,
     ...(confidence?{confidence}:{}),
     outcome_category:session.outcome!
    });
    renderHistory();renderStage();focusStage();
   };
   stage.querySelector<HTMLButtonElement>('[data-au-skip]')!.onclick=()=>{session=reduceActiveSession(session,{type:'SKIP_PREDICTION'});renderStage();focusStage();};
   return;
  }

  if(session.stage==='REVEAL'){
   const comparison=session.predictionCategory
    ?(session.outcome==='correct'
      ?t('Predicția ta coincide cu rezultatul canonic al acestei provocări.','Your prediction matches the canonical result for this challenge.')
      :t('Predicția ta diferă de rezultatul canonic. Diferența este informația de lucru pentru pasul următor.','Your prediction differs from the canonical result. The difference is the learning signal for the next step.'))
    :t('Ai ales să vezi rezultatul fără a salva o predicție.','You chose to reveal the result without saving a prediction.');
   stage.innerHTML=stageHeader+`<p class="eyebrow">${esc(challenge.id)} · ${t('REZULTAT CANONIC','CANONICAL RESULT')}</p><h3 data-au-stage-title tabindex="-1">${esc(choiceLabel(challenge.correct_choice_id))}</h3><p class="active-comparison" data-au-comparison="${session.outcome??'skipped'}">${esc(comparison)}</p>
    ${session.confidence?`<p class="note">${t('Încredere declarată','Stated confidence')}: <strong>${esc(confidenceLabel(session.confidence,lang))}</strong></p>`:''}
    ${refsMarkup()}<div class="active-actions"><button type="button" class="primary" data-au-explain>${t('De ce? Vezi explicația','Why? Show explanation')}</button></div>`;
   stage.querySelector<HTMLButtonElement>('[data-au-explain]')!.onclick=()=>{session=reduceActiveSession(session,{type:'SHOW_EXPLANATION'});renderStage();focusStage();};
   wireRefs();return;
  }

  if(session.stage==='EXPLAIN'){
   stage.innerHTML=stageHeader+`<p class="eyebrow">${esc(challenge.id)} · ${t('EXPLICAȚIE','EXPLANATION')}</p><h3 data-au-stage-title tabindex="-1">${t('Leagă predicția de mecanism','Connect the prediction to the mechanism')}</h3><p class="active-explanation">${esc(local(challenge.explanation,lang))}</p>
    ${refsMarkup()}<div class="active-actions"><button type="button" class="primary" data-au-boundary>${t('Verifică limita epistemică','Inspect epistemic boundary')}</button></div>`;
   stage.querySelector<HTMLButtonElement>('[data-au-boundary]')!.onclick=()=>{session=reduceActiveSession(session,{type:'SHOW_BOUNDARY'});renderStage();focusStage();};
   wireRefs();return;
  }

  if(session.stage==='BOUNDARY'){
   stage.innerHTML=stageHeader+`<p class="eyebrow">${esc(challenge.id)} · ${t('LIMITĂ EPISTEMICĂ','EPISTEMIC BOUNDARY')}</p><h3 data-au-stage-title tabindex="-1">${t('Ce nu demonstrează această provocare','What this challenge does not establish')}</h3><div class="boundary"><strong>${t('Limită','Boundary')}</strong><p>${esc(local(challenge.epistemic_boundary,lang))}</p></div>
    <div class="active-actions"><button type="button" class="primary" data-au-complete>${t('Încheie provocarea','Complete challenge')}</button></div>`;
   stage.querySelector<HTMLButtonElement>('[data-au-complete]')!.onclick=()=>{session=reduceActiveSession(session,{type:'COMPLETE'});renderStage();focusStage();};
   return;
  }

  const currentIndex=contract.challenges.findIndex(item=>item.id===challenge.id);
  const next=contract.challenges[(currentIndex+1)%contract.challenges.length];
  stage.innerHTML=stageHeader+`<p class="eyebrow">${esc(challenge.id)} · ${t('SECVENȚĂ COMPLETĂ','SEQUENCE COMPLETE')}</p><h3 data-au-stage-title tabindex="-1">${t('Ai parcurs predicție → rezultat → explicație → limită.','You completed prediction → result → explanation → boundary.')}</h3><p>${t('Poți repeta aceeași provocare sau poți trece la următoarea. Istoricul local este descriptiv și nu produce un profil psihologic.','You can repeat this challenge or move to the next one. Local history is descriptive and does not produce a psychological profile.')}</p>
   <div class="active-actions"><button type="button" data-au-repeat>${t('Repetă provocarea','Repeat challenge')}</button><button type="button" class="primary" data-au-next>${t('Următoarea provocare','Next challenge')}: ${esc(next.id)}</button></div>`;
  stage.querySelector<HTMLButtonElement>('[data-au-repeat]')!.onclick=()=>{session=reduceActiveSession(session,{type:'RESET'});selectedChoice='';selectedConfidence='';renderStage();focusStage();};
  stage.querySelector<HTMLButtonElement>('[data-au-next]')!.onclick=()=>{location.hash=`#understanding/active/${encodeURIComponent(next.id)}`;};
 };

 renderHistory();
 renderStage();
}
