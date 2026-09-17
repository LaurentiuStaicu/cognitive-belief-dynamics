import {mountLearning} from './learning';
import {type M1EditorialData,type EmpiricalTarget} from './editorial-stage';
import {type M1PresentationData} from './presentation-stage';
import {type M1AccessData} from './access-stage';
import {
 mountTheoryReader,type TheoryChapter,type TheoryGlossaryEntry,type TheoryVariable,
 type TheoryModule,type TheoryReference,type TheoryValidation
} from './theory-reader';
import {type NarrativeRun} from './narrative-stage';
import {mountGuidedTour} from './guided-tour';
import {mountActiveUnderstanding} from './active-understanding-ui';
import {mountSuiteOverview} from './suite-overview';
import './suite-overview.css';

type Lang='ro'|'en';
type Mode='overview'|'theory'|'mechanisms'|'tour'|'active';

export type UnderstandingTheoryData={
 chapters:TheoryChapter[];
 glossary:TheoryGlossaryEntry[];
 variables:TheoryVariable[];
 modules:TheoryModule[];
 references:TheoryReference[];
 validations:TheoryValidation[];
 releaseTag:string;
};

function route(){
 const raw=decodeURIComponent(location.hash.replace(/^#/,''));
 const parts=raw.split('/').filter(Boolean);
 if(parts[0]!=='understanding') return {mode:null as Mode|null,detail:undefined as string|undefined};
 const mode=(parts[1] as Mode|undefined)??'overview';
 return {mode:['overview','theory','mechanisms','tour','active'].includes(mode)?mode:'overview',detail:parts[2]};
}

export function mountUnderstanding(
 host:HTMLElement,
 lang:Lang,
 runs:NarrativeRun[],
 m1Editorial:M1EditorialData,
 m1Presentation:M1PresentationData,
 m1Access:M1AccessData,
 m1Targets:EmpiricalTarget[],
 theory:UnderstandingTheoryData,
 navigate:(target:string)=>void
){
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const current=route();
 const saved=localStorage.getItem('cem-understanding-mode') as Mode|null;
 const knownModes:Mode[]=['overview','theory','mechanisms','tour','active'];
 const mode:Mode=current.mode??(saved&&knownModes.includes(saved)?saved:'overview');
 const deepMode=mode!=='overview';

 host.innerHTML=`<section class="understanding-shell" data-understanding-mode-current="${mode}">
  ${deepMode?`<div class="section-heading understanding-heading">
   <div><p class="eyebrow">THEORY / LEARN</p><h2>${t('Aprofundare','Learn')}</h2><p>${t('Revino oricând la suprafața comună a modelului sau continuă cu teoria, mecanismele și exercițiile ghidate.','Return to the common model surface at any time, or continue with theory, mechanisms and guided learning.')}</p></div>
   <nav class="understanding-modes" aria-label="${t('Moduri de învățare','Learning modes')}">
    <button type="button" data-understanding-mode="overview" aria-pressed="false">${t('Model','Model')}</button>
    <button type="button" data-understanding-mode="theory" aria-pressed="${mode==='theory'}">${t('Teorie','Theory')}</button>
    <button type="button" data-understanding-mode="mechanisms" aria-pressed="${mode==='mechanisms'}">${t('Mecanisme','Mechanisms')}</button>
    <button type="button" data-understanding-mode="tour" aria-pressed="${mode==='tour'}">${t('Tur ghidat','Guided tour')}</button>
    <button type="button" data-understanding-mode="active" aria-pressed="${mode==='active'}">${t('Învățare activă','Active learning')}</button>
   </nav>
  </div>`:''}
  <div id="understandingContent"></div>
 </section>`;

 const sub=host.querySelector<HTMLElement>('#understandingContent')!;
 const openMode=(next:Mode)=>{
  localStorage.setItem('cem-understanding-mode',next);
  location.hash=next==='overview'?'#understanding/overview':`#understanding/${next}`;
 };
 host.querySelectorAll<HTMLButtonElement>('[data-understanding-mode]').forEach(button=>button.onclick=()=>openMode(button.dataset.understandingMode as Mode));

 if(mode==='overview'){
  mountSuiteOverview(sub,{
   lang,
   softwareVersion:theory.releaseTag.replace(/^v/,''),
   modelSpecification:'M1',
   variableCount:theory.variables.length,
   moduleCount:theory.modules.length,
   referenceCount:theory.references.length,
   validationCount:theory.validations.length,
   openUnderstanding:next=>openMode(next),
   openView:view=>navigate(view)
  });
  return;
 }

 if(mode==='theory'){
  mountTheoryReader(sub,{
   lang,
   chapters:theory.chapters,
   glossary:theory.glossary,
   variables:theory.variables,
   modules:theory.modules,
   references:theory.references,
   validations:theory.validations,
   releaseTag:theory.releaseTag,
   navigate
  },current.detail).catch(error=>{
   sub.innerHTML=`<div class="panel"><h3>${t('Teoria nu poate fi încărcată','Theory could not be loaded')}</h3><p>${String(error)}</p></div>`;
  });
  return;
 }

 if(mode==='mechanisms'){
  mountLearning(sub,lang,runs,m1Editorial,m1Presentation,m1Access,m1Targets,navigate);
  if(current.detail==='access'){
   const focusAccess=()=>{
    const stage=sub.querySelector<HTMLElement>('#m1AccessStage');
    stage?.scrollIntoView({block:'start'});
    stage?.focus({preventScroll:true});
   };
   requestAnimationFrame(()=>requestAnimationFrame(focusAccess));
  }else if(current.detail){
   requestAnimationFrame(()=>{
    sub.querySelector<HTMLButtonElement>(`[data-mechanism="${CSS.escape(current.detail!)}"]`)?.click();
   });
  }
  return;
 }

 if(mode==='active'){
  mountActiveUnderstanding(sub,lang,current.detail,theory.chapters,m1Access,navigate).catch(error=>{
   sub.innerHTML=`<div class="panel"><h3>${t('Modul activ nu poate fi încărcat','Active mode could not be loaded')}</h3><p>${String(error)}</p></div>`;
  });
  return;
 }

 mountGuidedTour(sub,lang,current.detail,navigate);
}
