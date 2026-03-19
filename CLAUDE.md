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
├── AI_CONTEXT.md          # 세션 핸드오프 대시보드 (필수 읽기)
├── content/profile.json   # 경력 Single Source of Truth
├── content/personal_profile.md
├── applications/{NN}_{company}/{position}/
│   ├── {company}_{position}_strategy.md
│   ├── artifacts/  drafts/  final/
├── docs/                  # 웹 포트폴리오 (→ IamSloth/portfolio subtree)
├── common/photos|evidence|snippets/
├── vault/                 # 비공개 아카이브
├── templates/resumes/
└── manual/NARRATIVE_STRATEGY.md
```

---

### 📋 지원 프로세스

```
[1] DISCOVER → [2] ANALYZE → [3] PREPARE → [4] SUBMIT → [5] TRACK → [6] CLOSE
```

| 단계 | 주체 | 설명 | 산출물 |
|------|------|------|--------|
| DISCOVER | 👤 User | 채용공고 발견 | `artifacts/` |
| ANALYZE | 🤖 Claude | JD 분석, 전략 수립 | `strategy.md` |
| PREPARE | 👥 협업 | 서류 작성 | `drafts/` → `final/` |
| SUBMIT | 👤 User | 제출 | 상태 업데이트 |
| TRACK | 👤→🤖 | 결과 추적 | `strategy.md` 업데이트 |
| CLOSE | 👥 협업 | 회고 | `strategy.md` #7 |

### 🆕 신규 지원 시작 워크플로우

1. **폴더 생성**: `applications/{NN}_{company}/{position}/` (다음 번호: AI_CONTEXT.md 참조)
2. **전략 문서 생성**: `{company}_{position}_strategy.md` (status: DISCOVERED)
3. **JD 저장**: `artifacts/jd_YYMMDD.md` 또는 `.pdf`
4. **템플릿 선택**: 템플릿 레지스트리에서 유사 포지션 참조
5. **작업 시작**: 참조 문서 복사 → `drafts/{doctype}_v1.html`
6. **반복**: v1 → v2 → ... → 완성 시 `final/{doctype}_{YYMMDD}.html`로 이동

### ⛔ Execution Gate — 파일 생성 전 필수 체크

> **CRITICAL**: 회사명 불명확 시 추측 금지 → User에게 질문.

1. 🚫 회사명 추측 금지 → 확인 후 `applications/{NN}_{company}/{position}/` 생성
2. 🚫 `strategy.md` 단독 파일명 금지 → `{company}_{position}_strategy.md` 필수
3. 🚫 7섹션 누락 금지 → #1 JD ~ #7 Interview Prep 전부 포함
4. 🚫 JD 미저장 금지 → `artifacts/jd_YYMMDD.md`
5. 🚫 마감일 누락 금지 → #6 Timeline에 기록
6. 🚫 frontmatter 누락 금지 → company, position, status(📋 DISCOVERED), discovered, last_updated

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

### 📛 파일명 + 상태 코드

> 상세 규칙은 `.claude/rules/naming-conventions.md`에 분리됨 (applications/** 작업 시 자동 로드)

- 영문 snake_case, 날짜 YYMMDD, 버전 _v1/_v2
- 제출용 PDF만 한국어: `임종권_지원서_{회사명}.pdf`
- Company 넘버링: `{NN}_{company}` (AI_CONTEXT.md에서 다음 번호 확인)

### 📂 분산 규칙 (.claude/rules/)

> 아래 가이드는 `.claude/rules/`에 분리됨 — 관련 파일 작업 시 자동 로드.

| 규칙 파일 | 내용 | 로드 조건 |
|----------|------|----------|
| `naming-conventions.md` | 파일명 규칙 + 상태 코드 | `applications/**` |
| `analyze-guide.md` | ANALYZE 상세 가이드 + 템플릿 레지스트리 | `applications/**/*strategy*.md` |
| `interview-prep.md` | 면접 준비 워크플로우 | `applications/**/drafts/interview_prep*.md` |
| `profile-sync.md` | profile.json 동기화 규칙 | `content/profile.json` |

---

### 🚫 금지 사항

- **루트 폴더에 MD 파일 난립 금지**: `README.md`, `CLAUDE.md`, `AI_CONTEXT.md`만 허용
- **중복 전략 문서 금지**: 한 지원당 하나의 `strategy.md`만
- **자동화 잔재 금지**: 루트에 `.js`, `.py` 파일 생성 금지
- **한글 파일명 금지**: 모든 파일명은 영문 snake_case

---

### 🤝 멀티 AI 공동작업 프로토콜

> 이 프로젝트는 여러 AI 에이전트가 교대로 작업함 (Opus, Sonnet, 기타).

- `AI_CONTEXT.md` (루트): **전체 현황 대시보드**. 세션 시작/종료 시 필독/갱신.
- `{company}_{position}_strategy.md` 핸드오프 섹션: 지원건별 상세 컨텍스트.
- **세션 종료 시**: AI_CONTEXT.md 업데이트 → git commit → push
- 커밋 `Co-Authored-By`로 어떤 AI가 작업했는지 추적

---

### 🚀 세션 시작 체크리스트

> **토큰 절약**: 아래 파일들을 먼저 읽으면 탐색 시간 대폭 절약

**매 세션 시작 시 필수 참조:**
1. `AI_CONTEXT.md` — 직전 세션 요약, 활성 작업 현황 (최우선 읽기)
2. `content/profile.json` — 경력 데이터 (Single Source of Truth)
3. `content/personal_profile.md` — 개인 성향, 커뮤니케이션 가이드 (ISFP, 간섭 싫어함)
4. `manual/NARRATIVE_STRATEGY.md` — 셀링 전략, "Why Him?"
5. 현재 지원 현황: `AI_CONTEXT.md`의 활성 지원 현황 테이블 참조

---

### 🔗 Quick Reference

| 용도 | 경로 |
|------|------|
| 프로필 사진 | `common/photos/profile.png` |
| 서명 이미지 | `common/photos/signature.png` |
| 경력 데이터 | `content/profile.json` |
| **개인 프로필** | `content/personal_profile.md` |
| 셀링 전략 | `manual/NARRATIVE_STRATEGY.md` |
| 기업별 전략 | `applications/{company}/{position}/{company}_{position}_strategy.md` |
| 이력서 템플릿 | `templates/resumes/` |
