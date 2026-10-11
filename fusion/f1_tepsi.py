"""Fusion lab 1: G1 çay tepsisi — parametrik taban + dört bardak yuvası (ÖRNEK ölçüler).
Kullanıcı parametreleri: bardak_cap, yuva_derinlik, aralik, kalinlik, kenar. Fusion MCP ile çalıştırılır (fusion_mcp_execute/script)."""
import adsk.core, adsk.fusion, json

P = dict(bardak_cap="56 mm", yuva_derinlik="12 mm", aralik="90 mm", kalinlik="16 mm", kenar="14 mm", kose="10 mm")


def run(_context: str):
    app = adsk.core.Application.get()
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    des = adsk.fusion.Design.cast(app.activeProduct)
    des.designType = adsk.fusion.DesignTypes.ParametricDesignType
    up = des.userParameters
    for k, v in P.items():
        up.add(k, adsk.core.ValueInput.createByString(v), "mm", "")
    print("parametre", [up.item(i).name for i in range(up.count)])
    root = des.rootComponent
    sk = root.sketches.add(root.xZConstructionPlane)   # Fusion Y-yukarı: yatay düzlem XZ
    # taban: 2 × 2 bardak dizisi; boy = 2*aralik + 2*kenar (cm biriminde API) → çizgiyi ölçüyle bağla
    L = up.itemByName("aralik").value * 2 + up.itemByName("kenar").value * 2
    r = sk.sketchCurves.sketchLines.addCenterPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(L / 2, L / 2, 0))
    d = sk.sketchDimensions
    d.addDistanceDimension(r.item(0).startSketchPoint, r.item(0).endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
                           adsk.core.Point3D.create(0, -L / 2 - 1, 0)).parameter.expression = "2 * aralik + 2 * kenar"
    d.addDistanceDimension(r.item(1).startSketchPoint, r.item(1).endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
                           adsk.core.Point3D.create(L / 2 + 1, 0, 0)).parameter.expression = "2 * aralik + 2 * kenar"
    ext = root.features.extrudeFeatures.addSimple(sk.profiles.item(0), adsk.core.ValueInput.createByString("kalinlik"),
                                                 adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    govde = ext.bodies.item(0); govde.name = "tepsi"
    print("taban", round(L * 10, 1), "mm kare")
    # yuvalar: üst yüzde 4 daire, aralik kadar ara, yuva_derinlik kadar oyuk
    ust = max((f for f in govde.faces), key=lambda f: f.centroid.y)
    sk2 = root.sketches.add(ust)
    a = up.itemByName("aralik").value / 2; rr = up.itemByName("bardak_cap").value / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            c = sk2.sketchCurves.sketchCircles.addByCenterRadius(sk2.modelToSketchSpace(adsk.core.Point3D.create(sx * a, ust.centroid.y, sy * a)), rr)
            m = c.centerSketchPoint.geometry; sk2.sketchDimensions.addDiameterDimension(c, adsk.core.Point3D.create(m.x + rr * 1.3, m.y + rr * 0.4, 0)).parameter.expression = "bardak_cap"
    prof = adsk.core.ObjectCollection.create()
    for i in range(sk2.profiles.count):
        p = sk2.profiles.item(i)
        if p.areaProperties().area < 3.2 * rr * rr * 1.01:   # yalnız daire profilleri
            prof.add(p)
    ex2 = root.features.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
    ex2.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString("yuva_derinlik")),
                         adsk.fusion.ExtentDirections.NegativeExtentDirection)
    ex2.participantBodies = [govde]
    root.features.extrudeFeatures.add(ex2)
    # köşe yuvarlatma: dikey kenarlar
    kenarlar = adsk.core.ObjectCollection.create()
    for e in govde.edges:
        g = e.geometry
        if isinstance(g, adsk.core.Line3D) and abs(g.startPoint.y - g.endPoint.y) > 0.5 and abs(g.startPoint.x) > 0.1 and abs(g.startPoint.z) > 0.1:
            kenarlar.add(e)
    fi = root.features.filletFeatures.createInput(); fi.addConstantRadiusEdgeSet(kenarlar, adsk.core.ValueInput.createByString("kose"), True)
    root.features.filletFeatures.add(fi)
    pp = govde.physicalProperties
    print(json.dumps(dict(yuva=prof.count, hacim_cm3=round(pp.volume, 2), alan_cm2=round(pp.area, 2),
                          kutu_mm=[round((govde.boundingBox.maxPoint.x - govde.boundingBox.minPoint.x) * 10, 1),
                                   round((govde.boundingBox.maxPoint.y - govde.boundingBox.minPoint.y) * 10, 1),
                                   round((govde.boundingBox.maxPoint.z - govde.boundingBox.minPoint.z) * 10, 1)],
                          kutle_g_PLA=round(pp.volume * 1.24, 1),
                          dikey_kenar=kenarlar.count)))
    app.activeViewport.fit()
