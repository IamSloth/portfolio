# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-02-20 |
| agent | Claude Opus 4.6 |
| work | 화영운수 1차면접 통과 → 자사양식 HWP 이메일 회신 + profile.json 병역 수정 |
| commit | (pending) |

### 이번 세션 요약
- **화영운수 1차면접 당일 통과** (2/20 10:00 전화 → 11:30 1차면접 → 13:00 2차면접 안내)
- 자사양식 HWP 이력서·자기소개서 작성 (`company_form_v1.html` → HWP 변환)
- Gmail IMAP으로 화영운수 메일 확인 → `reply_email.py`로 답장 발송 (첨부 3건)
- 이슈: 한국어 파일명 MIME 인코딩 "noname" → RFC 2231 수정 후 재발송
- profile.json 병역 기간 수정 (2012.05~2014.05 → 2010.07~2012.08)
- **2차 면접: 2026-02-23(월) 11:20까지 도착**

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 08 | 화영운수(주) | Bus Dispatch Admin | **INTERVIEW** | **2차 면접 2/23(월) 11:20**. 면접 준비 필요 | `08_hwayoungunsu/bus_dispatch_admin/` |
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
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `09_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
