# references.py
# ==========================================================
# MATERIAL REQUEST REFERENCES
# Project Type : New Build
# OLT          : MF-02
# # of Cards   : 2   /   1
# ==========================================================
# All parts (equipment + local materials) live in ONE list.
# QTY REQ is the single total quantity column.
# ==========================================================

REFERENCES = {
    "New Build": {
        "MF-02": {
            2: [
                # ---------- EQUIPMENT PARTS ----------
                ("3FE76762AA", "Lightspan MF-2 shelf incl. fan unit (LMXR-A)", 1),
                ("3FE76518AA", "MF2-FAN Module", 1),
                ("3FE76559BA", "Lightspan MF-2 DC power module (LPWR-B DC)", 2),
                ("3FE62600AA", "Optical Transceiver SFP+,1310nm SM,10km(brand: Nokia) (10GBase-LR)", 2),
                ("3FE53441AA", "PON Transceiver20km 1310nm(Tx)1490nm(Rx) - GPON SFP B+", 8),
                ("3FE47581AB", "Transcvr XGS-PON/GPON MPM B+(28dBm)Ctemp", 8),
                ("3FE76476AA", "LightspanMF-2 240Gbps NT with clock sync(brand: Nokia) (LMNT-A)", 2),
                ("3FE76353AA", "Lightspan MF 16port Multi-PON Line board (LWLT-C)", 2),

                # ---------- LOCAL MATERIALS / ACCESSORIES ----------
                ("3FE52344FLAA", "Simplex patch cord, LC/UPC - LC/UPC 8m(brand: Nokia)", 2),
                ("Blaine-Spiral-1/2mmx10ft", "Spiral Wrap 10mmx10ft", 1),
                ("L00HLT_VELCRO_10M", "VELCRO (HOOK & LOOP TIE) BLACK 10m/roll", 1),
                ("Blaine-16mm-Shrinkable", "Shrinkable tube 16mm x 200mm", 2),
                ("Blaine-8mmShrinkable", "Shrinkable tube 8mm x 200mm", 2),
                ("Blaine-12mmShrinkable", "Shrinkable tube 12mm x 200mm", 2),
                ("Blaine-Cartridge9mm", "Labeller tape", 1),
                ("L00TL14AWG", "cable shoe (#14 AWG)", 4),
                ("L00Lugs10mm2", "10mm2 Terminal Lugs", 6),
                ("L00Lugs16mm2", "16-10mm2 Terminal Lugs", 2),
                ("L00Lugs8mm2", "terminal lugs 8mm", 6),
                ("3FE77365BAAA", "POSITIVE POWER CABLE BLACK/10M", 2),
                ("3FE60713CAAA", "Simplex Patch Cord, SC/UPC - SC/APC 2m(brand: Nokia)", 32),
                ("L00YG16MM2", "WIRE GROUNDING CABLE YELLOW/GREEN 16MM N/A", 10),
                ("3FE77035BA", "Lightspan MF LT dmmy plte (388x204x25)mm", 1),
                ("Blaine-8\"Tie", "Plastic Cable Tie white", 1),
            ],
            1: [
                ("3FE53441AA", "PON Transceiver20km 1310nm(Tx)1490nm(Rx) - GPON SFP B+", 8),
                ("3FE47581AB", "Transcvr XGS-PON/GPON MPM B+(28dBm)Ctemp", 8),
                ("3FE76353AA", "Lightspan MF 16port Multi-PON Line board (LWLT-C)", 1),
                ("3FE60713CAAA", "Simplex Patch Cord, SC/UPC - SC/APC 2m(brand: Nokia)", 16),
                ("L00HLT_VELCRO_10M", "VELCRO (HOOK & LOOP TIE) BLACK 10m/roll", 1),
            ],
        }
    }
}


def get_reference(project_type: str, olt: str, cards: int):
    """Return the merged list of (part_no, description, qty_req)."""
    return REFERENCES.get(project_type, {}).get(olt, {}).get(cards, [])
