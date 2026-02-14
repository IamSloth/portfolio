# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-02-14 |
| agent | Claude Opus 4.6 |
| work | 포트폴리오(docs/) 대규모 리뉴얼 + 범용 이력서 신규 생성 |
| commit | see below |

### 이번 세션 변경 상세
- **docs/index.html**: 컬러 Teal+Amber 전환, 섹션 재구성(AI showcase→커리어스토리, 교육+수상→Skills 통합), GitHub 링크 제거, hero링크 pill 버튼 통일, 이모지 추가, 이력서PDF→resume.html 연결, 커리어스토리 한글 자연스럽게 재작성, CTA 2문장 분리
- **docs/style.css**: Teal+Amber CSS변수, text-wrap:balance, hero-cta pill, story-narrative max-width 780px, background-grid, scroll-indicator bounce, hero grain texture 등 전면 리팩터
- **docs/resume.html**: (신규) A4 범용 이력서 — Teal gradient 헤더, 2-column 레이아웃, 타임라인 경력3사, Unity 프로젝트 하이라이트(Amber), 키워드태그/자격증/학력/수상/병역. Ctrl+P로 PDF 저장 가능
- **docs/assets/projects/photo_blynk_graph.jpg**: IoT 카드 이미지 교체

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 07 | Kolon CSR | Energy Edu Ops | SUBMITTED | 사람인 제출 완료 (2026-02-13). 마감 2026-03-11 | `07_kolon/energy_edu_ops/` |
| 06a | SK E&S (추정) | ESG Admin | SUBMITTED | 이메일 제출 완료 (2026-02-12) | `06_sk_energy/esg_admin/` |
| 06b | SK E&S (추정) | CSR Planning | SUBMITTED | 이메일 제출 완료 (2026-02-12) | `06_sk_energy/csr_planning/` |
| 05 | SFEC | CSR Ops | SUBMITTED | Awaiting result | `05_sfec/csr_ops/` |
| 01 | Seoul Heroes (서울히어로즈) | Accounting | SUBMITTED | Awaiting result (접수마감 02/03, 면접 2월 둘째주 예정) | `01_seoul_heroes/accounting/` |
| 04 | Smilegate | Hope Studio PM | SUBMITTED | Awaiting result | `04_smilegate/hope_studio_csr_platform_pm/` |
| 03 | 11st | General Affairs | ON_HOLD | Paused | `03_11st/general_affairs/` |

## Pending Decisions

- **Kolon Energy Edu**: 사람인 제출 완료 (2026-02-13). 서류 결과 대기 중. 마감 2026-03-11.
- **SK E&S**: 2개 포지션 이메일 제출 완료 (2026-02-12). 서류 결과 대기 중.
- **Side business (인간지능)**: On hiatus. VAT zero-filing done. Resume when business restarts.
- **Job strategy**: 자발적퇴사→실업급여불가 상태. 파견직/계약직 경유→계약만료시 퇴직금+실업급여 확보 전략.

## Critical Files (Read Order)

1. `AI_CONTEXT.md` — This file. Session state and active tasks. (You're reading it now.)
2. `CLAUDE.md` — Project rules, folder structure, process definitions (Korean)
3. `content/profile.json` — Career data. **Single Source of Truth.** Update immediately when new info is discovered.
4. `content/personal_profile.md` — Personal traits guide (ISFP, prefers brevity, dislikes micromanagement)

## Conventions for All Agents

- **Filenames**: English snake_case only. No Korean filenames (except original form templates and final 제출본).
- **Scripts**: Place inside the relevant application's `scripts/` subfolder. Never in project root.
- **Commits**: Always include `Co-Authored-By: {Model Name} <noreply@anthropic.com>` trailer.
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `08_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
