import {semanticIndex,type SemanticIndex,type SemanticLang,type SemanticStatusFacets} from './semantic';
import {inspectSemanticIndex,type SemanticInspectorModel} from './semantic-inspector';

type InspectorUiOptions={lang:SemanticLang;id?:string;index?:SemanticIndex;onSelect?:(id:string)=>void;};
const esc=(value:string)=>value.replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!));

function layerLabel(layer:string,lang:SemanticLang):string{
 const labels:Record<string,[string,string]>={
  REGISTERED_EVIDENCE_RELATION:['Relație în registrul de dovezi','Evidence-registry relation'],
  COMPUTATIONAL_DEPENDENCY:['Dependență de calcul','Computational dependency'],
  DOCUMENTATION_RELATION:['Relație de documentație','Documentation relation']
 };const pair=labels[layer];return pair?(lang==='ro'?pair[0]:pair[1]):layer;
}
function statusMarkup(facets:SemanticStatusFacets|undefined,lang:SemanticLang):string{
 if(!facets)return '';const t=(ro:string,en:string)=>lang==='ro'?ro:en;const rows:string[]=[];
 const add=(label:string,value:string|undefined)=>{if(value)rows.push('<div><dt>'+esc(label)+'</dt><dd><span class="epistemic-status" data-status="'+esc(value)+'">'+esc(value)+'</span></dd></div>');};
 add(t('Dovadă fenomen','Phenomenon evidence'),facets.phenomenon_evidence);
 add(t('Dovadă mecanism','Mechanism evidence'),facets.mechanism_evidence);
 add(t('Formă funcțională','Functional form'),facets.functional_form);
 if(facets.source_tags?.length)rows.push('<div><dt>'+esc(t('Etichete sursă','Source tags'))+'</dt><dd>'+facets.source_tags.map(tag=>'<code>'+esc(tag)+'</code>').join(' ')+'</dd></div>');
 return rows.length?'<dl class="inspector-statuses">'+rows.join('')+'</dl>':'';
}
function sourceMarkup(path:string,sourceId:string,lang:SemanticLang):string{const t=(ro:string,en:string)=>lang==='ro'?ro:en;return '<div class="inspector-source"><strong>'+t('Sursă canonică','Canonical source')+'</strong><code>'+esc(path)+'</code><code>'+esc(sourceId)+'</code></div>';}

function entityMarkup(model:Extract<SemanticInspectorModel,{kind:'entity'}>,lang:SemanticLang):string{
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const related=model.related.map(relation=>'<li><button type="button" class="inspector-relation" data-inspect-id="'+esc(relation.id)+'"><span>'+esc(layerLabel(relation.layer,lang))+'</span><strong>'+(relation.direction==='incoming'?'←':'→')+' '+esc(relation.counterpartLabel)+'</strong><code>'+esc(relation.id)+'</code></button></li>').join('');
 return '<p class="eyebrow">'+esc(model.semanticType)+'</p><h2 id="semanticInspectorTitle">'+esc(model.title)+'</h2>'+
  (model.shortName?'<p><code>'+esc(model.shortName)+'</code></p>':'')+(model.summary?'<p>'+esc(model.summary)+'</p>':'')+
  '<p class="inspector-id"><code>'+esc(model.id)+'</code></p>'+statusMarkup(model.statusFacets,lang)+sourceMarkup(model.source.path,model.source.source_id,lang)+
  '<section class="inspector-related" aria-labelledby="inspectorRelatedTitle"><h3 id="inspectorRelatedTitle">'+t('Relații asociate','Related relations')+'</h3>'+
  (related?'<ul>'+related+'</ul>':'<p class="note">'+t('Nu sunt relații indexate pentru această entitate.','No indexed relations for this entity.')+'</p>')+'</section>';
}

function relationMarkup(model:Extract<SemanticInspectorModel,{kind:'relation'}>,lang:SemanticLang):string{
 const t=(ro:string,en:string)=>lang==='ro'?ro:en;
 const details:string[]=[];
 if(model.relationType)details.push('<div><dt>'+t('Tip relație','Relation type')+'</dt><dd><code>'+esc(model.relationType)+'</code></dd></div>');
 if(model.polarity)details.push('<div><dt>'+t('Polaritate','Polarity')+'</dt><dd><code>'+esc(model.polarity)+'</code></dd></div>');
 if(model.formula)details.push('<div><dt>'+t('Formulă','Formula')+'</dt><dd><code>'+esc(model.formula)+'</code></dd></div>');
 if(model.codeFile)details.push('<div><dt>'+t('Fișier cod','Code file')+'</dt><dd><code>'+esc(model.codeFile)+'</code></dd></div>');
 if(model.registeredRelationId)details.push('<div><dt>'+t('Relație înregistrată','Registered relation')+'</dt><dd><code>'+esc(model.registeredRelationId)+'</code></dd></div>');
 const refs=model.evidenceRefs?.length?'<div class="inspector-evidence-refs"><strong>'+t('Referințe de dovadă','Evidence references')+'</strong>'+model.evidenceRefs.map(id=>'<button type="button" data-inspect-id="'+esc(id)+'"><code>'+esc(id)+'</code></button>').join('')+'</div>':'';
 return '<p class="eyebrow">'+esc(layerLabel(model.layer,lang))+'</p><h2 id="semanticInspectorTitle">'+esc(model.title)+'</h2><p class="inspector-id"><code>'+esc(model.id)+'</code></p>'+
  '<div class="inspector-endpoints"><button type="button" data-inspect-id="'+esc(model.sourceId)+'"><span>'+t('Sursă','Source')+'</span><strong>'+esc(model.sourceLabel)+'</strong></button>'+
  '<span aria-hidden="true">→</span><button type="button" data-inspect-id="'+esc(model.targetId)+'"><span>'+t('Țintă','Target')+'</span><strong>'+esc(model.targetLabel)+'</strong></button></div>'+
  (details.length?'<dl class="inspector-details">'+details.join('')+'</dl>':'')+statusMarkup(model.statusFacets,lang)+refs+sourceMarkup(model.sourceRecord.path,model.sourceRecord.source_id,lang);
}

export function mountSemanticInspector(host:HTMLElement,options:InspectorUiOptions):void{
 const lang=options.lang;const index=options.index??semanticIndex;const t=(ro:string,en:string)=>lang==='ro'?ro:en;const id=options.id?.trim()??'';
 host.dataset.inspectorId=id;
 if(!id){host.dataset.inspectorKind='empty';host.innerHTML='<p class="eyebrow">'+t('INSPECTOR UNIVERSAL','UNIVERSAL INSPECTOR')+'</p><h2 id="semanticInspectorTitle">'+t('Selectează un obiect semantic','Select a semantic object')+'</h2><p>'+t('Folosește Search pentru a deschide aici o variabilă, un modul, o referință, un capitol, un nod de calcul sau o relație.','Use Search to open a variable, module, reference, chapter, computational node or relation here.')+'</p><p class="note">'+t('Inspectorul proiectează identitatea canonică și statusurile existente; nu atribuie un scor de importanță sau de adevăr.','The Inspector projects canonical identity and existing statuses; it does not assign importance or truth scores.')+'</p>';return;}
 const model=inspectSemanticIndex(index,id,lang);
 if(!model){host.dataset.inspectorKind='missing';host.innerHTML='<p class="eyebrow">'+t('INSPECTOR UNIVERSAL','UNIVERSAL INSPECTOR')+'</p><h2 id="semanticInspectorTitle">'+t('Obiect indisponibil','Object unavailable')+'</h2><p><code>'+esc(id)+'</code></p>';return;}
 host.dataset.inspectorKind=model.kind;host.innerHTML=model.kind==='entity'?entityMarkup(model,lang):relationMarkup(model,lang);
 host.querySelectorAll<HTMLButtonElement>('[data-inspect-id]').forEach(button=>button.onclick=()=>{const next=button.dataset.inspectId;if(next)options.onSelect?.(next);});
}
