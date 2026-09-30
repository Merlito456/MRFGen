import streamlit as st
from datetime import date
from mrf_generator import generate_mrf, build_mrf_name

st.set_page_config(page_title="MRF Generator", page_icon="📦", layout="wide")

st.title("📦 Material Request Form (MRF) Generator")
st.caption("NOKIA-FN MRF Generator — powered by Streamlit")

# ---------------- Sidebar: Meta ----------------
with st.sidebar:
    st.header("⚙️ MRF Metadata")
    req_date = st.date_input("Date", value=date.today())
    request_no = st.text_input("Request No.", value="004")
    site_id_meta = st.text_input("Site ID (for filename)", value="MIN132")
    site_name = st.text_input("Site Name", value="MIN132")
    olt_type = st.text_input("OLT Type", value="BA")
    subcon = st.text_input("Subcon", value="SUBCON")

# ---------------- Header info ----------------
st.subheader("1️⃣ Header Information")
c1, c2 = st.columns(2)
with c1:
    destination = st.text_input("Destination Code", value="")
    site_id = st.text_input("Site ID", value=site_id_meta)
with c2:
    destination_full = st.text_input("Destination (Full)", value="")
    site_address = st.text_area("Site Address", value="", height=80)

# ---------------- Equipment Parts ----------------
st.subheader("2️⃣ Equipment Parts (max 8)")
if "equipment" not in st.session_state:
    st.session_state.equipment = [{"part_no": "", "description": "", "qty_req": 0}]

eq_cols = st.columns([3, 1])
with eq_cols[1]:
    if st.button("➕ Add Equipment Row", use_container_width=True):
        if len(st.session_state.equipment) < 8:
            st.session_state.equipment.append({"part_no": "", "description": "", "qty_req": 0})

for i, item in enumerate(st.session_state.equipment):
    cols = st.columns([3, 5, 2, 1])
    item["part_no"] = cols[0].text_input(f"Part No. #{i+1}", value=item["part_no"], key=f"eq_pn_{i}")
    item["description"] = cols[1].text_input(f"Description #{i+1}", value=item["description"], key=f"eq_ds_{i}")
    item["qty_req"] = cols[2].number_input(f"Qty Req #{i+1}", min_value=0, value=int(item["qty_req"]), key=f"eq_qty_{i}")
    if cols[3].button("🗑️", key=f"eq_del_{i}") and len(st.session_state.equipment) > 1:
        st.session_state.equipment.pop(i)
        st.rerun()

# ---------------- Local Materials ----------------
st.subheader("3️⃣ Local Materials / Accessories (max 20)")
if "local" not in st.session_state:
    st.session_state.local = [{"part_no": "", "description": "", "qty_req": 0, "unit": "pcs"}]

lm_cols = st.columns([3, 1])
with lm_cols[1]:
    if st.button("➕ Add Local Row", use_container_width=True):
        if len(st.session_state.local) < 20:
            st.session_state.local.append({"part_no": "", "description": "", "qty_req": 0, "unit": "pcs"})

for i, item in enumerate(st.session_state.local):
    cols = st.columns([3, 5, 2, 2, 1])
    item["part_no"] = cols[0].text_input(f"Part No. L#{i+1}", value=item["part_no"], key=f"lm_pn_{i}")
    item["description"] = cols[1].text_input(f"Description L#{i+1}", value=item["description"], key=f"lm_ds_{i}")
    item["qty_req"] = cols[2].number_input(f"Qty Req L#{i+1}", min_value=0, value=int(item["qty_req"]), key=f"lm_qty_{i}")
    item["unit"] = cols[3].selectbox(
        f"Unit L#{i+1}", ["pcs", "pc", "m", "ft", "box", "roll", "set"],
        index=["pcs","pc","m","ft","box","roll","set"].index(item["unit"]),
        key=f"lm_unit_{i}"
    )
    if cols[4].button("🗑️", key=f"lm_del_{i}") and len(st.session_state.local) > 1:
        st.session_state.local.pop(i)
        st.rerun()

# ---------------- Signatories ----------------
st.subheader("4️⃣ Signatories")
c1, c2, c3 = st.columns(3)
request_by = c1.text_input("Requested By", value="")
receiver1 = c2.text_input("Receiver 1", value="")
receiver2 = c3.text_input("Receiver 2", value="")

# ---------------- Preview MRF Name ----------------
mrf_name_preview = build_mrf_name(
    month=req_date.month, day=req_date.day, year=req_date.year,
    request_no=request_no, site_id=site_id_meta, site_name=site_name,
    olt_type=olt_type, subcon=subcon
)
st.info(f"**MRF Name (auto):** `{mrf_name_preview}`")

# ---------------- Generate ----------------
st.divider()
if st.button("🚀 Generate MRF", type="primary", use_container_width=True):
    payload = {
        "date": req_date.strftime("%Y-%m-%d"),
        "destination": destination or destination_full,
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
    }
    try:
        xlsx_bytes = generate_mrf(payload)
        st.success("✅ MRF generated successfully!")
        st.download_button(
            label="📥 Download MRF (.xlsx)",
            data=xlsx_bytes,
            file_name=f"{mrf_name_preview}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"❌ Error: {e}")
