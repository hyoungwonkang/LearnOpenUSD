# 2-4 보충 실습: 경로 조건을 건 머티리얼 재바인딩
# 실행: 저장소 루트에서  uv run python PhysicalAI_SceneAssembly_Start/scripts/rebind_robot_covers.py
# 하는 일: N_05에서 주황(Steel_Painted_Orange)이 된 Mesh 중
#          로봇(/World/DRS40L) 아래에 있는 것"만" 흰색(Paint_Eggshell_White)으로 원복

from pxr import Usd, UsdShade

ASSET = 'PhysicalAI_SceneAssembly_Start/Assets/Machine_USD/N_05_Assembly/N_05_Assembly.usd'
SCOPE = '/World/DRS40L'                # ← 경로 조건 (이 아래만 건드림)
FROM_MAT = 'Steel_Painted_Orange'      # 이 재질이 붙어 있고
TO_MAT = '/World/Material/Paint_Eggshell_White'  # 이걸로 바꾼다

stage = Usd.Stage.Open(ASSET)
white = UsdShade.Material(stage.GetPrimAtPath(TO_MAT))

changed = []
for prim in stage.Traverse():
    if prim.GetTypeName() != 'Mesh':
        continue
    mat, _ = UsdShade.MaterialBindingAPI(prim).ComputeBoundMaterial()
    if (mat and mat.GetPrim().GetName() == FROM_MAT
            and str(prim.GetPath()).startswith(SCOPE)):   # ← 배운 그 if문
        UsdShade.MaterialBindingAPI.Apply(prim).Bind(white)
        changed.append(str(prim.GetPath()))

stage.GetRootLayer().Save()

print(f'{len(changed)}개 Mesh를 {FROM_MAT} -> Paint_Eggshell_White 로 원복:')
for p in changed:
    print(' ', p)
