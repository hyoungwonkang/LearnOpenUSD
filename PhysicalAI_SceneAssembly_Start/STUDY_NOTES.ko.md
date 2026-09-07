# 학습 노트 — Assembling Digital Twins (Windows + Linux 코스)

진행표는 COURSE_PROGRESS_WIN_LINUX.ko.md, 여기는 **배운 개념 정리** 전용.

## 핵심 정의 (2026-09-06)

> **OpenUSD**는 3D 씬을 정의하는 언어이자 그 언어로 개발하는 프레임워크이고,
> **Omniverse**는 USD 씬을 렌더링하고, 물리 시뮬레이션하고, 협업할 수 있는
> NVIDIA의 플랫폼이다.

- OpenUSD = Universal **Scene** Description. 지오메트리만이 아니라 재질·조명·
  애니메이션·물리까지 "씬 전체"를 기술
- Omniverse는 USD를 네이티브 언어로 쓰는 앱 제작 플랫폼. 지금 쓰는 앱
  "Physical AI Learning"은 Omniverse Kit SDK로 조립된 앱(KAT)
- WSL에서 쓰는 usd-core(pxr 모듈) = OpenUSD 라이브러리 그 자체 (GUI 없이도 동작)

## OpenUSD가 디지털 트윈에 중요한 이유 4가지 (1-3)

1. **재사용** — 한 번 만든 라인을 여러 공장 레이아웃에서 reference로 재사용
2. **대규모 씬** — 인스턴싱으로 동일 기계 수천 대를 효율적으로 표현
3. **협업** — 파일 잠금 없이 여러 명이 각자 레이어에서 동시 작업
4. **비파괴 편집** — 원본은 그대로 두고 덧씌우기(over). 실험 후 즉시 되돌리기 가능

## 에셋 파일 구조: 포장지와 내용물 (1-4, 1-7)

```
N_03_Feeder.usd  (정본/인터페이스 파일, 가벼움 ~16KB)
└─ /World/_3_Feeder_Machine        ← 프림 껍데기 + 위치 + 물리 스키마
     └─ payload = @./Source/03_Feeder_Machine.usd@   ← 실제 지오메트리 (무거움 ~43MB)
```

- 씬/어셈블리는 항상 **정본 파일만** 참조. Source는 정본이 payload로 끌어옴
- `_edit.usd`, `_WIP.usd` = 작업 중간본. `asset_ ....usd` = 원천 데이터
- 명명 규칙: `N_03_Feeder`(라인의 3번 셀) ↔ `03_Feeder_Machine`(기계 원본)
- `over "..."` 블록 = payload로 불러온 내용 위에 덧씌우는 비파괴 수정
- 기계 프림에 붙은 PhysicsArticulationRootAPI = 관절(로봇) 물리 시뮬레이션용 스키마

## Reference vs Payload (1-3, 1-5)

- **Reference** — 항상 자동 로드. 구조/메타데이터 같은 가벼운 합성에 사용
- **Payload** — 켜고 끌 수 있는 reference. 무거운 지오메트리·재질에 사용
- Payload 언로드의 장점: 스테이지에서 데이터 제거 / 경로는 유지(빠른 재로드) /
  씬 다시 열면 자동 로드 / 내 세션에만 적용 / **GPU 메모리 해제** / 합성 성능 향상
- GUI: Stage 트리 아이콘(주황 화살표=reference, 파랑=payload),
  Property > Payloads 섹션 체크박스로 언로드/재로드. F키 = 선택 대상에 줌

## Kind — 프림의 기능적 역할 (1-7)

- **Component** = 최소 재사용 단위 (로봇 DRS40L, 버튼, 신호등)
- **Assembly** = 컴포넌트들의 묶음 (기계 한 대 = 생산 셀 하나 = assembly)
- 이 강의 데이터: 기계 프림(_3_Feeder_Machine 등)이 kind=assembly
- 올바른 kind → 스크립트가 에셋을 식별/그룹화, 검증·최적화 정확도, 유지보수성 향상

## 합성(Composition) 체감 포인트 (1-7)

- Property 패널의 값 = **여러 파일의 의견(opinion)을 합성한 결과**
- 예: kind=assembly는 정본 usda에는 없고 payload된 Source 파일 안에 있음
  → 텍스트 사본 한 장만 보면 일부만 보임. grep으로 안 나온다고 없는 게 아님

## 메타데이터 (1-7)

- 레이어(파일) 메타데이터: `metersPerUnit`, `upAxis`, `defaultPrim`
  (씬=cm(0.01), 기계=mm(0.001)로 수정함, upAxis=Z)
- 단위가 다른 파일을 조립하면 `xformOp:scale:unitsResolve`가 자동 보정 (mm→cm = 0.1배)
- 프림 메타데이터: Name, Kind
- 커스텀 속성(예: Unique_ID int): Property > Add > Attribute로 추가.
  **그 프림 하나에만** 생김. 전역 강제는 USD 스키마 필요
  - 용도: 대규모 씬 자동 추적/검색, 실물 재고·PLM 시스템 연동, 견고한 스크립팅

## 프로젝트 폴더 구조 원칙 (1-6)

- 이름은 구체적으로 (machine1 ✗ → N_03_Feeder ✓)
- 원본(Assets)과 작업물(Assemblies, Scenes) 분리
- **참조는 상대 경로** — 폴더째 옮겨도 동작 (맥→Windows 이동이 그대로 된 이유)
- 구조를 문서화 (이 노트와 진행표가 그 실천)

## 도구 사용법 (1-4, 1-5)

- Script Editor: Developer > Script Editor. print 출력은 에디터 상단 출력창에 표시
- 에셋 인벤토리 스크립트: `os.walk()`로 폴더 순회하며 .usd 나열
- 뷰포트: 스크롤=줌, 휠클릭 드래그=팬, F=선택 프림에 화면 맞춤
- 눈(👁) 아이콘 = 프림 가시성 토글
- 주의: 실습 중 Ctrl+S는 강의가 시키는 경우에만 (시작 데이터 청결 유지)

## Asset Validator (1-8)

- 열기: Window > Utilities > Asset Validator. 대상 Stage → Enable All → Analyze
- 결과: 오류(빨강)/경고(노랑)/통과(초록). 체커별로 펼쳐 프림·설명·수정 제안 확인
- **모델 계층 규칙**: model 프림(component/subcomponent/assembly)은 반드시
  kind가 group 또는 assembly인 프림의 직계 자식이어야 함
- KindChecker 체크 → Fix Selected = 계층을 따라가며 끊어진 kind 자동 수리
- N_05 실측: Source 파일엔 원래 kind 1,048개가 있었고, Fix는 **최상위 파일에
  12개만** 추가 (World=group, 기계=assembly, 로봇 link 체인=group) — 끊어진
  연결고리만 고침. 합성 결과 2,592 프림 중 group 498/component 579/assembly 1
- 검증 팁: Fix가 세션 레이어에 갈 수 있으니 저장 후 파일을 다시 열어 확인
- 분류(triage) 원칙: 사용을 막는 오류부터, 가벼운 경고는 나중에. 자주 돌릴 것
- AnchoredAssetPathsChecker("에셋은 자기 폴더 안에서 자급자족" 검사)의 지적은
  **고치지 않고 둠** — 중앙 재질 라이브러리(Assets/Material)를 기계 7대가
  공유하는 우리 설계와 충돌하는 규칙. 결함이 아니라 의도 (2-3에서 정식으로 다룸)
