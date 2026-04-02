# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-04-01 |
| agent | Claude Opus 4.6 |
| work | 면접 결과 반영 (사경센터 REJECTED, 네이버파이낸셜 2건 REJECTED) + 대시보드 업데이트 |
| commit | latest |

### 이번 세션 요약
- **사경센터 탈락**: 최종면담 후 탈락. 합격자 명단 게시→3시간 대기→면담→직후 탈락 문자. 센터장 장능인 부당채용 의혹.
- **네이버파이낸셜 2건 탈락**: 대출비교 서비스 운영 + 정보보호 업무 운영 지원, 서류 불합격 (4/1)
- **법적 대응 검토**: 고용노동부 진정(부당해고=채용내정 취소), 국민신문고 민원, 잡플래닛 후기 등
- **파일 업데이트**: strategy.md×3, dashboard.html, AI_CONTEXT.md 상태 반영
- **이전 세션**: 면접 준비 대시보드 배포, GitHub Pages, Google Calendar 연동

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 09 | Neople (넥슨) | Budget Management | **📞 INTERVIEW** | 1차면접 3/10 완료, 결과 대기. **1순위** | `09_neople/budget_management/` |
| 19 | 서울사회적경제센터 | SE 매니저 | **❌ REJECTED** | 최종면담 탈락 (2026-04-01). 합격자 명단 게시 후 3시간 대기 → 면담 → 직후 탈락 문자. 부당채용 의혹 | `19_seoul_se_center/se_manager/` |
| 20 | 인덕원 게임사 (비공개) | Console QA | **❌ NO_RESPONSE** | 그린맨파워 이메일 제출 (2026-03-16). 무응답 | `20_indeokwon_gameco/console_qa/` |
| 21a | 네이버파이낸셜 | 대출비교 서비스 운영 | **❌ REJECTED** | 서류 불합격 (2026-04-01) | `21_naver_financial/loan_comparison_ops/` |
| 21b | 네이버파이낸셜 | 정보보호 업무 운영 지원 | **❌ REJECTED** | 서류 불합격 (2026-04-01) | `21_naver_financial/privacy_protection_support/` |
| 22 | 오스 주식회사 | 총무/자재관리 | **📞 INTERVIEW** | 면접 4/8(수) 11:00. 상시채용 | `22_os_corporation/general_affairs_materials/` |
| 23 | 데스코 (DESCO) | 경영지원/AX TEAM | **❌ NO_RESPONSE** | 무응답. 광명 근무. 6개월 계약 | `23_desco/ax_team/` |
| 24 | 엔씨소프트 (NCsoft) | 사내 복지시설 운영 (Workplace Motivation) | **📞 INTERVIEW** | 면접 4/1(수) 15:00 알파리움타워1동 지하1층 (판교). 연락처 02-2186-3373 | `24_ncsoft/workplace_motivation/` |
| 24 | 엔씨소프트 (NCsoft) | 3D스캔 어시스턴트 | **❌ REJECTED** | 서류 불합격 (2026-04-02) | `24_ncsoft/3d_scan_assistant/` |
| 24 | 엔씨소프트 (NCsoft) | 서비스 기획/운영 어시스턴트 | **❌ REJECTED** | 서류 불합격 (2026-04-02) | `24_ncsoft/service_planning_assistant/` |
| 25 | 캐논코리아 (Canon Korea) | 영업지원 (Sales Support) | **❌ NO_RESPONSE** | 미지원/무응답 | `25_canon_korea/sales_support/` |
| 26 | 빗썸나눔 (Bithumb Nanum) | CSR 활동 지원 | **📞 INTERVIEW** | 면접 4/6(월) 14:30. 장소 미정(추후 안내). 계약직 6개월 | `26_bithumb_nanum/csr_activity_support/` |
| 28 | 시프트업 (SHIFT UP) | 인사 담당자 (기업부설연구소 관리) | **❌ NO_RESPONSE** | 무응답. 계약직 1년. 상시채용 | `28_shift_up/hr_research_lab/` |
| 29 | 현대카드·현대커머셜 (씨아이템프러리) | 법인사업1팀 데이터 관리 | **❌ NO_RESPONSE** | 무응답. 파견 계약직 | `29_hyundai_card/corporate_biz_data/` |
| 30 | KB국민은행 철산 (휴머니아) | 사무지원 | **❌ NO_RESPONSE** | 무응답 | `30_kookmin_bank/cheolsan_admin_support/` |
| 31 | 크리에이티브멋 | 총무 | **❌ NO_RESPONSE** | 무응답. 상시채용 | `31_creative_mot/general_affairs/` |
| 32 | 한국투자증권 | 사무보조 (전문직급) | **❌ NO_RESPONSE** | 무응답. 마감 3/26 경과 | `32_korea_investment/office_assistant/` |
| 33 | 빗썸 (Bithumb) | 경영관리 담당자 | **❌ NO_RESPONSE** | 무응답. 정규직 5-10년 | `33_bithumb/management_admin/` |
| 34 | 청년재단 | 전산·자산관리 (코드 A) | **❌ NO_RESPONSE** | 무응답. 마감 3/30 경과 | `34_youth_foundation/it_asset_management/` |
| 35a | 토스뱅크 | PA Operations Specialist | **📞 INTERVIEW** | 직무 인터뷰 4/3(금) 10:00 Google Meet(avb-apqn-ifj). 1~1.5h. NDA 회신 필요. 계약직 1년 | `35_toss/35a_bank_pa_operations/` |
| 35b | 토스뱅크 | CSR Project Manager | **❌ REJECTED** | 서류 불합격 (2026-03-24). 정규직 | `35_toss/35b_bank_csr_pm/` |
| 35c | 토스증권 | GA Manager | **❌ REJECTED** | 서류 불합격 (2026-03-23). 정규직. 35h도 여기에 중복제출 | `35_toss/35c_securities_ga_manager/` |
| 35d | 토스페이먼츠 | GA Specialist | **❌ REJECTED** | 서류 불합격 (2026-03-27). 계약직 1년 | `35_toss/35d_payments_ga_specialist/` |
| 35e | 토스페이먼츠 | IT Admin | **❌ REJECTED** | 서류 불합격 (2026-03-25). 계약직 1년 | `35_toss/35e_payments_it_admin/` |
| 35f | 토스씨엑스 | GA Manager | **❌ REJECTED** | 서류 불합격 (2026-03-23). 계약직 1년 | `35_toss/35f_cx_ga_manager/` |
| 35g | 토스 (본사) | GA Manager | **❌ REJECTED** | 서류 불합격 (2026-03-23). 정규직. 폴더명 rename 미완 | `35_toss/35g_bank_ga_manager/` |
| 35h | 토스증권 | GA Specialist | **❌ REJECTED** | 서류 불합격 (2026-03-24). 계약직 1년. 35c에도 중복제출 | `35_toss/35h_securities_ga_specialist/` |
| 35i | 토스인컴 | GA Specialist | **❌ REJECTED** | 서류 불합격 (2026-03-23). 계약직 1년 | `35_toss/35i_income_ga_specialist/` |
| 35j | 토스뱅크 | IT Admin | **❌ NO_RESPONSE** | 무응답. 계약직 1년 | `35_toss/35j_bank_it_admin/` |
| 36 | 키움증권 (사람인HS 파견) | 사무보조 | **❌ NO_RESPONSE** | 무응답. 파견 1년×2년 | `36_kiwoom/office_assistant/` |
| 37 | 서울히어로즈(주) | 지원팀 경영지원(회계) | **❌ NO_RESPONSE** | 무응답. 마감 4/10 | `37_heroes_baseball/accounting/` |
| 38 | 나이스계열사 (스타에이치알 파견) | 경영지원실 사무 | **❌ NO_RESPONSE** | 무응답. 파견 1년 | `38_nice_group/business_support/` |
| 39 | 우아한형제들 (Woowa) | 로보틱스운영(로봇배달 서비스 운영지원) | **❌ NO_RESPONSE** | 무응답. 재지원(#12 탈락→개선) | `39_woowa/robotics_ops/` |
| 40 | 크래프톤 (KRAFTON) | IT 구매 및 경영지원 담당자 | **❌ NO_RESPONSE** | 무응답. 계약직 1년(육휴대체) | `40_krafton/it_procurement/` |
| 03 | 11st | General Affairs | **⏸️ ON_HOLD** | 지원 안 함 (보류 → 미지원 확정) | `03_11st/general_affairs/` |

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
| 11 | Netmarble Foundation | CSR | ❌ REJECTED | 서류전형 불합격 (2026-03-18) |
| 16 | 이크래더블 (아이위더스 파견) | TCB 보고서 작성 | ❌ REJECTED | 1차면접 불합격. 5분 면접 + "다른 곳도 보고 있다" 발언 |
| 10 | Mintrocket (넥슨) | HR General Affairs | ❌ REJECTED | 서류전형 불합격 (2026-03-23) |
| 12 | 우아한형제들 (Woowa) | Robotics Ops | ❌ REJECTED | 서류전형 불합격 (2026-03-19) |
| 14 | 함께하는사랑밭 | 행정·회계 및 사업관리 | ❌ NO_RESPONSE | 이메일 제출 (2026-03-04). 15일 무응답 |
| 15 | 신한투자증권 (에이젝코리아 파견) | 사무보조 (Back Office) | ❌ NO_RESPONSE | 사람인 제출 (2026-03-05). 14일 무응답 |
| 17 | 성공회대학교 | 학생복지처 일반직 | ❌ NO_RESPONSE | 사람인 제출 (2026-03-05). 14일 무응답 |
| 18 | KASW (한국사회복지사협회) | 자격관리본부 | ❌ REJECTED | 서류전형 불합격 |
| 24 | 엔씨소프트 (NCsoft) | HR 사무지원 | ❌ REJECTED | 서류전형 불합격 (2026-03-20) |
| 24 | 엔씨소프트 (NCsoft) | 3D스캔 어시스턴트 | ❌ REJECTED | 서류 불합격 (2026-04-02) |
| 24 | 엔씨소프트 (NCsoft) | 서비스 기획/운영 어시스턴트 | ❌ REJECTED | 서류 불합격 (2026-04-02) |
| 27 | 카카오 (Kakao) | AI 데이터 라벨링 어시스턴트 | ❌ REJECTED | 서류전형 불합격 (2026-03-20) |
| 19 | 서울사회적경제센터 | SE 매니저 | ❌ REJECTED | 최종면담 탈락 (2026-04-01). 합격자 명단 게시 후 면담에서 탈락. 부당채용 의혹 |
| 21a | 네이버파이낸셜 | 대출비교 서비스 운영 | ❌ REJECTED | 서류 불합격 (2026-04-01) |
| 21b | 네이버파이낸셜 | 정보보호 업무 운영 지원 | ❌ REJECTED | 서류 불합격 (2026-04-01) |
| 20 | 인덕원 게임사 (비공개) | Console QA | ❌ NO_RESPONSE | 무응답 |
| 23 | 데스코 (DESCO) | 경영지원/AX TEAM | ❌ NO_RESPONSE | 무응답 |
| 25 | 캐논코리아 | 영업지원 | ❌ NO_RESPONSE | 무응답 |
| 28 | 시프트업 | 인사 담당자 | ❌ NO_RESPONSE | 무응답 |
| 29 | 현대카드 (씨아이템프러리) | 법인사업1팀 데이터 관리 | ❌ NO_RESPONSE | 무응답 |
| 30 | KB국민은행 철산 | 사무지원 | ❌ NO_RESPONSE | 무응답 |
| 31 | 크리에이티브멋 | 총무 | ❌ NO_RESPONSE | 무응답 |
| 32 | 한국투자증권 | 사무보조 | ❌ NO_RESPONSE | 무응답. 마감 3/26 경과 |
| 33 | 빗썸 | 경영관리 담당자 | ❌ NO_RESPONSE | 무응답 |
| 34 | 청년재단 | 전산·자산관리 | ❌ NO_RESPONSE | 무응답. 마감 3/30 경과 |
| 35j | 토스뱅크 | IT Admin | ❌ NO_RESPONSE | 무응답 |
| 36 | 키움증권 | 사무보조 | ❌ NO_RESPONSE | 무응답 |
| 37 | 서울히어로즈 | 경영지원(회계) | ❌ NO_RESPONSE | 무응답. 마감 4/10 |
| 38 | 나이스계열사 | 경영지원실 사무 | ❌ NO_RESPONSE | 무응답 |
| 39 | 우아한형제들 | 로보틱스운영 | ❌ NO_RESPONSE | 무응답. 재지원 |
| 40 | 크래프톤 | IT 구매 및 경영지원 | ❌ NO_RESPONSE | 무응답 |

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
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `41_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
