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
├── AI_CONTEXT.md                    # 멀티AI 공동작업 대시보드 (세션 핸드오프)
├── common/                          # 공통 자산 금고
│   ├── photos/                      # 프로필 사진, 프로젝트 이미지
│   ├── evidence/                    # 범용 증거 (자격증 등)
│   └── snippets/                    # 재사용 텍스트 블록 (자소서 문단 등)
├── content/                         # Single Source of Truth
│   ├── profile.json                 # 경력 데이터
│   ├── personal_profile.md          # 개인 성향/커뮤니케이션 가이드
│   └── data.json                    # 보조 데이터 (현재 미사용, 확장용)
├── applications/                    # 기업별 지원 기록 ({NN}_{company} 넘버링)
│   └── {NN}_{company}/              # 예: 01_kiwoom/, 04_smilegate/
│       └── {position}/              # 예: accounting/, crossfire_test_engineer/
│           ├── {company}_{position}_strategy.md  # 메인 허브 (JD 분석 포함)
│           ├── artifacts/           # 증거자료 + 채용공고 원본 (이미지 등)
│           ├── drafts/              # 작업 중간본
│           └── final/               # 최종 제출물
├── docs/                            # 웹 포트폴리오 소스 (→ IamSloth/portfolio로 subtree push)
│   ├── index.html                   # 메인 페이지 (KO/EN 이중언어, 다크모드)
│   ├── style.css                    # 스타일시트
│   ├── lang.js                      # 언어/테마 토글
│   └── assets/                      # 이미지 (profile, projects)
├── vault/                           # 비공개 문서 아카이브 (제출물 백업, public repo 미포함)
│   └── x7k9m2p4/                    # 난독화 경로
├── templates/                       # 문서 템플릿
│   └── resumes/
├── manual/                          # 운영 문서
│   └── NARRATIVE_STRATEGY.md        # 셀링 전략
├── AI_CONTEXT.md                    # 멀티AI 세션 핸드오프 대시보드
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

### ⛔ STOP — 실행 전 필수 체크리스트 (Execution Gate)

> **CRITICAL**: 폴더/파일 생성 전 반드시 아래 항목을 확인하라. 이해했다고 넘어가지 말고, 실제로 체크하라.

```
┌─────────────────────────────────────────────────────────────────┐
│  BEFORE YOU CREATE ANY FILE, VERIFY ALL ITEMS BELOW:            │
├─────────────────────────────────────────────────────────────────┤
│  □ 1. COMPANY NAME CONFIRMED?                                   │
│     - If unknown, ASK USER first. Do NOT guess.                 │
│     - 회사명 불명확 시 User에게 질문. 추측 금지.                   │
│                                                                 │
│  □ 2. FOLDER PATH CORRECT?                                      │
│     - Pattern: applications/{company}/{position}/               │
│     - ❌ WRONG: applications/sports_service/operation/          │
│     - ✅ RIGHT: applications/tving/sports_ops/                  │
│                                                                 │
│  □ 3. STRATEGY.MD FILENAME CORRECT?                             │
│     - Pattern: {company}_{position}_strategy.md                 │
│     - ❌ WRONG: strategy.md, application_strategy.md            │
│     - ✅ RIGHT: tving_sports_ops_strategy.md                    │
│                                                                 │
│  □ 4. STRATEGY.MD HAS ALL 7 SECTIONS?                           │
│     - #1 JD Analysis                                            │
│     - #2 Fit Analysis                                           │
│     - #3 Go/No-Go                                               │
│     - #4 Positioning                                            │
│     - #5 Submission Log                                         │
│     - #6 Timeline                                               │
│     - #7 Interview Prep (add when DOC_PASSED)                   │
│                                                                 │
│  □ 5. JD SAVED TO ARTIFACTS?                                    │
│     - Location: artifacts/jd_YYMMDD.md                          │
│     - 오늘 날짜 기준 YYMMDD 형식                                   │
│                                                                 │
│  □ 6. DEADLINE RECORDED IN TIMELINE?                            │
│     - 마감일을 #6 Timeline 섹션에 반드시 기록                       │
│                                                                 │
│  □ 7. FRONTMATTER COMPLETE?                                     │
│     - company, position, status, discovered, last_updated       │
│     - status 초기값: 📋 DISCOVERED                               │
└─────────────────────────────────────────────────────────────────┘
```

**Common Mistakes to Avoid:**
- ❌ Using job category as company name (e.g., "sports_service" is NOT a company)
- ❌ Creating `strategy.md` without `{company}_{position}_` prefix
- ❌ Skipping JD save step
- ❌ Forgetting deadline in Timeline section
- ❌ Using custom section structure instead of the 7-section template

---

### 📊 ANALYZE 단계 상세 가이드

**Step 1: JD 파싱**
- 필수/우대 요건 분리
- 핵심 키워드 추출 (기술스택, 연차, 도메인)

**Step 2: profile.json ↔ JD 매칭**

| profile.json 필드 | JD 매칭 대상 |
|------------------|-------------|
| `experience[].achievements` | 핵심 업무 요구사항 |
| `skills.technical` | 기술스택/툴 요건 |
| `skills.certifications` | 자격 요건 |
| `education` | 학력/전공 요건 |

**Step 3: 매칭도 평가**
- ⭐⭐⭐: 직접 경험 있음 (증빙 가능)
- ⭐⭐: 유사 경험 있음 (스토리텔링 필요)
- ⭐: 간접 경험만 (약점 방어 필요)
- ✕: 경험 없음 (치명적 갭)

**Step 4: Go/No-Go 판단**
- ✕ 3개 이상 → No-Go 권고 (User 최종 결정)
- ⭐⭐⭐ 핵심 요건 충족 → Go

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

**Document Types**: `resume`, `coverletter`, `essay`, `application`, `portfolio`, `interview_prep`

**Company 폴더 넘버링**
- 채용공고 발견 날짜순으로 `{NN}_{company}` 형식 (01부터 시작)
- 신규 지원 시 마지막 번호 +1 부여
- 예: `01_kiwoom`, `06_sk_energy`, `07_next_company`

**Company/Position 네이밍 규칙**

| 항목 | 규칙 | 예시 |
|------|------|------|
| **Company** | 공식 영문명 소문자, 띄어쓰기→없음 | `kiwoom`, `smilegate`, `11st` |
| **Position** | JD 제목 기준, 2~4단어 snake_case | `accounting`, `backend_developer` |
| **프로젝트 특정** | `{project}_{role}` | `crossfire_test_engineer`, `hope_studio_csr_platform_pm` |
| **그룹사/부서** | 상위 조직 포함 | `smilegate/group_it_procurement` |

**예시 변환:**
- "카카오 백엔드 개발자" → `applications/07_kakao/backend_developer/`
- "네이버 PM" → `applications/08_naver/pm/`
- "스마일게이트 크로스파이어 QA" → `applications/04_smilegate/crossfire_qa/`
- "우아한형제들 QA(Test Engineer)" → `applications/09_woowa/qa_test_engineer/`
- "11번가 총무" → `applications/03_11st/general_affairs/`

---

### 📋 템플릿 레지스트리

> **제출 완료 문서 = 다음 지원의 베이스**

| 문서 유형 | 참조 소스 | 적합 포지션 |
|----------|----------|------------|
| **strategy.md 예시** | `applications/01_kiwoom/accounting/kiwoom_accounting_strategy.md` | 모든 지원 |
| 통합 이력서+자소서 (HTML) | `applications/01_kiwoom/accounting/final/application_260127.html` | 회계/총무/운영직 |
| 포트폴리오 (HTML) | `applications/04_smilegate/hope_studio_csr_platform_pm/final/portfolio_260131.html` | 기획/PM직 |
| **QA/테스트 전략 참조** | `applications/04_smilegate/crossfire_test_engineer/crossfire_test_engineer_strategy.md` | QA/Test Engineer |
| 범용 이력서 템플릿 | `templates/resumes/standard_v1.html` | 기본 베이스 |

**strategy.md 필수 구조:**
```yaml
---
company: {회사명}
position: {포지션명}
status: 📋 DISCOVERED
discovered: YYYY-MM-DD
last_updated: YYYY-MM-DD
---
# 1. 채용공고 분석 (JD Analysis)
# 2. 매칭 분석 (Fit Analysis)
# 3. 지원 판단 (Go/No-Go)
# 4. 지원 컨셉 (Positioning)
# 5. 제출 이력 (Submission Log)
# 6. 진행 상황 (Timeline)
# 7. 면접 준비 (Interview Prep)  ← DOC_PASSED 시 추가
```

**참조 원칙**: 유사 포지션의 `final/` 먼저 확인 → 없으면 `templates/`

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

### 📞 면접 준비 워크플로우 (DOC_PASSED 이후)

**트리거**: status가 `📬 DOC_PASSED`로 변경 시

**Step 1: 면접 준비 문서 생성**
- 위치: `drafts/interview_prep_v1.md`
- 필수 구조:
  ```
  # 면접 방어 전략
  ## 1. 🛡️ 약점 방어 (Defense Logic)
  - 예상 약점 리스트 (경력 공백, 경험 부족, 직무 전환 등)
  - 각 약점에 대한 방어 로직 (인정 → 전환 → 근거)

  ## 2. ⚔️ 필살기 (Attack Logic)
  - 핵심 경험 에피소드 2~3개 (STAR 기법)
  - "Why Me?" 차별점 (경쟁자 대비)
  - 면접관 주도권 가져오는 역질문

  ## 3. 💊 긴급 처방 (윽엑 방지)
  - 모르는 질문 대응 템플릿 ("잠시만요, 정리해서...")
  - 예상 질문 10~20개 + 핵심 답변 키워드
  ```

**Step 2: 모의 면접 (선택)**
- 모델: opus (고난도 판단)
- 방식: Claude가 면접관 역할 수행
- User 요청 시 실행 (자동 트리거 X)

**Step 3: strategy.md #7 기록**
- 면접 일정/형식 (1차 실무, 2차 임원 등)
- 핵심 대비 포인트 요약 (1~3줄)
- 모의 면접 결과 (실행한 경우)

**Step 4: 최종 점검 (면접 D-1)**
- 면접 당일 확인용 1페이지 요약 생성

---

### 🧠 프로필 실시간 동기화 (Profile Live Sync)

> `content/profile.json`은 지원자의 **Single Source of Truth**이다. Claude는 수석비서로서 지원자를 누구보다 정확히 파악해야 한다.

**profile.json 구조:**
```json
{
  "meta": { "version", "last_updated" },
  "personal_info": { "name_ko", "email", "phone", "address", "birthdate" },
  "education": [{ "school", "major", "degree", "date" }],
  "experience": [{ "company", "department", "role", "period", "achievements" }],
  "skills": { "technical", "certifications", "languages" }
}
```

**원칙**
- 대화 중 새로운 경력·스킬·자격·개인 정보가 확인되면 **즉시** `profile.json`에 반영
- 기존 정보와 충돌 시 User 확인 후 업데이트
- 업데이트 시 `meta.last_updated` 날짜도 갱신
- 반영 후 User에게 변경 사항 간략 보고

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
| 경력 데이터 | `content/profile.json` |
| **개인 프로필** | `content/personal_profile.md` |
| 셀링 전략 | `manual/NARRATIVE_STRATEGY.md` |
| 기업별 전략 | `applications/{company}/{position}/{company}_{position}_strategy.md` |
| 이력서 템플릿 | `templates/resumes/` |
