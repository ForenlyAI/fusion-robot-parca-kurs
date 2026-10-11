"""Dilimleme sonucunuzu ekibin ölçtüğüyle karşılaştırır.  Kullanım: python dilim/dilimle.py && python kontrol.py
Dilimleyici sürümleri tahmini farklı hesaplar; bu yüzden tolerans %10 (katman sayısı birebir)."""
import json, pathlib
B = pathlib.Path(__file__).resolve().parent
siz = json.loads((B / "dilim/OLCUMLER.json").read_text())
ref = dict(filament_g=142.28, baski_dk=800, katman=80)        # PrusaSlicer 2.7.2, 11.10.2026 (beklenen/dilim_ozet.txt)
hata = 0
for k, v in ref.items():
    fark = abs(siz[k] / v - 1) * 100
    ok = fark == 0 if k == "katman" else fark <= 10
    hata += not ok
    print(f"{'✓' if ok else '✗'} {k:12s} siz={siz[k]}  beklenen={v}  fark=%{fark:.1f}")
print("dilimleyici:", siz.get("surum"))
print("SONUÇ:", "geçti" if hata == 0 else f"{hata} değer tolerans dışında")
