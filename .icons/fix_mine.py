# -*- coding: utf-8 -*-
"""修正：头像精确扫描 + 两个瓦片底色重取样，更新 mine_b64.json"""
from PIL import Image
import json, base64, os

SRC = 'D:/中交信/21-银龄出行/wode.jpg'
OUTDIR = 'C:/Users/61971/WorkBuddy/2026-09-28-09-29-37/.icons'
im = Image.open(SRC).convert('RGB')
W, H = im.size
px = im.load()
BG = (60, 149, 239)

def diff(p, bg): return sum(abs(a - b) for a, b in zip(p, bg))
def row_extent(y, x0, x1, th=60):
    xs = [x for x in range(x0, x1) if diff(px[x, y], BG) > th]
    return (min(xs), max(xs)) if xs else None
def col_extent(x, y0, y1, th=60):
    ys = [y for y in range(y0, y1) if diff(px[x, y], BG) > th]
    return (min(ys), max(ys)) if ys else None
def avg(x0, y0, x1, y1):
    rs = gs = bs = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]; rs += r; gs += g; bs += b; n += 1
    return (rs // n, gs // n, bs // n)

# 头像：x=160 列扫描 y 250-475（避开下方白卡 y>=485）
c = col_extent(160, 250, 478)
print('col@160', c)
ymid = (c[0] + c[1]) // 2
r = row_extent(ymid, 30, 336)   # x 上限 336，避开昵称文字
print('row@%d' % ymid, r)
ax0, ax1 = r; ay0, ay1 = c
side = max(ax1 - ax0, ay1 - ay0) + 2
cx, cy = (ax0 + ax1) // 2, (ay0 + ay1) // 2
avbox = (cx - side // 2, cy - side // 2, cx + side // 2, cy + side // 2)
print('avbox', avbox, 'side', side)

# 瓦片底色重取样（glyph 左侧纯底区）
q = avg(60, 950, 120, 1000)   # 权益 glyph(195..270) 左侧
k = avg(60, 1250, 120, 1300)  # 客服 glyph(201..262) 左侧
print('t_quanyi', q, '#%02X%02X%02X' % q)
print('t_kefu', k, '#%02X%02X%02X' % k)

# 重新裁头像（JPEG）
cimg = im.crop(avbox)
p = os.path.join(OUTDIR, 'm_avatar.jpg')
cimg.save(p, 'JPEG', quality=88)
b = open(p, 'rb').read()
new_av = 'data:image/jpeg;base64,' + base64.b64encode(b).decode()
print('avatar jpg size', os.path.getsize(p), 'b64 len', len(new_av))

# 更新 JSON
J = json.load(open(os.path.join(OUTDIR, 'mine_b64.json')))
J['icons']['avatar'] = new_av
J['colors']['t_quanyi'] = list(q)
J['colors']['t_kefu'] = list(k)
json.dump(J, open(os.path.join(OUTDIR, 'mine_b64.json'), 'w'))
print('json updated; total b64', sum(len(v) for v in J['icons'].values()))
print('colors:', {kk: '#%02X%02X%02X' % tuple(vv) for kk, vv in J['colors'].items()})
