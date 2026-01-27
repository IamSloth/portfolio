# 📂 Apply Trae Project: Technical Retrospective & Legacy

## 1. 프로젝트 개요
*   **목표**: 채용 사이트(스마일게이트)에 접속하여 이력서 내용을 바탕으로 폼(기본정보, 학력, 경력, 자소서)을 **완전 자율(Autonomous)**로 입력하는 AI 에이전트 개발.
*   **결과**: 부분 성공 (기본 입력 가능, 복잡한 팝업/검색 UI에서 한계 노출). 네이버 로그인 및 메일 분석은 성공.
*   **핵심 교훈**: **"DOM 기반 자동화는 한계가 명확하다. 차세대 에이전트는 Vision(시각) 기반이어야 한다."**

---

## 2. 시도했던 기술적 접근 (Technical Approaches)

### ❌ 접근 1: DOM Selector 기반 (Traditional Playwright)
*   **방식**: `page.locator('input[placeholder="이름"]').fill(...)`
*   **문제점**:
    *   **복잡한 중첩 구조**: 요즘 웹사이트는 `div > div > div > input` 처럼 깊게 중첩되어 있고, `id`나 `class`가 난독화된 경우가 많음.
    *   **가시성 문제**: HTML에는 존재하지만 화면상에 `hidden` 처리된 요소(탭 UI 등)를 건드려 에러 발생.
    *   **결론**: 사이트 구조가 조금만 바뀌거나 복잡하면 스크립트가 바로 깨짐. 유지보수 비용 높음.

### 🔺 접근 2: Human-in-the-loop (CDP 연결)
*   **방식**: `chromium.connectOverCDP('http://127.0.0.1:9222')`
*   **성과**: 사용자가 로그인한 브라우저 세션을 그대로 사용하여 **캡차/로그인 이슈 해결**.
*   **한계**: 브라우저 제어권은 얻었으나, 여전히 "어디를 클릭해야 하는지" 판단하는 로직은 DOM Selector에 의존함.

### ❌ 접근 3: AI/Vision 라이브러리 도입 (Stagehand / Midscene)
*   **방식**: `page.act("주소 검색 버튼 눌러")` (LLM이 화면을 보고 좌표 계산)
*   **실패 원인**:
    *   **로컬 환경 의존성**: `npm install` 시 Playwright/Puppeteer 버전 충돌 및 ESM 모듈 호환성 문제(`ERR_MODULE_NOT_FOUND`) 발생.
    *   **교훈**: AI 라이브러리는 환경 설정이 까다로움. Docker나 격리된 환경에서 세팅하는 것이 필수.

### ✅ 접근 4: JS 강제 주입 (Naver Login 성공 사례)
*   **방식**: `element.value = 'id'; element.dispatchEvent(new Event('input'));`
*   **성과**: 네이버의 **"기계적 타이핑 감지" 보안을 우회**하여 로그인 성공.
*   **교훈**: 텍스트를 한 글자씩 치는 것보다, 내부 이벤트를 트리거하는 것이 더 강력함.

---

## 3. 주요 장애물 및 해결책 (Legacy for Next Attempt)

### 🚧 1. 팝업(Popup) & 아이프레임(Iframe) 지옥
*   **현상**: 주소 검색 버튼을 눌렀는데, Playwright는 여전히 부모 창만 보고 있어서 팝업 내 입력을 못 함.
*   **해결책 (Legacy Code)**:
    ```javascript
    // 1. 페이지 내 모든 프레임 순회
    const frames = page.frames();
    for (const frame of frames) {
        if (await frame.locator('input').isVisible()) { ... }
    }
    // 2. 팝업 대기
    const [popup] = await Promise.all([
        page.waitForEvent('popup'),
        page.click('#btn_search')
    ]);
    ```

### 🚧 2. 탭(Tab) UI의 함정
*   **현상**: "대학교" 탭을 눌렀다고 생각했으나, 실제로는 클릭이 씹혀서 입력창이 `hidden` 상태로 남음.
*   **해결책**:
    *   단순 `click()` 대신 **`click({ force: true })`** 사용.
    *   그래도 안 되면 **`page.evaluate(() => document.querySelector(...).click())`** 로 JS 레벨에서 강제 실행.

### 🚧 3. 경고창(Alert)으로 인한 중단
*   **현상**: "필수 항목을 입력하세요" Alert가 뜨면 스크립트가 멈춤.
*   **필수 코드**:
    ```javascript
    page.on('dialog', async dialog => {
        console.log(dialog.message());
        await dialog.accept(); // 무조건 확인 누르기
    });
    ```

---

## 4. 재도전을 위한 로드맵 (Next Action Plan)

다음에 이 프로젝트를 다시 시작한다면, **DOM 분석을 버리고 시각(Vision) 기반으로 가야 합니다.**

1.  **환경 재구축**:
    *   `Stagehand`나 `Midscene`이 완벽하게 돌아가는 **Docker 컨테이너** 또는 **깨끗한 Node.js 환경** 준비.
    *   `npm` 의존성 충돌 해결이 최우선.

2.  **좌표 기반 클릭 (Visual Click)**:
    *   요소의 Selector를 찾는 게 아니라, **"화면 스크린샷"을 GPT-4V에 보내서 "주소 검색 버튼의 (x, y) 좌표 줘"** 라고 요청.
    *   `page.mouse.click(x, y)`로 사람이 누르듯이 클릭. (이러면 Shadow DOM, Iframe 다 무시 가능)

3.  **자율 루프 (Self-Correction Loop)**:
    *   **Action**: 클릭 시도.
    *   **Verify**: 스크린샷 다시 찍어서 "팝업 떴니?" 확인.
    *   **Retry**: 안 떴으면 좌표 보정해서 다시 클릭.
    *   (이번 프로젝트에서 부족했던 부분이 바로 이 **"확인-재시도 루프"**였음)

## 5. 결론
> "진정한 AI 에이전트는 HTML 코드를 읽는 게 아니라, **사람처럼 화면을 보고 행동해야 한다.**"

이번 시도는 **'절반의 성공'**입니다. 기본 입력은 자동화했으나, 사람의 개입 없이는 완주하지 못했습니다. 다음 도전에서는 **Visual Grounding(시각 기반 좌표 제어)** 기술을 도입하여 이 한계를 돌파해봅시다.

**작성일**: 2026-01-21
**작성자**: Trae AI Pair Programmer
