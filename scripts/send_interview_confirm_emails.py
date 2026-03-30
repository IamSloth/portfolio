"""
send_interview_confirm_emails.py — 면접확인서 작성 요청 메일 발송
Usage: python -X utf8 scripts/send_interview_confirm_emails.py test
       python -X utf8 scripts/send_interview_confirm_emails.py real
"""
import smtplib
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "..")

GMAIL_USER = "ssujklim@gmail.com"
GMAIL_APP_PW = "byhf kmcf wefr ycoi"
TEST_ADDR = "deathbed0104@naver.com"

EMAILS = [
    {
        "id": "08",
        "company": "화영운수",
        "real_addr": "hwayoungbus@hanmail.net",
        "subject": "경기도 청년 면접수당 면접확인서 작성 요청 (임종권)",
        "body": """안녕하세요, 화영운수(주) 담당자님.

2026년 2월 20일 배차관리직 면접에 응시했던 임종권입니다.

다름이 아니라, 경기도 청년 면접수당 신청을 위해
면접확인서 작성을 부탁드리고자 메일 드립니다.

첨부한 면접확인서 양식에 회사 정보와 담당자 서명을 기재하신 후
회신해 주시면 감사하겠습니다.

바쁘신 중에 번거로운 부탁을 드려 죄송합니다.
감사합니다.

임종권 드림
연락처: 010-4052-0834
""",
        "attachments": [
            {
                "path": os.path.join(BASE_DIR, "applications", "08_hwayoungunsu",
                                     "bus_dispatch_admin", "final",
                                     "면접확인서_화영운수_260220.hwpx"),
                "name": "면접확인서_화영운수_260220.hwpx",
            },
            {
                "path": os.path.join(BASE_DIR, "applications", "08_hwayoungunsu",
                                     "bus_dispatch_admin", "final",
                                     "확인서 pdf.pdf"),
                "name": "면접확인서_화영운수_260220.pdf",
            },
        ],
    },
    {
        "id": "19",
        "company": "서울사회적경제센터",
        "real_addr": "info@sehub.net",
        "cc": "lily01@sehub.net",
        "subject": "경기도 청년 면접수당 면접확인서 작성 요청 (임종권)",
        "body": """안녕하세요, 서울특별시 사회적경제지원센터 담당자님.

2026년 3월 24일 사회적경제 매니저 면접에 응시했던 임종권입니다.

다름이 아니라, 경기도 청년 면접수당 신청을 위해
면접확인서 작성을 부탁드리고자 메일 드립니다.

첨부한 면접확인서 양식에 회사 정보와 담당자 서명을 기재하신 후
회신해 주시면 감사하겠습니다.

바쁘신 중에 번거로운 부탁을 드려 죄송합니다.
감사합니다.

임종권 드림
연락처: 010-4052-0834
""",
        "attachments": [
            {
                "path": os.path.join(BASE_DIR, "applications", "19_seoul_se_center",
                                     "se_manager", "final",
                                     "면접확인서_서울사회적경제센터_260324.hwpx"),
                "name": "면접확인서_서울사회적경제센터_260324.hwpx",
            },
            {
                "path": os.path.join(BASE_DIR, "applications", "19_seoul_se_center",
                                     "se_manager", "final",
                                     "면접확인서pdf.pdf"),
                "name": "면접확인서_서울사회적경제센터_260324.pdf",
            },
        ],
    },
    {
        "id": "16",
        "company": "아이위더스",
        "real_addr": "chc3194@hanmail.net",
        "subject": "경기도 청년 면접수당 면접확인서 작성 요청 (임종권)",
        "body": """안녕하세요, (주)아이위더스 담당자님.

2026년 3월 12일 면접에 응시했던 임종권입니다.

다름이 아니라, 경기도 청년 면접수당 신청을 위해
면접확인서 작성을 부탁드리고자 메일 드립니다.

첨부한 면접확인서 양식에 회사 정보와 담당자 서명을 기재하신 후
회신해 주시면 감사하겠습니다.

바쁘신 중에 번거로운 부탁을 드려 죄송합니다.
감사합니다.

임종권 드림
연락처: 010-4052-0834
""",
        "attachments": [
            {
                "path": os.path.join(BASE_DIR, "applications", "16_ecredible",
                                     "tcb_report", "final",
                                     "면접확인서_아이위더스_260312.hwpx"),
                "name": "면접확인서_아이위더스_260312.hwpx",
            },
            {
                "path": os.path.join(BASE_DIR, "applications", "16_ecredible",
                                     "tcb_report", "final",
                                     "면접확인서 pdf.pdf"),
                "name": "면접확인서_아이위더스_260312.pdf",
            },
        ],
    },
    {
        "id": "09",
        "company": "네오플",
        "real_addr": "hsoli97@neople.co.kr",
        "subject": "채용 진행 현황 문의 및 면접확인서 작성 요청 (임종권)",
        "body": """안녕하세요, 한혜준 담당자님.

2026년 3월 10일 예산관리 직무 면접에 응시했던 임종권입니다.

면접 이후 약 2주가 지나 채용 진행 현황이 궁금하여 여쭤봅니다.
결과 안내 일정이 정해져 있다면 알려주시면 감사하겠습니다.

추가로, 경기도 청년 면접수당 신청을 위해
면접확인서 작성을 부탁드리고자 합니다.
첨부한 양식에 회사 정보와 담당자 서명을 기재하신 후
회신해 주시면 감사하겠습니다.

바쁘신 중에 번거로운 부탁을 드려 죄송합니다.
감사합니다.

임종권 드림
연락처: 010-4052-0834
""",
        "attachments": [
            {
                "path": os.path.join(BASE_DIR, "applications", "09_neople",
                                     "budget_management", "final",
                                     "면접확인서_네오플_260310.hwpx"),
                "name": "면접확인서_네오플_260310.hwpx",
            },
            {
                "path": os.path.join(BASE_DIR, "applications", "09_neople",
                                     "budget_management", "final",
                                     "면접확인서 pdf.pdf"),
                "name": "면접확인서_네오플_260310.pdf",
            },
        ],
    },
]


def send_email(data, to_addr, mode):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = to_addr
    cc = data.get("cc", "")
    if cc:
        msg["Cc"] = cc
    msg["Subject"] = data["subject"]
    msg.attach(MIMEText(data["body"], "plain", "utf-8"))

    for att in data["attachments"]:
        if not os.path.exists(att["path"]):
            print(f"    ⚠ 첨부파일 없음: {att['path']}")
            continue
        with open(att["path"], "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment",
                        filename=("utf-8", "", att["name"]))
        msg.attach(part)

    recipients = [to_addr] + ([cc] if cc else [])
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(GMAIL_USER, GMAIL_APP_PW)
        smtp.sendmail(GMAIL_USER, recipients, msg.as_bytes())

    cc_info = f" (CC: {cc})" if cc else ""
    print(f"  ✓ [{data['id']}] {data['company']} → {to_addr}{cc_info} ({mode})")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "test"

    if mode == "real":
        print("=== REAL: 08,19,16 / TEST: 09(네오플) ===\n")
        for data in EMAILS:
            if data["id"] == "09":
                send_email(data, TEST_ADDR, "test→본인메일")
            else:
                send_email(data, data["real_addr"], "REAL")
    else:
        print("=== TEST MODE → deathbed0104@naver.com ===\n")
        for data in EMAILS:
            send_email(data, TEST_ADDR, "test")

    print(f"\nDone! Sent {len(EMAILS)} emails.")


if __name__ == "__main__":
    main()
