#!/usr/bin/env python3
"""Gera as artes (JPEG 1080x1350) dos posts do Marketing IA da iTease.
Uso: python3 render_artes.py <arquivo.json> <pasta_saida> [--datas 2026-12-02,2026-12-04]
O JSON tem o formato {"posts":[{"data":..., "slides":[...]}, ...]} (mesmo do painel).
Saída: <pasta_saida>/<data>-<NN>.jpg  (NN = número da lâmina) e imprime a lista de arquivos.
Requer: playwright (python) e Google Chrome em /usr/bin/google-chrome."""
import asyncio, json, sys, os
TPL = r"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
body{margin:0;background:#0B1020}

.sl{width:1080px;height:1350px;position:absolute;left:0;top:0;transform-origin:0 0;overflow:hidden;font-family:"Inter Display",Inter,sans-serif;color:#EEF2FA;
 background:radial-gradient(760px 620px at 0% 0%,rgba(34,211,238,.26),transparent 62%),radial-gradient(820px 700px at 100% 100%,rgba(139,92,246,.30),transparent 62%),
 repeating-linear-gradient(90deg,rgba(148,163,184,.07) 0 2px,transparent 2px 108px),repeating-linear-gradient(0deg,rgba(148,163,184,.05) 0 2px,transparent 2px 108px),#0B1020}
.sl .bar{position:absolute;left:84px;right:84px;top:76px;display:flex;justify-content:space-between;align-items:center}
.sl .tg{font-family:"JetBrains Mono",monospace;font-size:30px;letter-spacing:5px;color:#22D3EE;text-transform:uppercase}
.sl .lg{height:44px}
.sl .ft{position:absolute;left:84px;right:84px;bottom:70px;display:flex;justify-content:space-between;align-items:center;font-family:"JetBrains Mono",monospace;font-size:28px;color:#9AA6C1}
.sl .ft .pg{color:#EEF2FA}
.sl .bd{position:absolute;left:84px;right:84px;top:230px;bottom:190px;display:flex;flex-direction:column;justify-content:center}
.sl h1{color:#EEF2FA;font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:112px;line-height:1.02;letter-spacing:-3px;margin:0}
.sl h1 em,.sl h2 em{font-style:normal;color:#22D3EE}
.sl h2{font-family:"Inter Display",Inter,sans-serif;color:#EEF2FA;font-weight:800;font-size:84px;line-height:1.05;letter-spacing:-2px;margin:0}
.sl .sb{font-family:Inter,sans-serif;font-size:42px;line-height:1.35;color:#B8C3DA;margin-top:44px;font-weight:400}
.sl .bar2{width:150px;height:10px;border-radius:5px;background:linear-gradient(90deg,#22D3EE,#8B5CF6);margin-bottom:56px}
.sl .num{font-family:"JetBrains Mono",monospace;font-weight:600;font-size:150px;line-height:1;color:transparent;-webkit-text-stroke:3px #22D3EE;margin-bottom:34px}
.sl .card{margin-top:54px;background:rgba(18,26,46,.92);border:3px solid #243150;border-radius:34px;padding:38px 44px;font-family:Inter,sans-serif;font-size:36px;line-height:1.4;color:#DCE3F2;display:flex;gap:26px;align-items:flex-start}
.sl .card .ic{flex:none;width:64px;height:64px;border-radius:18px;background:rgba(251,146,60,.16);border:3px solid rgba(251,146,60,.6);color:#FB923C;display:grid;place-items:center;font-weight:800;font-size:38px}
.sl .card.ok .ic{background:rgba(34,211,238,.14);border-color:rgba(34,211,238,.6);color:#22D3EE}
.sl .swipe{display:inline-flex;align-items:center;gap:16px;margin-top:70px;font-family:"JetBrains Mono",monospace;font-size:30px;color:#EEF2FA;border:3px solid rgba(34,211,238,.6);border-radius:999px;padding:18px 34px;width:max-content}
.sl .btnc{margin-top:64px;display:inline-block;background:linear-gradient(90deg,#22D3EE,#8B5CF6);color:#0B1020;font-weight:800;font-size:44px;border-radius:999px;padding:30px 54px;width:max-content;font-family:Inter,sans-serif}
.sl .ct{margin-top:56px;font-family:"JetBrains Mono",monospace;font-size:32px;line-height:1.7;color:#B8C3DA}
.sl .ct b{color:#EEF2FA;font-weight:600}
.sl.u h1{font-size:96px}.sl.u .sb{font-size:38px;margin-top:34px}.sl.u .card{margin-top:40px;font-size:34px;padding:32px 38px}.sl.u .btnc{margin-top:44px;font-size:40px;padding:26px 48px}
.cg{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px}
.cg-i{background:#0D1428;border:1px solid var(--line);border-radius:14px;padding:8px;text-align:left;color:var(--tx);cursor:pointer;font-family:Inter}
.cg-i:hover{border-color:var(--cy)}
.cg-th{position:relative;aspect-ratio:4/5;border-radius:9px;overflow:hidden;background:#0B1020}
.cg-th .stage-sl{position:absolute;inset:0}
.cg-n{position:absolute;left:6px;bottom:6px;background:rgba(0,0,0,.65);color:#fff;font-size:10.5px;border-radius:8px;padding:2px 7px}
.cg-t{font-size:12px;margin-top:8px;color:var(--mut)}.cg-t b{color:var(--cy);font-family:"JetBrains Mono";font-weight:600}
.cg-s{font-size:13px;font-weight:600;margin-top:2px;line-height:1.3}
.cg-w{font-family:"JetBrains Mono";font-size:10.5px;color:var(--or);margin-top:4px}
.lb{position:fixed;inset:0;z-index:45;background:rgba(3,6,14,.94);overflow:auto;padding:24px 16px}
.lb-in{max-width:980px;margin:0 auto;position:relative}
.lb-x{position:absolute;right:0;top:0;width:38px;height:38px;border-radius:50%;border:1px solid var(--line);background:#121A2E;color:var(--tx);font-size:16px;cursor:pointer;z-index:2}
.lb-nav{display:flex;gap:8px;margin:0 50px 10px 0}
.lb .pv{background:#0F1629}
@media (max-width:900px){.cg{grid-template-columns:repeat(2,1fr)}.lb{padding:12px 8px}}

/* ---------- pedidos ---------- */
.pd{display:grid;grid-template-columns:minmax(0,440px) 1fr;gap:18px;align-items:start}
.pd-form{background:rgba(18,26,46,.85);border:1px solid var(--line);border-radius:20px;padding:20px}
.pd-form h2{margin:4px 0 12px}
.pd-form textarea,.pd-form input[type=text],.pd-form input[type=date]{width:100%;background:#0B1020;border:1px solid var(--line);border-radius:12px;padding:12px;font:14px/1.5 Inter;color:var(--tx);color-scheme:dark}
.pd-form textarea:focus,.pd-form input:focus{outline:none;border-color:rgba(34,211,238,.6)}
.pd-l{font-family:"JetBrains Mono";font-size:10.5px;letter-spacing:1.5px;color:var(--mut);text-transform:uppercase;margin:14px 0 7px}
.pd-l small{text-transform:none;letter-spacing:0;font-family:Inter;font-size:11.5px}
.pills{display:flex;flex-wrap:wrap;gap:7px}
.pills label{cursor:pointer}
.pills input{position:absolute;opacity:0;pointer-events:none}
.pills span{display:inline-block;padding:8px 12px;border-radius:999px;border:1px solid var(--line);font-size:13px;color:var(--mut);background:#0F1629}
.pills input:checked+span{border-color:rgba(34,211,238,.6);color:var(--tx);background:rgba(34,211,238,.1)}
.pills input:focus-visible+span{outline:2px solid var(--cy)}
.pd-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.pd-note{font-size:12px;color:var(--mut);margin-top:10px;line-height:1.45}
.pd-list .sec{font-family:"JetBrains Mono";font-size:10.5px;letter-spacing:1.5px;color:var(--mut);margin:4px 0 10px;text-transform:uppercase}
.rq{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;margin-bottom:10px}
.rq.done{border-left:3px solid var(--gr)}.rq.wait{border-left:3px solid var(--or)}.rq.run{border-left:3px solid var(--cy)}
.rq-h{display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap}
.rq-id{font-family:"JetBrains Mono";font-size:10.5px;color:var(--mut)}
.rq-t{font-size:14px;line-height:1.45;margin:6px 0 8px;white-space:pre-wrap}
.rq-m{display:flex;gap:6px;flex-wrap:wrap;align-items:center;font-size:11.5px;color:var(--mut)}
.rq-a{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.rq-a .btn2{padding:8px 12px;font-size:12.5px}
.run-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--cy);margin-right:4px;animation:blink 1s infinite}
@media (max-width:900px){.pd{grid-template-columns:1fr}.pd-row{grid-template-columns:1fr}}

.sl.u h1{font-size:96px}.sl.u .sb{font-size:38px;margin-top:34px}.sl.u .card{margin-top:40px;font-size:34px;padding:32px 38px}.sl.u .btnc{margin-top:44px;font-size:40px;padding:26px 48px}
.sl .bgx{position:absolute;inset:0;pointer-events:none}
.sl .bar,.sl .bd,.sl .ft{z-index:2}
.sl .ilu{position:absolute;right:70px;top:170px;width:270px;height:270px;z-index:1;opacity:.95}
.sl .ilu svg,.sl .ilu2 svg{width:100%;height:100%}
.sl .ilu2{display:inline-block;width:150px;height:150px;vertical-align:top;margin-left:34px}
.sl .nrow{display:flex;align-items:flex-end;margin-bottom:34px}.sl .nrow .num{margin-bottom:0}
.sl .big{font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:200px;line-height:.9;letter-spacing:-6px;margin-bottom:26px;background:linear-gradient(90deg,#22D3EE,#8B5CF6);-webkit-background-clip:text;background-clip:text;color:transparent}
.sl .big small{font-size:72px;letter-spacing:-1px;margin-left:14px}
.sl.has-ilu .bd h1{padding-right:250px}
/* claro */
.sl.st-claro{background:radial-gradient(700px 600px at 100% 0%,rgba(34,211,238,.18),transparent 60%),radial-gradient(700px 600px at 0% 100%,rgba(139,92,246,.14),transparent 60%),repeating-linear-gradient(90deg,rgba(11,26,51,.05) 0 2px,transparent 2px 108px),#F4F7FC;color:#0B1A33}
.sl.st-claro h1,.sl.st-claro h2{color:#0B1A33}.sl.st-claro h1 em,.sl.st-claro h2 em{color:#0891B2}
.sl.st-claro .sb{color:#334155}.sl.st-claro .tg{color:#0891B2}.sl.st-claro .ft{color:#475569}.sl.st-claro .ft .pg{color:#0B1A33}
.sl.st-claro .lgw,.sl.st-gradiente .lgw{background:#0B1020;border-radius:999px;padding:14px 26px}
.sl.st-claro .card{background:#fff;border-color:#CBD5E1;color:#1E293B}.sl.st-claro .ct{color:#334155}.sl.st-claro .ct b{color:#0B1A33}
.sl.st-claro .swipe{color:#0B1A33;border-color:#0891B2}.sl.st-claro .num{-webkit-text-stroke-color:#0891B2}
/* gradiente */
.sl.st-gradiente{background:radial-gradient(900px 700px at 0% 0%,rgba(255,255,255,.22),transparent 60%),linear-gradient(135deg,#22D3EE 0%,#6D8BF2 50%,#8B5CF6 100%);color:#0B1A33}
.sl.st-gradiente h1,.sl.st-gradiente h2{color:#0B1A33}.sl.st-gradiente h1 em,.sl.st-gradiente h2 em{color:#22D3EE;background:#0B1020;padding:0 14px;border-radius:12px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sl.st-gradiente .sb{color:#13203B}.sl.st-gradiente .tg{color:#0B1A33}.sl.st-gradiente .ft,.sl.st-gradiente .ft .pg{color:#0B1A33}
.sl.st-gradiente .bar2{background:#0B1020}.sl.st-gradiente .btnc{background:#0B1020;color:#22D3EE}
.sl.st-gradiente .card{background:rgba(11,16,32,.88);border-color:rgba(11,16,32,.9)}.sl.st-gradiente .ct,.sl.st-gradiente .ct b{color:#0B1A33}
.sl.st-gradiente .swipe{color:#0B1A33;border-color:#0B1020}.sl.st-gradiente .num{-webkit-text-stroke-color:#0B1020}
.sl.st-gradiente .big{background:none;color:#0B1020}
/* violeta */
.sl.st-violeta{background:radial-gradient(800px 700px at 100% 0%,rgba(139,92,246,.45),transparent 62%),radial-gradient(700px 600px at 0% 100%,rgba(34,211,238,.18),transparent 60%),repeating-linear-gradient(90deg,rgba(196,181,253,.06) 0 2px,transparent 2px 108px),#160E33}
.sl.st-violeta .card{background:rgba(30,20,70,.9);border-color:#3B2A7A}
/* alerta */
.sl.st-alerta{background:radial-gradient(760px 620px at 100% 0%,rgba(251,146,60,.30),transparent 62%),repeating-linear-gradient(135deg,rgba(251,146,60,.10) 0 26px,transparent 26px 90px) 0 0/100% 70px no-repeat,repeating-linear-gradient(90deg,rgba(148,163,184,.06) 0 2px,transparent 2px 108px),#0B1020}
.sl.st-alerta h1 em,.sl.st-alerta h2 em,.sl.st-alerta .tg{color:#FB923C}
.sl.st-alerta .bar2{background:linear-gradient(90deg,#FB923C,#F43F5E)}.sl.st-alerta .btnc{background:linear-gradient(90deg,#FB923C,#F97316);color:#1A0E05}
.sl.st-alerta .card.ok .ic{background:rgba(251,146,60,.16);border-color:rgba(251,146,60,.6);color:#FB923C}.sl.st-alerta .num{-webkit-text-stroke-color:#FB923C}
.sl.st-alerta .swipe{border-color:rgba(251,146,60,.7)}
.sl.st-alerta .big{background:linear-gradient(90deg,#FB923C,#F43F5E);-webkit-background-clip:text;background-clip:text}
</style></head><body><div id="host" style="position:relative;width:1080px;height:1350px;overflow:hidden"></div>
<script>
const LOGO="data:image/png;base64,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";
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const hl=s=>esc(s).replace(/\*([^*]+)\*/g,"<em>$1</em>");
const ILU=(()=>{const C="#22D3EE",V="#8B5CF6",a=`fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="7"`;
const g=`<defs><linearGradient id="ig" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${C}"/><stop offset="1" stop-color="${V}"/></linearGradient></defs>`;
const w=b=>`<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">${g}<circle cx="100" cy="100" r="92" fill="${C}" fill-opacity=".08" stroke="url(#ig)" stroke-opacity=".35" stroke-width="3"/>${b}</svg>`;
return{
escudo:w(`<path d="M100 38l52 20v40c0 36-24 58-52 68-28-10-52-32-52-68V58z" stroke="url(#ig)" ${a}/><path d="M76 100l17 17 33-36" stroke="${C}" ${a}/>`),
cadeado:w(`<rect x="58" y="92" width="84" height="66" rx="14" stroke="url(#ig)" ${a}/><path d="M74 92V72a26 26 0 0152 0v20" stroke="${C}" ${a}/><circle cx="100" cy="122" r="9" fill="${C}"/>`),
nuvem:w(`<path d="M66 138h74a28 28 0 000-56 40 40 0 00-76 10 24 24 0 002 46z" stroke="url(#ig)" ${a}/><path d="M100 104v40m-15-15l15 15 15-15" stroke="${C}" ${a}/>`),
notebook:w(`<rect x="52" y="62" width="96" height="64" rx="8" stroke="url(#ig)" ${a}/><path d="M38 142h124" stroke="${C}" ${a}/><path d="M74 94h52M74 110h30" stroke="${V}" ${a}/>`),
celular:w(`<rect x="70" y="40" width="60" height="120" rx="12" stroke="url(#ig)" ${a}/><path d="M92 144h16" stroke="${C}" ${a}/><path d="M84 72h32M84 90h22" stroke="${V}" ${a}/>`),
impressora:w(`<rect x="50" y="84" width="100" height="50" rx="10" stroke="url(#ig)" ${a}/><path d="M70 84V52h60v32M70 120h60v34H70z" stroke="${C}" ${a}/>`),
calendario:w(`<rect x="50" y="56" width="100" height="94" rx="12" stroke="url(#ig)" ${a}/><path d="M50 84h100M76 44v22M124 44v22" stroke="${C}" ${a}/><path d="M74 108h12M100 108h12M74 128h12" stroke="${V}" ${a}/>`),
grafico:w(`<path d="M50 150h104" stroke="url(#ig)" ${a}/><path d="M66 150v-34M92 150v-56M118 150v-42M144 150v-74" stroke="${C}" ${a}/><path d="M60 104l30-26 26 14 32-36" stroke="${V}" ${a}/>`),
presente:w(`<rect x="54" y="88" width="92" height="66" rx="8" stroke="url(#ig)" ${a}/><path d="M48 72h104v18H48zM100 72v82" stroke="${C}" ${a}/><path d="M100 72c-10-24-34-24-34-8s24 8 34 8c10 0 34 8 34-8s-24-16-34 8" stroke="${V}" ${a}/>`),
ia:w(`<rect x="62" y="62" width="76" height="76" rx="14" stroke="url(#ig)" ${a}/><path d="M84 46v16M116 46v16M84 138v16M116 138v16M46 84h16M46 116h16M138 84h16M138 116h16" stroke="${C}" ${a}/><text x="100" y="112" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="34" fill="${V}">IA</text>`),
predio:w(`<path d="M62 158V52h52v106M114 84h28v74" stroke="url(#ig)" ${a}/><path d="M76 72h8M92 72h8M76 92h8M92 92h8M76 112h8M92 112h8M126 104h4M126 124h4M84 158v-22h12v22" stroke="${C}" ${a}/>`),
servidor:w(`<rect x="56" y="48" width="88" height="30" rx="7" stroke="url(#ig)" ${a}/><rect x="56" y="86" width="88" height="30" rx="7" stroke="url(#ig)" ${a}/><rect x="56" y="124" width="88" height="30" rx="7" stroke="url(#ig)" ${a}/><path d="M72 63h6M72 101h6M72 139h6" stroke="${C}" ${a}/><path d="M104 63h24M104 101h24M104 139h24" stroke="${V}" ${a}/>`),
email:w(`<rect x="46" y="62" width="108" height="76" rx="10" stroke="url(#ig)" ${a}/><path d="M50 68l50 38 50-38" stroke="${C}" ${a}/>`)};})();
function panoBG(i,n,st){
  const W=1080*n,H=1350,x=-i*1080;let c1="#22D3EE",c2="#8B5CF6";if(st==="alerta"){c1="#FB923C";c2="#F43F5E"}else if(st==="claro"){c1="#0891B2";c2="#7C3AED"}else if(st==="gradiente"){c1="#0B1020";c2="#0B1020"}
  let pts="",dots="";const k=Math.max(3,n*2);for(let j=0;j<=k*4;j++){const px=j*W/(k*4),py=1150+Math.sin(j/k*Math.PI*1.6)*80+Math.cos(j/3)*14;pts+=`${j?"L":"M"}${px.toFixed(0)} ${py.toFixed(0)} `;if(j%4===2)dots+=`<circle cx="${px.toFixed(0)}" cy="${py.toFixed(0)}" r="13" fill="${c1}"/><circle cx="${px.toFixed(0)}" cy="${py.toFixed(0)}" r="30" fill="none" stroke="${c1}" stroke-opacity=".4" stroke-width="3"/>`}
  let circ="";for(let j=0;j<n;j++){circ+=`<circle cx="${j*1080+(j%2?260:820)}" cy="${j%2?1080:300}" r="${j%2?300:380}" fill="none" stroke="${c2}" stroke-opacity=".22" stroke-width="4"/>`;if(j<n-1)circ+=`<circle cx="${(j+1)*1080}" cy="1150" r="150" fill="${c2}" fill-opacity=".10" stroke="${c1}" stroke-opacity=".35" stroke-width="3"/>`}
  return `<svg class="bgx" style="left:${x}px;width:${W}px;height:${H}px;inset:auto;top:0" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">${circ}<path d="${pts}" fill="none" stroke="${c1}" stroke-opacity=".55" stroke-width="5"/>${dots}</svg>`;
}
function slideHTML(s,i,n,post){
  const tag=s.tag||("// "+(post.pilar||"iTease"));
  const st=(s.estilo||post.estilo||"escuro").toLowerCase();
  const ilu=s.ilustracao&&ILU[String(s.ilustracao).toLowerCase()];
  const pg=n>1?`<span class="pg">${String(i+1).padStart(2,"0")} / ${String(n).padStart(2,"0")}</span>`:`<span class="pg">@iteasesolucoes</span>`;
  let bd="",extra="";
  const t=s.tipo||"capa";
  const big=s.grande?(()=>{const m=String(s.grande).trim().split(/\s+/);return `<div class="big">${esc(m[0])}${m.length>1?`<small>${esc(m.slice(1).join(" "))}</small>`:""}</div>`})():"";
  if(t==="capa"||t==="unica"){
    if(ilu)extra=`<div class="ilu">${ilu}</div>`;
    bd=`${big||'<div class="bar2"></div>'}<h1>${hl(s.titulo)}</h1>${s.subtitulo?`<div class="sb">${hl(s.subtitulo)}</div>`:""}`+
      (s.destaque?`<div class="card ok"><div class="ic">✓</div><div>${hl(s.destaque)}</div></div>`:"")+
      (t==="capa"&&n>1?`<div class="swipe">Deslize para o lado  →</div>`:"")+
      (t==="unica"&&s.cta?`<div class="btnc">${esc(s.cta)}</div>`:"");
  }else if(t==="item"){
    bd=`<div class="nrow"><div class="num">${esc(s.numero||String(i).padStart(2,"0"))}</div>${ilu?`<div class="ilu2">${ilu}</div>`:""}</div><h2>${hl(s.titulo)}</h2>${s.texto?`<div class="sb">${hl(s.texto)}</div>`:""}`+
      (s.destaque?`<div class="card"><div class="ic">!</div><div>${hl(s.destaque)}</div></div>`:"");
  }else{
    bd=`<div class="bar2"></div><h2>${hl(s.titulo)}</h2>${s.texto?`<div class="sb">${hl(s.texto)}</div>`:""}<div class="btnc">${esc(s.cta||"Agende um diagnóstico gratuito")}</div>
      <div class="ct"><b>(19) 3935-6234</b><br>www.itease.com.br · @iteasesolucoes</div>`;
  }
  const pano=post.panoramico&&n>1?panoBG(i,n,st):"";
  const cls=`sl${t==="unica"?" u":""}${st!=="escuro"?" st-"+st:""}${ilu&&(t==="capa"||t==="unica")?" has-ilu":""}`;
  return `<div class="${cls}">${pano}${extra}<div class="bar"><span class="tg">${esc(tag)}</span><span class="lgw"><img class="lg" src="${LOGO}" alt="iTease" style="display:block"></span></div><div class="bd">${bd}</div><div class="ft"><span>www.itease.com.br</span>${pg}</div></div>`;
}
window.render=(post,i)=>{document.getElementById("host").innerHTML=slideHTML(post.slides[i],i,post.slides.length,post);};
</script></body></html>"""
async def main():
    src, out = sys.argv[1], sys.argv[2]
    datas = None
    if "--datas" in sys.argv: datas = set(sys.argv[sys.argv.index("--datas")+1].split(","))
    data = json.load(open(src, encoding="utf-8-sig"))
    os.makedirs(out, exist_ok=True)
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":1080,"height":1350}, device_scale_factor=1)
        await pg.set_content(TPL)
        for post in data.get("posts", []):
            if datas and post.get("data") not in datas: continue
            for i in range(len(post.get("slides", []))):
                await pg.evaluate("([p,i])=>window.render(p,i)", [post, i])
                await pg.wait_for_timeout(150)
                f = os.path.join(out, f"{post['data']}-{i+1:02d}.jpg")
                await pg.locator("#host").screenshot(path=f, type="jpeg", quality=90)
                print(f)
        await b.close()
asyncio.run(main())
