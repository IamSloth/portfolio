"""화영운수 2차 면접 서류 이메일 답장 (Gmail SMTP)"""

import argparse
import os
import smtplib
import sys
import io
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

try:
    import winreg
except ImportError:
    winreg = None

# Force UTF-8 stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

GMAIL_USER = "ssujklim@gmail.com"
RECIPIENT = "hwayoungbus@hanmail.net"

# Reply headers
ORIGINAL_SUBJECT = "화영운수(주) 2차 면접 시 준비서류 안내드립니다."
ORIGINAL_MSG_ID = "<20260220130306.aqh0wLgxQ8uImyjvY4fGfg@hwayoungbus.hanmail.net>"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FINAL_DIR = os.path.join(BASE_DIR, "final")

REPLY_SUBJECT = f"Re: {ORIGINAL_SUBJECT}"
REPLY_BODY = (
    "안녕하세요, 배차관리직에 지원한 임종권입니다.\n"
    "안내해 주신 서류 첨부하여 회신드립니다.\n\n"
    "1. 자사 이력서·자기소개서 (HWP)\n"
    "2. 주민등록등본 (주민번호 미공개)\n"
    "3. 건강보험 자격득실확인원\n"
    "※ 2, 3번은 사람인 지원 시 제출드렸으나, 혹시 몰라 다시 첨부드립니다.\n\n"
    "월요일(2/23) 오전 11시 20분까지 도착하겠습니다.\n"
    "면접 기회를 주셔서 감사합니다.\n\n"
    "임종권 드림"
)

ATTACHMENTS = [
    {
        "path": os.path.join(FINAL_DIR, "1. 화영운수_이력서,자기소개서_임종권_260220.hwp"),
        "name": "1. 화영운수_이력서,자기소개서_임종권.hwp",
    },
    {
        "path": os.path.join(FINAL_DIR, "임종권_주민등록등본_주민번호미공개_260220.pdf"),
        "name": "임종권_주민등록등본.pdf",
    },
    {
        "path": os.path.join(FINAL_DIR, "임종권_건강보험자격득실확인원_260220.pdf"),
        "name": "임종권_건강보험자격득실확인원.pdf",
    },
]


def get_password():
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if password:
        return password
    if winreg is not None:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
                value, _ = winreg.QueryValueEx(key, "GMAIL_APP_PASSWORD")
                if value:
                    return value
        except OSError:
            pass
    return None


def main():
    parser = argparse.ArgumentParser(description="화영운수 답장 이메일 발송")
    parser.add_argument("--password", help="Gmail 앱 비밀번호")
    parser.add_argument("--dry-run", action="store_true", help="미리보기만 (실발송 안함)")
    args = parser.parse_args()

    password = args.password or get_password()
    if not password:
        print("ERROR: Gmail password missing. Use --password or set GMAIL_APP_PASSWORD.")
        return

    # Preview
    print("=" * 60)
    print("화영운수 답장 이메일 미리보기")
    print("=" * 60)
    print(f"  From:       {GMAIL_USER}")
    print(f"  To:         {RECIPIENT}")
    print(f"  Subject:    {REPLY_SUBJECT}")
    print(f"  In-Reply-To: {ORIGINAL_MSG_ID}")
    print()
    print("  본문:")
    for line in REPLY_BODY.splitlines():
        print(f"    {line}")
    print()
    print("  첨부파일:")
    all_ok = True
    for att in ATTACHMENTS:
        exists = os.path.exists(att["path"])
        status = "OK" if exists else "NOT FOUND"
        size = ""
        if exists:
            size_kb = os.path.getsize(att["path"]) / 1024
            size = f" ({size_kb:.1f}KB)"
        print(f"    [{status}] {att['name']}{size}")
        if not exists:
            all_ok = False

    if not all_ok:
        print("\nERROR: 일부 첨부파일이 없음. 발송 중단.")
        return

    if args.dry_run:
        print("\n[DRY RUN] 발송하지 않음.")
        return

    confirm = input("\n발송하시겠습니까? (y/n): ").strip().lower()
    if confirm != "y":
        print("취소됨.")
        return

    # Build message
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = RECIPIENT
    msg["Subject"] = REPLY_SUBJECT
    msg["In-Reply-To"] = ORIGINAL_MSG_ID
    msg["References"] = ORIGINAL_MSG_ID
    msg.attach(MIMEText(REPLY_BODY, "plain", "utf-8"))

    for att in ATTACHMENTS:
        with open(att["path"], "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        # Use keyword arg so Python handles RFC 2231 encoding for Korean filenames
        part.add_header(
            "Content-Disposition",
            "attachment",
            filename=("utf-8", "", att["name"]),
        )
        msg.attach(part)

    # Send
    print("\nGmail SMTP 연결 중...")
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(GMAIL_USER, password)
    smtp.sendmail(GMAIL_USER, RECIPIENT, msg.as_string())
    smtp.quit()
    print("[OK] 답장 발송 완료!")


if __name__ == "__main__":
    main()
