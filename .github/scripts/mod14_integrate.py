from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(path:str):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

def dump(path:str,value):
    (ROOT/path).write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')

def append_unique(items,item):
    if not any(existing.get('id')==item['id'] for existing in items):
        items.append(item)

def replace(path:str,old:str,new:str):
    target=ROOT/path
    text=target.read_text(encoding='utf-8')
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f'patch anchor missing in {path}: {old[:80]!r}')
    target.write_text(text.replace(old,new),encoding='utf-8')

# Align contract references with the canonical REF.* namespace.
contract=load('model/contracts/world_model_v1.json')
for ref in contract['references']:
    if ref['id'].startswith('WM.REF.'):
        ref['id']='REF.WM.'+ref['id'][len('WM.REF.'):]
dump('model/contracts/world_model_v1.json',contract)
replace('schemas/world_model.schema.json','"pattern":"^WM\\\\.REF\\\\."','"pattern":"^REF\\\\.WM\\\\."')

# Canonical variables: narrow normative quantities plus provenance. Existing B/F/C/T/Aissue are not duplicated.
variables=load('model/variables.json')
new_variables=[
 {'id':'VAR.WORLD.PRIOR','short_name':'Pprior','ontology_type':'EXOGENOUS_INPUT','entity_type':'PropositionState','conceptual_module':'MOD.14','label':{'en':'Prior proposition probability','ro':'Probabilitatea anterioară a propoziției'},'definition':'Normative probability assigned to a binary proposition before the current diagnostic evidence item when the task supplies a defensible probabilistic prior.','what_it_is_not':'The descriptive CEM belief B, ground truth, or population prevalence unless a task explicitly defines it that way.','range':[0,1]},
 {'id':'VAR.WORLD.LIKELIHOOD_RATIO','short_name':'LR','ontology_type':'EXOGENOUS_INPUT','entity_type':'EvidenceRecord','conceptual_module':'MOD.14','label':{'en':'Diagnostic likelihood ratio','ro':'Raport de verosimilitate diagnostic'},'definition':'Externally supplied diagnostic ratio P(evidence|proposition true) / P(evidence|proposition false) from a defensible task-specific measurement model.','what_it_is_not':'Source trust, familiarity, amount of evidence, social agreement, salience, or subjective confidence.','range':[0,1000000]},
 {'id':'VAR.WORLD.POSTERIOR','short_name':'Pwm','ontology_type':'DERIVED_METRIC','entity_type':'PropositionState','conceptual_module':'MOD.14','label':{'en':'Normative world-model posterior','ro':'Posteriorul normativ al modelului realității'},'definition':'Normative binary proposition probability after a declared prior is updated with one or more defensible diagnostic likelihood ratios.','what_it_is_not':'VAR.BELIEF.CLAIM B, knowledge, truth, ideology, or a calibrated population opinion.','range':[0,1]},
 {'id':'VAR.WORLD.UNCERTAINTY','short_name':'Uwm','ontology_type':'DERIVED_METRIC','entity_type':'PropositionState','conceptual_module':'MOD.14','label':{'en':'Normative proposition uncertainty','ro':'Incertitudinea normativă a propoziției'},'definition':'Normalized binary Shannon entropy derived from Pwm, equal to one at p=0.5 and zero at p=0 or p=1.','what_it_is_not':'The decision-uncertainty registry, metacognitive confidence, model misspecification, or unknown unknowns.','range':[0,1]},
 {'id':'VAR.WORLD.PROVENANCE','short_name':'Prov','ontology_type':'OBSERVABLE','entity_type':'EvidenceRecord','conceptual_module':'MOD.14','label':{'en':'Evidence provenance record','ro':'Înregistrarea provenienței dovezii'},'definition':'Traceable record of an evidence item, source, acquisition context, and measurement assumptions relevant to a world-model update.','what_it_is_not':'Objective truth certification or the agent-relative source-reliability estimate T.'}
]
for item in new_variables: append_unique(variables,item)
dump('model/variables.json',variables)

# Canonical references used by Theory, Semantic Spine and registry.
references=load('model/references.json')
for ref in contract['references']:
    append_unique(references,{
      'id':ref['id'],'citation':ref['citation'],'doi':ref['doi'],'url':ref['url'],'access_url':ref['url'],
      'study_type':'REVIEW' if ref['id'] in {'REF.WM.KNILL_POUGET.2004','REF.WM.ZWAAN_RADVANSKY.1998','REF.WM.JOHNSON.1993','REF.WM.ECKER.2022'} else ('THEORETICAL' if ref['id']=='REF.WM.SPERBER.2010' else 'EXPERIMENTAL'),
      'checked_on':'2026-09-17','review_scope':'ABSTRACT_AND_SELECTED_SECTIONS'
    })
dump('model/references.json',references)

# Theory glossary: expand the existing world-model concept and register mechanism-level descriptors.
glossary=load('model/theory_glossary.json')
chapter_id='THEORY.16.WORLD_MODEL_CONSTRUCTION'
for item in glossary:
    if item['id']=='GLOSS.CONCEPT.WORLD_MODEL':
        item['short_definition']={'en':'Agent-relative, partial and revisable internal representation constructed from selected observations, prior information, memory, provenance/source cues, social context and uncertainty.','ro':'Reprezentare internă relativă la agent, parțială și revizuibilă, construită din observații selectate, informație anterioară, memorie, indicii de proveniență/sursă, context social și incertitudine.'}
        item['what_it_is_not']={'en':'External reality itself, a truth oracle, a complete neural predictive-coding implementation, or a population-calibrated belief model.','ro':'Nu este realitatea externă însăși, un oracol al adevărului, o implementare neuronală completă de predictive coding sau un model de convingere calibrat populațional.'}
        item['epistemic_status']=['EMPIRICAL','EXECUTABLE','CONCEPTUAL','INTERPRETIVE']
        if chapter_id not in item['related_chapters']: item['related_chapters'].append(chapter_id)

mechanisms=[
 ('GLOSS.MECH.WORLD_OBSERVE_SELECT','world-observe-select',{'en':'Observation and selection','ro':'Observare și selecție'},{'en':'Empirical/conceptual gate separating information availability from what is actually observed or encoded.','ro':'Poartă empirică/conceptuală care separă disponibilitatea informației de ceea ce este efectiv observat sau encodat.'},False,'MOD.14',['EMPIRICAL','CONCEPTUAL']),
 ('GLOSS.MECH.WORLD_PRIOR_MEMORY','world-prior-memory',{'en':'Prior and memory retrieval','ro':'Recuperarea informației anterioare și a memoriei'},{'en':'Task-dependent use of stored information and schemas during construction or revision of an internal representation.','ro':'Utilizarea dependentă de sarcină a informației stocate și a schemelor în construirea sau revizuirea reprezentării interne.'},False,'MOD.14',['EMPIRICAL','CONCEPTUAL']),
 ('GLOSS.MECH.WORLD_PROVENANCE_SOURCE','world-provenance-source',{'en':'Provenance and source evaluation','ro':'Evaluarea provenienței și a sursei'},{'en':'Source attribution and source-related evaluation kept distinct from objective reliability and from diagnostic likelihood ratios.','ro':'Atribuirea sursei și evaluarea legată de sursă, păstrate distincte de fiabilitatea obiectivă și de rapoartele de verosimilitate diagnostice.'},False,'MOD.14',['EMPIRICAL','CONCEPTUAL']),
 ('GLOSS.MECH.WORLD_SOCIAL_CONTEXT','world-social-context',{'en':'Social-context interpretation','ro':'Interpretarea contextului social'},{'en':'Interpretation of communicated information in social context without a generic conformity coefficient.','ro':'Interpretarea informației comunicate în context social fără un coeficient generic de conformism.'},False,'MOD.14',['EMPIRICAL','CONCEPTUAL']),
 ('GLOSS.MECH.WORLD_NORMATIVE_UPDATE','world-normative-update',{'en':'Normative proposition update','ro':'Actualizarea normativă a propoziției'},{'en':'Executable odds-form Bayesian reference update using an explicit prior and defensible diagnostic likelihood ratio.','ro':'Actualizare bayesiană executabilă de referință, în forma odds, folosind un prior explicit și un raport diagnostic justificabil.'},True,'#understanding/world-model',['EXECUTABLE']),
 ('GLOSS.MECH.WORLD_UNCERTAINTY','world-uncertainty',{'en':'Explicit proposition uncertainty','ro':'Incertitudine explicită a propoziției'},{'en':'Executable binary-entropy indicator derived from the normative proposition posterior.','ro':'Indicator executabil de entropie binară derivat din posteriorul normativ al propoziției.'},True,'#understanding/world-model',['EXECUTABLE','CONCEPTUAL']),
 ('GLOSS.MECH.WORLD_REASSESSMENT','world-reassessment',{'en':'Contradiction and reassessment','ro':'Contradicție și reevaluare'},{'en':'Revision pathway triggered by counterevidence, corrections or source reappraisal; descriptive dynamics remain task-specific.','ro':'Traseu de revizuire declanșat de dovezi contrare, corecții sau reevaluarea sursei; dinamica descriptivă rămâne specifică sarcinii.'},False,'MOD.14',['EMPIRICAL','CONCEPTUAL'])
]
for gid,token,label,definition,executable,target,status in mechanisms:
    append_unique(glossary,{'id':gid,'kind':'MECHANISM','token':token,'label':label,'short_definition':definition,'what_it_is_not':{'en':'A universal coefficient or population-calibrated law unless explicitly marked executable for the narrow normative reference.','ro':'Nu este un coeficient universal sau o lege calibrată populațional decât dacă este marcat explicit executabil pentru referința normativă îngustă.'},'epistemic_status':status,'executable':executable,'target':target,'related_chapters':[chapter_id]})
dump('model/theory_glossary.json',glossary)

# Dedicated bilingual Theory/Learn chapter with explicit links to existing constructs.
theory=load('model/theory_index.json')
chapter={
 'id':chapter_id,'order':16,
 'label':{'en':'World-model construction','ro':'Construirea modelului realității'},
 'summary':{'en':'Explains how an internal representation can be constructed and revised from selected information, prior/memory, provenance/source cues, social context and uncertainty while keeping empirical, executable, conceptual and interpretive levels separate.','ro':'Explică modul în care o reprezentare internă poate fi construită și revizuită din informație selectată, informație anterioară/memorie, indicii de proveniență/sursă, context social și incertitudine, separând nivelurile empiric, executabil, conceptual și interpretativ.'},
 'source_paths':{'en':'docs/theory/en/16-world-model-construction.md','ro':'docs/theory/ro/16-construirea-modelului-realitatii.md'},
 'prerequisites':['THEORY.01.WORLD_INFORMATION_REPRESENTATION'],
 'epistemic_status':['EMPIRICAL','EXECUTABLE','CONCEPTUAL','INTERPRETIVE'],
 'module_ids':['MOD.14'],
 'variable_ids':['VAR.WORLD.PRIOR','VAR.WORLD.LIKELIHOOD_RATIO','VAR.WORLD.POSTERIOR','VAR.WORLD.UNCERTAINTY','VAR.WORLD.PROVENANCE','VAR.EXPOSURE.COUNT','VAR.FAMILIARITY.CLAIM','VAR.CORRECTION.ACCESS','VAR.RELIABILITY.ESTIMATE','VAR.BELIEF.CLAIM','VAR.OBSERVED.SAMPLE.BALANCE','VAR.ISSUE.APPRAISAL','VAR.PREVIEW.IMPRESSION','VAR.ACCESS'],
 'mechanism_ids':['world-observe-select','world-prior-memory','world-provenance-source','world-social-context','world-normative-update','world-uncertainty','world-reassessment'],
 'validation_ids':[],
 'evidence_refs':[ref['id'] for ref in contract['references']],
 'sources':[{'role':'MODEL_EVIDENCE','ref':ref['id']} for ref in contract['references']]+[{'role':'BACKGROUND_THEORY','ref':'https://doi.org/10.1038/4580'}],
 'code_refs':[{'id':'mod14.bayes_update','path':'src/cognitive_epistemic_model/world_model.py','symbol':'bayes_update','language':'PYTHON','release_pin_required':True},{'id':'mod14.binary_uncertainty','path':'src/cognitive_epistemic_model/world_model.py','symbol':'binary_uncertainty','language':'PYTHON','release_pin_required':True}],
 'related_views':['learning','reference','process'],
 'anchors':['what-is-being-constructed','the-mechanism-loop','empirical-layer','executable-layer-a-narrow-normative-reference','why-pwm-is-not-b','sources-provenance-and-epistemic-vigilance','falsification-and-uncertainty','boundaries'],
 'what_it_does_not_claim':{'en':'MOD.14 does not claim a universal Bayesian brain, a complete neural world model, a truth oracle, population calibration, or identity between Pwm and the existing descriptive belief state B.','ro':'MOD.14 nu afirmă existența unui creier bayesian universal, a unui model neuronal complet al lumii, a unui oracol al adevărului, a calibrării populaționale sau a identității dintre Pwm și starea descriptivă existentă de convingere B.'}
}
append_unique(theory,chapter)
theory.sort(key=lambda item:item['order'])
dump('model/theory_index.json',theory)

# Export the MOD.14 contract to the static viewer.
replace('scripts/export_web.py','    (DEST / "interventions.json").write_text(\n','    (DEST / "world_model_v1.json").write_bytes(\n        (ROOT / "model" / "contracts" / "world_model_v1.json").read_bytes()\n    )\n\n    (DEST / "interventions.json").write_text(\n')
replace('web/scripts/sync-model.mjs',"copyFileSync(\n  fileURLToPath(new URL('model/contracts/decision_uncertainty_v1.json',root)),\n  fileURLToPath(new URL('decision_uncertainty.json',target))\n);\n","copyFileSync(\n  fileURLToPath(new URL('model/contracts/decision_uncertainty_v1.json',root)),\n  fileURLToPath(new URL('decision_uncertainty.json',target))\n);\ncopyFileSync(\n  fileURLToPath(new URL('model/contracts/world_model_v1.json',root)),\n  fileURLToPath(new URL('world_model_v1.json',target))\n);\n")

# Integrate the new mode without creating a second application shell.
replace('web/src/understanding.ts',"import {mountSuiteOverview} from './suite-overview';\nimport './suite-overview.css';\n","import {mountSuiteOverview} from './suite-overview';\nimport {mountWorldModel} from './world-model';\nimport './suite-overview.css';\nimport './world-model.css';\n")
replace('web/src/understanding.ts',"type Mode='overview'|'theory'|'mechanisms'|'tour'|'active';","type Mode='overview'|'theory'|'mechanisms'|'world-model'|'tour'|'active';")
replace('web/src/understanding.ts',"return {mode:['overview','theory','mechanisms','tour','active'].includes(mode)?mode:'overview',detail:parts[2]};","return {mode:['overview','theory','mechanisms','world-model','tour','active'].includes(mode)?mode:'overview',detail:parts[2]};")
replace('web/src/understanding.ts',"const knownModes:Mode[]=['overview','theory','mechanisms','tour','active'];","const knownModes:Mode[]=['overview','theory','mechanisms','world-model','tour','active'];")
replace('web/src/understanding.ts',"    <button type=\"button\" data-understanding-mode=\"mechanisms\" aria-pressed=\"${mode==='mechanisms'}\">${t('Mecanisme','Mechanisms')}</button>\n    <button type=\"button\" data-understanding-mode=\"tour\"", "    <button type=\"button\" data-understanding-mode=\"mechanisms\" aria-pressed=\"${mode==='mechanisms'}\">${t('Mecanisme','Mechanisms')}</button>\n    <button type=\"button\" data-understanding-mode=\"world-model\" aria-pressed=\"${mode==='world-model'}\">${t('Modelul realității','World model')}</button>\n    <button type=\"button\" data-understanding-mode=\"tour\"")
replace('web/src/understanding.ts'," if(mode==='active'){\n", " if(mode==='world-model'){\n  mountWorldModel(sub,lang,navigate).catch(error=>{\n   sub.innerHTML=`<div class=\"panel\"><h3>${t('MOD.14 nu poate fi încărcat','MOD.14 could not be loaded')}</h3><p>${String(error)}</p></div>`;\n  });\n  return;\n }\n\n if(mode==='active'){\n")

replace('web/src/suite-overview.ts',"openUnderstanding:(mode:'theory'|'mechanisms'|'tour'|'active')=>void;","openUnderstanding:(mode:'theory'|'mechanisms'|'world-model'|'tour'|'active')=>void;")
replace('web/src/suite-overview.ts',"      <button type=\"button\" class=\"cem-node\" data-suite-learn=\"mechanisms\"><strong>${t('Evaluare și acces','Evaluation & access')}</strong><small>Aissue · Paccess · Pengage</small></button>\n      <button type=\"button\" class=\"cem-node\" data-suite-learn=\"mechanisms\"><strong>${t('Convingere și acuratețe','Belief & accuracy')}</strong><small>B · W</small></button>","      <button type=\"button\" class=\"cem-node\" data-suite-learn=\"mechanisms\"><strong>${t('Evaluare și acces','Evaluation & access')}</strong><small>Aissue · Paccess · Pengage</small></button>\n      <button type=\"button\" class=\"cem-node\" data-suite-learn=\"world-model\"><strong>${t('Model intern și incertitudine','Internal model & uncertainty')}</strong><small>Pprior · LR → Pwm · Uwm</small></button>\n      <button type=\"button\" class=\"cem-node\" data-suite-learn=\"mechanisms\"><strong>${t('Convingere și acuratețe','Belief & accuracy')}</strong><small>B · W</small></button>")
replace('web/src/suite-overview.ts',"     <button type=\"button\" class=\"primary\" data-suite-learn=\"theory\">${t('Deschide teoria','Open theory')}</button>\n     <button type=\"button\" data-suite-learn=\"tour\">", "     <button type=\"button\" class=\"primary\" data-suite-learn=\"theory\">${t('Deschide teoria','Open theory')}</button>\n     <button type=\"button\" data-suite-learn=\"world-model\">${t('MOD.14 · Modelul realității','MOD.14 · World model')}</button>\n     <button type=\"button\" data-suite-learn=\"tour\">")
replace('web/src/suite-overview.ts',"button.dataset.suiteLearn as 'theory'|'mechanisms'|'tour'|'active'","button.dataset.suiteLearn as 'theory'|'mechanisms'|'world-model'|'tour'|'active'")

# Web test gate and existing frozen UI assumptions.
package=load('web/package.json')
package['scripts']['test:mod14']='node --test tests/world-model.test.ts'
package['scripts']['build']=package['scripts']['build'].replace('npm run test:oa7 &&','npm run test:oa7 && npm run test:mod14 &&')
dump('web/package.json',package)
replace('web/tests/suite-standard.test.ts',"type Mode='overview'\\|'theory'\\|'mechanisms'\\|'tour'\\|'active'","type Mode='overview'\\|'theory'\\|'mechanisms'\\|'world-model'\\|'tour'\\|'active'")
replace('web/scripts/smoke.mjs',"assert.equal(await page.locator('[data-understanding-mode]').count(),5);","assert.equal(await page.locator('[data-understanding-mode]').count(),6);")
replace('web/scripts/smoke.mjs',"assert.equal(await page.locator('[data-theory-chapter]').count(),16);","assert.equal(await page.locator('[data-theory-chapter]').count(),17);")

# Semantic compiler frozen coverage counts expand only through authoritative registries.
replace('tests/test_semantic_compiler.py','assert len(actual) == 114','assert len(actual) == 133')
replace('tests/test_semantic_compiler.py','assert len(documentation) == 162','assert len(documentation) == 199')
replace('tests/test_semantic_compiler.py','"DOCUMENTATION_RELATION": 162,','"DOCUMENTATION_RELATION": 199,')
replace('tests/test_semantic_compiler.py','assert len(index["relations"]) == 189','assert len(index["relations"]) == 226')
