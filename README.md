# Fusion ile Robot Parçası · öğrenci deposu

Forenly AI Academy kursunun çalışma deposu. Yürüyen örnek: kafede çay taşıyan **insansı robotun dört bardaklık tepsisi**. Forenly AI'nin foi sistemi insansı robotu bir işletmede kendi başına çalıştırır; robotun eline verilen her parça **robotun yük bütçesine** sığmalıdır. Bu kursta parçayı Fusion'da parametrik tasarlar, robot için hafifletir, baskıya hazırlar ve sonucu doğrularsınız.

| Hafta | Klasör | Ne yapar | Ekibin ölçtüğü sonuç (11.10.2026, Fusion 2705.1.25) |
|---|---|---|---|
| 1 | `fusion/f1_tepsi.py` | Kullanıcı parametreleriyle tepsi: taban, 4 bardak yuvası, köşe yuvarlatma | 208 × 208 × 16 mm, Ø56 yuva; hacim 572,63 cm³ |
| 2 | `fusion/f2_hafiflet.py` | Kütle ve ağırlık merkezi, yük bütçesi, alttan kabuk (2,4 mm duvar), parametre değişimi | 710,1 → 187,4 g (%−73,6); 4 bardakla 1.107 g, pay %44,6 (bardak ve sınır ÖRNEK) |
| 3 | `fusion/f3_cikti.py`, `dilim/dilimle.py` | STEP, STL, 3MF, F3D dışa aktarımı; PrusaSlicer ile dilimleme (PLA, 0,2 mm, %15 gyroid) | 80 katman, 142,28 g filament, 13 sa 19 dk 47 sn |
| 4 | `kontrol.py`, `olcum/` | Claude Code + Fusion MCP ile betik; sonucun doğrulanması | STL kütlesi ↔ Fusion farkı %0,03; Codespace dilimi farkı %0,8 |

## Üç katman

1. **Elle Fusion:** her adım önce menüden yapılır (Change Parameters, Sketch, Extrude, Fillet, Shell, Export).
2. **Fusion'ın kendi yapay zekâ yardımcısı:** bu kursta **denenmedi**; ondan bir sonuç vaat edilmez.
3. **Claude Code + Fusion MCP:** Fusion'da *Preferences › General › API › Fusion MCP Server* açılır; Claude Code'a "fusion/f1_tepsi.py'yi Fusion'da çalıştır" dersiniz. Betikler MCP olmadan da çalışır: *Utilities › Scripts and Add-Ins › +* ile ekleyip *Run*.

Fusion Codespace'te çalışmaz; Fusion adımları kendi bilgisayarınızdaki Fusion'da (deneme sürümü ya da kurumunuzun lisansı) yapılır. Kurs lisans satmaz.

## Codespaces'te çalışan adımlar

**Code → Codespaces → Create.** Ortam PrusaSlicer'ı kendiliğinden kurar.

```bash
pip install -r requirements.txt
python dilim/dilimle.py                  # beklenen/cay_tepsisi.stl'i dilimler
python dilim/dilimle.py benim.stl        # kendi Fusion çıktınızı dilimler
python olcum/hafta1.py && python olcum/hafta2.py && python olcum/hafta3.py && python olcum/hafta4.py
python kontrol.py                        # STL kütlesi + dilim + olcum/ karşılaştırması
python kontrol.py benim.stl --fusion-g 123.4   # kendi parçanız: STL kütlesi ↔ Fusion'ın yazdığı kütle
```

`olcum/` klasörü ekibin lab betikleridir: Fusion'ın dışa aktardığı STL'i NumPy ile okur; hacmi, kütleyi, ağırlık merkezini, kesitleri ve katman sayısını yeniden hesaplar (`olcum/ekran/` altına çizer). Sonuçlar `beklenen/OLCUMLER.json` ile birebir aynı çıkmalıdır.

## Görevler

1. **Parametre (Ders 1.2, 2.4):** `bardak_cap`'ı 60 mm yapın (Modify › Change Parameters). Model kendini yeniden kuruyor mu, kütle ne oldu? Geri alınca birebir aynı mı?
2. **Yük bütçesi (Ders 2.2):** tepsiyi 6 bardaklık yapın. ÖRNEK 2 kg kol sınırı içinde ne kadar pay kalıyor? Kendi robotunuz için sınırı üreticinin veri sayfasından alın ve kaynağını yazın.
3. **Baskı (Ders 3.2–3.4):** duvarı 2,4'ten 1,6 mm'ye indirin, yeniden dilimleyin. Süre ve filament ne kadar düştü? Tepsi yeterince sağlam mı, neden ölçmeden bilemeyiz?
4. **Claude Code (Ders 4.2):** Claude Code'dan "tepsinin altına 4 mm genişliğinde çapraz kaburga ekle, genişlik yeni bir parametre olsun, kütleyi yeniden ölç" isteyin. Değişen satırları okuyun, zaman çizelgesine bakın, kütleyi kendiniz doğrulayın. Bu sonucu ekip ölçmedi.
5. **Bitirme (Ders 4.4):** kendi robot parçanız, `RUBRIK.md`'ye göre.

## Sınırlar

- Bardak kütlesi (230 g) ve kol taşıma sınırı (2.000 g) **ÖRNEK**tir. Gerçek sınır robotun üreticisinin veri sayfasında yazar ve kol duruşuna göre çok değişir.
- Tepsinin ölçüleri tasarım seçimidir (ÖRNEK).
- Dayanım (gerilme) analizi bu kursta koşulmadı: Fusion Simulation çözücüsü bulut kredisi ister. Kabuk duvarının yeterliliği ölçülmeden "sağlam" denmez.
- Kütle Fusion'da katı kabuk için, dilimleyicide iki çevre + %15 dolgulu baskı için hesaplanır; ikisi bu yüzden farklıdır (187,4 g ↔ 142,28 g). Basılmış tepsi tartılmadı.
- PLA yoğunluğu 1,24 g/cm³: NatureWorks Ingeo 4043D teknik veri sayfası (ASTM D792). Öteki kaynaklar `olcum/kaynaklar.py` içinde.
- `fusion/f3_cikti.py` çıktıyı ev klasörünüzdeki `fusion-out` klasörüne yazar; ekip betiği sabit bir klasör yoluyla koşturdu, bu satır sizin bilgisayarınızda denenmedi.

Anlatım metni ve sayfa kurgusu yapay zekâ ile yazıldı, sayılar ölçümlerle denetlendi; ses yapay zekâ ile üretilir.
