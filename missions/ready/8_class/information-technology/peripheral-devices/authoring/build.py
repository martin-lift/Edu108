"""Rebuild the standard lesson mission, preserving its UUID and external image URLs."""
from pathlib import Path
import html
import json

ROOT = Path(__file__).resolve().parent.parent
IMAGES = json.loads((ROOT/'authoring/images.json').read_text('utf-8'))
STEPS = []
ASSETS = 'https://raw.githubusercontent.com/martin-lift/Edu108/main/missions/ready/8_class/information-technology/peripheral-devices/assets/'
CSS = '''body{font:19px/1.65 Arial,"Segoe UI",sans-serif;color:#20354c;background:#fff;margin:0;padding:24px;max-width:960px;box-sizing:border-box}p{margin:16px 0}h3{font-size:24px;color:#126a80;margin:24px 0 10px}strong{color:#145b72}li{margin:9px 0}figure{margin:20px 0;padding:14px;background:#f1f7fa;border:1px solid #dce7ee;border-radius:14px;text-align:center}figure img{display:block;max-width:100%;width:auto;height:auto;max-height:360px;margin:auto;object-fit:contain}figcaption{font-size:13px;line-height:1.5;color:#52687d;margin-top:10px}.gallery{display:flex;flex-wrap:wrap;gap:14px}.gallery figure{flex:1 1 260px;min-width:0;margin:0}.gallery img{max-height:280px}.diagram img{width:100%;max-height:none}.key,.example{padding:16px 20px;border-radius:9px;margin:20px 0}.key{background:#e7f5ef;border-left:5px solid #269378}.example{background:#fff3db;border-left:5px solid #e4ad3b}table{width:100%;border-collapse:collapse;font-size:17px}td,th{border:1px solid #c9dce5;padding:11px;text-align:left;vertical-align:top}th{background:#e6f0f6}a{color:#126797;overflow-wrap:anywhere}@media(max-width:550px){body{padding:14px}td,th{font-size:15px;padding:7px}}'''

def wrap(body):
    return '<!doctype html><html lang="bg"><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+body+'</body></html>'

def picture(key):
    im=IMAGES[key]
    credit=''
    if im['license'].lower() not in ('public domain','cc0'):
        credit=' · '+html.escape(im['author'])+' · <a href="'+html.escape(im['source'],quote=True)+'">източник</a> · <a href="'+html.escape(im['license_url'],quote=True)+'">'+html.escape(im['license'])+'</a>'
    return '<figure><img src="'+html.escape(im['url'],quote=True)+'" alt="'+html.escape(im['caption'],quote=True)+'"><figcaption>'+html.escape(im['caption'])+credit+'</figcaption></figure>'

def gallery(*keys):
    return '<div class="gallery">'+''.join(picture(k) for k in keys)+'</div>'

def diagram(name,caption):
    return '<figure class="diagram"><img src="'+ASSETS+name+'.svg" alt="'+html.escape(caption,quote=True)+'"><figcaption>'+caption+'</figcaption></figure>'

def info(sid,title,body):
    STEPS.append({'id':sid,'step_content':{'type':'information','title':title,'instruction':wrap(body),'instruction_format':'html'},'step_rules':{}})

def choice(sid,question,options,correct,feedback):
    assert len(options)==6 and 1<len(correct)<6
    STEPS.append({'id':sid,'step_content':{'type':'multiple_choice','title':'Провери разбирането си','instruction':wrap('<p>'+question+'</p><p><strong>Избери всички верни отговори.</strong></p>'),'instruction_format':'html','options':[{'id':str(i+1),'text':x} for i,x in enumerate(options)],'correct_option_ids':[str(i+1) for i in correct],'feedback':feedback},'step_rules':{'automatic_feedback':True,'send_progress':True,'ai_feedback':False}})

