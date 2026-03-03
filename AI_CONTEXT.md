# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-03-03 |
| agent | Antigravity |
| work | 넷마블문화재단 CSR 서류(이력서/자소서) 드래프트 작성 |
| commit | pending |

### 이번 세션 요약
- **넷마블문화재단**: 이력서 및 자소서 초안 `drafts/` 폴더에 작성 완료. JD 핵심역량 키워드 직접 반영 구조화.
- **포트폴리오 참고**: 스마일게이트, SFEC, 코오롱 서류 참고하여 작성 방향성 정렬.

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
| 11 | Netmarble Foundation | CSR | **PREPARING** | 이력서 및 자소서 드래프트 작성 완료. 리뷰 대기. | `11_netmarble/csr/` |
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
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `12_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
