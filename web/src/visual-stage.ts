import type {Core} from 'cytoscape';
import {dependencies} from './dependencies';
type Frame={time:number;familiarity:number;correction:number;reliability:number;belief:number;accuracy_weight:number;share_probability:number;share:boolean;events:{event_type:string}[]};
type Run={id:string;frames:Frame[]};
// Counts logged exposure events, not elapsed time. Share is the recorded RNG outcome.
export function snapshot(run:Run,index:number):Record<string,number>{
 const f=run.frames[index];
 return {Nexp:run.frames.slice(0,index+1).reduce((n,f)=>n+f.events.filter(e=>e.event_type==='ExposureEvent').length,0),F:f.familiarity,C:f.correction,T:f.reliability,B:f.belief,W:f.accuracy_weight,P:f.share_probability,Share:Number(f.share)};
}
export const polarity=(id:string)=>['exposure-f','f-b','b-p','prior-b','cue-w','baseline-w'].includes(id)?'+':id==='time-c'?'−':id==='p-share'||id==='random-share'?'~':'×';
export function mountVisualStage(cy:Core,lang:'ro'|'en',runs:Run[],initial:string,time:number,show:(id:string)=>void,edgeDetail:(id:string)=>void,open:(id:string,step:number)=>void,onFrame:(id:string,step:number)=>void){
 const tr=(ro:string,en:string)=>lang==='ro'?ro:en;
 let run=runs.find(r=>r.id===initial)!,index=Math.min(time,run.frames.length-1),selected=cy.nodes(':selected').first().id(),tourStep=0;
 const names:Record<string,string>={repetition:tr('Repetiție','Repetition'),correction:tr('Corecție','Correction'),source:tr('Sursă','Source'),accuracy:tr('Acuratețe','Accuracy')};
 const tours:Record<string,string[]>={repetition:['Nexp','F','B','P','Share'],correction:['C','B','P','Share'],accuracy:['W','P','Share']};
 const controls=document.createElement('section');controls.className='panel visual-controls';
 controls.innerHTML=`<h3>${tr('Explorează mecanismul pas cu pas','Explore the mechanism step by step')}</h3><div class="stage-options"><label><input id="stageBands" type="checkbox"> ${tr('Benzi funcționale','Functional bands')}</label><label><input id="stageFocus" type="checkbox"> ${tr('Focalizează vecinătatea selecției','Focus on selection neighbours')}</label><label for="stageRun">${tr('Rulare','Run')}</label><select id="stageRun">${runs.map(r=>`<option value="${r.id}">${names[r.id]}</option>`).join('')}</select><label for="stageTime">${tr('Pas','Step')}</label><input id="stageTime" type="range" min="0" max="${run.frames.length-1}" value="${index}"><output id="stageStep"></output><button id="stageOpen">${tr('Deschide explicația acestui pas','Open this step’s explanation')}</button></div><div class="stage-options"><label for="stageTour">${tr('Tur ghidat','Guided tour')}</label><select id="stageTour">${Object.keys(tours).map(id=>`<option value="${id}">${names[id]}</option>`).join('')}</select><button id="stageStart">${tr('Începe turul','Start tour')}</button><button id="stageNext" disabled>${tr('Următorul factor','Next factor')}</button></div><p id="stageTourText" role="status">${tr('Tururile parcurg dependențele pedagogic; nu injectează un impuls și nu recalculează modelul.','Tours traverse dependencies for learning; they do not inject an impulse or recalculate the model.')}</p><p class="note">${tr('Valorile provin din rularea Python precalculată. Benzile organizează calculul, nu descriu regiuni cerebrale sau etape psihologice demonstrate.','Values come from the precomputed Python run. Bands organize computation, not brain regions or established psychological stages.')} ${tr('+ / −: sensul în condițiile coeficienților de referință; ×: depinde de context sau interacțiune; ~: eșantionare aleatoare.','+ / −: direction under reference coefficients; ×: context-dependent or interaction; ~: random sampling.')}</p><div id="stageReadout" aria-live="polite"></div>`;
 document.querySelector('.graph-layout')!.before(controls);
 const q=<T extends HTMLElement>(id:string)=>controls.querySelector<T>('#'+id)!;
 q<HTMLSelectElement>('stageRun').value=run.id;
 const css=getComputedStyle(document.documentElement),accent=css.getPropertyValue('--accent').trim(),muted=css.getPropertyValue('--muted').trim();
 cy.style().selector('edge').style({'label':'data(polarity)','color':muted,'font-size':17,'text-background-color':css.getPropertyValue('--surface').trim()||css.getPropertyValue('--bg').trim(),'text-background-opacity':1,'text-background-padding':'3px'}).selector('.stage-dim').style({'opacity':.18}).update();
 cy.edges().forEach(e=>{e.data('polarity',polarity(e.id()));});
 const original=new Map(cy.nodes().map(n=>[n.id(),{...n.position()}]));
 const groups=[['Nexp','Correction','Feedback','Time','Prior','Evidence','Direction','Cue','Baseline','Reward','Random'],['F','C','T'],['B','W'],['P','Share']];
 const labels=[tr('Intrări și context','Inputs and context'),tr('Memorie și estimări','Memory and estimates'),tr('Judecată și ponderare','Judgment and weighting'),tr('Decizie și acțiune','Decision and action')];
 const host=document.getElementById('cy')!;host.style.position='relative';
 const bands=document.createElementNS('http://www.w3.org/2000/svg','svg');bands.classList.add('stage-bands');bands.setAttribute('aria-hidden','true');host.prepend(bands);bands.style.display='none';
 const drawBands=()=>{const zoom=cy.zoom(),pan=cy.pan();bands.innerHTML=groups.map((ids,i)=>{const count=ids.filter(id=>cy.getElementById(id).length).length;return `<g transform="translate(${pan.x},${pan.y}) scale(${zoom})"><rect x="${i*260-110}" y="-95" width="230" height="${Math.max(3,count)*115+135}" rx="14" fill="${accent}" fill-opacity="0.055" stroke="${muted}" stroke-opacity="0.3"/><text x="${i*260}" y="-60" text-anchor="middle" fill="${muted}" font-size="14">${labels[i]}</text></g>`;}).join('');};
 cy.on('pan zoom resize',drawBands);
 q<HTMLInputElement>('stageBands').onchange=e=>{const enabled=(e.target as HTMLInputElement).checked;bands.style.display=enabled?'block':'none';cy.nodes().positions(n=>{if(!enabled)return original.get(n.id())!;const group=groups.findIndex(ids=>ids.includes(n.id()));const ids=groups[group].filter(id=>cy.getElementById(id).length);return{x:group*260,y:ids.indexOf(n.id())*115};});cy.fit(undefined,65);drawBands();};
 const focus=()=>{cy.elements().removeClass('stage-dim');if(q<HTMLInputElement>('stageFocus').checked){const picked=cy.$(':selected');const visible=picked.nodes().closedNeighborhood().union(picked.edges()).union(picked.edges().connectedNodes());cy.elements().difference(visible).addClass('stage-dim');}};
 const update=()=>{
 onFrame(run.id,index);
 const values=snapshot(run,index);cy.nodes().forEach(n=>{if(n.data('baseLabel')===undefined)n.data('baseLabel',n.data('label'));const value=values[n.id()];n.data('label',n.data('baseLabel')+(value===undefined?'':`\n${Number.isInteger(value)?value:value.toFixed(3)}`));});
 q('stageStep').textContent=`${index} / ${run.frames.length-1}`;
 q('stageReadout').textContent=Object.entries(values).map(([k,v])=>`${k}: ${Number.isInteger(v)?v:v.toFixed(3)}`).join(' · ');
 focus();
 };
 const inspect=()=>{document.getElementById('stageNeighbours')?.remove();const node=cy.nodes(':selected').first();if(!node.length){focus();return;}selected=node.id();const panel=document.createElement('div');panel.id='stageNeighbours';
 panel.innerHTML=`<h3>${tr('Vecinătatea vizibilă a factorului','Visible factor neighbourhood')}: ${selected}</h3>`+(['target','source'] as const).map((end,i)=>`<p><strong>${i?tr('Ieșiri','Outputs'):tr('Intrări','Inputs')}</strong></p><div class="dependency-buttons">${dependencies.filter(e=>e[end]===selected&&cy.getElementById(e.id).length).map(e=>`<button data-stage-node="${i?e.target:e.source}">${i?e.target:e.source}</button><button data-stage-edge="${e.id}">${e.source} ${polarity(e.id)} → ${e.target}</button>`).join('')||tr('Niciuna în această vedere.','None in this view.')}</div>`).join('');
 document.getElementById('detail')!.append(panel);panel.querySelectorAll<HTMLButtonElement>('[data-stage-node]').forEach(b=>b.onclick=()=>{show(b.dataset.stageNode!);inspect();});panel.querySelectorAll<HTMLButtonElement>('[data-stage-edge]').forEach(b=>b.onclick=()=>{edgeDetail(b.dataset.stageEdge!);focus();});focus();};
 // Existing selection handlers render synchronously; append the accessible neighbourhood afterwards.
 cy.on('tap','node',inspect);cy.on('tap','edge',focus);
 document.getElementById('variable')!.addEventListener('change',inspect);document.getElementById('dependency')!.addEventListener('change',focus);
 document.getElementById('detail')!.addEventListener('click',()=>focus());
 q<HTMLInputElement>('stageFocus').onchange=focus;
 q<HTMLSelectElement>('stageRun').onchange=()=>{run=runs.find(r=>r.id===q<HTMLSelectElement>('stageRun').value)!;index=0;q<HTMLInputElement>('stageTime').value='0';q<HTMLInputElement>('stageTime').max=String(run.frames.length-1);q<HTMLButtonElement>('stageNext').disabled=true;update();};
 q<HTMLInputElement>('stageTime').oninput=()=>{index=Number(q<HTMLInputElement>('stageTime').value);update();};
 q('stageOpen').onclick=()=>open(run.id,index);
 const tour=()=>{const id=q<HTMLSelectElement>('stageTour').value;const route=tours[id].filter(key=>cy.getElementById(key).length);if(!route.length)return;q<HTMLInputElement>('stageFocus').checked=true;show(route[tourStep]);inspect();q('stageTourText').textContent=`${tr('Traseu explicativ','Explanatory route')}: ${route.join(' → ')} · ${tourStep+1}/${route.length}. ${tr('Factor selectat','Selected factor')}: ${route[tourStep]}.`;q<HTMLButtonElement>('stageNext').disabled=tourStep>=route.length-1;};
 q('stageStart').onclick=()=>{tourStep=0;run=runs.find(r=>r.id===q<HTMLSelectElement>('stageTour').value)!;index=run.id==='repetition'?4:5;q<HTMLSelectElement>('stageRun').value=run.id;q<HTMLInputElement>('stageTime').value=String(index);update();tour();};
 q('stageNext').onclick=()=>{tourStep++;tour();};q<HTMLSelectElement>('stageTour').onchange=()=>{q<HTMLButtonElement>('stageNext').disabled=true;};
 update();inspect();
}
