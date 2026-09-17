from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

variables_path=ROOT/'model/variables.json'
variables=json.loads(variables_path.read_text(encoding='utf-8'))
for item in variables:
    if item.get('id')=='VAR.WORLD.LIKELIHOOD_RATIO':
        item.pop('range',None)
variables_path.write_text(json.dumps(variables,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

ui_path=ROOT/'web/src/world-model.ts'
ui=ui_path.read_text(encoding='utf-8')
ui=ui.replace("const clamp=(value:number,min:number,max:number)=>Math.min(max,Math.max(min,value));\n","")
ui=ui.replace("const p=clamp(Number(priorInput.value),0,1);","const p=Number(priorInput.value);")
ui=ui.replace("LR must be finite and strictly positive. The operator fails closed.","Prior must be within [0,1] and LR must be finite and strictly positive. The operator fails closed.")
ui=ui.replace("LR trebuie să fie finit și strict pozitiv. Operatorul eșuează închis.","Priorul trebuie să fie în [0,1], iar LR trebuie să fie finit și strict pozitiv. Operatorul eșuează închis.")
ui_path.write_text(ui,encoding='utf-8')
