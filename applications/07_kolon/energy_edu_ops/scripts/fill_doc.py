"""
코오롱 에너지교육 운영인력 — 파인스태프 자사양식 .doc 자동 입력 (win32com)

사용법: python fill_doc.py
입력: artifacts/(주)파인스태프_자사양식.doc
출력: drafts/resume_v7.doc + drafts/resume_v7.pdf
"""
import os
import sys
import json
import tempfile
import win32com.client
from datetime import date

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', '..', '..'))
INPUT_DOC = os.path.join(BASE_DIR, 'artifacts', '(주)파인스태프_자사양식.doc')
OUTPUT_DOC = os.path.join(BASE_DIR, 'drafts', 'resume_v7.doc')
OUTPUT_PDF = os.path.join(BASE_DIR, 'drafts', 'resume_v7.pdf')
PROFILE_PATH = os.path.join(PROJECT_ROOT, 'content', 'profile.json')
PHOTO_PATH_PRIMARY = os.path.join(PROJECT_ROOT, 'common', 'photos', 'profile.png')
PHOTO_PATH_FALLBACK = os.path.join(PROJECT_ROOT, 'docs', 'assets', 'profile.png')
SEAL_PATH_PRIMARY = os.path.join(
    PROJECT_ROOT, 'applications', '01_seoul_heroes', 'accounting', 'artifacts', 'seal_stamp.png'
)


def load_profile():
    with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)



# wdAlignParagraphCenter = 1, wdAlignParagraphLeft = 0
WD_CENTER = 1
WD_LEFT = 0
WD_COLLAPSE_END = 0
WD_COLLAPSE_START = 1


def set_cell(table, row, col, value, font_size=10, font_name='굴림체', align=WD_CENTER):
    """테이블 셀에 텍스트 입력 + 서식 적용 (1-based index)"""
    try:
        cell = table.Cell(row, col)
        rng = cell.Range
        rng.Text = str(value)
        # 서식 적용
        rng.Font.Size = font_size
        rng.Font.Name = font_name
        rng.ParagraphFormat.Alignment = align
    except Exception as e:
        print(f"  [WARN] Cell({row},{col}) 접근 실패: {e}")


def resolve_photo_path():
    for p in (PHOTO_PATH_PRIMARY, PHOTO_PATH_FALLBACK):
        if os.path.exists(p):
            return p
    return None


def prepare_profile_photo(source_path, target_ratio, out_path):
    """증명사진 박스 비율에 맞춰 중앙 크롭."""
    try:
        from PIL import Image

        resampling = getattr(getattr(Image, 'Resampling', Image), 'LANCZOS')
        with Image.open(source_path) as img:
            img = img.convert('RGB')
            w, h = img.size
            src_ratio = w / h

            if src_ratio > target_ratio:
                # 가로가 넓은 경우 좌우 크롭
                new_w = int(h * target_ratio)
                left = max(0, (w - new_w) // 2)
                img = img.crop((left, 0, left + new_w, h))
            elif src_ratio < target_ratio:
                # 세로가 긴 경우 상단 약간 우선하여 크롭
                new_h = int(w / target_ratio)
                top = max(0, int((h - new_h) * 0.18))
                if top + new_h > h:
                    top = h - new_h
                img = img.crop((0, top, w, top + new_h))

            target_w = 480
            target_h = int(target_w / target_ratio)
            img = img.resize((target_w, target_h), resample=resampling)
            img.save(out_path, format='PNG')
        return out_path
    except Exception as e:
        print(f"  [WARN] 프로필 사진 전처리 실패, 원본 사용: {e}")
        return source_path


def insert_profile_photo(doc):
    """Table 2 사진칸에 프로필 사진 삽입."""
    photo_src = resolve_photo_path()
    if not photo_src:
        print("  [WARN] 프로필 사진 파일을 찾을 수 없습니다.")
        return

    try:
        t = doc.Tables(2)
        cell = t.Cell(1, 1)
        box_w = max(30.0, float(cell.Width))
        box_h = max(30.0, float(cell.Height))
        target_ratio = box_w / box_h

        prepared_path = os.path.join(tempfile.gettempdir(), 'kolon_profile_photo.png')
        use_path = prepare_profile_photo(photo_src, target_ratio, prepared_path)

        rng = cell.Range
        rng.Text = ''
        rng.Collapse(WD_COLLAPSE_START)
        pic = rng.InlineShapes.AddPicture(
            FileName=os.path.abspath(use_path),
            LinkToFile=False,
            SaveWithDocument=True
        )

        max_w = box_w - 4.0
        max_h = box_h - 4.0
        if pic.Width > 0 and pic.Height > 0:
            scale = min(max_w / pic.Width, max_h / pic.Height)
            pic.Width = pic.Width * scale
            pic.Height = pic.Height * scale

        cell.Range.ParagraphFormat.Alignment = WD_CENTER
    except Exception as e:
        print(f"  [WARN] 사진 삽입 실패: {e}")


def generate_seal(name, output_path, size=180):
    """도장 이미지가 없을 때 간단한 원형 인장 생성."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        margin = 8
        draw.ellipse(
            (margin, margin, size - margin, size - margin),
            outline=(200, 30, 30, 255),
            width=6
        )

        try:
            font = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', size // 4)
        except OSError:
            font = ImageFont.load_default()

        chars = list(name[:3])
        total_h = len(chars) * (size // 4 + 4)
        y_start = (size - total_h) // 2 + 4
        for i, ch in enumerate(chars):
            bbox = draw.textbbox((0, 0), ch, font=font)
            tw = bbox[2] - bbox[0]
            x = (size - tw) // 2
            y = y_start + i * (size // 4 + 4)
            draw.text((x, y), ch, fill=(200, 30, 30, 255), font=font)

        img.save(output_path, 'PNG')
        return output_path
    except Exception as e:
        print(f"  [WARN] 도장 생성 실패: {e}")
        return None


def resolve_seal_path(name):
    if os.path.exists(SEAL_PATH_PRIMARY):
        return SEAL_PATH_PRIMARY
    fallback = os.path.join(tempfile.gettempdir(), 'kolon_seal_stamp.png')
    return generate_seal(name, fallback, size=180)


def insert_signature_stamp(doc, name):
    """성명 줄 끝에 도장(서명) 이미지 삽입."""
    seal_path = resolve_seal_path(name)
    if not seal_path:
        print("  [WARN] 서명(도장) 이미지가 없어 삽입을 건너뜁니다.")
        return

    target_paragraph = None
    for i in range(1, doc.Paragraphs.Count + 1):
        p = doc.Paragraphs(i)
        text = p.Range.Text.strip().replace('\r', '').replace('\x07', '')
        if text.startswith('성명:') and name in text:
            target_paragraph = p
            break

    if not target_paragraph:
        print("  [WARN] 서명 삽입 위치를 찾지 못했습니다.")
        return

    try:
        rng = target_paragraph.Range.Duplicate
        if rng.End > rng.Start:
            rng.End -= 1  # paragraph mark 제외
        rng.Collapse(WD_COLLAPSE_END)
        rng.Text = ' '
        rng.Collapse(WD_COLLAPSE_END)

        pic = rng.InlineShapes.AddPicture(
            FileName=os.path.abspath(seal_path),
            LinkToFile=False,
            SaveWithDocument=True
        )
        target_w = 16.0  # pt
        if pic.Width > target_w:
            scale = target_w / pic.Width
            pic.Width = pic.Width * scale
            pic.Height = pic.Height * scale
    except Exception as e:
        print(f"  [WARN] 서명 삽입 실패: {e}")


def fill_application_field(doc):
    """Table 1: 지원분야 (C3: w=102pt)"""
    t = doc.Tables(1)
    set_cell(t, 1, 3, '코오롱 사회공헌사무국', font_size=9)  # 102pt 셀
    set_cell(t, 2, 3, '에너지교육 운영인력', font_size=9)


def fill_personal_info(doc, profile):
    """Table 3: 인적사항"""
    t = doc.Tables(3)
    p = profile['personal_info']

    # 이름 (C4: 144pt)
    set_cell(t, 1, 4, p['name_ko'], font_size=11)
    set_cell(t, 1, 6, p['birthdate'].replace('-', '.'), font_size=10)  # C6: 107pt
    set_cell(t, 2, 4, p['name_en'], font_size=10)
    set_cell(t, 2, 6, '남', font_size=10)

    # 주소 (C3: 234pt) + 소요시간 (C4: 89pt → "약 50분"만)
    set_cell(t, 3, 3, p['address'], font_size=9, align=WD_LEFT)
    set_cell(t, 3, 4, '약 50분', font_size=9)

    # 연락처
    set_cell(t, 4, 3, p['email'], font_size=9, align=WD_LEFT)
    set_cell(t, 5, 3, '-', font_size=10)
    set_cell(t, 5, 5, p['phone'], font_size=10)


def fill_education(doc, profile):
    """Table 4: 학력사항
    C2=학교명(90pt), C3=학교구분(54pt,label), C4=기간(189pt), C5=전공(95pt), C6=졸업(54pt)
    """
    t = doc.Tables(4)
    # 렌더러(Word/PDF 뷰어)별 열 폭 흔들림 방지
    try:
        t.AllowAutoFit = False
    except Exception:
        pass
    edu = profile['education']

    # R2: 고등학교 (C2: 90pt)
    hs = next((e for e in edu if '고등학교' in e.get('school', '')), None)
    if hs:
        # 학교명 칸 폭이 좁아 잘려 보일 수 있어 축약 표기 사용
        set_cell(t, 2, 2, '명문고', font_size=9)
        set_cell(t, 2, 4, '2007.03 ～ 2010.02', font_size=9)
        set_cell(t, 2, 6, '졸업', font_size=9)

    # R4: 대학교 (4년제)
    undergrad = next((e for e in edu if e.get('degree') == '학사'), None)
    if undergrad:
        set_cell(t, 4, 2, '숭실대', font_size=9)
        period = undergrad.get('period', '').replace(' ~ ', ' ～ ')
        set_cell(t, 4, 4, period, font_size=9)
        set_cell(t, 4, 5, '전기공학/경제학(복수)', font_size=8)  # 95pt, 글자 많아서 8pt
        set_cell(t, 4, 6, '졸업', font_size=9)

    # R5: 대학원
    grad = next((e for e in edu if e.get('degree') == '석사'), None)
    if grad:
        set_cell(t, 5, 2, '숭실대 복지대학원', font_size=8)
        period = grad.get('period', '').replace(' ~ ', ' ～ ')
        set_cell(t, 5, 4, period, font_size=9)
        set_cell(t, 5, 5, '사회적기업', font_size=9)
        set_cell(t, 5, 6, '졸업', font_size=9)


def fill_career(doc, profile):
    """Table 5: 경력사항
    C2=직장명(117pt), C3=기간(144pt), C4=근무부서(54pt), C5=담당업무(81pt), C6=퇴직사유(81pt)
    """
    t = doc.Tables(5)
    careers = [
        ('(사)함께만드는세상', '2023.01 ～ 2026.02', '경영지원부', '총무·IT지원', '자발적 퇴사'),
        ('(주)맨지온', '2020.03 ～ 2021.11', '개발부', '임베디드개발·QA', '계약만료'),
        ('(주)엣지크로스', '2016.05 ～ 2018.02', '기술연구소', 'H/W개발·자재관리', '계약만료'),
    ]
    for i, (company, period, dept, role, reason) in enumerate(careers):
        row = 2 + i
        set_cell(t, row, 2, company, font_size=9)
        set_cell(t, row, 3, period, font_size=9)
        set_cell(t, row, 4, dept, font_size=8)    # 54pt 좁음
        set_cell(t, row, 5, role, font_size=8)     # 81pt
        set_cell(t, row, 6, reason, font_size=8)   # 81pt


def fill_certifications(doc):
    """Table 6: 자격증
    C2=자격명(117pt), C3=취득일자(46pt), C4=발급기관(81pt), C5=자격명(90pt), C6=취득일자(54pt), C7=발급기관(90pt)
    """
    t = doc.Tables(6)
    set_cell(t, 2, 2, '사회복지사 1급', font_size=9)
    set_cell(t, 2, 3, '2020.02', font_size=9)
    set_cell(t, 2, 4, '보건복지부', font_size=9)
    set_cell(t, 2, 5, '1종대형 운전면허', font_size=8)  # 90pt
    set_cell(t, 2, 6, '2019.02', font_size=9)
    set_cell(t, 2, 7, '경찰청', font_size=9)


def fill_etc(doc, profile):
    """Table 7: 기타사항
    병역: C5=구분label, C6=값(74pt). OA: C9=항목label(72pt), C10=값
    """
    t = doc.Tables(7)
    mil = profile.get('military', {})

    # 장애인복지카드 (C3: 64pt)
    set_cell(t, 1, 3, 'N', font_size=10)

    # 병역사항 (C6: 74pt)
    set_cell(t, 2, 6, mil.get('service_type', ''), font_size=10)
    set_cell(t, 3, 6, mil.get('rank', ''), font_size=10)
    set_cell(t, 4, 6, '2012.05～2014.05', font_size=8)  # 74pt 좁음, 공백 제거
    # R5,C6=면제사유 → 만기제대이므로 빈칸

    # 취미 (C3: 64pt)
    set_cell(t, 5, 3, '야구관람, 게임', font_size=8)  # 64pt 좁음

    # OA 능력 (C10)
    set_cell(t, 2, 10, '상', font_size=10)    # 한글
    set_cell(t, 3, 10, '상', font_size=10)    # MS-Word
    set_cell(t, 4, 10, '상', font_size=10)    # EXCEL
    set_cell(t, 5, 10, '상', font_size=10)    # PowerPoint
    set_cell(t, 6, 10, '영어(하)', font_size=8)  # 외국어


def fill_self_intro(doc):
    """Table 8: 자기소개서 (성격소개, 경력특기, 지원동기)"""
    t = doc.Tables(8)

    # R2: 성격소개
    personality = (
        "전기공학 전공 기반의 문제해결력과 교육 현장 실무경험을 갖춘 인재입니다. "
        "운영 이슈에 빠르게 대응하고, 맡은 업무를 끝까지 책임집니다."
    )
    set_cell(t, 2, 1, personality, font_size=8, align=WD_LEFT)

    # R4: 경력사항 및 특기사항
    career_highlights = (
        "■ 교육운영 실무(3년)\n"
        "KDB시니어브리지아카데미 운영 지원: 모집·접수, 교육장/교구 관리, 외부협력 커뮤니케이션.\n"
        "■ 예산/인프라 관리\n"
        "인프라 예산 3.6억 원 집행·통제(집행률 88.5%), 재계약 협상으로 연 500만 원 절감.\n"
        "■ 즉시투입 역량\n"
        "1종 대형면허(12년 무사고), 전기공학 기반 에너지 콘텐츠 이해, ERP/SQL/Excel 활용."
    )
    set_cell(t, 4, 1, career_highlights, font_size=8, align=WD_LEFT)

    # R6: 미래계획 및 포부 (지원동기)
    motivation = (
        "기술과 교육의 접점에서 현장 품질을 높이고자 지원했습니다. "
        "전기공학 기반 이해력과 교육운영 경험을 결합해 에코 롱롱 프로그램에 기여하겠습니다.\n"
        "1종 대형면허 보유로 찾아가는 에너지학교 차량운행에 즉시 투입 가능하며, "
        "안전·정확·성실한 운영으로 지속 성과를 만들겠습니다."
    )
    set_cell(t, 6, 1, motivation, font_size=8, align=WD_LEFT)


def fill_date_signature(doc, name):
    """문서 하단 날짜 + 성명 입력"""
    today = date.today()
    # P286='년 월 일' → 실제 날짜로 교체
    # P287='성명: 서명 또는 (인)' → 이름 입력
    for i in range(1, doc.Paragraphs.Count + 1):
        p = doc.Paragraphs(i)
        text = p.Range.Text.strip().replace('\r', '').replace('\x07', '')
        if '년 월 일' in text and '보유' not in text and '이용' not in text:
            p.Range.Text = f'{today.year}년 {today.month:02d}월 {today.day:02d}일\r'
        elif '성명:' in text and '서명' in text:
            p.Range.Text = f'성명: {name}  (인)\r'


def fill_consent_checks(doc):
    """동의서의 동의함 체크박스를 채움."""
    for i in range(1, doc.Paragraphs.Count + 1):
        p = doc.Paragraphs(i)
        text = p.Range.Text.strip().replace('\r', '').replace('\x07', '')

        # 필수/선택/민감정보 항목 모두 동의함 체크
        if '동의함 □' in text and '동의하지 않음 □' in text:
            p.Range.Text = text.replace('동의함 □', '동의함 ■') + '\r'


def export_pdf(doc, pdf_path):
    """Word 문서를 PDF로 내보내기"""
    doc.ExportAsFixedFormat(
        os.path.abspath(pdf_path),
        ExportFormat=17,  # wdExportFormatPDF
    )
    print(f"PDF 저장: {pdf_path}")


def main():
    if not os.path.exists(INPUT_DOC):
        print(f"Error: {INPUT_DOC} not found")
        sys.exit(1)

    profile = load_profile()
    os.makedirs(os.path.dirname(OUTPUT_DOC), exist_ok=True)

    # Word COM 실행
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = False

    try:
        # 원본 복사해서 열기
        import shutil
        shutil.copy2(INPUT_DOC, OUTPUT_DOC)
        doc = word.Documents.Open(os.path.abspath(OUTPUT_DOC))

        print("1/7 지원분야...")
        fill_application_field(doc)

        print("2/7 인적사항...")
        fill_personal_info(doc, profile)
        insert_profile_photo(doc)

        print("3/7 학력사항...")
        fill_education(doc, profile)

        print("4/7 경력사항...")
        fill_career(doc, profile)

        print("5/7 자격증...")
        fill_certifications(doc)

        print("6/7 기타사항...")
        fill_etc(doc, profile)

        print("7/7 자기소개서...")
        fill_self_intro(doc)

        print("날짜/서명...")
        fill_date_signature(doc, profile['personal_info']['name_ko'])
        insert_signature_stamp(doc, profile['personal_info']['name_ko'])
        fill_consent_checks(doc)

        # 저장
        doc.Save()
        print(f"DOC 저장: {OUTPUT_DOC}")

        # PDF 내보내기
        export_pdf(doc, OUTPUT_PDF)

        doc.Close(False)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        word.Quit()


if __name__ == '__main__':
    main()
