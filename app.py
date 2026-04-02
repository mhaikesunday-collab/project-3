"""
BLAST DESIGN & COST ESTIMATION TOOL
Open-Pit Mining | Streamlit App
Author: mhaike
"""

import math
import streamlit as st
from datetime import datetime

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG  – must be first Streamlit call
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Blast Design Tool",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS  – full dark theme + blue/green accents
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

:root {
    --bg-deep:      #04101C;
    --bg-panel:     #071A2B;
    --bg-card:      #0A2236;
    --border:       #0D3D5C;
    --accent-blue:  #12A3D8;
    --accent-green: #0FBF6A;
    --mid-blue:     #0A7FAD;
    --mid-green:    #0C9A56;
    --text-main:    #D6EEF8;
    --text-muted:   #4D7A99;
    --text-label:   #88BDD6;
    --mono:         'Share Tech Mono', monospace;
    --body:         'Exo 2', sans-serif;
}

/* App background */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-deep) !important;
    color: var(--text-main) !important;
    font-family: var(--body);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--bg-panel) !important;
    border-right: 1px solid var(--border);
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Headers */
h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--accent-blue) !important;
    font-family: var(--mono) !important;
    letter-spacing: 1px;
}

/* Subheader specifically */
.stSubheader {
    color: var(--accent-green) !important;
    font-family: var(--mono) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 6px;
    margin-top: 20px;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

[data-testid="stMetricLabel"] {
    color: var(--text-label) !important;
    font-family: var(--body);
    font-size: 13px;
    font-weight: 400;
}

[data-testid="stMetricValue"] {
    color: var(--accent-green) !important;
    font-family: var(--mono);
    font-size: 28px !important;
    font-weight: 600;
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 20px 0;
}

/* General text, write, caption, info */
.stMarkdown, .stText, .stCaption, p, div:not(.stAlert) {
    color: var(--text-main) !important;
}

.stCaption {
    color: var(--text-muted) !important;
    font-family: var(--mono);
    font-size: 11px;
}

/* Download button */
.stDownloadButton button {
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green)) !important;
    color: white !important;
    font-family: var(--mono);
    font-size: 13px;
    letter-spacing: 2px;
    border: none;
    border-radius: 4px;
    padding: 10px 24px;
    transition: 0.2s;
}

.stDownloadButton button:hover {
    opacity: 0.85;
}

/* Input summary (st.write lines) */
.stMarkdown p, .stText p {
    color: var(--text-main);
}

/* Sidebar inputs already styled via default Streamlit, but we can refine */
[data-testid="stSidebar"] .stNumberInput input {
    background-color: #040E19 !important;
    color: var(--accent-blue) !important;
    border: 1px solid var(--border);
    border-radius: 4px;
}

[data-testid="stSidebar"] label {
    color: var(--text-label) !important;
}

/* Button in sidebar */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, var(--mid-blue), var(--mid-green));
    color: white;
    font-family: var(--mono);
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  BACKEND FUNCTIONS (UNCHANGED)
# ─────────────────────────────────────────────────────────────
def calc_burden(diameter: float, rock_density: float) -> float:
    return 25 * diameter * (1 / rock_density)

def calc_spacing(burden: float) -> float:
    return 1.25 * burden

def calc_holes(area: float, burden: float, spacing: float) -> int:
    return max(1, int(area / (burden * spacing)))

def calc_charge_per_hole(diameter: float, bench_height: float,
                          explosive_density: float) -> float:
    radius = diameter / 2
    volume = math.pi * (radius ** 2) * bench_height
    return volume * explosive_density

def calc_powder_factor(total_explosive: float, rock_volume: float) -> float:
    return total_explosive / rock_volume

def calc_total_cost(total_explosive: float, unit_cost: float) -> float:
    return total_explosive * unit_cost

def run_design(bench_height, hole_diameter, rock_density,
               explosive_density, unit_cost, area):
    burden      = calc_burden(hole_diameter, rock_density)
    spacing     = calc_spacing(burden)
    holes       = calc_holes(area, burden, spacing)
    charge      = calc_charge_per_hole(hole_diameter, bench_height, explosive_density)
    total_exp   = charge * holes
    rock_vol    = area * bench_height
    pf          = calc_powder_factor(total_exp, rock_vol)
    cost        = calc_total_cost(total_exp, unit_cost)
    return dict(burden=burden, spacing=spacing, holes=holes, charge=charge,
                total_exp=total_exp, rock_vol=rock_vol, pf=pf, cost=cost)

def generate_report_text(inputs: dict, results: dict) -> str:
    ts = datetime.now().strftime("%d %B %Y   %H:%M:%S")
    return f"""
BLAST DESIGN REPORT
{ts}

Burden: {results['burden']:.3f} m
Spacing: {results['spacing']:.3f} m
Holes: {results['holes']}
Charge per Hole: {results['charge']:.4f} t

Total Explosive: {results['total_exp']:.3f} t
Rock Volume: {results['rock_vol']:.2f} m³
Powder Factor: {results['pf']:.4f}

Cost: ${results['cost']:,.2f}
"""

# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ INPUT PARAMETERS")
    rock_density      = st.number_input("Rock Density (t/m³)", 0.1, value=2.7)
    bench_height      = st.number_input("Bench Height (m)", 0.1, value=10.0)
    area              = st.number_input("Bench Area (m²)", 1.0, value=5000.0)
    hole_diameter     = st.number_input("Hole Diameter (m)", 0.01, value=0.115)
    explosive_density = st.number_input("Explosive Density (t/m³)", 0.1, value=0.85)
    unit_cost         = st.number_input("Unit Cost ($/t)", 0.0, value=450.0)

    run_btn = st.button("CALCULATE")

# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────
st.title("💥 Blast Design & Cost Estimation")
st.caption("Open-Pit Mining | Drill & Blast Engineering Tool")

if run_btn or "results" not in st.session_state:
    inputs = dict(
        bench_height=bench_height,
        hole_diameter=hole_diameter,
        rock_density=rock_density,
        explosive_density=explosive_density,
        unit_cost=unit_cost,
        area=area,
    )
    results = run_design(**inputs)
    st.session_state["results"] = results
    st.session_state["inputs"] = inputs

results = st.session_state["results"]
inputs  = st.session_state["inputs"]

# ─────────────────────────────────────────────────────────────
#  OUTPUT SECTION
# ─────────────────────────────────────────────────────────────

st.subheader("Drill Design Parameters")

col1, col2 = st.columns(2)

with col1:
    st.metric("Burden (m)", f"{results['burden']:.3f}")
    st.metric("Spacing (m)", f"{results['spacing']:.3f}")
    st.metric("Number of Holes", results['holes'])

with col2:
    st.metric("Charge per Hole (t)", f"{results['charge']:.4f}")
    st.metric("Total Explosive (t)", f"{results['total_exp']:.3f}")

st.divider()

st.subheader("Explosive & Rock Volume")

col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Rock Volume (m³)", f"{results['rock_vol']:.2f}")

with col4:
    st.metric("Powder Factor (t/m³)", f"{results['pf']:.4f}")

with col5:
    st.metric("Bench Area (m²)", f"{inputs['area']:.1f}")

st.divider()

st.subheader("Cost Estimation")

st.metric("Total Blasting Cost ($)", f"{results['cost']:,.2f}")

st.caption(f"Based on {results['total_exp']:.3f} t × ${inputs['unit_cost']:.2f}/t")

st.divider()

st.subheader("Input Summary")

st.write(f"**Bench Height:** {inputs['bench_height']:.1f} m")
st.write(f"**Hole Diameter:** {inputs['hole_diameter']:.4f} m")
st.write(f"**Rock Density:** {inputs['rock_density']:.2f} t/m³")
st.write(f"**Explosive Density:** {inputs['explosive_density']:.2f} t/m³")
st.write(f"**Bench Area:** {inputs['area']:.1f} m²")
st.write(f"**Unit Cost:** ${inputs['unit_cost']:.2f} /t")

# ─────────────────────────────────────────────────────────────
#  DOWNLOAD REPORT
# ─────────────────────────────────────────────────────────────
report_text = generate_report_text(inputs, results)

st.download_button(
    "📄 Download Report (TXT)",
    report_text,
    file_name="blast_report.txt"
)
