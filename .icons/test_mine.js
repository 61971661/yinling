const fs = require('fs');
const HTML = 'C:/Users/61971/WorkBuddy/2026-09-28-09-29-37/index.html';
const html = fs.readFileSync(HTML, 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const code = scripts[scripts.length - 1];
console.log('scripts:', scripts.length, 'main code length:', code.length);

const els = {};
function el(id) {
  return els[id] || (els[id] = {
    id, innerHTML: '', value: '', style: {}, checked: false, src: '',
    classList: { add() {}, remove() {}, toggle() {} },
    addEventListener() {}, appendChild() {}
  });
}
global.document = { getElementById: el, querySelectorAll: () => [], createElement: () => el('_c' + Math.random()), body: { appendChild() {} } };
global.window = global;
global.alert = () => {};
global.confirm = () => true;

(0, eval)(code + '\n;globalThis.__S=S;globalThis.__render=render;globalThis.__nav=nav;globalThis.__ICON_MINE=ICON_MINE;globalThis.__PAGES=PAGES;');

let pass = 0, fail = 0;
function chk(name, cond) {
  if (cond) { pass++; console.log('PASS', name); }
  else { fail++; console.log('FAIL', name); }
}

// 0) ICON_MINE 素材完整
const IM = globalThis.__ICON_MINE;
const keys = ['avatar', 'edit', 'ord1', 'ord2', 'ord3', 'g_quanyi', 'g_youhui', 'g_chengke', 'g_kefu', 'g_fapiao', 'g_guanyu'];
chk('ICON_MINE 11 keys', IM && keys.every(k => typeof IM[k] === 'string' && IM[k].startsWith('data:image/')));
chk('avatar is jpeg', IM.avatar.startsWith('data:image/jpeg'));
chk('glyphs are png', ['g_quanyi', 'g_youhui', 'g_chengke', 'g_kefu', 'g_fapiao', 'g_guanyu'].every(k => IM[k].startsWith('data:image/png')));

const S = globalThis.__S, render = globalThis.__render, doNav = globalThis.__nav, PAGES = globalThis.__PAGES;

// 1) 未登录态「我的」页渲染
S.loggedIn = false; S.page = 'mine'; S.stack = []; render();
let h = els.screen.innerHTML;
chk('mine: 未登录文案', h.includes('未登录') && h.includes('点击登录壹行天下账号'));
chk('mine: 头像图', h.includes(IM.avatar.slice(0, 60)));
chk('mine: 三宫格', ['全部订单', '待支付', '未出行'].every(t => h.includes(t)));
chk('mine: 六瓦片', ['权益', '优惠券', '常用乘客', '在线客服', '申请发票', '关于我们'].every(t => h.includes(t)));
chk('mine: NEW 角标', h.includes('>NEW</span>'));
chk('mine: 客服电话', h.includes('客服电话：400-0000-184'));
chk('mine: 我的 tab 选中', /class="ti on"[^>]*/.test(h) && h.includes('我的'));
chk('mine: 蓝头部 #3C95EF', h.includes('#3C95EF'));
chk('mine: 权益瓦片跳订单', h.includes('onclick="nav(\'orders\')"'));
chk('mine: 六宫格 grid', h.includes('grid-template-columns:1fr 1fr 1fr'));

// 2) 已登录态
S.loggedIn = true; S.name = '微信用户'; S.phone = '15811012151'; render();
h = els.screen.innerHTML;
chk('mine: 昵称', h.includes('微信用户'));
chk('mine: 手机号脱敏', h.includes('158****2151'));

// 3) 权益瓦片 → 订单列表
doNav('orders');
chk('nav orders works', S.page === 'orders');
render();
h = els.screen.innerHTML;
chk('orders page renders', h.includes('权益卡订单'));

// 4) 回归：其余页面渲染不抛异常
for (const p of ['home', 'purchase', 'login', 'paySuccess', 'payIssue', 'yinling']) {
  let ok = true;
  try { S.page = p; render(); } catch (e) { ok = false; console.log('  err@' + p, e.message); }
  chk('regression: ' + p, ok);
}

console.log('\nRESULT: pass=' + pass + ' fail=' + fail);
process.exit(fail ? 1 : 0);
