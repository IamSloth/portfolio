"""셀 물리적 위치 정밀 덤프 — 원본 .doc"""
import os, sys, io
import win32com.client

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOC_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'artifacts', '(주)파인스태프_자사양식.doc')
)

# wdInformation constants
wdHorizontalPositionRelativeToPage = 5
wdVerticalPositionRelativeToPage = 6

def inspect(doc_path):
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = False
    try:
        doc = word.Documents.Open(doc_path, ReadOnly=True)

        for t_idx in [1, 3, 4, 5, 6, 7, 8]:  # 전체 테이블
            table = doc.Tables(t_idx)
            rows = table.Rows.Count
            print(f"=== Table {t_idx} (Rows={rows}) ===")

            for r in range(1, rows + 1):
                print(f"\n  Row {r}:")
                for c in range(1, 10):  # 넉넉히
                    try:
                        cell = table.Cell(r, c)
                        rng = cell.Range
                        text = rng.Text.strip().replace('\r','').replace('\x07','').replace('\xa0',' ')
                        # 셀 시작 위치
                        x = rng.Information(wdHorizontalPositionRelativeToPage)
                        y = rng.Information(wdVerticalPositionRelativeToPage)
                        # 셀 너비는 Range 끝 위치와의 차이로 추정
                        w = cell.Width
                        print(f"    C{c}: x={x:.0f} w={w:.0f}pt | '{text[:40]}'")
                    except Exception as e:
                        if 'requested member' not in str(e).lower():
                            pass  # 병합셀

        doc.Close(False)
    finally:
        word.Quit()

if __name__ == '__main__':
    inspect(sys.argv[1] if len(sys.argv) > 1 else DOC_PATH)
