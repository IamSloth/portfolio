"""
동양미래대학교 합본 PDF 재구성 — JD 서류 순서(가~아)대로 구분 페이지 부착
출력: final/[일학습병행사업] 임종권_지원서류_260303_v2.pdf
"""
import io
import os
from pypdf import PdfWriter, PdfReader
from PIL import Image, ImageDraw, ImageFont

BASE   = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(BASE, "../drafts")
FINAL  = os.path.join(BASE, "../final")

W, H   = 1240, 1754          # A4 @ 150DPI
NAVY   = (31, 55, 100)
YELLOW = (255, 200, 0)
WHITE  = (255, 255, 255)
GRAY   = (200, 200, 200)

HEADER_TEXT = "동양미래대학교 일학습병행사업 관리 및 운영 지원서류"

# ─── 폰트 ────────────────────────────────────────────────────
def load_fonts():
    try:
        return (
            ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 52),
            ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 38),
            ImageFont.truetype("C:/Windows/Fonts/malgun.ttf",   28),
        )
    except Exception:
        d = ImageFont.load_default()
        return d, d, d

F_LABEL, F_TITLE, F_SUB = load_fonts()


def make_section_page(label: str, title: str, subtitle: str = "") -> PdfReader:
    img  = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (W, 12)], fill=YELLOW)
    draw.rectangle([(0, H - 12), (W, H)], fill=YELLOW)

    def cx(text, font):
        bb = draw.textbbox((0, 0), text, font=font)
        return (W - (bb[2] - bb[0])) // 2

    draw.text((cx(HEADER_TEXT, F_SUB), 200), HEADER_TEXT, font=F_SUB, fill=YELLOW)
    draw.text((cx(label, F_LABEL), H // 2 - 90), label, font=F_LABEL, fill=YELLOW)
    draw.text((cx(title, F_TITLE), H // 2 + 10), title, font=F_TITLE, fill=WHITE)
    if subtitle:
        draw.text((cx(subtitle, F_SUB), H // 2 + 100), subtitle, font=F_SUB, fill=GRAY)

    buf = io.BytesIO()
    img.save(buf, format="PDF", resolution=150)
    buf.seek(0)
    return PdfReader(buf)


def img_to_pdf_reader(path: str) -> PdfReader:
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
    # 가로 기준 맞춤
    ratio = W / iw
    nh = int(ih * ratio)
    if nh > H:
        ratio = H / ih
        nw = int(iw * ratio)
        img = img.resize((nw, H), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), WHITE)
        canvas.paste(img, ((W - nw) // 2, 0))
    else:
        img = img.resize((W, nh), Image.LANCZOS)
        canvas = Image.new("RGB", (W, H), WHITE)
        canvas.paste(img, (0, (H - nh) // 2))
    buf = io.BytesIO()
    canvas.save(buf, format="PDF", resolution=150)
    buf.seek(0)
    return PdfReader(buf)


def pdf_range(path: str, start: int, end: int):
    """0-indexed start..end (inclusive)"""
    r = PdfReader(path)
    return [r.pages[i] for i in range(start, end + 1)]


# ─── 소스 경로 ────────────────────────────────────────────────
FORM   = os.path.join(DRAFTS, "[임종권] 지원서식_제출용.pdf")
GRAD_B = os.path.join(DRAFTS, "임종권_학사졸업증명서.pdf")
SCO_B  = os.path.join(DRAFTS, "숭실대학사성적증명서.jpg")
GRAD_M = os.path.join(DRAFTS, "임종권_석사학위수여증명서.pdf")
SCO_M  = os.path.join(DRAFTS, "숭실대석사성적증명서.jpg")
CERT   = os.path.join(DRAFTS, "자격증사본_원본대조필.pdf")
HLTH   = os.path.join(DRAFTS, "건강보험자격득실확인서_임종권.pdf")
OLD    = os.path.join(FINAL,  "[일학습병행사업] 임종권_지원서류_260303.pdf")
OUT    = os.path.join(FINAL,  "[일학습병행사업] 임종권_지원서류_260303_v2.pdf")


def main():
    w = PdfWriter()

    def add_section(label, title, subtitle=""):
        sp = make_section_page(label, title, subtitle)
        w.add_page(sp.pages[0])

    def add_pdf_pages(pages):
        for p in pages:
            w.add_page(p)

    # 가. 이력서 (지원서식 p1~2)
    add_section("가.", "이력서", "이력서 1부 (본교 서식)")
    add_pdf_pages(pdf_range(FORM, 0, 1))

    # 나. 자기소개서 (지원서식 p3~4)
    add_section("나.", "자기소개서", "자기소개서 1부 (본교 서식)")
    add_pdf_pages(pdf_range(FORM, 2, 3))

    # 다. 졸업증명서 및 성적증명서
    add_section("다.", "졸업증명서 및 성적증명서", "석사 이상은 학사 포함")
    add_pdf_pages(PdfReader(GRAD_B).pages)
    w.add_page(img_to_pdf_reader(SCO_B).pages[0])
    add_pdf_pages(PdfReader(GRAD_M).pages)
    w.add_page(img_to_pdf_reader(SCO_M).pages[0])

    # 라. 자격증 사본
    add_section("라.", "자격증 사본", "원본대조필 자필 서명")
    add_pdf_pages(PdfReader(CERT).pages)

    # 마. 경력증명서
    add_section("마.", "경력증명서", "건강보험자격득실확인서")
    add_pdf_pages(PdfReader(HLTH).pages)

    # 사. 주민등록초본 — 기존 합본 마지막 1p 추출
    add_section("사.", "주민등록초본", "병적사항 포함 (남자)")
    old_r = PdfReader(OLD)
    w.add_page(old_r.pages[-1])

    # 아. 개인정보동의서 (지원서식 p5~6)
    add_section("아.", "개인정보 수집·이용·제공 동의서")
    add_pdf_pages(pdf_range(FORM, 4, 5))

    with open(OUT, "wb") as f:
        w.write(f)

    print(f"생성 완료: {OUT}")
    print(f"총 페이지: {len(w.pages)}")


if __name__ == "__main__":
    main()
