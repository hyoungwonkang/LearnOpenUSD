# 3-3 손실습: Scope로 에셋 그룹 정리 (TODO를 채워서 완성하세요)
# 실행: 저장소 루트에서  uv run python PhysicalAI_SceneAssembly_Start/scripts/organize_scopes.py
#
# 목표 (공식 Workflow Considerations 레슨의 실습):
#   /World 아래에 용도별 Scope 4개를 만들고, /World/Props 의 펜스 8개를
#   /World/SafetyEquipment 밑으로 옮긴다. 다른 Scope 3개는 나중을 위해 비워 둔다.
#
# 배경: USD에는 "prim 이동" 함수가 없다. 레이어에 적힌 내용(spec)을
#       새 경로로 복사(Sdf.CopySpec)한 뒤 옛 경로를 지우는 두 단계로 옮긴다.
#       복사는 spec 통째로이므로 instanceable, references, Fence_05의 빨간색 over까지 함께 간다.

from pxr import Usd, UsdGeom, Sdf

LINE = 'PhysicalAI_SceneAssembly_Start/Assemblies/MyLine.usda'
GROUPS = ['StorageAndLogistics', 'SafetyEquipment', 'MaterialHandling', 'Utilities']

stage = Usd.Stage.Open(LINE)
layer = stage.GetRootLayer()

# ── TODO 1: GROUPS 의 이름마다 /World/<이름> Scope 만들기 ──────────
# 힌트: 3-1에서 Props를 만들 때 쓴 함수 (add_props_instanced.py 18행)
for name in GROUPS:
    UsdGeom.Scope.Define(stage, f'/World/{name}')

# ── TODO 2: 펜스 8개를 Props → SafetyEquipment 로 복사 ──────────────
# 힌트: Sdf.CopySpec(원본레이어, 원본경로, 대상레이어, 대상경로)
#       원본·대상 레이어는 둘 다 layer, 경로는 문자열로 줘도 됨
#       예) '/World/Props/Fence_01' → '/World/SafetyEquipment/Fence_01'
#       펜스 이름은 Fence_01 ~ Fence_08 (f'Fence_{k:02d}')
for k in range(8):
    Sdf.CopySpec(layer, f'/World/Props/Fence_{k+1:02d}', layer, f'/World/SafetyEquipment/Fence_{k+1:02d}')
    

# ── TODO 3: 옛 /World/Props 지우기 ──────────────────────────────────
# 힌트: add_props_instanced.py 15행에서 쓴 함수
stage.RemovePrim('/World/Props')


stage.Save()

# 검증 (채울 것 없음) — 결과 해석만
s = Usd.Stage.Open(LINE)
for g in GROUPS:
    prim = s.GetPrimAtPath(f'/World/{g}')
    kids = [c.GetName() for c in prim.GetChildren()] if prim else '없음!'
    print(f'{g:<20} 타입={prim.GetTypeName() if prim else "-":<6} 자식={kids}')
print('Props 남아있나?', bool(s.GetPrimAtPath('/World/Props')))
m = s.GetPrimAtPath('/World/SafetyEquipment/Fence_05/MetalFencing_A1')
print('Fence_05 색:', m.GetAttribute('primvars:displayColor').Get() if m else '없음!')
print('prim 수:', sum(1 for _ in s.Traverse()), '/ 프로토타입:', len(s.GetPrototypes()), '벌')
