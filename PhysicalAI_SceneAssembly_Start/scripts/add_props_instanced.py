# 3-1 + 3-2 손실습: 소품 추가와 인스턴싱 (TODO를 채워서 완성하세요)
# 실행: 저장소 루트에서  uv run python PhysicalAI_SceneAssembly_Start/scripts/add_props_instanced.py
#
# 목표: MyLine 앞쪽에 안전 펜스 기둥(MetalFencing_A1) 8개를 "인스턴스"로 배치
#   - 소품은 reference로 붙인다 (payload는 무거운 지오메트리용, 소품은 가벼우니 reference 관례)
#   - instanceable=True → 8개가 지오메트리 1벌(프로토타입)을 공유
#   - 주의: 펜스 에셋은 cm 단위(0.01), MyLine은 mm(0.001) → scale 보정 필요!

from pxr import Usd, UsdGeom, Gf

LINE = 'PhysicalAI_SceneAssembly_Start/Assemblies/MyLine.usda'
PROP = '../Factory/Assets/MetalFencing_A1.usd'   # MyLine.usda 기준 상대경로

stage = Usd.Stage.Open(LINE)
stage.RemovePrim('/World/Props')
before = sum(1 for _ in stage.Traverse())

props = UsdGeom.Scope.Define(stage, '/World/Props')   # 소품 전용 폴더(Scope)

for k in range(8):
    xf = UsdGeom.Xform.Define(stage, f'/World/Props/Fence_{k+1:02d}')
    prim = xf.GetPrim()

    # ── TODO 1: PROP 파일을 reference로 붙이기 ──────────────────
    # 힌트: payload 때는 prim.GetPayloads().AddPayload(경로) 였음 (build_my_line.py 참고)
    #       reference는 이름만 다른 같은 패턴
    prim.GetReferences().AddReference(PROP)

    # ── TODO 2: 인스턴싱 켜기 ───────────────────────────────────
    # 힌트: prim 의 메서드, SetInstanceable( ... )
    prim.SetInstanceable(True)

    # ── TODO 3: 위치와 크기 보정 ────────────────────────────────
    # 위치: x = -1200 (라인 앞), y = -3600 + k*1000 (1m 간격), z = 0
    # 힌트: xf.AddTranslateOp().Set(Gf.Vec3d( ... ))
    # 크기: cm 에셋 → mm 스테이지이므로 몇 배로 키워야 할까?
    # 힌트: xf.AddScaleOp().Set(Gf.Vec3f( ?, ?, ? ))
    xf.AddTranslateOp().Set(Gf.Vec3d(-1200, -3600 + k*1000, 0))
    xf.AddScaleOp().Set(Gf.Vec3f(10, 10, 10))

stage.GetPrimAtPath('/World/Props/Fence_05').SetInstanceable(False)
stage.Save()

# 측정 — 인스턴싱 효과를 숫자로 확인 (채울 것 없음, 결과 해석만)
after = sum(1 for _ in stage.Traverse())
protos = stage.GetPrototypes()
proxies = sum(1 for _ in stage.Traverse(Usd.TraverseInstanceProxies()))
print(f'추가 전 prim: {before}')
print(f'추가 후 prim: {after}')
print(f'프로토타입(공유 원본): {len(protos)}벌')
print(f'인스턴스 내부까지 세면: {proxies}')
