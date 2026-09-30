import streamlit as st
from datetime import date
from mrf_generator import generate_mrf, build_mrf_name
from references import get_equipment, get_local_materials

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
ref_c1, ref_c2, ref_c3 = st.columns(3)
project_type = ref_c1.selectbox("Project Type", ["New Build"])
olt = ref_c2.selectbox("OLT", ["MF-02"])
cards = ref_c3.selectbox("# of Cards", [1, 2], index=1)

if st.button("📥 Load Reference Materials", type="secondary"):
    eq = get_equipment(project_type, olt, cards)
    lm = get_local_materials(project_type, olt, cards)

    st.session_state.equipment = [
        {"part_no": p, "description": d, "qty_req": q} for p, d, q in eq
    ] or [{"part_no": "", "description": "", "qty_req": 0}]

    st.session_state.local = [
        {"part_no": p, "description": d, "qty_req": q, "unit": u}
        for p, d, q, u in lm
    ] or [{"part_no": "", "description": "", "qty_req": 0, "unit": "pcs"}]

    st.success(f"✅ Loaded {len(eq)} equipment + {len(lm)} local material(s)")
    st.rerun()

# ---------------- Header Info ----------------
st.subheader("1️⃣ Header Information")
c1, c2 = st.columns(2)
destination = c1.text_input("Destination Code", value="CAGAYAN DE ORO")
site_id = c2.text_input("Site ID (in sheet)", value=site_id_meta)
site_address = st.text_area(
    "Site Address",
    value="Osmeña Extension Cagayan de Oro City_Barangay 22 (Pob.), "
          "Cagayan De Oro City, Misamis Oriental",
    height=80,
)

# ---------------- Equipment ----------------
st.subheader("2️⃣ Equipment Parts (max 8)")
if "equipment" not in st.session_state:
    st.session_state.equipment = [{"part_no": "", "description": "", "qty_req": 0}]

if st.button("➕ Add Equipment Row"):
    if len(st.session_state.equipment) < 8:
        st.session_state.equipment.append({"part_no": "", "description": "", "qty_req": 0})

for i, item in enumerate(st.session_state.equipment):
    cols = st.columns([3, 5, 2, 1])
    item["part_no"] = cols[0].text_input(f"PN #{i+1}", item["part_no"], key=f"eq_pn_{i}")
    item["description"] = cols[1].text_input(f"Desc #{i+1}", item["description"], key=f"eq_ds_{i}")
    item["qty_req"] = cols[2].number_input(f"Qty #{i+1}", 0, value=int(item["qty_req"]), key=f"eq_qty_{i}")
    if cols[3].button("🗑️", key=f"eq_del_{i}") and len(st.session_state.equipment) > 1:
        st.session_state.equipment.pop(i); st.rerun()

# ---------------- Local Materials ----------------
st.subheader("3️⃣ Local Materials / Accessories (max 20)")
if "local" not in st.session_state:
    st.session_state.local = [{"part_no": "", "description": "", "qty_req": 0, "unit": "pcs"}]

if st.button("➕ Add Local Row"):
    if len(st.session_state.local) < 20:
        st.session_state.local.append({"part_no": "", "description": "", "qty_req": 0, "unit": "pcs"})

UNITS = ["pcs", "pc", "m", "ft", "box", "roll", "set"]
for i, item in enumerate(st.session_state.local):
    cols = st.columns([3, 5, 2, 2, 1])
    item["part_no"] = cols[0].text_input(f"PN L#{i+1}", item["part_no"], key=f"lm_pn_{i}")
    item["description"] = cols[1].text_input(f"Desc L#{i+1}", item["description"], key=f"lm_ds_{i}")
    item["qty_req"] = cols[2].number_input(f"Qty L#{i+1}", 0, value=int(item["qty_req"]), key=f"lm_qty_{i}")
    item["unit"] = cols[3].selectbox(f"Unit L#{i+1}", UNITS, index=UNITS.index(item["unit"]), key=f"lm_u_{i}")
    if cols[4].button("🗑️", key=f"lm_del_{i}") and len(st.session_state.local) > 1:
        st.session_state.local.pop(i); st.rerun()

# ---------------- Signatories ----------------
st.subheader("4️⃣ Signatories")
c1, c2, c3 = st.columns(3)
request_by = c1.text_input("Requested By", value="JOHN CARLO RABANES")
receiver1 = c2.text_input("Receiver 1", value="NOKIA INHOUSE - JOHN CARLO RABANES/09669343065")
receiver2 = c3.text_input("Receiver 2", value="DNA SUBCON - EASTMOND MIRANDA/09543991868")

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
        "equipment": st.session_state.equipment,
        "local_materials": st.session_state.local,
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
        st.success("✅ MRF generated!")
        st.download_button(
            "📥 Download MRF (.xlsx)",
            data=xlsx,
            file_name=f"{preview}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"❌ Error: {e}")
