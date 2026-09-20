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

## ⚠️ 학습 규칙 (2026-09-15 추가, 맥 트랙 경험에서)
**GUI 실습만 하지 말고, 매 레슨마다 usda 코드를 같이 볼 것.** 지금까지 NVIDIA 강의 화면만
따라가고 파일 내부를 안 봤는데, 맥 트랙에서 배운 핵심(over 잔재 판별, 바인딩 경로, custom
속성, float 부스러기)은 전부 usda 텍스트를 직접 읽어야 보이는 것들이었음. 레슨마다:
1. GUI에서 조작한 뒤 → 그 결과가 **어느 파일에 무엇으로 기록됐는지** usda로 확인
   - Windows: `usdcat 파일.usd | more` 또는 usdview의 Layer Stack/Composition 탭
   - WSL: `uv run python` + `Usd.Stage.Open(...).GetRootLayer().ExportToString()` 일부 출력
2. 수정 전/후 값을 대조 (over가 생겼는지, 어느 레이어에 적혔는지)
3. 새로 본 키워드(def/over/payload/custom 등)는 STUDY_NOTES.ko.md에 정리

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
- [x] 1-9. Workspace Preferences — `getting-started/workspace-preferences.html` (2026-09-14, 05_Assembly_Machine.usd에서 큐브 1unit→mpu 0.001 변경→1000unit 확인. NVIDIA Assets 탭은 이 KAT 빌드에 없음(omni.kit.browser.asset 미포함) → Factory/Assets/MetalFencing_A1.usd(cm) 드래그로 대체, unitsResolve=10 확인. 파일 미저장)

## Module 2: Best Practices for Managing Given Assets

- [x] 2-1. Managing Given Assets — `materials-assembly/managing-given-assets.html` (2026-09-20 완료. 읽기 레슨: 명명/폴더/버전, 상대경로·참조, reference vs payload 3단 워크플로. usda 사본 11개 생성 후 SceneAssembly→Factory/CL6=references(주황), CL6→기계 7대=payload(파랑), 기계 7대→../../Material/Material.usd 공유 구조를 사용자가 직접 줄 번호로 확인)
- [x] 2-2. Review Asset Materials — `materials-assembly/review-asset-materials.html` (2026-09-20. N_02 열기→Grey Studio→Mesh_0 선택→바인딩 Paint_Eggshell_White→Go To→Material 우클릭 Find in Content Browser로 Assets/Material/Material.usd 확인. usda 대조 후 사용자가 N_02_PCB_Router.usda 1210행 바인딩을 Steel_Painted_Orange로 직접 편집 → .usd 변환·Windows 반영 → Kit에서 주황 확인. 원복 안 함. 백업 scratchpad/backup_2-2)
- [x] 2-3. Centralized Materials Library — `materials-assembly/centralized-materials-library.html` (2026-09-20. Empty 템플릿→Assets/Material/MaterialLibrary.usd 저장, /World/Looks(Scope)에 Materials 탭에서 m_PolishedSteel/m_Blue_Paint/m_Terrazzo 추가. usda 사본 확인: MDL은 NVIDIA 클라우드 URL, Looks 스코프에 드래그 부작용 material:binding→m_Terrazzo 잔재 발견(Scope라 GUI엔 안 보임) — 무해하여 그대로 둠. 파일은 cm/Y-up이나 재질 전용이라 무관)
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
- 2026-09-14: Module 1 완료 (1-9). KAT 실행은 WSL에서 `cmd.exe /c start ... physical_ai_learning.kit.bat`로 가능. GPU HUD에서 8GB 카드 메모리 5GB+ 사용 확인 → 큰 씬은 payload 언로드 습관 필요.
