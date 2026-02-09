# AI_CONTEXT.md — 공동작업 컨텍스트

> **이 파일은 모든 AI 에이전트가 세션 시작 시 반드시 읽어야 함.**
> 세션 종료 시 반드시 업데이트 후 커밋할 것.

## 마지막 세션
- **날짜**: 2026-02-10
- **AI**: Claude Opus 4.6 (Claude Code VSCode)
- **작업**: SK에너지 스크립트 tools/→scripts/ 이동, v9 검증, 멀티AI 협업 인프라 구축
- **커밋**: 4596b20

## 활성 지원 현황

| 지원건 | 상태 | 최우선 TODO | 전략서 경로 |
|--------|------|-------------|-------------|
| SK에너지 ESG사무 | ✍️ PREPARING | v9 유저 확인 → final/ 이동 → 이메일 제출 | `applications/sk_energy/esg_admin/` |
| SFEC CSR운영 | 📤 SUBMITTED | 결과 대기 | `applications/sfec/csr_ops/` |
| 키움 회계 | 📤 SUBMITTED | 결과 대기 | `applications/kiwoom/accounting/` |
| 스마일게이트 희망스튜디오PM | 📤 SUBMITTED | 결과 대기 | `applications/smilegate/hope_studio_csr_platform_pm/` |
| 11번가 총무 | ⏸️ ON_HOLD | 보류 중 | `applications/11st/general_affairs/` |

## 보류/의사결정 사항
- SK에너지 v9: 유저 최종 검토 대기. OK면 `final/resume_260210.docx`로 복사 후 이메일 제출 (kje@saraminhs.co.kr, 제목: SK ESG_임종권)
- 개인사업 인간지능: 휴업 신청 완료, 부가세 무실적 신고 완료. 재개까지 보류.

## 다음 AI에게
- **CLAUDE.md** = 프로젝트 규칙/구조 (필독)
- **content/profile.json** = 경력 Single Source of Truth. 새 정보 발견 시 즉시 반영.
- **content/personal_profile.md** = 개인 성향 가이드 (ISFP, 간결 선호)
- 스크립트는 해당 지원 폴더 `scripts/` 하위에 배치. 루트에 .py 생성 금지.
- 파일명 영문 snake_case 필수. 한글 파일명 금지 (양식 원본 제외).
- 커밋 시 `Co-Authored-By: {AI Model} <noreply@anthropic.com>` 트레일러 포함.
