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
    parser.add_argument('--json-schema', action='store_true', help='Also check the published JSON Schema (requires jsonschema).')
    args = parser.parse_args()
    for path, package in ((args.student_repo, 'student108'), (args.teacher_repo, 'teacher108')):
        if not (path / package).is_dir():
            parser.error(f'Missing source checkout: {path}')
        sys.path.insert(0, str(path.resolve()))
    from student108.mission import validate_mission as student_validate
    from teacher108.mission import validate_mission as teacher_validate
    from teacher108.templates import TemplateStore, validate_content
    from teacher108.template_import import parse_template_json, validate_template
    schema_validator = None
    if args.json_schema:
        from jsonschema import Draft202012Validator
        schema = read(ROOT / 'schemas/mission-template-v1.schema.json')
        Draft202012Validator.check_schema(schema)
        schema_validator = Draft202012Validator(schema)

    library = read(ROOT / 'examples/step-content-library.json')
    content = {row['id']: row['step_content'] for row in library}
    assert len(content) == len(library), 'Duplicate library IDs'
    for cid, value in content.items():
        assert type(cid) is int and cid > 0
        assert validate_content(value) == value

    templates = sorted((ROOT / 'examples/templates').glob('*.json'))
    with tempfile.TemporaryDirectory(prefix='learn108-examples-') as directory:
        store = TemplateStore(Path(directory) / 'templates.sqlite3', teacher_id=1)
        for path in templates:
            if schema_validator:
                schema_validator.validate(read(path))
            template = parse_template_json(path.read_text(encoding='utf-8'))
            source_text = path.read_text(encoding='utf-8')
            identifier = store.import_template(template, source=source_text)
            if template['template_type'] == 'millionaire':
                assert store.load_document(identifier)['document'] == source_text, path
                continue
            restored = store.load(identifier)
            for key in ('template_type', 'title', 'description', 'class_name', 'subject', 'category', 'lesson', 'mission_rules'):
                assert restored[key] == template[key], (path, key)
            source = {row['id']: row['step_content'] for row in template['step_contents']}
            for old, new in zip(template['steps'], restored['steps']):
                assert old['title'] == new['title'] and old['step_rules'] == new['step_rules'], path
                for old_id, new_id in zip(old['variants'], new['variants']):
                    assert store.content(new_id)['content'] == source[old_id], path

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
            if isinstance(value, dict) and value.get('mission_version') == 4:
                student_validate(value)
                teacher_validate(value)
            if isinstance(value, dict) and value.get('template_version') == 1:
                validate_template(value)
                if schema_validator:
                    schema_validator.validate(value)
            snippets += 1
        for target in re.findall(r'\]\(([^)]+)\)', text):
            url = urlsplit(target)
            if not url.scheme and url.path:
                assert (path.parent / unquote(url.path)).resolve().is_file(), (path, target)
                links += 1
    print(f'OK: {len(content)} library entries, {len(templates)} template roundtrips, '
          f'{len(missions)} missions in both validators, {snippets} JSON snippets, {links} local links.')
    if schema_validator:
        print('JSON Schema Draft 2020-12 and all portable templates also passed.')


if __name__ == '__main__':
    main()
