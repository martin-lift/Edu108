from pathlib import Path
import html
OUT=Path(__file__).resolve().parent.parent/'assets'
OUT.mkdir(exist_ok=True)
HEAD='''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="650" viewBox="0 0 1000 650"><rect width="1000" height="650" rx="20" fill="#f3f8fc"/><defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#207e94"/></marker></defs>'''
def text(x,y,lines,size=24,color='#20354c',anchor='middle'):
 return '<text x="%s" y="%s" text-anchor="%s" font-family="Arial,Segoe UI,sans-serif" font-size="%s" fill="%s">'%(x,y,anchor,size,color)+''.join('<tspan x="%s" dy="%s">%s</tspan>'%(x,0 if i==0 else size*1.35,html.escape(line)) for i,line in enumerate(lines))+'</text>'
def box(x,y,w,h,lines,color='#fff'):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{color}" stroke="#a9c5d6" stroke-width="2"/>'+text(x+w/2,y+h/2-10*(len(lines)-1)+8,lines)
def arrow(x,y,xx,yy):
 return f'<path d="M{x} {y}L{xx} {yy}" fill="none" stroke="#207e94" stroke-width="4" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
def save(name,body):
 (OUT/(name+'.svg')).write_text(HEAD+body+'</svg>','utf-8')

b=text(500,48,['ДВА ТЕЛЕФОНА — ЕДНА СВЪРЗАНА МРЕЖА'],28)
b+=box(55,100,265,90,['Телефонът на Мая'],'#e0f2eb')+box(55,260,265,100,['Базова станция','в района на Мая'])
b+=box(680,100,265,90,['Телефонът на Иван'],'#e0f2eb')+box(680,260,265,100,['Базова станция','в района на Иван'])
b+=arrow(187,205,187,245)+arrow(812,205,812,245)
b+=text(390,227,['Радиовръзка'],20)+text(610,227,['Радиовръзка'],20)
b+=box(265,460,470,120,['Транспортни връзки + ядро','на мрежата на оператора','и връзки между оператори'],'#fff0d1')
for path in ['M187 380V520H245','M812 380V520H755']:
 b+=f'<path d="{path}" fill="none" stroke="#207e94" stroke-width="4" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
b+=text(500,620,['Стрелките показват обмен и в двете посоки.'],22)
save('route',b)

b=text(500,48,['КЛЕТКИ И ДВИЖЕНИЕ'],30)
for x,fill,label in [(230,'#b5dbe8','А'),(500,'#bfe5ce','Б'),(770,'#f5dca7','В')]:
 b+=f'<ellipse cx="{x}" cy="285" rx="205" ry="185" fill="{fill}" fill-opacity="0.7" stroke="#7097ab" stroke-width="2"/>'
 b+=text(x,180,['Клетка '+label],28)
 b+=f'<path d="M{x-30} 330L{x} 240L{x+30} 330M{x-20} 300H{x+20}M{x-12} 275H{x+12}" fill="none" stroke="#2c5d72" stroke-width="6"/>'
 b+=text(x,375,['Антена'],20)
b+='<path d="M55 475C260 425 650 530 940 460" fill="none" stroke="#91a6b3" stroke-width="32"/><path d="M55 475C260 425 650 530 940 460" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="20 18"/>'
b+=box(390,430,140,65,['Автобус'],'#ffffff')
b+='<path d="M560 445L680 445" stroke="#207e94" stroke-width="4" marker-end="url(#arrow)"/>'
b+=text(500,566,['Зоните се застъпват. Реалните им форми са различни.','Мрежата може да предаде връзката: А → Б → В.'],23)
save('cells',b)

b=text(500,48,['САТЕЛИТЪТ КАТО МОСТ'],30)
b+=box(345,100,310,85,['Комуникационен','сателит'],'#e0f2eb')
b+=box(30,290,330,120,['Отдалечена станция','+ сателитен терминал'])
b+=box(640,290,330,120,['Наземна станция','към сателитната мрежа'])
b+=arrow(200,270,360,200)+arrow(640,200,800,270)
b+=box(30,505,330,80,['Телефон'],'#e0f2eb')+arrow(195,430,195,485)
b+=box(640,505,330,80,['Мрежа на оператора'],'#fff0d1')+arrow(805,430,805,485)
b+=text(360,463,['Радиовръзка','с местната станция'],19)
b+=text(500,630,['Телефонът използва станцията; сателитът е следващ участък.'],22)
save('satellite',b)

b=text(500,50,['ОТ ГЛАСА ДО РАДИОСИГНАЛА'],30)
b+=box(50,110,380,115,['Мая говори','Микрофонът приема гласа'],'#e0f2eb')
b+=box(570,110,380,115,['Телефонът обработва','и преобразува сигнала'])
b+=arrow(450,167,550,167)
b+=text(240,300,['Звук: трептения на въздуха'],22)
b+='<path d="M75 360Q95 290 115 360T155 360T195 360T235 360T275 360T315 360T355 360T395 360" fill="none" stroke="#269378" stroke-width="5"/>'
b+=text(760,300,['Цифрови данни'],24)
b+=text(760,370,['0 1 0 0 1 1 0 1'],34,'#207e94')
b+=arrow(760,410,760,465)
b+=box(570,490,380,100,['Антената предава','чрез радиосигнал'],'#fff0d1')
b+=text(270,520,['Към базовата станция'],22)
b+=arrow(550,540,90,540)
b+=text(500,630,['При получателя данните отново се превръщат в звук.'],22)
save('voice',b.replace(' marker-start="url(#arrow)"',''))
print('Built 4 SVG diagrams')
