# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-03-17 |
| agent | Claude Opus 4.6 |
| work | NCsoft(#24) 지원 서류 풀세트 완성: strategy.md + form_data + application_v1.html(네이비) + ncsoft.html 전용 포트폴리오(rAF marquee, Awwwards급 리디자인) |
| commit | latest |

### 이번 세션 요약
- **NCsoft (24)**: JD 분석→strategy.md 생성, 채용시스템 입력용 form_data.md, 2페이지 A4 지원서(application_v1.html), NC 전용 포트폴리오(docs/ncsoft.html) 제작.
- **ncsoft.html**: 3차 리디자인 — CSS animation→JS rAF+Lerp 물리엔진(scroll velocity→가속+skew, hover→lerp 감속), outline/gradient 비대칭 타이포, Awwwards급 easing·색온도·border-radius 전면 교체.
- **application_v1.html**: CSS 변수 퍼플→네이비(#00365e) 교체. 개인정보(전화번호/주소) 제거.

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 09 | Neople (넥슨) | Budget Management | **📞 INTERVIEW** | 1차면접 3/10 완료, 결과 대기. **1순위** | `09_neople/budget_management/` |
| 10 | Mintrocket (넥슨) | HR General Affairs | **📤 SUBMITTED** | 넥슨 채용시스템 제출 완료 (2026-03-02). 결과 대기 | `10_mintrocket/hr_general_affairs/` |
| 11 | Netmarble Foundation | CSR | **📤 SUBMITTED** | 사이드바 이력서+자소서 제출 완료 (2026-03-03). 결과 대기 | `11_netmarble/csr/` |
| 12 | 우아한형제들 (Woowa) | Robotics Ops | **📤 SUBMITTED** | 온라인 지원 완료 (2026-03-03). 12개월 계약직. 결과 대기 | `12_woowa/robotics_ops/` |
| 14 | 함께하는사랑밭 | 행정·회계 및 사업관리 | **📤 SUBMITTED** | 이메일 제출 완료 (2026-03-04). 결과 대기 | `14_withgo/csr_admin/` |
| 15 | 신한투자증권 (에이젝코리아 파견) | 사무보조 (Back Office) | **📤 SUBMITTED** | 사람인 온라인 제출 완료 (2026-03-05). 결과 대기 | `15_shinhan_invest/office_assistant/` |
| 17 | 성공회대학교 | 학생복지처 일반직 | **📤 SUBMITTED** | 사람인 온라인 제출 완료 (2026-03-05). 결과 대기 | `17_sungkonghoe/student_welfare/` |
| 18 | KASW (한국사회복지사협회) | 자격관리본부 | **📤 SUBMITTED** | 이메일 제출 완료. 결과 대기 | `18_kasw/cert_review/` |
| 19 | 서울사회적경제센터 | SE 매니저 | **📤 SUBMITTED** | 사람인 제출 완료 (2026-03-08). 마감 3/19, 발표 3/20 | `19_seoul_se_center/se_manager/` |
| 20 | 인덕원 게임사 (비공개) | Console QA | **📤 SUBMITTED** | 그린맨파워 이메일 제출 완료 (2026-03-16). 결과 대기 | `20_indeokwon_gameco/console_qa/` |
| 21a | 네이버파이낸셜 | 대출비교 서비스 운영 | **📤 SUBMITTED** | 네이버 채용시스템 제출 완료 (2026-03-16). 결과 대기 | `21_naver_financial/loan_comparison_ops/` |
| 21b | 네이버파이낸셜 | 정보보호 업무 운영 지원 | **📤 SUBMITTED** | 네이버 채용시스템 제출 완료 (2026-03-16). 결과 대기 | `21_naver_financial/privacy_protection_support/` |
| 22 | 오스 주식회사 | 총무/자재관리 | **📋 DISCOVERED** | JD 분석 완료. 근무지 미확인. 상시채용 | `22_os_corporation/general_affairs_materials/` |
| 23 | 데스코 (DESCO) | 경영지원/AX TEAM | **📋 DISCOVERED** | JD 분석 완료. **광명 근무**. 6개월 계약(정규직 전환 가능). 상시채용 | `23_desco/ax_team/` |
| 24 | 엔씨소프트 (NCsoft) | 사내 복지시설 운영 (Workplace Motivation) | **📤 SUBMITTED** | 서류 제출 완료. 전용 포트폴리오 페이지 배포. 마감 5/12 | `24_ncsoft/workplace_motivation/` |
| 03 | 11st | General Affairs | **⏸️ ON_HOLD** | 지원 안 함 (보류 유지) | `03_11st/general_affairs/` |

### Closed Applications

| # | Company | Position | Status | Result |
|---|---------|----------|--------|--------|
| 01 | Seoul Heroes | Accounting | ❌ NO_RESPONSE | 팔로업 2통 무응답 → 사실상 탈락 |
| 01 | Seoul Heroes | Operations | ❌ NO_RESPONSE | 사람인 제출 (2026-02-26). 무응답 |
| 02 | Shift Up | — | ❌ NO_RESPONSE | 무응답 |
| 04 | Smilegate | Hope Studio PM | ❌ NO_RESPONSE | 무응답 |
| 05 | SFEC | CSR Ops | ❌ NO_RESPONSE | 무응답 |
| 06a | SK E&S | ESG Admin | ❌ NO_RESPONSE | 이메일 제출 (2026-02-12). 무응답 |
| 06b | SK E&S | CSR Planning | ❌ NO_RESPONSE | 이메일 제출 (2026-02-12). 무응답 |
| 07 | Kolon CSR | Energy Edu Ops | ❌ NO_RESPONSE | 사람인 제출 (2026-02-13). 무응답 |
| 08 | 화영운수(주) | Bus Dispatch Admin | ❌ REJECTED | 2차 면접 불합격. 광명에서 먼 곳 배치 의도 확인됨 |
| 13 | 동양미래대학교 | 일학습병행사업 관리 및 운영 | ❌ REJECTED | 면접 불합격 |
| 16 | 이크래더블 (아이위더스 파견) | TCB 보고서 작성 | ❌ REJECTED | 1차면접 불합격. 5분 면접 + "다른 곳도 보고 있다" 발언 |

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
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `25_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
