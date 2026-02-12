"""SK E&S 2개 포지션 이메일 발송 (Gmail SMTP)"""

import argparse
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    import winreg  # Windows-only fallback for persisted user env var
except ImportError:
    winreg = None


GMAIL_USER = "ssujklim@gmail.com"
RECIPIENT = "kje@saraminhs.co.kr"

SK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

EMAILS = [
    {
        "subject": "SK ESG_임종권 (ESG 사무)",
        "body": (
            "안녕하세요.\n"
            "SK ESG 사무 포지션에 지원한 임종권입니다.\n"
            "이력서를 첨부하여 송부드리니 검토 부탁드립니다.\n\n"
            "감사합니다.\n"
            "임종권 드림"
        ),
        "attachment": os.path.join(SK_DIR, "esg_admin", "drafts", "resume_v10.docx"),
        "attach_name": "임종권_이력서.docx",
    },
    {
        "subject": "SK ESG_임종권 (사회공헌 기획/운영)",
        "body": (
            "안녕하세요.\n"
            "SK 사회공헌 기획/운영 포지션에 지원한 임종권입니다.\n"
            "이력서를 첨부하여 송부드리니 검토 부탁드립니다.\n\n"
            "감사합니다.\n"
            "임종권 드림"
        ),
        "attachment": os.path.join(SK_DIR, "csr_planning", "drafts", "resume_v1.docx"),
        "attach_name": "임종권_이력서.docx",
    },
]


def console_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        safe = text.encode("cp949", errors="replace").decode("cp949", errors="replace")
        print(safe)


def get_saved_password():
    # Priority 1: process environment
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if password:
        return password

    # Priority 2 (Windows): HKCU\Environment persisted user variable
    if winreg is not None:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
                value, _ = winreg.QueryValueEx(key, "GMAIL_APP_PASSWORD")
                if value:
                    return value
        except OSError:
            pass

    return None


def send_one(smtp, email_info, recipient):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = recipient
    msg["Subject"] = email_info["subject"]
    msg.attach(MIMEText(email_info["body"], "plain", "utf-8"))

    filepath = email_info["attachment"]
    if not os.path.exists(filepath):
        console_print(f"  ERROR: 첨부파일 없음 -> {filepath}")
        return False

    with open(filepath, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="{email_info["attach_name"]}"',
    )
    msg.attach(part)

    smtp.sendmail(GMAIL_USER, recipient, msg.as_string())
    return True


def main():
    parser = argparse.ArgumentParser(description="SK ESG 이메일 발송")
    parser.add_argument("--password", help="Gmail 앱 비밀번호")
    parser.add_argument("--dry-run", action="store_true", help="미리보기만 수행 (실발송 안함)")
    args = parser.parse_args()

    password = args.password or get_saved_password()
    if not password:
        console_print("ERROR: Gmail password missing. Use --password or set GMAIL_APP_PASSWORD.")
        return

    console_print("=" * 60)
    console_print("SK E&S 이메일 발송 미리보기")
    console_print("=" * 60)

    for i, em in enumerate(EMAILS, 1):
        console_print(f"\n--- 메일 {i} ---")
        console_print(f"  From:    {GMAIL_USER}")
        console_print(f"  To:      {RECIPIENT}")
        console_print(f"  Subject: {em['subject']}")
        console_print(f"  Attach:  {em['attach_name']} ({em['attachment']})")
        exists = os.path.exists(em["attachment"])
        console_print(f"  파일존재: {'OK' if exists else 'ERROR - NOT FOUND'}")
        console_print("  본문:")
        for line in em["body"].splitlines():
            console_print(f"    {line}")

    if args.dry_run:
        console_print("\n[DRY RUN] 발송하지 않음.")
        return

    confirm = input("\n발송하시겠습니까? (y/n): ").strip().lower()
    if confirm != "y":
        console_print("취소됨.")
        return

    console_print("\nGmail SMTP 연결 중...")
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(GMAIL_USER, password)

    for i, em in enumerate(EMAILS, 1):
        console_print(f"\n메일 {i} 발송 중... [{em['subject']}]")
        ok = send_one(smtp, em, RECIPIENT)
        if ok:
            console_print("  [OK] 발송 완료")
        else:
            console_print("  [FAIL] 발송 실패")

    smtp.quit()
    console_print("\n모든 메일 발송 완료.")


if __name__ == "__main__":
    main()
