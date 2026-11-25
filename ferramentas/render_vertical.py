#!/usr/bin/env python3
"""Gera Stories (JPEG 1080x1920) e Reels (MP4 1080x1920, H.264) do Marketing IA da iTease.

Uso: python3 render_vertical.py <arquivo.json> <pasta_saida>

JSON:
{
  "stories": [ {"data":"2026-11-26","horario":"09:00","tag":"Black Friday","titulo":"Amanhã é *Black Friday*",
                "texto":"Frase de apoio curta.","rodape":"itease.com.br"} ],
  "reels":   [ {"data":"2026-11-26","horario":"12:00","tag":"Golpes","legenda":"...","hashtags":["#a"],
                "cenas":[ {"titulo":"...","texto":"...","destaque":"texto mono opcional"} ] } ]
}
*texto entre asteriscos* fica em ciano. Saídas:
  <saida>/stories/<data>-<HHMM>.jpg
  <saida>/reels/<data>-reel.mp4  (+ <data>-reel-capa.jpg)
Requer: playwright (chromium), ffmpeg.
"""
import base64, html, json, os, re, subprocess, sys, tempfile
from playwright.sync_api import sync_playwright

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(AQUI, "..", "marca", "logo-branco.png")
LOGO_B64 = base64.b64encode(open(LOGO, "rb").read()).decode()

CSS = """
*{box-sizing:border-box}body{margin:0}
.v{width:1080px;height:1920px;position:relative;overflow:hidden;font-family:Inter,sans-serif;color:#EEF2FA;
 background:radial-gradient(900px 800px at 0% 0%,rgba(34,211,238,.28),transparent 62%),
 radial-gradient(1000px 900px at 100% 100%,rgba(139,92,246,.32),transparent 62%),
 repeating-linear-gradient(90deg,rgba(148,163,184,.07) 0 2px,transparent 2px 108px),
 repeating-linear-gradient(0deg,rgba(148,163,184,.05) 0 2px,transparent 2px 108px),#0B1020}
.top{position:absolute;left:90px;right:90px;top:200px;display:flex;justify-content:space-between;align-items:center}
.tg{font-family:"DejaVu Sans Mono",monospace;font-size:34px;letter-spacing:6px;color:#22D3EE;text-transform:uppercase}
.top img{height:54px}
.bd{position:absolute;left:90px;right:90px;top:420px;bottom:420px;display:flex;flex-direction:column;justify-content:center}
.bar{width:170px;height:12px;border-radius:6px;background:linear-gradient(90deg,#22D3EE,#8B5CF6);margin-bottom:64px}
h1{font-family:"Inter Display",Inter,sans-serif;font-weight:800;font-size:120px;line-height:1.02;letter-spacing:-3px;margin:0}
h1 em{font-style:normal;color:#22D3EE}
.tx{font-size:52px;line-height:1.35;color:#B8C3DA;margin-top:56px}
.tx em{font-style:normal;color:#EEF2FA;font-weight:700}
.dq{margin-top:64px;font-family:"DejaVu Sans Mono",monospace;font-size:46px;color:#EEF2FA;background:rgba(18,26,46,.92);
 border:3px solid #243150;border-radius:30px;padding:36px 44px;word-break:break-all}
.dq em{font-style:normal;color:#FB923C}
.ft{position:absolute;left:90px;right:90px;bottom:300px;font-family:"DejaVu Sans Mono",monospace;font-size:34px;color:#9AA6C1;display:flex;justify-content:space-between}
.ft b{color:#EEF2FA;font-weight:400}
.pg{position:absolute;left:90px;right:90px;bottom:240px;height:8px;border-radius:4px;background:rgba(148,163,184,.18)}
.pg i{display:block;height:8px;border-radius:4px;background:linear-gradient(90deg,#22D3EE,#8B5CF6)}
"""

def fmt(s):
    s = html.escape(s or "")
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s).replace("\n", "<br>")

def page(tag, titulo, texto, destaque=None, rodape="@iteasesolucoes", progresso=None):
    pg = f'<div class="pg"><i style="width:{progresso*100:.1f}%"></i></div>' if progresso is not None else ""
    dq = f'<div class="dq">{fmt(destaque)}</div>' if destaque else ""
    tx = f'<div class="tx">{fmt(texto)}</div>' if texto else ""
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="v"><div class="top"><span class="tg">// {html.escape(tag or 'iTease')}</span>
<img src="data:image/png;base64,{LOGO_B64}"></div>
<div class="bd"><div class="bar"></div><h1>{fmt(titulo)}</h1>{tx}{dq}</div>
<div class="ft"><span>{html.escape(rodape)}</span><b>iTease · TI para empresas</b></div>{pg}</div></body></html>"""

def shot(pw_page, doc, out, fmt_="jpeg"):
    pw_page.set_content(doc, wait_until="load")
    pw_page.screenshot(path=out, type=fmt_, quality=92 if fmt_ == "jpeg" else None, clip={"x":0,"y":0,"width":1080,"height":1920})

def main():
    src, out = sys.argv[1], sys.argv[2]
    d = json.load(open(src))
    os.makedirs(os.path.join(out, "stories"), exist_ok=True)
    os.makedirs(os.path.join(out, "reels"), exist_ok=True)
    feitos = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width":1080,"height":1920})
        for s in d.get("stories", []):
            f = os.path.join(out, "stories", f"{s['data']}-{s['horario'].replace(':','')}.jpg")
            shot(pg, page(s.get("tag"), s["titulo"], s.get("texto"), s.get("destaque"), s.get("rodape","@iteasesolucoes")), f)
            feitos.append(f)
        for r in d.get("reels", []):
            tmp = tempfile.mkdtemp()
            cenas = r["cenas"]; n = len(cenas); pngs = []
            for i, c in enumerate(cenas):
                f = os.path.join(tmp, f"c{i:02d}.png")
                shot(pg, page(r.get("tag"), c["titulo"], c.get("texto"), c.get("destaque"), progresso=(i+1)/n), f, "png")
                pngs.append(f)
            capa = os.path.join(out, "reels", f"{r['data']}-reel-capa.jpg")
            shot(pg, page(r.get("tag"), cenas[0]["titulo"], cenas[0].get("texto"), cenas[0].get("destaque")), capa)
            dur, fade, fps = float(r.get("segundos_por_cena", 3.2)), 0.4, 30
            ins, filt = [], []
            for i, f in enumerate(pngs):
                ins += ["-loop", "1", "-t", f"{dur}", "-i", f]
                frames = int(dur*fps)
                filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0009,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={fps},setsar=1,format=yuv420p[v{i}]")
            last = "v0"; off = dur - fade
            for i in range(1, n):
                filt.append(f"[{last}][v{i}]xfade=transition=fade:duration={fade}:offset={off:.2f}[x{i}]")
                last = f"x{i}"; off += dur - fade
            total = dur*n - fade*(n-1)
            mp4 = os.path.join(out, "reels", f"{r['data']}-reel.mp4")
            cmd = ["ffmpeg","-y","-loglevel","error"] + ins + ["-f","lavfi","-t",f"{total:.2f}","-i","anullsrc=r=44100:cl=stereo",
                   "-filter_complex",";".join(filt),"-map",f"[{last}]","-map",f"{n}:a","-c:v","libx264","-preset","veryfast","-crf","21",
                   "-pix_fmt","yuv420p","-c:a","aac","-b:a","96k","-shortest","-movflags","+faststart",mp4]
            subprocess.run(cmd, check=True)
            feitos += [mp4, capa]
        b.close()
    print("\n".join(feitos))

if __name__ == "__main__":
    main()
