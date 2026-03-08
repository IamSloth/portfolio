"""
서울사회적경제지원센터 매니저 — 합본 PDF 생성
JD 제출서류 순서(가~아) 구분페이지 + 자사양식 + 증빙서류 → PDF 1개
Usage: python merge_pdf.py
"""
import io
import os
from pypdf import PdfWriter, PdfReader
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE, "..")
EVIDENCE = os.path.join(BASE, "..", "..", "..", "..", "common", "evidence")
FINAL = os.path.join(APP_DIR, "final")

W, H = 1240, 1754  # A4 @ 150DPI
NAVY = (31, 55, 100)
YELLOW = (255, 200, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

HEADER_TEXT = "서울특별시 사회적경제지원센터 매니저 지원서류"

# ─── 소스 파일 ──────────────────────────────────────────
FORM = os.path.join(FINAL, "제출용(v3).pdf")
GRAD_M = os.path.join(EVIDENCE, "graduation_cert_master_260303.pdf")
GRAD_B = os.path.join(EVIDENCE, "graduation_cert_bachelor_260303.pdf")
HEALTH = os.path.join(EVIDENCE, "health_insurance_qualification_260220.pdf")
CERT_SW = os.path.join(EVIDENCE, "cert_social_welfare_original.jpg")
CERT_DL = os.path.join(EVIDENCE, "cert_drivers_license_front.jpg")

OUT = os.path.join(FINAL, "application_260308.pdf")


# ─── 폰트 ──────────────────────────────────────────────
def load_fonts():
    try:
        return (
            ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 52),
            ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", 38),
            ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 28),
        )
    except Exception:
        d = ImageFont.load_default()
        return d, d, d


F_LABEL, F_TITLE, F_SUB = load_fonts()


def make_section_page(label, title, subtitle=""):
    img = Image.new("RGB", (W, H), NAVY)
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


def img_to_pdf_reader(path):
    img = Image.open(path).convert("RGB")
    iw, ih = img.size
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


def pdf_range(reader, start, end):
    """0-indexed start..end (inclusive)"""
    return [reader.pages[i] for i in range(start, end + 1)]


def main():
    w = PdfWriter()
    form = PdfReader(FORM)

    def add_section(label, title, subtitle=""):
        sp = make_section_page(label, title, subtitle)
        w.add_page(sp.pages[0])

    # ── 가. 응시원서 (v3 p1~2) ──
    add_section("가.", "응시원서", "응시원서 1부 (자사양식)")
    for p in pdf_range(form, 0, 1):
        w.add_page(p)

    # ── 나. 개인정보 동의서 (v3 p3) ──
    add_section("나.", "개인정보 수집 및 활용 동의서")
    w.add_page(form.pages[2])

    # ── 다. 이력서 (v3 p4) ──
    add_section("다.", "이력서", "이력서 1부 (자사양식)")
    w.add_page(form.pages[3])

    # ── 라. 자기소개서 (v3 p5) ──
    add_section("라.", "자기소개서", "자기소개서 1부 (자사양식)")
    w.add_page(form.pages[4])

    # ── 마. 경력기술서 (v3 p6) ──
    add_section("마.", "경력기술서", "경력기술서 1부 (자사양식)")
    w.add_page(form.pages[5])

    # ── 바. 학위증 ──
    add_section("바.", "학위증", "석사 학위수여증명서 + 학사 졸업증명서")
    for p in PdfReader(GRAD_M).pages:
        w.add_page(p)
    for p in PdfReader(GRAD_B).pages:
        w.add_page(p)

    # ── 사. 경력(재직)증명서 ──
    add_section("사.", "경력(재직)증명서", "건강보험자격득실확인서")
    for p in PdfReader(HEALTH).pages:
        w.add_page(p)

    # ── 아. 자격증 사본 ──
    add_section("아.", "자격증 사본", "사회복지사 1급 + 1종 대형 운전면허")
    w.add_page(img_to_pdf_reader(CERT_SW).pages[0])
    w.add_page(img_to_pdf_reader(CERT_DL).pages[0])

    with open(OUT, "wb") as f:
        w.write(f)

    print(f"생성 완료: {OUT}")
    print(f"총 페이지: {len(w.pages)}")


if __name__ == "__main__":
    main()
