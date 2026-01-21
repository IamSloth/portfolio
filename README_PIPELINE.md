# The Ultimate Job Application Pipeline (Lim-System)

이 프로젝트는 **임종권(Lim Jong Kwon)** 님의 구직 활동을 위한 **지능형 자동화 파이프라인**입니다.
단순한 이력서 생성을 넘어, **데이터 관리 -> 이력서 렌더링 -> 브라우저 자동 지원**까지 연결되는 End-to-End 시스템입니다.

## 📂 Core Structure

```
apply_trae/
├── config/
│   └── profile.json       # [핵심] 모든 개인정보와 경력 데이터 (Source of Truth)
├── companies/             # [NEW] 기업별 지원 스크립트 관리
│   └── _submitted/        # [ARCHIVE] 지원 완료된 기업
│       └── shiftup/
├── src/
│   ├── core/
│   │   └── resume_generator.js # [표준] V7 기반 이력서 생성기
│   └── legacy/            # 구버전 스크립트 보관소
├── assets/
│   └── templates/
│       └── standard_v1.html    # 표준 이력서 HTML (구 V7)
└── output/                # 생성된 PDF 결과물
```

## 🚀 How to Use (3 Steps)

### 1. 데이터 업데이트
`config/profile.json` 수정.

### 2. 이력서 생성 (Generator)
```bash
# 표준 이력서 (PDF) 생성
node src/core/resume_generator.js
```

### 3. 자동 지원 (Submitter)
```bash
# 새로운 기업 폴더 생성 후 스크립트 작성 권장
# 예: companies/nexon/submit.js
```

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
