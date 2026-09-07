# Assembling Digital Twins — 정식 코스 진행표 (Windows + Linux)

원본 강의: https://docs.nvidia.com/learning/physical-ai/assembling-digital-twins/latest/
시작일: 2026-09-06

이전 맥북 진행(COURSE_PROGRESS_MAC.ko.md)은 usd-core CLI로 재구성한 변형이었음.
이 진행표는 **RTX GPU + Kit 앱이 구동되는 현재 환경에서 원본 강의 커리큘럼을
그대로 충실히 따라가는 새 코스**의 기록.

## 실습 환경
- Kit 앱: `C:\Users\hwplu\dev\Physical-AI-Learning-KAT` → `.\repo.bat launch`
- 에셋: `C:\Users\hwplu\dev\PhysicalAI_SceneAssembly_Start` (metersPerUnit 수정본 포함)
- 보조(CLI/Python 검증): WSL `~/LearnOpenUSD`에서 `uv run python` (usd-core 25.11)
  - 리눅스 wheel에는 usdcat/usdchecker CLI 없음 → Python API로 대체
- 주의: WSL2에서는 Kit 앱 실행 불가 (NVIDIA Vulkan 드라이버 미제공, CUDA/D3D12만
  패스스루) → GUI는 반드시 Windows 쪽에서 실행
- WSL 쪽 에셋도 동일 구성 (zip은 `unzip -n`으로 풀어 단위 수정본 보존)

---

## Module 1: Getting Started With Digital Twin Scene Assembly

- [x] 1-1. Overview — `getting-started/overview.html` (2026-09-06)
- [x] 1-2. Course Application Access — `getting-started/course-application-access.html`
  - 2026-09-06 완료: 에셋 zip + KAT 다운로드, Windows 빌드/실행, SceneAssembly.usd 오픈 확인
- [x] 1-3. OpenUSD Basics — `getting-started/openusd-basics.html` (2026-09-06)
- [x] 1-4. Asset Library Navigation — `getting-started/asset-library-navigation.html` (2026-09-06, Script Editor로 에셋 인벤토리 실습)
- [x] 1-5. Open Factory Environment — `getting-started/open-factory-environment.html` (2026-09-06, F키 줌·Roof 숨기기·Payload 언로드 실습. Factory.usd에 카메라/visibility 잔여 기록 저장됨 — 무해)
- [x] 1-6. Project Folder Structure — `getting-started/project-folder-structure.html` (2026-09-06)
- [x] 1-7. Asset Metadata Review — `getting-started/asset-metadata-review.html` (2026-09-06, N_05에 Kind=assembly 확인, Unique_ID=105001 추가·저장. WSL 원본에 반영됨)
- [x] 1-8. Asset Validator Troubleshooting — `getting-started/asset-validator-troubleshooting.html` (2026-09-07, N_05 분석 → KindChecker Fix Selected → kind 의견 12개 저장 검증)
- [ ] 1-9. Workspace Preferences — `getting-started/workspace-preferences.html`

## Module 2: Best Practices for Managing Given Assets

- [ ] 2-1. Managing Given Assets — `materials-assembly/managing-given-assets.html`
- [ ] 2-2. Review Asset Materials — `materials-assembly/review-asset-materials.html`
- [ ] 2-3. Centralized Materials Library — `materials-assembly/centralized-materials-library.html`
- [ ] 2-4. Replace Asset Materials — `materials-assembly/replace-asset-materials.html`
- [ ] 2-5. Assemble Production Line — `materials-assembly/assemble-production-line.html` ★ 핵심 실습
- [ ] 2-6. Precision Machine Placement — `materials-assembly/precision-machine-placement.html`
- [ ] 2-7. Configuring Custom Attributes — `materials-assembly/configuring-custom-attributes.html`

## Module 3: Scene Optimization and Data Integration

- [ ] 3-1. Adding Props to the Stage — `optimization-data/adding-props-stage.html`
- [ ] 3-2. Instancing Best Practices — `optimization-data/instancing-best-practices.html`
- [ ] 3-3. Workflow Considerations — `optimization-data/workflow-considerations.html`
- [ ] 3-4. Asset Inventory Export — `optimization-data/asset-inventory-export.html`
- [ ] 3-5. Setup Navigation Waypoints — `optimization-data/setup-navigation-waypoints.html`

## Module 4: What's Next

- [ ] 4-1. What's Next — `whats-next.html`

---

## 참고
일부 레슨은 맥북에서 명령어 방식으로 미리 공부한 적이 있지만,
이번 코스는 복습을 겸해 처음부터 끝까지 순서대로 전부 진행한다.
(맥북에서 했던 기록은 COURSE_PROGRESS_MAC.ko.md 참고)

## 진행 메모
(레슨 완료 시 날짜와 특이사항을 여기에 기록)
- 2026-09-06: 환경 구축 완료 (1-2). 상세(빌드 과정·트러블슈팅)는 위 실습 환경 섹션 참고.
