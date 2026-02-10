# DOC Form Automation Guide (Kolon Energy Edu)

## Scope
- Template: `artifacts/(주)파인스태프_자사양식.doc`
- Script: `scripts/fill_doc.py`
- Output:
  - Draft: `drafts/resume_v7.doc`, `drafts/resume_v7.pdf`
  - Final: `final/resume_260210.doc`, `final/resume_260210.pdf`

## Run
```powershell
python applications/07_kolon/energy_edu_ops/scripts/fill_doc.py
```

## Prerequisites
- Windows + Microsoft Word installed
- Python packages:
  - `pywin32`
  - `Pillow` (photo crop + fallback seal generation)

## Fixed Rules (Do Not Break)
1. `.doc` 템플릿은 `python-docx` 금지, `win32com`만 사용.
2. 셀 입력 기본 폰트는 `굴림체` 사용.
3. 학력표(`Table 4`)는 `AllowAutoFit=False` 고정.
4. 사진은 `Table 2` 셀(1,1)에 삽입.
5. 서명은 성명 줄 끝에 도장 이미지 삽입.
6. 동의서 체크박스는 `동의함 □` → `동의함 ■` 치환.

## Assets Used
- Profile photo: `common/photos/profile.png` (fallback: `docs/assets/profile.png`)
- Seal stamp: `applications/01_kiwoom/accounting/artifacts/seal_stamp.png`
- Fallback seal auto-generation when stamp file is missing

## Common Failure Patterns and Fixes
- 증상: 학력표/인적표 좌측 잘림
  - 원인: 글꼴 강제 변경, 표 AutoFit 흔들림
  - 조치: `굴림체` 유지 + `Table 4 AllowAutoFit=False`

- 증상: 페이지가 4페이지로 늘어남
  - 원인: 자기소개서 셀 텍스트 과다
  - 조치: `Table 8` 텍스트 압축 + 8pt 유지

- 증상: `WinError 32` 파일 잠김
  - 원인: Word 프로세스가 문서를 점유
  - 조치: `WINWORD` 종료 후 재실행

## Clean Workspace Policy
- `drafts/`에는 검토 대상 버전만 유지 (현재 `resume_v7.*`)
- 실험 산출물(`_exp`, `_pdf_preview_*`, `_stage_diag`, `_pi_diag`)은 커밋 금지
- 임시 잠금파일(`~$*.doc`)은 즉시 삭제
