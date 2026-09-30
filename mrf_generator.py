import openpyxl
from openpyxl.styles import Alignment
from datetime import datetime
import io

TEMPLATE_PATH = "MRF_template.xlsx"
SHEET_NAME = "NOKIA-FN_09152026-004_MIN132-BA"

# ---------- Row/Column mapping ----------
DATE_ROW = 6
DESTINATION_ROW = 8
SITE_ID_ROW = 10
SITE_ADDRESS_ROW = 11

# Merged block: rows 18..46 used as ONE continuous table
MERGED_ROWS = list(range(18, 26)) + list(range(27, 47))   # 8 + 20 = 28 slots

REQUEST_BY_ROW = 48
RECEIVER1_ROW = 47
RECEIVER2_ROW = 48
MRF_NAME_ROW = 56

COL_PART = "A"
COL_DESC = "B"
COL_QTY_REQ = "D"
COL_UNIT = "E"   # still shows unit (pcs, m, etc.)


def _set_cell(ws, row, col, value):
    if value is None or value == "":
        return
    cell = ws[f"{col}{row}"]
    cell.value = value
    cell.alignment = Alignment(wrap_text=True, vertical="center")


def build_mrf_name(month, day, year, request_no, site_id, site_name,
                   olt_type, subcon, project_type=None):
    """Format: NOKIA-FN_MONTHDAYYEAR-REQUESTNO_SITEID_SITENAME_OLTTYPE_SUBCON"""
    date_part = f"{month:02d}{day:02d}{year}"
    parts = ["NOKIA-FN", f"{date_part}-{request_no}", site_id, site_name,
             olt_type, subcon]
    if project_type:
        parts.append(project_type.replace(" ", ""))
    return "_".join(p for p in parts if p)


def generate_mrf(data: dict) -> bytes:
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb[SHEET_NAME]

    # ---- Header ----
    if data.get("date"):
        d = datetime.strptime(data["date"], "%Y-%m-%d")
        _set_cell(ws, DATE_ROW, "E", d.strftime("%B %d, %Y"))

    _set_cell(ws, DESTINATION_ROW, "E", data.get("destination"))
    _set_cell(ws, SITE_ID_ROW, "E", data.get("site_id"))
    _set_cell(ws, SITE_ADDRESS_ROW, "E", data.get("site_address"))

    # ---- Merged Materials (single continuous list, single QTY column) ----
    items = data.get("materials", [])
    for i, row in enumerate(MERGED_ROWS):
        if i >= len(items):
            break
        item = items[i]
        _set_cell(ws, row, COL_PART, item.get("part_no"))
        _set_cell(ws, row, COL_DESC, item.get("description"))
        _set_cell(ws, row, COL_QTY_REQ, item.get("qty_req"))
        _set_cell(ws, row, COL_UNIT, item.get("unit"))

    # ---- Signatories ----
    _set_cell(ws, REQUEST_BY_ROW, COL_PART, data.get("request_by"))
    _set_cell(ws, RECEIVER1_ROW, "D", data.get("receiver1"))
    _set_cell(ws, RECEIVER2_ROW, "D", data.get("receiver2"))

    # ---- MRF Name ----
    if data.get("date"):
        d = datetime.strptime(data["date"], "%Y-%m-%d")
        mrf_name = build_mrf_name(
            month=d.month, day=d.day, year=d.year,
            request_no=data.get("request_no", "001"),
            site_id=data.get("site_id", ""),
            site_name=data.get("site_name", ""),
            olt_type=data.get("olt_type", ""),
            subcon=data.get("subcon", ""),
            project_type=data.get("project_type"),
        )
        _set_cell(ws, MRF_NAME_ROW, "F", mrf_name)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()
