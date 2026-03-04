"""
함께하는사랑밭 입사지원서 이메일 발송
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
    os.path.dirname(os.path.abspath(__file__)),
    "../final/application_260305.hwp"
)
ATTACHMENT_NAME = "[입사지원] 임종권_입사지원서_260305.hwp"

SUBJECT = "[입사지원] 서울에너지플러스사업 행정·회계 담당자 - 임종권"
BODY = """안녕하세요, 황수빈 팀장님.

서울에너지플러스사업 확대에 따른 행정·회계 및 사업 관리 담당자 채용에 지원하는 임종권입니다.

아래와 같이 지원서류를 첨부드립니다.

  ■ 제출서류
  가. 개인정보처리방침 동의서 및 입사지원서 1부 (자사양식)

검토 부탁드립니다.
감사합니다.

임종권 드림
010-4052-0834
ssujklim@gmail.com
"""

TO_TEST = "deathbed0104@naver.com"
TO_REAL = "sbhwang@withgo.kr"


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
    print(f"✅ 발송 완료 → {to_addr}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"
    if mode == "real":
        send(TO_REAL)
    else:
        send(TO_TEST)
