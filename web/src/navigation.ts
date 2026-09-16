export type UiLang='ro'|'en';

export type AppView='learning'|'structure'|'process'|'runs'|'comparison'|'planning'|'reference';
export type NavigationGroupId='understand'|'analyze'|'act'|'library';

export type NavigationItem={
 view:AppView;
 label:Record<UiLang,string>;
 description:Record<UiLang,string>;
};

export type NavigationGroup={
 id:NavigationGroupId;
 label:Record<UiLang,string>;
 description:Record<UiLang,string>;
 defaultView:AppView;
 items:readonly NavigationItem[];
};

export const navigationGroups:readonly NavigationGroup[]=[
 {
  id:'understand',
  label:{ro:'Înțelege',en:'Understand'},
  description:{ro:'Teorie, mecanisme, hartă și metodologie.',en:'Theory, mechanisms, map and methodology.'},
  defaultView:'learning',
  items:[
   {view:'learning',label:{ro:'Teorie și mecanisme',en:'Theory & mechanisms'},description:{ro:'Explicații ghidate ale variabilelor și mecanismelor.',en:'Guided explanations of variables and mechanisms.'}},
   {view:'structure',label:{ro:'Hartă',en:'Map'},description:{ro:'Dependențe computaționale și relații înregistrate.',en:'Computational dependencies and registered relations.'}},
   {view:'process',label:{ro:'Metodologie · Visual ODD',en:'Methodology · Visual ODD'},description:{ro:'Procese, limite și convenții ale modelului.',en:'Model processes, boundaries and conventions.'}}
  ]
 },
 {
  id:'analyze',
  label:{ro:'Analizează',en:'Analyze'},
  description:{ro:'Rulează și compară scenariile de referință.',en:'Inspect and compare the reference scenarios.'},
  defaultView:'runs',
  items:[
   {view:'runs',label:{ro:'Scenarii',en:'Scenarios'},description:{ro:'Rulări de referință și explicații pe pași.',en:'Reference runs and step explanations.'}},
   {view:'comparison',label:{ro:'Comparații',en:'Comparisons'},description:{ro:'Contraste sincronizate între scenarii.',en:'Synchronized contrasts between scenarios.'}}
  ]
 },
 {
  id:'act',
  label:{ro:'Acționează',en:'Act'},
  description:{ro:'Prioritizează măsuri și planifică acțiunile.',en:'Prioritize measures and plan actions.'},
  defaultView:'planning',
  items:[
   {view:'planning',label:{ro:'Priorități și plan',en:'Priorities & plan'},description:{ro:'Laboratorul de intervenții și calendarul selectat.',en:'Intervention laboratory and selected action schedule.'}}
  ]
 },
 {
  id:'library',
  label:{ro:'Bibliotecă',en:'Library'},
  description:{ro:'Consultă obiectele și dovezile canonice.',en:'Consult canonical objects and evidence.'},
  defaultView:'reference',
  items:[
   {view:'reference',label:{ro:'Registru științific',en:'Scientific registry'},description:{ro:'Variabile, relații, module, referințe și statut epistemic.',en:'Variables, relations, modules, references and epistemic status.'}}
  ]
 }
] as const;

export const requiredExistingViews:readonly AppView[]=['learning','planning','structure','runs','comparison','process','reference'];

export function navigationGroupForView(view:AppView):NavigationGroup{
 const group=navigationGroups.find(candidate=>candidate.items.some(item=>item.view===view));
 if(!group)throw new Error('view is not mapped into OA-3 information architecture: '+view);
 return group;
}

export function navigationItem(view:AppView):NavigationItem{
 const item=navigationGroupForView(view).items.find(candidate=>candidate.view===view);
 if(!item)throw new Error('view item is not mapped: '+view);
 return item;
}

export function isAppView(value:string):value is AppView{return requiredExistingViews.includes(value as AppView);}
