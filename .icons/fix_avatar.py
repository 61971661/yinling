# -*- coding: utf-8 -*-
"""flood fill 精确提取头像圆 + 复核瓦片底色"""
from PIL import Image
import json, base64, os
from collections import deque

SRC = 'D:/中交信/21-银龄出行/wode.jpg'
OUTDIR = 'C:/Users/61971/WorkBuddy/2026-09-28-09-29-37/.icons'
im = Image.open(SRC).convert('RGB')
W, H = im.size
px = im.load()
BG = (60, 149, 239)
def diff(p, bg): return sum(abs(a - b) for a, b in zip(p, bg))

# 种子点取头像中心（此前裁块内约 (95,140) → 原图 (164,362)）
seed = (164, 362)
print('seed color', px[seed[0], seed[1]])
th = 45
seen = set()
q = deque([seed])
xs = []; ys = []
X0, Y0, X1, Y1 = 0, 150, 460, 620
while q:
    x, y = q.popleft()
    if (x, y) in seen: continue
    seen.add((x, y))
    if not (X0 <= x < X1 and Y0 <= y < Y1): continue
    if diff(px[x, y], BG) <= th: continue
    xs.append(x); ys.append(y)
    q.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
bb = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
print('avatar flood bbox', bb, 'w', bb[2]-bb[0], 'h', bb[3]-bb[1])

side = max(bb[2]-bb[0], bb[3]-bb[1]) + 2
cx, cy = (bb[0]+bb[2])//2, (bb[1]+bb[3])//2
avbox = (cx-side//2, cy-side//2, cx+side//2, cy+side//2)
print('avbox', avbox, 'side', side)

cimg = im.crop(avbox)
p = os.path.join(OUTDIR, 'm_avatar.jpg')
cimg.save(p, 'JPEG', quality=88)
b = open(p, 'rb').read()
new_av = 'data:image/jpeg;base64,' + base64.b64encode(b).decode()
print('avatar jpg', os.path.getsize(p), 'b64', len(new_av))

# 瓦片底色多点复核
def avg(x0, y0, x1, y1):
    rs = gs = bs = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, bb2 = px[x, y]; rs += r; gs += g; bs += bb2; n += 1
    return (rs//n, gs//n, bs//n)
for label, box in [
    ('kefu A(60,1270,100,1290)', (60, 1270, 100, 1290)),
    ('kefu B(300,1400,340,1420)', (300, 1400, 340, 1420)),
    ('kefu C(55,1200,95,1225)', (55, 1200, 95, 1225)),
    ('quanyi A(60,950,100,1000)', (60, 950, 100, 1000)),
    ('quanyi B(300,1050,340,1090)', (300, 1050, 340, 1090)),
]:
    v = avg(*box)
    print(label, v, '#%02X%02X%02X' % v)

J = json.load(open(os.path.join(OUTDIR, 'mine_b64.json')))
J['icons']['avatar'] = new_av
json.dump(J, open(os.path.join(OUTDIR, 'mine_b64.json'), 'w'))
print('json updated; total b64', sum(len(v) for v in J['icons'].values()))
