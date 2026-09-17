import type {Language,Text} from './content';

type Chapter={id:string;order:number;label:Record<Language,string>;summary:Record<Language,string>;source_paths:Record<Language,string>;sources:{role:string;ref:string}[];what_it_does_not_claim:Record<Language,string>};
type Glossary={id:string;token:string;label:Record<Language,string>;short_definition:Record<Language,string>;what_it_is_not:Record<Language,string>;related_chapters:string[]};
type Variable={id:string;short_name:string;label:Record<Language,string>};
type Module={id:string;label:Record<Language,string>};
type Reference={id:string;citation:string;url:string;access_url?:string};
type Validation={id:string;name:string};

type Data={chapters:Chapter[];glossary:Glossary[];variables:Variable[];modules:Module[];references:Reference[];validations:Validation[]};

type Options={language:Language;initialSlug?:string;onBack:()=>void;onMechanism?:(slug:string)=>void};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!));
const safeUrl=(value:string)=>{try{const url=new URL(value);return url.protocol==='https:'?esc(value):'#';}catch{return '#';}};
const slug=(chapter:Chapter)=>chapter.source_paths.en.split('/').pop()!.replace(/\.md$/,'').replace(/^\d+-/,'');

async function load<T>(name:string):Promise<T>{const response=await fetch(`./model/${name}.json`);if(!response.ok)throw new Error(`${name}: HTTP ${response.status}`);return response.json();}
async function data():Promise<Data>{const [chapters,glossary,variables,modules,references,validations]=await Promise.all([load<Chapter[]>('theory_index'),load<Glossary[]>('theory_glossary'),load<Variable[]>('variables'),load<Module[]>('modules'),load<Reference[]>('references'),load<Validation[]>('validation_tests')]);return {chapters,glossary,variables,modules,references,validations};}

function naturalize(raw:string,language:Language,d:Data){
 const variable=new Map<string,string>();
 for(const item of d.variables){variable.set(item.id,item.label[language]||item.label.en);variable.set(item.short_name,item.label[language]||item.label.en);}
 const modules=new Map(d.modules.map(item=>[item.id,item.label[language]||item.label.en]));
 const glossary=new Map(d.glossary.map(item=>[item.token,item.label[language]||item.label.en]));
 const refs=new Map(d.references.map(item=>[item.id,item]));
 const validations=new Map(d.validations.map(item=>[item.id,item.name]));
 let text=raw.replace(/\[\[(VAR|MODULE|MECH|CONCEPT|VAL|REF|VIEW|CODE):([^\]]+)\]\]/g,(_,kind:string,value:string)=>{
  const key=value.trim();
  if(kind==='VAR')return variable.get(key)??(language==='ro'?'variabilă a mecanismului':'mechanism variable');
  if(kind==='MODULE')return modules.get(key)??(language==='ro'?'modul CEM':'CEM module');
  if(kind==='MECH'||kind==='CONCEPT')return glossary.get(key)??key.replace(/[-_]/g,' ');
  if(kind==='VAL')return validations.get(key)??(language==='ro'?'test de validare':'validation test');
  if(kind==='REF')return refs.get(key)?.citation??(language==='ro'?'sursă științifică':'scientific source');
  if(kind==='VIEW')return language==='ro'?'traseul relevant din aplicație':'the relevant pathway in the application';
  return language==='ro'?'detaliu tehnic disponibil în proveniența de cercetare':'technical detail available in research provenance';
 });
 for(const [key,value] of [...modules,...variable].sort((a,b)=>b[0].length-a[0].length)){
  if(key.length<2)continue;
  text=text.replace(new RegExp(`\\b${key.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}\\b`,'g'),value);
 }
 const short:Record<string,Text>={
  B:{en:'belief judgment',ro:'judecata de credință'},W:{en:'attention to accuracy',ro:'atenția la acuratețe'},F:{en:'familiarity',ro:'familiaritate'},C:{en:'corrective accessibility',ro:'accesibilitatea corecției'},T:{en:'estimated source reliability',ro:'fiabilitatea estimată a sursei'},LR:{en:'likelihood ratio',ro:'raport de verosimilitate'},Pprior:{en:'probabilistic prior',ro:'prior probabilistic'},Pwm:{en:'world-model probability',ro:'probabilitatea din world model'},Uwm:{en:'world-model uncertainty',ro:'incertitudinea world model-ului'},Aissue:{en:'issue appraisal',ro:'evaluarea problemei'},Sobs:{en:'observed information sample',ro:'eșantionul informațional observat'},Nexp:{en:'number of exposures',ro:'numărul expunerilor'},Paccess:{en:'access probability',ro:'probabilitatea de acces'},EngageIntent:{en:'engagement intention',ro:'intenția de engagement'}};
 for(const [key,value] of Object.entries(short))text=text.replace(new RegExp(`\\b${key}\\b`,'g'),value[language]);
 text=text.replace(/\bM0(?:\.[A-Za-z0-9._-]+)?\b/g,language==='ro'?'modelul executabil de referință':'the reference executable model');
 text=text.replace(/\bM1(?:\.[A-Za-z0-9._-]+)?\b/g,language==='ro'?'stratul de validare empirică':'the empirical validation layer');
 text=text.replace(/\bMOD\.[A-Za-z0-9._-]+\b/g,language==='ro'?'modul CEM':'CEM module');
 text=text.replace(/\b(?:ODD|REF|VAR|LINK|CODE|VAL)\.[A-Za-z0-9._-]+\b/g,language==='ro'?'înregistrare tehnică':'technical record');
 text=text.replace(/(?:docs|web|src|model|tests|scripts)\/[A-Za-z0-9_./-]+\.(?:md|ts|tsx|js|mjs|json|py|css)/g,language==='ro'?'resursă tehnică':'technical resource');
 return text;
}

function inline(value:string){
 let out=esc(value);
 out=out.replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/\*([^*]+)\*/g,'<em>$1</em>').replace(/`([^`]+)`/g,'<span class="theory-term">$1</span>');
 out=out.replace(/\[([^\]]+)\]\((https:\/\/[^)]+)\)/g,(_,label,url)=>`<a href="${safeUrl(url)}" target="_blank" rel="noopener noreferrer">${label} ↗</a>`);
 return out;
}

function markdown(raw:string,language:Language,d:Data){
 const clean=naturalize(raw,language,d);
 const lines=clean.split(/\r?\n/);
 let html='';let list=false;let skipCode=false;
 const closeList=()=>{if(list){html+='</ul>';list=false;}};
 for(const source of lines){
  const line=source.trim();
  if(line.startsWith('```')){skipCode=!skipCode;continue;}
  if(skipCode)continue;
  if(!line){closeList();continue;}
  if(/^[-+*]\s+/.test(line)){if(!list){html+='<ul>';list=true;}html+=`<li>${inline(line.replace(/^[-+*]\s+/,''))}</li>`;continue;}
  closeList();
  if(/^#{1,4}\s/.test(line)){const level=Math.min(4,line.match(/^#+/)![0].length);html+=`<h${level}>${inline(line.replace(/^#{1,4}\s+/,''))}</h${level}>`;continue;}
  if(/^>\s?/.test(line)){html+=`<blockquote>${inline(line.replace(/^>\s?/,''))}</blockquote>`;continue;}
  if(/^[A-Za-z][A-Za-z ]{0,25}'?\s*=/.test(line)||/^[A-Za-z][A-Za-z0-9_ ]{0,20}\s*[+×*]/.test(line)){html+=`<p class="technical-omission">${language==='ro'?'Forma matematică de implementare este păstrată în proveniența tehnică; aici este prezentată interpretarea conceptuală.':'The implementation equation is retained in technical provenance; the public reader presents its conceptual interpretation.'}</p>`;continue;}
  html+=`<p>${inline(line)}</p>`;
 }
 closeList();return html;
}

function chapterSources(chapter:Chapter,d:Data,language:Language){
 const refs=new Map(d.references.map(item=>[item.id,item]));
 const seen=new Set<string>();
 const items=chapter.sources.map(source=>{
  const ref=refs.get(source.ref);
  const label=ref?.citation??source.ref;
  const url=ref?.url??source.ref;
  if(!/^https:\/\//.test(url)||seen.has(url))return '';
  seen.add(url);return `<li><a href="${safeUrl(url)}" target="_blank" rel="noopener noreferrer">${esc(label)} ↗</a></li>`;
 }).filter(Boolean).join('');
 return items?`<section class="theory-sources"><h3>${language==='ro'?'Surse și lecturi':'Sources and further reading'}</h3><ul>${items}</ul></section>`:'';
}

export async function mountTheory(host:HTMLElement,options:Options){
 const d=await data();const language=options.language;const ordered=[...d.chapters].sort((a,b)=>a.order-b.order);
 let current=ordered.find(item=>slug(item)===options.initialSlug)??ordered[0];
 let mode:'chapters'|'glossary'='chapters';
 host.innerHTML=`<div class="theory-v2"><aside class="panel theory-v2-sidebar"><div class="theory-v2-toolbar"><button class="secondary-button" type="button" data-theory-back>${language==='ro'?'← Înapoi la pathway':'← Back to pathway'}</button><div class="theory-mode-switch"><button type="button" data-theory-mode="chapters" aria-pressed="true">${language==='ro'?'Capitole':'Chapters'}</button><button type="button" data-theory-mode="glossary" aria-pressed="false">${language==='ro'?'Glosar':'Glossary'}</button></div><label><span class="eyebrow">${language==='ro'?'Caută':'Search'}</span><input id="theory-v2-search" type="search" placeholder="${language==='ro'?'concept, mecanism, capitol':'concept, mechanism, chapter'}"/></label></div><nav id="theory-v2-nav" aria-label="${language==='ro'?'Cuprins teorie':'Theory contents'}"></nav></aside><article class="panel theory-v2-reader" id="theory-v2-reader" tabindex="-1" aria-live="polite"></article></div>`;
 const nav=host.querySelector<HTMLElement>('#theory-v2-nav')!;const reader=host.querySelector<HTMLElement>('#theory-v2-reader')!;const search=host.querySelector<HTMLInputElement>('#theory-v2-search')!;
 const renderNav=()=>{
  const q=search.value.trim().toLocaleLowerCase(language==='ro'?'ro-RO':'en-US');
  if(mode==='chapters'){
   const filtered=ordered.filter(item=>!q||`${naturalize(item.label[language],language,d)} ${naturalize(item.summary[language],language,d)}`.toLocaleLowerCase(language==='ro'?'ro-RO':'en-US').includes(q));
   nav.innerHTML=`<ol class="theory-v2-chapters">${filtered.map(item=>`<li><button type="button" data-theory-chapter="${esc(slug(item))}" aria-current="${item.id===current.id?'page':'false'}"><span>${String(item.order).padStart(2,'0')}</span><strong>${esc(naturalize(item.label[language],language,d))}</strong><small>${esc(naturalize(item.summary[language],language,d))}</small></button></li>`).join('')}</ol>`;
   nav.querySelectorAll<HTMLButtonElement>('[data-theory-chapter]').forEach(button=>button.onclick=()=>{current=ordered.find(item=>slug(item)===button.dataset.theoryChapter)!;void renderChapter();renderNav();});
  }else{
   const filtered=d.glossary.filter(item=>!q||`${naturalize(item.label[language],language,d)} ${naturalize(item.short_definition[language],language,d)}`.toLocaleLowerCase(language==='ro'?'ro-RO':'en-US').includes(q));
   nav.innerHTML=`<div class="theory-v2-glossary">${filtered.map(item=>`<button type="button" data-glossary="${esc(item.id)}"><strong>${esc(naturalize(item.label[language],language,d))}</strong><small>${esc(naturalize(item.short_definition[language],language,d))}</small></button>`).join('')}</div>`;
   nav.querySelectorAll<HTMLButtonElement>('[data-glossary]').forEach(button=>button.onclick=()=>{const item=d.glossary.find(entry=>entry.id===button.dataset.glossary)!;reader.innerHTML=`<p class="eyebrow">${language==='ro'?'GLOSAR':'GLOSSARY'}</p><h1>${esc(naturalize(item.label[language],language,d))}</h1><p class="lead">${esc(naturalize(item.short_definition[language],language,d))}</p><div class="boundary"><strong>${language==='ro'?'Ce nu înseamnă':'What it is not'}</strong><p>${esc(naturalize(item.what_it_is_not[language],language,d))}</p></div>`;reader.focus({preventScroll:false});});
  }
 };
 const renderChapter=async()=>{
  reader.setAttribute('aria-busy','true');reader.innerHTML=`<p class="loading">${language==='ro'?'Se încarcă teoria…':'Loading theory…'}</p>`;
  const file=current.source_paths[language].split('/').pop()!;
  const response=await fetch(`./theory/${language}/${file}`);if(!response.ok)throw new Error(`theory: HTTP ${response.status}`);
  const raw=await response.text();
  reader.innerHTML=`<p class="eyebrow">${language==='ro'?'TEORIE CEM':'CEM THEORY'} · ${String(current.order).padStart(2,'0')}</p><div class="theory-v2-article">${markdown(raw,language,d)}</div><div class="boundary"><strong>${language==='ro'?'Ce nu afirmă acest capitol':'What this chapter does not claim'}</strong><p>${esc(naturalize(current.what_it_does_not_claim[language],language,d))}</p></div>${chapterSources(current,d,language)}`;
  reader.setAttribute('aria-busy','false');reader.focus({preventScroll:false});
 };
 host.querySelector<HTMLButtonElement>('[data-theory-back]')!.onclick=options.onBack;
 host.querySelectorAll<HTMLButtonElement>('[data-theory-mode]').forEach(button=>button.onclick=()=>{mode=button.dataset.theoryMode as 'chapters'|'glossary';host.querySelectorAll<HTMLButtonElement>('[data-theory-mode]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));renderNav();});
 search.oninput=renderNav;renderNav();await renderChapter();
}
