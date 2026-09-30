import openpyxl
from openpyxl.styles import Alignment
from datetime import datetime
from copy import copy
import io

TEMPLATE_PATH = "MRF_template.xlsx"
SHEET_NAME = "NOKIA-FN_09152026-004_MIN132-BA"

# ---------- Row/Column mapping ----------
DATE_ROW = 6
DESTINATION_ROW = 8
SITE_ID_ROW = 10
SITE_ADDRESS_ROW = 11   # spans 11-12

EQUIP_ROWS = range(18, 26)      # 18..25
LOCAL_ROWS = range(27, 47)      # 27..46

REQUEST_BY_ROWS = range(48, 50) # 48..49 col A
RECEIVER1_ROW = 47              # col D-F-G
RECEIVER2_ROW = 48              # col D-F-G

MRF_NAME_ROW = 56               # col F

# Columns
COL_PART = "A"
COL_DESC = "B"
COL_QTY_REQ = "D"
COL_QTY_ISSUED = "E"   # used to indicate unit (pcs, pc, m, etc.)


def _set_cell(ws, row, col, value):
    if value is None or value == "":
        return
    cell = ws[f"{col}{row}"]
    cell.value = value
    cell.alignment = Alignment(wrap_text=True, vertical="center")


def build_mrf_name(month, day, year, request_no, site_id, site_name, olt_type, subcon):
    """Format: NOKIA-FN_MONTHDAYYEAR-REQUESTNO_SITEID_SITENAME_OLTTYPE_SUBCON"""
    date_part = f"{month:02d}{day:02d}{year}"
    return f"NOKIA-FN_{date_part}-{request_no}_{site_id}_{site_name}_{olt_type}_{subcon}"


def generate_mrf(data: dict) -> bytes:
    """
    data structure:
    {
        "date": "2026-09-15",             # ISO date
        "destination": "...",
        "site_id": "...",
        "site_address": "...",
        "equipment": [                    # up to 8
            {"part_no": "...", "description": "...", "qty_req": 1}
        ],
        "local_materials": [              # up to 20
            {"part_no": "...", "description": "...", "qty_req": 1, "unit": "pcs"}
        ],
        "request_by": "...",
        "receiver1": "...",
        "receiver2": "...",
        "request_no": "004",
        "site_name": "MIN132",
        "olt_type": "BA",
        "subcon": "SUBCON"
    }
    """
    wb = openpyxl.load_workbook(TEMPLATE_PATH)
    ws = wb[SHEET_NAME]

    # ---- Header ----
    if data.get("date"):
        d = datetime.strptime(data["date"], "%Y-%m-%d")
        _set_cell(ws, DATE_ROW, "E", d.strftime("%B %d, %Y"))
        _set_cell(ws, DATE_ROW, "F", "")
        _set_cell(ws, DATE_ROW, "G", "")

    _set_cell(ws, DESTINATION_ROW, "E", data.get("destination"))
    _set_cell(ws, SITE_ID_ROW, "E", data.get("site_id"))
    _set_cell(ws, SITE_ADDRESS_ROW, "E", data.get("site_address"))

    # ---- Equipment parts ----
    for i, row in enumerate(EQUIP_ROWS):
        if i < len(data.get("equipment", [])):
            item = data["equipment"][i]
            _set_cell(ws, row, COL_PART, item.get("part_no"))
            _set_cell(ws, row, COL_DESC, item.get("description"))
            _set_cell(ws, row, COL_QTY_REQ, item.get("qty_req"))

    # ---- Local materials ----
    for i, row in enumerate(LOCAL_ROWS):
        if i < len(data.get("local_materials", [])):
            item = data["local_materials"][i]
            _set_cell(ws, row, COL_PART, item.get("part_no"))
            _set_cell(ws, row, COL_DESC, item.get("description"))
            _set_cell(ws, row, COL_QTY_REQ, item.get("qty_req"))
            _set_cell(ws, row, COL_QTY_ISSUED, item.get("unit"))

    # ---- Signatories ----
    _set_cell(ws, REQUEST_BY_ROWS.start, COL_PART, data.get("request_by"))
    _set_cell(ws, RECEIVER1_ROW, "D", data.get("receiver1"))
    _set_cell(ws, RECEIVER2_ROW, "D", data.get("receiver2"))

    # ---- MRF Name ----
    if data.get("date"):
        d = datetime.strptime(data["date"], "%Y-%m-%d")
        mrf_name = build_mrf_name(
            month=d.month,
            day=d.day,
            year=d.year,
            request_no=data.get("request_no", "001"),
            site_id=data.get("site_id", ""),
            site_name=data.get("site_name", ""),
            olt_type=data.get("olt_type", ""),
            subcon=data.get("subcon", ""),
        )
        _set_cell(ws, MRF_NAME_ROW, "F", mrf_name)

    # ---- Save to bytes ----
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()
