"""Author the requested textbook missions, with stable IDs and per-lesson worked illustrations."""
from pathlib import Path
import html,json,textwrap,uuid,random
BASE=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
READY=BASE/'missions/ready/8_class/information-technology'
URL='https://raw.githubusercontent.com/martin-lift/Edu108/main/missions/ready/8_class/information-technology/'
CSS='''body{font:19px/1.65 Arial,"Segoe UI",sans-serif;color:#20354c;background:white;margin:0;padding:24px;max-width:960px;box-sizing:border-box}p{margin:16px 0}h3{font-size:24px;color:#146b80}strong{color:#155e75}li{margin:9px 0}figure{margin:20px 0;padding:14px;background:#f1f7fa;border:1px solid #dce7ee;border-radius:14px;text-align:center}figure img{display:block;width:100%;height:auto;margin:auto}figcaption{font-size:13px;line-height:1.45;color:#52687d;margin-top:9px}.key,.example{padding:16px 20px;border-radius:9px;margin:20px 0}.key{background:#e7f5ef;border-left:5px solid #269378}.example{background:#fff3db;border-left:5px solid #e4ad3b}table{width:100%;border-collapse:collapse;font-size:17px}td,th{border:1px solid #c9dce5;padding:10px;text-align:left;vertical-align:top}th{background:#e6f0f6}a{color:#126797;overflow-wrap:anywhere}code{font:17px Consolas,monospace;overflow-wrap:anywhere;background:#edf3f8;padding:2px 4px}pre{white-space:pre-wrap;background:#edf3f8;padding:14px;border-radius:8px;overflow-wrap:anywhere}@media(max-width:550px){body{padding:14px}td,th{font-size:15px;padding:7px}}'''
def wrap(s):return '<!doctype html><html lang="bg"><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+s+'</body></html>'
def P(*ps):return ''.join('<p>'+p+'</p>' for p in ps)
def E(s):return '<div class="example">'+s+'</div>'
def K(s):return '<div class="key">'+s+'</div>'
def T(head,rows):return '<table><tr>'+''.join('<th>'+x+'</th>' for x in head)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</table>'
def F(key,caption):
 im=json.loads((HERE/'sofia-images.json').read_text('utf-8'))[key]
 credit=''
 if im['license'].lower() not in ('public domain','cc0'):
  credit=' · '+html.escape(im['author'])+' · <a href="'+html.escape(im['source'],quote=True)+'">източник</a> · <a href="'+html.escape(im['license_url'],quote=True)+'">'+html.escape(im['license'])+'</a>'
 return '<figure><img style="max-height:340px;object-fit:contain" src="'+html.escape(im['url'],quote=True)+'" alt="'+html.escape(caption,quote=True)+'"><figcaption>'+html.escape(caption)+credit+'</figcaption></figure>'
def C(question,options,correct,feedback):
 assert len(options)==6 and 1<len(correct)<6
 return dict(question=question,options=options,correct=correct,feedback=feedback)
def O(question,guide,answer):
 assert question.count('?')==1
 return dict(question=question,guide=guide,answer=answer)
def I(sid,title,body,visual,check=None):return dict(id=sid,title=title,body=body,visual=visual,check=check)
def svg_text(x,y,lines,size=23,anchor='start',color='#20354c'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}" font-family="Arial,Segoe UI,sans-serif">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.35}">{html.escape(s)}</tspan>' for i,s in enumerate(lines))+'</text>'
def make_svg(title,rows,path):
 # A different concrete example is supplied for each topic, not a repeated generic icon.
 pairs=[(textwrap.wrap(str(a),24),textwrap.wrap(str(b),48)) for a,b in rows]
 heights=[max(len(a),len(b))*31+36 for a,b in pairs]
 h=130+sum(heights)+20*len(rows)+55
 out=f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{h}" viewBox="0 0 1100 {h}"><rect width="1100" height="{h}" rx="20" fill="#f2f7fb"/>'
 out+=svg_text(550,42,textwrap.wrap(title,65),27,'middle')
 y=100
 for n,((a,b),rh) in enumerate(zip(pairs,heights)):
  col=['#e2eefb','#e2f4eb','#fff0d1'][n%3]
  out+=f'<rect x="35" y="{y}" width="1030" height="{rh}" rx="14" fill="white" stroke="#b4cbd9"/><path d="M35 {y+14}Q35 {y}49 {y}H350V{y+rh}H49Q35 {y+rh}35 {y+rh-14}Z" fill="{col}"/>'
  out+=svg_text(55,y+34,a,23)+svg_text(375,y+34,b,23)
  y+=rh+20
 out+=svg_text(550,h-28,['Готов учебен пример'],20,'middle', '#52687d')+'</svg>'
 path.write_text(out,'utf-8')
def build(number,slug,title,pages,intro,topics,summary,coverage,sources,notes=''):
 ids_path=HERE/'identities.json'
 ids=json.loads(ids_path.read_text('utf-8')) if ids_path.exists() else {}
 if str(number) not in ids:
  ids[str(number)]=dict(slug=slug,title=title,mission_id=str(uuid.uuid4()))
  ids_path.write_text(json.dumps(ids,ensure_ascii=False,indent=2)+'\n','utf-8')
 dest=READY/slug; (dest/'illustrations').mkdir(parents=True,exist_ok=True)
 steps=[]
 def information(sid,heading,body,rows):
  make_svg('Проследи примера',rows,dest/'illustrations'/f'{sid}.svg')
  caption='Учебна схема с готови данни за разглеждане.'
  suffix='?v=2' if sid=='summary' else ''
  image='<figure><img src="'+URL+slug+'/illustrations/'+sid+'.svg'+suffix+'" alt="'+html.escape(' '.join(a+': '+b for a,b in rows),quote=True)+'"><figcaption>'+caption+'</figcaption></figure>'
  steps.append({'id':sid,'step_content':{'type':'information','title':heading,'instruction':wrap(image+body),'instruction_format':'html'},'step_rules':{}})
 information('intro','За какво е този урок?',intro,[('Тема',title),('Как ще учим','Разглеждаме обяснения, ситуации и готови примери.'),('Резултат','Обясняваме решенията със свои думи и проверяваме разбирането.')])
 for topic in topics:
  information(topic['id'],topic['title'],topic['body'],topic['visual'])
  c=topic['check']
  if not c:continue
  if 'options' in c:
   order=list(range(6));random.Random(ids[str(number)]['mission_id']+topic['id']).shuffle(order)
   sc={'type':'multiple_choice','title':'Провери разбирането си','instruction':wrap(P(c['question'],'<strong>Избери всички верни отговори.</strong>')),'instruction_format':'html','options':[{'id':str(i+1),'text':c['options'][old]} for i,old in enumerate(order)],'correct_option_ids':[str(i+1) for i,old in enumerate(order) if old in c['correct']],'feedback':c['feedback']}
  else:
   sc={'type':'open_answer','title':'Обясни със свои думи','instruction':wrap(P(c['question'],c['guide'])),'instruction_format':'html','reference_answer':c['answer']}
  steps.append({'id':topic['id']+'-check','step_content':sc,'step_rules':{'automatic_feedback':True,'send_progress':True,'ai_feedback':False}})
 assert 1<=len(summary)<=5
 summary_cases={
 11:[('Инсталиране','Добавяме програмата.'),('End Task','Спираме текущата работа.'),('Деинсталиране','Премахваме програмата.')],
 12:[('За цялата задача','Самоучител с последователни действия.'),('За отделна команда','Справка в помощната система.')],
 13:[('Три файла','Събираме ги в arhiv.zip.'),('Извличане','Получаваме ги в избраната папка.')],
 14:[('Само една част','Липсващите части пречат на извличането.'),('Пълен комплект','Събираме частите и извличаме.')],
 15:[('Pirin + Rila','Шест файла в planini.zip.'),('Добавени задачи','Осем файла в arhiv.zip.')],
 16:[('HTML','Кое е заглавието и кое е абзацът?'),('CSS','Какъв е цветът и размерът?'),('Браузър','Показва резултата.')],
 17:[('Аудитория','Ученици търсят график.'),('Решение','Ясна връзка към тренировките.'),('Поддръжка','Поправяме променения час.')],
 18:[('Редактиране','Текст, изображения, подредба и връзки.'),('Запис и Browse','Проверяваме действителния резултат.')],
 19:[('Четири страници','Една обща заглавна част и меню.'),('Собствена тема','Различни текстове и изображения.')],
 20:[('Шаблон → редакция','Приспособяваме за София.'),('Преглед → публикация','Проверяваме и после даваме уеб достъп.')]
 }
 information('summary','Най-важното от урока','<ul>'+''.join('<li>'+s+'</li>' for s in summary)+'</ul>',summary_cases[number])
 mission={'mission_version':4,'mission_id':ids[str(number)]['mission_id'],'mission_content':{'title':title,'class_name':'8. клас','subject':'Информационни технологии','category':'Мисия за стандартен урок','lesson':title,'description':f'По урок {number}, стр. {pages}, Домино, ИТ за 8. клас. Самостоятелни обяснения и завършени примери в реда на учебника.','content_format':'html','steps':steps},'mission_rules':{'allow_back_navigation':True,'show_progress_panel':True}}
 mission['next_mission_id']=ids.get(str(number+1),{}).get('mission_id')
 (dest/(slug+'.mission.json')).write_text(json.dumps(mission,ensure_ascii=False,indent=2)+'\n','utf-8')
 doc=f'# {title}\n\nСтандартна мисия по урок {number}, стр. {pages} от [учебника по ИТ за 8. клас, Домино](https://ebook.domino.bg/books/8/it/#page={pages.split("–")[0]}).\n\n{len(steps)} стъпки. Съдържанието е за начинаещи ученици. Изображенията са оригинални схеми на конкретни примери, публикувани с външни URL; не се представят за екранни снимки на реален ученически компютър. Отворените отговори имат предварителна обратна връзка; AI е изключен.\n\n## Покритие на урока\n\n'+ '\n'.join('- '+x for x in coverage)+'\n\n## Източници за проверка\n\n'+'\n'.join('- ['+label+']('+url+')' for label,url in sources)+'\n\n'+notes+'\n\n## Изходен код\n\nСъдържанието и възстановяването на JSON и схемите са в `authoring/it8-textbook-batch/lesson'+str(number)+'.py` и `engine.py` от корена на хранилището. UUID се запазва в identities.json. Не се изисква достъп до непредоставените материали от папките Razdel на издателя.\n'
 (dest/'README.md').write_text(doc,'utf-8')
 print(number,slug,len(steps),'steps',flush=True)
 return mission
