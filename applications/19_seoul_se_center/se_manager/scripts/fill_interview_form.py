"""
fill_interview_form.py — 경기도 청년 면접수당 면접확인서(hwpx) 자동 채우기
서울특별시 사회적경제지원센터 면접 (2026-03-24)
"""
import zipfile
import xml.etree.ElementTree as ET
import os
import shutil

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..")
INPUT_HWPX = os.path.join(BASE_DIR, "..", "..", "..", "templates", "forms",
                          "(작성서식)+면접확인서_+대체서약서_v20260121.hwpx")
OUTPUT_HWPX = os.path.join(BASE_DIR, "artifacts", "면접확인서_서울사회적경제센터_260324.hwpx")

# ── Data to fill ──
DATA = {
    "name": "임종권",
    "birth": "1992.01.04",
    "interview_month": "3",
    "interview_day": "24",
    "company": "서울특별시 사회적경제지원센터",
    "phone": "02-2088-6386",
    "address": "서울특별시 구로구 개봉로23길 10, 5층",
}

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


def register_namespaces():
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)


def get_cell_text(cell):
    """Get concatenated text from all runs in a cell."""
    texts = []
    for t in cell.iter(f"{NS_P}t"):
        if t.text:
            texts.append(t.text.strip())
    return " ".join(texts)


def set_cell_text(cell, value):
    """Set text of first run's <hp:t> in a cell. Create if needed."""
    # Find first paragraph
    paras = list(cell.iter(f"{NS_P}p"))
    if not paras:
        return False

    p = paras[0]
    runs = list(p.findall(f"{NS_P}run"))

    if runs:
        # Use first run, set its <hp:t>
        t = runs[0].find(f"{NS_P}t")
        if t is None:
            t = ET.SubElement(runs[0], f"{NS_P}t")
        t.text = value
        # Remove extra runs (clean up)
        for extra_run in runs[1:]:
            p.remove(extra_run)
    else:
        # Create a new run with <hp:t>
        run = ET.SubElement(p, f"{NS_P}run")
        t = ET.SubElement(run, f"{NS_P}t")
        t.text = value

    return True


def fill_section0(xml_content):
    """Fill in form fields in section0.xml."""
    root = ET.fromstring(xml_content)
    tables = list(root.iter(f"{NS_P}tbl"))

    # ── Table 2: 면접응시자 정보 ──
    # Row 0: ['성   명', (empty), '생년월일', (empty)]
    tbl2 = tables[2]
    rows2 = list(tbl2.findall(f".//{NS_P}tr"))
    if rows2:
        cells = list(rows2[0].findall(f"{NS_P}tc"))
        if len(cells) >= 4:
            # Cell 1: 성명 value
            set_cell_text(cells[1], DATA["name"])
            print(f"  성명: {DATA['name']}")
            # Cell 3: 생년월일 value
            set_cell_text(cells[3], DATA["birth"])
            print(f"  생년월일: {DATA['birth']}")

    # ── Date fields (면접일): runs with "2026년" ... "월" ... "일" ──
    # Find all runs globally, modify the space before "월" and empty before "일"
    all_runs = list(root.iter(f"{NS_P}run"))
    date_filled = 0
    for i, run in enumerate(all_runs):
        t = run.find(f"{NS_P}t")
        if t is None or not t.text:
            continue
        if t.text.strip() == "2026년" and date_filled < 2:
            # Next run should be space (month value), then "월", then empty (day), then "일"
            if i + 4 < len(all_runs):
                # Run i+1: month value (currently " ")
                t_month = all_runs[i + 1].find(f"{NS_P}t")
                if t_month is None:
                    t_month = ET.SubElement(all_runs[i + 1], f"{NS_P}t")
                t_month.text = DATA["interview_month"]

                # Run i+2 should be "월", Run i+3 should be empty (day value)
                t_day = all_runs[i + 3].find(f"{NS_P}t")
                if t_day is None:
                    t_day = ET.SubElement(all_runs[i + 3], f"{NS_P}t")
                t_day.text = DATA["interview_day"]

                date_filled += 1
                print(f"  면접일 #{date_filled}: {DATA['interview_month']}월 {DATA['interview_day']}일")

    # ── Table 5: 면접시행 회사 정보 ──
    # Row 0: ['회 사 명', (empty), '(내선)', (empty)]
    # Row 1: ['주     소', (empty)]
    # Row 2: ['면접확인서 작 성 자', ...] — leave as is
    tbl5 = tables[5]
    rows5 = list(tbl5.findall(f".//{NS_P}tr"))
    if len(rows5) >= 2:
        # Row 0: company name + phone
        cells0 = list(rows5[0].findall(f"{NS_P}tc"))
        if len(cells0) >= 4:
            set_cell_text(cells0[1], DATA["company"])
            print(f"  회사명: {DATA['company']}")
            set_cell_text(cells0[3], DATA["phone"])
            print(f"  전화번호: {DATA['phone']}")

        # Row 1: address
        cells1 = list(rows5[1].findall(f"{NS_P}tc"))
        if len(cells1) >= 2:
            set_cell_text(cells1[1], DATA["address"])
            print(f"  주소: {DATA['address']}")

    return ET.tostring(root, encoding="unicode", xml_declaration=True)


def main():
    register_namespaces()

    print(f"Input:  {INPUT_HWPX}")
    print(f"Output: {OUTPUT_HWPX}")

    # Copy hwpx and modify section0.xml inside
    shutil.copy2(INPUT_HWPX, OUTPUT_HWPX)

    # Read section0.xml from the copy
    with zipfile.ZipFile(OUTPUT_HWPX, "r") as zin:
        section0 = zin.read("Contents/section0.xml").decode("utf-8")

    # Fill in fields
    print("\nFilling fields...")
    modified = fill_section0(section0)

    # Write back: rebuild ZIP with modified section0.xml
    import tempfile
    tmp_path = OUTPUT_HWPX + ".tmp"

    with zipfile.ZipFile(OUTPUT_HWPX, "r") as zin:
        with zipfile.ZipFile(tmp_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "Contents/section0.xml":
                    zout.writestr(item, modified.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))

    # Replace original with modified
    os.replace(tmp_path, OUTPUT_HWPX)
    print(f"\nDone! → {OUTPUT_HWPX}")


if __name__ == "__main__":
    main()
