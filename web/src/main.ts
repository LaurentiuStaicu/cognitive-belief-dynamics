import cytoscape from 'cytoscape';
import './style.css';

type Variable = {id:string; short_name:string; label:{en:string;ro:string}; definition:string};
type Link = {id:string; source:string; target:string; relation_type:string; mechanism_evidence_status:string};

async function loadJson<T>(path:string): Promise<T> {
  const r = await fetch(path);
  if (!r.ok) throw new Error(`Failed to load ${path}`);
  return r.json() as Promise<T>;
}

async function init() {
  // Public build will copy model JSON into /model at build time.
  const vars = await loadJson<Variable[]>('./model/variables.json');
  const links = await loadJson<Link[]>('./model/links.json');
  const known = new Set(vars.map(v => v.id));
  const graphLinks = links.filter(l => known.has(l.source) && known.has(l.target));
  const elements = [
    ...vars.map(v => ({data:{id:v.id,label:v.label.en,definition:v.definition}})),
    ...graphLinks.map(l => ({data:{id:l.id,source:l.source,target:l.target,label:l.relation_type}}))
  ];
  cytoscape({
    container: document.getElementById('cy'), elements,
    style: [
      {selector:'node',style:{'label':'data(label)','text-wrap':'wrap','text-max-width':140,'width':55,'height':55}},
      {selector:'edge',style:{'curve-style':'bezier','target-arrow-shape':'triangle','label':'data(label)','font-size':9}}
    ],
    layout:{name:'cose'}
  });
  const structured = document.getElementById('structured')!;
  structured.innerHTML = vars.map(v => `<article><h3>${v.label.en}</h3><p>${v.definition}</p><code>${v.id}</code></article>`).join('');
  document.getElementById('structureBtn')!.addEventListener('click',()=>{document.getElementById('graphView')!.hidden=false;document.getElementById('structuredView')!.hidden=true;});
  document.getElementById('accessibleBtn')!.addEventListener('click',()=>{document.getElementById('graphView')!.hidden=true;document.getElementById('structuredView')!.hidden=false;});
}

init().catch(e => document.body.insertAdjacentHTML('beforeend', `<pre>${String(e)}</pre>`));
