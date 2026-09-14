import json
from pathlib import Path
import tomllib
from cognitive_epistemic_model import __version__

ROOT = Path(__file__).resolve().parents[1]


def test_release_versions_are_consistent():
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text())
    assert 'version' in project['project']['dynamic']
    assert project['tool']['hatch']['version']['path'] == 'src/cognitive_epistemic_model/__init__.py'
    npm = __version__.replace('a', '-alpha.')
    assert json.loads((ROOT / 'web/package.json').read_text())['version'] == npm
    lock = json.loads((ROOT / 'web/package-lock.json').read_text())
    assert lock['version'] == lock['packages']['']['version'] == npm
    version = json.loads((ROOT / 'web/public/model/version.json').read_text())
    assert version['version'] == __version__
    assert version['release_tag'] == 'v' + __version__
    for name in ['runs', 'interventions', 'explanations']:
        assert json.loads((ROOT / f'web/public/model/{name}.json').read_text())['model_version'] == __version__
    assert f'Alpha {__version__}' in (ROOT / 'README.md').read_text()
    assert (ROOT / f'releases/v{__version__}.md').is_file()
    assert (ROOT / 'LICENSE').is_file()
    assert (ROOT / 'LICENSES/CC-BY-4.0.txt').is_file()
