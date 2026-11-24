"""Validate content, reader feedback and optionally render in actual Student108."""
import json, sys, re, os, argparse
from pathlib import Path
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

parser=argparse.ArgumentParser()
parser.add_argument('--workspace',type=Path,required=True)
parser.add_argument('--render',action='store_true')
parser.add_argument('--local-images',action='store_true',help='Preview local SVG bytes before publication; do not change the deliverable JSON.')
args=parser.parse_args()
sys.path[:0]=[str(args.workspace/'work/new-systems/qt-runtime'),str(args.workspace/'work/student108-current'),str(args.workspace/'work/Teacher108-feedback')]
from student108.mission import validate_mission
from teacher108.mission import validate_mission as teacher_validate
from student108.model import Attempt
from build import DATA
folder=Path(__file__).resolve().parent.parent
m=json.loads((folder/'small-network.mission.json').read_text(encoding='utf-8'))
assert validate_mission(m)==m and teacher_validate(m)==m
steps=m['mission_content']['steps']
assert len(steps)==48
assert not {'packet','packet-check','header','header-check','second-level','second-level-check','subdomain','subdomain-check'} & {s['id'] for s in steps}
assert [s['id'] for s in steps if s['step_content']['type']=='information']==['intro']+[row[0] for row in DATA]+['summary']
assert sum(bool(s['step_rules'].get('ai_feedback')) for s in steps)==1
assert not any(s['step_content']['type']=='file' for s in steps)
class Body(HTMLParser):
    def __init__(self):super().__init__();self.tags=[];self.images=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag not in {'meta','img','br','hr','link','input'}:self.tags.append(tag)
        if tag=='img':assert a.get('alt');self.images.append(a['src'])
        if tag=='a':self.links.append(a.get('href',''))
    def handle_endtag(self,tag):assert self.tags.pop()==tag
for i,s in enumerate(steps):
    c=s['step_content'];p=Body();p.feed(c['instruction']);assert not p.tags
    assert not re.search(r'<h[12]\b',c['instruction'])
    if c['type']=='information':
        assert len(p.images)==(2 if s['id']=='tld' else 1)
        for src in p.images:
            assert src.startswith('https://raw.githubusercontent.com/') and src in p.links
            ET.parse(folder/'images'/Path(src).name)
    if c['type']=='multiple_choice':
        assert steps[i-1]['step_content']['type']=='information'
        assert len(c['options'])==6 and len(c['correct_option_ids'])==2
        good=c['correct_option_ids'];wrong=next(o['id'] for o in c['options'] if o['id'] not in good)
        for answer,expected in [(good,True),(good[:-1],False),(good+[wrong],False)]:
            a=Attempt(m,{'id':'qa'});a.current=i;a.submit(s['id'],answer);a.check_feedback()
            result=a.feedback_for(s['id']);assert result['correct']==expected and result['explanation']==c['feedback']
    if c['type']=='open_answer':assert c['instruction'].count('?')==1 and c['reference_answer'] and s['step_rules']['ai_feedback']
assert steps[-1]['step_content']['instruction'].count('<li>')==5
print('PASS: both models; 48 steps; 26 SVGs; 66 choice-feedback cases; one AI question; separate domain diagrams; no practical/file tasks.',flush=True)
if not args.render:sys.exit()
if args.local_images:
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    from functools import partial
    from threading import Thread
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(folder)))
    Thread(target=server.serve_forever,daemon=True).start()
    for s in steps:
        c=s['step_content']
        def embed(match):
            return f'src="http://127.0.0.1:{server.server_port}/images/{match.group(1)}"'
        c['instruction']=re.sub(r'src="https://raw.githubusercontent.com/[^\"]+/images/([^\"]+)"',embed,c['instruction'])
os.environ['QT_QPA_PLATFORM']='offscreen'
os.environ['QTWEBENGINE_CHROMIUM_FLAGS']='--disable-gpu --no-sandbox'
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from student108.preview import PreviewWindow
out=args.workspace/'work/network-qa';out.mkdir(exist_ok=True)
app=QApplication([]);w=PreviewWindow(out/'session');w.resize(1180,1000);w.show();w.accept_mission(m)
state={'index':0,'poll':0};results=[]
def advance():
    if state['index']==len(steps):app.quit();return
    state['poll']=0;w.render(state['index']);QTimer.singleShot(600,inspect)
def inspect():
    views=w.findChildren(QWebEngineView)
    views[0].page().runJavaScript("JSON.stringify({text:document.body.innerText,frames:Array.from(document.querySelectorAll('iframe.lesson-html')).map(f=>({height:f.clientHeight,bodyHeight:f.contentDocument.body.scrollHeight,width:f.contentDocument.body.scrollWidth,viewport:f.contentDocument.documentElement.clientWidth,images:Array.from(f.contentDocument.images).map(i=>({src:i.src,width:i.naturalWidth,complete:i.complete}))}))})",got)
def got(raw):
    r=json.loads(raw or '{}');images=[im for f in r.get('frames',[]) for im in f['images']]
    if (not r.get('text') or any(not im['complete'] or im['width']==0 for im in images)) and state['poll']<12:
        state['poll']+=1;QTimer.singleShot(500,inspect);return
    idx=state['index'];results.append({'id':steps[idx]['id'],**r})
    if steps[idx]['id'] in ['intro','smtp','ipv4','ipv6','mask','tld','cctld','url','url-answer','summary']:w.grab().save(str(out/(steps[idx]['id']+'.png')))
    print('Rendered',steps[idx]['id'],[(im['width'],im['complete']) for im in images],flush=True)
    state['index']+=1;QTimer.singleShot(0,advance)
QTimer.singleShot(500,advance);QTimer.singleShot(300000,app.quit);app.exec()
(out/'render.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(results)==len(steps)
assert all(r.get('frames') and len(r['frames'][0]['images'])==(2 if s['id']=='tld' else 1) for r,s in zip(results,steps) if s['step_content']['type']=='information')
assert all(im['width']>0 for r in results for f in r['frames'] for im in f['images'])
assert all(f['width']<=f['viewport']+2 and f['height']>=f['bodyHeight']-2 for r in results for f in r['frames'])
print('PASS: actual Student108 rendered all steps; '+('local illustration bytes' if args.local_images else 'external illustrations')+' loaded; no clipping.',flush=True)
