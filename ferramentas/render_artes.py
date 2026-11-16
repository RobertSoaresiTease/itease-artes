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
</style></head><body><div id="host" style="position:relative;width:1080px;height:1350px;overflow:hidden"></div>
<script>
const LOGO="data:image/png;base64,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";
const esc=s=>String(s==null?"":s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const hl=s=>esc(s).replace(/\*([^*]+)\*/g,"<em>$1</em>");
function slideHTML(s,i,n,post){
  const tag=s.tag||("// "+(post.pilar||"iTease"));
  const pg=n>1?`<span class="pg">${String(i+1).padStart(2,"0")} / ${String(n).padStart(2,"0")}</span>`:`<span class="pg">@iteasesolucoes</span>`;
  let bd="";
  const t=s.tipo||"capa";
  if(t==="capa"||t==="unica"){
    bd=`<div class="bar2"></div><h1>${hl(s.titulo)}</h1>${s.subtitulo?`<div class="sb">${hl(s.subtitulo)}</div>`:""}`+
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
  return `<div class="sl${t==="unica"?" u":""}"><div class="bar"><span class="tg">${esc(tag)}</span><img class="lg" src="${LOGO}" alt="iTease"></div><div class="bd">${bd}</div><div class="ft"><span>www.itease.com.br</span>${pg}</div></div>`;
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
