# 🚀 Lim-System: Job Application Pipeline & Portfolio Hub

이 프로젝트는 **임종권(Lim Jong Kwon)** 님의 커리어 데이터를 관리하고, 기업별 맞춤형 지원 전략을 아카이빙하며, 차후 포트폴리오 웹사이트의 데이터 소스로 활용되는 **커리어 운영 본부**입니다.

## 📂 Project Structure

```text
Job-Application-Pipeline-Desktop/
├── 📂 common/                       # [Shared Assets] 공통 자산 금고
│   ├── 📂 photos/                   # 프로필 사진
│   ├── 📂 evidence/                 # 범용 증거 (자격증 등)
│   └── 📂 snippets/                 # 재사용 텍스트 블록
├── 📂 content/                      # [Data Source] 경력 데이터
│   ├── 📄 profile.json              # Source of Truth (DB 역할)
│   └── 📄 data.json                 # 기타 보조 데이터
├── 📂 applications/                 # [Archive] 기업별 지원 기록
│   └── 📂 {company}_{position}/     # 예: kiwoom_accounting/
│       ├── 📄 {company}_{position}_strategy.md
│       ├── 📂 jd/                   # 채용공고 원본
│       ├── 📂 artifacts/            # 회사별 증거자료
│       ├── 📂 drafts/               # 작업 중간본
│       └── 📂 final/                # 최종 제출물
├── 📂 templates/                    # [Renderer] 문서 템플릿
│   ├── 📂 resumes/
│   └── 📂 web/                      # (Future) 포트폴리오 사이트
├── 📂 manual/                       # [Operations] 운영 문서
│   ├── 📄 NARRATIVE_STRATEGY.md     # 셀링 포인트 전략
│   ├── 📄 CASE_STUDY_*.md           # 지원 케이스 스터디
│   └── 📄 PROJECT_RETROSPECTIVE.md  # 기술적 회고록
├── 📄 CLAUDE.md                     # AI 협업 규칙 (헌법)
└── 📄 README.md                     # 이 문서
```

## 📋 Application Process

```
[1] DISCOVER → [2] ANALYZE → [3] PREPARE → [4] SUBMIT → [5] TRACK → [6] CLOSE
    👤 User      🤖 Claude     👥 협업       👤 User     👤→🤖       👥 협업
```

## 🛠️ Key Goals

1. **Single Source of Truth**: 모든 경력 정보는 `content/profile.json` 하나로 통제
2. **Strategic Archiving**: 기업별 지원 전략과 결과를 `strategy.md`로 기록
3. **Shared Assets**: 공통 자산은 `common/`에서 관리, 중복 방지
4. **Portfolio Foundation**: 정리된 데이터로 포트폴리오 웹사이트 빌드 준비

## 📛 Naming Convention

- **언어**: 영문 only
- **케이스**: snake_case
- **날짜**: YYMMDD (예: 260127)
- **버전**: _v1, _v2

## 🗂️ Current Applications

| Company | Position | Status |
|---------|----------|--------|
| 키움 히어로즈 | 회계담당 | 📤 SUBMITTED |
| 시프트업 | 총무담당자 (자산) | 🗄️ ARCHIVED |

---
**Powered by Claude (AI Pair Programming)**
