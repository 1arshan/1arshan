#!/usr/bin/env python3
"""Generate the profile README graphics. Run: python3 assets/build.py

Each graphic is written twice (-dark, -light) from one definition. Motion is
CSS only: GitHub strips scripts, and CSS can honour prefers-reduced-motion.
Keyframes use relative transforms so a frozen graphic still looks right.
"""
from pathlib import Path

OUT = Path(__file__).parent
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "dark": dict(panel="#161b22", line="#30363d", text="#e6edf3", dim="#8b949e",
                 green="#3fb950", blue="#58a6ff", red="#f85149", amber="#d29922"),
    "light": dict(panel="#f6f8fa", line="#d0d7de", text="#1f2328", dim="#656d76",
                  green="#1a7f37", blue="#0969da", red="#cf222e", amber="#9a6700"),
}

BASE_CSS = f"""
text{{font-family:{FONT};fill:var(--text)}}
.dim{{fill:var(--dim)}}
.link{{stroke:var(--line);stroke-width:2;fill:none}}
.pill{{fill:var(--panel);stroke:var(--line);stroke-width:2}}
.mid{{text-anchor:middle;dominant-baseline:central}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def anim(selector, name, secs=10, delay=0):
    return (f"{selector}{{animation:{name} {secs}s linear {delay}s infinite}}\n")


def keyframes(name, stops):
    """stops: {percent(s) as text: css declarations}."""
    body = "".join(f"{pct}{{{css}}}" for pct, css in stops.items())
    return f"@keyframes {name}{{{body}}}\n"


def packet(name, dx, dy, color):
    """A dot that travels (dx, dy) from its drawn position, then vanishes."""
    return keyframes(name, {
        "0%": "transform:translate(0,0);opacity:0",
        "6%": "opacity:1",
        "48%": "opacity:1",
        "55%": f"transform:translate({dx}px,{dy}px);opacity:0",
        "100%": f"transform:translate({dx}px,{dy}px);opacity:0",
    }) + f".{name}{{fill:var(--{color})}}\n"


def svg(title, width, height, css, body):
    def render(theme):
        tokens = ";".join(f"--{k}:{v}" for k, v in THEMES[theme].items())
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" role="img">'
            f"<title>{title}</title>"
            f"<style>svg{{{tokens}}}{BASE_CSS}{css}</style>"
            f'<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="14" '
            f'fill="var(--panel)" stroke="var(--line)" stroke-width="2"/>'
            f"{body}</svg>\n"
        )
    return render


def tile(title, name, sub, css, body):
    """A 440x260 card: animation above, name and one line below."""
    caption = (
        f'<text x="26" y="206" font-size="30" font-weight="700">{name}</text>'
        f'<text x="26" y="238" font-size="20" class="dim">{sub}</text>'
        f'<text x="414" y="206" font-size="22" class="dim" text-anchor="end">↗</text>'
    )
    return svg(title, 440, 260, css, body + caption)


def hero():
    css = (
        keyframes("blink", {"0%,49%": "opacity:1", "50%,100%": "opacity:0"})
        + ".cursor{fill:var(--green);animation:blink 1.2s steps(1) infinite}\n"
        + packet("p-ai", -106, -78, "blue") + anim(".p-ai", "p-ai", 9)
        + packet("p-sec", 118, -68, "green") + anim(".p-sec", "p-sec", 9, -6)
        + packet("p-bot", 44, 92, "amber") + anim(".p-bot", "p-bot", 9, -3)
        + keyframes("p-bad", {
            "0%": "transform:translate(0,0);opacity:0",
            "8%": "opacity:1",
            "30%": "transform:translate(-40px,-62px);opacity:1",
            "36%,100%": "transform:translate(-40px,-62px);opacity:0",
        })
        + ".p-bad{fill:var(--red)}\n" + anim(".p-bad", "p-bad", 9, -8)
        + keyframes("shield", {
            "0%,28%": "opacity:0", "32%": "opacity:1",
            "46%": "opacity:0", "100%": "opacity:0",
        })
        + ".shield{fill:none;stroke:var(--red);stroke-width:2.5}\n"
        + anim(".shield", "shield", 9, -8)
    )
    body = """
<text x="36" y="72" font-size="18" class="dim">$ whoami</text>
<text x="36" y="124" font-size="42" font-weight="700">arshan ahmad</text>
<text x="36" y="170" font-size="23">i build ai systems</text>
<text x="36" y="204" font-size="23">and break insecure ones</text>
<rect class="cursor" x="360" y="186" width="13" height="22"/>
<line class="link" x1="590" y1="150" x2="470" y2="62"/>
<line class="link" x1="590" y1="150" x2="725" y2="72"/>
<line class="link" x1="590" y1="150" x2="640" y2="256"/>
<line class="link" x1="772" y1="172" x2="732" y2="110" stroke-dasharray="4 6"/>
<circle class="p-ai" cx="590" cy="150" r="6"/>
<circle class="p-sec" cx="590" cy="150" r="6"/>
<circle class="p-bot" cx="590" cy="150" r="6"/>
<circle class="p-bad" cx="772" cy="172" r="6"/>
<rect class="pill" x="412" y="42" width="116" height="40" rx="20"/>
<text class="mid" x="470" y="62" font-size="16">ai agents</text>
<rect class="pill" x="667" y="52" width="116" height="40" rx="20"/>
<text class="mid" x="725" y="72" font-size="16">security</text>
<rect class="shield" x="659" y="44" width="132" height="56" rx="28"/>
<rect class="pill" x="582" y="236" width="116" height="40" rx="20"/>
<text class="mid" x="640" y="256" font-size="16">robotics</text>
<circle class="pill" cx="590" cy="150" r="42"/>
<text class="mid" x="590" y="150" font-size="16" font-weight="700">arshan</text>
"""
    return svg("Arshan Ahmad: I build AI systems and break insecure ones", 800, 300, css, body)


def reliefnet():
    def chip(cls, y, label):
        return (
            f'<g class="{cls}"><rect class="pill" x="24" y="{y}" width="150" height="36" rx="8"/>'
            f'<text class="mid" x="99" y="{y + 18}" font-size="15">{label}</text></g>'
        )

    def slide(name, dy):
        return keyframes(name, {
            "0%,12%": "transform:translate(0,0);opacity:1",
            "38%": f"transform:translate(120px,{dy}px);opacity:0",
            "88%": f"transform:translate(120px,{dy}px);opacity:0",
            "96%,100%": "transform:translate(0,0);opacity:1",
        })

    css = (
        slide("c1", 50) + slide("c2", 0) + slide("c3", -50)
        + anim(".c1", "c1") + anim(".c2", "c2") + anim(".c3", "c3")
        + keyframes("node", {
            "0%,30%": "opacity:.25", "40%,88%": "opacity:1", "96%,100%": "opacity:.25",
        })
        + anim(".node", "node")
        + keyframes("claim", {
            "0%,50%": "stroke-dashoffset:96", "64%,88%": "stroke-dashoffset:0",
            "96%,100%": "stroke-dashoffset:96",
        })
        + ".claim{stroke:var(--green);stroke-width:3;stroke-dasharray:96;fill:none}\n"
        + anim(".claim", "claim")
    )
    body = (
        chip("c1", 22, "need food") + chip("c2", 72, "help, ward 12") + chip("c3", 122, "family of 5")
        + '<g class="node"><circle class="pill" cx="262" cy="90" r="38" style="stroke:var(--blue)"/>'
        + '<text class="mid" x="262" y="90" font-size="15">family</text></g>'
        + '<line class="claim" x1="300" y1="90" x2="396" y2="90"/>'
        + '<circle class="pill" cx="384" cy="90" r="30" style="stroke:var(--green)"/>'
        + '<text class="mid" x="384" y="90" font-size="14">agent</text>'
    )
    return tile("ReliefNet: AI agents sharing one FalkorDB memory graph", "ReliefNet",
                "agents on one falkordb graph", css, body)


def pentest():
    ports = ["22", "80", "443", "3000", "8080", "3306"]
    hits = {"8080": "red", "3000": "amber"}
    cells, css = "", ""
    for i, port in enumerate(ports):
        x = 30 + (i % 3) * 130
        y = 26 + (i // 3) * 74
        lit = hits.get(port, "green")
        cells += (
            f'<rect class="pill cell{i}" x="{x}" y="{y}" width="118" height="58" rx="8"/>'
            f'<text class="mid" x="{x + 59}" y="{y + 29}" font-size="18">{port}</text>'
        )
        start = 8 + (i % 3) * 18
        css += keyframes(f"cell{i}", {
            f"0%,{start}%": "stroke:var(--line)",
            f"{start + 4}%,85%": f"stroke:var(--{lit})",
            "92%,100%": "stroke:var(--line)",
        }) + anim(f".cell{i}", f"cell{i}")
    css += (
        keyframes("scan", {
            "0%,4%": "transform:translateX(0);opacity:0", "8%": "opacity:1",
            "66%": "transform:translateX(380px);opacity:1",
            "70%,100%": "transform:translateX(380px);opacity:0",
        })
        + ".scan{stroke:var(--green);stroke-width:3}\n" + anim(".scan", "scan")
    )
    body = cells + '<line class="scan" x1="30" y1="16" x2="30" y2="168"/>'
    return tile("AI-driven penetration testing framework", "AI pentest agents",
                "llm recon + vuln discovery", css, body)


def fast_flux():
    ips = ["203.0.113.7", "198.51.100.42", "192.0.2.19"]
    texts, css = "", ""
    for i, ip in enumerate(ips):
        texts += f'<text class="ip ip{i} mid" x="312" y="70" font-size="18">{ip}</text>'
        css += anim(f".ip{i}", "ip", 9, [0, -6, -3][i])
    css += (
        keyframes("ip", {
            "0%": "opacity:0", "4%,28%": "opacity:1", "33%,100%": "opacity:0",
        })
        + keyframes("ttl", {
            "0%": "transform:scaleX(1)", "33.3%": "transform:scaleX(0)",
            "33.4%": "transform:scaleX(1)", "66.6%": "transform:scaleX(0)",
            "66.7%": "transform:scaleX(1)", "100%": "transform:scaleX(0)",
        })
        + ".ttl{fill:var(--amber);transform-origin:212px 120px}\n" + anim(".ttl", "ttl", 9)
        + keyframes("flag", {"0%,60%": "opacity:0", "66%,94%": "opacity:1", "100%": "opacity:0"})
        + ".ip1,.ip2{opacity:0}\n"
        + ".flag{stroke:var(--red)}\n.flagt{fill:var(--red)}\n"
        + anim(".flagg", "flag", 9)
    )
    body = (
        '<rect class="pill" x="24" y="46" width="146" height="48" rx="8"/>'
        '<text class="mid" x="97" y="70" font-size="16">evil.test</text>'
        '<line class="link" x1="170" y1="70" x2="212" y2="70"/>'
        '<rect class="pill" x="212" y="46" width="200" height="48" rx="8"/>'
        + texts +
        '<rect class="link" x="212" y="114" width="200" height="12" rx="6"/>'
        '<rect class="ttl" x="212" y="114" width="200" height="12" rx="6"/>'
        '<text x="24" y="125" font-size="15" class="dim">ttl 5s</text>'
        '<g class="flagg"><rect class="pill flag" x="212" y="140" width="200" height="34" rx="8"/>'
        '<text class="mid flagt" x="312" y="157" font-size="15">ml: fast flux</text></g>'
    )
    return tile("Fast Flux networks: emulation and ML detection", "Fast Flux",
                "emulation + ml detection", css, body)


def virgi_bot():
    css = (
        keyframes("bot", {
            "0%,6%": "transform:translateX(0)", "46%,54%": "transform:translateX(240px)",
            "94%,100%": "transform:translateX(0)",
        })
        + anim(".bot", "bot")
        + keyframes("box", {
            "0%,6%": "transform:translate(0,0);opacity:1",
            "46%": "transform:translate(240px,0);opacity:1",
            "52%": "transform:translate(292px,34px);opacity:1",
            "88%": "transform:translate(292px,34px);opacity:1",
            "92%": "transform:translate(292px,34px);opacity:0",
            "93%": "transform:translate(0,0);opacity:0",
            "100%": "transform:translate(0,0);opacity:1",
        })
        + anim(".box", "box")
        + ".crate{fill:var(--amber)}\n.body{fill:var(--blue)}\n.wheel{fill:var(--text)}\n"
    )
    body = (
        '<line class="link" x1="24" y1="166" x2="416" y2="166"/>'
        '<rect class="pill" x="344" y="112" width="70" height="54" rx="4"/>'
        '<text class="mid dim" x="379" y="96" font-size="14">orders</text>'
        '<g class="bot"><rect class="body" x="44" y="112" width="74" height="36" rx="6"/>'
        '<circle class="wheel" cx="62" cy="156" r="10"/><circle class="wheel" cx="100" cy="156" r="10"/>'
        '<circle cx="66" cy="130" r="4" fill="var(--panel)"/><circle cx="96" cy="130" r="4" fill="var(--panel)"/></g>'
        '<rect class="crate box" x="62" y="80" width="38" height="32" rx="3"/>'
    )
    return tile("Virgi-bot: warehouse robot, e-Yantra 2nd place", "Virgi-bot",
                "e-yantra 2nd place robot", css, body)


GRAPHICS = {
    "hero": hero(),
    "reliefnet": reliefnet(),
    "pentest": pentest(),
    "fast-flux": fast_flux(),
    "virgi-bot": virgi_bot(),
}

if __name__ == "__main__":
    for name, render in GRAPHICS.items():
        for theme in THEMES:
            (OUT / f"{name}-{theme}.svg").write_text(render(theme), encoding="utf-8")
