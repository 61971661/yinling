# -*- coding: utf-8 -*-
"""从 wode.jpg 裁切「我的」页图标素材 + 取色，输出 mine_b64.json"""
from PIL import Image
import json, base64, io, os

SRC = 'D:/中交信/21-银龄出行/wode.jpg'
OUTDIR = 'C:/Users/61971/WorkBuddy/2026-09-28-09-29-37/.icons'
os.makedirs(OUTDIR, exist_ok=True)
im = Image.open(SRC).convert('RGB')
W, H = im.size
px = im.load()
print('size', W, H)

def sat(p): return max(p) - min(p)
def diff(p, bg): return sum(abs(a - b) for a, b in zip(p, bg))

def avg(x0, y0, x1, y1):
    rs = gs = bs = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]; rs += r; gs += g; bs += b; n += 1
    return (rs // n, gs // n, bs // n)

# ---- 颜色取样 ----
colors = {
    'head': avg(300, 455, 780, 480),
    'page': avg(300, 1650, 780, 1700),
    't_quanyi':   avg(50, 892, 90, 932),
    't_youhui':   avg(408, 890, 448, 930),
    't_chengke':  avg(712, 890, 752, 930),
    't_kefu':     avg(50, 1188, 90, 1228),
    't_fapiao':   avg(408, 1188, 448, 1228),
    't_guanyu':   avg(712, 1188, 752, 1228),
}
best = None
for y in range(1490, 1630):
    for x in range(120, 960, 2):
        r, g, b = px[x, y]
        if r > 140 and r - g > 50 and r - b > 30:
            s = r - g
            if best is None or s > best[0]:
                best = (s, (x, y), (r, g, b))
colors['red'] = best[2] if best else (226, 105, 98)
print('red sample at', best[1] if best else None)
for k, v in colors.items():
    print(k, v, '#%02X%02X%02X' % tuple(v))

# ---- 头像扫描（蓝底上的圆形头像）----
BG = (66, 146, 245)
def row_extent(y, x0, x1, bg, th=60):
    xs = [x for x in range(x0, x1) if diff(px[x, y], bg) > th]
    return (min(xs), max(xs)) if xs else None
def col_extent(x, y0, y1, bg, th=60):
    ys = [y for y in range(y0, y1) if diff(px[x, y], bg) > th]
    return (min(ys), max(ys)) if ys else None

r = row_extent(355, 10, 430, BG)
c = col_extent(185, 240, 530, BG)
print('avatar row', r, 'col', c)
ax0, ax1 = r; ay0, ay1 = c
side = max(ax1 - ax0, ay1 - ay0) + 4
cx, cy = (ax0 + ax1) // 2, (ay0 + ay1) // 2
avbox = (cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)
print('avbox', avbox)

# ---- 六个瓦片 glyph 检测（饱和像素 bbox）----
tiles = [
    ('quanyi',  40, 882, 350, 1134),
    ('youhui', 398, 880, 666, 1134),
    ('chengke',702, 880, 966, 1134),
    ('kefu',    40, 1178, 350, 1434),
    ('fapiao', 398, 1178, 670, 1434),
    ('guanyu', 702, 1178, 966, 1434),
]
glyphs = {}
for name, x0, y0, x1, y1 in tiles:
    xs = []; ys = []
    for y in range(y0 + 18, y0 + 168):
        for x in range(x0 + 8, x1 - 8):
            if sat(px[x, y]) > 55:
                xs.append(x); ys.append(y)
    bb = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    glyphs[name] = bb
    print('glyph', name, bb, (bb[2] - bb[0], bb[3] - bb[1]))

# ---- 裁切保存 ----
saved = {}
def crop_save(box, name, fmt='PNG', q=90, expand=0, clip=None):
    if expand:
        b = (max(box[0] - expand, clip[0] if clip else 0),
             max(box[1] - expand, clip[1] if clip else 0),
             min(box[2] + expand, clip[2] if clip else W),
             min(box[3] + expand, clip[3] if clip else H))
    else:
        b = box
    cimg = im.crop(b)
    if fmt == 'PNG':
        cimg = cimg.convert('P', palette=Image.ADAPTIVE, colors=128)
    ext = 'png' if fmt == 'PNG' else 'jpg'
    p = os.path.join(OUTDIR, 'm_' + name + '.' + ext)
    cimg.save(p, fmt, **({'quality': q} if fmt == 'JPEG' else {'optimize': True}))
    saved[name] = (p, 'jpeg' if ext == 'jpg' else 'png')
    print('crop', name, b, cimg.size, os.path.getsize(p))

crop_save(avbox, 'avatar', 'JPEG', 88)
crop_save((930, 316, 1034, 412), 'edit', 'PNG')
crop_save((126, 547, 263, 684), 'ord1', 'PNG')
crop_save((469, 547, 607, 684), 'ord2', 'PNG')
crop_save((812, 547, 950, 684), 'ord3', 'PNG')
for name, x0, y0, x1, y1 in tiles:
    bb = glyphs[name]
    crop_save(bb, 'g_' + name, 'PNG', expand=8, clip=(x0, y0, x1, y1))

# ---- 输出 JSON ----
out = {}
for k, (p, mime) in saved.items():
    b = open(p, 'rb').read()
    out[k] = 'data:image/' + mime + ';base64,' + base64.b64encode(b).decode()
json.dump({'colors': {k: list(v) for k, v in colors.items()}, 'icons': out},
          open(os.path.join(OUTDIR, 'mine_b64.json'), 'w'))
tot = sum(len(v) for v in out.values())
print('TOTAL base64 chars:', tot)
for k, v in out.items():
    print(' ', k, len(v))
