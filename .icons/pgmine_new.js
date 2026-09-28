/* ================= 页面：我的（按真实设计 wode.jpg 还原） ================= */
const MINE_ORD=[['全部订单','ord1'],['待支付','ord2'],['未出行','ord3']];
const MINE_FUNC=[
  ['权益','g_quanyi','#FDEDD6',"nav('orders')",'NEW'],
  ['优惠券','g_youhui','#F2FEF4',"toast('原型示意：与本次需求无关','info')",''],
  ['常用乘客','g_chengke','#FBFBF1',"toast('原型示意：与本次需求无关','info')",''],
  ['在线客服','g_kefu','#FAF8F7',"toast('原型示意：与本次需求无关','info')",''],
  ['申请发票','g_fapiao','#E7F3FF',"toast('原型示意：与本次需求无关','info')",''],
  ['关于我们','g_guanyu','#FBF6FC',"toast('原型示意：与本次需求无关','info')",'']
];
function pgMine(){
  const im=k=>'<img src="'+ICON_MINE[k]+'" alt="" style="display:block;width:100%;height:100%">';
  return statusBar(true)+navBar('我的',{cls:'blue'})
    +'<div class="pbody" style="background:#F0F3F6">'
    /* 蓝色头部：头像 + 昵称/手机号 + 编辑 */
    +'<div style="background:#3C95EF;padding:14px 20px 26px;display:flex;align-items:center;gap:14px">'
    +'<div style="width:58px;height:58px;border-radius:50%;overflow:hidden;flex:none;box-shadow:0 0 0 2px rgba(255,255,255,.5)"><img src="'+ICON_MINE.avatar+'" alt="头像" style="display:block;width:106%;height:106%;margin:-3%"></div>'
    +'<div style="flex:1;min-width:0;color:#fff">'
    +'<div style="font-size:17px;font-weight:700">'+(S.loggedIn?S.name:'未登录')+'</div>'
    +'<div style="font-size:13px;opacity:.95;margin-top:5px">'+(S.loggedIn?maskPhone(S.phone):'点击登录壹行天下账号')+'</div>'
    +'</div>'
    +'<div onclick="toast(\'原型示意：编辑个人资料\',\'info\')" style="width:24px;height:24px;flex:none;cursor:pointer">'+im('edit')+'</div>'
    +'</div>'
    /* 三宫格订单入口 */
    +'<div style="background:#fff;border-radius:14px;margin:-8px 14px 0;padding:20px 6px 12px;display:flex;box-shadow:0 6px 16px rgba(50,100,170,.08)">'
    +MINE_ORD.map(t=>'<div onclick="nav(\'orders\')" style="flex:1;display:flex;flex-direction:column;align-items:center;gap:8px;cursor:pointer">'
      +'<div style="width:46px;height:46px">'+im(t[1])+'</div>'
      +'<div style="font-size:12px;color:#3a4250">'+t[0]+'</div></div>').join('')
    +'</div>'
    /* 六宫格功能瓦片（「权益」为本次需求新增入口，NEW 标记） */
    +'<div style="background:#fff;border-radius:14px;margin:14px 14px 0;padding:12px;box-shadow:0 6px 16px rgba(50,100,170,.06)">'
    +'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px">'
    +MINE_FUNC.map(t=>'<div onclick="'+t[3]+'" style="position:relative;background:'+t[2]+';border-radius:10px;height:88px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;cursor:pointer">'
      +'<div style="width:32px;height:32px">'+im(t[1])+'</div>'
      +'<div style="font-size:12px;color:#3a4250">'+t[0]+'</div>'
      +(t[4]?'<span style="position:absolute;top:7px;right:7px;background:#FF6B3D;color:#fff;font-size:8px;line-height:1;padding:2px 5px;border-radius:8px;font-weight:700">'+t[4]+'</span>':'')
      +'</div>').join('')
    +'</div></div>'
    /* 客服电话 */
    +'<div onclick="toast(\'原型示意：拨打客服电话 400-0000-184\',\'info\')" style="background:#fff;border-radius:14px;margin:14px 14px 0;padding:13px;text-align:center;font-size:14px;font-weight:600;color:#FC6262;cursor:pointer">客服电话：400-0000-184</div>'
    +'<div style="height:16px"></div>'
    +'</div>'+tabbar('user');
}
