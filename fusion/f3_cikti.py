"""Fusion lab 3: tasarımı üretime ver — STEP (CAD değişimi), 3MF ve STL (3B baskı), F3D (Fusion arşivi).
Çıktı: C:\\users\\ubuntu\\fusion-out (Linux tarafında ~/.autodesk_fusion/wineprefixes/default/drive_c/users/ubuntu/fusion-out)."""
import adsk.core, adsk.fusion, os, json

OUT = r"C:\users\ubuntu\fusion-out"


def run(_context: str):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct); em = des.exportManager; root = des.rootComponent
    os.makedirs(OUT, exist_ok=True)
    govde = root.bRepBodies.itemByName("tepsi")
    em.execute(em.createSTEPExportOptions(os.path.join(OUT, "g1_cay_tepsisi.step"), root))
    st = em.createSTLExportOptions(govde, os.path.join(OUT, "g1_cay_tepsisi.stl"))
    st.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
    em.execute(st)
    em.execute(em.createC3MFExportOptions(govde, os.path.join(OUT, "g1_cay_tepsisi.3mf")))
    em.execute(em.createFusionArchiveExportOptions(os.path.join(OUT, "g1_cay_tepsisi.f3d"), root))
    up = des.userParameters
    print(json.dumps(dict(dosyalar={f: os.path.getsize(os.path.join(OUT, f)) for f in sorted(os.listdir(OUT)) if f.startswith("g1_cay")},
                          parametreler={up.item(i).name: up.item(i).expression for i in range(up.count)}), ensure_ascii=False))
