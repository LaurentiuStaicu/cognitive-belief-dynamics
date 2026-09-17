from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Keep MOD.14-owned normative quantities inside its dedicated contract so the
# frozen OA-6E/R7 scientific variable registry remains byte-for-byte unchanged.
contract_path = ROOT / 'model/contracts/world_model_v1.json'
contract = json.loads(contract_path.read_text(encoding='utf-8'))
id_map = {
    'WM.VAR.PRIOR': 'VAR.WORLD.PRIOR',
    'WM.VAR.LR': 'VAR.WORLD.LIKELIHOOD_RATIO',
    'WM.VAR.POSTERIOR': 'VAR.WORLD.POSTERIOR',
    'WM.VAR.UNCERTAINTY': 'VAR.WORLD.UNCERTAINTY',
    'WM.VAR.PROVENANCE': 'VAR.WORLD.PROVENANCE',
}
for item in contract['variables']:
    item['id'] = id_map.get(item['id'], item['id'])
    if item['id'] == 'VAR.WORLD.LIKELIHOOD_RATIO':
        item.pop('range', None)
for relation in contract['relations']:
    relation['source'] = id_map.get(relation['source'], relation['source'])
    relation['target'] = id_map.get(relation['target'], relation['target'])
contract_path.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

schema_path = ROOT / 'schemas/world_model.schema.json'
schema = schema_path.read_text(encoding='utf-8')
schema = schema.replace('^WM\\\\.VAR\\\\.', '^VAR\\\\.WORLD\\\\.')
schema_path.write_text(schema, encoding='utf-8')

# Project contract variables into the Semantic Spine without mutating the
# legacy/frozen model/variables.json registry.
semantic_path = ROOT / 'src/cognitive_epistemic_model/semantic.py'
semantic = semantic_path.read_text(encoding='utf-8')
load_anchor = '    variables = _load(model_dir / "variables.json")\n'
load_insert = load_anchor + '    world_model = _load(model_dir / "contracts" / "world_model_v1.json")\n'
if 'world_model = _load(model_dir / "contracts" / "world_model_v1.json")' not in semantic:
    semantic = semantic.replace(load_anchor, load_insert)

loop_anchor = '    for item in computational["extra_nodes"]:\n'
world_loop = '''    for item in world_model["variables"]:\n        entity: dict[str, Any] = {\n            "id": item["id"],\n            "semantic_type": "VARIABLE",\n            "labels": _labels(\n                item["label"],\n                alternative={"und": [item["short_name"]]},\n            ),\n            "source": _source(\n                "model/contracts/world_model_v1.json",\n                item["id"],\n            ),\n            "short_name": item["short_name"],\n            "summary": {"en": item["definition"]},\n            "related_ids": ["MOD.14"],\n            "status_facets": {"source_tags": item["status"]},\n        }\n        entities.append(entity)\n\n'''
if 'for item in world_model["variables"]:' not in semantic:
    semantic = semantic.replace(loop_anchor, world_loop + loop_anchor)

source_anchor = '                "model/contracts/oa0_optimization_baseline.json",\n'
source_insert = source_anchor + '                "model/contracts/world_model_v1.json",\n'
if '                "model/contracts/world_model_v1.json",\n' not in semantic:
    semantic = semantic.replace(source_anchor, source_insert)
semantic_path.write_text(semantic, encoding='utf-8')

# Keep semantic coverage tests authoritative across both the frozen base registry
# and MOD.14's scoped contract registry.
semantic_test_path = ROOT / 'tests/test_semantic_compiler.py'
semantic_test = semantic_test_path.read_text(encoding='utf-8')
expected_anchor = '''    expected |= {\n        item["semantic_id"]\n        for item in load(MODEL / "computational_dependencies.json")["extra_nodes"]\n    }\n\n'''
expected_insert = expected_anchor + '''    expected |= {\n        item["id"]\n        for item in load(MODEL / "contracts" / "world_model_v1.json")["variables"]\n    }\n\n'''
if 'load(MODEL / "contracts" / "world_model_v1.json")["variables"]' not in semantic_test:
    semantic_test = semantic_test.replace(expected_anchor, expected_insert)
semantic_test_path.write_text(semantic_test, encoding='utf-8')

# Enforce the architectural boundary explicitly in MOD.14's own tests.
contract_test_path = ROOT / 'tests/test_world_model_contract.py'
contract_test = contract_test_path.read_text(encoding='utf-8')
boundary_test = '''\n\ndef test_world_model_variables_live_in_scoped_contract_not_frozen_r7_registry():\n    central_ids = {item["id"] for item in load(ROOT / "model" / "variables.json")}\n    contract_ids = {item["id"] for item in load(CONTRACT)["variables"]}\n    expected = {\n        "VAR.WORLD.PRIOR",\n        "VAR.WORLD.LIKELIHOOD_RATIO",\n        "VAR.WORLD.POSTERIOR",\n        "VAR.WORLD.UNCERTAINTY",\n        "VAR.WORLD.PROVENANCE",\n    }\n    assert contract_ids == expected\n    assert not (expected & central_ids)\n'''
if 'test_world_model_variables_live_in_scoped_contract_not_frozen_r7_registry' not in contract_test:
    contract_test += boundary_test
contract_test_path.write_text(contract_test, encoding='utf-8')

# Browser reference operator must reject invalid priors rather than silently clamp.
ui_path = ROOT / 'web/src/world-model.ts'
ui = ui_path.read_text(encoding='utf-8')
ui = ui.replace("const clamp=(value:number,min:number,max:number)=>Math.min(max,Math.max(min,value));\n", "")
ui = ui.replace("const p=clamp(Number(priorInput.value),0,1);", "const p=Number(priorInput.value);")
ui = ui.replace(
    "LR must be finite and strictly positive. The operator fails closed.",
    "Prior must be within [0,1] and LR must be finite and strictly positive. The operator fails closed.",
)
ui = ui.replace(
    "LR trebuie să fie finit și strict pozitiv. Operatorul eșuează închis.",
    "Priorul trebuie să fie în [0,1], iar LR trebuie să fie finit și strict pozitiv. Operatorul eșuează închis.",
)
ui_path.write_text(ui, encoding='utf-8')

# Normalize a duplicate one-shot test insertion from the temporary integration helper.
package_path = ROOT / 'web/package.json'
package = json.loads(package_path.read_text(encoding='utf-8'))
build = package['scripts']['build']
while 'npm run test:mod14 && npm run test:mod14 &&' in build:
    build = build.replace('npm run test:mod14 && npm run test:mod14 &&', 'npm run test:mod14 &&')
package['scripts']['build'] = build
package_path.write_text(json.dumps(package, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
