"""파인스태프 자사양식 .doc 구조 탐색 (win32com)"""
import os
import sys
import io
import win32com.client

# Windows cp949 콘솔 인코딩 이슈 방지
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOC_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'artifacts', '(주)파인스태프_자사양식.doc')
)


def inspect(doc_path):
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = False

    try:
        doc = word.Documents.Open(doc_path, ReadOnly=True)

        # 기본 정보
        print(f"=== Document: {os.path.basename(doc_path)} ===")
        print(f"Tables: {doc.Tables.Count}")
        print(f"Paragraphs: {doc.Paragraphs.Count}")
        print()

        # 각 테이블 구조 덤프
        for t_idx in range(1, doc.Tables.Count + 1):
            table = doc.Tables(t_idx)
            rows = table.Rows.Count
            cols = table.Columns.Count
            print(f"[Table {t_idx}] Rows={rows}, Cols={cols}")

            for r in range(1, rows + 1):
                row_data = []
                for c in range(1, cols + 1):
                    try:
                        cell = table.Cell(r, c)
                        text = cell.Range.Text.strip().replace('\r', '').replace('\x07', '').replace('\xa0', ' ')
                        display = text[:30] if text else '(empty)'
                        row_data.append(f"[{c}]={display}")
                    except Exception:
                        row_data.append(f"[{c}]=MERGED")
                print(f"  R{r}: {' | '.join(row_data)}")
            print()

        # 본문 단락 (테이블 밖)
        print("=== Paragraphs (outside tables) ===")
        for i, p in enumerate(doc.Paragraphs):
            text = p.Range.Text.strip().replace('\r', '').replace('\x07', '').replace('\xa0', ' ')
            if text and len(text) > 1:
                print(f"  P{i+1}: '{text[:80]}'")

        doc.Close(False)
    finally:
        word.Quit()


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else DOC_PATH
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)
    inspect(path)
