import streamlit as st
from datetime import date
from mrf_generator import generate_mrf, build_mrf_name
from references import get_reference

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="MRF Generator",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main { background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%); }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px; }

    .hero {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%);
        padding: 2rem 2.5rem; border-radius: 20px; color: white;
        margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(30, 64, 175, 0.25);
    }
    .hero h1 { font-size: 2.2rem; font-weight: 800; margin: 0 0 0.5rem 0; letter-spacing: -0.02em; }
    .hero p { font-size: 1rem; opacity: 0.9; margin: 0; }

    .section-title {
        font-size: 1.15rem; font-weight: 700; color: #1e293b;
        margin: 1.5rem 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;
        padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0;
    }

    .metric-card {
        background: white; border-radius: 14px; padding: 1.2rem 1.5rem;
        border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }
    .metric-card:hover { box-shadow: 0 6px 16px rgba(0,0,0,0.08); transform: translateY(-2px); }
    .metric-label {
        font-size: 0.75rem; font-weight: 600; color: #64748b;
        text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem;
    }
    .metric-value { font-size: 1.6rem; font-weight: 800; color: #0f172a; line-height: 1.1; }
    .metric-value.blue { color: #3b82f6; }
    .metric-value.green { color: #10b981; }
    .metric-value.purple { color: #8b5cf6; }

    .table-header {
        background: linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 100%);
        padding: 0.6rem 1rem; border-radius: 10px;
        font-size: 0.72rem; font-weight: 700; color: #475569;
        text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem;
    }

    .ref-panel {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 1px solid #bae6fd; border-radius: 14px;
        padding: 1.2rem 1.5rem; margin-bottom: 1rem;
    }

    .stButton > button {
        border-radius: 10px; font-weight: 600;
        transition: all 0.15s ease; border: 1px solid #cbd5e1;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        border: none; color: white; font-weight: 700; font-size: 1rem;
        padding: 0.7rem 1rem; box-shadow: 0 6px 20px rgba(30, 64, 175, 0.3);
    }
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #059669, #10b981);
        color: white; border: none; font-weight: 700;
        padding: 0.7rem 1rem; box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
    }

    .stTextInput input, .stNumberInput input, .stTextArea textarea {
        border-radius: 8px; border: 1px solid #e2e8f0;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px; background: #f1f5f9; padding: 6px; border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; padding: 8px 20px; font-weight: 600; color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background: white !important; color: #1e40af !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# AUTO-UNIT DETECTION
# ============================================================
UNIT_RULES = [
    (["velcro", "10m/roll"], "roll"),
    (["patch cord", "patchcord"], "pcs"),
    (["cable shoe", "lugs", "terminal lug"], "pcs"),
    (["grounding cable", "wire grounding"], "m"),
    (["power cable", "positive power"], "pcs"),
    (["plastic cable tie", "tie white"], "pcs"),
    (["shrinkable"], "pcs"),
    (["labeller", "label tape"], "pc"),
    (["spiral wrap"], "pc"),
    (["shelf", "fan module", "line board", "lmnt", "lmxr", "lwlt"], "pc"),
    (["transceiver", "sfp", "xgspon", "pon"], "pcs"),
    (["dummy", "dmmy", "plate"], "pcs"),
]


def detect_unit(part_no: str, description: str) -> str:
    haystack = f"{part_no or ''} {description or ''}".lower()
    for keywords, unit in UNIT_RULES:
        if any(kw in haystack for kw in keywords):
            return unit
    return ""


def auto_unit_for_item(item: dict) -> str:
    existing = (item.get("unit") or "").strip()
    if existing:
        return existing
    return detect_unit(item.get("part_no", ""), item.get("description", ""))


# ============================================================
# SESSION STATE INIT
# ============================================================
if "materials" not in st.session_state:
    st.session_state.materials = [
        {"part_no": "", "description": "", "qty_req": "", "unit": "", "note": ""}
    ]

# ============================================================
# HERO HEADER
# ============================================================
st.markdown("""
<div class="hero">
    <h1>📦 Material Request Form Generator</h1>
    <p>NOKIA-FN · Streamline your MRF creation in seconds</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR — METADATA
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ MRF Metadata")
    req_date = st.date_input("📅 Date", value=date.today(), key="meta_date")
    request_no = st.text_input("🔢 Request No.", value="001", key="meta_req_no")

    st.markdown("---")
    st.markdown("##### 🏢 Site Details")
    site_id_meta = st.text_input("Site ID", value="MIN355-LCGCDO", key="meta_site_id")
    site_name = st.text_input("Site Name", value="MF2", key="meta_site_name")
    olt_type = st.text_input("OLT Type", value="MF-02", key="meta_olt_type")
    subcon = st.text_input("Subcon", value="JOHN_CARLO_RABANES", key="meta_subcon")

    st.markdown("---")
    auto_unit_enabled = st.toggle(
        "🔮 Auto-detect units", value=True,
        help="Automatically assign units based on part number & description",
        key="meta_auto_unit",
    )
    st.markdown("---")
    st.caption("💡 **Tip:** Load a reference preset to autofill common MF-02 builds.")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📚  References", "📝  Materials", "✍️  Signatories"])

# ------------------------------------------------------------
# TAB 1 — REFERENCES
# ------------------------------------------------------------
with tab1:
    st.markdown('<div class="section-title">📚 Material Request References</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="ref-panel">
        <b>💡 Quick Start:</b> Pick a project type, OLT model, and number of cards.
        Click <b>Load Reference</b> to autofill the materials table with the standard build kit.
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    project_type = c1.selectbox("🏗 Project Type", ["New Build"], key="ref_project_type")
    olt = c2.selectbox("📡 OLT Model", ["MF-02"], key="ref_olt")
    cards = c3.selectbox("🃏 # of Cards", [1, 2], index=1, key="ref_cards")

    col_a, col_b, _ = st.columns([1, 1, 3])
    with col_a:
        if st.button("📥 Load Reference", use_container_width=True,
                     type="primary", key="load_reference_btn"):
            ref = get_reference(project_type, olt, cards)
            st.session_state.materials = [
                {"part_no": p, "description": d, "qty_req": q, "unit": u, "note": n}
                for p, d, q, u, n in ref
            ] or [{"part_no": "", "description": "", "qty_req": "", "unit": "", "note": ""}]
            st.success(f"✅ Loaded {len(ref)} part(s)")
            st.rerun()
    with col_b:
        if st.button("🧹 Clear All", use_container_width=True,
                     key="clear_all_references"):
            st.session_state.materials = [
                {"part_no": "", "description": "", "qty_req": "", "unit": "", "note": ""}
            ]
            st.rerun()

# ------------------------------------------------------------
# TAB 2 — MATERIALS
# ------------------------------------------------------------
with tab2:
    st.markdown('<div class="section-title">📝 Materials (Equipment + Local)</div>',
                unsafe_allow_html=True)

    # ---- Metric Cards ----
    m1, m2, m3, m4 = st.columns(4)

    total_items = sum(
        1 for it in st.session_state.materials
        if (it.get("part_no") or "").strip() or (it.get("description") or "").strip()
    )
    total_qty = sum(
        int(it["qty_req"]) for it in st.session_state.materials
        if isinstance(it.get("qty_req"), int)
    )
    total_notes = sum(
        1 for it in st.session_state.materials if (it.get("note") or "").strip()
    )
    max_slots = 28
    remaining = max_slots - len(st.session_state.materials)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📦 Total Items</div>
            <div class="metric-value blue">{total_items}</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🧮 Total Quantity</div>
            <div class="metric-value green">{total_qty}</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📝 Notes</div>
            <div class="metric-value purple">{total_notes}</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">➕ Slots Left</div>
            <div class="metric-value">{remaining}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    # ---- Action Buttons ----
    b1, b2, _, b3 = st.columns([1, 1, 3, 1])
    with b1:
        if st.button("➕ Add Row", use_container_width=True,
                     key="add_row_materials"):
            if len(st.session_state.materials) < max_slots:
                st.session_state.materials.append(
                    {"part_no": "", "description": "", "qty_req": "", "unit": "", "note": ""}
                )
                st.rerun()
            else:
                st.warning(f"⚠️ Maximum {max_slots} rows reached.")
    with b2:
        if st.button("🧹 Clear All", use_container_width=True,
                     key="clear_all_materials"):
            st.session_state.materials = [
                {"part_no": "", "description": "", "qty_req": "", "unit": "", "note": ""}
            ]
            st.rerun()
    with b3:
        if auto_unit_enabled:
            if st.button("🔮 Re-detect Units", use_container_width=True,
                         key="redetect_units_btn"):
                for it in st.session_state.materials:
                    it["unit"] = detect_unit(it.get("part_no", ""),
                                             it.get("description", ""))
                st.rerun()

    # ---- Table Header ----
    st.markdown('<div class="table-header">', unsafe_allow_html=True)
    hdr = st.columns([3, 5.5, 1.5, 1.5, 3.5, 0.6])
    hdr[0].markdown("**PART NUMBER**")
    hdr[1].markdown("**DESCRIPTION**")
    hdr[2].markdown("**QTY**")
    hdr[3].markdown("**UNIT**")
    hdr[4].markdown("**📝 NOTE**")
    hdr[5].markdown("**✖**")
    st.markdown('</div>', unsafe_allow_html=True)

    UNITS = ["", "pcs", "pc", "m", "ft", "box", "roll", "set"]

    for i, item in enumerate(st.session_state.materials):
        cols = st.columns([3, 5.5, 1.5, 1.5, 3.5, 0.6])

        item["part_no"] = cols[0].text_input(
            f"pn_{i}", item["part_no"],
            key=f"m_pn_{i}", label_visibility="collapsed",
            placeholder="e.g. 3FE76762AA",
        )
        item["description"] = cols[1].text_input(
            f"ds_{i}", item["description"],
            key=f"m_ds_{i}", label_visibility="collapsed",
            placeholder="Description...",
        )

        # --- QTY ---
        raw_qty = cols[2].text_input(
            f"q_{i}",
            value="" if item["qty_req"] in ("", 0, None) else str(item["qty_req"]),
            key=f"m_q_{i}", label_visibility="collapsed", placeholder="0",
        )
        stripped = raw_qty.strip()
        if stripped.isdigit():
            item["qty_req"] = int(stripped)
        elif stripped == "":
            item["qty_req"] = ""
        else:
            item["qty_req"] = stripped

        # --- UNIT ---
        detected = auto_unit_for_item(item) if auto_unit_enabled else (item.get("unit") or "")
        current_unit = item.get("unit") or detected
        unit_index = UNITS.index(current_unit) if current_unit in UNITS else 0

        item["unit"] = cols[3].selectbox(
            f"u_{i}", UNITS, index=unit_index,
            key=f"m_u_{i}", label_visibility="collapsed",
        )
        if auto_unit_enabled and not item["unit"]:
            item["unit"] = detected

        # --- NOTE ---
        item["note"] = cols[4].text_input(
            f"note_{i}", item.get("note", ""),
            key=f"m_note_{i}", label_visibility="collapsed",
            placeholder="e.g. 16 if two LT cards",
        )

        # --- DELETE ---
        if cols[5].button("🗑️", key=f"m_del_{i}") and len(st.session_state.materials) > 1:
            st.session_state.materials.pop(i)
            st.rerun()

# ------------------------------------------------------------
# TAB 3 — SIGNATORIES + HEADER INFO
# ------------------------------------------------------------
with tab3:
    st.markdown('<div class="section-title">📋 Header Information</div>',
                unsafe_allow_html=True)

    h1, h2 = st.columns(2)
    destination = h1.text_input("🎯 Destination Code", value="CAGAYAN DE ORO",
                                key="hdr_destination")
    site_id = h2.text_input("🏷 Site ID (in sheet)", value=site_id_meta,
                            key="hdr_site_id")
    site_address = st.text_area(
        "📍 Site Address",
        value="Osmeña Extension Cagayan de Oro City_Barangay 22 (Pob.), "
              "Cagayan De Oro City, Misamis Oriental",
        height=80,
        key="hdr_site_address",
    )

    st.markdown('<div class="section-title">✍️ Signatories</div>',
                unsafe_allow_html=True)

    s1, s2, s3 = st.columns(3)
    request_by = s1.text_input("👤 Requested By", value="JOHN CARLO RABANES",
                               key="sig_request_by")
    receiver1 = s2.text_input("📥 Receiver 1",
                              value="NOKIA INHOUSE - JOHN CARLO RABANES/09669343065",
                              key="sig_receiver1")
    receiver2 = s3.text_input("📤 Receiver 2",
                              value="DNA SUBCON - EASTMOND MIRANDA/09543991868",
                              key="sig_receiver2")

    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

    preview = build_mrf_name(
        month=req_date.month, day=req_date.day, year=req_date.year,
        request_no=request_no, site_id=site_id_meta, site_name=site_name,
        olt_type=olt_type, subcon=subcon, project_type=project_type,
    )
    st.markdown(f"""
    <div class="ref-panel">
        <div class="metric-label">🏷 Auto-generated MRF Name</div>
        <code style="font-size:0.95rem; color:#1e40af;">{preview}</code>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# GENERATE & DOWNLOAD
# ============================================================
st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">🚀 Generate & Download</div>',
            unsafe_allow_html=True)

g1, g2 = st.columns([1, 1])

with g1:
    if st.button("🚀 Generate MRF", type="primary",
                 use_container_width=True, key="generate_mrf_btn"):
        payload = {
            "date": req_date.strftime("%Y-%m-%d"),
            "destination": destination,
            "site_id": site_id,
            "site_address": site_address,
            "materials": st.session_state.materials,
            "request_by": request_by,
            "receiver1": receiver1,
            "receiver2": receiver2,
            "request_no": request_no,
            "site_name": site_name,
            "olt_type": olt_type,
            "subcon": subcon,
            "project_type": project_type,
        }
        try:
            xlsx = generate_mrf(payload)
            st.session_state["_xlsx"] = xlsx
            st.session_state["_fname"] = f"{preview}.xlsx"
            st.session_state["_preview"] = preview
            st.success(f"✅ MRF generated! Total Quantity: **{total_qty}**")
        except Exception as e:
            st.error(f"❌ Error: {e}")

with g2:
    if "_xlsx" in st.session_state:
        st.download_button(
            "📥 Download MRF (.xlsx)",
            data=st.session_state["_xlsx"],
            file_name=st.session_state["_fname"],
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="download_mrf_btn",
        )

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:3rem;">
    Built with ❤️ using Streamlit · NOKIA-FN MRF Generator
</div>
""", unsafe_allow_html=True)
