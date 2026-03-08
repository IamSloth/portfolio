"""
fill_hwpx.py — 서울사회적경제지원센터 매니저 지원서류 자동 채우기
(응시원서 + 개인정보동의서 + 이력서 + 자기소개서 + 경력기술서)
Usage: python fill_hwpx.py
"""
import zipfile
import xml.etree.ElementTree as ET
import json
import os

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..")
PROFILE_PATH = os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "content", "profile.json")
INPUT_HWPX = os.path.join(BASE_DIR, "artifacts", "미담장학회_자사양식.hwpx")
OUTPUT_HWPX = os.path.join(BASE_DIR, "drafts", "application_form_v2.hwpx")

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
    for t_elem in cell.iter(f"{NS_P}t"):
        t_elem.text = value
        return True
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


def overwrite_cell_text(cell, new_text):
    """Overwrite ALL <hp:t> in cell: first gets new_text, rest cleared."""
    first = True
    for t_elem in cell.iter(f"{NS_P}t"):
        if first:
            t_elem.text = new_text
            first = False
        else:
            t_elem.text = ""
    return not first


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


# ══════════════════════════════════════════════════════════
# 1. 응시원서 (Table 0, 20 rows)
# ══════════════════════════════════════════════════════════
def fill_application_form(root, profile):
    tables = get_tables(root)
    pi = profile["personal_info"]
    children = list(root)

    t0 = tables[0]
    rows = get_rows(t0)

    # ── R0: 주소(C1), 이동전화(C2) ──
    cells_r0 = get_cells(rows[0])
    set_cell_text(cells_r0[1], "(14277) 경기도 광명시 도덕로 79 1405호")
    # 이동전화 — label 뒤에 번호 추가
    replace_cell_text(cells_r0[2], "이동전화", f"이동전화  {pi['phone']}")

    # ── R1: (empty, 1c) — 주소 연장 또는 전화값 ──
    # skip (빈 셀)

    # ── R2: 긴급연락처 (C0, 1c) ──
    cells_r2 = get_cells(rows[2])
    replace_cell_text(cells_r2[0], "긴급연락처", f"긴급연락처  {pi['phone']}")

    # ── R5: 최종학력 - 대학교이하 ──
    # C0=대학교이하(label), C1=입학년월, C2=학교+과+년, C3=상태
    cells_r5 = get_cells(rows[5])
    replace_cell_text(cells_r5[1], "년    월", "2010년 03월")
    replace_cell_text(cells_r5[2], "대학교 과 년",
                      "숭실대학교 전기공학부 4년")
    overwrite_cell_text(cells_r5[3], "졸업")

    # ── R6: 최종학력 - 대학원 ──
    cells_r6 = get_cells(rows[6])
    replace_cell_text(cells_r6[1], "년    월", "2018년 03월")
    overwrite_cell_text(cells_r6[2], "숭실대학교 사회복지대학원 2년")
    overwrite_cell_text(cells_r6[3], "졸업")

    # ── R8~R10: 주요경력 3건 ──
    # R8: 함께만드는세상
    cells_r8 = get_cells(rows[8])
    overwrite_cell_text(cells_r8[0], "2023.01 ~ 2026.02")
    set_cell_text(cells_r8[1], "(사)함께만드는세상")
    set_cell_text(cells_r8[2], "경영지원부")
    set_cell_text(cells_r8[3], "대리")
    overwrite_cell_text(cells_r8[4], "3년  1개월")

    # R9: 맨지온
    cells_r9 = get_cells(rows[9])
    overwrite_cell_text(cells_r9[0], "2020.03 ~ 2021.11")
    set_cell_text(cells_r9[1], "(주)맨지온")
    set_cell_text(cells_r9[2], "개발부")
    set_cell_text(cells_r9[3], "대리")
    overwrite_cell_text(cells_r9[4], "1년  9개월")

    # R10: 엣지크로스
    cells_r10 = get_cells(rows[10])
    overwrite_cell_text(cells_r10[0], "2016.05 ~ 2018.02")
    set_cell_text(cells_r10[1], "(주)엣지크로스")
    set_cell_text(cells_r10[2], "기술연구소")
    set_cell_text(cells_r10[3], "주임")
    overwrite_cell_text(cells_r10[4], "1년 10개월")

    # ── R12~R14: 자격사항 ──
    # R12: 사회복지사 1급
    cells_r12 = get_cells(rows[12])
    overwrite_cell_text(cells_r12[0], "2021년  02월  04일")
    set_cell_text(cells_r12[1], "사회복지사 1급")
    set_cell_text(cells_r12[2], "보건복지부")

    # R13: 1종 대형 운전면허
    cells_r13 = get_cells(rows[13])
    overwrite_cell_text(cells_r13[0], "2019년  02월")
    set_cell_text(cells_r13[1], "1종 대형 운전면허")
    set_cell_text(cells_r13[2], "경찰청")

    # ── R15: 성명(한글) ──
    # R15 (4c): C0=응시번호, C1=(empty), C2=성명, C3=(한글)
    cells_r15 = get_cells(rows[15])
    replace_cell_text(cells_r15[3], "(한글)", pi["name_ko"])

    # ── R16: 성명(한자) ──
    cells_r16 = get_cells(rows[16])
    replace_cell_text(cells_r16[0], "(한자)", pi["name_hanja"])

    # ── R17: 생년월일 ──
    # R17 (4c): C0=응시분야, C1=매니저, C2=생년월일, C3=년월일(만세)
    cells_r17 = get_cells(rows[17])
    overwrite_cell_text(cells_r17[3], "1992년  01월  04일(만 34세)")

    # ── 응시원서 날짜 (Child[6]) ──
    for t_elem in children[6].iter(f"{NS_P}t"):
        if t_elem.text and "월" in t_elem.text:
            t_elem.text = "2026년  03월  06일"

    # ── 응시원서 성명(인) (Child[8]) ──
    name_sp = " ".join(pi["name_ko"])
    for t_elem in children[8].iter(f"{NS_P}t"):
        if t_elem.text and "(인)" in t_elem.text:
            t_elem.text = f"성명   {name_sp}  (인)"


# ══════════════════════════════════════════════════════════
# 2. 개인정보 수집 및 활용 동의서 (Children paragraphs)
# ══════════════════════════════════════════════════════════
def fill_consent(root, profile):
    pi = profile["personal_info"]
    children = list(root)
    name_sp = " ".join(pi["name_ko"])

    # Child[45]: 날짜
    for t_elem in children[45].iter(f"{NS_P}t"):
        if t_elem.text and "월" in t_elem.text:
            t_elem.text = "2026년    03월     06일"

    # Child[47]: 성명(서명)
    for t_elem in children[47].iter(f"{NS_P}t"):
        if t_elem.text and "성명" in t_elem.text:
            t_elem.text = f"성명:   {name_sp}     (서명)"


# ══════════════════════════════════════════════════════════
# 3. 이력서 (Table 3, 29 rows)
# ══════════════════════════════════════════════════════════
def fill_resume(root, profile):
    tables = get_tables(root)
    pi = profile["personal_info"]

    t3 = tables[3]
    rows = get_rows(t3)

    # ── R0: 지원분야, 직급 ──
    fill_table_cell(tables, 3, 0, 2, "매니저")
    # R1: 채용형태
    fill_table_cell(tables, 3, 1, 1, "계약직")

    # ── R3: 성명(한글) ──
    cells_r3 = get_cells(rows[3])
    replace_cell_text(cells_r3[2], "(empty)", pi["name_ko"])
    # fallback: try setting empty cell
    set_cell_text(cells_r3[2], pi["name_ko"])

    # ── R7~R8: 교육 - 전공분야/학위취득일/학위종류 ──
    # R7: 석사 (최종학력 먼저)
    fill_table_cell(tables, 3, 7, 0, "사회적기업전공 (숭실대 사회복지대학원)")
    fill_table_cell(tables, 3, 7, 1, "2020.02")
    fill_table_cell(tables, 3, 7, 2, "석사")

    # R8: 학사
    fill_table_cell(tables, 3, 8, 0, "전기공학부 (숭실대 공과대학)")
    fill_table_cell(tables, 3, 8, 1, "2017.02")
    fill_table_cell(tables, 3, 8, 2, "학사")

    # ── R10~R11: 직업훈련/기타 ──
    # R10: 폴리텍 AR 과정
    cells_r10 = get_cells(rows[10])
    replace_cell_text(cells_r10[0], "□ 직업훈련", "■ 직업훈련")
    fill_table_cell(tables, 3, 10, 2, "증강현실(AR) 시스템제어 (한국폴리텍 광명)")
    replace_cell_text(cells_r10[3], "~", "2022.06 ~ 2022.12")

    # ── R14~R18: 경력사항 5행 ──
    # R14: 함께만드는세상
    fill_table_cell(tables, 3, 14, 0, "(사)함께만드는세상")
    fill_table_cell(tables, 3, 14, 1, "경영지원부")
    fill_table_cell(tables, 3, 14, 2, "대리")
    fill_table_cell(tables, 3, 14, 3, "총무·IT지원·예산관리")
    cells_r14 = get_cells(rows[14])
    replace_cell_text(cells_r14[4], "~", "2023.01 ~ 2026.02")
    fill_table_cell(tables, 3, 14, 5, "3년 1월")

    # R15: 맨지온
    fill_table_cell(tables, 3, 15, 0, "(주)맨지온")
    fill_table_cell(tables, 3, 15, 1, "개발부")
    fill_table_cell(tables, 3, 15, 2, "대리")
    fill_table_cell(tables, 3, 15, 3, "임베디드 개발·QA")
    cells_r15 = get_cells(rows[15])
    replace_cell_text(cells_r15[4], "~", "2020.03 ~ 2021.11")
    fill_table_cell(tables, 3, 15, 5, "1년 9월")

    # R16: 엣지크로스
    fill_table_cell(tables, 3, 16, 0, "(주)엣지크로스")
    fill_table_cell(tables, 3, 16, 1, "기술연구소")
    fill_table_cell(tables, 3, 16, 2, "주임")
    fill_table_cell(tables, 3, 16, 3, "HW개발·자재관리")
    cells_r16 = get_cells(rows[16])
    replace_cell_text(cells_r16[4], "~", "2016.05 ~ 2018.02")
    fill_table_cell(tables, 3, 16, 5, "1년10월")

    # ── R19: 총경력 ──
    cells_r19 = get_cells(rows[19])
    replace_cell_text(cells_r19[1], "(    )년  (   )월", "( 3  )년  ( 1 )월")

    # ── R23~R26: 자격·수상 ──
    # R23: 사회복지사 1급
    fill_table_cell(tables, 3, 23, 0, "사회복지사 1급")
    fill_table_cell(tables, 3, 23, 1, "2021.02.04")
    fill_table_cell(tables, 3, 23, 2, "보건복지부")

    # R23: 수상 (같은 행 오른쪽)
    fill_table_cell(tables, 3, 23, 3, "메타버스 콘텐츠 리크루팅 캠프 대상")
    fill_table_cell(tables, 3, 23, 4, "2022.09")
    fill_table_cell(tables, 3, 23, 5, "과학기술정보통신부")

    # R24: 1종 대형 운전면허
    fill_table_cell(tables, 3, 24, 0, "1종 대형 운전면허")
    fill_table_cell(tables, 3, 24, 1, "2019.02")
    fill_table_cell(tables, 3, 24, 2, "경찰청")

    # ── R28: 날짜·서명 (5개 <hp:t> 분리: 사실확인문/날짜/작성자/공백/인) ──
    cells_r28 = get_cells(rows[28])
    replace_cell_text(cells_r28[0], "20  년    월     일", "2026년  03월   06일")
    name_sp = " ".join(pi["name_ko"])
    replace_cell_text(cells_r28[0], "작성자 :        ", f"작성자 : {name_sp}  ")


# ══════════════════════════════════════════════════════════
# 4. 자기소개서 (Table 4, 5 rows)
# ══════════════════════════════════════════════════════════
Q1_TEXT = (
    "사회적기업 석사 학위와 비영리법인 3년 실무 경험을 바탕으로 매니저 직무에 "
    "적합하다고 판단합니다.\n"
    "첫째, 숭실대 사회복지대학원 사회적기업전공 석사 과정에서 사회적경제 정책, "
    "협동조합·사회적기업 운영 원리, 사회적 가치 측정 방법론을 학습하여 센터 "
    "사업의 기획과 기업 지원에 이론적 기반을 갖추고 있습니다.\n"
    "둘째, (사)함께만드는세상에서 3년간 인프라 예산 약 3.6억 원을 편성·집행·"
    "정산하고, 외주업체 8개의 계약·관리를 총괄했습니다. ERP 도입 프로젝트에서 "
    "요구사항 정의부터 계정과목 표준화, 검수까지 전담하여 사업 기획·운영과 "
    "행정·회계 역량을 갖추었습니다.\n"
    "셋째, 8개 외주업체 관리와 ERP 도입 과정에서 다양한 이해관계자와 소통·"
    "조율한 경험이 있어 대내외 협력 업무에 즉시 기여할 수 있습니다.\n"
    "사회복지사 1급 자격으로 사회서비스 현장을 이해하는 실무자로서 센터의 사업 "
    "목표 달성에 기여하겠습니다."
)

Q2_TEXT = (
    "학업, 자격 취득, 실무를 단계적으로 축적하며 전문성을 쌓아 왔습니다.\n"
    "첫째, 전기공학 학사 후 기술의 사회적 가치에 주목하여 숭실대 사회복지대학원 "
    "사회적기업전공 석사에 진학했습니다. 사회적경제 정책, 사회적기업 경영, "
    "사회적 가치 측정론을 연구하며 학문적 기반을 갖추었습니다.\n"
    "둘째, 석사 과정과 병행하여 사회복지사 1급을 취득했습니다. 사회복지 정책과 "
    "행정 실무를 습득하여 사회적경제 생태계의 수혜자 관점을 이해하는 기반이 "
    "됩니다.\n"
    "셋째, (사)함께만드는세상에서 예산 관리, 외주업체 운영, ERP 도입 등 비영리 "
    "조직 운영의 핵심 업무를 3년간 담당하며 현장 역량을 축적했습니다. 특히 ERP "
    "도입 프로젝트를 주도하며 사업 기획·프로세스 설계 역량을 키웠습니다.\n"
    "넷째, 한국폴리텍에서 AR 시스템제어 과정을 수료하고, 엑셀 고급 기능과 AI "
    "도구 활용으로 데이터 기반 업무 수행이 가능합니다."
)


def fill_coverletter(root, profile):
    tables = get_tables(root)
    pi = profile["personal_info"]

    # R0 C1: 성명
    fill_table_cell(tables, 4, 0, 1, pi["name_ko"])

    # R2 C0: Q1 답변 (빈 셀)
    rows4 = get_rows(tables[4])
    cells_r2 = get_cells(rows4[2])
    set_cell_multiline(cells_r2[0], Q1_TEXT)

    # R4 C0: Q2 답변 (빈 셀)
    cells_r4 = get_cells(rows4[4])
    set_cell_multiline(cells_r4[0], Q2_TEXT)


# ══════════════════════════════════════════════════════════
# 5. 경력기술서 (Table 5, 3 rows)
# ══════════════════════════════════════════════════════════
CAREER_DESC_TEXT = (
    "비영리법인 (사)함께만드는세상에서 3년간(2023.01~2026.02) 총무·IT지원·"
    "예산관리 업무를 수행한 경험을 중심으로 핵심 역량을 기술합니다.\n"
    "1. 사업 예산 편성·집행·정산 (연간 약 3.6억 원)\n"
    "연간 예산을 직접 편성·집행하고 정산 보고서를 작성했습니다. 집행률 88.5%를 "
    "유지하며, 재계약 협상으로 연 약 500만 원을 절감했습니다. 제한된 예산으로 "
    "성과를 내야 하는 사회적경제 조직 운영에 적용 가능한 역량입니다.\n"
    "2. ERP 도입 프로젝트 실무 전담 (2023.07~2024.12)\n"
    "커스텀 ERP 도입 프로젝트에서 요구사항 수집, 프로세스 설계, 계정과목 표준화, "
    "검수까지 18개월간 전담했습니다. 조직 업무를 분석하고 시스템으로 구현한 "
    "사업 기획·운영 역량의 근거입니다.\n"
    "3. 외주업체 8개 계약·관리·정산\n"
    "소방·승강기·전기·방역 등 8개 업체의 계약 체결부터 정산까지 총괄했습니다. "
    "이해관계자 관리 역량은 센터의 기업 지원 및 대외 협력 업무에 연결됩니다.\n"
    "4. 학력·자격\n"
    "숭실대 사회적기업전공 석사(2020.02)와 사회복지사 1급(2021.02)을 통해 "
    "사회적경제의 이론과 사회서비스 현장에 대한 전문성을 갖추고 있습니다."
)


def fill_career_description(root, profile):
    tables = get_tables(root)
    pi = profile["personal_info"]

    # R0 C1: 성명
    fill_table_cell(tables, 5, 0, 1, pi["name_ko"])

    # R1 C1: 주제
    fill_table_cell(tables, 5, 1, 1,
                    "비영리법인 사업관리 3년 — 사회적경제 조직 운영의 이론과 실무")

    # R2 C0: 본문 (기존 작성요령 텍스트를 본문으로 교체)
    rows5 = get_rows(tables[5])
    cells_r2 = get_cells(rows5[2])
    set_cell_multiline(cells_r2[0], CAREER_DESC_TEXT)


# ══════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════
def fill_hwpx_template(input_path, output_path, profile):
    for prefix, uri in NAMESPACES.items():
        ET.register_namespace(prefix, uri)

    with zipfile.ZipFile(input_path, "r") as zin:
        section_xml = zin.read("Contents/section0.xml").decode("utf-8")
        root = ET.fromstring(section_xml)

        fill_application_form(root, profile)
        fill_consent(root, profile)
        fill_resume(root, profile)
        fill_coverletter(root, profile)
        fill_career_description(root, profile)

        modified_xml = ET.tostring(root, encoding="unicode", xml_declaration=False)
        modified_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>' + modified_xml

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == "Contents/section0.xml":
                    zout.writestr(item, modified_xml.encode("utf-8"))
                else:
                    zout.writestr(item, zin.read(item.filename))

    print(f"생성 완료: {output_path}")


if __name__ == "__main__":
    profile = load_profile()
    fill_hwpx_template(INPUT_HWPX, OUTPUT_HWPX, profile)

    # 글자수 검증
    q1_len = len(Q1_TEXT.replace("\n", ""))
    q2_len = len(Q2_TEXT.replace("\n", ""))
    cd_len = len(CAREER_DESC_TEXT.replace("\n", ""))
    print(f"\n── 글자수 검증 ──")
    print(f"Q1 (1000자 이내): {q1_len}자 {'✅' if q1_len <= 1000 else '❌ 초과!'}")
    print(f"Q2 (1000자 이내): {q2_len}자 {'✅' if q2_len <= 1000 else '❌ 초과!'}")
    print(f"경력기술서: {cd_len}자")

    # 간략 검증
    print("\n── 텍스트 검증 ──")
    with zipfile.ZipFile(OUTPUT_HWPX, "r") as z:
        content = z.read("Contents/section0.xml").decode("utf-8")
        vroot = ET.fromstring(content)
        for t in vroot.iter(f"{NS_P}t"):
            if t.text and t.text.strip():
                text = t.text.strip()
                if any(kw in text for kw in [
                    "임종권", "광명", "010-", "함께만드는", "사회적기업",
                    "매니저", "사회복지사", "2026", "졸업", "석사",
                    "비영리", "ERP", "외주"
                ]):
                    print(f"  → {text[:80]}")
