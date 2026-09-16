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

type Lang='ro'|'en';
type Mode='theory'|'mechanisms'|'tour';

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
 const mode=(parts[1] as Mode|undefined)??'theory';
 return {mode:['theory','mechanisms','tour'].includes(mode)?mode:'theory',detail:parts[2]};
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
 const mode:Mode=current.mode??(saved&&['theory','mechanisms','tour'].includes(saved)?saved:'theory');

 host.innerHTML=`<section class="understanding-shell">
  <div class="section-heading understanding-heading">
   <div><p class="eyebrow">${t('NIVELUL 1','LEVEL 1')}</p><h2>${t('Înțelegere','Understanding')}</h2><p>${t('Construiește mai întâi modelul mental al teoriei, apoi inspectează mecanismele executabile și parcurge aplicația ghidat.','Build the theoretical mental model first, then inspect executable mechanisms and follow the application with guidance.')}</p></div>
   <nav class="understanding-modes" aria-label="${t('Moduri de înțelegere','Understanding modes')}">
    <button type="button" data-understanding-mode="theory" aria-pressed="${mode==='theory'}">${t('Teorie','Theory')}</button>
    <button type="button" data-understanding-mode="mechanisms" aria-pressed="${mode==='mechanisms'}">${t('Mecanisme','Mechanisms')}</button>
    <button type="button" data-understanding-mode="tour" aria-pressed="${mode==='tour'}">${t('Tur ghidat','Guided tour')}</button>
   </nav>
  </div>
  <div id="understandingContent"></div>
 </section>`;

 const sub=host.querySelector<HTMLElement>('#understandingContent')!;
 host.querySelectorAll<HTMLButtonElement>('[data-understanding-mode]').forEach(button=>button.onclick=()=>{
  const next=button.dataset.understandingMode as Mode;
  localStorage.setItem('cem-understanding-mode',next);
  location.hash=`#understanding/${next}`;
 });

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

 mountGuidedTour(sub,lang,current.detail,navigate);
}
