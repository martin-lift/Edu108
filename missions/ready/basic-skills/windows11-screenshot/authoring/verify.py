"""Validate the mission and exercise file attachment in the real Student108 reader."""
import base64
import hashlib
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
WORK = next(p / 'work' for p in HERE.parents if (p / 'work/student108-current').is_dir())
OUT = WORK / 'screenshot-qa'
OUT.mkdir(exist_ok=True)
sys.path[:0] = [str(WORK / 'new-systems/qt-runtime'), str(WORK / 'student108-current'), str(WORK / 'Teacher108-feedback')]
from student108.mission import validate_mission
from teacher108.mission import validate_mission as teacher_validate
from student108.model import Attempt

m = json.loads((HERE.parent / 'windows11-screenshot.mission.json').read_text(encoding='utf-8'))
validate_mission(m)
teacher_validate(m)
content = m['mission_content']
steps = content['steps']
assert content['category'] == 'Базови умения'
assert not any(key in content for key in ('class_name', 'lesson', 'subject'))
assert content['title'] == 'Екранна снимка (Screenshot) в Windows 11 — заснемане и записване'
assert steps[0]['step_content']['title'] == 'За какво е този урок'
assert [s['step_content']['type'] for s in steps] == ['information'] * 7 + ['file']
assert all(not s['step_rules'].get('ai_feedback') and not s['step_rules'].get('automatic_feedback') for s in steps)
assert steps[-1]['step_rules']['send_progress']
assert all('options' not in s['step_content'] and 'reference_answer' not in s['step_content'] for s in steps)

fixture = OUT / 'moqt-screenshot.png'
fixture.write_bytes(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII='))
a = Attempt(m, {'id': 'qa', 'name': 'QA'})
a.current = len(steps) - 1
a.attach('submit-image', fixture)
value = a.submissions['submit-image']['value']
assert value['filename'] == fixture.name
assert base64.b64decode(value['content']) == fixture.read_bytes()
assert value['sha256'] == hashlib.sha256(fixture.read_bytes()).hexdigest()
restored = Attempt.restore(a.snapshot(completed=True), {'id': 'qa', 'name': 'QA'})
assert restored.submissions['submit-image']['value'] == value
print('PASS: both schemas; category; no class/lesson; 7 information + final file; no checks; attachment bytes and restoration.', flush=True)

if '--render' not in sys.argv:
    sys.exit()

os.environ['QT_QPA_PLATFORM'] = 'offscreen'
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu --no-sandbox'
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from student108.preview import PreviewWindow

app = QApplication([])
w = PreviewWindow(OUT / 'session')
w.resize(1300, 1020)
w.show()
w.accept_mission(m)
state = {'index': 0, 'poll': 0, 'settled': False}
results = []


def advance():
    if state['index'] == len(steps):
        (OUT / 'render.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
        app.quit()
        return
    state['poll'] = 0
    state['settled'] = False
    w.render(state['index'])
    if state['index'] == len(steps) - 1:
        original = QFileDialog.getOpenFileName
        QFileDialog.getOpenFileName = lambda *args, **kwargs: (str(fixture), '')
        try:
            w.attach_file()
        finally:
            QFileDialog.getOpenFileName = original
    QTimer.singleShot(700, inspect)


def inspect():
    w.findChildren(QWebEngineView)[0].page().runJavaScript("JSON.stringify({text:document.body.innerText,check:!!document.getElementById('check-answer'),filename:document.getElementById('filename')?.textContent,frames:Array.from(document.querySelectorAll('iframe.lesson-html')).map(f=>({height:f.clientHeight,bodyHeight:f.contentDocument.body.scrollHeight,width:f.contentDocument.body.scrollWidth,viewport:f.contentDocument.documentElement.clientWidth,images:Array.from(f.contentDocument.images).map(i=>({url:i.src,width:i.naturalWidth,complete:i.complete}))}))})", got)


def got(raw):
    result = json.loads(raw or '{}')
    images = [im for f in result.get('frames', []) for im in f['images']]
    if (not result.get('text') or any(not im['complete'] for im in images)) and state['poll'] < 25:
        state['poll'] += 1
        QTimer.singleShot(700, inspect)
        return
    if not state['settled']:
        state['settled'] = True
        QTimer.singleShot(900, inspect)
        return
    index = state['index']
    w.grab().save(str(OUT / f'step-{index:02}.png'))
    if index == 0:
        w.grab().save(str(fixture))
    assert not result['check']
    if index == len(steps) - 1:
        assert fixture.name in result['filename']
        assert 'Завърши мисията' in w.next_button.text()
        attached = w.attempt.submissions['submit-image']['value']
        assert base64.b64decode(attached['content']) == fixture.read_bytes()
        assert Attempt.restore(w.attempt.snapshot(), w.student).submissions['submit-image']['value'] == attached
    results.append({'id': steps[index]['id'], **result})
    print('Rendered', steps[index]['id'], 'images', [(i['width'], i['complete']) for i in images], flush=True)
    state['index'] += 1
    QTimer.singleShot(0, advance)


QTimer.singleShot(500, advance)
QTimer.singleShot(180000, app.quit)
app.exec()
assert len(results) == len(steps)
assert all(i['width'] > 0 for r in results for f in r['frames'] for i in f['images'])
assert all(f['width'] <= f['viewport'] + 2 and f['height'] >= f['bodyHeight'] - 2 for r in results for f in r['frames'])
print('PASS: all steps in Student108; external image loaded; no overflow; file selected through actual attachment handler and restored.', flush=True)
