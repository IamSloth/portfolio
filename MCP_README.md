# Standard MCP Servers Setup (2026 Edition)

이 프로젝트에는 2026년 기준 가장 널리 사용되는 **표준 MCP 서버**들이 포함되어 있습니다.
AI 모델(Claude, Trae 등)이 이 서버들을 통해 로컬 파일, 깃허브, 메모리, 웹 검색 등을 수행할 수 있습니다.

## 📦 설치된 서버 목록 (Installed Servers)

1.  **📂 Filesystem (`@modelcontextprotocol/server-filesystem`)**
    *   로컬 파일 읽기/쓰기/탐색.
    *   기본 설정: 현재 프로젝트 폴더(`apply_trae`) 접근 허용.
2.  **🧠 Memory (`@modelcontextprotocol/server-memory`)**
    *   지식 그래프 기반의 장기 기억 저장소.
    *   사용자의 선호도나 프로젝트 컨텍스트를 기억합니다.
3.  **🐙 GitHub (`@modelcontextprotocol/server-github`)**
    *   GitHub 리포지토리 검색, 이슈 관리, 파일 조회.
    *   *설정 필요*: `GITHUB_PERSONAL_ACCESS_TOKEN` 환경변수.
4.  **🔍 Brave Search (`@modelcontextprotocol/server-brave-search`)**
    *   실시간 웹 검색 (구글링 대체).
    *   *설정 필요*: `BRAVE_API_KEY` 환경변수.
5.  **🤖 Lim-Agent (Custom)**
    *   우리가 만든 취업 전용 에이전트 (이력서 관리 + 브라우저 자동화).

## ⚙️ 설정 방법 (Configuration)

### Claude Desktop 사용 시
프로젝트 루트에 생성된 `claude_desktop_config.json` 파일의 내용을
`%APPDATA%\Claude\claude_desktop_config.json` 파일에 복사해서 붙여넣으세요.
(단, `<YOUR_TOKEN_HERE>` 부분은 실제 키로 변경해야 합니다.)

### Trae / 기타 IDE 사용 시
각 도구의 MCP 설정 메뉴에서 위 서버들을 등록하여 사용할 수 있습니다.

## 📝 사용 예시
*   "Filesystem 서버를 써서 `src` 폴더 구조를 보여줘."
*   "Memory 서버에 '나는 Python보다 Node.js를 선호한다'라고 저장해."
*   "Brave Search로 최신 React 트렌드를 검색해줘."
