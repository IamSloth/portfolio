<system_rules>
1. **Thinking Process**: ALWAYS process logic and reason internally in **English** (for maximum logic density and accuracy).
2. **Output Language**: Translate the final result and communicate ONLY in **Korean**.
3. **Brevity Protocol (Crucial)**:
   - Korean output must be **extremely concise**.
   - NO conversational fillers (e.g., "확인했습니다", "코드를 수정해드리겠습니다", "참고하세요").
   - Use dry, direct endings (e.g., "~함", "~임", or short polite forms like "수정완료").
   - If the answer is code, output **ONLY the code**.
4. **Code Presentation**:
   - NEVER output full files for small changes. ALWAYS use `diff` or `search_and_replace` blocks.
   - Only show relevant lines around the change.
5. **Context Hygiene**:
   - Proactively suggest running `/compact` or `/clear` after completing a logical unit of work.
</system_rules>

## 프로젝트 헌법 (Project Constitution)

> **철칙**: 이 프로젝트는 **문서 아카이빙 + 포트폴리오 데이터 허브**입니다. 자동화 시도는 실패했으며, 수동 관리 체제로 전환되었습니다.

---

### 📂 폴더 구조

```
Job-Application-Pipeline-Desktop/
├── common/                          # 공통 자산 금고
│   ├── photos/                      # 프로필 사진 (profile.png)
│   ├── evidence/                    # 범용 증거 (자격증 등)
│   └── snippets/                    # 재사용 텍스트 블록
├── content/                         # Single Source of Truth
│   ├── profile.json                 # 경력 데이터
│   └── data.json                    # 보조 데이터
├── applications/                    # 기업별 지원 기록 (회사 → 포지션 2단계)
│   └── {company}/                   # 예: kiwoom/, smilegate/
│       └── {position}/              # 예: accounting/, crossfire_test_engineer/
│           ├── {position}_strategy.md  # 메인 허브 (JD 분석 포함)
│           ├── artifacts/           # 증거자료 + 채용공고 원본 (이미지 등)
│           ├── drafts/              # 작업 중간본
│           └── final/              # 최종 제출물
├── templates/                       # 문서 템플릿
│   ├── resumes/
│   └── web/
├── manual/                          # 운영 문서, 회고
│   ├── NARRATIVE_STRATEGY.md
│   ├── CASE_STUDY_{company}.md
│   └── PROJECT_RETROSPECTIVE.md
├── README.md
└── CLAUDE.md
```

---

### 📋 지원 프로세스

```
[1] DISCOVER → [2] ANALYZE → [3] PREPARE → [4] SUBMIT → [5] TRACK → [6] CLOSE
```

| 단계 | 주체 | 설명 | 산출물 |
|------|------|------|--------|
| DISCOVER | 👤 User | 채용공고 발견 | `jd/` |
| ANALYZE | 🤖 Claude | JD 분석, 전략 수립 | `strategy.md` |
| PREPARE | 👥 협업 | 서류 작성 | `drafts/` → `final/` |
| SUBMIT | 👤 User | 제출 | 상태 업데이트 |
| TRACK | 👤→🤖 | 결과 추적 | `strategy.md` 업데이트 |
| CLOSE | 👥 협업 | 회고 | `CASE_STUDY_*.md` |

---

### 🤖 모델 라우팅 (Sub-agent)

Task tool로 서브에이전트 실행 시, 작업 난이도에 따라 모델을 동적 선택한다.

| 모델 | 용도 | 프로세스 단계 |
|------|------|---------------|
| **haiku** ⚡ | 파일/폴더 검색, 구조 검증, 컨벤션 체크, 상태 업데이트 | DISCOVER, TRACK |
| **sonnet** ⚖️ | JD 분석, 전략서 작성, 이력서/자소서 드래프트, 매칭도 분석 | ANALYZE, PREPARE |
| **opus** 🧠 | 최종 품질 리뷰, 약점 포지션 포지셔닝, 면접 시뮬레이션, 회고 분석 | PREPARE(리뷰), CLOSE |

**선택 기준**
- 단순 조회/검증 → haiku (비용↓ 속도↑)
- 창작/분석 → sonnet (기본값)
- 고난도 판단/리뷰 → opus (품질↑)

---

### 📛 파일명 규칙

**기본 원칙**
- 언어: **영문**
- 케이스: **snake_case**
- 날짜: **YYMMDD**
- 버전: **_v1, _v2**

**폴더별 규칙**

| 폴더 | 패턴 | 예시 |
|------|------|------|
| `artifacts/` | `{type}_{desc}.{ext}` | `evidence_scoreboard.png`, `jd_260115.pdf` |
| `drafts/` | `{doctype}_v{n}.{ext}` | `resume_v1.pdf` |
| `final/` | `{doctype}_{YYMMDD}.{ext}` | `application_260127.pdf` |

**Document Types**: `resume`, `coverletter`, `essay`, `application`, `portfolio`

---

### 🏷️ 상태 코드

| 코드 | 이모지 | 설명 |
|------|--------|------|
| DISCOVERED | 📋 | 공고 발견 |
| ANALYZING | 📊 | JD 분석 중 |
| PREPARING | ✍️ | 서류 작성 중 |
| ON_HOLD | ⏸️ | 서류 준비 완료, 제출 보류 (strategy.md에 사유 기록) |
| SUBMITTED | 📤 | 제출 완료 |
| DOC_PASSED | 📬 | 서류 통과 |
| INTERVIEW | 📞 | 면접 진행 |
| FINAL | 🎯 | 최종 면접 |
| ACCEPTED | ✅ | 합격 |
| REJECTED | ❌ | 불합격 |
| ARCHIVED | 🗄️ | 회고 완료 |

---

### 🧠 프로필 실시간 동기화 (Profile Live Sync)

> `content/profile.json`은 지원자의 **Single Source of Truth**이다. Claude는 수석비서로서 지원자를 누구보다 정확히 파악해야 한다.

**원칙**
- 대화 중 새로운 경력·스킬·자격·개인 정보가 확인되면 **즉시** `profile.json`에 반영
- 기존 정보와 충돌 시 User 확인 후 업데이트
- 업데이트 시 `meta.last_updated` 날짜도 갱신
- 반영 후 User에게 변경 사항 간략 보고

---

### 🚫 금지 사항

- **루트 폴더에 MD 파일 난립 금지**: `README.md`와 `CLAUDE.md`만 허용
- **중복 전략 문서 금지**: 한 지원당 하나의 `strategy.md`만
- **자동화 잔재 금지**: `.js`, `.py` 스크립트 파일 생성 금지
- **한글 파일명 금지**: 모든 파일명은 영문 snake_case

---

### 🔗 Quick Reference

| 용도 | 경로 |
|------|------|
| 프로필 사진 | `common/photos/profile.png` |
| 경력 데이터 | `content/profile.json` |
| 셀링 전략 | `manual/NARRATIVE_STRATEGY.md` |
| 기업별 전략 | `applications/{company}/{position}/{position}_strategy.md` |
| 이력서 템플릿 | `templates/resumes/` |
