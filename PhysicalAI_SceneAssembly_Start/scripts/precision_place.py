# 2-6 실습: 정밀 배치 — 원본 CL6_Line_Full에서 역공학한 기준 좌표를 MyLine에 적용
# 실행: 저장소 루트에서  uv run python PhysicalAI_SceneAssembly_Start/scripts/precision_place.py
#
# 배경: 2-5의 "500mm 균일 간격"은 컨베이어가 끊기는 배치였음.
#       실제 라인은 기계끼리 맞닿거나(±수 mm) 돌출부가 겹치게 배치된다.
#       아래 좌표는 CL6_Line_Full.usd 의 배치를 그대로 추출한 값 (mm, Y축 방향 라인).

from pxr import Usd, UsdGeom, Gf

PLACEMENTS = {  # 원본 CL6_Line_Full 역공학 좌표
    'N_01_PCB_On_Board':  (192.7, -3817.2, 0.0),
    'N_02_PCB_Router':    (492.2, -1957.9, 0.0),
    'N_03_Feeder':        (604.2,  -758.9, 0.0),
    'N_04_PCB_Assembly':  (604.2,    -3.3, 0.0),
    'N_05_Assembly':      (604.2,   751.2, 0.0),
    'N_06_Test':          (604.2,  1505.8, 0.0),
    'N_07_Laser_Cutting': (604.2,  2110.5, 0.0),
}

stage = Usd.Stage.Open('PhysicalAI_SceneAssembly_Start/Assemblies/MyLine.usda')
for name, (x, y, z) in PLACEMENTS.items():
    xf = UsdGeom.Xformable(stage.GetPrimAtPath(f'/World/{name}'))
    # 기존 translate op를 찾아 값만 교체 (op를 중복 추가하지 않도록)
    ops = [op for op in xf.GetOrderedXformOps() if op.GetOpType() == UsdGeom.XformOp.TypeTranslate]
    op = ops[0] if ops else xf.AddTranslateOp()
    op.Set(Gf.Vec3d(x, y, z))
    print(f'{name:<22} -> ({x:7.1f}, {y:8.1f}, {z:4.1f})')
stage.Save()
print('\nMyLine.usda 정밀 배치 완료 (원본 CL6 기준 좌표 적용)')
