"""
한국사회복지사협회 자격관리본부 지원서류 이메일 발송
사용법:
  테스트: python send_email.py test
  실제:   python send_email.py real
"""
import smtplib
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

GMAIL_USER = "ssujklim@gmail.com"
GMAIL_APP_PW = "byhf kmcf wefr ycoi"

ATTACHMENT_PATH = os.path.join(
    os.path.dirname(__file__),
    "../final/(손으로수정)application_form_v1.hwp"
)
ATTACHMENT_NAME = "자격관리본부(단기계약직)_임종권.hwp"

SUBJECT = "자격관리본부(단기계약직)_임종권"
BODY = """안녕하세요, 한국사회복지사협회 채용 담당자님.

자격관리본부 단기계약직(채용 제2026-05호) 채용에 지원하는 임종권입니다.

■ 제출서류
가. 이력서 및 자기소개서 1부 (제공양식)
나. 개인정보 수집·이용 동의서 1부 (제공양식)

검토 부탁드립니다. 감사합니다.

임종권 드림
010-4052-0834 / ssujklim@gmail.com
"""

TO_TEST = "deathbed0104@naver.com"
TO_REAL = "kasw.hr@kasw.or.kr"

def send(to_addr):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to_addr
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
        smtp.sendmail(GMAIL_USER, to_addr, msg.as_bytes())
    print(f"발송 완료 → {to_addr}")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "real":
        send(TO_REAL)
    else:
        send(TO_TEST)
