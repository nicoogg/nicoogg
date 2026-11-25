"""Animated SVGs for the nicoogg profile README.

    python3 scripts/build.py            # everything
    python3 scripts/build.py activity   # only the live activity card (run by .github/workflows/activity.yml)

Each SVG is self-contained (fonts and avatar embedded) and animated with SMIL + CSS only:
GitHub shows README images as <img>, where scripts never run."""
import base64, sys, os, json, urllib.request, datetime

S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(S)
OUT = os.path.join(ROOT, "assets")
FONTS = os.path.join(ROOT, "assets", "fonts")
ONLY = sys.argv[1] if len(sys.argv) > 1 else "all"
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
REG, MED = b64(f"{FONTS}/GeistMono-Regular.woff2"), b64(f"{FONTS}/GeistMono-Medium.woff2")
AV = b64(f"{S}/avatar.png")
FONT_CSS = f"""@font-face{{font-family:G;src:url(data:font/woff2;base64,{REG}) format('woff2');font-weight:400}}
@font-face{{font-family:G;src:url(data:font/woff2;base64,{MED}) format('woff2');font-weight:500}}
text{{font-family:G,ui-monospace,Menlo,monospace}}"""
ESC = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def typed(id_, x, y, w_char, text, begin, per=0.055):
    """clip rect that grows one character at a time; returns (clipPath, end_time)"""
    n = len(text)
    vals = ";".join(f"{i * w_char:.1f}" for i in range(n + 1))
    times = ";".join(f"{i / n:.4f}" for i in range(n + 1))
    dur = n * per
    clip = (f'<clipPath id="{id_}"><rect x="{x}" y="{y}" height="80" width="0">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{times}" calcMode="discrete" begin="{begin}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
    return clip, begin + dur


# ───────────────────────── banner ─────────────────────────
def banner():
    W, H = 1280, 400
    cw = 54 * 0.6  # Geist Mono advance at 54px
    l1, l2 = "/* I build tools", "that actually ship */"
    c1, e1 = typed("t1", 96, 128, cw, l1, 0.4)
    c2, e2 = typed("t2", 96, 186, cw, l2, e1 + 0.15)
    # caret: follows line 1, then line 2, then blinks
    xs1 = ";".join(f"{96 + i * cw + 4:.1f}" for i in range(len(l1) + 1))
    xs2 = ";".join(f"{96 + i * cw + 4:.1f}" for i in range(len(l2) + 1))
    k1 = ";".join(f"{i / len(l1):.4f}" for i in range(len(l1) + 1))
    k2 = ";".join(f"{i / len(l2):.4f}" for i in range(len(l2) + 1))
    chips_t = e2 + 0.2
    chips = [("GS Loft", " developer", None), ("corvex", " in dev", "#3ddc84"), ("corvexai", " 4B · local AI", "#3ddc84"), ("wantdownload", " live", "#2f6bff")]
    chip_svg, cx = [], 96
    for i, (b, rest, dot) in enumerate(chips):
        w = (len(b) + len(rest)) * 7.2 + 20 + (14 if dot else 0)
        tx = cx + 10 + (14 if dot else 0)
        d = (f'<circle cx="{cx + 14}" cy="279" r="3" fill="{dot}"><animate attributeName="r" values="3;5;3" dur="1.6s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;.4;1" dur="1.6s" repeatCount="indefinite"/></circle>') if dot else ""
        chip_svg.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{chips_t + i * .18:.2f}s" dur=".4s" fill="freeze"/>
  <animateTransform attributeName="transform" type="translate" from="0 8" to="0 0" begin="{chips_t + i * .18:.2f}s" dur=".4s" fill="freeze"/>
  <rect x="{cx}" y="266" width="{w:.0f}" height="26" rx="4" fill="#111" stroke="#2A2A2A"/>{d}
  <text x="{tx}" y="283.5" font-size="12" fill="#8A8A8A"><tspan fill="#fff" font-weight="500">{b}</tspan>{rest}</text></g>''')
        cx += w + 10

    # right side: avatar block + project nodes with wires and packets
    ax, ay, asz = 985, 76, 232
    acx, acy = ax + asz / 2, ay + asz / 2
    nodes = [(900, 84, "№01 corvex"), (880, 318, "№02 wantdownload"), (690, 318, "№03 GS Loft"), (700, 84, "№04 corvexai")]
    wires, pk, labs = [], [], []
    for i, (nx, ny, lab) in enumerate(nodes):
        path = f"M{acx},{acy} L{nx},{ny}"
        wires.append(f'<path d="{path}" stroke="#fff" stroke-opacity=".35" stroke-dasharray="3 5" fill="none"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1.2s" repeatCount="indefinite"/></path>')
        pk.append(f'<rect x="-2.5" y="-2.5" width="5" height="5" fill="#fff"><animateMotion path="{path}" dur="{2.2 + i * .5:.1f}s" begin="{i * .6:.1f}s" repeatCount="indefinite"/></rect>')
        pk.append(f'<rect x="-2" y="-2" width="4" height="4" fill="#fff" opacity=".5"><animateMotion path="{path}" dur="{2.6 + i * .4:.1f}s" begin="{.9 + i * .3:.1f}s" repeatCount="indefinite" keyPoints="1;0" keyTimes="0;1" calcMode="linear"/></rect>')
        tw = len(lab) * 6.6 + 16
        lx = min(nx - tw / 2, W - 60 - tw)
        labs.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{1 + i * .25:.2f}s" dur=".5s" fill="freeze"/>
  <rect x="{lx:.0f}" y="{ny - 11}" width="{tw:.0f}" height="22" fill="#000" stroke="#fff" stroke-opacity=".8"/>
  <text x="{lx + 8:.0f}" y="{ny + 4}" font-size="11" fill="#fff">{ESC(lab)}</text></g>''')

    statuses = ["shipping corvex · security agents + corvexai", "corvexai · our own 4B security model · runs on 127.0.0.1", "live: wantdownload.vercel.app", "working @ GS Loft · verona", "portfolio → nicoogg.github.io"]
    n = len(statuses)
    foot = []
    for i, st in enumerate(statuses):
        # visible for its slice of the loop
        a, b = i / n, (i + 1) / n
        kt = f"0;{max(a, 0.0001):.4f};{min(a + .02, b):.4f};{b - .02:.4f};{b:.4f};1" if i else f"0;0.02;{b - .02:.4f};{b:.4f};1"
        vals = "0;0;1;1;0;0" if i else "0;1;1;0;0"
        foot.append(f'<text x="72" y="379" font-size="12" fill="#777" letter-spacing=".7" opacity="0">&gt; {ESC(st)}<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{n * 3}s" repeatCount="indefinite"/></text>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="nicoogg · I build tools that actually ship">
<title>nicoogg · I build tools that actually ship</title>
<style>{FONT_CSS}
.grid{{animation:pan 20s linear infinite}} @keyframes pan{{to{{transform:translate(40px,40px)}}}}
.mark{{transform-origin:84px 24px;animation:spin 18s linear infinite}} @keyframes spin{{to{{transform:rotate(360deg)}}}}
.scan{{animation:scan 3s cubic-bezier(.4,0,.6,1) infinite}} @keyframes scan{{0%{{transform:translateY(0);opacity:0}}10%{{opacity:1}}75%{{transform:translateY({asz}px);opacity:1}}76%,100%{{opacity:0}}}}
.cur{{animation:blink 1.05s steps(1) {e2:.2f}s infinite}} @keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
</style>
<defs>
  <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#141414"/></pattern>
  <linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="#0A0A0A"/><stop offset=".35" stop-color="#0A0A0A" stop-opacity="0"/></linearGradient>
  <linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".22"/></linearGradient>
  <clipPath id="col"><rect x="48" y="0" width="{W - 96}" height="{H}"/></clipPath>
  <clipPath id="avc"><rect x="{ax}" y="{ay}" width="{asz}" height="{asz}"/></clipPath>
  {c1}{c2}
</defs>
<rect width="{W}" height="{H}" fill="#000"/>
<g clip-path="url(#col)"><rect x="48" width="{W - 96}" height="{H}" fill="#0A0A0A"/><g class="grid"><rect x="8" y="-40" width="{W}" height="{H + 80}" fill="url(#g)"/></g></g>
<path d="M48.5 0V{H}M{W - 48.5} 0V{H}" stroke="#1C1C1C"/>
<path d="M48 48.5H{W - 48}M48 {H - 55.5}H{W - 48}" stroke="#1C1C1C"/>
<g font-size="13" fill="#454545"><text x="44" y="53">+</text><text x="{W - 52}" y="53">+</text><text x="44" y="{H - 51}">+</text><text x="{W - 52}" y="{H - 51}">+</text></g>

<g class="mark" stroke="#C8C8C8" stroke-width="2" stroke-linecap="square"><path d="M84 16v16M77 20l14 8M77 28l14-8"/></g>
<text x="100" y="29" font-size="12" font-weight="500" fill="#C8C8C8" letter-spacing=".7">nicoogg</text>
<text x="{W - 72}" y="29" font-size="12" fill="#555" text-anchor="end" letter-spacing=".7">// developer · verona, italy</text>

<!-- radar rings from the avatar -->
<g fill="none" stroke="#fff" stroke-dasharray="1 5">
  <circle cx="{acx}" cy="{acy}" r="130" opacity="0"><animate attributeName="r" values="130;330" dur="4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".55;0" dur="4s" repeatCount="indefinite"/></circle>
  <circle cx="{acx}" cy="{acy}" r="130" opacity="0"><animate attributeName="r" values="130;330" dur="4s" begin="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".55;0" dur="4s" begin="2s" repeatCount="indefinite"/></circle>
</g>
<g clip-path="url(#col)">{"".join(wires)}{"".join(pk)}</g>

<!-- avatar with scan line -->
<rect x="{ax - 1}" y="{ay - 1}" width="{asz + 2}" height="{asz + 2}" fill="#000" stroke="#fff" stroke-opacity=".85"/>
<image href="data:image/png;base64,{AV}" x="{ax}" y="{ay}" width="{asz}" height="{asz}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin=".2s" dur="1s" fill="freeze"/></image>
<g clip-path="url(#avc)"><g class="scan"><rect x="{ax}" y="{ay - 40}" width="{asz}" height="40" fill="url(#scanG)"/><rect x="{ax}" y="{ay}" width="{asz}" height="1.2" fill="#fff"/></g></g>
{"".join(labs)}

<!-- title, typed -->
<g transform="translate(96 82)"><rect width="196" height="24" rx="4" fill="#161616" stroke="#2A2A2A"/><rect x="4" y="3" width="18" height="18" rx="3" fill="#282828"/>
  <text x="13" y="16.5" font-size="12" fill="#fff" text-anchor="middle">+</text><text x="30" y="16.5" font-size="12" font-weight="500" fill="#C8C8C8" letter-spacing=".6">OPERATOR_ONLINE</text>
  <circle cx="186" cy="12" r="3" fill="#3ddc84"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle></g>
<text x="96" y="170" font-size="54" letter-spacing="0" clip-path="url(#t1)"><tspan fill="#4A4A4A">/*</tspan><tspan fill="#8A8A8A"> I build tools</tspan></text>
<text x="96" y="228" font-size="54" clip-path="url(#t2)"><tspan fill="#fff">that actually ship </tspan><tspan fill="#4A4A4A">*/</tspan></text>
<g class="cur"><rect y="129" width="24" height="46" fill="#fff" x="100">
  <animate attributeName="x" values="{xs1}" keyTimes="{k1}" calcMode="discrete" begin=".4s" dur="{len(l1) * .055:.2f}s" fill="freeze"/>
  <animate attributeName="y" to="187" begin="{e1 + .1:.2f}s" dur=".01s" fill="freeze"/>
  <animate attributeName="x" values="{xs2}" keyTimes="{k2}" calcMode="discrete" begin="{e1 + .15:.2f}s" dur="{len(l2) * .055:.2f}s" fill="freeze"/>
</rect></g>
{"".join(chip_svg)}

<g>{"".join(foot)}</g>
<text x="{W - 72}" y="379" font-size="12" fill="#555" text-anchor="end" letter-spacing=".7">nicoogg.github.io</text>
</svg>'''


# ───────────────────────── terminal ─────────────────────────
def terminal():
    W = 860
    lines = [("$ ", "whoami --verbose", "#fff"),
             ("role .............. ", "developer", None), ("portfolio ......... ", "nicoogg.github.io", None),
             ("work .............. ", "GS Loft · github.com/GS-Loft-Dev", None),
             ("building .......... ", "corvex · security agents + corvexai", "#3ddc84"),
             ("live .............. ", "wantdownload · wantdownload.vercel.app", "#6f9bff"),
             ("based in .......... ", "Verona, Italy", None)]
    cw = 14 * 0.6
    H = 64 + len(lines) * 26 + 34
    out, clips, t = [], [], 0.5
    for i, (a, b, col) in enumerate(lines):
        y = 66 + i * 26
        full = a + b
        if i == 0:
            c, t2 = typed(f"l{i}", 28, y - 20, cw, full, t, .06)
        else:
            # output lines print fast, like a real command
            c, t2 = typed(f"l{i}", 28, y - 20, cw, full, t, .012)
        clips.append(c)
        fill_a = "#3ddc84" if i == 0 else "#666"
        fill_b = col or "#d6d6d6"
        out.append(f'<text x="28" y="{y}" font-size="14" clip-path="url(#l{i})"><tspan fill="{fill_a}">{ESC(a)}</tspan><tspan fill="{fill_b}">{ESC(b)}</tspan></text>')
        t = t2 + (0.45 if i == 0 else 0.12)
    yc = 66 + len(lines) * 26
    out.append(f'<text x="28" y="{yc}" font-size="14" fill="#3ddc84" opacity="0">$ <animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".01s" fill="freeze"/></text>')
    out.append(f'<rect x="{28 + 2 * cw + 2:.1f}" y="{yc - 13}" width="8" height="16" fill="#fff" opacity="0"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="whoami: developer at GS Loft, building corvex, wantdownload live, portfolio nicoogg.github.io">
<style>{FONT_CSS}</style>
<defs>{"".join(clips)}</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="#0A0A0A" stroke="#222"/>
<path d="M0 32.5H{W}" stroke="#1C1C1C"/>
<circle cx="22" cy="16" r="5" fill="#2a2a2a"/><circle cx="40" cy="16" r="5" fill="#2a2a2a"/><circle cx="58" cy="16" r="5" fill="#2a2a2a"/>
<text x="{W / 2}" y="20" font-size="11" fill="#666" text-anchor="middle">nicoogg@dash: ~</text>
<circle cx="{W - 24}" cy="16" r="3.5" fill="#3ddc84"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
{"".join(out)}
</svg>'''


# ───────────────────────── status badges ─────────────────────────
def badge(label, color):
    w = len(label) * 6.6 + 34
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} 22" width="{w:.0f}" height="22" role="img" aria-label="{label}">
<style>@font-face{{font-family:G;src:url(data:font/woff2;base64,{REG}) format('woff2')}} text{{font-family:G,ui-monospace,Menlo,monospace}}</style>
<rect x=".5" y=".5" width="{w - 1:.0f}" height="21" rx="4" fill="#0A0A0A" stroke="#2A2A2A"/>
<circle cx="13" cy="11" r="7" fill="{color}" opacity=".3"><animate attributeName="r" values="3.5;8;3.5" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".5;0;.5" dur="1.8s" repeatCount="indefinite"/></circle>
<circle cx="13" cy="11" r="3.5" fill="{color}"/>
<text x="24" y="15" font-size="11" fill="#e6e6e6" letter-spacing=".5">{label}</text>
</svg>'''



# ───────────────────────── looping shell session ─────────────────────────
class Timeline:
    """Discrete SMIL animations that all share one looping duration, so a whole scripted session repeats in sync."""
    def __init__(self, total): self.T = total
    def disc(self, attr, steps):
        # steps: [(seconds, value), ...] — value holds from its time until the next one
        if steps[0][0] > 0: raise ValueError("first step must be at 0")
        kt = ";".join(f"{min(1, t / self.T):.5f}" for t, _ in steps)
        vals = ";".join(str(v) for _, v in steps)
        return f'<animate attributeName="{attr}" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{self.T:.2f}s" repeatCount="indefinite"/>'


def session():
    W, LH, top = 860, 21, 62
    cw = 13 * 0.6
    PROMPT = "nicoogg@dash:~$ "
    scenes = [
        ("whoami", ["nicoogg — developer @ GS Loft · building corvex · shipping wantdownload"]),
        ("ls projects/", ["<d>corvex.md</d>   <d>corvexai.md</d>   <d>wantdownload.md</d>   <d>gsloft.md</d>"]),
        ("cat projects/corvex.md", ["<b>№01 corvex</b>  <g>[in development]</g>",
                                    "security agents powered by corvexai, our own local AI.",
                                    "they test dashboards, code and computers, find the gaps and fix them."]),
        ("corvexai --specs", ["<b>corvexai</b>  <g>[our own AI model · one job: security]</g>",
                              "size ...... 4B parameters · 2.9 GB · runs on a laptop too",
                              "runs on ... your machine, only on 127.0.0.1 · no question leaves",
                              "bench ..... <g>96%</g> issues found · <g>100%</g> defenses recognised, exact line",
                              "powers .... CORVUS (assistant) + ORACLE (AI code audit)"]),
        ("neofetch", ["<b>      ██      </b>  nicoogg@dash", "<b>  ██  ██  ██  </b>  os ....... nicoogg.os 2.0", "<b>    ██████    </b>  host ..... GS Loft",
                      "<b>  ██  ██  ██  </b>  projects . 5 (1 live, 2 in dev)", "<b>      ██      </b>  ai ....... corvexai 4B · local"]),
        ("open nicoogg.github.io", ["<g>→ every command works for real there. come type something.</g>"]),
    ]
    per, gap, hold = .065, .35, 2.6
    # timing
    t, plan = .6, []
    for c, outs in scenes:
        t0 = t; t_type_end = t0 + len(c) * per; t_out = t_type_end + gap
        line_t = [t_out + i * .09 for i in range(len(outs))]
        t_end = (line_t[-1] if line_t else t_out) + hold
        plan.append((c, outs, t0, t_type_end, line_t, t_end)); t = t_end + .25
    T = t
    tl = Timeline(T)

    def colorize(o):
        o = ESC(o).replace("&lt;b&gt;", '<tspan fill="#fff" font-weight="500">').replace("&lt;/b&gt;", "</tspan>")
        for tag, col in (("g", "#3ddc84"), ("y", "#f5a524"), ("d", "#6f9bff")):
            o = o.replace(f"&lt;{tag}&gt;", f'<tspan fill="{col}">').replace(f"&lt;/{tag}&gt;", "</tspan>")
        return o

    groups = []
    px = 24 + len(PROMPT) * cw
    for i, (c, outs, t0, tte, line_t, t_end) in enumerate(plan):
        vis = tl.disc("visibility", [(0, "hidden"), (t0 - .25 if i else .0001, "visible"), (t_end + .249, "hidden")] if i else [(0, "visible"), (t_end + .249, "hidden")])
        y = top
        widths = [(0, 0)] + [(t0 + k * per, f"{(k + 1) * cw:.1f}") for k in range(len(c))] + [(t_end + .249, 0)]
        widths = [w for j, w in enumerate(widths) if j == 0 or w[0] > widths[j - 1][0]]
        clip = f'<clipPath id="c{i}"><rect x="{px:.1f}" y="{y - 15}" height="22" width="0">{tl.disc("width", widths)}</rect></clipPath>'
        body = [f'<text x="24" y="{y}"><tspan fill="#3ddc84">nicoogg@dash</tspan><tspan fill="#777">:</tspan><tspan fill="#6f9bff">~</tspan><tspan fill="#777">$ </tspan></text>',
                f'<text x="{px:.1f}" y="{y}" fill="#fff" clip-path="url(#c{i})">{ESC(c)}</text>']
        for k, (o, lt) in enumerate(zip(outs, line_t)):
            body.append(f'<text x="24" y="{y + (k + 1) * LH}" fill="#cfcfcf" visibility="hidden">{tl.disc("visibility", [(0, "hidden"), (lt, "visible"), (t_end + .249, "hidden")])}{colorize(o)}</text>')
        # caret: follows the typing, then waits on a fresh prompt under the output
        ny = y + (len(outs) + 1) * LH
        cx = [(0, f"{px:.1f}")] + [(t0 + k * per, f"{px + (k + 1) * cw:.1f}") for k in range(len(c))] + [(line_t[-1] + .05, f"{px:.1f}")]
        cy = [(0, y - 12), (line_t[-1] + .05, ny - 12)]
        body.append(f'<text x="24" y="{ny}" visibility="hidden">{tl.disc("visibility", [(0, "hidden"), (line_t[-1] + .05, "visible"), (t_end + .249, "hidden")])}<tspan fill="#3ddc84">nicoogg@dash</tspan><tspan fill="#777">:</tspan><tspan fill="#6f9bff">~</tspan><tspan fill="#777">$ </tspan></text>')
        body.append(f'<rect class="cur" width="8" height="15" fill="#fff">{tl.disc("x", cx)}{tl.disc("y", cy)}</rect>')
        groups.append((clip, f'<g visibility="{"visible" if i == 0 else "hidden"}">{vis}{"".join(body)}</g>'))

    H = top + 7 * LH + 22
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="A looping shell session: whoami, ls projects, cat corvex, neofetch, scan. Try it live at nicoogg.github.io">
<style>{FONT_CSS} text{{font-size:13px}} .cur{{animation:b 1s steps(1) infinite}} @keyframes b{{50%{{opacity:0}}}}</style>
<defs>{"".join(c for c, _ in groups)}</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="#0A0A0A" stroke="#222"/>
<path d="M0 32.5H{W}" stroke="#1C1C1C"/>
<circle cx="22" cy="16" r="5" fill="#ff5f57" opacity=".8"/><circle cx="40" cy="16" r="5" fill="#febc2e" opacity=".8"/><circle cx="58" cy="16" r="5" fill="#28c840" opacity=".8"/>
<text x="{W / 2}" y="20" font-size="11" fill="#666" text-anchor="middle" style="font-size:11px">nicoogg@dash: ~ — portfolio-sh</text>
<g transform="translate({W - 86} 9)"><rect width="70" height="15" rx="3" fill="#111" stroke="#2a2a2a"/><circle cx="10" cy="7.5" r="3" fill="#3ddc84"><animate attributeName="opacity" values="1;.25;1" dur="1.4s" repeatCount="indefinite"/></circle><text x="18" y="11" fill="#9a9a9a" style="font-size:8.5px">REC · LOOP</text></g>
{"".join(g for _, g in groups)}
<rect x="0" y="{H - 3}" height="2" fill="#3ddc84" opacity=".6" width="0"><animate attributeName="width" values="0;{W}" dur="{T:.2f}s" repeatCount="indefinite"/></rect>
</svg>"""


# ───────────────────────── command buttons ─────────────────────────
def chip(cmd):
    label = f"$ {cmd}"
    w = len(label) * 7.2 + 28
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} 28" width="{w:.0f}" height="28" role="img" aria-label="run {cmd}">
<style>@font-face{{font-family:G;src:url(data:font/woff2;base64,{REG}) format('woff2')}} text{{font-family:G,ui-monospace,Menlo,monospace}}</style>
<defs><linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".18"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="r"><rect x="1" y="1" width="{w - 2:.0f}" height="26" rx="5"/></clipPath></defs>
<rect x=".5" y=".5" width="{w - 1:.0f}" height="27" rx="5" fill="#0A0A0A" stroke="#333"/>
<g clip-path="url(#r)"><rect x="-60" y="0" width="60" height="28" fill="url(#sh)"><animate attributeName="x" values="-60;{w + 60:.0f};{w + 60:.0f}" keyTimes="0;.35;1" dur="4s" begin="{(sum(map(ord, cmd)) % 30) / 10:.1f}s" repeatCount="indefinite"/></rect></g>
<text x="12" y="18" font-size="12" fill="#3ddc84">$</text><text x="26" y="18" font-size="12" fill="#e6e6e6">{ESC(cmd)}</text>
<rect x="{w - 14:.0f}" y="9" width="6" height="11" fill="#e6e6e6"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
</svg>"""


# ───────────────────────── live activity (refreshed by GitHub Actions) ─────────────────────────
def activity():
    req = urllib.request.Request("https://api.github.com/users/nicoogg/events/public?per_page=40", headers={"User-Agent": "nicoogg-readme", "Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"): req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    try: events = json.load(urllib.request.urlopen(req, timeout=20))
    except Exception as e: print("events:", e); events = []
    now = datetime.datetime.now(datetime.timezone.utc)
    def ago(ts):
        m = int((now - datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))).total_seconds() // 60)
        return f"{m}m" if m < 60 else f"{m // 60}h" if m < 1440 else f"{m // 1440}d"
    def desc(e):
        p = e.get("payload") or {}
        t = e["type"]
        if t == "PushEvent":
            c = (p.get("commits") or [{}])[0].get("message", "").split("\n")[0]
            return "push", c or f"commits to {(p.get('ref') or 'main').replace('refs/heads/', '')}"
        return {"CreateEvent": ("create", f"{p.get('ref_type', '')} {p.get('ref') or ''}".strip()), "WatchEvent": ("star", "starred"),
                "ForkEvent": ("fork", "forked"), "PublicEvent": ("open", "made public"), "ReleaseEvent": ("release", (p.get("release") or {}).get("tag_name", "")),
                "PullRequestEvent": ("pr", f"{p.get('action', '')} pull request"), "IssuesEvent": ("issue", f"{p.get('action', '')} issue")}.get(t, (t.replace("Event", "").lower(), ""))
    rows = []
    for e in events:
        k, m = desc(e)
        rows.append((str(e.get("id", ""))[-7:], k, e["repo"]["name"], m, ago(e["created_at"])))
        if len(rows) == 7: break
    if not rows: rows = [("0000000", "idle", "nicoogg", "no public activity in the last days", "—")]
    W, top, LH = 860, 84, 22
    H = top + len(rows) * LH + 44
    cw = 12 * 0.6
    lines = []
    for i, (h, k, repo, m, a) in enumerate(rows):
        y = top + i * LH
        msg = m if len(m) < 52 else m[:49] + "…"
        lines.append(f"""<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{1.1 + i * .22:.2f}s" dur=".3s" fill="freeze"/>
<animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" begin="{1.1 + i * .22:.2f}s" dur=".3s" fill="freeze"/>
<text x="24" y="{y}"><tspan fill="#f5a524">{ESC(h)}</tspan><tspan fill="#3ddc84"> {ESC(k):<7}</tspan><tspan fill="#fff">{ESC(repo)}</tspan><tspan fill="#777"> · </tspan><tspan fill="#cfcfcf">{ESC(msg)}</tspan></text>
<text x="{W - 24}" y="{y}" fill="#666" text-anchor="end">{ESC(a)} ago</text></g>""")
    cmd = "git log --live --author=nicoogg"
    stamp = now.strftime("%Y-%m-%d %H:%M UTC")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Latest public GitHub activity of nicoogg, updated {stamp}">
<style>{FONT_CSS} text{{font-size:12px;white-space:pre}} .cur{{animation:b 1s steps(1) infinite}} @keyframes b{{50%{{opacity:0}}}}</style>
<defs><clipPath id="ty"><rect x="140" y="40" height="20" width="0"><animate attributeName="width" from="0" to="{len(cmd) * cw:.0f}" begin=".3s" dur=".7s" fill="freeze" calcMode="discrete" values="{";".join(f"{i * cw:.1f}" for i in range(len(cmd) + 1))}"/></rect></clipPath></defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="8" fill="#0A0A0A" stroke="#222"/>
<path d="M0 32.5H{W}" stroke="#1C1C1C"/>
<circle cx="22" cy="16" r="5" fill="#2a2a2a"/><circle cx="40" cy="16" r="5" fill="#2a2a2a"/><circle cx="58" cy="16" r="5" fill="#2a2a2a"/>
<text x="{W / 2}" y="20" fill="#666" text-anchor="middle" style="font-size:11px">live activity · refreshed every 6h by GitHub Actions</text>
<g transform="translate({W - 74} 9)"><rect width="58" height="15" rx="3" fill="#111" stroke="#2a2a2a"/><circle cx="10" cy="7.5" r="3" fill="#3ddc84"><animate attributeName="r" values="3;4.5;3" dur="1.4s" repeatCount="indefinite"/></circle><text x="18" y="11" fill="#9a9a9a" style="font-size:8.5px">LIVE</text></g>
<text x="24" y="54"><tspan fill="#3ddc84">nicoogg@dash</tspan><tspan fill="#777">:</tspan><tspan fill="#6f9bff">~</tspan><tspan fill="#777">$</tspan></text>
<text x="140" y="54" fill="#fff" clip-path="url(#ty)">{cmd}</text>
{"".join(lines)}
<text x="24" y="{H - 16}" fill="#555" style="font-size:10px">updated {stamp} · {len(rows)} events</text>
<rect class="cur" x="{W - 32}" y="{H - 27}" width="8" height="14" fill="#fff"/>
</svg>"""


os.makedirs(OUT, exist_ok=True)
def write(name, svg): open(os.path.join(OUT, name), "w").write(svg); print("wrote", name, len(svg) // 1024, "KB")
if ONLY in ("all", "activity"): write("activity.svg", activity())
if ONLY == "all":
    write("banner.svg", banner())
    write("session.svg", session())
    write("status-live.svg", badge("LIVE", "#3ddc84"))
    write("status-dev.svg", badge("IN DEVELOPMENT", "#f5a524"))
    write("status-work.svg", badge("DAY JOB", "#6f9bff"))
    for c in ["help", "neofetch", "projects", "corvexai", "git log", "scan", "matrix", "firewall"]:
        write(f"cmd-{c.replace(' ', '-')}.svg", chip(c))
