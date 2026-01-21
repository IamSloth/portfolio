# Lim-Pipeline MCP Agent

이 폴더는 **Model Context Protocol (MCP)** 기반의 서브 에이전트를 포함하고 있습니다.
이 에이전트는 Claude Desktop이나 Trae와 같은 AI 모델이 **브라우저를 제어하고, 이력서 데이터를 읽고, 지원서를 제출**할 수 있게 해줍니다.

## 🛠️ 기능 (Capabilities)
1. **Candidate Profile**: `config/profile.json` 데이터를 읽어 임종권 님의 경력 정보를 제공합니다.
2. **Browser Automation**: Playwright를 통해 웹사이트 이동, 폼 입력, 클릭 등을 수행합니다.
3. **File System**: 최신 이력서 PDF 파일 경로를 찾아줍니다.

## 🚀 실행 방법 (Claude Desktop)
Claude Desktop 설정 파일(`claude_desktop_config.json`)에 다음을 추가하세요:

```json
{
  "mcpServers": {
    "lim-agent": {
      "command": "node",
      "args": [
        "C:/Users/superjk/Desktop/apply_trae/src/agent/server.js"
      ]
    }
  }
}
```

## 🧪 테스트
터미널에서 직접 실행하여 오류가 없는지 확인할 수 있습니다 (stdio 통신이라 아무 반응이 없는 게 정상입니다):
```bash
node src/agent/server.js
```
