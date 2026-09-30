import streamlit as st
from datetime import date
from mrf_generator import generate_mrf, build_mrf_name
from references import get_reference

st.set_page_config(page_title="MRF Generator", page_icon="📦", layout="wide")
st.title("📦 Material Request Form (MRF) Generator")

# ---------------- Sidebar: Metadata ----------------
with st.sidebar:
    st.header("⚙️ MRF Metadata")
    req_date = st.date_input("Date", value=date.today())
    request_no = st.text_input("Request No.", value="001")
    site_id_meta = st.text_input("Site ID", value="MIN355-LCGCDO")
    site_name = st.text_input("Site Name", value="MF2")
    olt_type = st.text_input("OLT Type", value="MF-02")
    subcon = st.text_input("Subcon", value="JOHN_CARLO_RABANES")

# ---------------- Reference Library ----------------
st.subheader("📚 Material Request References")
c1, c2, c3, c4 = st.columns([2, 2, 2, 2])
project_type = c1.selectbox("Project Type", ["New Build"])
olt = c2.selectbox("OLT", ["MF-02"])
cards = c3.selectbox("# of Cards", [1, 2], index=1)
if c4.button("📥 Load Reference", use_container_width=True):
    ref = get_reference(project_type, olt, cards)
    st.session_state.materials = [
        {"part_no": p, "description": d, "qty_req": q, "unit": ""}
        for p, d, q in ref
    ] or [{"part_no": "", "description": "", "qty_req": "", "unit": ""}]
    st.success(f"✅ Loaded {len(ref)} part(s)")
    st.rerun()

# ---------------- Header Info ----------------
st.subheader("1️⃣ Header Information")
h1, h2 = st.columns(2)
destination = h1.text_input("Destination Code", value="CAGAYAN DE ORO")
site_id = h2.text_input("Site ID (in sheet)", value=site_id_meta)
site_address = st.text_area(
    "Site Address",
    value="Osmeña Extension Cagayan de Oro City_Barangay 22 (Pob.), "
          "Cagayan De Oro City, Misamis Oriental",
    height=80,
)

# ---------------- MERGED Materials Table ----------------
st.subheader("2️⃣ Materials (Equipment + Local — single combined list, max 28)")

if "materials" not in st.session_state:
    st.session_state.materials = [{"part_no": "", "description": "", "qty_req": "", "unit": ""}]

b1, b2, _ = st.columns([1, 1, 6])
if b1.button("➕ Add Row"):
    if len(st.session_state.materials) < 28:
        st.session_state.materials.append(
            {"part_no": "", "description": "", "qty_req": "", "unit": ""}
        )
if b2.button("🧹 Clear All"):
    st.session_state.materials = [{"part_no": "", "description": "", "qty_req": "", "unit": ""}]
    st.rerun()

UNITS = ["", "pcs", "pc", "m", "ft", "box", "roll", "set"]

# Header row
hdr = st.columns([3, 6, 2, 2, 1])
hdr[0].markdown("**PART NUMBER**")
hdr[1].markdown("**DESCRIPTION**")
hdr[2].markdown("**QTY REQ (TOTAL)**")
hdr[3].markdown("**UNIT**")
hdr[4].markdown("**✖**")

total_qty = 0
for i, item in enumerate(st.session_state.materials):
    cols = st.columns([3, 6, 2, 2, 1])

    item["part_no"] = cols[0].text_input(
        f"pn_{i}", item["part_no"],
        key=f"m_pn_{i}", label_visibility="collapsed",
    )
    item["description"] = cols[1].text_input(
        f"ds_{i}", item["description"],
        key=f"m_ds_{i}", label_visibility="collapsed",
    )

    # --- QTY: text_input so blank stays blank ---
    raw_qty = cols[2].text_input(
        f"q_{i}",
        value="" if item["qty_req"] in ("", 0, None) else str(item["qty_req"]),
        key=f"m_q_{i}",
        label_visibility="collapsed",
        placeholder="0",
    )
    # Normalize: keep as int if numeric, else keep blank
    stripped = raw_qty.strip()
    if stripped.isdigit():
        item["qty_req"] = int(stripped)
    elif stripped == "":
        item["qty_req"] = ""
    else:
        item["qty_req"] = stripped  # allow text just in case

    item["unit"] = cols[3].selectbox(
        f"u_{i}", UNITS,
        index=UNITS.index(item["unit"]) if item["unit"] in UNITS else 0,
        key=f"m_u_{i}", label_visibility="collapsed",
    )

    if cols[4].button("🗑️", key=f"m_del_{i}") and len(st.session_state.materials) > 1:
        st.session_state.materials.pop(i)
        st.rerun()

    # Total: only add numeric values
    if isinstance(item["qty_req"], int):
        total_qty += item["qty_req"]

st.markdown(f"### 🧮 **TOTAL QUANTITY: `{total_qty}`**")

# ---------------- Signatories ----------------
st.subheader("3️⃣ Signatories")
s1, s2, s3 = st.columns(3)
request_by = s1.text_input("Requested By", value="JOHN CARLO RABANES")
receiver1 = s2.text_input("Receiver 1", value="NOKIA INHOUSE - JOHN CARLO RABANES/09669343065")
receiver2 = s3.text_input("Receiver 2", value="DNA SUBCON - EASTMOND MIRANDA/09543991868")

# ---------------- Preview ----------------
preview = build_mrf_name(
    month=req_date.month, day=req_date.day, year=req_date.year,
    request_no=request_no, site_id=site_id_meta, site_name=site_name,
    olt_type=olt_type, subcon=subcon, project_type=project_type,
)
st.info(f"**Auto MRF Name:** `{preview}`")

# ---------------- Generate ----------------
st.divider()
if st.button("🚀 Generate MRF", type="primary", use_container_width=True):
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
        st.success(f"✅ MRF generated! Total Quantity: **{total_qty}**")
        st.download_button(
            "📥 Download MRF (.xlsx)",
            data=xlsx,
            file_name=f"{preview}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"❌ Error: {e}")
