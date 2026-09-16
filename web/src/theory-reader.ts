import {semanticEntity,semanticLabel} from './semantic';
type Lang='ro'|'en';

export type TheoryChapter={
 id:string;
 order:number;
 label:Record<Lang,string>;
 summary:Record<Lang,string>;
 source_paths:Record<Lang,string>;
 prerequisites:string[];
 epistemic_status:string[];
 module_ids:string[];
 variable_ids:string[];
 mechanism_ids:string[];
 validation_ids:string[];
 evidence_refs:string[];
 sources:{role:string;ref:string}[];
 code_refs:{id:string;path:string;symbol:string;language:string;release_pin_required:boolean}[];
 related_views:string[];
 anchors:string[];
 what_it_does_not_claim:Record<Lang,string>;
};

export type TheoryGlossaryEntry={
 id:string;
 kind:'MECHANISM'|'CONCEPT';
 token:string;
 label:Record<Lang,string>;
 short_definition:Record<Lang,string>;
 what_it_is_not:Record<Lang,string>;
 epistemic_status:string[];
 executable:boolean;
 target:string;
 related_chapters:string[];
};

export type TheoryVariable={
 id:string;
 short_name:string;
 label:Record<Lang,string>;
 definition:string;
 what_it_is_not:string;
 conceptual_module:string;
 ontology_type:string;
 range?:number[];
};

export type TheoryModule={id:string;label:Record<Lang,string>};
export type TheoryReference={id:string;citation:string;url:string;access_url:string;checked_on:string;review_scope:string};
export type TheoryValidation={id:string;name:string;pattern:string;claim_scope:string};

type Context={
 lang:Lang;
 chapters:TheoryChapter[];
 glossary:TheoryGlossaryEntry[];
 variables:TheoryVariable[];
 modules:TheoryModule[];
 references:TheoryReference[];
 validations:TheoryValidation[];
 releaseTag:string;
 navigate:(target:string)=>void;
};

const tokenRe=/\[\[(VAR|MODULE|MECH|VAL|REF|VIEW|CODE|CONCEPT):([^\]]+)\]\]/g;

const sem=(id:string,lang:Lang,fallback:string)=>semanticLabel(id,lang,fallback);

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({
 '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'
}[char]!));

export function theoryChapterSlug(chapter:TheoryChapter){
 const name=chapter.source_paths.en.split('/').pop()!.replace(/\.md$/,'');
 return name.replace(/^\d+-/,'');
}

function statusLabel(status:string,lang:Lang){
 const labels:Record<string,[string,string]>={
  EMPIRICAL:['Empiric','Empirical'],
  EXECUTABLE:['Executabil','Executable'],
  CONCEPTUAL:['Conceptual','Conceptual'],
  INTERPRETIVE:['Interpretativ','Interpretive']
 };
 const pair=labels[status]??[status,status];
 return lang==='ro'?pair[0]:pair[1];
}

function codeRefs(ctx:Context){
 return new Map(ctx.chapters.flatMap(ch=>ch.code_refs).map(ref=>[ref.id,ref]));
}

function displayToken(kind:string,value:string,ctx:Context){
 if(kind==='VAR'){
  const item=ctx.variables.find(v=>v.id===value||v.short_name===value);
  return semanticEntity(item?.id??value)?.short_name??item?.short_name??value;
 }
 if(kind==='MODULE'){const item=ctx.modules.find(m=>m.id===value);return item?sem(item.id,ctx.lang,item.label[ctx.lang]):value;}
 if(kind==='MECH'||kind==='CONCEPT'){const item=ctx.glossary.find(g=>g.token===value);return item?sem(item.id,ctx.lang,item.label[ctx.lang]):value;}
 if(kind==='VAL'){const item=ctx.validations.find(v=>v.id===value);return item?sem(item.id,ctx.lang,item.name):value;}
 if(kind==='CODE') return codeRefs(ctx).get(value)?.symbol??value;
 if(kind==='VIEW'){
  const first=value.split(':')[0];
  const labels:Record<string,[string,string]>={
   learning:['Înțelegere','Understanding'],planning:['Priorități și acțiuni','Priorities and actions'],
   structure:['Hartă','Graph'],runs:['Scenarii','Scenarios'],comparison:['Comparații','Comparisons'],
   process:['Visual ODD','Visual ODD'],reference:['Registru','Registry']
  };
  const pair=labels[first]??[value,value];
  return ctx.lang==='ro'?pair[0]:pair[1];
 }
 return value;
}

function renderInline(text:string,ctx:Context){
 let html='';
 let last=0;
 for(const match of text.matchAll(tokenRe)){
  const index=match.index??0;
  html+=esc(text.slice(last,index));
  const kind=match[1],value=match[2].trim();
  html+=`<button type="button" class="theory-token" data-theory-token-kind="${esc(kind)}" data-theory-token-value="${esc(value)}">${esc(displayToken(kind,value,ctx))}</button>`;
  last=index+match[0].length;
 }
 html+=esc(text.slice(last));
 return html.replace(/\`([^\`]+)\`/g,'<code>$1</code>');
}

function renderMarkdown(source:string,ctx:Context){
 const lines=source.replace(/\r\n/g,'\n').split('\n');
 const out:string[]=[];
 let listType:''|'ul'|'ol'='';
 const closeList=()=>{if(listType){out.push(`</${listType}>`);listType='';}};
 for(const raw of lines){
  const line=raw.trim();
  if(!line){closeList();continue;}
  const heading=line.match(/^(#{1,4})\s+(.+)$/);
  if(heading){
   closeList();
   const level=Math.min(5,heading[1].length+1);
   out.push(`<h${level}>${renderInline(heading[2],ctx)}</h${level}>`);
   continue;
  }
  if(line.startsWith('> ')){
   closeList();
   out.push(`<blockquote>${renderInline(line.slice(2),ctx)}</blockquote>`);
   continue;
  }
  const unordered=line.match(/^[-*]\s+(.+)$/);
  const ordered=line.match(/^\d+\.\s+(.+)$/);
  if(unordered||ordered){
   const wanted=unordered?'ul':'ol';
   if(listType!==wanted){closeList();listType=wanted;out.push(`<${wanted}>`);}
   out.push(`<li>${renderInline((unordered??ordered)![1],ctx)}</li>`);
   continue;
  }
  closeList();
  out.push(`<p>${renderInline(line,ctx)}</p>`);
 }
 closeList();
 return out.join('');
}

function chapterSources(chapter:TheoryChapter,ctx:Context){
 const t=(ro:string,en:string)=>ctx.lang==='ro'?ro:en;
 if(!chapter.sources.length) return '';
 const roleLabel=(role:string)=>{
  const labels:Record<string,[string,string]>={
   MODEL_EVIDENCE:['Dovadă a modelului','Model evidence'],
   BACKGROUND_THEORY:['Teorie de fundal','Background theory'],
   INTERPRETIVE_SOURCE:['Sursă interpretativă','Interpretive source']
  };
  const pair=labels[role]??[role,role];
  return ctx.lang==='ro'?pair[0]:pair[1];
 };
 const items=chapter.sources.map(source=>{
  const value=esc(source.ref);
  const rendered=/^https?:\/\//.test(source.ref)
   ? '<a href="'+value+'" target="_blank" rel="noopener">'+value+' ↗</a>'
   : '<code>'+value+'</code>';
  return '<li><strong>'+esc(roleLabel(source.role))+'</strong> '+rendered+'</li>';
 }).join('');
 return '<div class="theory-sources"><strong>'+t('Surse ale capitolului','Chapter sources')+'</strong><ul>'+items+'</ul></div>';
}

function inspectorDefault(chapter:TheoryChapter,ctx:Context){
 const t=(ro:string,en:string)=>ctx.lang==='ro'?ro:en;
 return `<p class="eyebrow">${t('CAPITOL ACTIV','ACTIVE CHAPTER')}</p>
 <h2>${esc(sem(chapter.id,ctx.lang,chapter.label[ctx.lang]))}</h2>
 <p>${esc(chapter.summary[ctx.lang])}</p>
 <div class="theory-statuses">${chapter.epistemic_status.map(status=>`<span data-status="${esc(status)}">${esc(statusLabel(status,ctx.lang))}</span>`).join('')}</div>
 ${chapterSources(chapter,ctx)}
 <div class="boundary"><strong>${t('Ce nu afirmă','What it does not claim')}</strong><p>${esc(chapter.what_it_does_not_claim[ctx.lang])}</p></div>
 <p class="note">${t('Selectează un termen din text pentru definiție, statut, dovadă și legătura către aplicație sau cod.','Select a term in the text for its definition, status, evidence and link to the application or code.')}</p>`;
}

function inspectorFor(kind:string,value:string,chapter:TheoryChapter,ctx:Context){
 const t=(ro:string,en:string)=>ctx.lang==='ro'?ro:en;
 if(kind==='VAR'){
  const item=ctx.variables.find(v=>v.id===value||v.short_name===value);
  if(!item) return inspectorDefault(chapter,ctx);
  const range=item.range?item.range.join(' … '):t('nedeclarat','not declared');
  return `<p class="eyebrow">VAR · ${esc(item.ontology_type)}</p><h2><code>${esc(item.short_name)}</code> ${esc(sem(item.id,ctx.lang,item.label[ctx.lang]))}</h2>
  <p>${esc(item.definition)}</p><dl class="theory-meta"><dt>${t('Domeniu','Range')}</dt><dd>${esc(range)}</dd><dt>${t('Modul','Module')}</dt><dd>${esc(item.conceptual_module)}</dd></dl>
  <div class="boundary"><strong>${t('Nu reprezintă','What it is not')}</strong><p>${esc(item.what_it_is_not)}</p></div>
  <button type="button" data-theory-open-view="reference:${esc(item.id)}">${t('Deschide în Registru','Open in Registry')}</button>`;
 }
 if(kind==='MODULE'){
  const item=ctx.modules.find(m=>m.id===value);
  return item?`<p class="eyebrow">${esc(item.id)}</p><h2>${esc(sem(item.id,ctx.lang,item.label[ctx.lang]))}</h2><p class="note">${t('Modul conceptual. Deschide Visual ODD pentru a vedea ce părți sunt executabile și ce părți rămân arhitecturale.','Conceptual module. Open Visual ODD to see which parts are executable and which remain architectural.')}</p><button type="button" data-theory-open-view="process">${t('Deschide Visual ODD','Open Visual ODD')}</button>`:inspectorDefault(chapter,ctx);
 }
 if(kind==='MECH'||kind==='CONCEPT'){
  const glossaryKind=kind==='MECH'?'MECHANISM':'CONCEPT';
  const item=ctx.glossary.find(g=>g.token===value&&g.kind===glossaryKind);
  if(!item) return inspectorDefault(chapter,ctx);
  return `<p class="eyebrow">${kind}</p><h2>${esc(sem(item.id,ctx.lang,item.label[ctx.lang]))}</h2><p>${esc(item.short_definition[ctx.lang])}</p>
  <div class="theory-statuses">${item.epistemic_status.map(status=>`<span data-status="${esc(status)}">${esc(statusLabel(status,ctx.lang))}</span>`).join('')}</div>
  <div class="boundary"><strong>${t('Nu reprezintă','What it is not')}</strong><p>${esc(item.what_it_is_not[ctx.lang])}</p></div>
  ${kind==='MECH'&&item.executable?`<button type="button" data-theory-open-mechanism="${esc(item.token)}">${t('Deschide mecanismul','Open mechanism')}</button>`:''}`;
 }
 if(kind==='VAL'){
  const item=ctx.validations.find(v=>v.id===value);
  return item?`<p class="eyebrow">${esc(item.id)} · ${esc(item.claim_scope)}</p><h2>${esc(sem(item.id,ctx.lang,item.name))}</h2><p>${esc(item.pattern)}</p><button type="button" data-theory-open-view="process">${t('Vezi protocolul de validare','Open validation protocol')}</button>`:inspectorDefault(chapter,ctx);
 }
 if(kind==='REF'){
  const item=ctx.references.find(r=>r.id===value);
  return item?`<p class="eyebrow">${esc(item.id)} · ${esc(item.review_scope)}</p><h2>${t('Sursă','Source')}</h2><p>${esc(item.citation)}</p><p class="note">${t('Verificată la','Checked on')} ${esc(item.checked_on)}</p><a class="button-link" href="${esc(item.url)}" target="_blank" rel="noopener">${t('Deschide DOI ↗','Open DOI ↗')}</a>`:inspectorDefault(chapter,ctx);
 }
 if(kind==='CODE'){
  const ref=codeRefs(ctx).get(value);
  if(!ref) return inspectorDefault(chapter,ctx);
  const url=`https://github.com/LaurentiuStaicu/cognitive-epistemic-model/blob/${encodeURIComponent(ctx.releaseTag)}/${ref.path}`;
  return `<p class="eyebrow">CODE · ${esc(ref.language)}</p><h2><code>${esc(ref.symbol)}</code></h2><p><code>${esc(ref.path)}</code></p><p class="note">${t('Linkul este fixat la release-ul pe care îl rulează aplicația, nu la main.','The link is pinned to the release running in the application, not main.')}</p><a class="button-link" href="${url}" target="_blank" rel="noopener">${t('Deschide codul ↗','Open code ↗')}</a>`;
 }
 if(kind==='VIEW'){
  return `<p class="eyebrow">APP LINK</p><h2>${esc(displayToken(kind,value,ctx))}</h2><p>${t('Această legătură deschide suprafața aplicației asociată conceptului. Browser Back te poate readuce la acest capitol.','This link opens the application surface associated with the concept. Browser Back can return you to this chapter.')}</p><button type="button" data-theory-open-view="${esc(value)}">${t('Deschide','Open')}</button>`;
 }
 return inspectorDefault(chapter,ctx);
}

export async function mountTheoryReader(host:HTMLElement,context:Context,requestedSlug?:string){
 const ctx=context;
 const t=(ro:string,en:string)=>ctx.lang==='ro'?ro:en;
 const ordered=[...ctx.chapters].sort((a,b)=>a.order-b.order);
 let chapter=ordered.find(item=>theoryChapterSlug(item)===requestedSlug)??ordered[0];

 host.innerHTML=`<div class="theory-layout">
  <nav class="panel theory-chapters" aria-label="${t('Capitole de teorie','Theory chapters')}">
   <p class="eyebrow">${t('CUPRINS','CONTENTS')}</p>
   <label class="theory-chapter-select">${t('Capitol','Chapter')}<select id="theoryChapterSelect">${ordered.map(item=>`<option value="${esc(theoryChapterSlug(item))}" ${item.id===chapter.id?'selected':''}>${String(item.order).padStart(2,'0')} · ${esc(sem(item.id,ctx.lang,item.label[ctx.lang]))}</option>`).join('')}</select></label>
   <ol class="theory-chapter-list">${ordered.map(item=>`<li><button type="button" data-theory-chapter="${esc(theoryChapterSlug(item))}" aria-current="${item.id===chapter.id?'page':'false'}"><span>${String(item.order).padStart(2,'0')}</span>${esc(sem(item.id,ctx.lang,item.label[ctx.lang]))}</button></li>`).join('')}</ol>
  </nav>
  <article class="panel theory-reader" id="theoryArticle" tabindex="-1" aria-busy="true"><p class="loading">${t('Se încarcă teoria…','Loading theory…')}</p></article>
  <aside class="panel theory-inspector" id="theoryInspector" tabindex="-1" aria-label="${t('Inspector contextual','Contextual inspector')}" aria-live="polite"></aside>
 </div>`;

 const article=host.querySelector<HTMLElement>('#theoryArticle')!;
 const inspector=host.querySelector<HTMLElement>('#theoryInspector')!;

 const bindInspector=()=>{
  host.querySelectorAll<HTMLButtonElement>('[data-theory-token-kind]').forEach(button=>{
   button.onclick=()=>{
    const kind=button.dataset.theoryTokenKind!,value=button.dataset.theoryTokenValue!;
    inspector.innerHTML=inspectorFor(kind,value,chapter,ctx);
    inspector.querySelectorAll<HTMLButtonElement>('[data-theory-open-view]').forEach(open=>open.onclick=()=>ctx.navigate(open.dataset.theoryOpenView!));
    inspector.querySelectorAll<HTMLButtonElement>('[data-theory-open-mechanism]').forEach(open=>open.onclick=()=>{
     const token=open.dataset.theoryOpenMechanism!;
     location.hash=`#understanding/mechanisms/${encodeURIComponent(token)}`;
    });
    inspector.focus({preventScroll:true});
   };
  });
 };

 const loadChapter=async(next:TheoryChapter)=>{
  chapter=next;
  host.querySelectorAll<HTMLButtonElement>('[data-theory-chapter]').forEach(button=>button.setAttribute('aria-current',String(button.dataset.theoryChapter===theoryChapterSlug(chapter)?'page':'false')));
  article.setAttribute('aria-busy','true');
  article.innerHTML=`<p class="loading">${t('Se încarcă teoria…','Loading theory…')}</p>`;
  inspector.innerHTML=inspectorDefault(chapter,ctx);
  const relative=chapter.source_paths[ctx.lang].replace(/^docs\/theory\//,'');
  const response=await fetch(`./theory/${relative}`);
  if(!response.ok) throw new Error(`theory source: HTTP ${response.status}`);
  const markdown=await response.text();
  article.innerHTML=renderMarkdown(markdown,ctx);
  article.setAttribute('aria-busy','false');
  bindInspector();
 };

 host.querySelectorAll<HTMLButtonElement>('[data-theory-chapter]').forEach(button=>button.onclick=()=>{
  const slug=button.dataset.theoryChapter!;
  location.hash=`#understanding/theory/${encodeURIComponent(slug)}`;
 });
 host.querySelector<HTMLSelectElement>('#theoryChapterSelect')!.onchange=event=>{
  const slug=(event.currentTarget as HTMLSelectElement).value;
  location.hash=`#understanding/theory/${encodeURIComponent(slug)}`;
 };
 await loadChapter(chapter);
 if(requestedSlug)article.focus({preventScroll:false});
}
