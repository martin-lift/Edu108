import sys, os, json, re, base64, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[7]/'work'
MISSION=Path(__file__).resolve().parent.parent/'mobile-devices.mission.json'
OUT=ROOT/'mobile-qa';OUT.mkdir(exist_ok=True)
sys.path[:0]=[str(ROOT/'new-systems/qt-runtime'),str(ROOT/'student108-current'),str(ROOT/'Teacher108-feedback')]
from student108.mission import validate_mission
from teacher108.mission import validate_mission as tv
from student108.model import Attempt
m=json.loads(MISSION.read_text(encoding='utf-8'));validate_mission(m);tv(m)
steps=m['mission_content']['steps']
assert [s['id'] for s in steps[:2]]==['intro','mobile-devices']
assert steps[-1]['id']=='summary'
assert sum(bool(s['step_rules'].get('ai_feedback')) for s in steps)==1
assert steps[-1]['step_content']['instruction'].count('<li>')<=5
counts={}
for i,s in enumerate(steps):
 c=s['step_content'];kind=c['type'];counts[kind]=counts.get(kind,0)+1
 if kind=='information':assert '<img ' in c['instruction']
 if kind=='multiple_choice':
  prev=steps[i-1]['step_content'];assert prev['type']=='information'
  text=re.sub('<style>.*?</style>','',prev['instruction'],flags=re.S)
  assert len(re.findall(r'\w+',re.sub('<[^>]*>',' ',text)))>=50
  assert len(c['options'])==6 and 1<len(c['correct_option_ids'])<6
  good=c['correct_option_ids'];wrong=next(x['id'] for x in c['options'] if x['id'] not in good)
  for answer,expected in [(good,True),(good[:-1],False),(good+[wrong],False)]:
   a=Attempt(m,{'id':'qa','name':'QA'});a.current=i;a.submit(s['id'],answer);a.check_feedback()
   f=a.feedback_for(s['id']);assert f['correct']==expected and f['explanation']
 if kind=='open_answer':
  assert c['instruction'].count('?')==1 and c['reference_answer']
  assert s['step_rules']['send_progress']
  if s['step_rules'].get('ai_feedback'):
   assert not s['step_rules']['automatic_feedback']
  else:
   assert s['step_rules']['automatic_feedback']
   a=Attempt(m,{'id':'qa','name':'QA'});a.current=i;a.submit(s['id'],'Пробен отговор със свои думи.');a.check_feedback()
   assert a.feedback_for(s['id'])['reference_answer']==c['reference_answer']
print('PASS: Student + Teacher schemas, order, illustrations, choices and AI configuration:',counts,flush=True)
assert not any(s['step_content']['type']=='file' for s in steps)
assert 'OneDrive' not in json.dumps(m,ensure_ascii=False)
print('PASS: one question per open answer; every step illustrated.',flush=True)
assert all('<img ' in s['step_content']['instruction'] for s in steps)
a=Attempt(m,{'id':'qa','name':'QA'});a.current=next(i for i,s in enumerate(steps) if s['id']=='os-answer')
a.submit('os-answer','Android е при 6 от 10 устройства в примерната група.')
assert Attempt.restore(a.snapshot(),{'id':'qa','name':'QA'}).submissions['os-answer']['value']==a.submissions['os-answer']['value']
if '--render' not in sys.argv:sys.exit()
os.environ['QT_QPA_PLATFORM']='offscreen'
os.environ['QTWEBENGINE_CHROMIUM_FLAGS']='--disable-gpu --no-sandbox'
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from student108.preview import PreviewWindow
app=QApplication([]);w=PreviewWindow(OUT/'session');w.resize(1300,1020);w.show();w.accept_mission(m)
samples=list(range(len(steps)));state={'n':0,'poll':0};results=[]

def advance():
 if state['n']==len(samples):
  (OUT/'render.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');QTimer.singleShot(0,app.quit);return
 state['poll']=0;state['settled']=False;w.render(samples[state['n']]);QTimer.singleShot(700,inspect)
def inspect():
 views=w.findChildren(QWebEngineView)
 views[0].page().runJavaScript("JSON.stringify({frames:Array.from(document.querySelectorAll('iframe.lesson-html')).map(f=>({height:f.clientHeight,bodyHeight:f.contentDocument.body.scrollHeight,width:f.contentDocument.body.scrollWidth,viewport:f.contentDocument.documentElement.clientWidth,images:Array.from(f.contentDocument.images).map(i=>({src:i.src,width:i.naturalWidth,complete:i.complete}))})),text:document.body.innerText})",got)
def got(raw):
 result=json.loads(raw or '{}');imgs=[im for f in result.get('frames',[]) for im in f['images']]
 if (not result.get('text') or any(not im['complete'] for im in imgs)) and state['poll']<20:
  state['poll']+=1;QTimer.singleShot(700,inspect);return
 if not state['settled']:
  state['settled']=True;QTimer.singleShot(900,inspect);return
 idx=samples[state['n']];w.grab().save(str(OUT/f'step-{idx:02}.png'))
 results.append({'id':steps[idx]['id'],'kind':steps[idx]['step_content']['type'],**result})
 print('Rendered',idx+1,steps[idx]['id'],'images',[(im['width'],im['complete']) for im in imgs],flush=True)
 state['n']+=1;QTimer.singleShot(0,advance)
QTimer.singleShot(500,advance);QTimer.singleShot(600000,app.quit);app.exec()
assert len(results)==len(samples)
assert all(im['width']>0 for r in results for f in r['frames'] for im in f['images'])
assert all(f['width']<=f['viewport']+2 for r in results for f in r['frames'])
assert all(f['height']>=f['bodyHeight']-2 for r in results for f in r['frames'])
print('PASS: actual Student108 renderer, every step; all external images loaded; no horizontal overflow.',flush=True)
