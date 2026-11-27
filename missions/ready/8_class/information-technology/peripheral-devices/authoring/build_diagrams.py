from pathlib import Path
from html import escape
OUT=Path(__file__).resolve().parent.parent/'assets';OUT.mkdir(exist_ok=True)
def text(x,y,lines,size=25,anchor='middle'):
 return f'<text x="{x}" y="{y}" font-family="Arial,Segoe UI,sans-serif" font-size="{size}" fill="#20354c" text-anchor="{anchor}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.35}">{escape(s)}</tspan>' for i,s in enumerate(lines))+'</text>'
def box(x,y,w,h,lines,fill='#fff',size=24):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="#a8c4d5" stroke-width="2"/>'+text(x+w/2,y+h/2-(len(lines)-1)*size*.65+8,lines,size)
def arrow(x,y,xx,yy):
 return f'<path d="M{x} {y}L{xx} {yy}" stroke="#207e94" stroke-width="4" marker-end="url(#a)"/>'
def save(name,b):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="710" viewBox="0 0 1100 710"><rect width="1100" height="710" rx="20" fill="#f2f7fb"/><defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#207e94"/></marker></defs>'+b+'</svg>'
 (OUT/(name+'.svg')).write_text(s,'utf-8')
b=text(550,52,['КАК ЗАЯВКАТА ЗА ПЕЧАТ СТИГА ДО ПРИНТЕРА'],28)
for y,lines,col in [(95,['Човекът избира „Печат“'],'#e4f3eb'),(210,['Програма за текст + Windows'],'#fff'),(325,['Драйвер — програма за устройството'],'#e2eefc'),(440,['Контролер — управляваща електроника'],'#fff0d3'),(555,['Принтер — отпечатан лист'],'#e4f3eb')]:
 b+=box(160,y,780,80,lines,col)
 if y<555:b+=arrow(550,y+88,550,y+105)
b+=text(550,682,['Опростена схема на ролите, а не списък на всички вътрешни части.'],20)
save('interaction',b)
b=text(550,55,['КАБЕЛЪТ И ДРАЙВЕРЪТ ИМАТ РАЗЛИЧНИ РОЛИ'],28)
b+=box(60,115,450,120,['Драйвер','Програма в операционната система'],'#e2eefc',23)
b+=box(590,115,450,120,['Контролер','Електронна част на хардуера'],'#fff0d3',23)
b+=arrow(530,175,570,175)
b+=box(60,330,450,120,['Порт и кабел','Физическа връзка'],'#fff')
b+=box(590,330,450,120,['Принтер','Извежда информация на хартия'],'#e4f3eb',23)
b+=text(550,535,['За работа са нужни съвместими устройство, връзка и софтуер.'],26)
b+=text(550,603,['Драйвер ≠ кабел','Драйвер ≠ контролер'],28)
save('driver',b)
b=text(550,52,['ДИСПЕЧЕР НА УСТРОЙСТВА — УЧЕБЕН ИЗГЛЕД'],28)
b+=box(50,100,1000,75,['Търсене → Device Manager / Диспечер на устройства'],'#e2eefc',25)
b+='<rect x="70" y="220" width="520" height="360" rx="16" fill="#fff" stroke="#a8c4d5"/>'
for n,line in enumerate(['▸ Клавиатури','▸ Монитори','▸ Мрежови карти','▾ Disk drives / Дискови устройства','     Учебна USB памет']):
 b+=text(100,265+n*58,[line],23,'start')
b+=box(650,245,380,110,['Properties','Свойства на избраното устройство'],'#e4f3eb',22)
b+=arrow(610,420,650,370)
b+=box(650,430,380,100,['Driver / Драйвер','Информация за драйвера'],'#fff0d3',23)
b+=arrow(840,375,840,410)
b+=text(550,655,['Примерът показва пътя до информацията; не променя настройки.'],23)
save('manager',b)
b=text(550,52,['ДАННИ ЗА ДРАЙВЕРА — ГОТОВ УЧЕБЕН ПРИМЕР'],27)
b+=box(55,100,990,75,['Устройство: Учебна USB памет'],'#e4f3eb')
b+='<rect x="55" y="220" width="480" height="340" rx="18" fill="#fff" stroke="#a8c4d5"/>'
b+=text(295,265,['Driver / Драйвер'],28)
b+=text(85,330,['Доставчик: Microsoft','Версия: 10.0.26100.1','Има и поле за дата на драйвера'],22,'start')
b+=box(100,455,390,70,['Driver Details'],'#e2eefc')
b+=arrow(550,480,600,480)
b+=box(620,260,425,250,['Driver Details','Файлове на драйвера:','disk.sys','partmgr.sys'],'#fff0d3',26)
b+=text(550,628,['Версията описва софтуера, а не обема на паметта.','Файловете на драйвера са различни от личните документи.'],24)
save('details',b)
print('Built 4 instructional diagrams')
