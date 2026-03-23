# Claude Code Channels — Discord (jobhelper) 셋업 가이드

## 사전 조건 ✅ (모두 완료)
- [x] Claude Code 2.1.81 (Channels 지원)
- [x] Bun 1.3.11 설치됨
- [x] Discord 봇 "jobhelper" 생성 + 서버 초대 완료
- [x] 봇 토큰 확보 + 저장 (`~/.claude/channels/discord/.env`)
- [x] Discord 플러그인 설치 (`discord@claude-plugins-official`)
- [x] access.json 초기화 (pairing 모드)

## 실행 (터미널에서 한 줄)

```bash
claude --channels plugin:discord@claude-plugins-official
```

## 최초 연결 (페어링)
1. 위 명령 실행 → Discord 봇 온라인 전환
2. Discord에서 jobhelper 봇에게 DM 전송
3. 터미널에 페어링 코드 표시됨
4. 터미널에서 입력:
```bash
/discord:access pair <코드>
```
5. 보안 잠금:
```bash
/discord:access policy allowlist
```

## 사용법
- Discord에서 jobhelper 봇에게 DM 또는 멘션
- "히어로즈 면접 날짜 확인해줘" → 로컬 프로젝트에서 실행 → 답변 반환
- 세션이 열려있는 동안에만 동작 (터미널 닫으면 중단)

## 주의사항
- `claude.ai` 로그인 필수 (API key 인증 불가)
- Research Preview 단계 — 공식 allowlist 플러그인만 지원
- 항상 켜두려면 터미널을 백그라운드로 유지하거나 tmux/screen 사용
