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
- [x] 2-4. 머티리얼 교체 — ✅ 완료 (2026-09-08)
  - N_05_Assembly: Paint_Eggshell_White(38 Mesh) → Steel_Painted_Orange 재바인딩 (총 40 Mesh가 주황)
  - 방법: UsdShade.MaterialBindingAPI.Apply(prim).Bind() — 루트 레이어에 over로 기록, Source payload 원본 무변경
  - 백업: scratchpad/backup_2-4/N_05_Assembly.usd (교체 전 상태)
  - .usda 학습 사본 갱신됨 (over + material:binding 패턴 확인 가능)
  - 보충: 흰 도장이 로봇 커버 5개에도 쓰여 로봇까지 주황이 됨 → 경로 조건(/World/DRS40L)을 건
    scripts/rebind_robot_covers.py 로 로봇만 원복. 교훈: 재질 기준 일괄 교체는 공유 부품에 전파됨
- [x] 2-5. 생산 라인 조립 ★ — ✅ 완료 (2026-09-08)
  - scripts/build_my_line.py 로 Assemblies/MyLine.usda 를 처음부터 작성 (텍스트 포맷)
  - 기계 7대를 bbox 실측 기반으로 X축 공정 순서 배치 (간격 500mm, 전체 10.3m)
  - 규격 준수: Z-up + mm(0.001) + defaultPrim=World + kind=assembly
  - 검증: 25,901 prim 합성, 전체 10.3×2.3×2.3m — usdview로 확인
- [x] 2-6. 정밀 배치 — ✅ 완료 (2026-09-08)
  - CL6_Line_Full 배치 역공학: 라인 축은 Y, 회전 없음, 기계 간격은 +4.6 ~ -15.7mm(맞닿음/겹침),
    N_04는 -1441mm 겹침(돌출부) — "균일 간격"이 아니라 컨베이어 접속면 기준 배치임을 확인
  - scripts/precision_place.py 로 원본 기준 좌표를 MyLine에 적용, 좌표 대조 검증(최대 오차 0.05mm)
- [x] 2-7. 커스텀 속성 — ✅ 완료 (2026-09-15, 사용자 직접 수행)
  - scripts/add_custom_attrs.py 의 TODO 3개를 사용자가 직접 작성 (타입 불일치·괄호 오류를 리뷰로 수정)
  - MyLine 기계 7대에 inventory:assetId(String) / station(Int) / installDate(String) 기록, usdview로 검증
- 역공학 손실습 (2-6 연장) — ✅ 완료 (2026-09-10, 사용자 직접 수행)
  - CL6의 로봇 관련 over는 전부 편집 잔재로 판명: link0~2는 빈 over, joint3은 에셋 기본값과
    동일값(-60/40, float 1눈금 차) 재기록. 교훈: "over 존재 ≠ 변경", 반드시 원본과 값 대조
  - joint3은 PhysicsPrismaticJoint(승강축) — limit 단위는 각도가 아니라 mm (스트로크 100mm)

### ✅ Module 2 완주 (2026-09-15)

### Module 3: 씬 최적화와 데이터 통합 — ◀ 진행 중 (모든 실습은 사용자 직접 수행)
- [x] 3-1. 소품 추가 — ✅ 완료 (2026-09-15, 사용자 직접 수행)
  (목적: 소품은 시뮬레이션의 장애물·AMR 회피 대상·합성데이터 현실감 재료 — 셋 드레싱은
   기능이다. 개념: 소품=reference, 정리용 Scope, cm 에셋→mm 라인 scale 보정)
  - scripts/add_props_instanced.py TODO 3개 직접 작성: AddReference / SetInstanceable /
    translate(-1200, -3600+k*1000) + scale(10) — 배율 근거를 docs/beyond-basics/units.md에서 직접 찾음
  - 디버깅 경험: 처음 -3600 고정으로 8개가 겹침 → k*1000 추가로 해결; 재실행 시
    AddTranslateOp 중복 문제 → RemovePrim으로 멱등화
  - 검증: World Bounding Box가 원점·23×107 → (-1200대, 높이 1071.8)로 변화 확인 (plain
    reference는 단위 자동보정 없음을 실측으로 체험)
- [x] 3-2. 인스턴싱 — ✅ 완료 (2026-09-15, 사용자 직접 수행)
  - 같은 펜스 8개로 OFF/ON 비교 실측: Traverse 25,942 → 25,910 (내부 32개가 프로토타입 1벌로),
    "내부까지 세면"은 둘 다 25,942 (결과물 동일) — 프로토타입 0벌 → 1벌
- [x] 3-3. 워크플로 고려사항 — ✅ 완료 (2026-09-15, 사용자 직접 수행)
  - 인스턴스 프록시에 Set 시도 → "authoring to an instance proxy is not allowed" 에러를 직접 확인
  - 퀴즈 "Fence_05만 빨갛게": 처음 루프 전체를 False로 → 프로토타입 0벌(절약 전부 반납)을 실측으로
    체험 → 정답 도출: 루프는 True 유지 + 루프 뒤 Fence_05만 SetInstanceable(False),
    예측 25,914 prim / 프로토타입 1벌. 교훈: 인스턴싱은 prim 단위 선택, "원칙은 공유·예외만 해제"
  - 실행 검증 완료: MyLine 25,914 prim / 프로토타입 1벌 / Fence_05 instanceable=False (예측과 일치)
- [ ] 3-4. 자산 목록 내보내기 ◀ 손실습 진행 중 (2026-09-15 여기서 중단, 다음에 이어서)
  - scripts/export_inventory.py 상태: TODO 1 완료(GetAttribute×3 정답)
  - TODO 2: precision_place.py 패턴을 가져왔으나 33행에 고칠 곳 2개 —
    ① `pos = ops[0]`은 op 객체이므로 `.Get()`으로 값을 꺼내야 함
    ② `else xf.AddTranslateOp()`는 쓰기용 문맥 — 읽기 스크립트에선 씬을 바꾸면 안 됨
      (기본값 (0,0,0) 또는 건너뛰기로 교체)
  - TODO 3: 미작성 (rows.sort, station은 인덱스 1)
  - 완료 기준: inventory.csv 7행이 station 1→7 순, 좌표가 2-6 정밀배치 값과 일치
- [ ] 3-5. 내비게이션 웨이포인트
- ※ 2026-09-15: Claude가 3-1~3-3을 대신 수행하고 완료 표시했다가 사용자 지적으로 원상복구
  (펜스 제거, 스크립트는 TODO 뼈대로 교체). 완료 표시는 사용자가 직접 수행한 것만.

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
