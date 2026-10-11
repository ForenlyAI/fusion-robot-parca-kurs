#!/usr/bin/env python3
"""Hafta 2 · Robot İçin Hafifletmek — kütle, ağırlık merkezi, yük bütçesi, kabuk ve parametre değişimi.
Fusion sayıları OLCUMLER.json f1/f2 alanlarından (f2_hafiflet.py); STL sayıları bu betikte hesaplanır.
Bardak kütlesi ve kol taşıma sınırı ÖRNEK'tir (ortak.py).
  python3 hafta2.py   → ekran/2.x/*.txt + *.png, OLCUMLER.json d2_* alanları"""
import math
import numpy as np
import ortak as O

F = O.fusion()
tri = O.stl_oku()


def dikey_kesisim(k, x0):
    ys = []
    for a, b in k:
        if (a[0] - x0) * (b[0] - x0) < 0 and b[0] != a[0]:
            ys.append(a[1] + (x0 - a[0]) / (b[0] - a[0]) * (b[1] - a[1]))
    return sorted(round(float(y), 2) for y in ys)


# ---- 2.1 Kütle ve ağırlık merkezi (dolu tepsi) ---------------------------------------------------------
ns = O.oturum("2.1", "kutle-oturumu", """
hacim = 572.63                     # Fusion: dolu tepsinin hacmi (cm³)
yogunluk = 1.24                    # PLA, g/cm³ (üretici veri sayfası)
round(hacim * yogunluk, 1)         # kütle (g) — Fusion 710.1 g yazdı
blok = 208 * 208 * 16 - 1373.5     # köşesi yuvarlatılmış dolu blok (mm³), merkezi Y = 8
yuva = 118224.4                    # dört yuvanın boşluğu (mm³), merkezi Y = 10
y = (blok * 8 - yuva * 10) / (blok - yuva)
round(y, 2)                        # ağırlık merkezi tabandan (mm); X = Z = 0 (simetri)
""")
O.olc(d2_1_hacim_cm3=F["f1"]["hacim_cm3"], d2_1_yogunluk=O.PLA_G_CM3, d2_1_kutle_g=F["f1"]["kutle_g_PLA"],
      d2_1_el_kutle_g=round(F["f1"]["hacim_cm3"] * O.PLA_G_CM3, 1), d2_1_am_y_mm=round(ns["y"], 2))

fig = O.sekil("Ağırlık merkezi · dolu tepsi, önden görünüş")
ax = fig.add_axes([0.05, 0.15, 0.9, 0.6])
ax.fill([-104, 104, 104, -104], [0, 0, 16, 16], color="#E5E7EB", ec="#1f2a37", lw=2.5)
for cx in (-45, 45):
    ax.fill([cx - 28, cx + 28, cx + 28, cx - 28], [4, 4, 16, 16], color="white", ec="#9CA3AF", lw=1.5, ls="--")
ax.plot([0], [ns["y"]], "o", ms=22, mfc="#C2410C", mec="white", mew=3)
ax.annotate(f"ağırlık merkezi\nY = {O.tr(ns['y'], 2)} mm", (0, ns["y"]), (40, 26), fontsize=24, color="#C2410C",
            arrowprops=dict(arrowstyle="->", color="#C2410C", lw=2))
ax.axhline(8, color="#6B7280", lw=1.5, ls=":")
ax.text(-102, 8.6, "kalınlığın ortası Y = 8", fontsize=20, color="#6B7280")
ax.set_aspect(2.2); ax.set_xlim(-112, 112); ax.set_ylim(-3, 34); ax.axis("off")
fig.text(0.05, 0.1, f"hacim {O.tr(F['f1']['hacim_cm3'], 2)} cm³ × PLA 1,24 g/cm³ = {O.tr(F['f1']['kutle_g_PLA'], 1)} g · yuvalar kesik çizgiyle · düşey ölçek 2,2 kat",
         fontsize=21, color="#374151")
O.ekran_kaydet(fig, "2.1", "agirlik-merkezi", "f1_tepsi.py hacmi + parametrelerden hesap")

# ---- 2.2 Robot yük bütçesi (dolu tepsi) ----------------------------------------------------------------
ns = O.oturum("2.2", "butce-oturumu", """
tepsi = 710.1                       # Fusion, dolu tepsi (g)
bardak = 230                        # ÖRNEK: bardak + tabak + çay (g)
sinir = 2000                        # ÖRNEK: kol taşıma sınırı (g), üretici veri sayfasından doğrulanmalı
yuk = tepsi + 4 * bardak
round(yuk)                          # robotun kolundaki toplam (g)
round(yuk / sinir * 100, 1)         # sınırın yüzde kaçı
round((1 - yuk / sinir) * 100, 1)   # kalan pay (%)
round(tepsi / yuk * 100, 1)         # yükün yüzde kaçı yalnız tepsi
""")
yuk = ns["yuk"]
O.olc(d2_2_tepsi_g=F["f2"]["once_g"], d2_2_bardak_g=O.BARDAK_G, d2_2_bardak=4, d2_2_sinir_g=O.KOL_SINIR_G,
      d2_2_yuk_g=round(yuk), d2_2_oran_yuzde=round(yuk / O.KOL_SINIR_G * 100, 1), d2_2_pay_yuzde=round((1 - yuk / O.KOL_SINIR_G) * 100, 1),
      d2_2_tepsi_payi_yuzde=round(F["f2"]["once_g"] / yuk * 100, 1))

# ---- 2.3 Kabukla hafifletme ------------------------------------------------------------------------------
ns = O.oturum("2.3", "kabuk-oturumu", """
import ortak as O
tri = O.stl_oku("cikti/cay_tepsisi.stl")       # kabuktan sonra dışa aktarılan tepsi
v = O.hacim(tri) / 1000
round(v, 2)                                     # STL hacmi (cm³)
round(v * 1.24, 1)                              # kütle (g) — Fusion 187.4 g yazdı
round(abs(v * 1.24 - 187.4) / 187.4 * 100, 2)   # Fusion ile fark (%)
O.agirlik_merkezi(tri).round(2)                 # ağırlık merkezi X, Y, Z (mm)
round((1 - 187.4 / 710.1) * 100, 1)             # kabukla azalma (%)
yuk = 187.4 + 4 * 230
round(yuk), round((1 - yuk / 2000) * 100, 1)    # dört bardakla toplam (g) ve kalan pay (%)
""")
v = ns["v"]
k = O.kesit(tri, 2, 45.0)
ust = dikey_kesisim(k, 0.0)
taban = dikey_kesisim(k, 45.0)
O.olc(d2_3_stl_cm3=round(v, 2), d2_3_stl_g=round(v * O.PLA_G_CM3, 1), d2_3_fusion_g=F["f2"]["sonra_g"],
      d2_3_fark_yuzde=round(abs(v * O.PLA_G_CM3 - F["f2"]["sonra_g"]) / F["f2"]["sonra_g"] * 100, 2),
      d2_3_am_y_mm=round(float(O.agirlik_merkezi(tri)[1]), 2), d2_3_azalma_yuzde=F["f2"]["azalma_yuzde"],
      d2_3_dolu_tepsi_g=F["f2"]["dolu_tepsi_g"], d2_3_pay_yuzde=F["f2"]["pay_yuzde"],
      d2_3_ust_kabuk_mm=round(ust[1] - ust[0], 2), d2_3_yuva_tabani_mm=round(taban[1] - taban[0], 2), d2_3_duvar_mm=2.4)

fig = O.sekil("Kabuktan sonra kesit · Z = 45, iki yuvanın ortasından")
ax = fig.add_axes([0.04, 0.15, 0.92, 0.6])
for (a, b) in k:
    ax.plot([a[0], b[0]], [a[1], b[1]], color="#1f2a37", lw=2.4)
ax.annotate("", (0, 16), (0, 13.6), arrowprops=dict(arrowstyle="<->", lw=2, color="#7E22CE"))
ax.text(2, 18.5, f"üst kabuk {O.tr(ust[1] - ust[0], 1)} mm", fontsize=22, color="#7E22CE")
ax.annotate("", (45, 4), (45, 1.6), arrowprops=dict(arrowstyle="<->", lw=2, color="#0F766E"))
ax.text(47, -2.6, f"yuva tabanı {O.tr(taban[1] - taban[0], 1)} mm", fontsize=22, color="#0F766E")
ax.text(-104, -4.5, "alt yüz açık: kabuk alttan boşaltıldı", fontsize=21, color="#C2410C")
ax.set_aspect(2.2); ax.set_xlim(-112, 112); ax.set_ylim(-7, 24); ax.axis("off")
fig.text(0.04, 0.1, f"STL: {O.tr(v, 2)} cm³ → {O.tr(v * O.PLA_G_CM3, 1)} g · Fusion {O.tr(F['f2']['sonra_g'], 1)} g · düşey ölçek 2,2 kat",
         fontsize=21, color="#374151")
O.ekran_kaydet(fig, "2.3", "kabuk-kesiti", "cikti/cay_tepsisi.stl kesiti")

# yük bütçesi grafiği (2.2 ve 2.3): dolu tepsi ↔ kabuklu tepsi
fig = O.sekil("Robot kolu yük bütçesi · dört bardakla (bardak ve sınır ÖRNEK)")
ax = fig.add_axes([0.17, 0.14, 0.78, 0.62])
ad = ["dolu tepsi", "kabuklu tepsi"]
tepsi = [F["f2"]["once_g"], F["f2"]["sonra_g"]]
bardak = [4 * O.BARDAK_G] * 2
ax.barh(ad, tepsi, color="#1D4ED8", label="tepsi (Fusion ölçümü)")
ax.barh(ad, bardak, left=tepsi, color="#93C5FD", hatch="//", ec="white", label="4 bardak (ÖRNEK)")
ax.axvline(O.KOL_SINIR_G, color="#C2410C", lw=4, ls="--")
ax.text(O.KOL_SINIR_G - 25, -0.62, "kol sınırı 2.000 g (ÖRNEK)", color="#C2410C", ha="right", fontsize=22)
for i in range(2):
    t = tepsi[i] + bardak[i]
    ax.text(2080, i, f"{O.tr(t, 0)} g\npay %{O.tr((1 - t / O.KOL_SINIR_G) * 100, 1)}", va="center", fontsize=24)
ax.set_xlim(0, 2500); ax.set_ylim(1.6, -0.8); ax.set_xlabel("gram"); ax.legend(loc="upper left", fontsize=20, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
O.ekran_kaydet(fig, "2.2", "yuk-butcesi", "OLCUMLER.json f2 + ÖRNEK bardak ve sınır")

# ---- 2.4 Parametre değişince ------------------------------------------------------------------------------
ns = O.oturum("2.4", "degisim-oturumu", """
import math
once, cap60, geri = 187.4, 189.2, 187.4   # Fusion: bardak_cap 56 → 60 → 56 (g)
round(cap60 - once, 1)                    # kabuklu tepside değişim (g)
geri == once                              # geri alınca birebir aynı mı
dolu = lambda d: (208 * 208 * 16 - 1373.5 - 4 * math.pi * (d / 2)**2 * 12) / 1000 * 1.24
round(dolu(60) - dolu(56), 1)             # dolu tepsi olsaydı değişim (g), elle hesap
""")
O.olc(d2_4_once_g=F["f2"]["sonra_g"], d2_4_cap60_g=F["f2"]["cap60_g"], d2_4_geri_g=F["f2"]["cap56_geri_g"],
      d2_4_degisim_g=round(F["f2"]["cap60_g"] - F["f2"]["sonra_g"], 1), d2_4_birebir=F["f2"]["cap56_geri_g"] == F["f2"]["sonra_g"],
      d2_4_dolu_degisim_g=round(ns["dolu"](60) - ns["dolu"](56), 1))

fig = O.sekil("bardak_cap 56 → 60 → 56 · Fusion'ın yeniden kurduğu kütle")
ax = fig.add_axes([0.1, 0.16, 0.5, 0.64])
x = ["Ø56", "Ø60", "Ø56 geri"]
yv = [F["f2"]["sonra_g"], F["f2"]["cap60_g"], F["f2"]["cap56_geri_g"]]
ax.bar(x, yv, color=["#1D4ED8", "#C2410C", "#1D4ED8"], width=0.55)
for i, v in enumerate(yv):
    ax.text(i, v + 0.15, f"{O.tr(v, 1)} g", ha="center", fontsize=26)
ax.set_ylim(185, 191); ax.set_ylabel("kabuklu tepsi (g)"); ax.spines[["top", "right"]].set_visible(False)
fig.text(0.64, 0.7, "Kabuklu tepside: +1,8 g", fontsize=28, weight="bold", color="#C2410C")
fig.text(0.64, 0.62, f"Dolu tepsi olsaydı: {O.tr(ns['dolu'](60) - ns['dolu'](56), 1).replace('-', '−')} g", fontsize=28, color="#374151")
fig.text(0.64, 0.54, "(elle hesap, aynı değişiklik)", fontsize=22, color="#6B7280")
fig.text(0.64, 0.42, "Geri alınca: birebir 187,4 g", fontsize=26, color="#1D4ED8")
fig.text(0.64, 0.30, "Düşey eksen 185'ten başlar", fontsize=20, color="#6B7280")
O.ekran_kaydet(fig, "2.4", "parametre-degisimi", "OLCUMLER.json f2 (Fusion) + elle hesap")
print("hafta 2 tamam")
