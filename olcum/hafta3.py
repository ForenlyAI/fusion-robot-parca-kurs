#!/usr/bin/env python3
"""Hafta 3 · Baskıya Hazırlık — dışa aktarma biçimleri, dilimleme, Fusion ↔ dilimleyici kütlesi, baskı yönü.
Dosya boyları Fusion'ın yazdığı dosyalardan (OLCUMLER.json f3), dilimleme PrusaSlicer 2.7.2 özetinden (dilim/dilim_ozet.txt).
  python3 hafta3.py   → ekran/3.x/*.txt + *.png, OLCUMLER.json d3_* alanları"""
import re, zipfile
import numpy as np
import ortak as O

F = O.fusion()
tri = O.stl_oku()

# ---- 3.1 Dışa aktarma biçimleri ---------------------------------------------------------------------
ns = O.oturum("3.1", "dosya-oturumu", """
import re, zipfile
import ortak as O
boy = {"STEP": 40048, "STL": 104684, "3MF": 26070, "F3D": 142200}   # Fusion'ın yazdığı dosyalar (bayt)
{k: round(v / 1000) for k, v in boy.items()}                         # kilobayt
len(O.stl_oku("cikti/cay_tepsisi.stl"))                              # STL: yalnız üçgen
xml = zipfile.ZipFile("cikti/cay_tepsisi.3mf").read("3D/3dmodel.model").decode()
xml.count("<triangle "), re.search(r'unit="(\\w+)"', xml).group(1)   # 3MF: üçgen + birim
step = open("cikti/cay_tepsisi.step").read()
"ADVANCED_FACE" in step, step.count("CYLINDRICAL_SURFACE")          # STEP: gerçek yüzeyler
""")
boy = ns["boy"]
O.olc(d3_1_boy_kb={k: round(v / 1000) for k, v in boy.items()}, d3_1_stl_ucgen=len(tri), d3_1_3mf_ucgen=ns["xml"].count("<triangle "),
      d3_1_3mf_birim=re.search(r'unit="(\w+)"', ns["xml"]).group(1), d3_1_step_silindir=ns["step"].count("CYLINDRICAL_SURFACE"))

fig = O.sekil("Aynı tepsi, dört dosya · Fusion'ın dışa aktardığı boyutlar")
ax = fig.add_axes([0.12, 0.16, 0.5, 0.62])
renk = {"STEP": "#0F766E", "STL": "#C2410C", "3MF": "#1D4ED8", "F3D": "#7E22CE"}
k = list(boy)
ax.barh(k, [boy[x] / 1000 for x in k], color=[renk[x] for x in k])
for i, x in enumerate(k):
    ax.text(boy[x] / 1000 + 2, i, f"{round(boy[x] / 1000)} KB", va="center", fontsize=24)
ax.set_xlim(0, 175); ax.set_xlabel("kilobayt"); ax.invert_yaxis(); ax.spines[["top", "right"]].set_visible(False)
for i, s in enumerate(["STEP · gerçek yüzeyler, başka CAD'e", "STL · yalnız üçgen, birim yok", "3MF · üçgen + birim (mm), baskıya",
                       "F3D · Fusion arşivi, geçmişiyle"]):
    fig.text(0.66, 0.72 - i * 0.14, s, fontsize=24, color=renk[k[i]])
fig.text(0.66, 0.15, f"STL {len(tri)} üçgen · 3MF {ns['xml'].count('<triangle ')} üçgen", fontsize=21, color="#374151")
O.ekran_kaydet(fig, "3.1", "dosya-bicimleri", "OLCUMLER.json f3 + cikti/ klasörü")

# ---- 3.2 Dilimleme -----------------------------------------------------------------------------------
ozet = dict(re.findall(r"; (.+?) = (.+)", open(O.LAB / "dilim/dilim_ozet.txt").read()))
sure = ozet["estimated printing time (normal mode)"]
ayar = open(O.LAB / "dilim/dilimle.py").read()   # dilimleme ayarları (öğrenci deposundaki betiğin kopyası)
uc_c = int(re.search(r'"--temperature", "(\d+)"', ayar).group(1)); tabla_c = int(re.search(r'"--bed-temperature", "(\d+)"', ayar).group(1))
dk = sum(int(v) * {"h": 60, "m": 1, "s": 1 / 60}[u] for v, u in re.findall(r"(\d+)([hms])", sure))
ns = O.oturum("3.2", "dilim-oturumu", """
import re
ozet = dict(re.findall(r"; (.+?) = (.+)", open("dilim/dilim_ozet.txt").read()))   # PrusaSlicer 2.7.2 G-code sonu
ozet["layer_height"], ozet["fill_density"], ozet["fill_pattern"], ozet["perimeters"]
16 / float(ozet["layer_height"])                 # 16 mm kalınlık ÷ 0.2 mm katman
float(ozet["filament used [g]"]), round(float(ozet["filament used [mm]"]) / 1000, 1)   # g, metre
ozet["estimated printing time (normal mode)"]
""")
O.olc(d3_2_uc_c=uc_c, d3_2_tabla_c=tabla_c, d3_2_katman_mm=float(ozet["layer_height"]), d3_2_dolgu=ozet["fill_density"], d3_2_desen=ozet["fill_pattern"],
      d3_2_cevre=int(ozet["perimeters"]), d3_2_katman=round(16 / float(ozet["layer_height"])), d3_2_katman_dilim=F["dilim"]["katman"],
      d3_2_filament_g=float(ozet["filament used [g]"]), d3_2_filament_m=round(float(ozet["filament used [mm]"]) / 1000, 1),
      d3_2_sure=sure, d3_2_sure_dk=round(dk, 1), d3_2_codespace_g=F["dilim"]["codespace_bookworm"]["filament_g"],
      d3_2_codespace_dk=F["dilim"]["codespace_bookworm"]["baski_dk"],
      d3_2_codespace_fark_yuzde=round(abs(F["dilim"]["codespace_bookworm"]["filament_g"] / float(ozet["filament used [g]"]) - 1) * 100, 1))

# ---- 3.3 Fusion ↔ dilimleyici kütlesi -----------------------------------------------------------------
ns = O.oturum("3.3", "kutle-farki-oturumu", """
fusion, dilim = 187.4, 142.28                    # g: Fusion (dolu kabuk) · PrusaSlicer (%15 dolgu)
round(fusion - dilim, 1), round((1 - dilim / fusion) * 100, 1)   # fark (g, %)
round(dilim / 1.24, 1)                           # dilimleyicinin bastığı plastik (cm³)
yuk = dilim + 4 * 230
round(yuk), round((1 - yuk / 2000) * 100, 1)     # basılmış tepsiyle yük ve kalan pay (bardak ve sınır ÖRNEK)
""")
dilim_g = float(ozet["filament used [g]"])
O.olc(d3_3_fusion_g=F["f2"]["sonra_g"], d3_3_dilim_g=dilim_g, d3_3_fark_g=round(F["f2"]["sonra_g"] - dilim_g, 1),
      d3_3_fark_yuzde=round((1 - dilim_g / F["f2"]["sonra_g"]) * 100, 1), d3_3_dilim_cm3=round(dilim_g / O.PLA_G_CM3, 1),
      d3_3_yuk_g=round(dilim_g + 4 * O.BARDAK_G), d3_3_pay_yuzde=round((1 - (dilim_g + 4 * O.BARDAK_G) / O.KOL_SINIR_G) * 100, 1))

fig = O.sekil("Tepsinin kütlesi: tasarım → baskı")
ax = fig.add_axes([0.1, 0.16, 0.55, 0.62])
ad = ["dolu tasarım\n(Fusion)", "kabuklu tasarım\n(Fusion)", "baskı, %15 dolgu\n(PrusaSlicer)"]
yv = [F["f2"]["once_g"], F["f2"]["sonra_g"], dilim_g]
ax.bar(ad, yv, color=["#9CA3AF", "#1D4ED8", "#0F766E"], width=0.6)
for i, v in enumerate(yv):
    ax.text(i, v + 12, f"{O.tr(v, 1)} g", ha="center", fontsize=26)
ax.set_ylim(0, 820); ax.set_ylabel("gram"); ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="x", labelsize=19)
fig.text(0.69, 0.72, "Neden farklı?", fontsize=28, weight="bold")
for i, s in enumerate(["Fusion kabuk duvarını", "tamamen dolu sayar.", "Dilimleyici iki çevre +", "%15 gyroid dolgu basar.",
                       f"fark {O.tr(F['f2']['sonra_g'] - dilim_g, 1)} g · %{O.tr((1 - dilim_g / F['f2']['sonra_g']) * 100, 1)}"]):
    fig.text(0.69, 0.64 - i * 0.07, s, fontsize=24, color="#374151" if i < 4 else "#C2410C")
O.ekran_kaydet(fig, "3.3", "kutle-karsilastirma", "OLCUMLER.json f2 + dilim/dilim_ozet.txt")

# ---- 3.4 Baskı yönü ----------------------------------------------------------------------------------
ns = O.oturum("3.4", "yon-oturumu", """
import numpy as np, ortak as O
tri = O.stl_oku("cikti/cay_tepsisi.stl")
O.kutu(tri)                                      # Fusion: Y yukarı → boy Y'de 16 mm
R = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]) # X ekseninde 90° döndür (--rotate-x 90)
O.kutu(tri @ R.T)                                # şimdi kalınlık Z'de: dilimleyicinin yukarısı
round(208 / 0.2), round(16 / 0.2)                # döndürmeden ↔ döndürünce katman sayısı
""")
O.olc(d3_4_yukseklik_once_mm=208, d3_4_yukseklik_mm=16, d3_4_katman_once=1040, d3_4_katman=80, d3_4_dondurme="--rotate-x 90")

fig = O.sekil("Baskı yönü · dilimleyicinin yukarısı Z")
for j, (Rm, bas, renk) in enumerate([(np.eye(3), "döndürmeden: 208 mm yükseklik, 1.040 katman", "#C2410C"),
                                       (np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]), "X'te 90° döndürünce: 16 mm, 80 katman", "#0F766E")]):
    ax = fig.add_axes([0.04 + j * 0.49, 0.1, 0.44, 0.68])
    t = tri @ Rm.T
    k = O.kesit(t, 1, float(t[:, :, 1].mean()))   # önden kesit: X–Z
    for (a, b) in k:
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#1f2a37", lw=1.8)
    ax.axhline(t[:, :, 2].min(), color="#6B7280", lw=6)
    ax.text(0, t[:, :, 2].min() - 14, "baskı tablası", ha="center", fontsize=20, color="#6B7280")
    ax.set_aspect("equal"); ax.set_xlim(-130, 130); ax.set_ylim(-130, 130); ax.axis("off")
    ax.set_title(bas, fontsize=22, color=renk)
O.ekran_kaydet(fig, "3.4", "baski-yonu", "cikti/cay_tepsisi.stl döndürülüp kesildi")
print("hafta 3 tamam", sure, round(dk, 1))
