"""ui.py - Omnix TRACE dark dashboard theme: CSS, HTML building blocks and SVG recolouring for previews.

All functions return HTML strings (rendered with st.markdown(..., unsafe_allow_html=True)); nothing here does
computation. Publication exports are unaffected: they keep their white, journal-ready styling.
"""
from __future__ import annotations

import base64
import html
import os

# ------------------------------------------------------------------------------------------------ palette
BG = "#0A0E1A"          # page
PANEL = "#0F1424"       # sidebar
CARD = "#111729"        # cards
CARD_2 = "#151C33"      # raised / inputs
BORDER = "#1F2942"
INK = "#E2E8F0"
MUTED = "#94A3B8"
FAINT = "#64748B"
INDIGO = "#6366F1"
INDIGO_L = "#A5B4FC"
GREEN = "#34D399"
AMBER = "#F59E0B"
PURPLE = "#A78BFA"
SKY = "#38BDF8"
ROSE = "#F43F5E"
TEAL = "#2DD4BF"

LAYER_COLORS = {"mRNA": "#6366F1", "protein": "#34D399", "metabolite": "#F59E0B"}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');
html, body, [class*="css"], .stMarkdown, .stText, button, input, select, textarea {{
  font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}}
.stApp {{ background: {BG}; }}
.block-container {{ padding-top: 1.2rem; padding-bottom: 3rem; max-width: 1480px; }}
header[data-testid="stHeader"] {{ background: transparent; }}
h1, h2, h3, h4, h5 {{ color: {INK} !important; font-weight: 650; letter-spacing: -0.01em; }}
h3 {{ font-size: 1.12rem !important; }}
h4 {{ font-size: 1.0rem !important; }}
p, li, label, .stMarkdown {{ color: {INK}; }}
[data-testid="stCaptionContainer"], .stCaption {{ color: {MUTED} !important; }}
a {{ color: {INDIGO_L} !important; }}
code {{ color: {INDIGO_L}; background: {CARD_2}; }}

/* ---------- sidebar */
section[data-testid="stSidebar"] {{ background: {PANEL}; border-right: 1px solid {BORDER}; }}
section[data-testid="stSidebar"] .block-container {{ padding-top: 1rem; }}
section[data-testid="stSidebar"] [role="radiogroup"] {{ gap: 8px; }}
section[data-testid="stSidebar"] [role="radiogroup"] > label {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 10px; padding: 10px 12px; margin: 0;
  width: 100%; transition: border-color .15s, background .15s;
}}
section[data-testid="stSidebar"] [role="radiogroup"] > label:hover {{ border-color: #33407a; }}
section[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {{
  border-color: {INDIGO}; background: rgba(99,102,241,0.10); box-shadow: 0 0 0 1px rgba(99,102,241,.35) inset;
}}
section[data-testid="stSidebar"] [data-testid="stExpander"] details {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 10px;
}}
section[data-testid="stSidebar"] [data-testid="stExpander"] summary p {{ font-weight: 550; }}
section[data-testid="stSidebar"] hr {{ border-color: {BORDER}; margin: 1.1rem 0 0.6rem 0; }}

/* ---------- inputs */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, .stTextInput input, .stNumberInput input {{
  background: {CARD_2} !important; border-color: {BORDER} !important; border-radius: 8px !important;
}}
.stSlider [data-baseweb="slider"] div[role="slider"] {{ background: {INDIGO}; border-color: {INDIGO}; }}

/* ---------- buttons */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
  border-radius: 9px; border: 1px solid {BORDER}; background: {CARD_2}; color: {INK}; font-weight: 550;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{ border-color: {INDIGO}; color: #fff; }}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"],
.stDownloadButton > button[kind="primary"] {{
  background: linear-gradient(90deg, #E11D48 0%, #9333EA 60%, {INDIGO} 100%); border: 0; color: #fff;
  font-weight: 650; box-shadow: 0 6px 20px rgba(147,51,234,.25);
}}
.stButton > button[kind="primary"]:hover {{ filter: brightness(1.08); }}

/* ---------- tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 1px solid {BORDER}; flex-wrap: wrap; }}
.stTabs [data-baseweb="tab"] {{
  height: 44px; padding: 0 12px; color: {MUTED}; background: transparent; border-radius: 8px 8px 0 0;
}}
.stTabs [data-baseweb="tab"] p {{ font-size: 0.93rem; font-weight: 550; }}
.stTabs [data-baseweb="tab"]:hover {{ color: {INK}; background: rgba(99,102,241,0.06); }}
.stTabs [aria-selected="true"] {{ color: {INDIGO_L} !important; background: rgba(99,102,241,0.10) !important; }}
.stTabs [data-baseweb="tab-highlight"] {{ background: {INDIGO}; height: 2px; }}
.stTabs [data-baseweb="tab-border"] {{ display: none; }}

/* ---------- cards (bordered containers) and expanders */
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"]) {{
  background: {CARD}; border: 1px solid {BORDER} !important; border-radius: 14px;
}}
[data-testid="stExpander"] details {{ background: {CARD}; border: 1px solid {BORDER}; border-radius: 10px; }}
/* side-by-side cards wrap onto separate rows when the main area is narrow (half-screen windows) */
div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"] > div > div[data-testid="stLayoutWrapper"]) {{
  flex-wrap: wrap; row-gap: 1rem; }}
div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"] > div > div[data-testid="stLayoutWrapper"]) > div[data-testid="stColumn"] {{
  flex: 1 1 400px !important; min-width: min(400px, 100%); }}
[data-testid="stDataFrame"] {{ border: 1px solid {BORDER}; border-radius: 10px; overflow: hidden; }}
[data-testid="stMetricValue"] {{ color: {INK}; font-family: 'JetBrains Mono', monospace; }}

/* ---------- custom blocks */
.tr-head {{ display:flex; align-items:center; gap:16px; flex-wrap:wrap; padding: 4px 0 14px 0;
  border-bottom: 1px solid {BORDER}; margin-bottom: 16px; }}
.tr-logo {{ width:46px; height:46px; border-radius:12px; display:flex; align-items:center; justify-content:center;
  background: linear-gradient(135deg, #7C3AED, #DB2777); box-shadow: 0 6px 18px rgba(124,58,237,.35); overflow:hidden; }}
.tr-logo img {{ width: 34px; height: 34px; object-fit: contain; }}
.tr-title {{ display:flex; flex-direction:column; line-height:1.2; }}
.tr-title b {{ font-size: 1.45rem; color:{INK}; font-weight:700; letter-spacing:-.01em; }}
.tr-title span {{ color:{MUTED}; font-size: .92rem; }}
.tr-ver {{ font-family:'JetBrains Mono',monospace; font-size:.78rem; color:{INDIGO_L}; border:1px solid #33407a;
  background: rgba(99,102,241,.12); padding: 2px 9px; border-radius: 999px; margin-left: 8px; vertical-align: middle; }}
.tr-pill {{ display:inline-flex; align-items:center; gap:8px; padding: 6px 14px; border-radius:999px;
  font-size:.86rem; font-weight:550; border:1px solid; white-space:nowrap; }}
.tr-pill .dot {{ width:9px; height:9px; border-radius:50%; }}
.tr-pill.ok {{ color:{GREEN}; border-color: rgba(52,211,153,.45); background: rgba(52,211,153,.08); }}
.tr-pill.ok .dot {{ background:{GREEN}; box-shadow: 0 0 8px {GREEN}; }}
.tr-pill.idle {{ color:{MUTED}; border-color:{BORDER}; background:{CARD}; }}
.tr-pill.idle .dot {{ background:{FAINT}; }}
.tr-pill.info {{ color:{INDIGO_L}; border-color:#33407a; background: rgba(99,102,241,.08); }}
.tr-pill .mono {{ font-family:'JetBrains Mono',monospace; }}
.tr-spacer {{ flex:1; }}

.tr-banner {{ display:flex; gap:16px; align-items:flex-start; padding:16px 18px; border-radius:14px;
  border:1px solid #2a3470; background: linear-gradient(90deg, rgba(99,102,241,.10), rgba(17,23,41,.6));
  margin: 2px 0 14px 0; flex-wrap: wrap; }}
.tr-banner .ic {{ width:42px; height:42px; border-radius:10px; background: rgba(99,102,241,.18);
  display:flex; align-items:center; justify-content:center; color:{INDIGO_L}; font-size:1.3rem; flex: none; }}
.tr-banner .body {{ flex: 1 1 360px; min-width: 260px; }}
.tr-tag {{ display:inline-block; padding:3px 10px; border-radius:7px; background: rgba(99,102,241,.18);
  color:{INDIGO_L}; font-weight:600; font-size:.88rem; border:1px solid #33407a; margin-right:10px; }}
.tr-contrast {{ font-family:'JetBrains Mono',monospace; font-size:.86rem; color:{MUTED}; }}
.tr-contrast .case {{ color:#FB7185; }} .tr-contrast .ref {{ color:{GREEN}; }}
.tr-banner p {{ margin: 8px 0 0 0; color:#CBD5E1; font-size:.92rem; }}

.tr-sec {{ display:flex; align-items:center; gap:9px; color:{INK}; font-weight:650; letter-spacing:.06em;
  text-transform:uppercase; font-size:.84rem; margin: 14px 0 10px 0; }}
.tr-sec .ic {{ color:{INDIGO_L}; font-size: 1rem; }}
.tr-sec .badge {{ margin-left:auto; text-transform:none; letter-spacing:0; font-family:'JetBrains Mono',monospace;
  font-size:.74rem; color:{INDIGO_L}; border:1px solid #33407a; background:rgba(99,102,241,.1); padding:1px 8px;
  border-radius:6px; font-weight:500; }}

.tr-cardhead {{ margin: 2px 0 6px 0; }}
.tr-cardhead b {{ color:{INK}; font-size:1.06rem; font-weight:650; display:flex; align-items:center; gap:9px; }}
.tr-cardhead b .ic {{ color:{INDIGO_L}; }}
.tr-cardhead span {{ color:{MUTED}; font-size:.88rem; }}

.tr-metrics {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(165px, 1fr)); gap: 14px; margin-bottom: 8px; }}
.tr-metric {{ background:{CARD}; border:1px solid {BORDER}; border-radius:14px; padding: 16px 18px 14px 18px;
  border-bottom: 3px solid var(--accent); position:relative; min-height: 132px; }}
.tr-metric.hl {{ background: linear-gradient(180deg, color-mix(in srgb, var(--accent) 9%, {CARD}), {CARD}); }}
.tr-metric .lab {{ color: var(--labc, {MUTED}); font-size:.9rem; font-weight:550; display:flex; justify-content:space-between; gap: 8px; }}
.tr-metric .lab .ic {{ color: var(--accent); font-size: 1.05rem; }}
.tr-metric .val {{ font-family:'JetBrains Mono',monospace; font-size: 2.15rem; font-weight:700; color: var(--valc, {INK});
  margin: 8px 0 6px 0; line-height:1.1; }}
.tr-metric .sub {{ color:{MUTED}; font-size:.8rem; }}
.tr-metric .sub b {{ color: var(--accent); font-weight:600; }}

.tr-find {{ display:flex; gap:12px; align-items:flex-start; padding: 11px 4px; border-bottom:1px solid {BORDER}; }}
.tr-find:last-child {{ border-bottom: 0; }}
.tr-find .kind {{ flex:none; font-size:.72rem; font-weight:650; letter-spacing:.04em; text-transform:uppercase;
  padding: 3px 8px; border-radius:6px; border:1px solid; min-width: 92px; text-align:center; margin-top: 2px; }}
.tr-find .txt {{ color:#CBD5E1; font-size:.92rem; line-height:1.45; }}
.tr-find .txt b {{ color:{INK}; }}
.tr-find .txt .stat {{ font-family:'JetBrains Mono',monospace; font-size:.8rem; color:{MUTED}; }}

.trace-note {{ background: rgba(99,102,241,.08); border:1px solid #2a3470; border-left: 4px solid {INDIGO};
  padding: 10px 14px; border-radius: 10px; margin: 6px 0 12px 0; color:#CBD5E1; }}
.trace-warn {{ background: rgba(245,158,11,.08); border:1px solid #5b4314; border-left: 4px solid {AMBER};
  padding: 10px 14px; border-radius: 10px; margin: 6px 0 12px 0; color:#FCD34D; }}
.tr-figpaper {{ background:#FFFFFF; border-radius: 10px; padding: 10px; }}
</style>
"""

ICONS = {"layers": "&#9776;", "chart": "&#9638;", "check": "&#10003;", "flask": "&#9879;", "branch": "&#10023;",
         "stack": "&#9781;", "trend": "&#8599;", "bolt": "&#9889;", "db": "&#9707;", "spark": "&#10022;",
         "search": "&#9906;", "grid": "&#9638;", "target": "&#9678;", "flow": "&#8644;"}


def _esc(x) -> str:
    return html.escape(str(x))


def logo_data_uri(path: str) -> str | None:
    if path and os.path.exists(path):
        return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()
    return None


def header(version: str, logo_path: str | None, status: str, kb_text: str) -> str:
    uri = logo_data_uri(logo_path)
    logo = f'<img src="{uri}"/>' if uri else '<span style="color:#fff;font-size:1.4rem">&#10022;</span>'
    return (f'<div class="tr-head"><div class="tr-logo">{logo}</div>'
            f'<div class="tr-title"><b>Omnix TRACE <span class="tr-ver">v{_esc(version)}</span></b>'
            f'<span>Directional Tri-Omics Integration Pipeline</span></div>{status}'
            f'<div class="tr-spacer"></div><span class="tr-pill info">{_esc(kb_text)}</span></div>')


def status_pill(done: bool, seconds: float | None = None) -> str:
    if done:
        t = f' <span class="mono">&middot; {seconds:.1f}s</span>' if seconds is not None else ""
        return f'<span class="tr-pill ok"><span class="dot"></span>Execution completed{t}</span>'
    return '<span class="tr-pill idle"><span class="dot"></span>Awaiting run</span>'


def banner(tier_text: str, case: str, ref: str, alpha: float) -> str:
    tier, _, desc = tier_text.partition(":")
    return (f'<div class="tr-banner"><div class="ic">{ICONS["stack"]}</div><div class="body">'
            f'<span class="tr-tag">{_esc(tier.strip())}</span>'
            f'<span class="tr-contrast">Contrast: <span class="case">{_esc(case)}</span> vs '
            f'<span class="ref">{_esc(ref)}</span></span>'
            f'<p>Directional integration of <b>transcriptomics &rarr; proteomics &rarr; enzyme function &rarr; '
            f'metabolomics</b>. {_esc(desc.strip()).capitalize()}. Every reaction is scored for directional '
            f'concordance, calibrated by label and network-topology permutations.</p></div>'
            f'<span class="tr-pill ok" style="align-self:center">&#10003; FDR calibrated (q &lt; {alpha:g})</span></div>')


def section(title: str, icon: str = "chart", badge: str | None = None) -> str:
    b = f'<span class="badge">{_esc(badge)}</span>' if badge else ""
    return f'<div class="tr-sec"><span class="ic">{ICONS.get(icon, icon)}</span>{_esc(title)}{b}</div>'


def card_head(title: str, subtitle: str = "", icon: str = "chart") -> str:
    sub = f"<span>{subtitle}</span>" if subtitle else ""
    return f'<div class="tr-cardhead"><b><span class="ic">{ICONS.get(icon, icon)}</span>{_esc(title)}</b>{sub}</div>'


def metric_cards(items: list[dict]) -> str:
    """items: dict(label, value, sub, accent, icon, highlight=False)."""
    out = []
    for it in items:
        hl = it.get("highlight", False)
        style = f'--accent:{it["accent"]};' + (f'--labc:{it["accent"]};--valc:{it["accent"]};' if hl else "")
        out.append(f'<div class="tr-metric{" hl" if hl else ""}" style="{style}">'
                   f'<div class="lab"><span>{_esc(it["label"])}</span><span class="ic">{ICONS.get(it.get("icon", "chart"), "")}</span></div>'
                   f'<div class="val">{_esc(it["value"])}</div><div class="sub">{it.get("sub", "")}</div></div>')
    return '<div class="tr-metrics">' + "".join(out) + "</div>"


KIND_STYLE = {"Bottleneck": ("#FB923C", "rgba(251,146,60,.4)"), "Throughput": (GREEN, "rgba(52,211,153,.4)"),
              "Reaction": (INDIGO_L, "#33407a"), "Metabolite-driven": (AMBER, "rgba(245,158,11,.4)"),
              "Pathway": (PURPLE, "rgba(167,139,250,.4)"), "Canonical": (SKY, "rgba(56,189,248,.4)"),
              "Target": (ROSE, "rgba(244,63,94,.4)"), "Concordance": (TEAL, "rgba(45,212,191,.4)")}


def findings(rows: list[tuple[str, str]]) -> str:
    """rows: (kind, html text)."""
    if not rows:
        return f'<div class="tr-find"><div class="txt" style="color:{MUTED}">No findings match this filter.</div></div>'
    out = []
    for kind, txt in rows:
        c, b = KIND_STYLE.get(kind, (MUTED, BORDER))
        out.append(f'<div class="tr-find"><span class="kind" style="color:{c};border-color:{b}">{_esc(kind)}</span>'
                   f'<div class="txt">{txt}</div></div>')
    return "".join(out)


# --------------------------------------------------------------------------- dark previews of static figures
# Publication figures are drawn white; for on-screen preview in the dark dashboard their colours are mapped
# to the dashboard palette (exports keep the original white styling).
SVG_DARK_MAP = {
    "#ffffff": CARD, "#1f2a28": INK, "#5d6d6a": MUTED, "#4a5754": MUTED, "#000000": "#CBD5E1",
    "#e3f2ef": "#11302C", "#00695c": "#14B8A6", "#00574d": "#5EEAD4", "#e4e9e8": "#1E293B", "#eceeef": "#1E293B",
    "#eceff0": "#1E293B", "#eeeeee": "#1E293B", "#f4f8fb": "#0E1528", "#c9d3d1": "#334155", "#333333": "#94A3B8",
    "#444444": "#94A3B8", "#555555": "#94A3B8", "#8a9593": "#64748B", "#b9c4c2": "#475569", "#9aa5a2": "#7C8BA1",
    "#262626": "#CBD5E1", "#f2f4f3": INK,
}


def darken_svg(svg: bytes) -> bytes:
    s = svg.decode("utf-8")
    for a, b in SVG_DARK_MAP.items():
        s = s.replace(a, b.lower()).replace(a.upper(), b.lower())
    # text drawn in matplotlib's default colour carries no fill attribute (renders black): give text groups
    # a light default; groups with an explicit colour keep it
    i = s.find(">", s.find("<svg")) + 1
    s = s[:i] + '<style>g[id^="text_"]{fill:#CBD5E1}</style>' + s[i:]
    return s.encode("utf-8")


# --------------------------------------------------------------------------- dark Plotly figures
_PLOTLY_MAP = {
    '"#1F2A28"': f'"{INK}"', '"rgba(255,255,255,0.8)"': '"rgba(17,23,41,0.88)"', '"white"': f'"{CARD}"',
    '"#555"': '"#94A3B8"', '"#666"': '"#94A3B8"', '"#888"': '"#94A3B8"', '"#333"': '"#94A3B8"',
    '"#999"': '"#5B6B85"', '"#BBB"': '"#475569"', '"#BBBBBB"': '"#64748B"', '"#CCC"': '"#475569"',
    '"#6B7775"': f'"{MUTED}"', '"#7F8C8D"': '"#64748B"', '"#F0F2F2"': '"#1E293B"', '"#C9D3D1"': '"#334155"',
    '"#D5DBDB"': '"#334155"', '"#D0D5D4"': '"#3B4660"', '"#E3F2EF"': '"#11302C"', '"#00695C"': '"#14B8A6"',
    '"#F4F6F6"': '"#1E293B"', '"#E65100"': '"#FB923C"',
}


def dark_template():
    import plotly.graph_objects as go
    import plotly.io as pio
    t = go.layout.Template(pio.templates["plotly_dark"])
    ax = dict(gridcolor="#1E293B", linecolor="#334155", zerolinecolor="#334155", tickcolor="#334155",
              title_font=dict(color=MUTED), tickfont=dict(color=MUTED))
    t.layout.update(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, Segoe UI, sans-serif", color=INK, size=13),
                    xaxis=ax, yaxis=ax, legend=dict(font=dict(color="#CBD5E1"), bgcolor="rgba(0,0,0,0)"),
                    hoverlabel=dict(bgcolor=CARD_2, bordercolor=BORDER, font=dict(color=INK)),
                    colorway=[INDIGO, GREEN, AMBER, PURPLE, SKY, ROSE, TEAL])
    return t


def dark_figure(fig):
    """Recolour a TRACE Plotly figure for the dark dashboard (screen only; downloads of the publication
    renderer keep the white journal style)."""
    import plotly.graph_objects as go
    js = fig.to_json()
    for a, b in _PLOTLY_MAP.items():
        js = js.replace(a, b)
    out = go.Figure(go.Figure(**__import__("json").loads(js)))
    out.update_layout(template=dark_template(), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    out.update_layout(font=dict(color=INK))
    out.update_xaxes(gridcolor="#1E293B", linecolor="#334155", zerolinecolor="#334155")
    out.update_yaxes(gridcolor="#1E293B", linecolor="#334155", zerolinecolor="#334155")
    if out.layout.title and out.layout.title.text:
        out.layout.title.font.color = INK
    return out
