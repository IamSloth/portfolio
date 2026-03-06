"""
fill_hwpx.py — 한국사회복지사협회 자격관리본부 이력서+자기소개서+동의서 자동 채우기
Usage: python fill_hwpx.py
"""
import zipfile
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime, date

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..")
PROFILE_PATH = os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "content", "profile.json")
INPUT_HWPX = os.path.join(
    BASE_DIR, "artifacts",
    "붙임2. 이력서 및 자기소개서, 개인정보수입이용동의서(자격관리본부 단기계약직).hwpx"
)
OUTPUT_HWPX = os.path.join(BASE_DIR, "drafts", "application_form_v1.hwpx")

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
    "epub": "http://www.idpf.org/2007/ops",
    "config": "urn:oasis:names:tc:opendocument:xmlns:config:1.0",
}

NS_P = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"


def load_profile():
    with open(PROFILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_tables(root):
    return list(root.iter(f"{NS_P}tbl"))


def get_rows(tbl):
    return list(tbl.findall(f"{NS_P}tr"))


def get_cells(row):
    return list(row.findall(f"{NS_P}tc"))


def get_cell_text(cell):
    texts = []
    for t in cell.iter(f"{NS_P}t"):
        if t.text:
            texts.append(t.text)
    return "".join(texts).strip()


def set_cell_text(cell, value):
    """Set text in the first empty <hp:t>, or first <hp:t> if all have text."""
    for t_elem in cell.iter(f"{NS_P}t"):
        if not t_elem.text or not t_elem.text.strip():
            t_elem.text = value
            return True
    # Overwrite first <hp:t>
    for t_elem in cell.iter(f"{NS_P}t"):
        t_elem.text = value
        return True
    # Create in first run
    for run in cell.iter(f"{NS_P}run"):
        t_new = ET.SubElement(run, f"{NS_P}t")
        t_new.text = value
        return True
    return False


def replace_cell_text(cell, old_text, new_text):
    for t_elem in cell.iter(f"{NS_P}t"):
        if t_elem.text and old_text in t_elem.text:
            t_elem.text = t_elem.text.replace(old_text, new_text)
            return True
    return False


def fill_table_cell(tables, table_idx, row_idx, col_idx, value):
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


def set_cell_multiline(cell, text, para_pr_id=None, char_pr_id=None):
    """Set multi-line text by creating separate <hp:p> for each line."""
    sublist = cell.find(f"{NS_P}subList")
    if sublist is None:
        return False

    existing_p = sublist.find(f"{NS_P}p")
    ppr = para_pr_id or (existing_p.get("paraPrIDRef", "0") if existing_p is not None else "0")
    existing_run = existing_p.find(f"{NS_P}run") if existing_p is not None else None
    cpr = char_pr_id or (existing_run.get("charPrIDRef", "0") if existing_run is not None else "0")

    for p in list(sublist.findall(f"{NS_P}p")):
        sublist.remove(p)

    lines = text.split("\n")
    for line in lines:
        p = ET.SubElement(sublist, f"{NS_P}p")
        p.set("id", "0")
        p.set("paraPrIDRef", ppr)
        p.set("styleIDRef", "0")
        p.set("pageBreak", "0")
        p.set("columnBreak", "0")
        p.set("merged", "0")
        run = ET.SubElement(p, f"{NS_P}run")
        run.set("charPrIDRef", cpr)
        t_elem = ET.SubElement(run, f"{NS_P}t")
        t_elem.text = line
    return True


def fill_resume(root, profile):
    """이력서 부분 채우기 (Table 0~3 + paragraph 서명)"""
    tables = get_tables(root)
    pi = profile["personal_info"]
    exp = profile["experience"]
    certs = profile["certifications"]

    # ── Table 0: 인적사항 헤더 ──
    # R1: 지원구분 → 경력 체크
    rows0 = get_rows(tables[0])
    cells_r1 = get_cells(rows0[1])
    replace_cell_text(cells_r1[1], "신입(   ) /경력(     )", "신입(   ) /경력(  ○  )")

    # R2: 성명 (한글 + 영문) — PREV 형식: (한글) 임 종 권 (영문) LIM JONG KWON
    cells_r2 = get_cells(rows0[2])
    name_spaced = " ".join(pi["name_ko"])  # "임 종 권"
    name_en_upper = pi["name_en"].upper()  # "LIM JONG KWON"
    replace_cell_text(cells_r2[1], "(한글)                                            (영문)",
                      f"(한글) {name_spaced}                       (영문)  {name_en_upper}")

    # ── Table 1: 연락처 ──
    rows1 = get_rows(tables[1])
    # R0: 현주소 — PREV 형식: 우편번호 포함, 간결
    cells_1r0 = get_cells(rows1[0])
    set_cell_text(cells_1r0[1], "(14277) 경기도 광명시 도덕로 79 1405호")

    # R1: 본인휴대폰 + 전자우편 — PREV 형식: 라벨 유지
    cells_1r1 = get_cells(rows1[1])
    replace_cell_text(cells_1r1[1], "(본인휴대폰)", f"(본인휴대폰) {pi['phone']}")
    set_cell_text(cells_1r1[3], pi["email"])

    # R2: 비상연락처 — PREV 형식: 라벨 유지
    cells_1r2 = get_cells(rows1[2])
    replace_cell_text(cells_1r2[0], "(비상연락처)", f"(비상연락처) {pi['phone']}")

    # R3: 가점항목 — 해당없으므로 그대로 둠

    # ── Table 2: 주요 경력사항 (R3~R5) — PREV 형식: 2줄 분리, zero-pad, 불릿 ──
    rows2 = get_rows(tables[2])

    # 함께만드는세상 (3년 1월)
    cells_2r3 = get_cells(rows2[3])
    set_cell_multiline(cells_2r3[0], "(사)함께만드는세상\n(경영지원부)")
    replace_cell_text(cells_2r3[1], "~", "2023.01.09 ~ 2026.02.01")
    replace_cell_text(cells_2r3[2], "년  월  일", "3년  1월  일")
    set_cell_text(cells_2r3[3], "대리")
    set_cell_multiline(cells_2r3[4], "- 예산 3.6억 집행·정산\n- ERP 도입 PM\n- 외주업체 관리")

    # 맨지온 (1년 9월)
    cells_2r4 = get_cells(rows2[4])
    set_cell_multiline(cells_2r4[0], "(주)맨지온\n(개발부)")
    replace_cell_text(cells_2r4[1], "~", "2020.03.01 ~ 2021.11.20")
    replace_cell_text(cells_2r4[2], "년  월  일", "1년  9월  일")
    set_cell_text(cells_2r4[3], "대리")
    set_cell_multiline(cells_2r4[4], "- 임베디드 개발\n- IoT 모니터링\n- QA")

    # 엣지크로스 (1년 10월)
    cells_2r5 = get_cells(rows2[5])
    set_cell_multiline(cells_2r5[0], "(주)엣지크로스\n(기술연구소)")
    replace_cell_text(cells_2r5[1], "~", "2016.05.01 ~ 2018.02.28")
    replace_cell_text(cells_2r5[2], "년  월  일", "1년  10월  일")
    set_cell_text(cells_2r5[3], "주임")
    set_cell_multiline(cells_2r5[4], "- HW개발(회로·PCB·시제품)\n- BOM 관리")

    # ── Table 3: 자격증 보유현황 (R2~R4) ──
    fill_table_cell(tables, 3, 2, 0, "사회복지사 1급")
    fill_table_cell(tables, 3, 2, 1, "제1급-0046810")
    fill_table_cell(tables, 3, 2, 2, "2021년 2월 4일")

    fill_table_cell(tables, 3, 3, 0, "1종 대형 운전면허")
    fill_table_cell(tables, 3, 3, 2, "2019년 2월")

    # ── Paragraph [8]: 지원날짜 ──
    children = list(root)
    for t_elem in children[8].iter(f"{NS_P}t"):
        if t_elem.text and "년" in t_elem.text and "월" in t_elem.text:
            t_elem.text = "                                             지 원 날 짜 : 2026 년  03 월  06 일   "

    # ── Paragraph [9]: 지원자 서명 ──
    name_sp = " ".join(pi["name_ko"])
    for t_elem in children[9].iter(f"{NS_P}t"):
        if t_elem.text and "지 원 자" in t_elem.text:
            t_elem.text = f"                                             지 원 자 :      {name_sp}     (서명)"


def fill_coverletter(root, profile):
    """자기소개서 부분 채우기 (Table 4 + Table 5 교체 + paragraph 서명)"""
    tables = get_tables(root)
    pi = profile["personal_info"]
    children = list(root)

    # ── Table 4: 성명 / 모집분야 — PREV 형식: 띄어쓰기 ──
    name_spaced = " ".join(pi["name_ko"])
    fill_table_cell(tables, 4, 0, 1, name_spaced)
    fill_table_cell(tables, 4, 0, 3, "자격관리본부 단기계약직")

    # ── Table 5: 자기소개서 본문 — 안내문 삭제 후 본문으로 교체 ──
    # Table 5는 안내사항이 담긴 1행 1열 테이블. 이 안의 텍스트를 모두 자기소개서 본문으로 교체
    rows5 = get_rows(tables[5])
    cells_5r0 = get_cells(rows5[0])
    cell = cells_5r0[0]

    coverletter_text = (
        "1. 지원동기\n"
        "\n"
        "비영리 법인에서 3년간 예산 집행·정산·서류 검증 업무를 수행했습니다. "
        "외주업체 8개의 계약서·세금계산서·정산서를 대조·검증하는 일이 일상이었습니다.\n"
        "자격증 심사와 실습기관 심사는 제가 해온 서류 검증·기준 적합성 확인과 "
        "본질적으로 같다고 생각합니다. 대학원에서 사회복지학을 전공하고 "
        "사회복지사 1급을 취득한 사람으로서, 자격관리의 공적 책임을 잘 알기에 지원합니다.\n"
        "\n"
        "2. 생활신조와 가치관\n"
        "\n"
        "\"맡은 일은 끝까지 확인한다\"는 원칙으로 일합니다. "
        "예산 정산에서 1원 단위까지 맞추고, ERP 도입 시에도 실무 부서와 반복 확인하여 "
        "현장에 맞는 기준을 만들었습니다. "
        "심사 업무도 같은 태도로 정확히 판단하되, "
        "지원자와 기관의 입장도 이해하는 균형을 갖추겠습니다.\n"
        "\n"
        "3. 성격의 장단점\n"
        "\n"
        "[장점] 꼼꼼함과 체계적 정리 — 외주 8개사 계약·정산을 동시 관리하며 "
        "서류 누락이나 기한 초과 없이 마무리하는 것이 강점입니다.\n"
        "[단점] 확인 과정이 길어질 수 있으나, 반복 업무에 엑셀 매크로와 AI 도구를 "
        "활용하여 검증 속도를 높이는 방식으로 보완하고 있습니다.\n"
        "\n"
        "4. 앞으로의 각오\n"
        "\n"
        "- 예산 집행·정산 경험 → 심사 서류의 기준 적합성 검증\n"
        "- ERP 도입·프로세스 설계 → 심사 절차의 체계적 수행\n"
        "- 사회복지사 1급 + 석사 → 자격관리 직무의 전문적 맥락 이해\n"
        "\n"
        "맡겨진 심사 건수를 정확하고 신속하게 처리하여 "
        "자격관리본부의 업무 부담을 실질적으로 덜어드리겠습니다."
    )

    set_cell_multiline(cell, coverletter_text)

    # ── Paragraph [15]: 작성 날짜 ──
    for t_elem in children[15].iter(f"{NS_P}t"):
        if t_elem.text and "년" in t_elem.text and "월" in t_elem.text:
            t_elem.text = "    2026 년  03 월  06 일"

    # ── Paragraph [16]: 작성자 서명 ──
    name_sp2 = " ".join(pi["name_ko"])
    for t_elem in children[16].iter(f"{NS_P}t"):
        if t_elem.text and "작 성 자" in t_elem.text:
            t_elem.text = f"          작 성 자 :    {name_sp2}   (서명)"


def fill_consent(root, profile):
    """개인정보 동의서 체크 + 서명"""
    tables = get_tables(root)
    pi = profile["personal_info"]
    children = list(root)

    # ── Table 6: 동의 1 (R1) → □ → ■ ──
    rows6 = get_rows(tables[6])
    cells_6r1 = get_cells(rows6[1])
    replace_cell_text(cells_6r1[0], "동의함 □", "동의함 ■")

    # ── Table 7: 동의 2 (R1) → □ → ■ ──
    rows7 = get_rows(tables[7])
    cells_7r1 = get_cells(rows7[1])
    replace_cell_text(cells_7r1[0], "동의함 □", "동의함 ■")

    # ── Paragraph [40]: 날짜 ──
    for t_elem in children[40].iter(f"{NS_P}t"):
        if t_elem.text and "년" in t_elem.text and "월" in t_elem.text:
            t_elem.text = "2026 년   03 월  06 일"

    # ── Paragraph [42]: 성명 (인) ──
    name_sp3 = " ".join(pi["name_ko"])
    for t_elem in children[42].iter(f"{NS_P}t"):
        if t_elem.text and "성  명" in t_elem.text:
            t_elem.text = f"성  명 :  {name_sp3}  (인)"


def fill_hwpx_template(input_path, output_path, profile):
    """Main: open hwpx, modify section0.xml, write new hwpx."""
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    with zipfile.ZipFile(input_path, "r") as zin:
        section_xml = zin.read("Contents/section0.xml").decode("utf-8")
        root = ET.fromstring(section_xml)

        fill_resume(root, profile)
        fill_coverletter(root, profile)
        fill_consent(root, profile)

        modified_xml = ET.tostring(root, encoding="unicode", xml_declaration=False)
        modified_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>' + modified_xml

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "Contents/section0.xml":
                    zout.writestr(item, modified_xml.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))

    print(f"✅ 생성 완료: {output_path}")


if __name__ == "__main__":
    profile = load_profile()
    fill_hwpx_template(INPUT_HWPX, OUTPUT_HWPX, profile)

    # Quick verification
    print("\n── 검증: 생성된 파일 텍스트 추출 ──")
    with zipfile.ZipFile(OUTPUT_HWPX, "r") as z:
        content = z.read("Contents/section0.xml").decode("utf-8")
        root = ET.fromstring(content)
        for t in root.iter(f"{NS_P}t"):
            if t.text and t.text.strip():
                text = t.text.strip()
                if any(kw in text for kw in [
                    "임종권", "광명", "010-", "ssujklim", "함께만드는",
                    "맨지온", "엣지크로스", "사회복지사", "2026", "경력(", "동의함 ■",
                    "지원동기", "생활신조", "성격의", "각오"
                ]):
                    print(f"  → {text[:80]}")
