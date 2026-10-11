"""Sonuçlarınızı ekibin ölçtüğüyle karşılaştırır (Ders 4.3).
  python dilim/dilimle.py && python kontrol.py          # dilim + STL kütlesi
  python kontrol.py benim.stl --fusion-g 123.4           # kendi parçanızın STL kütlesi ↔ Fusion'ın yazdığı kütle
Dilimleyici sürümleri tahmini farklı hesaplar; bu yüzden filament ve sürede tolerans %10, katman sayısı birebir.
Kütle denetimi: STL hacmi × PLA 1,24 g/cm³ ↔ Fusion kütlesi, tolerans %10. olcum/ betikleri koşulduysa ölçümleri beklenen/ ile karşılaştırır."""
import json, pathlib, struct, sys
B = pathlib.Path(__file__).resolve().parent
TOL = 10
hata, sayi = 0, 0


def yaz(ok, ad, siz, beklenen, fark):
    global hata, sayi
    hata += not ok; sayi += 1
    print(f"{'✓' if ok else '✗'} {ad:14s} siz={siz}  beklenen={beklenen}  fark=%{fark:.2f}")


def stl_kutle_g(yol, yogunluk=1.24):
    b = pathlib.Path(yol).read_bytes()
    n = struct.unpack("<I", b[80:84])[0]
    hacim = 0.0
    for i in range(n):
        v = struct.unpack("<9f", b[84 + 50 * i + 12: 84 + 50 * i + 48])
        a, c, d = v[0:3], v[3:6], v[6:9]
        hacim += (a[0] * (c[1] * d[2] - c[2] * d[1]) - a[1] * (c[0] * d[2] - c[2] * d[0]) + a[2] * (c[0] * d[1] - c[1] * d[0])) / 6
    return hacim / 1000 * yogunluk


# 1) STL kütlesi ↔ Fusion
av = sys.argv[1:]
fusion_g = 187.4   # Fusion, kabuklu tepsi (Ders 2.3)
if "--fusion-g" in av:
    i = av.index("--fusion-g"); fusion_g = float(av[i + 1]); del av[i:i + 2]
stl = pathlib.Path(av[0]) if av else B / "beklenen/cay_tepsisi.stl"
g = stl_kutle_g(stl)
f = abs(g / fusion_g - 1) * 100
yaz(f <= TOL, "STL kütlesi", round(g, 1), fusion_g, f)

# 2) Dilim sonucu (dilim/dilimle.py koşulduysa)
dj = B / "dilim/OLCUMLER.json"
if dj.exists():
    siz = json.loads(dj.read_text())
    ref = dict(filament_g=142.28, baski_dk=800, katman=80)   # PrusaSlicer 2.7.2, 11.10.2026 (beklenen/dilim_ozet.txt)
    for k, v in ref.items():
        f = abs(siz[k] / v - 1) * 100
        yaz(f == 0 if k == "katman" else f <= TOL, k, siz[k], v, f)
    print("dilimleyici:", siz.get("surum"))
else:
    print("· dilim yok: önce  python dilim/dilimle.py")

# 3) olcum/ betikleri (python olcum/hafta1.py … hafta4.py) koşulduysa: ekibin ölçümüyle birebir mi?
oj, bj = B / "olcum/OLCUMLER.json", B / "beklenen/OLCUMLER.json"
siz, bek = json.loads(oj.read_text()), json.loads(bj.read_text())
anahtar = [k for k in bek if k.startswith("d")]
if any(k in siz for k in anahtar):
    fark = [k for k in anahtar if siz.get(k) != bek[k]]
    yaz(not fark, "olcum/ fark", len(fark), 0, 0.0)
    for k in fark[:10]:
        print("   ", k, siz.get(k), "≠", bek[k])
else:
    print("· olcum/ koşulmadı: python olcum/hafta1.py (… hafta4.py)")
print("SONUÇ:", "geçti" if hata == 0 else f"{hata} denetim tutmadı", f"({sayi} denetim)")
sys.exit(1 if hata else 0)
