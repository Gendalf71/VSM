import os, math, textwrap
import svgwrite
import cairosvg

BASE = '/mnt/data/rzd_vsm_github/assets/figures'
os.makedirs(BASE, exist_ok=True)
W, H = 1400, 900
MARGIN = 50
TITLE_Y = 60
SUB_Y = 95
BODY_TOP = 125
FOOT_Y = H - 28

# Palette
NAVY = '#0b1736'
BG = '#f7f8fb'
MID = '#dfe5ef'
DARK = '#24334d'
TEXT = '#1d2737'
MUTED = '#5c6b80'
ACCENTS = {
    'red':'#ff5a5f','orange':'#f59e0b','yellow':'#fbbf24','green':'#22c55e',
    'blue':'#38bdf8','purple':'#a855f7','teal':'#06b6d4','gray':'#94a3b8'
}

font_main = 'DejaVu Sans, Arial, sans-serif'

def add_defs(dwg):
    marker = dwg.marker(insert=(10,5), size=(10,10), orient='auto', id='arrow')
    marker.add(dwg.path(d='M 0 0 L 10 5 L 0 10 z', fill=TEXT))
    dwg.defs.add(marker)
    marker2 = dwg.marker(insert=(10,5), size=(10,10), orient='auto', id='arrow_white')
    marker2.add(dwg.path(d='M 0 0 L 10 5 L 0 10 z', fill='white'))
    dwg.defs.add(marker2)
    circ = dwg.marker(insert=(4,4), size=(8,8), orient='auto', id='dot')
    circ.add(dwg.circle(center=(4,4), r=3, fill=TEXT))
    dwg.defs.add(circ)


def title_block(dwg, title, subtitle, dark=False):
    color = 'white' if dark else TEXT
    subc = '#cfd6e2' if dark else MUTED
    dwg.add(dwg.text(title, insert=(MARGIN, TITLE_Y), font_size=34, font_weight='700', fill=color, font_family=font_main))
    dwg.add(dwg.text(subtitle, insert=(MARGIN, SUB_Y), font_size=18, fill=subc, font_family=font_main))


def footer(dwg, text, dark=False):
    color = '#b3bfd2' if dark else '#7b8799'
    dwg.add(dwg.text(text, insert=(MARGIN, FOOT_Y), font_size=14, fill=color, font_family=font_main))


def note_box(dwg, x,y,w,h, text_lines, dark=False):
    fill = '#122449' if dark else '#eef2f8'
    stroke = '#28406c' if dark else '#cbd5e1'
    txtc = 'white' if dark else TEXT
    dwg.add(dwg.rect((x,y),(w,h),rx=14, ry=14, fill=fill, stroke=stroke, stroke_width=1.2))
    ty = y+28
    for i,line in enumerate(text_lines):
        dwg.add(dwg.text(line, insert=(x+18, ty+i*20), font_size=16, fill=txtc, font_family=font_main))


def arrow_label(dwg, start, end, label, color=TEXT, font_size=16, anchor='start', offset=(0,0), dark=False):
    stroke = 'white' if dark and color==TEXT else color
    dwg.add(dwg.line(start=start, end=end, stroke=stroke, stroke_width=2.2, marker_end=dwg.marker(id='arrow_white' if dark and stroke=='white' else 'arrow').get_funciri()))
    x = end[0]+offset[0]
    y = end[1]+offset[1]
    dwg.add(dwg.text(label, insert=(x,y), font_size=font_size, fill=('white' if dark and color==TEXT else color), font_family=font_main, text_anchor=anchor))


def save_svg_png(name, build_func):
    svg_path = os.path.join(BASE, name + '.svg')
    png_path = os.path.join(BASE, name + '.png')
    dwg = svgwrite.Drawing(svg_path, size=(W,H), viewBox=f'0 0 {W} {H}')
    add_defs(dwg)
    build_func(dwg)
    dwg.save()
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=W, output_height=H)
    print('saved', name)

# Fig 1

def fig1(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=NAVY))
    title_block(dwg, 'Фото 1. Сеть ВСМ от Москвы: схема для проверки чисел', 'Авторская реконструкция по публикации Минтранса; южная подпись 715 км / 3 ч помечена как требующая сверки.', dark=True)
    cx, cy = 680, 455
    dwg.add(dwg.circle(center=(cx,cy), r=34, fill='white', stroke='#8bd3ff', stroke_width=4))
    dwg.add(dwg.text('Москва', insert=(cx, cy+7), text_anchor='middle', font_size=24, font_weight='700', fill='#0b1736', font_family=font_main))
    nodes = [
        ('Санкт-Петербург', (1050,180), ACCENTS['red'], '679 км / 2 ч 15 мин', 'средняя ≈ 302 км/ч'),
        ('Минск', (250,390), ACCENTS['purple'], '715 км / около 3 ч', 'средняя ≈ 238 км/ч'),
        ('Рязань', (980,500), ACCENTS['blue'], '205 км / 1 ч 05 мин', ''),
        ('Воронеж', (920,610), ACCENTS['green'], '', ''),
        ('Адлер', (1150,720), ACCENTS['green'], 'южный луч', 'подпись на схеме требует проверки'),
        ('Нижний Новгород', (1035,340), ACCENTS['yellow'], '', ''),
        ('Казань', (1160,270), ACCENTS['orange'], '', ''),
        ('Екатеринбург', (1290,150), ACCENTS['orange'], '1532 км / 6 ч 36 мин', 'средняя ≈ 232 км/ч'),
    ]
    # paths
    # custom points for clean routing
    paths = {
        'Санкт-Петербург': [(cx,cy),(760,390),(850,300),(940,230),(1050,180)],
        'Минск': [(cx,cy),(560,440),(470,425),(360,410),(250,390)],
        'Рязань': [(cx,cy),(810,470),(900,490),(980,500)],
        'Воронеж': [(cx,cy),(760,520),(840,575),(920,610)],
        'Адлер': [(cx,cy),(770,530),(880,610),(1000,680),(1150,720)],
        'Нижний Новгород': [(cx,cy),(815,425),(925,385),(1035,340)],
        'Казань': [(cx,cy),(830,405),(980,340),(1080,310),(1160,270)],
        'Екатеринбург': [(cx,cy),(850,380),(990,310),(1140,235),(1290,150)],
    }
    for label, pos, color, line1, line2 in nodes:
        pts = paths[label]
        path_str = 'M ' + ' L '.join(f'{x},{y}' for x,y in pts)
        dwg.add(dwg.path(d=path_str, fill='none', stroke=color, stroke_width=6, stroke_linecap='round'))
        # node dots along path for east/south routes
        for px,py in pts[1:-1]:
            if label in ('Екатеринбург','Адлер','Казань','Нижний Новгород'):
                dwg.add(dwg.circle((px,py), r=6, fill=color))
        dwg.add(dwg.circle(pos, r=8, fill=color, stroke='white', stroke_width=2))
        align = 'start'; tx = pos[0]+15; ty = pos[1]-8
        if pos[0] > 1000:
            align = 'end'; tx = pos[0]-15
        if label == 'Минск': align='end'; tx=pos[0]-15
        dwg.add(dwg.text(label, insert=(tx,ty), text_anchor=align, font_size=24, font_weight='700', fill='white', font_family=font_main))
        if line1:
            dwg.add(dwg.text(line1, insert=(tx,ty+25), text_anchor=align, font_size=16, fill='#cfd6e2', font_family=font_main))
        if line2:
            dwg.add(dwg.text(line2, insert=(tx,ty+45), text_anchor=align, font_size=16, fill='#aeb8c8', font_family=font_main))
    note_box(dwg, 55, 690, 450, 120,
             ['Контрольная пометка:',
              'Питер: 715 км / 3 ч у южного луча в исходной инфографике',
              'нельзя принимать за параметр полного маршрута Москва — Адлер.'], dark=True)
    footer(dwg, 'Авторская схема; задача — аккуратно показать направления и спорную подпись без наложения текста.', dark=True)

# Fig 2

def fig2(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=BG))
    title_block(dwg, 'Рис. 2. Безбалластный путь ВСМ на слабом грунте', 'Не новые рельсы, а жёсткая геометрия: рельс — плита — основание — сваи.')
    # layers
    x0, y0, width = 170, 300, 980
    # rail heads and pads
    for x in [420,930]:
        dwg.add(dwg.rect((x-10,190),(20,60),fill='#4b5563'))
        dwg.add(dwg.rect((x-30,180),(60,14),fill='#4b5563'))
        dwg.add(dwg.polygon(points=[(x-25,240),(x+25,240),(x+15,275),(x-15,275)], fill='#f97316'))
    # slab and base
    dwg.add(dwg.rect((x0,y0),(width,55), rx=8, ry=8, fill='#cbd5e1', stroke='#64748b', stroke_width=2))
    dwg.add(dwg.rect((x0+35,y0+55),(width-70,48), fill='#64748b'))
    ground_y=500
    dwg.add(dwg.rect((0,ground_y),(W,H-ground_y), fill='#d7c3a2'))
    dwg.add(dwg.rect((0,ground_y+60),(W,H-ground_y-60), fill='#b69f7c'))
    # piles
    for x in [320,470,620,785,950,1110]:
        dwg.add(dwg.rect((x,355),(22,220), fill='#94a3b8', stroke='#64748b', stroke_width=1.5))
    # labels with arrows, placed around margins
    arrow_label(dwg,(520,155),(455,180),'рельс / скрепление', offset=(-8,-10))
    arrow_label(dwg,(915,145),(1020,300),'бетонная плита', offset=(16,5))
    arrow_label(dwg,(920,215),(1030,350),'основание', offset=(16,6))
    arrow_label(dwg,(1125,455),(1121,455),'свая передаёт нагрузку в устойчивые слои', offset=(20,-8))
    arrow_label(dwg,(170,615),(250,560),'слабый грунт / мороз / сезонные деформации', offset=(-10,0))
    footer(dwg, 'Авторская схема. Проверочный смысл: показать слои, жёсткость опоры и отсутствие наложения подписей на конструкцию.')

# Fig 3

def fig3(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=NAVY))
    title_block(dwg, 'Рис. 3. Пятно контакта «колесо — рельс»', 'На высокой скорости микроскопическая зона контакта решает износ, шум, вибрацию и безопасность.', dark=True)
    # rail
    dwg.add(dwg.rect((230,560),(940,28), rx=8, fill='#7c8aa1'))
    dwg.add(dwg.rect((320,588),(760,55), rx=8, fill='#51627d'))
    dwg.add(dwg.rect((160,650),(1080,36), rx=6, fill='#51627d'))
    # wheel
    cx, cy = 560, 425
    dwg.add(dwg.circle((cx,cy), 160, fill='#d8dee8', stroke='#94a3b8', stroke_width=4))
    dwg.add(dwg.circle((cx,cy), 92, fill=NAVY, stroke='#475569', stroke_width=4))
    # contact ellipse
    dwg.add(dwg.ellipse(center=(610,560), r=(110,18), fill='#facc15', opacity=0.9))
    dwg.add(dwg.ellipse(center=(610,560), r=(75,12), fill='#ef4444', opacity=0.95))
    # forces
    dwg.add(dwg.line((560,320),(560,510), stroke='white', stroke_width=5, marker_end=dwg.marker(id='arrow_white').get_funciri()))
    dwg.add(dwg.text('N', insert=(573,360), font_size=26, fill='white', font_weight='700', font_family=font_main))
    dwg.add(dwg.text('вертикальная нагрузка', insert=(595,380), font_size=16, fill='#cfd6e2', font_family=font_main))
    dwg.add(dwg.line((470,575),(330,620), stroke='#22c55e', stroke_width=4, marker_end=dwg.marker(id='arrow').get_funciri()))
    dwg.add(dwg.text('касательная сила / тяга', insert=(190,640), font_size=16, fill='#22c55e', font_family=font_main))
    dwg.add(dwg.line((742,575),(860,620), stroke='#f97316', stroke_width=4, marker_end=dwg.marker(id='arrow').get_funciri()))
    dwg.add(dwg.text('фланец, износ, боковые силы', insert=(866,640), font_size=16, fill='#f97316', font_family=font_main))
    # callout labels
    arrow_label(dwg,(950,480),(760,545),'пятно контакта в реальности маленькое, но работает как силовая зона', color='white', dark=True, offset=(22,-8))
    footer(dwg, 'Схема условная. Геометрия колеса и рельса показана укрупнённо ради читабельности.')

# Fig4

def fig4(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=BG))
    title_block(dwg, 'Рис. 4. Железобетонная балка 700 т: масштаб стройки', 'Для пассажира мост через Шошу — минуту ровного хода. Для строителя — сотни таких точных изделий.')
    # support and ground
    dwg.add(dwg.rect((0,710),(W,40), fill='#94a3b8'))
    for x in [250,1130]:
        dwg.add(dwg.rect((x,340),(40,370), fill='#a8b1bf'))
    dwg.add(dwg.rect((280,405),(840,95), rx=10, fill='#cbd5e1', stroke='#64748b', stroke_width=2))
    dwg.add(dwg.rect((315,432),(770,40), rx=10, fill='#b7c3d5'))
    dwg.add(dwg.text('700 тонн', insert=(700,468), text_anchor='middle', font_size=32, font_weight='700', fill=TEXT, font_family=font_main))
    # dimension arrow above beam
    dwg.add(dwg.line((270,355),(1110,355), stroke=TEXT, stroke_width=2, marker_start=dwg.marker(id='arrow').get_funciri(), marker_end=dwg.marker(id='arrow').get_funciri()))
    dwg.add(dwg.text('длина условная; важен порядок масштаба', insert=(690,340), text_anchor='middle', font_size=16, fill=MUTED, font_family=font_main))
    # bus and carriage
    # bus
    dwg.add(dwg.rect((385,590),(120,58), rx=8, fill='#f59e0b', stroke='#92400e', stroke_width=2))
    for wx in [408,440,472]:
        dwg.add(dwg.rect((wx,604),(22,16), rx=3, fill='#f8fafc'))
    dwg.add(dwg.circle((418,652),11,fill='#1f2937')); dwg.add(dwg.circle((480,652),11,fill='#1f2937'))
    dwg.add(dwg.text('автобус', insert=(445,687), text_anchor='middle', font_size=16, fill=MUTED, font_family=font_main))
    # railcar
    dwg.add(dwg.rect((720,565),(220,84), rx=20, fill='#e5e7eb', stroke='#64748b', stroke_width=2))
    for wx in [770,830,890]:
        dwg.add(dwg.rect((wx,588),(26,18), rx=3, fill='#bae6fd'))
    dwg.add(dwg.circle((790,650),12,fill='#1f2937')); dwg.add(dwg.circle((895,650),12,fill='#1f2937'))
    dwg.add(dwg.text('вагон ВСМ, условный', insert=(830,687), text_anchor='middle', font_size=16, fill=MUTED, font_family=font_main))
    # labels under beam, not overlapping objects
    dwg.add(dwg.text('изготовить → проверить → перевезти → поднять → поставить на опоры', insert=(700,555), text_anchor='middle', font_size=18, fill=TEXT, font_family=font_main))
    footer(dwg, 'Авторская схема по числу 700 т из сообщения Минтранса. Пропорции не являются заводским чертежом.')

# Fig5

def fig5(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=NAVY))
    title_block(dwg, 'Рис. 5. Токосъём на 360–400 км/ч', 'Пантограф возбуждает волну в проводе; допустимые отрывы при высокой скорости считаются уже миллисекундами.', dark=True)
    # catenary and contact wire
    ywire = 230
    dwg.add(dwg.line((130,ywire),(1270,ywire), stroke='white', stroke_width=4))
    # poles/hangers
    for x in range(180,1250,130):
        dwg.add(dwg.line((x,180),(x,ywire), stroke='#94a3b8', stroke_width=2))
    # wave
    pts=[]
    for i in range(0,1100):
        x=150+i
        y=ywire+10*math.sin(i/70.0)
        pts.append((x,y))
    d='M '+ ' L '.join(f'{x:.1f},{y:.1f}' for x,y in pts)
    dwg.add(dwg.path(d=d, fill='none', stroke='#fbbf24', stroke_width=4))
    # roof and pantograph
    dwg.add(dwg.rect((180,570),(1040,90), rx=25, fill='#e5e7eb', stroke='#94a3b8', stroke_width=2))
    for x in [300,450,600,750,900]:
        dwg.add(dwg.rect((x,595),(64,22), rx=4, fill='#bae6fd'))
    base=(600,565)
    dwg.add(dwg.line((620,565),(560,420), stroke='#ff4d4f', stroke_width=6))
    dwg.add(dwg.line((620,565),(690,420), stroke='#ff4d4f', stroke_width=6))
    dwg.add(dwg.line((560,420),(690,420), stroke='#ff4d4f', stroke_width=6))
    dwg.add(dwg.line((625,420),(625,255), stroke='#ff4d4f', stroke_width=6))
    dwg.add(dwg.line((590,255),(660,255), stroke='#ff4d4f', stroke_width=5))
    # labels arranged above and below
    arrow_label(dwg,(890,285),(760,255),'контактный провод', color='white', dark=True, offset=(20,-8))
    arrow_label(dwg,(960,335),(810,240),'волна в контактной сети', color='white', dark=True, offset=(18,0))
    arrow_label(dwg,(785,448),(690,420),'контактная сила', color='white', dark=True, offset=(18,0))
    note_box(dwg, 80, 690, 470, 110,
             ['Контрольный вопрос ТМ: 25 кВ 50 Гц или 2×25 кВ?',
              'однорычажный пантограф и допустимый отрыв 5–10 мс?',
              'диагностика провода и контактных вставок?'], dark=True)
    footer(dwg, 'Авторская схема. Не является проектом контактной сети; служит для читабельного объяснения динамики токосъёма.', dark=True)

# Fig6

def fig6(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=BG))
    title_block(dwg, 'Рис. 6. Кузовной профиль 980 мм: где вопрос к заводу', 'Схема показывает гипотезу по крупному алюминиевому профилю; точный смысл 980 мм требует заводского чертежа.')
    # left profile block
    dwg.add(dwg.rect((230,245),(340,360), rx=20, fill='#cbd5e1', stroke='#475569', stroke_width=3))
    for y in [295,390,485]:
        dwg.add(dwg.rect((290,y),(210,48), rx=8, fill=BG, stroke='#64748b', stroke_width=2))
    dwg.add(dwg.text('условный крупный профиль', insert=(400,650), text_anchor='middle', font_size=18, fill=MUTED, font_family=font_main))
    # right zoom box
    dwg.add(dwg.rect((760,245),(410,360), rx=18, fill='#f8fbff', stroke='#60a5fa', stroke_width=2, stroke_dasharray='10,8'))
    for y in [295,425]:
        dwg.add(dwg.rect((800,y),(310,55), rx=8, fill='#dbe4ef', stroke='#64748b', stroke_width=2))
    # weld zone
    dwg.add(dwg.path(d='M 835 390 C 880 370, 930 410, 975 390 S 1060 370, 1105 390', fill='none', stroke='#ef4444', stroke_width=4))
    dwg.add(dwg.text('сварной шов', insert=(920,385), font_size=16, fill='#ef4444', font_family=font_main, text_anchor='middle'))
    # dimension 980 mm between top and bottom boxes
    dwg.add(dwg.line((742,295),(742,480), stroke=TEXT, stroke_width=2, marker_start=dwg.marker(id='arrow').get_funciri(), marker_end=dwg.marker(id='arrow').get_funciri()))
    dwg.add(dwg.text('980 мм', insert=(720,392), text_anchor='middle', font_size=22, fill=TEXT, font_family=font_main, transform='rotate(-90,720,392)'))
    dwg.add(dwg.line((742,295),(800,295), stroke=TEXT, stroke_width=2))
    dwg.add(dwg.line((742,480),(800,480), stroke=TEXT, stroke_width=2))
    dwg.add(dwg.text('Контроль: геометрия, остаточные напряжения, ультразвук/рентген.', insert=(760,655), font_size=18, fill=TEXT, font_family=font_main))
    footer(dwg, 'Авторская схема. Не утверждает точную форму профиля; показывает технологический смысл заявления о сварке профиля 980 мм.')

# Fig7

def fig7(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=BG))
    title_block(dwg, 'Рис. 7. Тормозная кривая ВСМ: где автоматика сильнее человека', 'ATP/ETCS-аналог не ждёт, пока машинист «почувствует»: скорость контролируется по безопасной кривой.')
    # axes and grid
    left, top, right, bottom = 150, 210, 1160, 710
    for i in range(6):
        y = top + i*(bottom-top)/5
        dwg.add(dwg.line((left,y),(right,y), stroke='#d7dee8', stroke_width=1))
    for i in range(6):
        x = left + i*(right-left)/5
        dwg.add(dwg.line((x,top),(x,bottom), stroke='#d7dee8', stroke_width=1))
    dwg.add(dwg.line((left,bottom),(right,bottom), stroke=TEXT, stroke_width=3, marker_end=dwg.marker(id='arrow').get_funciri()))
    dwg.add(dwg.line((left,bottom),(left,top), stroke=TEXT, stroke_width=3, marker_end=dwg.marker(id='arrow').get_funciri()))
    # curves
    def poly(points, color, dash=None):
        d='M '+' L '.join(f'{x:.1f},{y:.1f}' for x,y in points)
        dwg.add(dwg.path(d=d, fill='none', stroke=color, stroke_width=4, stroke_dasharray=dash if dash else 'none'))
    xs=[left+30+i*(right-left-100)/130 for i in range(131)]
    def f_red(t): return top+60 + 10*t + 300*(t**5)
    def f_blue(t): return top+105 + 8*t + 260*(t**4.2)
    def f_green(t): return top+72 + 18*t + 360*(t**6)
    red=[(x, f_red(i/130.0)) for i,x in enumerate(xs)]
    blue=[(x, f_blue(i/130.0)) for i,x in enumerate(xs)]
    green=[(x, f_green(i/130.0)) for i,x in enumerate(xs)]
    poly(red, '#ef4444')
    poly(blue, '#2563eb', '10,8')
    poly(green, '#22c55e')
    # warning line
    xwarn = right-110
    dwg.add(dwg.line((xwarn, top+40),(xwarn,bottom), stroke='#111827', stroke_width=2, stroke_dasharray='8,8'))
    dwg.add(dwg.text('точка безопасной остановки', insert=(xwarn-10, top+25), text_anchor='end', font_size=16, fill=TEXT, font_family=font_main))
    # legend box upper right
    note_box(dwg, 770, 220, 300, 120, [], dark=False)
    legend=[('разрешённая скорость','#ef4444','solid'),('фактическая скорость','#2563eb','dash'),('аварийная тормозная кривая','#22c55e','solid')]
    yy=260
    for lbl,col,kind in legend:
        dwg.add(dwg.line((805,yy),(875,yy), stroke=col, stroke_width=4, stroke_dasharray='10,8' if kind=='dash' else 'none'))
        dwg.add(dwg.text(lbl, insert=(895,yy+5), font_size=16, fill=TEXT, font_family=font_main))
        yy+=30
    dwg.add(dwg.text('скорость', insert=(92,195), font_size=18, fill=TEXT, font_family=font_main))
    dwg.add(dwg.text('дистанция до цели', insert=(1000,752), font_size=18, fill=TEXT, font_family=font_main))
    footer(dwg, 'Если фактическая скорость пересекает безопасную кривую, автоматика должна вмешаться раньше человека.')

# Fig8

def fig8(dwg):
    dwg.add(dwg.rect((0,0),(W,H),fill=BG))
    title_block(dwg, 'Рис. 8. Где будущая российская ВСМ на мировой шкале', 'Сравнение коммерческих / эксплуатационных скоростей и проектных ориентиров по открытым источникам статьи.')
    # axis
    left, top = 360, 230
    right = 1240
    dwg.add(dwg.line((left,710),(right,710), stroke=TEXT, stroke_width=3, marker_end=dwg.marker(id='arrow').get_funciri()))
    for val in [0,100,200,300,400,500,600]:
        x=left+val*(right-left)/600
        dwg.add(dwg.line((x,250),(x,710), stroke='#d7dee8', stroke_width=1))
        dwg.add(dwg.text(str(val), insert=(x,738), text_anchor='middle', font_size=16, fill=MUTED, font_family=font_main))
    dwg.add(dwg.text('км/ч', insert=(right+10,738), font_size=18, fill=TEXT, font_family=font_main))
    items=[
        ('«Сапсан»',250,ACCENTS['gray']),
        ('Tokaido Shinkansen',285,'#60a5fa'),
        ('TGV',320,'#2563eb'),
        ('Fuxing / CR400',350,'#f59e0b'),
        ('Будущий ЭВС360',360,'#ef4444'),
        ('Shanghai Maglev',430,'#a855f7'),
    ]
    y=300
    for label,val,col in items:
        dwg.add(dwg.text(label, insert=(120,y+12), font_size=20, fill=TEXT, font_family=font_main))
        x2=left+val*(right-left)/600
        dwg.add(dwg.rect((left,y-10), (x2-left,24), rx=10, ry=10, fill=col, opacity=0.95))
        extra=' / до 400' if label=='Будущий ЭВС360' else ''
        dwg.add(dwg.text(f'{val}{extra}', insert=(x2+12,y+8), font_size=18, fill=TEXT, font_family=font_main))
        y+=70
    note_box(dwg, 70, 770, 1260, 76,
             ['Урок: рекордная скорость не равна успеху. Нужны частота, загрузка, обслуживание, безопасность и экономика.'], dark=False)
    footer(dwg, 'Сравнение не претендует на исчерпывающую энциклопедию; задача — показать место проекта на понятной шкале скоростей.')

for name, func in [
    ('fig01_network_map', fig1),
    ('fig02_ballastless_track', fig2),
    ('fig03_wheel_rail_contact', fig3),
    ('fig04_700t_beam_scale', fig4),
    ('fig05_pantograph_catenary', fig5),
    ('fig06_aluminum_profile_980mm', fig6),
    ('fig07_braking_curve', fig7),
    ('fig08_world_comparison', fig8),
]:
    save_svg_png(name, func)
