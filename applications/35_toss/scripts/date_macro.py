"""
토스 채용 폼 날짜 입력 매크로
================================
pip install 불필요 (ctypes stdlib만 사용)

사용법:
  1. python date_macro.py
  2. 메뉴에서 번호 선택
  3. 3초 카운트다운 동안 브라우저 날짜 필드 클릭
  4. 자동 타이핑 시작
"""
import ctypes, time, sys

user32 = ctypes.windll.user32

# ── 키 매핑 ──
VK = {str(i): 0x30 + i for i in range(10)}
VK['.'] = 0xBE
VK['-'] = 0xBD
VK['\t'] = 0x09
KEYEVENTF_UP = 0x0002

def press(vk):
    user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.015)
    user32.keybd_event(vk, 0, KEYEVENTF_UP, 0)
    time.sleep(0.015)

def type_str(text, delay=0.04):
    for ch in text:
        if ch in VK:
            press(VK[ch])
        time.sleep(delay)

def countdown(sec=3):
    for i in range(sec, 0, -1):
        print(f"  {i}...", end=" ", flush=True)
        time.sleep(1)
    print("입력!")

# ── 경력 데이터 ──
COMPANIES = [
    {
        "name": "① 함께만드는세상",
        "title": "총무·IT지원 (대리)",
        "start": "2023.01.09",
        "end":   "2026.02.01",
    },
    {
        "name": "② 맨지온",
        "title": "임베디드 시스템 개발 및 QA (대리)",
        "start": "2020.03.01",
        "end":   "2021.11.20",
    },
    {
        "name": "③ 엣지크로스",
        "title": "H/W 개발 및 자재 관리 (주임)",
        "start": "2016.05.02",
        "end":   "2018.02.02",
    },
]

# ── 개별 값 (년/월/일 분리 입력용) ──
DATES_SPLIT = []
for c in COMPANIES:
    sy, sm, sd = c["start"].split(".")
    ey, em, ed = c["end"].split(".")
    DATES_SPLIT.append({
        "name": c["name"],
        "start_y": sy, "start_m": sm.lstrip("0"), "start_d": sd.lstrip("0"),
        "end_y": ey, "end_m": em.lstrip("0"), "end_d": ed.lstrip("0"),
    })

def menu():
    print("\n" + "="*50)
    print("  토스 채용 폼 날짜 입력 매크로")
    print("="*50)
    print()
    print("── 날짜 통째로 입력 (2023.01.09 형식) ──")
    for i, c in enumerate(COMPANIES):
        print(f"  {i*2+1}. {c['name']} 시작일: {c['start']}")
        print(f"  {i*2+2}. {c['name']} 종료일: {c['end']}")
    print()
    print("── 년/월/일 분리 입력 (캘린더 필드용) ──")
    for i, d in enumerate(DATES_SPLIT):
        print(f"  {7+i}. {d['name']} 시작 → 년({d['start_y']}) 월({d['start_m']}) 일({d['start_d']})")
    print()
    print("── 텍스트 ──")
    for i, c in enumerate(COMPANIES):
        print(f"  {10+i}. {c['name']} 회사명+직무명 연속 입력")
    print()
    print("  0. 종료")
    print()

def run_single(text):
    print(f"\n  → '{text}' 입력 예정")
    print("  브라우저 입력 필드를 클릭하세요!")
    countdown(3)
    type_str(text)
    print("  ✅ 완료\n")

def run_split_start(idx):
    d = DATES_SPLIT[idx]
    parts = [
        (f"시작 년: {d['start_y']}", d["start_y"]),
        (f"시작 월: {d['start_m']}", d["start_m"]),
        (f"시작 일: {d['start_d']}", d["start_d"]),
        (f"종료 년: {d['end_y']}", d["end_y"]),
        (f"종료 월: {d['end_m']}", d["end_m"]),
        (f"종료 일: {d['end_d']}", d["end_d"]),
    ]
    print(f"\n  {d['name']} — 6개 필드 연속 입력")
    for label, val in parts:
        input(f"  [{label}] 필드 클릭 후 Enter → ")
        type_str(val, delay=0.03)
        print(f"    ✅ '{val}' 입력됨")
    print("  ✅ 전체 완료\n")

def run_company_text(idx):
    c = COMPANIES[idx]
    print(f"\n  회사명: {c['name'].split(' ',1)[1]}")
    input("  회사명 필드 클릭 후 Enter → ")
    name = c["name"].split(" ", 1)[1]  # remove ① prefix
    # Can't type Korean with keybd_event, use clipboard
    import subprocess
    subprocess.run(["powershell", "-Command",
        f'Set-Clipboard -Value "{name}"'], capture_output=True)
    print(f"    📋 '{name}' 클립보드 복사됨 → Ctrl+V로 붙여넣기")

    print(f"  직무명: {c['title']}")
    input("  직무명 필드 클릭 후 Enter → ")
    subprocess.run(["powershell", "-Command",
        f'Set-Clipboard -Value "{c["title"]}"'], capture_output=True)
    print(f"    📋 '{c['title']}' 클립보드 복사됨 → Ctrl+V로 붙여넣기")
    print("  ✅ 완료\n")

if __name__ == "__main__":
    while True:
        menu()
        try:
            choice = input("번호 선택: ").strip()
            if choice == "0":
                break
            n = int(choice)
            if 1 <= n <= 6:
                idx = (n - 1) // 2
                is_end = (n - 1) % 2 == 1
                date = COMPANIES[idx]["end"] if is_end else COMPANIES[idx]["start"]
                run_single(date)
            elif 7 <= n <= 9:
                run_split_start(n - 7)
            elif 10 <= n <= 12:
                run_company_text(n - 10)
            else:
                print("  잘못된 번호")
        except (ValueError, KeyboardInterrupt):
            print("\n종료")
            break
