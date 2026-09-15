# 2-7 손실습: 커스텀 속성 붙이기 (TODO를 채워서 완성하세요)
# 실행: 저장소 루트에서  uv run python PhysicalAI_SceneAssembly_Start/scripts/add_custom_attrs.py
#
# 목표: MyLine.usda의 기계 7대에 자산 관리용 커스텀 속성 3개를 붙인다
#   inventory:assetId     (String)  "CL6-M01" ~ "CL6-M07"
#   inventory:station     (Int)     1 ~ 7  (공정 순서)
#   inventory:installDate (String)  "2026-09-10"

from pxr import Usd, Sdf

MACHINES = ['N_01_PCB_On_Board', 'N_02_PCB_Router', 'N_03_Feeder',
            'N_04_PCB_Assembly', 'N_05_Assembly', 'N_06_Test', 'N_07_Laser_Cutting']

stage = Usd.Stage.Open('PhysicalAI_SceneAssembly_Start/Assemblies/MyLine.usda')

for i, name in enumerate(MACHINES, start=1):   # i = 1, 2, ... 7
    prim = stage.GetPrimAtPath(f'/World/{name}')

    # ── TODO 1: assetId 속성 만들고 값 넣기 ─────────────────────
    # 힌트: prim.CreateAttribute('inventory:assetId', Sdf.ValueTypeNames.String)
    #       .Set() 에 넣을 문자열은 f'CL6-M{i:02d}' 형태로 만들 수 있음 (M01, M02...)
    prim.CreateAttribute('inventory:assetId', Sdf.ValueTypeNames.String).Set(f'CL6-M{i:02d}')

    # ── TODO 2: station 속성 (정수형!) ──────────────────────────
    # 힌트: 타입은 Sdf.ValueTypeNames.Int, 값은 i
    prim.CreateAttribute('inventory:station', Sdf.ValueTypeNames.Int).Set(i)

    # ── TODO 3: installDate 속성 ────────────────────────────────
    prim.CreateAttribute('inventory:installDate', Sdf.ValueTypeNames.String).Set('2026-09-15')

    print(f'{name}: 속성 3개 기록')

stage.Save()
print('저장 완료')
