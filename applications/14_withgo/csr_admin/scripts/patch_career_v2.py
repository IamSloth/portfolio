"""
patch_career_v2.py — v2.hwpx 경력기술서 텍스트만 직접 교체 (서명이미지 보존)
Usage: python patch_career_v2.py
"""
import os, zipfile
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..")
TARGET = os.path.join(BASE_DIR, "drafts", "application_form_v2.hwpx")

# Namespace registration (preserve hwpx prefixes)
NAMESPACES = {
    "hp": "http://www.hancom.co.kr/hwpml/2011/paragraph",
    "hp6": "urn:hancom:hwpml:paragraph",
    "hs": "http://www.hancom.co.kr/hwpml/2011/section",
    "hs6": "urn:hancom:hwpml:section",
    "hh": "http://www.hancom.co.kr/hwpml/2011/head",
    "hc": "http://www.hancom.co.kr/hwpml/2011/core",
    "hc6": "urn:hancom:hwpml:core",
    "config": "urn:hancom:hwpml:config",
    "case": "urn:hancom:hwpml:case",
    "hwpdata": "urn:hancom:hwpml:hwpdata",
    "hml": "http://www.hancom.co.kr/hwpml/2011/HwpML",
}
for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

NS_P = "{http://www.hancom.co.kr/hwpml/2011/paragraph}"

# AS-IS → TO-BE mapping (exact text replacement)
REPLACEMENTS = {
    "  - 시설관리비·지급수수료·자산취득비 등 복합 관리": "  - 지출내역 정리·증빙관리·정산보고서 작성",
    "■ 커스텀 ERP 도입 PM 18개월 (Tibero/Nexacro 기반)": "■ 커스텀 ERP 도입 PM (Tibero/Nexacro)",
    "  - 요구정의→프로세스설계→계정과목표준화→검수": "  - 공익법인 회계 계정과목 표준화·프로세스 설계",
    "■ PC/네트워크 트러블슈팅 내재화 (비용 30%↓)": "■ IT자산 대장관리·유휴장비 재배치 (중복투자 방지)",
    "■ 소방안전관리자 법정 점검 수행": "■ 총무 행정 전반 (비품·문서관리·행사지원)",
}


def patch():
    if not os.path.exists(TARGET):
        print(f"❌ 파일 없음: {TARGET}")
        return

    with zipfile.ZipFile(TARGET, "r") as zin:
        section_xml = zin.read("Contents/section0.xml").decode("utf-8")
        all_items = zin.infolist()
        all_data = {item.filename: zin.read(item.filename) for item in all_items}

    root = ET.fromstring(section_xml)

    # Find and replace text in <hp:t> elements
    replaced = 0
    for t_elem in root.iter(f"{NS_P}t"):
        if t_elem.text and t_elem.text in REPLACEMENTS:
            old = t_elem.text
            t_elem.text = REPLACEMENTS[old]
            replaced += 1
            print(f"  ✔ {old.strip()[:20]}… → {REPLACEMENTS[old].strip()[:20]}…")

    if replaced == 0:
        print("⚠️ 교체 대상 텍스트를 찾지 못함")
        return

    # Rebuild ZIP with patched section0.xml
    new_section = ET.tostring(root, encoding="unicode")
    all_data["Contents/section0.xml"] = new_section.encode("utf-8")

    with zipfile.ZipFile(TARGET, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in all_items:
            zout.writestr(item, all_data[item.filename])

    print(f"\n✅ 패치 완료 ({replaced}건): {TARGET}")


if __name__ == "__main__":
    patch()
