# Lim-System: Job Application Pipeline & Portfolio Hub

> **AI Agent?** → `AI_CONTEXT.md` 먼저 읽고, `CLAUDE.md` 읽으세요. 그게 전부입니다.

취업 지원 전 과정을 관리하는 **커리어 운영 본부**입니다.
경력 데이터 관리, 기업별 맞춤 지원 전략 아카이빙, 그리고 웹 포트폴리오까지 하나의 레포에서 운영합니다.

---

## Architecture

이 프로젝트는 **듀얼 레포 구조**로 운영됩니다.

```
┌─────────────────────────────────────────────────────────────────┐
│  IamSloth/Job-Application-Pipeline  (Private)                   │
│                                                                 │
│  applications/  ← 기업별 지원 전략 + 서류                       │
│  content/       ← profile.json (Single Source of Truth)         │
│  common/        ← 공통 자산 (사진, 증빙, 텍스트 블록)            │
│  manual/        ← 운영 문서 (셀링 전략 등)                       │
│  templates/     ← 문서 템플릿                                    │
│  vault/         ← 비공개 문서 아카이브 (제출물 백업)              │
│                                                                 │
│  docs/ ──── subtree push ────→  IamSloth/portfolio  (Public)    │
│    ├ index.html                 GitHub Pages 배포                │
│    ├ style.css                  https://iamsloth.github.io/portfolio/
│    ├ lang.js                                                    │
│    └ assets/                                                    │
└─────────────────────────────────────────────────────────────────┘
```

| 레포 | 공개 | 용도 |
|------|------|------|
| `IamSloth/Job-Application-Pipeline` | Private | 전체 파이프라인 (전략, 서류, 데이터, 포트폴리오 소스) |
| `IamSloth/portfolio` | Public | 웹 포트폴리오 배포 전용 (GitHub Pages) |

**핵심 규칙**: `vault/`과 개인정보(전화번호, 주소 등)는 **절대** public repo에 포함되지 않습니다.

---

## Project Structure

```text
Job-Application-Pipeline-Desktop/
├── AI_CONTEXT.md                    # [Handoff] 멀티AI 세션 대시보드
├── CLAUDE.md                        # [Rules] AI 협업 규칙 (헌법)
├── common/                          # [Shared Assets] 공통 자산 금고
│   ├── photos/                      # 프로필 사진, 프로젝트 이미지
│   ├── evidence/                    # 범용 증거 (자격증 등)
│   └── snippets/                    # 재사용 텍스트 블록
├── content/                         # [Data Source] 경력 데이터
│   ├── profile.json                 # Source of Truth (DB 역할)
│   ├── personal_profile.md          # 개인 성향/커뮤니케이션 가이드
│   └── data.json                    # 보조 데이터 (미사용)
├── applications/                    # [Archive] 기업별 지원 기록 ({NN}_{company}/ 넘버링)
│   └── {NN}_{company}/{position}/   # 예: 01_seoul_heroes/accounting/
│       ├── {company}_{position}_strategy.md
│       ├── artifacts/               # 증거자료 + 채용공고 원본
│       ├── drafts/                  # 작업 중간본
│       └── final/                   # 최종 제출물
├── docs/                            # [Portfolio] 웹 포트폴리오 소스
│   ├── index.html                   # 메인 페이지 (KO/EN 이중언어)
│   ├── style.css                    # 스타일 (다크모드 포함)
│   ├── lang.js                      # 언어/테마 토글
│   └── assets/                      # 이미지 (profile, projects)
├── vault/                           # [Vault] 비공개 문서 아카이브
│   └── x7k9m2p4/                    # 제출물 백업 (PDF, HTML)
├── templates/                       # [Renderer] 문서 템플릿
│   └── resumes/
├── manual/                          # [Operations] 운영 문서
│   └── NARRATIVE_STRATEGY.md
└── README.md                        # 이 문서
```

---

## Portfolio Deployment

### 배포 URL
**https://iamsloth.github.io/portfolio/**

### 기술 스택
- 순수 HTML/CSS/JS (빌드 도구 없음)
- KO/EN 이중언어 토글
- 라이트/다크 모드 토글
- Pretendard 웹폰트
- 반응형 + 인쇄 최적화

### 포트폴리오 수정 → 배포 워크플로우

```
1. docs/ 파일 수정 (이 private repo에서 작업)
2. private repo에 commit & push
3. public repo로 동기화:
   git subtree push --prefix=docs portfolio main
4. GitHub Pages 자동 빌드 (1~2분 소요)
5. 배포 확인: https://iamsloth.github.io/portfolio/
```

### 초기 설정 (최초 1회)

```bash
# portfolio 리모트 추가
git remote add portfolio https://github.com/IamSloth/portfolio.git
```

### 주의사항
- `vault/`은 `docs/` 밖에 있으므로 subtree push에서 **자동 제외**됨
- `docs/` 안에 개인정보(전화번호, 주소) 포함 금지
- subtree push는 `docs/` 내부만 전송 → public repo에 다른 폴더 노출 없음

---

## Vault (비공개 아카이브)

어디서든 제출물에 접근할 수 있는 비공개 백업 공간입니다.

- **위치**: `vault/x7k9m2p4/`
- **접근 방법**: GitHub 웹에서 직접 열람 또는 로컬 클론
- **public repo에 미포함** (docs/ 밖에 위치하므로)

### 파일 추가 방법
```
1. final/ 폴더의 완성 파일을 vault/x7k9m2p4/에 복사
2. vault/x7k9m2p4/index.html에 링크 추가
3. commit & push (private repo만)
```

---

## Application Process

```
[1] DISCOVER → [2] ANALYZE → [3] PREPARE → [4] SUBMIT → [5] TRACK → [6] CLOSE
    👤 User      🤖 Claude     👥 협업       👤 User     👤→🤖       👥 협업
```

각 단계의 상세 가이드는 `CLAUDE.md`를 참조하세요.

---

## Current Applications

| # | Company | Position | Status | Folder |
|---|---------|----------|--------|--------|
| 06 | SK에너지 | ESG 사무 | ✍️ PREPARING | `06_sk_energy/esg_admin/` |
| 05 | 시니어금융교육협의회 | CSR Ops | 📤 SUBMITTED | `05_sfec/csr_ops/` |
| 04 | 스마일게이트 희망스튜디오 | CSR 플랫폼 PM | 📤 SUBMITTED | `04_smilegate/hope_studio_csr_platform_pm/` |
| 03 | 11번가 | 총무 | ⏸️ ON_HOLD | `03_11st/general_affairs/` |
| 02 | 시프트업 | 자산담당 | 🗄️ ARCHIVED | `02_shiftup/asset/` |
| 01 | 서울히어로즈 | 회계담당 | 📤 SUBMITTED | `01_seoul_heroes/accounting/` |
| 04 | 스마일게이트 | 그룹IT구매 | ❌ REJECTED | `04_smilegate/group_it_procurement/` |
| 04 | 스마일게이트 | 협업툴운영 | 🗄️ ARCHIVED | `04_smilegate/collaboration_tools_ops/` |
| 04 | 스마일게이트 | 크로스파이어 QA | 🗄️ ARCHIVED | `04_smilegate/crossfire_test_engineer/` |
| 04 | 캣파크뮤지엄 | 테마파크 운영지원 | 🗄️ ARCHIVED | `04_smilegate/catparkmuseum_themepark_ops_support/` |

---

## Naming Convention

- **언어**: 영문 only
- **케이스**: snake_case
- **날짜**: YYMMDD (예: 260127)
- **버전**: _v1, _v2

---

## Key Principles

1. **Single Source of Truth**: 모든 경력 정보는 `content/profile.json` 하나로 통제
2. **One Source Multi-Use**: 포트폴리오 웹은 범용 — 모든 지원에 공통 사용
3. **Dual Repo Safety**: 개인정보와 전략 문서는 private repo에만 존재
4. **Strategic Archiving**: 기업별 지원 전략과 결과를 `strategy.md`로 기록

---

**Powered by Claude (AI Pair Programming)**
