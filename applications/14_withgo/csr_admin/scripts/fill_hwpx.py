"""
fill_hwpx.py — 함께하는사랑밭 입사지원서(hwpx) 자동 채우기
Usage: python fill_hwpx.py
"""
import zipfile
import xml.etree.ElementTree as ET
import json
import os
import copy
from datetime import datetime, date

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..")
PROFILE_PATH = os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "content", "profile.json")
INPUT_HWPX = os.path.join(BASE_DIR, "artifacts", "(사)함께하는사랑밭_자사양식.hwpx")
OUTPUT_HWPX = os.path.join(BASE_DIR, "drafts", "application_form_v1.hwpx")
SIGNATURE_PATH = os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "common", "photos", "signature.png")

# ── HWPX Namespaces (must register before parsing to preserve prefixes) ──
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
    "epub": "http://www.idpf.org/2007/ops",
    "config": "urn:oasis:names:tc:opendocument:xmlns:config:1.0",
}

NS_P = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
NS_C = "{http://www.hancom.co.kr/hwpml/2011/core}"
NS_H = "{http://www.hancom.co.kr/hwpml/2011/head}"
NS_HC = "{http://www.hancom.co.kr/hwpml/2011/core}"


def add_left_align_style(docinfo_xml):
    """Add LEFT-aligned paraPr (id=45) to docInfo.xml, based on id=21."""
    root = ET.fromstring(docinfo_xml)
    # Find paraPrList
    parapr_list = root.find(f".//{NS_H}paraPrList")
    if parapr_list is None:
        return docinfo_xml  # fallback: no change

    # Find paraPr id="21" as template
    pr21 = None
    for pr in parapr_list.findall(f"{NS_H}paraPr"):
        if pr.get("id") == "21":
            pr21 = pr
            break
    if pr21 is None:
        return docinfo_xml

    # Deep copy and modify
    pr45 = copy.deepcopy(pr21)
    pr45.set("id", "45")

    # Change alignment: CENTER → LEFT
    align = pr45.find(f"{NS_H}align")
    if align is not None:
        align.set("horizontal", "LEFT")

    # Add left margin (400 HWPUNIT ≈ 1.4mm)
    margin = pr45.find(f"{NS_H}margin")
    if margin is not None:
        left_elem = margin.find(f"{NS_HC}left")
        if left_elem is not None:
            left_elem.set("value", "400")

    parapr_list.append(pr45)

    return ET.tostring(root, encoding="unicode")


def create_inline_pic(bin_item_id, display_w=2500, display_h=2500):
    """Create an inline <hp:pic> element for signature image."""
    w, h = str(display_w), str(display_h)
    hw, hh = str(display_w // 2), str(display_h // 2)

    pic = ET.Element(f"{NS_P}pic")
    for k, v in {"id": "0", "zOrder": "0", "numberingType": "PICTURE",
                 "textWrap": "TOP_AND_BOTTOM", "textFlow": "BOTH_SIDES",
                 "lock": "0", "dropcapstyle": "None", "href": "",
                 "groupLevel": "0", "instid": "0", "reverse": "0"}.items():
        pic.set(k, v)

    ET.SubElement(pic, f"{NS_P}offset", x="0", y="0")
    ET.SubElement(pic, f"{NS_P}orgSz", width=w, height=h)
    ET.SubElement(pic, f"{NS_P}curSz", width=w, height=h)
    ET.SubElement(pic, f"{NS_P}flip", horizontal="0", vertical="0")
    ET.SubElement(pic, f"{NS_P}rotationInfo",
                  angle="0", centerX=hw, centerY=hh, rotateimage="1")

    ri = ET.SubElement(pic, f"{NS_P}renderingInfo")
    identity = {"e1": "1", "e2": "0", "e3": "0", "e4": "0", "e5": "1", "e6": "0"}
    for tag in ["transMatrix", "scaMatrix", "rotMatrix"]:
        ET.SubElement(ri, f"{NS_C}{tag}", **identity)

    ir = ET.SubElement(pic, f"{NS_P}imgRect")
    for name, x, y in [("pt0", "0", "0"), ("pt1", w, "0"), ("pt2", w, h), ("pt3", "0", h)]:
        ET.SubElement(ir, f"{NS_C}{name}", x=x, y=y)

    ET.SubElement(pic, f"{NS_P}imgClip", left="0", right="0", top="0", bottom="0")
    ET.SubElement(pic, f"{NS_P}inMargin", left="0", right="0", top="0", bottom="0")
    ET.SubElement(pic, f"{NS_C}img", binaryItemIDRef=bin_item_id,
                  bright="0", contrast="0", effect="REAL_PIC", alpha="0")
    ET.SubElement(pic, f"{NS_P}effects")
    ET.SubElement(pic, f"{NS_P}sz", width=w, widthRelTo="ABSOLUTE",
                  height=h, heightRelTo="ABSOLUTE", protect="0")
    ET.SubElement(pic, f"{NS_P}pos", treatAsChar="1", affectLSpacing="0",
                  flowWithText="0", allowOverlap="0", holdAnchorAndSO="0",
                  vertRelTo="LINE", horzRelTo="COLUMN", vertAlign="BOTTOM",
                  horzAlign="LEFT", vertOffset="0", horzOffset="0")
    ET.SubElement(pic, f"{NS_P}outMargin", left="0", right="0", top="0", bottom="0")
    return pic


def fill_consent_and_signature(root):
    """Check 동의 checkbox (T12) and insert signature images."""
    tables = get_tables(root)

    # ── T12: 동의 체크박스 체크 ──
    rows12 = get_rows(tables[12])
    cells12 = get_cells(rows12[0])
    # [0,1] = 동의 checkbox → change to checked
    for run in cells12[1].iter(f"{NS_P}run"):
        run.set("charPrIDRef", "36")  # use normal text font
        for t in run.findall(f"{NS_P}t"):
            t.text = "■"

    # ── 서명 이미지 삽입 ──
    sig_pic_id = "image2"
    # Find all "(서명)" text and replace with signature image
    for t_elem in root.iter(f"{NS_P}t"):
        if t_elem.text and "(서명)" in t_elem.text:
            # Remove "(서명)" from text
            t_elem.text = t_elem.text.replace("(서명)", "").rstrip()
            # Find parent run → parent paragraph
            parent_run = None
            parent_p = None
            for p in root.iter(f"{NS_P}p"):
                for run in p.findall(f"{NS_P}run"):
                    for t in run.findall(f"{NS_P}t"):
                        if t is t_elem:
                            parent_run = run
                            parent_p = p
                            break
            # Also search inside table cells (subList → p → run)
            if parent_p is None:
                for sublist in root.iter(f"{NS_P}subList"):
                    for p in sublist.findall(f"{NS_P}p"):
                        for run in p.findall(f"{NS_P}run"):
                            for t in run.findall(f"{NS_P}t"):
                                if t is t_elem:
                                    parent_run = run
                                    parent_p = p
                                    break

            if parent_p is not None:
                # Create new run with signature pic
                sig_run = ET.SubElement(parent_p, f"{NS_P}run")
                sig_run.set("charPrIDRef", "21")
                sig_run.append(create_inline_pic(sig_pic_id))


def load_profile():
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def calc_age(birthdate_str):
    bd = datetime.strptime(birthdate_str, "%Y-%m-%d")
    today = date.today()
    return today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))


def get_tables(root):
    """Return list of all <hp:tbl> elements in document order."""
    return list(root.iter(f"{NS_P}tbl"))


def get_rows(tbl):
    """Return direct <hp:tr> children of a table."""
    return list(tbl.iter(f"{NS_P}tr"))


def get_cells(row):
    """Return direct <hp:tc> children of a row."""
    return list(row.iter(f"{NS_P}tc"))


def get_cell_text(cell):
    """Extract all text from a cell."""
    texts = []
    for t in cell.iter(f"{NS_P}t"):
        if t.text:
            texts.append(t.text)
    return "".join(texts).strip()


def set_cell_text(cell, value):
    """Set text in the first <hp:t> element of a cell.
    If cell has an empty <hp:t>, fill it. If no <hp:t>, create one in the first <hp:run>.
    """
    # Find first <hp:t> that is empty or the first one
    for t_elem in cell.iter(f"{NS_P}t"):
        if not t_elem.text or not t_elem.text.strip():
            t_elem.text = value
            return True
    # If all <hp:t> have text, try to find first run and add <hp:t>
    for run in cell.iter(f"{NS_P}run"):
        t_new = ET.SubElement(run, f"{NS_P}t")
        t_new.text = value
        return True
    return False


def set_cell_multiline(cell, text, para_pr_id="26", char_pr_id="3"):
    """Set multi-line text in a cell by creating separate <hp:p> for each line.
    Splits text by \\n and creates a paragraph for each line inside <hp:subList>.
    """
    sublist = cell.find(f"{NS_P}subList")
    if sublist is None:
        return False

    # Remove existing paragraphs
    for p in list(sublist.findall(f"{NS_P}p")):
        sublist.remove(p)

    lines = text.split("\n")
    for line in lines:
        p = ET.SubElement(sublist, f"{NS_P}p")
        p.set("id", "0")
        p.set("paraPrIDRef", str(para_pr_id))
        p.set("styleIDRef", "0")
        p.set("pageBreak", "0")
        p.set("columnBreak", "0")
        p.set("merged", "0")
        run = ET.SubElement(p, f"{NS_P}run")
        run.set("charPrIDRef", str(char_pr_id))
        t_elem = ET.SubElement(run, f"{NS_P}t")
        t_elem.text = line

    return True


def fill_table_cell(tables, table_idx, row_idx, col_idx, value):
    """Fill a specific cell by table/row/col index."""
    if not value:
        return
    tbl = tables[table_idx]
    rows = get_rows(tbl)
    if row_idx >= len(rows):
        return
    cells = get_cells(rows[row_idx])
    if col_idx >= len(cells):
        return
    set_cell_text(cells[col_idx], str(value))


def replace_cell_text(cell, old_text, new_text):
    """Replace text in a cell's <hp:t> elements."""
    for t_elem in cell.iter(f"{NS_P}t"):
        if t_elem.text and old_text in t_elem.text:
            t_elem.text = t_elem.text.replace(old_text, new_text)
            return True
    return False


def fill_application_form(root, profile):
    """Fill 입사지원서 (page 1) data."""
    tables = get_tables(root)
    pi = profile["personal_info"]
    mil = profile["military"]
    edu = profile["education"]
    exp = profile["experience"]
    certs = profile["certifications"]

    age = calc_age(pi["birthdate"])
    bd = pi["birthdate"].replace("-", ".")

    # ── Table 0: 지원분야 / 희망연봉 ──
    fill_table_cell(tables, 0, 0, 1, "행정·회계 및 사업관리 담당자")
    fill_table_cell(tables, 0, 0, 3, "회사 내규에 따름")

    # ── Table 1: 인적사항 ──
    # R0: 한글 이름, 생년월일(만 세)
    fill_table_cell(tables, 1, 0, 2, pi["name_ko"])
    # 생년월일 + 만 세 → cell[3] 라벨 유지, cell[4]에 날짜+나이
    rows1 = get_rows(tables[1])
    cells_r0 = get_cells(rows1[0])
    replace_cell_text(cells_r0[4], "(만  세)", f"{bd}  (만 {age}세)")

    # R1: 한자 + 성별
    cells_r1 = get_cells(rows1[1])
    fill_table_cell(tables, 1, 1, 1, "林 鐘 權")
    replace_cell_text(cells_r1[3], "□남     □여", "■남     □여")

    # R2: 영문
    fill_table_cell(tables, 1, 2, 1, pi["name_en"])

    # R3: 주소
    cells_r3 = get_cells(rows1[3])
    replace_cell_text(cells_r3[1], "(현주소)", pi["address"])

    # R4: 휴대폰, E-mail
    fill_table_cell(tables, 1, 4, 2, pi["phone"])
    fill_table_cell(tables, 1, 4, 4, pi["email"])

    # ── Table 2: 학력사항 (최종학력부터, R1~R4) ──
    edu_data = [
        # [기간(학교명), 전공, 입학연월, 졸업연월, 졸업구분, 학위]
        [f"{edu[0]['school']}", edu[0]["major"], edu[0]["period"].split(" ~ ")[0], edu[0]["period"].split(" ~ ")[1], "졸업", edu[0]["degree"]],
        [f"{edu[1]['school']}", "전기공학(복수:경제학)", edu[1]["period"].split(" ~ ")[0], edu[1]["period"].split(" ~ ")[1], "졸업", edu[1]["degree"]],
        [f"{edu[2]['school']}", "", edu[2]["period"].split(" ~ ")[0], edu[2]["period"].split(" ~ ")[1], "졸업", ""],
        ["폴리텍 광명교육원", edu[3].get("major", ""), "", edu[3].get("date", ""), edu[3]["degree"], ""],
    ]
    for ri, row_data in enumerate(edu_data):
        for ci, val in enumerate(row_data):
            if ci == 4:  # 졸업구분 → replace existing text
                rows2 = get_rows(tables[2])
                cells = get_cells(rows2[ri + 1])
                if ci < len(cells):
                    replace_cell_text(cells[ci], "졸업 / 재학 / 수료", val)
            else:
                fill_table_cell(tables, 2, ri + 1, ci, val)

    # ── Table 3: 경력사항 (R1~R3) ──
    exp_data = [
        ["2023.01 – 2026.02", exp[0]["company"], "대리", "총무·IT, 예산관리, ERP도입"],
        ["2020.03 – 2021.11", exp[1]["company"], "대리", "임베디드 개발, IoT, QA"],
        ["2016.05 – 2018.02", exp[2]["company"], "주임", "H/W개발, BOM관리"],
    ]
    for ri, row_data in enumerate(exp_data):
        for ci, val in enumerate(row_data):
            fill_table_cell(tables, 3, ri + 1, ci, val)

    # ── Table 4: 기타활동 — skip (leave empty) ──

    # ── Table 5: 자격사항 (R1~R2) ──
    cert_data = [
        [certs[0]["acquired"], certs[0]["name"], "", certs[0]["organization"]],
        [certs[1]["acquired"], certs[1]["name"], "", certs[1]["organization"]],
    ]
    for ri, row_data in enumerate(cert_data):
        for ci, val in enumerate(row_data):
            fill_table_cell(tables, 5, ri + 1, ci, val)

    # ── Table 6: 병역사항 ──
    rows6 = get_rows(tables[6])
    cells6 = get_cells(rows6[0])
    replace_cell_text(cells6[1], "□ 병역필  □ 미필  □ 해당없음", "■ 병역필  □ 미필  □ 해당없음")
    replace_cell_text(cells6[3], "0000.00.00-0000.00.00 (0년 0월)", "2010.07.28-2012.08.02 (2년 1월)")

    # ── Table 7: 어학/OA (R1~R3) ──
    oa_data = [
        ["", "", "", "MS Office", "상"],
        ["", "", "", "한글(HWP)", "상"],
        ["", "", "", "AI Tools", "상"],
    ]
    for ri, row_data in enumerate(oa_data):
        for ci, val in enumerate(row_data):
            if ci == 4:  # 능력 → replace
                rows7 = get_rows(tables[7])
                cells = get_cells(rows7[ri + 1])
                if ci < len(cells):
                    replace_cell_text(cells[ci], "상, 중, 하", val)
            elif val:
                fill_table_cell(tables, 7, ri + 1, ci, val)

    # ── Table 8: 교육훈련 (R1) ──
    fill_table_cell(tables, 8, 1, 0, "AR 시스템제어")
    fill_table_cell(tables, 8, 1, 1, "2022.06 ~ 2022.12")
    fill_table_cell(tables, 8, 1, 2, "Unity/C# AR 개발")
    fill_table_cell(tables, 8, 1, 3, "폴리텍 광명교육원")

    # ── 작성일 / 서명 (paragraph level, not table) ──
    # These are outside tables, find by text pattern
    for t_elem in root.iter(f"{NS_P}t"):
        if t_elem.text and "작성일 :" in t_elem.text and "년" in t_elem.text and "월" in t_elem.text:
            t_elem.text = "작성일 :  2026년  03월  05일"
        elif t_elem.text and "지원자 :" in t_elem.text and "(서명)" in t_elem.text:
            t_elem.text = f"지원자 :   {pi['name_ko']}     (서명)"

    # ── Table 9: 자기소개서 (R1,R3,R5,R7 = answer cells) ──
    essays = [
        # 1. 지원동기
        "비영리 법인 (사)함께만드는세상에서 3년간 연간 약 3.6억 원 규모의 인프라 예산을 "
        "직접 집행·통제하며 집행률 88.5%를 달성했습니다. 외주업체 8개의 계약·정산을 총괄하고, "
        "증빙 관리와 지출 내역 정리를 일상 업무로 수행했습니다.\n"
        "에너지플러스 사업의 행정·회계 업무(예산 관리, 증빙 정리, 정산 취합, 행정 보고)가 "
        "제가 3년간 해온 업무와 정확히 일치하여 지원합니다.",

        # 2. 설립이념 + 가치관
        "'가장 효과적이고 효율적인 방법으로 돕는다'는 설립이념에 공감합니다. "
        "비영리 현장에서 3년간 일하며, 선한 의도만으로는 사업이 지속될 수 없고 "
        "체계적인 행정과 투명한 회계가 뒷받침되어야 한다는 것을 체감했습니다.\n"
        "이를 실천하여 재계약 협상으로 연 약 500만 원을 절감하고, "
        "네트워크·PC 트러블슈팅 내재화로 유지보수 비용을 30% 줄였습니다. "
        "행정·회계 담당자로서 사랑밭의 사업이 시민에게 닿는 인프라 역할을 맡겠습니다.",

        # 3. 전문성 + 차별화
        "세 가지 축으로 전문성을 쌓아왔습니다.\n"
        "첫째, 예산 관리. 3.6억 원 편성·집행·결산을 직접 수행하며 불용액을 최소화했습니다.\n"
        "둘째, 시스템 구축. ERP 도입 프로젝트를 18개월간 전담하며 "
        "회계 프로세스 설계부터 계정과목 표준화, 최종 검수까지 풀사이클을 수행했습니다.\n"
        "셋째, 자격과 도구. 사회복지사 1급으로 비영리 사업 구조를 이해하고, "
        "AI 도구를 활용하여 반복 행정의 효율을 높이고 있습니다.",

        # 4. 힘든 상황
        "ERP 도입 프로젝트가 가장 힘들었습니다. 18개월간 기존 업무를 병행하면서 "
        "부서마다 업무 방식이 달라 요구사항이 충돌하는 상황이 반복되었습니다.\n"
        "각 부서 실무자를 직접 인터뷰하여 업무 프로세스를 문서화하고, "
        "공통 영역(계정과목, 결재선)을 먼저 표준화하여 합의점을 만들었습니다. "
        "'시스템은 현장 실무자의 목소리에서 출발해야 정착된다'는 점을 배웠습니다.",
    ]
    answer_rows = [1, 3, 5, 7]
    for i, ri in enumerate(answer_rows):
        rows9 = get_rows(tables[9])
        cells = get_cells(rows9[ri])
        set_cell_multiline(cells[0], essays[i])

    # ── 개인정보동의서 서명일/성명 ──
    for t_elem in root.iter(f"{NS_P}t"):
        if t_elem.text and "년     월       일" in t_elem.text:
            t_elem.text = "2026년   03월      05일"
        elif t_elem.text and "성 명 :" in t_elem.text and "(서명)" in t_elem.text:
            t_elem.text = f"성 명 :    {pi['name_ko']}      (서명)"


def set_paragraph_text(para, text, char_pr_id="21"):
    """Set text in a paragraph by modifying its first run or creating one."""
    NS = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"
    run = para.find(f"{NS}run")
    if run is not None:
        # Update charPrIDRef
        run.set("charPrIDRef", str(char_pr_id))
        # Find or create <hp:t>
        t_elem = run.find(f"{NS}t")
        if t_elem is None:
            t_elem = ET.SubElement(run, f"{NS}t")
        t_elem.text = text
    else:
        # Create new run + t
        run = ET.SubElement(para, f"{NS}run")
        run.set("charPrIDRef", str(char_pr_id))
        t_elem = ET.SubElement(run, f"{NS}t")
        t_elem.text = text


def create_career_table(root):
    """Create career description table by cloning Table 3 structure."""
    tables = get_tables(root)
    t3 = tables[3]  # 경력사항 table (4col x 4row)

    # Deep copy Table 3 as template
    career_tbl = copy.deepcopy(t3)

    # Update table attributes
    career_tbl.set("rowCnt", "4")  # header + 3 companies

    # Career data: [기간, 회사명(부서), 직위, 주요 업무 및 성과 (multiline)]
    header = ["근무기간", "회사명 (부서)", "직위", "주요 업무 및 성과"]

    career_data = [
        {
            "period": "2023.01\n~\n2026.02",
            "company": "(사)함께만드는세상\n(경영지원부)",
            "position": "대리",
            "duties": [
                "■ 인프라 예산 약 3.6억 원 집행·통제 (집행률 88.5%)",
                "  - 지출내역 정리·증빙관리·정산보고서 작성",
                "■ 커스텀 ERP 도입 PM (Tibero/Nexacro)",
                "  - 공익법인 회계 계정과목 표준화·프로세스 설계",
                "■ 외주 8개 업체 계약·정산 총괄 (연 500만 원 절감)",
                "■ IT자산 대장관리·유휴장비 재배치 (중복투자 방지)",
                "■ 총무 행정 전반 (비품·문서관리·행사지원)",
            ],
        },
        {
            "period": "2020.03\n~\n2021.11",
            "company": "(주)맨지온\n(개발부)",
            "position": "대리",
            "duties": [
                "■ ESP32 기반 해수담수화 임베디드 시스템 개발 (C/C++)",
                "■ Blynk 연동 IoT 센서 모니터링 대시보드 구축",
                "■ 사용자 관점 UI/UX 테스트 시나리오 설계 및 QA",
                "■ 기술 문서화 및 프로토타입 시연",
            ],
        },
        {
            "period": "2016.05\n~\n2018.02",
            "company": "주식회사 엣지크로스\n(기술연구소)",
            "position": "주임",
            "duties": [
                "■ H/W 개발 풀사이클 (회로설계→PCB→시제품→검증)",
                "■ 자재명세서(BOM) 관리 체계화, 납기 준수율 100%",
                "■ 부품 수급 관리 및 협력업체 조율",
            ],
        },
    ]

    # --- Column width redistribution ---
    COL_WIDTHS = [7500, 9500, 4500, 26121]  # total = 47621
    rows = list(career_tbl.findall(f"{NS_P}tr"))
    for row in rows:
        cells = list(row.findall(f"{NS_P}tc"))
        for ci, cell in enumerate(cells):
            cellsz = cell.find(f"{NS_P}cellSz")
            if cellsz is not None:
                cellsz.set("width", str(COL_WIDTHS[ci]))

    # Fill header row
    header_cells = list(rows[0].findall(f"{NS_P}tc"))
    for ci, text in enumerate(header):
        _clear_and_set_cell(header_cells[ci], text)

    # Fill data rows
    for ri, data in enumerate(career_data):
        data_cells = list(rows[ri + 1].findall(f"{NS_P}tc"))
        _clear_and_set_cell(data_cells[0], data["period"])
        _clear_and_set_cell(data_cells[1], data["company"])
        _clear_and_set_cell(data_cells[2], data["position"])
        # 담당업무: multi-line, LEFT-aligned (paraPrIDRef=45)
        _clear_and_set_cell_multiline(data_cells[3], data["duties"], para_pr_override="45")

    return career_tbl


def _clear_and_set_cell(cell, text):
    """Clear existing cell text and set new text (supports \\n for multi-paragraph)."""
    sublist = cell.find(f"{NS_P}subList")
    if sublist is None:
        return
    # Get style from existing paragraph
    existing_p = sublist.find(f"{NS_P}p")
    para_pr = existing_p.get("paraPrIDRef", "21") if existing_p is not None else "21"
    existing_run = existing_p.find(f"{NS_P}run") if existing_p is not None else None
    char_pr = existing_run.get("charPrIDRef", "28") if existing_run is not None else "28"

    # Remove all existing paragraphs
    for p in list(sublist.findall(f"{NS_P}p")):
        sublist.remove(p)

    lines = text.split("\n")
    for line in lines:
        p = ET.SubElement(sublist, f"{NS_P}p")
        p.set("id", "0")
        p.set("paraPrIDRef", para_pr)
        p.set("styleIDRef", "0")
        p.set("pageBreak", "0")
        p.set("columnBreak", "0")
        p.set("merged", "0")
        run = ET.SubElement(p, f"{NS_P}run")
        run.set("charPrIDRef", char_pr)
        t_elem = ET.SubElement(run, f"{NS_P}t")
        t_elem.text = line


def _clear_and_set_cell_multiline(cell, lines, para_pr_override=None):
    """Set multi-line content in a cell from a list of strings."""
    sublist = cell.find(f"{NS_P}subList")
    if sublist is None:
        return
    existing_p = sublist.find(f"{NS_P}p")
    para_pr = para_pr_override or (existing_p.get("paraPrIDRef", "21") if existing_p is not None else "21")
    existing_run = existing_p.find(f"{NS_P}run") if existing_p is not None else None
    char_pr = existing_run.get("charPrIDRef", "28") if existing_run is not None else "28"

    for p in list(sublist.findall(f"{NS_P}p")):
        sublist.remove(p)

    for line in lines:
        p = ET.SubElement(sublist, f"{NS_P}p")
        p.set("id", "0")
        p.set("paraPrIDRef", para_pr)
        p.set("styleIDRef", "0")
        p.set("pageBreak", "0")
        p.set("columnBreak", "0")
        p.set("merged", "0")
        run = ET.SubElement(p, f"{NS_P}run")
        run.set("charPrIDRef", char_pr)
        t_elem = ET.SubElement(run, f"{NS_P}t")
        t_elem.text = line


def fill_career_description(root):
    """Fill 경력기술서 (page 3) with a table cloned from Table 3."""
    all_children = list(root)

    # Create the career table
    career_tbl = create_career_table(root)

    # Insert table into paragraph 40 (first empty career desc paragraph)
    p40 = all_children[40]
    # Find or create a <hp:run> in p40
    run = p40.find(f"{NS_P}run")
    if run is None:
        run = ET.SubElement(p40, f"{NS_P}run")
        run.set("charPrIDRef", "21")
    # Insert table into run
    run.append(career_tbl)

    # Completely remove empty paragraphs (41~66) to avoid blank pages
    for idx in range(66, 40, -1):  # reverse order to avoid index shift
        if idx < len(all_children):
            root.remove(all_children[idx])

    # Force page break before 개인정보동의서 (now at new index 41)
    new_children = list(root)
    if len(new_children) > 41:
        new_children[41].set("pageBreak", "1")


def fill_hwpx_template(input_path, output_path, profile):
    """Main function: open hwpx, modify section0.xml, write new hwpx."""
    # Register namespaces to preserve prefixes
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    # Read original ZIP
    with zipfile.ZipFile(input_path, "r") as zin:
        section_xml = zin.read("Contents/section0.xml").decode("utf-8")
        header_xml = zin.read("Contents/header.xml").decode("utf-8")

        # Parse XML
        root = ET.fromstring(section_xml)

        # Fill data
        fill_application_form(root, profile)
        fill_consent_and_signature(root)
        fill_career_description(root)

        # Serialize modified section XML
        modified_xml = ET.tostring(root, encoding="unicode", xml_declaration=False)
        modified_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>' + modified_xml

        # Add LEFT-aligned paraPr style to header.xml
        modified_header = add_left_align_style(header_xml)
        modified_header_bytes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'
                                 + modified_header).encode("utf-8") \
            if not modified_header.startswith("<?xml") else modified_header.encode("utf-8")

        # Read and patch content.hpf (add signature image manifest entry)
        hpf_xml = zin.read("Contents/content.hpf").decode("utf-8")
        if "image2" not in hpf_xml:
            hpf_xml = hpf_xml.replace(
                '</opf:manifest>',
                '<opf:item id="image2" href="BinData/image2.png" '
                'media-type="image/png" isEmbeded="1"/></opf:manifest>'
            )

        # Read signature image
        with open(SIGNATURE_PATH, "rb") as f:
            sig_bytes = f.read()

        # Write new hwpx
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "Contents/section0.xml":
                    zout.writestr(item, modified_xml.encode("utf-8"))
                elif item.filename == "Contents/header.xml":
                    zout.writestr(item, modified_header_bytes)
                elif item.filename == "Contents/content.hpf":
                    zout.writestr(item, hpf_xml.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))
            # Add signature image
            zout.writestr("BinData/image2.png", sig_bytes)

    print(f"✅ 생성 완료: {output_path}")


if __name__ == "__main__":
    profile = load_profile()
    fill_hwpx_template(INPUT_HWPX, OUTPUT_HWPX, profile)

    # Quick verification: extract text from output
    print("\n── 검증: 생성된 파일 텍스트 추출 ──")
    with zipfile.ZipFile(OUTPUT_HWPX, "r") as z:
        content = z.read("Contents/section0.xml").decode("utf-8")
        root = ET.fromstring(content)
        for t in root.iter(f"{NS_P}t"):
            if t.text and t.text.strip():
                text = t.text.strip()
                # Only show filled-in data (not labels)
                if any(kw in text for kw in ["임종권", "광명", "010-", "ssujklim", "숭실", "함께만드는",
                                               "맨지온", "엣지크로스", "사회복지사", "병역필", "작성일",
                                               "작성 예정", "폴리텍", "MS Office", "2026"]):
                    print(f"  → {text[:80]}")
