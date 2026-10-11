#!/usr/bin/env python3
"""Hafta 1 · Parametrik Tepsi — Fusion'ın ölçtüğü tepsiyi (f1_tepsi.py) parametrelerden ve dışa aktarılan STL'den yeniden hesaplar.
  python3 hafta1.py   → ekran/1.x/*.txt + *.png, OLCUMLER.json d1_* alanları"""
import math
import numpy as np
import matplotlib.pyplot as plt
import ortak as O

F = O.fusion()
tri = O.stl_oku()

# ---- 1.1 Fusion ve robot parçası: eksenler ve birim -------------------------------------------------
ns = O.oturum("1.1", "eksen-oturumu", """
import ortak as O
tri = O.stl_oku("cikti/cay_tepsisi.stl")   # Fusion'ın dışa aktardığı tepsi (mm)
len(tri)                                   # üçgen sayısı
kutu = O.kutu(tri)                         # X, Y, Z yönünde boy (mm)
kutu
"XYZ"[int(kutu.argmin())]                  # en ince yön = kalınlık = Fusion'da yukarı ekseni
tri[:, :, 1].min(), tri[:, :, 1].max()     # taban Y = 0'da, üst yüz Y = 16'da
""")
kutu = ns["kutu"]
O.olc(d1_1_ucgen=len(tri), d1_1_kutu_mm=kutu, d1_1_yukari="Y", d1_1_birim="mm")

# ---- 1.2 Kullanıcı parametreleri ----------------------------------------------------------------------
P = dict(bardak_cap=56, aralik=90, kalinlik=16, kenar=14, kose=10, yuva_derinlik=12, duvar=2.4)
ns = O.oturum("1.2", "parametre-oturumu", """
P = dict(bardak_cap=56, aralik=90, kalinlik=16, kenar=14, kose=10, yuva_derinlik=12, duvar=2.4)   # f1 + f2 (mm)
len(P)                                        # kullanıcı parametresi sayısı
boy = 2 * P["aralik"] + 2 * P["kenar"]        # Fusion ifadesi: 2 * aralik + 2 * kenar
boy
P["aralik"] - P["bardak_cap"]                 # iki yuva arasında kalan et (mm)
P["kenar"] + (P["aralik"] - P["bardak_cap"]) / 2   # yuva kenarından tepsi kenarına (mm)
P["kalinlik"] - P["yuva_derinlik"]            # yuvanın altında kalan taban (mm)
""")
O.olc(d1_2_parametre=len(P), d1_2_parametreler=P, d1_2_boy_mm=ns["boy"], d1_2_yuva_arasi_mm=P["aralik"] - P["bardak_cap"],
      d1_2_kenar_payi_mm=P["kenar"] + (P["aralik"] - P["bardak_cap"]) / 2, d1_2_yuva_alti_mm=P["kalinlik"] - P["yuva_derinlik"],
      d1_2_stl_boy_mm=float(kutu[0]))

# parametre şeması: üst görünüş (STL'in üst yüz kesiti) + parametre adları
def ust_kesit(ax, y, dis=False):
    k = O.kesit(tri, 1, y)
    if dis:   # yalnız dış çevre (kabuğun iç duvarı ve yuvalar çizilmez)
        def dis_mi(s):
            m = np.abs(s.mean(axis=0))
            if m[0] > 94 and m[1] > 94:   # köşe yayı: dış yay R10, iç duvar yayı daha küçük
                return np.hypot(m[0] - 94, m[1] - 94) > 8.8
            return m.max() > 102.8
        k = [s for s in k if dis_mi(s)]
    for (a, b) in k:
        ax.plot([a[0], b[0]], [a[1], b[1]], color="#1f2a37", lw=2.2)
    ax.set_aspect("equal"); ax.axis("off")

fig = O.sekil("Tepsinin üst yüzü ve parametreler · cay_tepsisi.stl")
ax = fig.add_axes([0.05, 0.05, 0.6, 0.78]); ust_kesit(ax, 15.9)
a = P["aralik"] / 2
ax.annotate("", (-104, -118), (104, -118), arrowprops=dict(arrowstyle="<->", lw=2, color="#C2410C"))
ax.text(0, -128, "2 × aralik + 2 × kenar = 208", ha="center", va="top", fontsize=22, color="#C2410C")
ax.annotate("", (-a, 0), (a, 0), arrowprops=dict(arrowstyle="<->", lw=2, color="#1D4ED8"))
ax.text(0, 4, "aralik = 90", ha="center", fontsize=20, color="#1D4ED8")
ax.annotate("", (a - 28, a), (a + 28, a), arrowprops=dict(arrowstyle="<->", lw=2, color="#0F766E"))
ax.text(a, a + 32, "bardak_cap = 56", ha="center", fontsize=20, color="#0F766E")
ax.annotate("", (104, -a), (104 - 14, -a), arrowprops=dict(arrowstyle="<->", lw=2, color="#7E22CE"))
ax.text(108, -a, "kenar = 14", ha="left", va="center", fontsize=20, color="#7E22CE")
ax.set_xlim(-130, 170); ax.set_ylim(-140, 130)
fig.text(0.68, 0.74, "Kullanıcı parametreleri (mm)", fontsize=26, weight="bold")
for i, (k, v) in enumerate(P.items()):
    fig.text(0.68, 0.67 - i * 0.065, f"{k:<14s} {O.tr(v, 1 if v != int(v) else 0)}", fontsize=26, family="DejaVu Sans Mono")
O.ekran_kaydet(fig, "1.2", "parametre-semasi", "cikti/cay_tepsisi.stl üst yüz kesiti")

# ---- 1.3 Çizim ve kalınlık verme --------------------------------------------------------------------
blok = 208 * 208 * 16
O.olc(d1_3_taban_mm=[208, 208], d1_3_kalinlik_mm=16, d1_3_blok_cm3=blok / 1000, d1_3_blok_g=blok / 1000 * O.PLA_G_CM3)
fig = O.sekil("Kalınlık verilmiş taban · üst görünüş, köşeler R10")
ax = fig.add_axes([0.05, 0.05, 0.6, 0.78]); ust_kesit(ax, 0.1, dis=True)
ax.annotate("", (-104, -116), (104, -116), arrowprops=dict(arrowstyle="<->", lw=2, color="#C2410C"))
ax.text(0, -124, "208 mm", ha="center", va="top", fontsize=24, color="#C2410C")
ax.annotate("", (118, -104), (118, 104), arrowprops=dict(arrowstyle="<->", lw=2, color="#C2410C"))
ax.text(124, 0, "208 mm", ha="left", va="center", fontsize=24, color="#C2410C", rotation=90)
ax.set_xlim(-130, 160); ax.set_ylim(-140, 120)
fig.text(0.68, 0.72, "Taban kesiti (Y = 0)", fontsize=24, weight="bold")
for i, s in enumerate(["çizim düzlemi: XZ (yatay)", "kalınlık: 16 mm (Y yönünde)", f"dolu blok: {O.tr(blok / 1000, 1)} cm³",
                       "köşe yuvarlatma: R10", "ölçüler ÖRNEK"]):
    fig.text(0.68, 0.64 - i * 0.07, s, fontsize=24)
O.ekran_kaydet(fig, "1.3", "taban-olculu", "cikti/cay_tepsisi.stl taban kesiti")

# ---- 1.4 Yuva ve yuvarlatma: hacmi elle hesapla, Fusion'la karşılaştır -------------------------------
ns = O.oturum("1.4", "hacim-oturumu", """
import math
blok = 208 * 208 * 16                          # dolu kare blok (mm³)
kose = 4 * (10**2 - math.pi * 10**2 / 4) * 16  # dört köşe yuvarlatmasının aldığı (mm³)
yuva = 4 * math.pi * 28**2 * 12                # dört yuva: Ø56, derinlik 12 (mm³)
round((blok - kose - yuva) / 1000, 2)          # elle hesap (cm³)
fusion = 572.63                                # Fusion physicalProperties.volume (f1_tepsi.py)
round(abs((blok - kose - yuva) / 1000 - fusion) / fusion * 100, 3)   # fark (%)
""")
el = ns["blok"] - ns["kose"] - ns["yuva"]
O.olc(d1_4_yuva=F["f1"]["yuva"], d1_4_yuva_cm3=ns["yuva"] / 1000, d1_4_kose_cm3=ns["kose"] / 1000, d1_4_el_cm3=el / 1000,
      d1_4_fusion_cm3=F["f1"]["hacim_cm3"], d1_4_fark_yuzde=abs(el / 1000 - F["f1"]["hacim_cm3"]) / F["f1"]["hacim_cm3"] * 100)

# yuva kesiti: dolu tepsinin hesaplanmış kesiti (Fusion'da kabuktan önceki hâl) — Z = 45 düzlemi, iki yuvanın ortasından
fig = O.sekil("Dolu tepsinin kesiti · iki yuvanın ortasından (Z = 45)")
ax = fig.add_axes([0.05, 0.12, 0.9, 0.62])
x = [-104, -73, -73, -17, -17, 17, 17, 73, 73, 104, 104, -104, -104]
y = [16, 16, 4, 4, 16, 16, 4, 4, 16, 16, 0, 0, 16]
ax.fill(x, y, color="#E5E7EB", ec="#1f2a37", lw=2.5, hatch="//")
ax.annotate("", (73, 20), (17, 20), arrowprops=dict(arrowstyle="<->", lw=2, color="#0F766E"))
ax.text(45, 21, "Ø56", ha="center", va="bottom", fontsize=24, color="#0F766E")
ax.annotate("", (78, 16), (78, 4), arrowprops=dict(arrowstyle="<->", lw=2, color="#C2410C"))
ax.text(80, 10, "12", va="center", fontsize=24, color="#C2410C")
ax.annotate("", (-78, 4), (-78, 0), arrowprops=dict(arrowstyle="<->", lw=2, color="#7E22CE"))
ax.text(-76, 2, "4", va="center", fontsize=24, color="#7E22CE")
ax.set_aspect(2.2); ax.set_xlim(-112, 112); ax.set_ylim(-3, 26); ax.axis("off")
fig.text(0.05, 0.08, f"elle hesap {O.tr(el / 1000, 2)} cm³ · Fusion {O.tr(F['f1']['hacim_cm3'], 2)} cm³ · düşey ölçek 2,2 kat büyütüldü",
         fontsize=22, color="#374151")
O.ekran_kaydet(fig, "1.4", "yuva-kesiti", "parametrelerden hesap (f1_tepsi.py ölçüleri)")
print("hafta 1 tamam", round(el / 1000, 2))
