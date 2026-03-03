# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-03-03 |
| agent | Claude Opus 4.6 |
| work | 상태 확정 + CLAUDE.md 분산화 + 커스텀 스킬 생성 |
| commit | dc54d09 (상태 확정), (pending: 분산화) |

### 이번 세션 요약
- **민트로켓·네오플**: SUBMITTED 상태 확정 완료
- **CLAUDE.md 분산화**: 377줄→266줄 (-30%). ANALYZE 가이드/면접 준비/프로필 동기화를 `.claude/rules/`로 분리 (조건부 로드 → 매 턴 토큰 절약)
- **커스텀 스킬 2개 생성**: `/jd-analyze` (JD→strategy.md 자동생성, sonnet), `/coverletter-review` (opus 리뷰, 격리 실행)
- `.claude/` 폴더는 `.gitignore` 대상 → 로컬 전용 설정

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 01 | Seoul Heroes | Operations | **SUBMITTED** | 사람인 제출 완료 (2026-02-26). 마감 03/13 | `01_seoul_heroes/operations/` |
| 10 | Mintrocket (넥슨) | HR General Affairs | **SUBMITTED** | 넥슨 채용시스템 제출 완료 (2026-03-02). 3차 지원. 결과 대기 | `10_mintrocket/hr_general_affairs/` |
| 09 | Neople (넥슨) | Budget Management | **SUBMITTED** | 넥슨 채용시스템 제출 완료 (2026-03-02). 결과 대기 | `09_neople/budget_management/` |
| 07 | Kolon CSR | Energy Edu Ops | SUBMITTED | 사람인 제출 완료 (2026-02-13). 마감 2026-03-11 | `07_kolon/energy_edu_ops/` |
| 06a | SK E&S (추정) | ESG Admin | SUBMITTED | 이메일 제출 완료 (2026-02-12) | `06_sk_energy/esg_admin/` |
| 06b | SK E&S (추정) | CSR Planning | SUBMITTED | 이메일 제출 완료 (2026-02-12) | `06_sk_energy/csr_planning/` |
| 05 | SFEC | CSR Ops | SUBMITTED | Awaiting result | `05_sfec/csr_ops/` |
| 04 | Smilegate | Hope Studio PM | SUBMITTED | Awaiting result | `04_smilegate/hope_studio_csr_platform_pm/` |
| 03 | 11st | General Affairs | ON_HOLD | Paused | `03_11st/general_affairs/` |

### Closed Applications

| # | Company | Position | Status | Result |
|---|---------|----------|--------|--------|
| 01 | Seoul Heroes | Accounting | NO_RESPONSE | 팔로업 2통 무응답 → 사실상 탈락 |
| 08 | 화영운수(주) | Bus Dispatch Admin | REJECTED | 2차 면접 불합격 |

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
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `10_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
