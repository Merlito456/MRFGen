# references.py
# ==========================================================
# MATERIAL REQUEST REFERENCES
# Project Type : New Build
# OLT          : MF-02
# # of Cards   : 2 / 1
# ==========================================================
# Tuple format: (part_no, description, qty_req, unit, note)
# ==========================================================

REFERENCES = {
    "New Build": {
        "MF-02": {
            # ==================================================
            # 2 LT CARDS (matches sample: NOKIA-FN_07032026-001)
            # Dummy plate (3FE77035BA) EXCLUDED — 1-card sites only
            # ==================================================
            2: [
                # ---------- EQUIPMENT PARTS ----------
                ("3FE76762AA", "Lightspan MF-2 shelf incl. fan unit (LMXR-A)", 1, "pc", ""),
                ("3FE76518AA", "MF2-FAN Module", 1, "pc", ""),
                ("3FE76559BA", "Lightspan MF-2 DC power module (LPWR-B DC)", 2, "pcs", ""),
                ("3FE62600AA", "Optical Transceiver SFP+,1310nm SM,10km(brand: Nokia) (10GBase-LR)", 2, "pcs", ""),
                ("3FE53441AA", "PON Transceiver20km 1310nm(Tx)1490nm(Rx) - GPON SFP B+", 16, "pcs", "16 if two LT cards"),
                ("3FE47581AB", "Transcvr XGS-PON/GPON MPM B+(28dBm)Ctemp", 16, "pcs", "16 if two LT cards"),
                ("3FE76476AA", "LightspanMF-2 240Gbps NT with clock sync(brand: Nokia) (LMNT-A)", 2, "pcs", ""),
                ("3FE76353AA", "Lightspan MF 16port Multi-PON Line board (LWLT-C)", 2, "pcs", "2 for two LT cards"),

                # ---------- LOCAL MATERIALS / ACCESSORIES ----------
                ("3FE52344FLAA", "Simplex patch cord, LC/UPC - LC/UPC 8m(brand: Nokia)", 2, "pcs", ""),
                ("Blaine-Spiral-1/2mmx10ft", "Spiral Wrap 10mmx10ft", 1, "pc", ""),
                ("L00HLT_VELCRO_10M", "VELCRO (HOOK & LOOP TIE) BLACK 10m/roll", 1, "pc", ""),
                ("Blaine-16mm-Shrinkable", "Shrinkable tube 16mm x 200mm", 2, "pcs", ""),
                ("Blaine-8mmShrinkable", "Shrinkable tube 8mm x 200mm", 2, "pcs", ""),
                ("Blaine-12mmShrinkable", "Shrinkable tube 12mm x 200mm", 2, "pcs", ""),
                ("Blaine-Cartridge9mm", "Labeller tape", 1, "pc", ""),
                ("L00TL14AWG", "cable shoe (#14 AWG)", 4, "pcs", ""),
                ("L00Lugs10mm2", "10mm2 Terminal Lugs", 6, "pcs", ""),
                ("L00Lugs16mm2", "16-10mm2 Terminal Lugs", 2, "pcs", ""),
                ("L00Lugs8mm2", "terminal lugs 8mm", 6, "pcs", ""),
                ("3FE77365BAAA", "POSITIVE POWER CABLE BLACK/10M", 2, "pcs", "for power cable"),
                ("3FE60713CAAA", "Simplex Patch Cord, SC/UPC - SC/APC 2m(brand: Nokia)", 32, "pcs", "32 for 2 LT Cards"),
                ("L00YG16MM2", "WIRE GROUNDING CABLE YELLOW/GREEN 16MM N/A", 10, "m", ""),
                ("Blaine-8\"Tie", "Plastic Cable Tie white", 1, "pcs", ""),
                # ⛔ 3FE77035BA (dummy plate) REMOVED — only for 1-LT-card sites
            ],

            # ==================================================
            # 1 LT CARD (scaled down; dummy plate INCLUDED)
            # ==================================================
            1: [
                ("3FE76762AA", "Lightspan MF-2 shelf incl. fan unit (LMXR-A)", 1, "pc", ""),
                ("3FE76518AA", "MF2-FAN Module", 1, "pc", ""),
                ("3FE76559BA", "Lightspan MF-2 DC power module (LPWR-B DC)", 1, "pc", ""),
                ("3FE62600AA", "Optical Transceiver SFP+,1310nm SM,10km(brand: Nokia) (10GBase-LR)", 1, "pc", ""),
                ("3FE53441AA", "PON Transceiver20km 1310nm(Tx)1490nm(Rx) - GPON SFP B+", 8, "pcs", ""),
                ("3FE47581AB", "Transcvr XGS-PON/GPON MPM B+(28dBm)Ctemp", 8, "pcs", ""),
                ("3FE76476AA", "LightspanMF-2 240Gbps NT with clock sync(brand: Nokia) (LMNT-A)", 1, "pc", ""),
                ("3FE76353AA", "Lightspan MF 16port Multi-PON Line board (LWLT-C)", 1, "pc", ""),

                ("3FE52344FLAA", "Simplex patch cord, LC/UPC - LC/UPC 8m(brand: Nokia)", 2, "pcs", ""),
                ("Blaine-Spiral-1/2mmx10ft", "Spiral Wrap 10mmx10ft", 1, "pc", ""),
                ("L00HLT_VELCRO_10M", "VELCRO (HOOK & LOOP TIE) BLACK 10m/roll", 1, "pc", ""),
                ("Blaine-16mm-Shrinkable", "Shrinkable tube 16mm x 200mm", 2, "pcs", ""),
                ("Blaine-8mmShrinkable", "Shrinkable tube 8mm x 200mm", 2, "pcs", ""),
                ("Blaine-12mmShrinkable", "Shrinkable tube 12mm x 200mm", 2, "pcs", ""),
                ("Blaine-Cartridge9mm", "Labeller tape", 1, "pc", ""),
                ("L00TL14AWG", "cable shoe (#14 AWG)", 4, "pcs", ""),
                ("L00Lugs10mm2", "10mm2 Terminal Lugs", 6, "pcs", ""),
                ("L00Lugs16mm2", "16-10mm2 Terminal Lugs", 2, "pcs", ""),
                ("L00Lugs8mm2", "terminal lugs 8mm", 6, "pcs", ""),
                ("3FE77365BAAA", "POSITIVE POWER CABLE BLACK/10M", 1, "pc", "for power cable"),
                ("3FE60713CAAA", "Simplex Patch Cord, SC/UPC - SC/APC 2m(brand: Nokia)", 16, "pcs", "16 for 1 LT Card"),
                ("L00YG16MM2", "WIRE GROUNDING CABLE YELLOW/GREEN 16MM N/A", 10, "m", ""),
                ("3FE77035BA", "Lightspan MF LT dmmy plte (388x204x25)mm", 1, "pcs", "for sites with 1 LT card only"),
                ("Blaine-8\"Tie", "Plastic Cable Tie white", 1, "pcs", ""),
            ],
        }
    }
}


def get_reference(project_type: str, olt: str, cards: int):
    """Return merged list of (part_no, description, qty_req, unit, note)."""
    ref = REFERENCES.get(project_type, {}).get(olt, {}).get(cards, [])
    # Normalize tuples (allow legacy 4-tuple) → always 5-tuple
    normalized = []
    for row in ref:
        if len(row) == 5:
            normalized.append(row)
        elif len(row) == 4:
            normalized.append((*row, ""))
        else:
            raise ValueError(f"Unexpected reference tuple length: {row}")
    return normalized
