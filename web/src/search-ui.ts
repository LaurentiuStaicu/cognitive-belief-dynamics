import {semanticIndex,type SemanticIndex,type SemanticLang} from './semantic';
import {searchSemanticIndex,type SemanticSearchResult} from './semantic-search';

type SearchUiOptions={lang:SemanticLang;index?:SemanticIndex;initialQuery?:string;onQueryChange?:(query:string)=>void;};

const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!));

function typeLabel(type:string,lang:SemanticLang):string{
 const labels:Record<string,[string,string]>={
  VARIABLE:['Variabilă','Variable'],MODULE:['Modul','Module'],REFERENCE:['Referință','Reference'],VALIDATION:['Validare','Validation'],
  EMPIRICAL_TARGET:['Țintă empirică','Empirical target'],THEORY_CHAPTER:['Capitol de teorie','Theory chapter'],
  GLOSSARY_ENTRY:['Termen','Glossary entry'],COMPUTATIONAL_NODE:['Nod de calcul','Computational node']
 };
 const pair=labels[type];return pair?(lang==='ro'?pair[0]:pair[1]):type;
}

function resultMarkup(result:SemanticSearchResult,lang:SemanticLang):string{
 const short=result.shortName?'<code>'+esc(result.shortName)+'</code>':'';
 return '<li class="semantic-search-result" data-search-result-id="'+esc(result.id)+'">'+
  '<div class="semantic-search-result-heading"><strong>'+esc(result.label)+'</strong><span>'+esc(typeLabel(result.semanticType,lang))+'</span></div>'+
  '<div class="semantic-search-result-meta">'+short+'<code>'+esc(result.id)+'</code></div></li>';
}

export function mountSemanticSearch(host:HTMLElement,options:SearchUiOptions):void{
 const lang=options.lang;const index=options.index??semanticIndex;const t=(ro:string,en:string)=>lang==='ro'?ro:en;const initial=options.initialQuery??'';
 host.innerHTML='<search class="global-search" aria-labelledby="semanticSearchTitle">'+
  '<form id="semanticSearchForm" class="semantic-search-form">'+
   '<div class="semantic-search-heading"><div><p class="eyebrow">'+t('CĂUTARE SEMANTICĂ','SEMANTIC SEARCH')+'</p><h2 id="semanticSearchTitle">'+t('Găsește un concept în model','Find a concept in the model')+'</h2></div>'+
   '<p>'+t('Caută după nume, ID canonic, abreviere sau termen asociat. Ordinea rezultatelor este lexicală, nu un scor al dovezilor.','Search by name, canonical ID, abbreviation or related term. Result order is lexical, not an evidence score.')+'</p></div>'+
   '<div class="semantic-search-controls"><label for="semanticSearchInput">'+t('Termen de căutare','Search term')+'</label>'+
    '<div class="semantic-search-input-row"><input id="semanticSearchInput" name="q" type="search" autocomplete="off" value="'+esc(initial)+'" placeholder="'+esc(t('ex.: familiaritate, acuratețe, VAR.FAMILIARITY.CLAIM','e.g. familiarity, accuracy, VAR.FAMILIARITY.CLAIM'))+'">'+
     '<button type="submit">'+t('Caută','Search')+'</button><button type="reset">'+t('Șterge','Clear')+'</button></div></div>'+
   '<p id="semanticSearchSummary" class="semantic-search-summary" aria-live="polite"></p><ol id="semanticSearchResults" class="semantic-search-results"></ol>'+
  '</form></search>';
 const form=host.querySelector<HTMLFormElement>('#semanticSearchForm')!;const input=host.querySelector<HTMLInputElement>('#semanticSearchInput')!;
 const summary=host.querySelector<HTMLElement>('#semanticSearchSummary')!;const resultsHost=host.querySelector<HTMLOListElement>('#semanticSearchResults')!;
 const render=(query:string)=>{
  const trimmed=query.trim();options.onQueryChange?.(query);
  if(!trimmed){summary.textContent='';resultsHost.replaceChildren();return;}
  const results=searchSemanticIndex(index,trimmed,{lang,limit:20});
  summary.textContent=results.length===0?t('Niciun rezultat semantic.','No semantic results.'):(lang==='ro'?String(results.length)+' rezultate semantice.':String(results.length)+' semantic results.');
  resultsHost.innerHTML=results.map(result=>resultMarkup(result,lang)).join('');
 };
 form.onsubmit=event=>{event.preventDefault();render(input.value);};
 form.onreset=()=>{queueMicrotask(()=>{input.value='';render('');input.focus();});};
 if(initial.trim())render(initial);
}
