"""
fill_interview_forms_batch.py — 경기도 청년 면접수당 면접확인서(hwpx) 일괄 생성
#19 서울사회적경제센터 artifacts 확인서를 레퍼런스로 사용
"""
import zipfile
import xml.etree.ElementTree as ET
import os

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..")

# 유저가 직접 수정한 #19 면접확인서를 원본으로 사용
REFERENCE_HWPX = os.path.join(BASE_DIR, "applications", "19_seoul_se_center",
                               "se_manager", "artifacts",
                               "면접확인서_서울사회적경제센터_260324.hwpx")

# ── HWPX Namespaces ──
NAMESPACES = {
    "ha": "http://www.hancom.co.kr/hwpml/2011/app",
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hp10": "http://www.hancom.co.kr/hwpml/2016/paragraph",
    "hs": "http://www.hancom.co.kr/hwpml/2011/section",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hhs": "http://www.hancom.co.kr/hwpml/2011/history",
    "hm": "http://www.hancom.co.kr/hwpml/2011/master-page",
    "hpf": "http://www.hancom.co.kr/schema/2011/hpf",
    "dc": "http://purl.org/dc/elements/1.1/",
    "opf": "http://www.idpf.org/2007/opf/",
    "ooxmlchart": "http://www.hancom.co.kr/hwpml/2016/ooxmlchart",
    "hwpunitchar": "http://www.hancom.co.kr/hwpml/2016/HwpUnitChar",
    "epub": "http://www.idpf.org/2007/ops",
    "config": "urn:oasis:names:tc:opendocument:xmlns:config:1.0",
}
NS_P = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"

# ── Interview data ──
INTERVIEWS = [
    {
        "id": "08",
        "month": "2",
        "day": "20",
        "company": "화영운수(주)",
        "phone": "",
        "address": "경기도 광명시 도덕로 13",
        "output": os.path.join(BASE_DIR, "applications", "08_hwayoungunsu",
                               "bus_dispatch_admin", "final",
                               "면접확인서_화영운수_260220.hwpx"),
    },
    {
        "id": "09",
        "month": "3",
        "day": "10",
        "company": "주식회사 네오플",
        "phone": "",
        "address": "제주특별자치도 제주시 1100로 3198-13 네오마루",
        "output": os.path.join(BASE_DIR, "applications", "09_neople",
                               "budget_management", "final",
                               "면접확인서_네오플_260310.hwpx"),
    },
    {
        "id": "16",
        "month": "3",
        "day": "12",
        "company": "(주)아이위더스",
        "phone": "",
        "address": "",
        "output": os.path.join(BASE_DIR, "applications", "16_ecredible",
                               "tcb_report", "final",
                               "면접확인서_아이위더스_260312.hwpx"),
    },
]


def register_namespaces():
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)


def set_cell_text(cell, value):
    """Set text of first run's <hp:t> in a cell, clear extra paragraphs."""
    # Paragraphs live inside <hp:subList> (not direct children of <hp:tc>)
    sublist = cell.find(f"{NS_P}subList")
    if sublist is not None:
        paras = list(sublist.findall(f"{NS_P}p"))
    else:
        paras = list(cell.iter(f"{NS_P}p"))
    if not paras:
        return
    p = paras[0]
    runs = list(p.findall(f"{NS_P}run"))
    if runs:
        t = runs[0].find(f"{NS_P}t")
        if t is None:
            t = ET.SubElement(runs[0], f"{NS_P}t")
        t.text = value
        for r in runs[1:]:
            p.remove(r)
    else:
        run = ET.SubElement(p, f"{NS_P}run")
        t = ET.SubElement(run, f"{NS_P}t")
        t.text = value
    # Remove extra paragraphs (e.g. company name split across 2 lines)
    parent = sublist if sublist is not None else cell
    for extra_p in paras[1:]:
        parent.remove(extra_p)


def fill_form(xml_content, data):
    """Fill form fields matching the user's #19 reference pattern."""
    root = ET.fromstring(xml_content)
    tables = list(root.iter(f"{NS_P}tbl"))

    # Table 2 R0: 성명 (cells[1]), 생년월일 (cells[3]) — already filled, keep as-is

    # Table 3 R0: date — user format: "3월" "24일" → change to new month/day
    tbl3 = tables[3]
    rows3 = list(tbl3.findall(f".//{NS_P}tr"))
    if rows3:
        cells = list(rows3[0].findall(f"{NS_P}tc"))
        if len(cells) >= 2:
            set_cell_text(cells[0], f"{data['month']}월")
            set_cell_text(cells[1], f"{data['day']}일")

    # Table 5: company info
    tbl5 = tables[5]
    rows5 = list(tbl5.findall(f".//{NS_P}tr"))
    if len(rows5) >= 2:
        cells0 = list(rows5[0].findall(f"{NS_P}tc"))
        if len(cells0) >= 4:
            set_cell_text(cells0[1], data["company"])
            set_cell_text(cells0[3], data["phone"])
        cells1 = list(rows5[1].findall(f"{NS_P}tc"))
        if len(cells1) >= 2:
            set_cell_text(cells1[1], data["address"])

    # Fix date runs: "2026년" patterns — find and update month/day
    all_runs = list(root.iter(f"{NS_P}run"))
    for i, run in enumerate(all_runs):
        t = run.find(f"{NS_P}t")
        if t is None or not t.text:
            continue
        txt = t.text.strip()

        # Pattern 1: " (실제면접일)" → keep as-is
        # Pattern 2: "3월" standalone run → update
        if txt == "3월":
            t.text = f"{data['month']}월"
        elif txt == "24일":
            t.text = f"{data['day']}일"
        # Pattern 3: "2026년    3 월   24  일" combined → update
        elif "2026년" in txt and "월" in txt and "일" in txt:
            t.text = f"2026년    {data['month']} 월   {data['day']}  일"
        # Pattern 4: standalone "3" after "2026년" run
        elif txt == "3" and i > 0:
            prev_t = all_runs[i - 1].find(f"{NS_P}t")
            if prev_t is not None and prev_t.text and "2026년" in prev_t.text:
                t.text = data["month"]
        elif txt == "24" and i > 0:
            prev_t = all_runs[i - 2].find(f"{NS_P}t") if i >= 2 else None
            if prev_t is not None and prev_t.text and "월" in prev_t.text:
                t.text = data["day"]

    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def generate_one(data):
    """Generate one interview confirmation form from reference."""
    output_path = data["output"]
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Read section0.xml from the reference hwpx directly
    with zipfile.ZipFile(REFERENCE_HWPX, "r") as z:
        section0 = z.read("Contents/section0.xml").decode("utf-8")

    modified = fill_form(section0, data)

    # Build output hwpx from reference, replacing section0.xml
    # If output exists and is locked, delete .tmp leftover and write fresh
    tmp_path = output_path + ".tmp"
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    with zipfile.ZipFile(REFERENCE_HWPX, "r") as zin:
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "Contents/section0.xml":
                    zout.writestr(item, modified.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))

    try:
        os.replace(tmp_path, output_path)
    except PermissionError:
        # Original file locked — keep as .tmp and notify
        print(f"  ⚠ {os.path.basename(output_path)} locked, saved as .tmp")
        return
    print(f"  ✓ {os.path.basename(output_path)}")


def main():
    register_namespaces()
    print(f"Reference: {os.path.basename(REFERENCE_HWPX)}\n")

    for data in INTERVIEWS:
        print(f"[{data['id']}] {data['company']} — {data['month']}월 {data['day']}일")
        generate_one(data)

    print(f"\nDone! Generated {len(INTERVIEWS)} forms.")


if __name__ == "__main__":
    main()
