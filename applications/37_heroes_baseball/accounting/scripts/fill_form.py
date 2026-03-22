"""
Fill (주)서울히어로즈_자사양식.docx with:
- 성명: 임종권
- 생년월일: 1992.01.04
- Essay content (essay_v3 content, paragraph-by-paragraph)

Strategy: use the ref essay_v3.docx as the base (it already has name/birthdate/essay),
but rebuild it cleanly from the source docx XML by injecting the same paragraph structure.
"""
import zipfile
import shutil
import os
import re

SRC = r"C:\Users\superjk\Desktop\Job-Application-Pipeline-Desktop\applications\37_heroes_baseball\accounting\artifacts\(주)서울히어로즈_자사양식.docx"
REF = r"C:\Users\superjk\Desktop\Job-Application-Pipeline-Desktop\applications\37_heroes_baseball\accounting\drafts\essay_v3.docx"
OUT = r"C:\Users\superjk\Desktop\Job-Application-Pipeline-Desktop\applications\37_heroes_baseball\accounting\final\essay_260322.docx"

os.makedirs(os.path.dirname(OUT), exist_ok=True)

# Read source document.xml
with zipfile.ZipFile(SRC, 'r') as z:
    src_xml = z.read('word/document.xml').decode('utf-8')

# The source has two blank table cells (성명 cell and 생년월일 cell).
# We need to fill them.

# Pattern for the 2nd <w:tc> (성명 blank cell):
# <w:tc><w:tcPr><w:tcW w:w="2812" ...></w:tcPr><w:p ...><w:pPr>...<w:rPr>...</w:rPr></w:pPr></w:p></w:tc>
# We'll replace the empty paragraph in the 2nd cell with one containing 임종권
# and in the 4th cell with 1992.01.04

# More reliable: use the ref XML which already has everything correct.
# Just copy the ref's document.xml into a new zip built from SRC files.

with zipfile.ZipFile(REF, 'r') as z:
    ref_doc_xml = z.read('word/document.xml').decode('utf-8')

# Write output: copy all files from SRC, but replace word/document.xml with REF's version
shutil.copy2(SRC, OUT)

# Now update document.xml in the output zip
import io

# Read all files from SRC into memory
src_files = {}
with zipfile.ZipFile(SRC, 'r') as z:
    for name in z.namelist():
        src_files[name] = z.read(name)

# Write new zip with replaced document.xml
with zipfile.ZipFile(OUT, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
    for name, data in src_files.items():
        if name == 'word/document.xml':
            zout.writestr(name, ref_doc_xml.encode('utf-8'))
        else:
            zout.writestr(name, data)

print(f"Done: {OUT}")
