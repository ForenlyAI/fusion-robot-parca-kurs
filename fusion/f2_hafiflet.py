"""Fusion lab 2: tepsiyi alttan boşalt (Shell), kütle ve ağırlık merkezini ölç, robot yük bütçesiyle karşılaştır.
Önce f1_tepsi.py koşulmuş olmalı (aktif tasarım). Yük bütçesi ÖRNEK: G1 temel kol yükü ~2 kg (Unitree, duruşa göre değişir)."""
import adsk.core, adsk.fusion, json

PLA = 1.24          # g/cm³ (PLA, üretici veri sayfalarındaki tipik değer)
BARDAK_G = 230      # ÖRNEK: ince belli çay bardağı + tabak + çay
KOL_SINIR_G = 2000  # G1 temel model kol yükü ~2 kg


def olc(govde):
    pp = govde.physicalProperties
    m = pp.volume * PLA; c = pp.centerOfMass
    return dict(hacim_cm3=round(pp.volume, 1), kutle_g=round(m, 1), agirlik_merkezi_mm=[round(c.x * 10, 1), round(c.y * 10, 1), round(c.z * 10, 1)])


def run(_context: str):
    app = adsk.core.Application.get()
    des = adsk.fusion.Design.cast(app.activeProduct); root = des.rootComponent; up = des.userParameters
    govde = root.bRepBodies.itemByName("tepsi")
    once = olc(govde)
    if not up.itemByName("duvar"):
        up.add("duvar", adsk.core.ValueInput.createByString("2.4 mm"), "mm", "kabuk duvarı (0,4 mm nozul × 6)")
    alt = min((f for f in govde.faces), key=lambda f: f.centroid.y)
    yuzler = adsk.core.ObjectCollection.create(); yuzler.add(alt)
    si = root.features.shellFeatures.createInput(yuzler, False)
    si.insideThickness = adsk.core.ValueInput.createByString("duvar")
    root.features.shellFeatures.add(si)
    sonra = olc(govde)
    toplam = sonra["kutle_g"] + 4 * BARDAK_G
    r = dict(once=once, sonra=sonra, azalma_yuzde=round((1 - sonra["kutle_g"] / once["kutle_g"]) * 100, 1),
             dolu_tepsi_g=round(toplam), kol_siniri_g=KOL_SINIR_G, pay_yuzde=round((1 - toplam / KOL_SINIR_G) * 100, 1))
    # parametrik deneme: bardak çapı 56 → 60 mm, model kendini yeniden kurar mı?
    up.itemByName("bardak_cap").expression = "60 mm"
    r["cap60_kutle_g"] = olc(govde)["kutle_g"]
    up.itemByName("bardak_cap").expression = "56 mm"
    r["cap56_geri_kutle_g"] = olc(govde)["kutle_g"]
    r["zaman_cizelgesi"] = [des.timeline.item(i).entity.objectType.split("::")[-1] for i in range(des.timeline.count)]
    print(json.dumps(r, ensure_ascii=False))
    app.activeViewport.fit()
