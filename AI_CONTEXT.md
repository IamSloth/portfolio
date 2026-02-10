# AI_CONTEXT.md — Multi-Agent Handoff State

> **READ THIS FIRST.** This file is the shared handoff state for all AI agents working on this project.
> Update this file at the end of every session, then commit and push.

## Last Session

| Field | Value |
|-------|-------|
| date | 2026-02-10 |
| agent | Claude Opus 4.6 (Claude Code / VSCode) |
| work | Numbered application folders (01_~06_), rewrote AI_CONTEXT.md in English |
| commit | ff53bc9 |

## Active Applications

| # | Company | Position | Status | Priority TODO | Strategy Path |
|---|---------|----------|--------|---------------|---------------|
| 06 | SK Energy | ESG Admin | PREPARING | User confirms v9 → move to final/ → email submit | `06_sk_energy/esg_admin/` |
| 05 | SFEC | CSR Ops | SUBMITTED | Awaiting result | `05_sfec/csr_ops/` |
| 01 | Kiwoom | Accounting | SUBMITTED | Awaiting result | `01_kiwoom/accounting/` |
| 04 | Smilegate | Hope Studio PM | SUBMITTED | Awaiting result | `04_smilegate/hope_studio_csr_platform_pm/` |
| 03 | 11st | General Affairs | ON_HOLD | Paused | `03_11st/general_affairs/` |

## Pending Decisions

- **SK Energy v9**: User final review pending. If OK → copy to `final/resume_260210.docx` → email to kje@saraminhs.co.kr (subject: SK ESG_임종권)
- **Side business (인간지능)**: On hiatus. VAT zero-filing done. Resume when business restarts.

## Critical Files (Read Order)

1. `CLAUDE.md` — Project rules, folder structure, process definitions (Korean)
2. `AI_CONTEXT.md` — This file. Session state and active tasks.
3. `content/profile.json` — Career data. **Single Source of Truth.** Update immediately when new info is discovered.
4. `content/personal_profile.md` — Personal traits guide (ISFP, prefers brevity, dislikes micromanagement)

## Conventions for All Agents

- **Filenames**: English snake_case only. No Korean filenames (except original form templates).
- **Scripts**: Place inside the relevant application's `scripts/` subfolder. Never in project root.
- **Commits**: Always include `Co-Authored-By: {Model Name} <noreply@anthropic.com>` trailer.
- **Application folders**: Numbered by discovery date: `{NN}_{company}/`. Next new company = `07_`.
- **Profile sync**: If you discover new career/skill/cert info during work, update `profile.json` immediately.
- **Session end**: Update this file → commit → push. Keep entries concise (token budget matters).
