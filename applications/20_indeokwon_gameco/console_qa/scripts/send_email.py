"""
인덕원 콘솔 게임 QA 지원 이메일 발송 (그린맨파워)
사용법: python send_email.py
"""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

GMAIL_USER = "ssujklim@gmail.com"
GMAIL_APP_PW = "byhf kmcf wefr ycoi"

ATTACHMENT_PATH = os.path.join(
    os.path.dirname(__file__),
    "../final/임종권 — 콘솔 게임 QA 지원.pdf"
)
ATTACHMENT_NAME = "임종권_콘솔게임QA_이력서.pdf"

SUBJECT = "[인덕원 콘솔 게임 QA] 임종권 지원합니다"
BODY = """\
김이슬 대리님, 안녕하세요.
인덕원 콘솔 게임 QA 포지션에 지원하는 임종권입니다.

GTA 5, 몬스터헌터 라이즈 등 오픈월드·액션 게임을 즐겨 플레이하는 게이머이며,
이전 직장에서 테스트 시나리오 설계 및 QA 업무를 직접 주도한 경험이 있습니다.
유저로서 조작감에 민감하게 반응하고, QA 전문가로서 이를 체계적으로 분석할 수 있습니다.

이력서를 첨부드리오니 검토 부탁드립니다.
감사합니다.

임종권 드림
010-4052-0834 / ssujklim@gmail.com
"""

TO_REAL = "yiseul69@nate.com"

def send():
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_REAL
    msg["Subject"] = SUBJECT
    msg.attach(MIMEText(BODY, "plain", "utf-8"))

    with open(ATTACHMENT_PATH, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        "attachment",
        filename=("utf-8", "", ATTACHMENT_NAME)
    )
    msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(GMAIL_USER, GMAIL_APP_PW)
        smtp.sendmail(GMAIL_USER, TO_REAL, msg.as_bytes())
    print(f"발송 완료 → {TO_REAL}")

if __name__ == "__main__":
    send()
