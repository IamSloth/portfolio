"""v10.docx → v10.pdf 변환 (win32com)"""
import os
import win32com.client

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INPUT = os.path.join(BASE_DIR, 'drafts', 'resume_v10.docx')
OUTPUT = os.path.join(BASE_DIR, 'drafts', 'resume_v10.pdf')

word = win32com.client.Dispatch('Word.Application')
word.Visible = False
word.DisplayAlerts = False

try:
    doc = word.Documents.Open(os.path.abspath(INPUT))
    doc.ExportAsFixedFormat(os.path.abspath(OUTPUT), ExportFormat=17)
    print(f"PDF 저장: {OUTPUT}")
    doc.Close(False)
finally:
    word.Quit()
