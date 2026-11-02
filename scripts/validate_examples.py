"""Check documentation examples against the actual Student108/Teacher108 models."""
import argparse
import json
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--student-repo', type=Path, default=ROOT.parent / 'Student108')
    parser.add_argument('--teacher-repo', type=Path, default=ROOT.parent / 'Teacher108')
    args = parser.parse_args()
    for path, package in ((args.student_repo, 'student108'), (args.teacher_repo, 'teacher108')):
        if not (path / package).is_dir():
            parser.error(f'Missing source checkout: {path}')
        sys.path.insert(0, str(path.resolve()))
    from student108.mission import validate_mission as student_validate
    from teacher108.mission import validate_mission as teacher_validate
    from teacher108.templates import TemplateStore, validate_content

    library = read(ROOT / 'examples/step-content-library.json')
    content = {row['id']: row['step_content'] for row in library}
    assert len(content) == len(library), 'Duplicate library IDs'
    for cid, value in content.items():
        assert type(cid) is int and cid > 0
        assert validate_content(value) == value

    templates = sorted((ROOT / 'examples/templates').glob('*.json'))
    with tempfile.TemporaryDirectory(prefix='learn108-examples-') as directory:
        store = TemplateStore(Path(directory) / 'templates.sqlite3', teacher_id=1)
        mapped = {cid: store.save_content(value) for cid, value in content.items()}
        for path in templates:
            template = read(path)
            for step in template['steps']:
                step['variants'] = [mapped[cid] for cid in step['variants']]
            identifier = store.save(template)
            restored = store.load(identifier)
            assert {key: restored[key] for key in template} == template, path

    missions = sorted((ROOT / 'examples/missions').glob('*.json'))
    for path in missions:
        mission = read(path)
        assert student_validate(mission) == mission, path
        assert teacher_validate(mission) == mission, path
        for step in mission['mission_content']['steps']:
            if 'step_content_id' in step:
                assert step['step_content'] == content[step['step_content_id']], path

    # The two derived examples retain the template order and use allowed variants.
    template = read(ROOT / 'examples/templates/hardware-software.json')
    assert len(template['steps'][0]['variants']) * len(template['steps'][1]['variants']) == 30
    for name in ('hardware-software-a.json', 'hardware-software-b.json'):
        mission = read(ROOT / 'examples/missions' / name)
        assert len(mission['mission_content']['steps']) == len(template['steps'])
        for step, source in zip(mission['mission_content']['steps'], template['steps']):
            assert step['step_content_id'] in source['variants']
    a = read(ROOT / 'examples/missions/hardware-software-a.json')
    assert a['mission_rules'] == template['mission_rules']
    assert [s['step_rules'] for s in a['mission_content']['steps']] == [s['step_rules'] for s in template['steps']]

    snippets = links = 0
    for path in ROOT.rglob('*.md'):
        text = path.read_text(encoding='utf-8')
        for match in re.finditer(r'```json\s*\n(.*?)\n```', text, re.S):
            value = json.loads(match[1])
            if isinstance(value, dict) and value.get('schema_version') == 4:
                student_validate(value)
                teacher_validate(value)
            snippets += 1
        for target in re.findall(r'\]\(([^)]+)\)', text):
            url = urlsplit(target)
            if not url.scheme and url.path:
                assert (path.parent / unquote(url.path)).resolve().is_file(), (path, target)
                links += 1
    print(f'OK: {len(content)} library entries, {len(templates)} template roundtrips, '
          f'{len(missions)} missions in both validators, {snippets} JSON snippets, {links} local links.')


if __name__ == '__main__':
    main()
