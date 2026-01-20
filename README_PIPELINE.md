# The Ultimate Job Application Pipeline (Lim-System)

이 프로젝트는 **임종권(Lim Jong Kwon)** 님의 구직 활동을 위한 **지능형 자동화 파이프라인**입니다.
단순한 이력서 생성을 넘어, **데이터 관리 -> 이력서 렌더링 -> 브라우저 자동 지원**까지 연결되는 End-to-End 시스템입니다.

## 📂 Core Structure

```
apply_trae/
├── config/
│   └── profile.json       # [핵심] 모든 개인정보와 경력 데이터는 여기에만 있습니다.
├── assets/
│   ├── templates/         # 이력서 HTML 템플릿 모음
│   │   ├── formal_a4.html      # 공문서 스타일 (Shift Up 제출본)
│   │   └── design_modern.html  # 디자인 강조 스타일
│   └── profile_photo.jpg  # 증명사진 (자동 감지)
├── src/
│   ├── core/              # 핵심 로직 (Generator, Submitter)
│   └── ...                # (Legacy scripts)
└── output/                # 생성된 PDF 결과물
```

## 🚀 How to Use (3 Steps)

### 1. 데이터 업데이트
`config/profile.json` 파일을 열어 경력이나 자격증을 수정하세요.
(이 파일 하나만 고치면 모든 스타일의 이력서에 자동 반영됩니다.)

### 2. 이력서 생성 (Generator)
원하는 스타일의 이력서를 PDF로 생성합니다.
*(현재는 `src/generate_resume_v7.js`가 V7 버전을 생성합니다. 추후 `src/core/resume_generator.js`로 통합 예정)*

### 3. 자동 지원 (Submitter)
Playwright를 통해 채용 사이트에 자동 접속하여 폼을 채우고 파일을 업로드합니다.
* **시프트업 전용**: `node src/final_submission_v7.js`
* **범용 (Vision AI)**: `src/tools/vision_capture.js`를 활용하여 폼 구조를 파악한 뒤 스크립트 작성.

## 💡 History (Shift Up Case Study)
* **2026-01-20**: 시프트업 총무 직군 지원
* **Strategy**: "게임 개발을 이해하는 총무" (Game Dev Literacy)
* **Outcome**:
    * V7 (공문서 스타일) + V3 (디자인) + Fusion (표지+이력서) 시도.
    * 최종적으로 **V7 (A4 최적화, 공문서 스타일)** 제출.
    * **Key Lesson**: 게임 회사라도 총무 직군은 "깔끔하고 정돈된(칼각)" 문서를 선호할 확률이 높음.

## 🔧 Maintenance
* **사진 교체**: `assets/` 폴더에 새 사진(`new_photo.jpg`)을 넣으면 가장 최신 파일을 자동으로 인식합니다.
* **브라우저 충돌**: `channel: 'msedge'` 옵션으로 Edge 브라우저 사용 가능.

---
**Powered by Trae AI & Anti-Gravity (Pair Programming)**
