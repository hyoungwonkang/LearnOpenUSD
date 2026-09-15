# 3-4 손실습: 자산 목록 내보내기 (TODO를 채워서 완성하세요)
# 실행: 저장소 루트에서  uv run python PhysicalAI_SceneAssembly_Start/scripts/export_inventory.py
#
# 목표: MyLine의 기계 7대에서 2-7 때 심은 inventory 속성들을 수확해 CSV로 저장
# 결과: PhysicalAI_SceneAssembly_Start/inventory.csv
#   assetId,station,installDate,machine,posX,posY
#   CL6-M01,1,2026-09-15,N_01_PCB_On_Board,192.7,-3817.2
#   ...

import csv
from pxr import Usd, UsdGeom

stage = Usd.Stage.Open('PhysicalAI_SceneAssembly_Start/Assemblies/MyLine.usda')

rows = []
for prim in stage.GetPrimAtPath('/World').GetChildren():
    # 소품(Props)이나 inventory 없는 prim은 건너뛰기
    if not prim.HasAttribute('inventory:assetId'):
        continue

    # ── TODO 1: 세 속성 값 읽기 ─────────────────────────────────
    # 힌트: prim.GetAttribute('inventory:assetId').Get()  → 'CL6-M01'
    asset_id = prim.GetAttribute('inventory:assetId').Get()
    station = prim.GetAttribute('inventory:station').Get()
    install = prim.GetAttribute('inventory:installDate').Get()

    # ── TODO 2: 기계 위치(translate) 읽기 ───────────────────────
    # 힌트: 2-6 역공학 때 배운 GetOrderedXformOps() 순회에서
    #       op.GetOpType() == UsdGeom.XformOp.TypeTranslate 인 op의 .Get()
    #       (x, y) 두 값만 쓰면 됨
    xf = UsdGeom.Xformable(prim)
    ops = [op for op in xf.GetOrderedXformOps() if op.GetOpType() == UsdGeom.XformOp.TypeTranslate]
    op = ops[0] if ops else xf.AddTranslateOp()
    pos = op.Get()

    rows.append([asset_id, station, install, prim.GetName(),
                 round(pos[0], 1), round(pos[1], 1)])

# ── TODO 3: station 순서로 정렬 ─────────────────────────────────
# 힌트: rows.sort(key=...)  — 각 row에서 station은 몇 번째 요소?


with open('PhysicalAI_SceneAssembly_Start/inventory.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['assetId', 'station', 'installDate', 'machine', 'posX', 'posY'])
    w.writerows(rows)

print(f'{len(rows)}대 기계 → inventory.csv 저장 완료')
