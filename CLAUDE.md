<system_rules>
1. **Thinking Process**: ALWAYS process logic and reason internally in **English** (for maximum logic density and accuracy).
2. **Output Language**: Translate the final result and communicate ONLY in **Korean**.
3. **Brevity Protocol (Crucial)**:
   - Korean output must be **extremely concise**.
   - NO conversational fillers (e.g., "확인했습니다", "코드를 수정해드리겠습니다", "참고하세요").
   - Use dry, direct endings (e.g., "~함", "~임", or short polite forms like "수정완료").
   - If the answer is code, output **ONLY the code**.
4. **Code Presentation**:
   - NEVER output full files for small changes. ALWAYS use `diff` or `search_and_replace` blocks.
   - Only show relevant lines around the change.
5. **Context Hygiene**:
   - Proactively suggest running `/compact` or `/clear` after completing a logical unit of work.
</system_rules>

## Project Constitution

> **Core Rule**: This project is a **document archiving + portfolio data hub**. Automation attempts failed; switched to manual management.

---

### 📂 Folder Structure

```
├── AI_CONTEXT.md          # Session handoff dashboard (required reading)
├── content/profile.json   # Career Single Source of Truth
├── content/personal_profile.md
├── applications/{NN}_{company}/{position}/
│   ├── {company}_{position}_strategy.md
│   ├── artifacts/  drafts/  final/
├── docs/                  # Web portfolio (→ IamSloth/portfolio subtree)
├── common/photos|evidence|snippets/
├── vault/                 # Private archive
├── templates/resumes/
└── manual/NARRATIVE_STRATEGY.md
```

---

### 📋 Application Process

```
[1] DISCOVER → [2] ANALYZE → [3] PREPARE → [4] SUBMIT → [5] TRACK → [6] CLOSE
```

| Stage | Owner | Description | Output |
|-------|-------|-------------|--------|
| DISCOVER | 👤 User | Find job posting | `artifacts/` |
| ANALYZE | 🤖 Claude | JD analysis, strategy | `strategy.md` |
| PREPARE | 👥 Collab | Write documents | `drafts/` → `final/` |
| SUBMIT | 👤 User | Submit | Status update |
| TRACK | 👤→🤖 | Track results | `strategy.md` update |
| CLOSE | 👥 Collab | Retrospective | `strategy.md` #7 |

### 🆕 New Application Workflow

1. **Create folder**: `applications/{NN}_{company}/{position}/` (next number: check AI_CONTEXT.md)
2. **Create strategy doc**: `{company}_{position}_strategy.md` (status: DISCOVERED)
3. **Save JD**: `artifacts/jd_YYMMDD.md` or `.pdf`
4. **Select template**: Reference similar position in template registry
5. **Start work**: Copy reference doc → `drafts/{doctype}_v1.html`
6. **Iterate**: v1 → v2 → ... → move to `final/{doctype}_{YYMMDD}.html` when done

### ⛔ Execution Gate — Required checks before creating files

> **CRITICAL**: Never guess company name if unclear → ask User.

1. 🚫 No guessing company name → confirm then create `applications/{NN}_{company}/{position}/`
2. 🚫 No bare `strategy.md` filename → must be `{company}_{position}_strategy.md`
3. 🚫 No missing sections → include all #1 JD ~ #7 Interview Prep
4. 🚫 No unsaved JD → `artifacts/jd_YYMMDD.md`
5. 🚫 No missing deadline → record in #6 Timeline
6. 🚫 No missing frontmatter → company, position, status(📋 DISCOVERED), discovered, last_updated

---

### 🤖 Model Routing (Sub-agent)

When running sub-agents via Task tool, select model dynamically based on task complexity.

| Model | Use | Process Stage |
|-------|-----|---------------|
| **haiku** ⚡ | File/folder search, structure validation, convention check, status update | DISCOVER, TRACK |
| **sonnet** ⚖️ | JD analysis, strategy writing, resume/cover letter draft, match analysis | ANALYZE, PREPARE |
| **opus** 🧠 | Final quality review, weak-position strategy, interview simulation, retrospective | PREPARE(review), CLOSE |

**Selection criteria**
- Simple lookup/validation → haiku (cost↓ speed↑)
- Creative/analysis → sonnet (default)
- High-judgment review → opus (quality↑)

---

### 📛 Filename + Status Codes

> Detailed rules in `.claude/rules/naming-conventions.md` (auto-loaded for `applications/**`)

- English snake_case, date YYMMDD, version _v1/_v2
- Submission PDF only uses Korean: `임종권_지원서_{회사명}.pdf`
- Company numbering: `{NN}_{company}` (check AI_CONTEXT.md for next number)

### 📂 Distributed Rules (.claude/rules/)

> Guides below are separated into `.claude/rules/` — auto-loaded when working on related files.

| Rule File | Content | Load Condition |
|-----------|---------|----------------|
| `naming-conventions.md` | Filename rules + status codes | `applications/**` |
| `analyze-guide.md` | ANALYZE detailed guide + template registry | `applications/**/*strategy*.md` |
| `interview-prep.md` | Interview prep workflow | `applications/**/drafts/interview_prep*.md` |
| `profile-sync.md` | profile.json sync rules | `content/profile.json` |

---

### 🚫 Prohibitions

- **No MD file clutter in root**: only `README.md`, `CLAUDE.md`, `AI_CONTEXT.md` allowed
- **No duplicate strategy docs**: one `strategy.md` per application only
- **No automation remnants**: no `.js`, `.py` files in root
- **No Korean filenames**: all filenames must be English snake_case

---

### 🤝 Multi-AI Collaboration Protocol

> This project is worked on by multiple AI agents in rotation (Opus, Sonnet, others).

- `AI_CONTEXT.md` (root): **Full status dashboard**. Read/update at session start/end.
- `{company}_{position}_strategy.md` handoff section: per-application detailed context.
- **At session end**: Update AI_CONTEXT.md → git commit → push
- Track which AI worked via commit `Co-Authored-By`

---

### 🚀 Session Start Checklist

> **Token savings**: Reading these files first drastically reduces exploration time.

**Required references at every session start:**
1. `AI_CONTEXT.md` — Previous session summary, active work status (read first)
2. `content/profile.json` — Career data (Single Source of Truth)
3. `content/personal_profile.md` — Personal traits, communication guide (ISFP, dislikes interference)
4. `manual/NARRATIVE_STRATEGY.md` — Selling strategy, "Why Him?"
5. Current application status: see active applications table in `AI_CONTEXT.md`

---

### 🔗 Quick Reference

| Purpose | Path |
|---------|------|
| Profile photo | `common/photos/profile.png` |
| Signature image | `common/photos/signature.png` |
| Career data | `content/profile.json` |
| **Personal profile** | `content/personal_profile.md` |
| Selling strategy | `manual/NARRATIVE_STRATEGY.md` |
| Per-company strategy | `applications/{company}/{position}/{company}_{position}_strategy.md` |
| Resume templates | `templates/resumes/` |
