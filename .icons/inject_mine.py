# -*- coding: utf-8 -*-
"""注入 ICON_MINE 常量 + 替换 pgMine 函数"""
import json, os

HTML = 'C:/Users/61971/WorkBuddy/2026-09-28-09-29-37/壹行天下银龄出行权益卡-小程序原型.html'
DIR = 'C:/Users/61971/WorkBuddy/2026-09-28-09-29-37/.icons'

J = json.load(open(os.path.join(DIR, 'mine_b64.json')))
icons = J['icons']
order = ['avatar', 'edit', 'ord1', 'ord2', 'ord3', 'g_quanyi', 'g_youhui', 'g_chengke', 'g_kefu', 'g_fapiao', 'g_guanyu']
assert set(order) == set(icons.keys()), set(icons.keys()) ^ set(order)

lines = ['/* 「我的」页真实图标（裁自设计图 wode.jpg） */\nconst ICON_MINE={']
parts = []
for k in order:
    parts.append(k + ":'" + icons[k] + "'")
lines.append(','.join(parts))
lines.append('};')
ICON_MINE_JS = '\n'.join(lines)
print('ICON_MINE js length', len(ICON_MINE_JS))

NEW_FN = open(os.path.join(DIR, 'pgmine_new.js'), encoding='utf-8').read()
if not NEW_FN.endswith('\n'):
    NEW_FN += '\n'

s = open(HTML, encoding='utf-8').read()
orig_len = len(s)

# 1) 注入 ICON_MINE：插到 const ICON_IMG={...}; 块之后
i = s.find('const ICON_IMG={')
assert i >= 0, 'ICON_IMG not found'
j = s.find('};', i)
assert j > i, 'ICON_IMG end not found'
insert_at = j + 2
s = s[:insert_at] + '\n' + ICON_MINE_JS + '\n' + s[insert_at:]
print('ICON_MINE injected at', insert_at)

# 2) 替换 pgMine 整段（从「页面：我的」注释到「页面：订单列表」注释前）
a = s.find('/* ================= 页面：我的')
assert a >= 0, 'pgMine comment not found'
b = s.find('/* ================= 页面：订单列表', a)
assert b > a, 'orders comment not found'
old_seg = s[a:b]
assert 'function pgMine' in old_seg and old_seg.count('function pgMine') == 1
assert "tabbar('user')" in old_seg
s = s[:a] + NEW_FN + s[b:]
print('pgMine replaced: old', len(old_seg), '-> new', len(NEW_FN))

open(HTML, 'w', encoding='utf-8').write(s)
print('HTML size', orig_len, '->', len(s))

# 校验
s2 = open(HTML, encoding='utf-8').read()
assert s2.count('function pgMine') == 1, s2.count('function pgMine')
assert 'const ICON_MINE={' in s2
assert s2.count('ICON_MINE') >= 2
print('verify OK: pgMine x1, ICON_MINE present')
