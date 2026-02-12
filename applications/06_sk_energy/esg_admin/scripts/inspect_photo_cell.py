"""사진 셀 구조 확인"""
import os
from docx import Document
from docx.oxml.ns import qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT = os.path.join(BASE_DIR, 'drafts', 'resume_v9.docx')

doc = Document(INPUT)
t = doc.tables[0]

print(f"Table 0: {len(t.rows)} rows x {len(t.columns)} cols")
print()

# 첫 몇 행의 셀 구조 확인
for r_idx in range(min(8, len(t.rows))):
    row = t.rows[r_idx]
    tr = row._tr
    trPr = tr.find(qn('w:trPr'))
    h_val = None
    if trPr is not None:
        trH = trPr.find(qn('w:trHeight'))
        if trH is not None:
            h_val = trH.get(qn('w:val'))

    cells_info = []
    for c_idx, cell in enumerate(row.cells):
        tc = cell._tc
        tcPr = tc.tcPr
        w_val = None
        vmerge = None
        gridSpan = None
        if tcPr is not None:
            tcW = tcPr.find(qn('w:tcW'))
            if tcW is not None:
                w_val = tcW.get(qn('w:w'))
            vm = tcPr.find(qn('w:vMerge'))
            if vm is not None:
                vmerge = vm.get(qn('w:val'), 'continue')
            gs = tcPr.find(qn('w:gridSpan'))
            if gs is not None:
                gridSpan = gs.get(qn('w:val'))

        text = cell.text[:20].replace('\n', ' ').strip()
        merge_str = f" vMerge={vmerge}" if vmerge else ""
        span_str = f" span={gridSpan}" if gridSpan else ""
        cells_info.append(f"C{c_idx}(w={w_val}{merge_str}{span_str})[{text}]")

    print(f"R{r_idx} (h={h_val}): {' | '.join(cells_info)}")
