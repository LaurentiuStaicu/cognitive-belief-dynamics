import type {SemanticEntity,SemanticIndex,SemanticLang} from './semantic';

export type SemanticSearchMatch=
 |'ID_EXACT'|'SHORT_NAME_EXACT'|'PREFERRED_LABEL_EXACT'|'ALTERNATIVE_LABEL_EXACT'
 |'PREFERRED_LABEL_PREFIX'|'SHORT_NAME_PREFIX'|'ID_PREFIX'
 |'PREFERRED_LABEL_TOKENS'|'ANY_LABEL_TOKENS'|'METADATA_TOKENS'|'SUMMARY_TOKENS';

export type SemanticSearchOptions={
 lang:SemanticLang;
 limit?:number;
 semanticTypes?:readonly string[];
};

export type SemanticSearchResult={
 id:string;
 semanticType:string;
 label:string;
 shortName?:string;
 match:SemanticSearchMatch;
 /** Lexical retrieval ordering only. Never an epistemic/evidence score. */
 retrievalScore:number;
 statusFacets?:SemanticEntity['status_facets'];
};

export function normalizeSearchText(value:string):string{
 return value.normalize('NFKD').replace(/\p{M}/gu,'').toLocaleLowerCase('und').replace(/[^\p{L}\p{N}]+/gu,' ').trim().replace(/\s+/g,' ');
}

function tokens(value:string):string[]{return normalizeSearchText(value).split(' ').filter(Boolean);}
function localizedLabel(entity:SemanticEntity,lang:SemanticLang):string{
 const p=entity.labels.preferred;
 return p[lang]??p.und??p.en??p.ro??entity.id;
}
function allPreferred(entity:SemanticEntity):string[]{return Object.values(entity.labels.preferred).filter((v):v is string=>typeof v==='string');}
function allAlternative(entity:SemanticEntity):string[]{return Object.values(entity.labels.alternative??{}).flatMap(value=>value??[]);}
function allSummary(entity:SemanticEntity):string[]{return Object.values(entity.summary??{}).filter((v):v is string=>typeof v==='string');}
function containsAll(haystack:string,needles:string[]):boolean{const normalized=normalizeSearchText(haystack);return needles.every(token=>normalized.includes(token));}

function rank(entity:SemanticEntity,query:string,lang:SemanticLang):{match:SemanticSearchMatch;retrievalScore:number}|null{
 const q=normalizeSearchText(query);if(!q)return null;
 const qTokens=tokens(q);
 const id=normalizeSearchText(entity.id);
 const short=normalizeSearchText(entity.short_name??'');
 const preferredLocal=normalizeSearchText(localizedLabel(entity,lang));
 const preferred=allPreferred(entity).map(normalizeSearchText);
 const alternative=allAlternative(entity).map(normalizeSearchText);
 const metadata=[entity.semantic_type,...(entity.semantic_roles??[])].map(normalizeSearchText);
 const summaries=allSummary(entity);
 if(id===q)return {match:'ID_EXACT',retrievalScore:1000};
 if(short&&short===q)return {match:'SHORT_NAME_EXACT',retrievalScore:950};
 if(preferredLocal===q||preferred.includes(q))return {match:'PREFERRED_LABEL_EXACT',retrievalScore:900};
 if(alternative.includes(q))return {match:'ALTERNATIVE_LABEL_EXACT',retrievalScore:850};
 if(preferredLocal.startsWith(q)||preferred.some(value=>value.startsWith(q)))return {match:'PREFERRED_LABEL_PREFIX',retrievalScore:800};
 if(short&&short.startsWith(q))return {match:'SHORT_NAME_PREFIX',retrievalScore:750};
 if(id.startsWith(q))return {match:'ID_PREFIX',retrievalScore:700};
 if(containsAll(preferredLocal,qTokens))return {match:'PREFERRED_LABEL_TOKENS',retrievalScore:600};
 if([...preferred,...alternative].some(value=>containsAll(value,qTokens)))return {match:'ANY_LABEL_TOKENS',retrievalScore:550};
 if(metadata.some(value=>containsAll(value,qTokens)))return {match:'METADATA_TOKENS',retrievalScore:300};
 if(summaries.some(value=>containsAll(value,qTokens)))return {match:'SUMMARY_TOKENS',retrievalScore:200};
 return null;
}

export function searchSemanticIndex(index:SemanticIndex,query:string,options:SemanticSearchOptions):SemanticSearchResult[]{
 const limit=Math.max(1,Math.min(options.limit??20,100));
 const allowed=options.semanticTypes?new Set(options.semanticTypes):null;
 const results:SemanticSearchResult[]=[];
 for(const entity of index.entities){
  if(allowed&&!allowed.has(entity.semantic_type))continue;
  const ranked=rank(entity,query,options.lang);
  if(!ranked)continue;
  const item:SemanticSearchResult={
   id:entity.id,
   semanticType:entity.semantic_type,
   label:localizedLabel(entity,options.lang),
   match:ranked.match,
   retrievalScore:ranked.retrievalScore
  };
  if(entity.short_name!==undefined)item.shortName=entity.short_name;
  if(entity.status_facets!==undefined)item.statusFacets=entity.status_facets;
  results.push(item);
 }
 return results.sort((a,b)=>b.retrievalScore-a.retrievalScore||a.id.localeCompare(b.id,'en')).slice(0,limit);
}

