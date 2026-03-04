"""
동양미래대학교 지원서류 이메일 발송
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
    "../final/[일학습병행사업] 임종권_지원서류_260303_v2.pdf"
)
ATTACHMENT_NAME = "[일학습병행사업] 임종권_지원서류_260303.pdf"

SUBJECT = "[지원서류 제출] 일학습병행사업 관리 및 운영 지원 — 임종권"
BODY = """안녕하세요. 동양미래대학교 사무처 총무팀 담당자님,

이번 일학습병행사업 관리 및 운영 계약직 일반직원 채용에 지원하게 된 임종권입니다.

아래와 같이 지원서류를 PDF 1개 파일로 합산하여 첨부 드립니다.

  ■ 제출서류
  가. 이력서 1부 (본교 서식)
  나. 자기소개서 1부 (본교 서식)
  다. 졸업증명서 및 성적증명서 각 1부 (학사·석사)
  라. 자격증 사본 1부 (원본대조필)
  마. 경력증명서 1부 (건강보험자격득실확인서)
  사. 주민등록초본 1부 (병적사항 포함)
  아. 개인정보 수집·이용·제공 동의서 1부

검토에 불편함이 없도록 서류를 구성하였습니다.
귀한 기회를 주셔서 감사드리며, 좋은 결과를 기대하겠습니다.

감사합니다.

임종권 드림
010-4052-0834
ssujklim@gmail.com
"""

TO_TEST = "deathbed0104@naver.com"
TO_REAL  = "eusung@dongyang.ac.kr"

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
