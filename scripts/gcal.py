#!/usr/bin/env python3
"""Google Calendar 일정 등록 유틸리티."""
import json, os, sys
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

DIR = os.path.dirname(os.path.abspath(__file__))
CRED = os.path.join(DIR, "google_credentials.json")
TOKEN = os.path.join(DIR, "google_token.json")
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_service():
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CRED, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN, "w") as f:
            f.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def add_event(summary, start, end, description="", location="", color=None):
    """일정 추가. start/end = 'YYYY-MM-DDTHH:MM:SS' 형식.
    color: 1=라벤더, 2=세이지, 3=포도, 4=플라밍고, 5=바나나,
           6=귤, 7=공작, 8=흑연, 9=블루베리, 10=바질, 11=토마토
    """
    service = get_service()
    event = {
        "summary": summary,
        "start": {"dateTime": start, "timeZone": "Asia/Seoul"},
        "end": {"dateTime": end, "timeZone": "Asia/Seoul"},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 1440},   # D-1 (하루 전)
                {"method": "popup", "minutes": 180},     # 3시간 전
                {"method": "popup", "minutes": 60},      # 1시간 전
                {"method": "popup", "minutes": 30},       # 30분 전
            ],
        },
    }
    if description:
        event["description"] = description
    if location:
        event["location"] = location
    if color:
        event["colorId"] = str(color)
    result = service.events().insert(calendarId="primary", body=event).execute()
    print(f"OK: {result.get('htmlLink')}")
    return result


def list_events(max_results=10):
    """다가오는 일정 조회."""
    service = get_service()
    now = datetime.utcnow().isoformat() + "Z"
    result = service.events().list(
        calendarId="primary", timeMin=now,
        maxResults=max_results, singleEvents=True,
        orderBy="startTime"
    ).execute()
    for e in result.get("items", []):
        start = e["start"].get("dateTime", e["start"].get("date"))
        print(f"  {start}  {e['summary']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gcal.py auth | list | add <json>")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "auth":
        get_service()
        print("인증 완료!")
    elif cmd == "list":
        list_events()
    elif cmd == "add" and len(sys.argv) > 2:
        data = json.loads(sys.argv[2])
        add_event(**data)
