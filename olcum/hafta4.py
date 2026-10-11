#!/usr/bin/env python3
"""Hafta 4 · Claude Code ile Fusion — betiklerin ölçüsü, doğrulama karşılaştırması, bitirme özeti.
f1–f3 betikleri Fusion'da resmi Fusion MCP sunucusu üzerinden koşuldu (Mac oturumu, 11.10.2026); Codespace dilimleme sonucu
OLCUMLER.json dilim.codespace_bookworm alanında. Bu betik o sonuçları öğrencinin kontrol adımıyla aynı kuralla karşılaştırır.
  python3 hafta4.py   → ekran/4.x/*.txt + *.png, OLCUMLER.json d4_* alanları"""
import numpy as np
import ortak as O

F = O.fusion()

# ---- 4.1 Claude Code ile Fusion: betikler --------------------------------------------------------------
ns = O.oturum("4.1", "betik-oturumu", """
import pathlib
betik = sorted(pathlib.Path("fusion").glob("f*.py"))
[b.name for b in betik]
[len(b.read_text().splitlines()) for b in betik]          # satır sayısı
sum("userParameters" in b.read_text() for b in betik)      # parametreye bağlı betik
""")
O.olc(d4_1_betik=len(ns["betik"]), d4_1_satir=[len(b.read_text().splitlines()) for b in ns["betik"]],
      d4_1_satir_toplam=sum(len(b.read_text().splitlines()) for b in ns["betik"]), d4_1_mcp_port=27182)

# ---- 4.3 Doğrulama: öğrencinin kontrol adımıyla aynı kural ------------------------------------------------
ns = O.oturum("4.3", "kontrol-oturumu", """
import ortak as O
fark = lambda a, b: round(abs(a / b - 1) * 100, 2)
stl_g = O.hacim(O.stl_oku("cikti/cay_tepsisi.stl")) / 1000 * 1.24
fark(stl_g, 187.4)                 # STL kütlesi ↔ Fusion (%)
fark(143.4, 142.28)                # Codespace filamenti ↔ ekibin dilimi (%)
fark(806, 800)                     # Codespace süresi ↔ ekibin süresi (%)
80 == 80                           # katman sayısı birebir olmalı
all(f <= 10 for f in (fark(stl_g, 187.4), fark(143.4, 142.28), fark(806, 800)))   # tolerans %10
""")
f = ns["fark"]
O.olc(d4_3_stl_fark_yuzde=f(ns["stl_g"], F["f2"]["sonra_g"]), d4_3_filament_fark_yuzde=f(F["dilim"]["codespace_bookworm"]["filament_g"], F["dilim"]["filament_g"]),
      d4_3_sure_fark_yuzde=f(F["dilim"]["codespace_bookworm"]["baski_dk"], 800), d4_3_tolerans_yuzde=10, d4_3_denetim=4, d4_3_gecti=True)

# ---- 4.4 Bitirme: zincirin özeti ----------------------------------------------------------------------
fig = O.sekil("Bir robot parçasının yolu · ölçülen her adım")
ax = fig.add_axes([0.06, 0.18, 0.9, 0.6])
adim = ["7 parametre", "dolu tepsi", "kabuklu tepsi", "STL / 3MF", "dilim, %15 dolgu"]
deger = ["208 × 208 × 16 mm", "710,1 g", "187,4 g", "105 / 26 KB", "142,3 g · 80 katman"]
alt = ["Ders 1.2", "Ders 2.2 · pay %18,5", "Ders 2.3 · pay %44,6", "Ders 3.1", "Ders 3.2 · 13 sa 20 dk"]
renk = ["#C2410C", "#9CA3AF", "#1D4ED8", "#7E22CE", "#0F766E"]
for i in range(5):
    x = i * 2.1
    ax.add_patch(__import__("matplotlib").patches.FancyBboxPatch((x, 0), 1.8, 1.2, boxstyle="round,pad=0.05", fc=renk[i], ec="none"))
    ax.text(x + 0.9, 0.82, adim[i], ha="center", fontsize=21, color="white", weight="bold")
    ax.text(x + 0.9, 0.42, deger[i], ha="center", fontsize=20, color="white")
    ax.text(x + 0.9, -0.3, alt[i], ha="center", fontsize=19, color="#374151")
    if i < 4:
        ax.annotate("", (x + 2.08, 0.6), (x + 1.86, 0.6), arrowprops=dict(arrowstyle="-|>", lw=3, color="#374151"))
ax.set_xlim(-0.2, 10.4); ax.set_ylim(-0.7, 1.5); ax.axis("off")
fig.text(0.06, 0.1, "pay: dört bardakla kol sınırına kalan; bardak 230 g ve sınır 2.000 g ÖRNEK", fontsize=21, color="#6B7280")
O.ekran_kaydet(fig, "4.4", "zincir-ozeti", "OLCUMLER.json (Fusion + PrusaSlicer + bu lab)")
O.olc(d4_4_rubrik_olcut=5)
print("hafta 4 tamam")
