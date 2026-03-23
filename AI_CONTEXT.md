# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-03-23 |
| agent | Claude Opus 4.6 |
| work | #40 크래프톤 IT Procurement 서류 준비 + 웹포폴 제작 |
| commit | latest |

### 이번 세션 요약
- **#40 크래프톤 IT 구매 및 경영지원 담당자**: 서류 준비 완료
  - 이력서(resume_v2) + 자기소개서(coverletter_v1) HTML→PDF
  - 웹 포트폴리오: `docs/krafton-it-procurement.html` (크래프톤 CI 레드 #f9423a)
  - QR코드 → 포트폴리오 연결, 푸터 디자인 2차 반복(서명 제거→타이틀+면책문구)
  - Greenhouse 채용시스템 제출 예정 (계약직 1년, 육아휴직 대체)
- **이전 세션**: #39 우아한형제들 재지원, #38 나이스계열사 제출, #37 서울히어로즈

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 09 | Neople (넥슨) | Budget Management | **📞 INTERVIEW** | 1차면접 3/10 완료, 결과 대기. **1순위** | `09_neople/budget_management/` |
| 19 | 서울사회적경제센터 | SE 매니저 | **📤 SUBMITTED** | 사람인 제출 완료 (2026-03-08). 마감 3/19, 발표 3/20 | `19_seoul_se_center/se_manager/` |
| 20 | 인덕원 게임사 (비공개) | Console QA | **📤 SUBMITTED** | 그린맨파워 이메일 제출 완료 (2026-03-16). 결과 대기 | `20_indeokwon_gameco/console_qa/` |
| 21a | 네이버파이낸셜 | 대출비교 서비스 운영 | **📤 SUBMITTED** | 네이버 채용시스템 제출 완료 (2026-03-16). 결과 대기 | `21_naver_financial/loan_comparison_ops/` |
| 21b | 네이버파이낸셜 | 정보보호 업무 운영 지원 | **📤 SUBMITTED** | 네이버 채용시스템 제출 완료 (2026-03-16). 결과 대기 | `21_naver_financial/privacy_protection_support/` |
| 22 | 오스 주식회사 | 총무/자재관리 | **📤 SUBMITTED** | 제출 완료. 응답 없음. 상시채용 | `22_os_corporation/general_affairs_materials/` |
| 23 | 데스코 (DESCO) | 경영지원/AX TEAM | **📤 SUBMITTED** | 제출 완료. 응답 없음. 광명 근무. 6개월 계약. 상시채용 | `23_desco/ax_team/` |
| 24 | 엔씨소프트 (NCsoft) | 사내 복지시설 운영 (Workplace Motivation) | **📤 SUBMITTED** | 서류 제출 완료. 전용 포트폴리오 페이지 배포. 마감 5/12 | `24_ncsoft/workplace_motivation/` |
| 24 | 엔씨소프트 (NCsoft) | 3D스캔 어시스턴트 | **📤 SUBMITTED** | 제출 완료 (2026-03-17). 마감 4/3. 결과 대기 | `24_ncsoft/3d_scan_assistant/` |
| 24 | 엔씨소프트 (NCsoft) | 서비스 기획/운영 어시스턴트 | **📤 SUBMITTED** | 제출 완료 (2026-03-17). 마감 3/25. 결과 대기 | `24_ncsoft/service_planning_assistant/` |
| 25 | 캐논코리아 (Canon Korea) | 영업지원 (Sales Support) | **📋 DISCOVERED** | 계약직 1년, 강남 본사. ERP/데이터/부서조율 ⭐⭐⭐ 매칭. 마감일 확인 필요 | `25_canon_korea/sales_support/` |
| 26 | 빗썸나눔 (Bithumb Nanum) | CSR 활동 지원 | **📤 SUBMITTED** | 나인하이어 제출 완료 (2026-03-18). 계약직 6개월. 상시채용 | `26_bithumb_nanum/csr_activity_support/` |
| 28 | 시프트업 (SHIFT UP) | 인사 담당자 (기업부설연구소 관리) | **📤 SUBMITTED** | 채용페이지 제출 완료 (2026-03-18). 계약직 1년. 상시채용 | `28_shift_up/hr_research_lab/` |
| 29 | 현대카드·현대커머셜 (씨아이템프러리) | 법인사업1팀 데이터 관리 | **📤 SUBMITTED** | 사람인 제출 완료 (2026-03-18). 파견 계약직. 결과 대기 | `29_hyundai_card/corporate_biz_data/` |
| 30 | KB국민은행 철산 (휴머니아) | 사무지원 | **📤 SUBMITTED** | 이메일 제출 완료 (2026-03-18) → baeilsuk@naver.com. 결과 대기 | `30_kookmin_bank/cheolsan_admin_support/` |
| 31 | 크리에이티브멋 | 총무 | **📤 SUBMITTED** | 사람인 제출 완료 (2026-03-19). 상시채용. 포폴: creative-mot.html | `31_creative_mot/general_affairs/` |
| 32 | 한국투자증권 | 사무보조 (전문직급) | **📤 SUBMITTED** | 채용포털 제출 완료 (2026-03-19). 전문계약직 1년단위, 여의도 본사. 마감 3/26 | `32_korea_investment/office_assistant/` |
| 33 | 빗썸 (Bithumb) | 경영관리 담당자 | **📤 SUBMITTED** | 나인하이어 제출 완료 (2026-03-19). 정규직 5-10년. 상시채용. 포폴: bithumb.html | `33_bithumb/management_admin/` |
| 34 | 청년재단 | 전산·자산관리 (코드 A) | **📤 SUBMITTED** | 인크루트 제출 완료 (2026-03-19). 정규직, 경력3년+. 마감 3/30. **Strong Go** | `34_youth_foundation/it_asset_management/` |
| 35a | 토스뱅크 | PA Operations Specialist | **📤 SUBMITTED** | Greenhouse 제출 완료 (2026-03-20). 계약직 1년 | `35_toss/35a_bank_pa_operations/` |
| 35b | 토스뱅크 | CSR Project Manager | **📤 SUBMITTED** | Greenhouse 제출 완료 (2026-03-20). 정규직 | `35_toss/35b_bank_csr_pm/` |
| 35c | 토스증권 | GA Manager | **❌ REJECTED** | 서류 불합격 (2026-03-23). 정규직. 35h도 여기에 중복제출 | `35_toss/35c_securities_ga_manager/` |
| 35d | 토스페이먼츠 | GA Specialist | **📤 SUBMITTED** | Greenhouse 제출 완료 (2026-03-20). 계약직 1년 | `35_toss/35d_payments_ga_specialist/` |
| 35e | 토스페이먼츠 | IT Admin | **📤 SUBMITTED** | Greenhouse 제출 완료 (2026-03-20). 계약직 1년 | `35_toss/35e_payments_it_admin/` |
| 35f | 토스씨엑스 | GA Manager | **❌ REJECTED** | 서류 불합격 (2026-03-23). 계약직 1년 | `35_toss/35f_cx_ga_manager/` |
| 35g | 토스 (본사) | GA Manager | **❌ REJECTED** | 서류 불합격 (2026-03-23). 정규직. 폴더명 rename 미완 | `35_toss/35g_bank_ga_manager/` |
| 35h | 토스증권 | GA Specialist | **📤 SUBMITTED** | Greenhouse 제출 완료 (2026-03-20). 계약직 1년. 35c에도 중복제출 | `35_toss/35h_securities_ga_specialist/` |
| 35i | 토스인컴 | GA Specialist | **❌ REJECTED** | 서류 불합격 (2026-03-23). 계약직 1년 | `35_toss/35i_income_ga_specialist/` |
| 35j | 토스뱅크 | IT Admin | **📤 SUBMITTED** | Greenhouse 제출 완료 (2026-03-20). 계약직 1년 | `35_toss/35j_bank_it_admin/` |
| 36 | 키움증권 (사람인HS 파견) | 사무보조 | **📤 SUBMITTED** | 사람인 제출 완료 (2026-03-20). 파견 1년×2년계약, 여의도. 상시채용 | `36_kiwoom/office_assistant/` |
| 37 | 서울히어로즈(주) | 지원팀 경영지원(회계) | **📤 SUBMITTED** | 사람인 제출 완료 (2026-03-22). 계약직 1년, 고척돔. 마감 4/10. **0순위** | `37_heroes_baseball/accounting/` |
| 38 | 나이스계열사 (스타에이치알 파견) | 경영지원실 사무 | **📤 SUBMITTED** | 사람인 제출 완료 (2026-03-23). 파견 1년, 신도림. 상시채용 | `38_nice_group/business_support/` |
| 39 | 우아한형제들 (Woowa) | 로보틱스운영(로봇배달 서비스 운영지원) | **📤 SUBMITTED** | 채용페이지 제출 완료 (2026-03-23). 기간제 12개월. 재지원(#12 탈락→개선). 포폴: woowa-robotics.html | `39_woowa/robotics_ops/` |
| 40 | 크래프톤 (KRAFTON) | IT 구매 및 경영지원 담당자 | **✍️ PREPARING** | 서류 준비 완료, Greenhouse 제출 예정. 계약직 1년(육휴대체). 포폴: krafton-it-procurement.html | `40_krafton/it_procurement/` |
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
| 27 | 카카오 (Kakao) | AI 데이터 라벨링 어시스턴트 | ❌ REJECTED | 서류전형 불합격 (2026-03-20) |

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
