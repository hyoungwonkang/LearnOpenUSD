# Assembling Digital Twins — 맥북 진행표

원본 강의: https://docs.nvidia.com/learning/physical-ai/assembling-digital-twins/latest/index.html
(원본은 Windows/Linux + RTX GPU에서 USD Composer(KAT)로 진행하는 강의. 이 진행표는
맥북에서 usd-core CLI/Python으로 재구성한 버전이며, 레슨 구분은 원본 목차를 참고해 재편성한 것)

작업 환경: `uv run python` / `uv run usdcat` / `uv run usdchecker` (저장소 루트에서 실행)
3D 확인: `usdcat --flatten` → `usdzip` → macOS 미리보기 (MDL 재질은 회색으로 표시됨)

## 진행 상황

### Module 1: 시작하기 — ✅ 완료 (2026-09-02)
- OpenUSD 기초: 레이어/스테이지, reference vs payload, defaultPrim, USDA 텍스트 포맷
- 폴더 구조: 에셋(Machine_USD) → 어셈블리(CL6_Line_Full) → 씬(SceneAssembly) 3단 계층
- 메타데이터 검토: 단위 불일치 발견 (머신 m 선언 / 라인 mm / 공장·씬 cm)
- 검증: usdchecker에서 GeomSubset familyType 'unrestricted' 규격 위반 발견 (CAD 변환 결함, 미수정)

### Module 2: 에셋 관리 모범 사례 — ◀ 진행 중
- [x] 2-1. 단위(metersPerUnit) 수정 — ✅ 완료 (2026-09-02)
  - 실측(BBoxCache)으로 기계 7대의 좌표 숫자가 mm임을 검증 (예: N_03_Feeder = 0.88×0.76×2.31m)
  - 7개 파일 metersPerUnit 1.0 → 0.001 수정 (지오메트리 무변경, 선언만 교정)
  - 백업: /private/tmp/claude-501/-Users-macrent-dev-LearnOpenUSD/b1a889fe-e754-4f83-87bb-00630a130742/scratchpad/backup_machine_usd/
  - 결과: 머신(mm)→라인(mm) 무보정, 라인(mm)→씬(cm) unitsResolve 0.1 로 전체 정합
- [x] 2-2. 머티리얼 검토 — ✅ 완료 (2026-09-02)
  - 중앙 라이브러리(Material.usd)에 재질 17종, MDL 파일 10개로 구현 (1 MDL → 다색 변형 subIdentifier)
  - N_03_Feeder 검토: Mesh 848개 중 421개 바인딩(1위 Aluminum_Brushed 311개), 427개 미바인딩
  - 미바인딩 중 291개는 visible 상태로 회색 렌더링됨 (미완성 dressing = Start 데이터 특성)
  - 라이브러리 밖 로컬 재질 1종 발견(material_U3A_... , Mesh 5개) → 2-4 교체 후보
- [x] 2-3. 중앙 머티리얼 라이브러리 — ✅ 완료 (2026-09-02)
  - 기계 7대 전부 /World/Material에 ../../Material/Material.usd 를 payload (단일 공유 라이브러리 확인)
  - 바인딩은 합성 후 씬 내부 경로(/World/Material/재질명)를 가리킴 → 라이브러리 수정 = 7대 동시 반영
  - 2-2의 '정체불명 재질' 정체 판명: SCARA 로봇 자체 재질(Delta_Blue.usd, 로봇 파란색) — 결함 아닌 벤더 번들
- [ ] 2-4. 머티리얼 교체 ◀ 다음
- [ ] 2-5. 생산 라인 조립 ★ 핵심 실습
- [ ] 2-6. 정밀 배치
- [ ] 2-7. 커스텀 속성

### Module 3: 씬 최적화와 데이터 통합 — 대기
- 소품 추가 / 인스턴싱 / 자산 목록 내보내기 / 내비게이션 웨이포인트

### Module 4: 마무리 — 대기

## 도구
- usdview 소스 빌드 완료 (2026-09-02, USD 25.11, Storm/Metal 렌더러)
  - 실행: `~/dev/usdview.sh <파일.usd>` (빌드: ~/dev/usd-install, venv: ~/dev/usdview-venv)
  - 빌드 마지막 codesign 단계는 전체 Xcode 부재로 실패했으나 실행에 지장 없음
  - MDL 재질은 표시 안 됨(회색), UsdPreviewSurface만 표시

## 메모
- SceneAssembly.usd에 defaultPrim 없음 (수정 후보)
- N_01 폴더의 _WIP/_edit 파일은 작업 중간본, 정본은 N_01_PCB_On_Board.usd
- 학습용 텍스트 사본: SceneAssembly.usda, N_03_Feeder.usda (씬은 원본 .usd를 사용)
