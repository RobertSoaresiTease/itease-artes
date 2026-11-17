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
/* ---------- estilos das artes (v2: estilos, ilustrações e carrossel panorâmico) ---------- */
.sl .bgl{position:absolute;top:0;bottom:0;left:0;width:1080px;z-index:0}
.sl .bar,.sl .bd,.sl .ft{z-index:3}
.sl .ill{position:absolute;z-index:2}
.sl .ill svg,.sl .pnl svg{display:block}
.sl .pnl{position:absolute;top:0;height:1350px;z-index:1}
.sl .lgp{display:inline-flex;align-items:center;background:#0B1020;border-radius:999px;padding:12px 24px}
.bgl.b-escuro{background:radial-gradient(760px 620px at 0% 0%,rgba(34,211,238,.26),transparent 62%),radial-gradient(820px 700px at 100% 100%,rgba(139,92,246,.30),transparent 62%),repeating-linear-gradient(90deg,rgba(148,163,184,.07) 0 2px,transparent 2px 108px),repeating-linear-gradient(0deg,rgba(148,163,184,.05) 0 2px,transparent 2px 108px),#0B1020}
.bgl.b-claro{background:radial-gradient(760px 620px at 100% 0%,rgba(34,211,238,.20),transparent 62%),radial-gradient(820px 700px at 0% 100%,rgba(139,92,246,.16),transparent 62%),repeating-linear-gradient(90deg,rgba(11,16,32,.05) 0 2px,transparent 2px 108px),repeating-linear-gradient(0deg,rgba(11,16,32,.04) 0 2px,transparent 2px 108px),#F4F7FC}
.bgl.b-gradiente{background:radial-gradient(700px 600px at 88% 8%,rgba(255,255,255,.30),transparent 60%),repeating-linear-gradient(90deg,rgba(11,16,32,.07) 0 2px,transparent 2px 108px),repeating-linear-gradient(0deg,rgba(11,16,32,.05) 0 2px,transparent 2px 108px),linear-gradient(135deg,#22D3EE 0%,#8B5CF6 100%)}
.bgl.b-violeta{background:radial-gradient(900px 700px at 100% 0%,rgba(139,92,246,.55),transparent 62%),radial-gradient(700px 600px at 0% 100%,rgba(34,211,238,.22),transparent 62%),repeating-radial-gradient(circle at 50% 50%,rgba(255,255,255,.035) 0 2px,transparent 2px 54px),#160E33}
.bgl.b-alerta{background:radial-gradient(800px 640px at 100% 0%,rgba(251,146,60,.30),transparent 62%),radial-gradient(700px 600px at 0% 100%,rgba(139,92,246,.20),transparent 62%),repeating-linear-gradient(135deg,rgba(251,146,60,.06) 0 22px,transparent 22px 64px),#0B1020}
/* panorâmico: a camada larga recebe o fundo, sem cantos que criem emenda */
.pnl.b-escuro{background:radial-gradient(1200px 700px at 30% 10%,rgba(34,211,238,.20),transparent 62%),radial-gradient(1200px 760px at 75% 95%,rgba(139,92,246,.26),transparent 62%),repeating-linear-gradient(90deg,rgba(148,163,184,.07) 0 2px,transparent 2px 108px),repeating-linear-gradient(0deg,rgba(148,163,184,.05) 0 2px,transparent 2px 108px),#0B1020}
.pnl.b-claro{background:radial-gradient(1200px 700px at 25% 5%,rgba(34,211,238,.18),transparent 62%),radial-gradient(1200px 760px at 80% 100%,rgba(139,92,246,.15),transparent 62%),repeating-linear-gradient(90deg,rgba(11,16,32,.05) 0 2px,transparent 2px 108px),repeating-linear-gradient(0deg,rgba(11,16,32,.04) 0 2px,transparent 2px 108px),#F4F7FC}
.pnl.b-gradiente{background:repeating-linear-gradient(90deg,rgba(11,16,32,.07) 0 2px,transparent 2px 108px),repeating-linear-gradient(0deg,rgba(11,16,32,.05) 0 2px,transparent 2px 108px),linear-gradient(100deg,#22D3EE 0%,#8B5CF6 100%)}
.pnl.b-violeta{background:radial-gradient(1300px 800px at 60% 0%,rgba(139,92,246,.50),transparent 62%),radial-gradient(1000px 700px at 20% 100%,rgba(34,211,238,.18),transparent 62%),#160E33}
.pnl.b-alerta{background:radial-gradient(1300px 760px at 50% 0%,rgba(251,146,60,.24),transparent 62%),repeating-linear-gradient(135deg,rgba(251,146,60,.06) 0 22px,transparent 22px 64px),#0B1020}
/* claro */
.sl.s-claro{color:#0B1020}
.sl.s-claro h1,.sl.s-claro h2{color:#0B1020}
.sl.s-claro h1 em,.sl.s-claro h2 em{color:#0891B2}
.sl.s-claro .sb{color:#3B4763}.sl.s-claro .tg{color:#0891B2}
.sl.s-claro .ft{color:#5B6785}.sl.s-claro .ft .pg{color:#0B1020}
.sl.s-claro .card{background:#FFFFFF;border-color:#D5DEEE;color:#1E293B}
.sl.s-claro .num{-webkit-text-stroke-color:#0891B2}
.sl.s-claro .swipe{color:#0B1020;border-color:rgba(8,145,178,.55)}
.sl.s-claro .ct{color:#3B4763}.sl.s-claro .ct b{color:#0B1020}
.sl.s-claro .big{color:#0891B2}
/* gradiente */
.sl.s-gradiente{color:#0B1020}
.sl.s-gradiente h1,.sl.s-gradiente h2{color:#0B1020}
.sl.s-gradiente h1 em,.sl.s-gradiente h2 em{color:#22D3EE;background:#0B1020;padding:0 14px;border-radius:14px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.sl.s-gradiente .sb{color:#13203B}.sl.s-gradiente .tg{color:#0B1020}
.sl.s-gradiente .ft{color:#1B2440}.sl.s-gradiente .ft .pg{color:#0B1020}
.sl.s-gradiente .card{background:rgba(11,16,32,.90);border-color:rgba(11,16,32,.9);color:#EEF2FA}
.sl.s-gradiente .bar2{background:#0B1020}
.sl.s-gradiente .btnc{background:#0B1020;color:#EEF2FA}
.sl.s-gradiente .num{-webkit-text-stroke-color:#0B1020}
.sl.s-gradiente .swipe{color:#0B1020;border-color:rgba(11,16,32,.55)}
.sl.s-gradiente .ct{color:#13203B}.sl.s-gradiente .ct b{color:#0B1020}
.sl.s-gradiente .big{color:#FFFFFF}
/* violeta */
.sl.s-violeta .tg{color:#C4B5FD}
.sl.s-violeta .card{background:rgba(30,20,66,.92);border-color:#3B2B78}
.sl.s-violeta .big{color:#22D3EE}
/* alerta */
.sl.s-alerta .tg{color:#FB923C}
.sl.s-alerta h1 em,.sl.s-alerta h2 em{color:#FB923C}
.sl.s-alerta .bar2{background:linear-gradient(90deg,#FB923C,#8B5CF6)}
.sl.s-alerta .num{-webkit-text-stroke-color:#FB923C}
.sl.s-alerta .swipe{border-color:rgba(251,146,60,.6)}
.sl.s-alerta .btnc{background:linear-gradient(90deg,#FB923C,#F472B6)}
.sl.s-alerta .big{color:#FB923C}
/* número gigante */
.sl .big{font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:330px;line-height:.86;letter-spacing:-14px;color:#22D3EE;margin:0 0 26px -10px}
.sl .big small{font-size:96px;letter-spacing:-2px;margin-left:18px}
/* com ilustração */
.sl.hi .ill{right:70px;top:170px;width:400px;height:400px}
.sl.hi .bd{top:560px;justify-content:flex-start}
.sl.hi h1{font-size:88px}
.sl.hi .sb{font-size:36px;margin-top:28px}
.sl.hi .bar2{margin-bottom:34px}
.sl.hi .card{margin-top:30px;font-size:31px;padding:28px 34px}
.sl.hi .btnc{margin-top:34px;font-size:36px;padding:24px 44px}
.sl.hi .swipe{margin-top:40px}
.sl.hi.u h1{font-size:80px}
.sl.hi .bd>.bar2:first-child{margin-bottom:30px}
.sl.hi.t-item .ill{top:200px;width:300px;height:300px}
.sl.hi.t-item .bd{top:230px;justify-content:center}
.sl.hi.t-item h2{font-size:84px}
.sl.hi.t-item .sb{font-size:42px;margin-top:44px}
.sl.hi.t-cta .bd{top:540px}
.sl.gb .bd{top:190px;bottom:170px}
.sl.gb .big{font-size:240px;letter-spacing:-10px}
.sl.gb.u h1{font-size:80px}
.sl.gb.u .sb{margin-top:26px}
.sl.gb.u .card{margin-top:30px}
.sl.gb.u .btnc{margin-top:34px}
</style></head><body><div id="host" style="position:relative;width:1080px;height:1350px;overflow:hidden"></div>
<script>
const LOGO="data:image/png;base64,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";
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const hl=s=>esc(s).replace(/\*([^*]+)\*/g,"<em>$1</em>");
/* estilos v2: "estilo" (escuro|claro|gradiente|violeta|alerta), "ilustracao" por lâmina, "grande" (número gigante) e "panoramico" (carrossel com fundo contínuo) */
const ESTILOS=["escuro","claro","gradiente","violeta","alerta"];
const PAL={
  escuro:{a:"#22D3EE",b:"#8B5CF6",o:"#FB923C",c:"#121A2E",s:"#2B3A60",l:"#EEF2FA",d:"#0B1020"},
  violeta:{a:"#22D3EE",b:"#A78BFA",o:"#FB923C",c:"#1E1442",s:"#3B2B78",l:"#EEF2FA",d:"#0B1020"},
  alerta:{a:"#FB923C",b:"#8B5CF6",o:"#FB923C",c:"#121A2E",s:"#3A2F3F",l:"#EEF2FA",d:"#0B1020"},
  claro:{a:"#06B6D4",b:"#8B5CF6",o:"#FB923C",c:"#FFFFFF",s:"#C9D5EA",l:"#0B1020",d:"#0B1020"},
  gradiente:{a:"#FFFFFF",b:"#0B1020",o:"#FB923C",c:"#0B1020",s:"#0B1020",l:"#EEF2FA",d:"#0B1020"}
};
let ILL_N=0;
function illSVG(name,P){
  const k="g"+(++ILL_N);
  const G=`<defs><linearGradient id="${k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${P.a}"/><stop offset="1" stop-color="${P.b}"/></linearGradient></defs>`;
  const F=`url(#${k})`;
  const ring=`<circle cx="200" cy="200" r="186" fill="none" stroke="${P.a}" stroke-opacity=".25" stroke-width="3" stroke-dasharray="4 14"/><circle cx="200" cy="200" r="150" fill="${P.c}" fill-opacity=".55" stroke="${P.s}" stroke-width="3"/>`;
  const D={
    escudo:`${ring}<path d="M200 82 L292 116 V196 C292 256 252 296 200 318 C148 296 108 256 108 196 V116 Z" fill="${F}"/><path d="M200 104 L272 131 V196 C272 243 241 275 200 294 Z" fill="#FFFFFF" fill-opacity=".14"/><path d="M158 202 L189 233 L246 172" fill="none" stroke="${P.d}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round"/>`,
    cadeado:`${ring}<path d="M150 176 V142 C150 112 172 92 200 92 C228 92 250 112 250 142 V176" fill="none" stroke="${P.l}" stroke-width="22" stroke-linecap="round"/><rect x="122" y="170" width="156" height="132" rx="26" fill="${F}"/><circle cx="200" cy="224" r="18" fill="${P.d}"/><rect x="192" y="232" width="16" height="38" rx="8" fill="${P.d}"/>`,
    nuvem:`${ring}<path d="M128 236 C100 236 86 214 90 194 C94 172 114 160 134 164 C140 128 170 110 200 112 C236 114 258 140 262 168 C292 166 312 188 310 212 C308 228 296 236 280 236 Z" fill="${P.c}" stroke="${F}" stroke-width="10" stroke-linejoin="round"/><path d="M200 300 V176 M170 206 L200 176 L230 206" fill="none" stroke="${F}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><rect x="152" y="292" width="96" height="22" rx="11" fill="${F}"/>`,
    notebook:`${ring}<rect x="102" y="116" width="196" height="132" rx="14" fill="${P.c}" stroke="${P.l}" stroke-opacity=".5" stroke-width="6"/><rect x="116" y="130" width="168" height="104" rx="6" fill="${F}"/><rect x="132" y="148" width="70" height="10" rx="5" fill="${P.d}" fill-opacity=".55"/><rect x="132" y="168" width="110" height="10" rx="5" fill="${P.d}" fill-opacity=".35"/><rect x="132" y="188" width="88" height="10" rx="5" fill="${P.d}" fill-opacity=".35"/><path d="M80 262 H320 L304 286 H96 Z" fill="${P.l}" fill-opacity=".85"/>`,
    celular:`${ring}<rect x="138" y="70" width="124" height="246" rx="26" fill="${P.d}" stroke="${P.l}" stroke-opacity=".6" stroke-width="6"/><rect x="150" y="96" width="100" height="196" rx="10" fill="${P.c}"/><rect x="158" y="112" width="70" height="30" rx="12" fill="${F}"/><rect x="172" y="152" width="70" height="30" rx="12" fill="${P.s}"/><rect x="158" y="192" width="80" height="36" rx="12" fill="${P.o}"/><text x="198" y="218" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="24" fill="${P.d}">!</text><rect x="182" y="78" width="36" height="8" rx="4" fill="${P.s}"/>`,
    impressora:`${ring}<rect x="140" y="92" width="120" height="70" rx="6" fill="${P.l}" fill-opacity=".9"/><rect x="96" y="150" width="208" height="104" rx="22" fill="${F}"/><rect x="130" y="226" width="140" height="68" rx="6" fill="${P.l}"/><rect x="146" y="244" width="80" height="8" rx="4" fill="${P.s}"/><rect x="146" y="262" width="104" height="8" rx="4" fill="${P.s}"/><circle cx="276" cy="176" r="8" fill="${P.d}"/><circle cx="292" cy="112" r="34" fill="${P.o}"/><path d="M278 98 L306 126 M306 98 L278 126" stroke="${P.d}" stroke-width="9" stroke-linecap="round"/>`,
    calendario:`${ring}<rect x="104" y="106" width="192" height="190" rx="22" fill="${P.c}" stroke="${P.s}" stroke-width="5"/><path d="M104 128 C104 116 114 106 126 106 H274 C286 106 296 116 296 128 V156 H104 Z" fill="${F}"/><rect x="142" y="88" width="14" height="40" rx="7" fill="${P.l}"/><rect x="244" y="88" width="14" height="40" rx="7" fill="${P.l}"/>${[0,1,2,3].map(r=>[0,1,2,3].map(c=>`<rect x="${124+c*40}" y="${172+r*28}" width="30" height="18" rx="5" fill="${r===2&&c===2?P.o:P.s}" fill-opacity="${r===2&&c===2?1:.7}"/>`).join("")).join("")}`,
    grafico:`${ring}<rect x="108" y="226" width="40" height="70" rx="8" fill="${P.s}"/><rect x="164" y="190" width="40" height="106" rx="8" fill="${P.s}"/><rect x="220" y="150" width="40" height="146" rx="8" fill="${F}"/><rect x="276" y="112" width="40" height="184" rx="8" fill="${F}"/><path d="M96 214 L170 166 L226 180 L310 92" fill="none" stroke="${P.l}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/><circle cx="310" cy="92" r="14" fill="${P.o}"/>`,
    presente:`${ring}<rect x="112" y="170" width="176" height="132" rx="14" fill="${F}"/><rect x="100" y="136" width="200" height="46" rx="12" fill="${P.l}" fill-opacity=".92"/><rect x="186" y="136" width="28" height="166" fill="${P.o}"/><path d="M200 136 C176 96 132 104 146 128 C152 138 176 138 200 136 C224 138 248 138 254 128 C268 104 224 96 200 136 Z" fill="none" stroke="${P.o}" stroke-width="12" stroke-linejoin="round"/><path d="M300 84 l6 16 16 6 -16 6 -6 16 -6 -16 -16 -6 16 -6z M96 96 l4 10 10 4 -10 4 -4 10 -4 -10 -10 -4 10 -4z" fill="${P.a}"/>`,
    ia:`${ring}<rect x="128" y="128" width="144" height="144" rx="26" fill="${P.c}" stroke="${F}" stroke-width="10"/>${[0,1,2].map(i=>`<rect x="${158+i*34}" y="96" width="14" height="30" rx="7" fill="${P.s}"/><rect x="${158+i*34}" y="274" width="14" height="30" rx="7" fill="${P.s}"/><rect x="96" y="${158+i*34}" width="30" height="14" rx="7" fill="${P.s}"/><rect x="274" y="${158+i*34}" width="30" height="14" rx="7" fill="${P.s}"/>`).join("")}<path d="M200 150 C206 184 216 194 250 200 C216 206 206 216 200 250 C194 216 184 206 150 200 C184 194 194 184 200 150 Z" fill="${F}"/><path d="M252 132 l4 11 11 4 -11 4 -4 11 -4 -11 -11 -4 11 -4z" fill="${P.o}"/>`,
    predio:`${ring}<rect x="126" y="112" width="104" height="192" rx="10" fill="${F}"/><rect x="230" y="176" width="64" height="128" rx="8" fill="${P.c}" stroke="${P.s}" stroke-width="5"/>${[0,1,2,3,4].map(r=>[0,1,2].map(c=>`<rect x="${140+c*28}" y="${128+r*32}" width="18" height="18" rx="4" fill="${P.d}" fill-opacity="${(r+c)%3===0?.25:.6}"/>`).join("")).join("")}${[0,1,2].map(r=>`<rect x="246" y="${194+r*32}" width="32" height="16" rx="4" fill="${P.a}" fill-opacity=".6"/>`).join("")}<path d="M300 68 C282 68 270 82 270 98 C270 120 300 146 300 146 C300 146 330 120 330 98 C330 82 318 68 300 68 Z" fill="${P.o}"/><circle cx="300" cy="98" r="10" fill="${P.d}"/>`,
    servidor:`${ring}${[0,1,2].map(i=>`<rect x="114" y="${104+i*66}" width="172" height="54" rx="12" fill="${i===0?F:P.c}" stroke="${P.s}" stroke-width="5"/><circle cx="142" cy="${131+i*66}" r="8" fill="${i===2?P.o:P.a}"/><rect x="164" y="${125+i*66}" width="96" height="10" rx="5" fill="${i===0?P.d:P.s}" fill-opacity=".7"/>`).join("")}`,
    email:`${ring}<rect x="96" y="128" width="208" height="148" rx="18" fill="${P.c}" stroke="${F}" stroke-width="10"/><path d="M104 140 L200 214 L296 140" fill="none" stroke="${F}" stroke-width="10" stroke-linejoin="round"/><circle cx="292" cy="128" r="36" fill="${P.o}"/><text x="292" y="143" text-anchor="middle" font-family="Inter,sans-serif" font-weight="800" font-size="44" fill="${P.d}">!</text>`
  };
  return `<svg viewBox="0 0 400 400" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">${G}${D[name]||D.escudo}</svg>`;
}
function panoSVG(n,P,estilo){
  const W=n*1080,H=1350,y0=1205;
  let d=`M0 ${y0}`;for(let i=0;i<n;i++){const x=i*1080;d+=` C${x+300} ${y0-70} ${x+780} ${y0+70} ${x+1080} ${y0}`}
  const st=estilo==="gradiente"?"#0B1020":P.a,st2=estilo==="gradiente"?"#FFFFFF":P.b;
  let s=`<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="pg${++ILL_N}" x1="0" x2="1"><stop offset="0" stop-color="${st}"/><stop offset="1" stop-color="${st2}"/></linearGradient></defs>`;
  for(let i=1;i<n;i++){const x=i*1080;s+=`<circle cx="${x}" cy="${i%2?560:820}" r="${i%2?300:230}" fill="none" stroke="${st}" stroke-opacity=".16" stroke-width="4"/><circle cx="${x}" cy="${i%2?560:820}" r="${i%2?190:140}" fill="none" stroke="${st2}" stroke-opacity=".14" stroke-width="3" stroke-dasharray="6 16"/>`}
  s+=`<path d="${d}" fill="none" stroke="url(#pg${ILL_N})" stroke-width="8" stroke-linecap="round" opacity=".85"/>`;
  for(let i=0;i<n;i++){const x=i*1080+540;s+=`<circle cx="${x}" cy="${y0}" r="16" fill="${estilo==="claro"?"#FFFFFF":"#0B1020"}" stroke="${st}" stroke-width="6"/>`}
  return s+"</svg>";
}
function slideHTML(s,i,n,post){
  post=post||{};
  const est=ESTILOS.includes(s.estilo)?s.estilo:ESTILOS.includes(post.estilo)?post.estilo:"escuro";
  const P=PAL[est];const pano=!!post.panoramico&&n>1;
  const tag=s.tag||("// "+(post.pilar||"iTease"));
  const pg=n>1?`<span class="pg">${String(i+1).padStart(2,"0")} / ${String(n).padStart(2,"0")}</span>`:`<span class="pg">@iteasesolucoes</span>`;
  let bd="";
  const t=s.tipo||"capa";
  const gm=s.grande?String(s.grande).match(/^(\S+)\s*(.*)$/):null;
  const big=gm?`<div class="big">${esc(gm[1])}${gm[2]?`<small>${esc(gm[2])}</small>`:""}</div>`:"";
  if(t==="capa"||t==="unica"){
    bd=(big||`<div class="bar2"></div>`)+`<h1>${hl(s.titulo)}</h1>${s.subtitulo?`<div class="sb">${hl(s.subtitulo)}</div>`:""}`+
      (s.destaque?`<div class="card ok"><div class="ic">✓</div><div>${hl(s.destaque)}</div></div>`:"")+
      (t==="capa"&&n>1?`<div class="swipe">Deslize para o lado  →</div>`:"")+
      (t==="unica"&&s.cta?`<div class="btnc">${esc(s.cta)}</div>`:"");
  }else if(t==="item"){
    bd=`<div class="num">${esc(s.numero||String(i).padStart(2,"0"))}</div><h2>${hl(s.titulo)}</h2>${s.texto?`<div class="sb">${hl(s.texto)}</div>`:""}`+
      (s.destaque?`<div class="card"><div class="ic">!</div><div>${hl(s.destaque)}</div></div>`:"");
  }else{ // cta
    bd=`<div class="bar2"></div><h2>${hl(s.titulo)}</h2>${s.texto?`<div class="sb">${hl(s.texto)}</div>`:""}<div class="btnc">${esc(s.cta||"Agende um diagnóstico gratuito")}</div>
      <div class="ct"><b>(19) 3935-6234</b><br>www.itease.com.br · @iteasesolucoes</div>`;
  }
  const ill=s.ilustracao?`<div class="ill">${illSVG(s.ilustracao,P)}</div>`:"";
  const light=est==="claro"||est==="gradiente";
  const logo=light?`<span class="lgp"><img class="lg" src="${LOGO}" alt="iTease"></span>`:`<img class="lg" src="${LOGO}" alt="iTease">`;
  const bg=pano?`<div class="pnl b-${est}" style="width:${n*1080}px;left:${-i*1080}px">${panoSVG(n,P,est)}</div>`:`<div class="bgl b-${est}"></div>`;
  const cls=`sl s-${est} t-${t}${t==="unica"?" u":""}${ill?" hi":""}${big?" gb":""}`;
  return `<div class="${cls}">${bg}${ill}<div class="bar"><span class="tg">${esc(tag)}</span>${logo}</div><div class="bd">${bd}</div><div class="ft"><span>www.itease.com.br</span>${pg}</div></div>`;
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
