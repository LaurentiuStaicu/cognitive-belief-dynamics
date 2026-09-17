import './style.css';
import {evidenceSummary,interventions,mechanisms,productCopy,questions,relations,relationStatusLabels,secondaryFactors,sources,theorySections,t,type Language,type Mechanism,type MechanismId} from './content';

type View='explore'|'theory'|'interventions';
type State={language:Language;view:View;question:'repetition'|null;mechanism:MechanismId|null};

const app=document.querySelector<HTMLDivElement>('#app')!;
const savedLanguage=localStorage.getItem('cem.product.language');
const state:State={language:savedLanguage==='ro'?'ro':'en',view:'explore',question:null,mechanism:null};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!));
const txt=(value:{en:string;ro:string})=>esc(t(value,state.language));

function header():string{
 return `<a class="skip-link" href="#main">${state.language==='ro'?'Sari la conținut':'Skip to content'}</a>
 <header class="product-header">
  <div class="brand"><img src="./icon.svg" alt=""/><div><h1>${txt(productCopy.title)}</h1><p>${txt(productCopy.subtitle)}</p></div></div>
  <nav class="header-nav" aria-label="${state.language==='ro'?'Secțiuni':'Sections'}">
   <button type="button" data-view="explore" aria-pressed="${state.view==='explore'}">${state.language==='ro'?'Explorează':'Explore'}</button>
   <button type="button" data-view="theory" aria-pressed="${state.view==='theory'}">${txt(productCopy.theory)}</button>
   <button type="button" data-view="interventions" aria-pressed="${state.view==='interventions'}">${txt(productCopy.interventions)}</button>
  </nav>
  <div class="language-switch" role="group" aria-label="Language"><button type="button" data-lang="en" aria-pressed="${state.language==='en'}">EN</button><button type="button" data-lang="ro" aria-pressed="${state.language==='ro'}">RO</button></div>
 </header>`;
}

function questionPanel():string{
 return `<section class="panel question-panel" aria-labelledby="question-heading">
  <div class="section-heading"><div><p class="eyebrow">${txt(productCopy.choose)}</p><h2 id="question-heading">${state.language==='ro'?'De unde vrei să începi?':'Where do you want to start?'}</h2><p>${state.language==='ro'?'Prototipul validează mai întâi un singur traseu complet. Celelalte fenomene nu sunt conectate până când acest traseu nu trece auditul vizual și de utilitate.':'The prototype validates one complete pathway first. Other phenomena are not connected until this path passes the visual and usefulness audit.'}</p></div></div>
  <div class="question-grid">${questions.map(question=>question.enabled
   ?`<button type="button" class="question-card" data-enabled="true" data-question="${question.id}"><strong>${txt(question.label)}</strong><span>${txt(question.group)} · ${state.language==='ro'?'Explorează traseul':'Explore pathway'}</span></button>`
   :`<div class="question-card" data-enabled="false" aria-disabled="true"><strong>${txt(question.label)}</strong><span>${txt(question.group)}</span></div>`).join('')}</div>
 </section>`;
}

function edge(from:MechanismId,to:MechanismId,index:number):string{
 const relation=relations.find(item=>item.from===from&&item.to===to)!;
 const label=relationStatusLabels[relation.status];
 return `<div class="path-edge" aria-label="${esc(`${t(mechanisms[index].label,state.language)} → ${t(mechanisms[index+1].label,state.language)}: ${t(label,state.language)}`)}">
  <div class="edge-line" aria-hidden="true"></div>
  <span class="edge-status" data-status="${relation.status}">${txt(label)}</span>
  <button class="edge-help" type="button" title="${txt(relation.note)}" aria-label="${state.language==='ro'?'Explicația statutului legăturii':'Explain relation status'}">?</button>
 </div>`;
}

function pathway():string{
 if(!state.question)return '';
 const path=mechanisms.map((mechanism,index)=>{
  const node=`<button type="button" class="path-node" data-mechanism="${mechanism.id}"><span class="step">${String(index+1).padStart(2,'0')}</span><div><strong>${txt(mechanism.label)}</strong><p>${txt(mechanism.short)}</p></div><span class="open-hint">${state.language==='ro'?'Detalii + dovezi':'Details + evidence'} →</span></button>`;
  if(index===mechanisms.length-1)return node;
  return `${node}${edge(mechanism.id,mechanisms[index+1].id,index)}`;
 }).join('');
 return `<section class="pathway-section" aria-labelledby="pathway-heading">
  <div class="panel pathway-panel">
   <div class="section-heading"><div><p class="eyebrow">Pathway Explorer</p><h2 id="pathway-heading">${txt(productCopy.pathTitle)}</h2><p>${txt(productCopy.pathIntro)}</p></div><button class="secondary-button" type="button" data-view="theory">${state.language==='ro'?'Citește teoria':'Read theory'}</button></div>
   <div class="pathway-row" data-pathway="repetition">${path}</div>
   <div class="secondary" aria-label="${state.language==='ro'?'Factori secundari':'Secondary factors'}">${secondaryFactors.map(item=>`<details><summary>+ ${txt(item.label)}</summary><p>${txt(item.text)}</p></details>`).join('')}</div>
  </div>
 </section>`;
}

function insightStrip():string{
 if(!state.question)return '';
 const cards=[evidenceSummary.strongest,evidenceSummary.uncertainty,evidenceSummary.moderators,evidenceSummary.cannot];
 return `<section class="insight-section" aria-labelledby="insight-heading"><div class="panel"><div class="section-heading"><div><p class="eyebrow">${txt(productCopy.evidenceStrip)}</p><h2 id="insight-heading">${state.language==='ro'?'Dovezi, incertitudine și limite':'Evidence, uncertainty and limits'}</h2></div><button type="button" class="secondary-button" data-view="interventions">${txt(productCopy.interventions)}</button></div><div class="insight-grid">${cards.map(card=>`<article class="insight-card"><h3>${txt(card.title)}</h3><p>${txt(card.body)}</p></article>`).join('')}</div></div></section>`;
}

function exploreView():string{
 return `<div class="full-view" data-active="true" data-product-view="explore"><section class="hero"><p class="eyebrow">CEM · PRODUCT REBUILD PROTOTYPE</p><h2>${state.language==='ro'?'Cum poate informația ajunge să schimbe ceea ce credem și facem?':'How can information end up changing what we believe and do?'}</h2><p>${txt(productCopy.intro)}</p></section>${questionPanel()}${pathway()}${insightStrip()}</div>`;
}

function theoryView():string{
 return `<div class="full-view" data-active="true" data-product-view="theory"><section class="hero"><p class="eyebrow">${txt(productCopy.theory)}</p><h2>${state.language==='ro'?'Repetiție, familiaritate și adevăr perceput':'Repetition, familiarity and judged truth'}</h2><p>${state.language==='ro'?'Reader-ul public folosește limbaj natural și separă dovezile despre fenomen de alegerile modelului executabil.':'The public reader uses natural language and separates evidence about the phenomenon from executable-model choices.'}</p></section><div class="reader-shell"><aside class="panel reader-toc"><label class="eyebrow" for="theory-search">${state.language==='ro'?'Caută în capitol':'Search this chapter'}</label><input id="theory-search" type="search" placeholder="${state.language==='ro'?'ex. eterogenitate':'e.g. heterogeneity'}"/><nav>${theorySections.map((section,index)=>`<button type="button" data-theory-jump="theory-${index}">${txt(section.title)}</button>`).join('')}</nav><div class="drawer-actions"><button class="secondary-button" type="button" data-view="explore">${txt(productCopy.back)}</button></div></aside><article class="panel reader-article" id="theory-article"><h2>${state.language==='ro'?'Repetiție, familiaritate și adevăr perceput':'Repetition, familiarity and judged truth'}</h2><p>${state.language==='ro'?'Acest capitol recuperează teoria CEM relevantă pentru traseul prototip și o actualizează cu sinteza din 2026, fără identificatori de registry sau simboluri interne.':'This chapter recovers the CEM theory relevant to the prototype pathway and updates it with the 2026 synthesis, without registry identifiers or internal symbols.'}</p>${theorySections.map((section,index)=>`<section class="theory-section" id="theory-${index}" data-theory-section><h3>${txt(section.title)}</h3><p>${txt(section.body)}</p></section>`).join('')}<div class="citations"><h3>${state.language==='ro'?'Surse principale':'Key sources'}</h3>${sources.map(source=>`<a href="${esc(source.url)}" target="_blank" rel="noopener noreferrer">${esc(source.label)} ↗</a>`).join('')}</div></article></div></div>`;
}

function interventionsView():string{
 return `<div class="full-view" data-active="true" data-product-view="interventions"><section class="hero"><p class="eyebrow">${txt(productCopy.interventions)}</p><h2>${state.language==='ro'?'Ce intervenții au fost testate pe segmentele acestui traseu?':'Which interventions have been tested on parts of this pathway?'}</h2><p>${state.language==='ro'?'Acestea sunt rezultate din studii, nu recomandări normative ale CEM.':'These are findings from studies, not normative CEM recommendations.'}</p></section><section class="panel"><div class="intervention-grid">${interventions.map(item=>`<article class="intervention-card"><h3>${txt(item.label)}</h3><dl><div><dt>${state.language==='ro'?'Mecanism țintă':'Target mechanism'}</dt><dd>${txt(item.target)}</dd></div><div><dt>Evidence</dt><dd>${txt(item.evidence)}</dd></div><div><dt>Outcome</dt><dd>${txt(item.outcome)}</dd></div><div><dt>Effect</dt><dd>${txt(item.effect)}</dd></div><div><dt>${state.language==='ro'?'Populație / context':'Population / context'}</dt><dd>${txt(item.context)}</dd></div><div><dt>${state.language==='ro'?'Durabilitate':'Durability'}</dt><dd>${txt(item.duration)}</dd></div><div><dt>${state.language==='ro'?'Trade-offs / efecte nedorite':'Trade-offs / adverse effects'}</dt><dd>${txt(item.tradeoffs)}</dd></div></dl></article>`).join('')}</div><p class="nonprescriptive">${state.language==='ro'?'CEM nu selectează automat o intervenție „corectă”. Efectele depind de context, implementare, acoperire și outcome-ul măsurat.':'CEM does not automatically select a “correct” intervention. Effects depend on context, implementation, coverage and the measured outcome.'}</p><div class="drawer-actions"><button class="secondary-button" type="button" data-view="explore">${txt(productCopy.back)}</button><button class="secondary-button" type="button" data-view="theory">${txt(productCopy.theory)}</button></div></section></div>`;
}

function drawer():string{
 return `<div class="context-backdrop" data-open="false" id="context-backdrop"></div><aside class="context-drawer" data-open="false" id="context-drawer" aria-hidden="true" aria-label="${state.language==='ro'?'Detalii mecanism':'Mechanism details'}"></aside>`;
}

function mechanismDrawer(mechanism:Mechanism){
 const drawer=document.querySelector<HTMLElement>('#context-drawer')!;
 const backdrop=document.querySelector<HTMLElement>('#context-backdrop')!;
 drawer.innerHTML=`<div class="drawer-header"><div><p class="eyebrow">${state.language==='ro'?'Mecanism selectat':'Selected mechanism'}</p><h2>${txt(mechanism.label)}</h2></div><button type="button" class="drawer-close" data-close-drawer>${txt(productCopy.close)}</button></div><div class="drawer-body">
  <section class="detail-block"><h3>WHAT IS IT?</h3><p>${txt(mechanism.what)}</p></section>
  <section class="detail-block"><h3>WHY DOES IT MATTER?</h3><p>${txt(mechanism.why)}</p></section>
  <section class="detail-block"><h3>WHAT INFLUENCES IT?</h3><ul>${mechanism.influencedBy.map(item=>`<li>${txt(item)}</li>`).join('')}</ul></section>
  <section class="detail-block"><h3>WHAT DOES IT INFLUENCE?</h3><ul>${mechanism.influences.map(item=>`<li>${txt(item)}</li>`).join('')}</ul></section>
  <section class="detail-block"><h3>WHAT DOES THE EVIDENCE SAY?</h3><p>${txt(mechanism.evidence)}</p></section>
  ${mechanism.effect?`<section class="detail-block effect-callout"><h3>HOW LARGE IS THE EFFECT?</h3><p>${txt(mechanism.effect)}</p></section>`:''}
  <section class="detail-block"><h3>WHEN DOES IT CHANGE?</h3><p>${txt(mechanism.conditions)}</p></section>
  <section class="detail-block"><h3>WHAT ELSE COULD EXPLAIN IT?</h3><p>${txt(mechanism.competing)}</p></section>
  <section class="detail-block"><h3>WHAT ARE THE LIMITATIONS?</h3><p>${txt(mechanism.limitations)}</p></section>
  <section class="detail-block"><h3>INTERVENTIONS STUDIED</h3><p>${txt(mechanism.interventions)}</p></section>
  <div class="drawer-actions"><button type="button" class="primary-button" data-open-theory>${state.language==='ro'?'Citește teoria completă':'Read full theory'}</button><button type="button" class="secondary-button" data-open-interventions>${txt(productCopy.interventions)}</button></div>
 </div>`;
 drawer.dataset.open='true';drawer.setAttribute('aria-hidden','false');backdrop.dataset.open='true';
 const close=()=>{drawer.dataset.open='false';drawer.setAttribute('aria-hidden','true');backdrop.dataset.open='false';state.mechanism=null;};
 drawer.querySelector<HTMLButtonElement>('[data-close-drawer]')!.onclick=close;backdrop.onclick=close;
 drawer.querySelector<HTMLButtonElement>('[data-open-theory]')!.onclick=()=>{close();state.view='theory';render();};
 drawer.querySelector<HTMLButtonElement>('[data-open-interventions]')!.onclick=()=>{close();state.view='interventions';render();};
 drawer.querySelector<HTMLButtonElement>('[data-close-drawer]')!.focus();
}

function footer():string{
 return `<footer class="product-footer"><span>InfoClar Model Suite · CEM clean-slate product prototype</span><span>${state.language==='ro'?'Modelul științific și MOD.14 rămân neschimbate':'Scientific model and MOD.14 remain unchanged'}</span></footer>`;
}

function bind(){
 document.querySelectorAll<HTMLButtonElement>('[data-lang]').forEach(button=>button.onclick=()=>{state.language=button.dataset.lang as Language;localStorage.setItem('cem.product.language',state.language);render();});
 document.querySelectorAll<HTMLButtonElement>('[data-view]').forEach(button=>button.onclick=()=>{state.view=button.dataset.view as View;render();});
 document.querySelector<HTMLButtonElement>('[data-question="repetition"]')?.addEventListener('click',()=>{state.question='repetition';render();document.querySelector('#pathway-heading')?.scrollIntoView({block:'start',behavior:'smooth'});});
 document.querySelectorAll<HTMLButtonElement>('[data-mechanism]').forEach(button=>button.onclick=()=>{const mechanism=mechanisms.find(item=>item.id===button.dataset.mechanism)!;state.mechanism=mechanism.id;mechanismDrawer(mechanism);});
 document.querySelectorAll<HTMLButtonElement>('[data-theory-jump]').forEach(button=>button.onclick=()=>document.getElementById(button.dataset.theoryJump!)?.scrollIntoView({block:'start',behavior:'smooth'}));
 const search=document.querySelector<HTMLInputElement>('#theory-search');
 if(search)search.oninput=()=>{const query=search.value.trim().toLocaleLowerCase(state.language==='ro'?'ro-RO':'en-US');document.querySelectorAll<HTMLElement>('[data-theory-section]').forEach(section=>section.hidden=Boolean(query)&&!section.textContent!.toLocaleLowerCase(state.language==='ro'?'ro-RO':'en-US').includes(query));};
}

function render(){
 document.documentElement.lang=state.language;
 const view=state.view==='explore'?exploreView():state.view==='theory'?theoryView():interventionsView();
 app.innerHTML=`${header()}<main id="main" class="product-main" tabindex="-1">${view}${drawer()}${footer()}</main>`;
 bind();
}

render();
