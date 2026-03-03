# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-03-03 |
| agent | Claude Sonnet 4.6 |
| work | 동양미래대학교 일학습병행사업 관리 및 운영 지원 서류 전체 작성 + 합본 PDF 생성 |
| commit | latest |

### 이번 세션 요약
- **동양미래대학교 일학습병행사업**: `13_dongyang/general_admin/` 생성. 오늘 마감(2026-03-03). 지원분야를 일반행정→일학습병행사업으로 변경. HWP 직접 입력 방식. hwp_form_data.md에 전체 입력 데이터 작성. 자격증사본 PDF 생성(자필 원본대조필 포함). 전체 서류 합본 PDF(19페이지) 생성: `final/[일학습병행사업] 임종권_지원서류_260303.pdf`. 이메일 발송 완료: eusung@dongyang.ac.kr.

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 10 | Mintrocket (넥슨) | HR General Affairs | **SUBMITTED** | 넥슨 채용시스템 제출 완료 (2026-03-02). 3차 지원. 결과 대기 | `10_mintrocket/hr_general_affairs/` |
| 09 | Neople (넥슨) | Budget Management | **SUBMITTED** | 넥슨 채용시스템 제출 완료 (2026-03-02). 결과 대기 | `09_neople/budget_management/` |
| 11 | Netmarble Foundation | CSR | **SUBMITTED** | 사이드바 이력서+자소서 제출 완료 (2026-03-03). 결과 대기 | `11_netmarble/csr/` |
| 12 | 우아한형제들 (Woowa) | Robotics Ops | **SUBMITTED** | 온라인 지원 완료 (2026-03-03). 12개월 계약직. 결과 대기 | `12_woowa/robotics_ops/` |
| 13 | 동양미래대학교 | 일학습병행사업 관리 및 운영 | **SUBMITTED** | 이메일 제출 완료 (2026-03-03). 마감일 = 제출일. 면접 2026-03-06 예정. 결과 대기 | `13_dongyang/general_admin/` |
| 03 | 11st | General Affairs | ON_HOLD | 지원 안 함 (보류 유지) | `03_11st/general_affairs/` |

### Closed Applications

| # | Company | Position | Status | Result |
|---|---------|----------|--------|--------|
| 01 | Seoul Heroes | Accounting | ❌ NO_RESPONSE | 팔로업 2통 무응답 → 사실상 탈락 |
| 01 | Seoul Heroes | Operations | ❌ NO_RESPONSE | 사람인 제출 (2026-02-26). 마감 03/13 후 무응답 |
| 02 | Shift Up | — | ❌ NO_RESPONSE | 무응답 |
| 04 | Smilegate | Hope Studio PM | ❌ NO_RESPONSE | 무응답 |
| 05 | SFEC | CSR Ops | ❌ NO_RESPONSE | 무응답 |
| 06a | SK E&S | ESG Admin | ❌ NO_RESPONSE | 이메일 제출 (2026-02-12). 무응답 |
| 06b | SK E&S | CSR Planning | ❌ NO_RESPONSE | 이메일 제출 (2026-02-12). 무응답 |
| 07 | Kolon CSR | Energy Edu Ops | ❌ NO_RESPONSE | 사람인 제출 (2026-02-13). 마감 03-11 후 무응답 |
| 08 | 화영운수(주) | Bus Dispatch Admin | ❌ REJECTED | 2차 면접 불합격. 광명에서 먼 곳 배치 의도 확인됨 |

## Pending Decisions
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
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `13_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
