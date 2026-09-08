# 2-5 실습: 생산 라인 어셈블리를 처음부터 작성
# 실행: 저장소 루트에서  uv run python PhysicalAI_SceneAssembly_Start/scripts/build_my_line.py
# 결과: Assemblies/MyLine.usda (텍스트 포맷 — 열어서 읽을 수 있음)
#
# 하는 일:
#   1. 기계 7대 각각의 바운딩 박스를 실측
#   2. X축을 따라 공정 순서(N_01→N_07)로, 기계 사이 500mm 간격으로 배치
#   3. 규격을 지킨 어셈블리 작성: Z-up, mm 단위, defaultPrim, kind=assembly

from pxr import Usd, UsdGeom, Gf

MACHINES = ['N_01_PCB_On_Board', 'N_02_PCB_Router', 'N_03_Feeder',
            'N_04_PCB_Assembly', 'N_05_Assembly', 'N_06_Test', 'N_07_Laser_Cutting']
BASE = 'PhysicalAI_SceneAssembly_Start'
OUT = f'{BASE}/Assemblies/MyLine.usda'
GAP = 500.0  # 기계 사이 간격 (mm)

# ── 1. 각 기계의 바운딩 박스 실측 ──────────────────────────────
bboxes = {}
cache_time = Usd.TimeCode.Default()
for name in MACHINES:
    src = Usd.Stage.Open(f'{BASE}/Assets/Machine_USD/{name}/{name}.usd')
    cache = UsdGeom.BBoxCache(cache_time, ['default', 'render'])
    r = cache.ComputeWorldBound(src.GetPrimAtPath('/World')).ComputeAlignedRange()
    bboxes[name] = (r.GetMin(), r.GetMax())
    size = r.GetSize()
    print(f'{name:<22} 폭(X) {size[0]:7.0f}mm  깊이(Y) {size[1]:7.0f}mm')

# ── 2. 새 스테이지 작성 (규격부터 제대로) ──────────────────────
stage = Usd.Stage.CreateNew(OUT)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)   # Z-up (이 프로젝트 규약)
UsdGeom.SetStageMetersPerUnit(stage, 0.001)        # mm (2-1에서 정합화한 단위)

world = UsdGeom.Xform.Define(stage, '/World')
stage.SetDefaultPrim(world.GetPrim())              # SceneAssembly.usd가 빼먹은 그것!
Usd.ModelAPI(world.GetPrim()).SetKind('assembly')  # 모델 계층: 이 파일은 어셈블리

# ── 3. 기계들을 payload로 불러와 X축으로 순서대로 배치 ─────────
cursor = 0.0  # 다음 기계의 왼쪽 끝이 놓일 X 좌표
for name in MACHINES:
    prim = UsdGeom.Xform.Define(stage, f'/World/{name}')
    prim.GetPrim().GetPayloads().AddPayload(f'../Assets/Machine_USD/{name}/{name}.usd')
    lo, hi = bboxes[name]
    # 기계 원점이 bbox 중앙이 아닐 수 있으므로, "왼쪽 끝을 cursor에 맞추는" 이동량을 계산
    tx = cursor - lo[0]
    ty = -lo[1]  # 앞면(Y 최소)을 y=0 라인에 정렬
    prim.AddTranslateOp().Set(Gf.Vec3d(tx, ty, 0.0))
    print(f'배치: {name:<22} translate=({tx:8.0f}, {ty:6.0f}, 0)')
    cursor += (hi[0] - lo[0]) + GAP

stage.Save()
print(f'\n저장 완료: {OUT}')
print(f'라인 전체 길이: {cursor - GAP:.0f}mm (= {(cursor - GAP)/1000:.1f}m)')
