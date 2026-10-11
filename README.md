# Fusion ile Robot Parçası: Parametrik Tasarımdan Baskıya · öğrenci deposu

Forenly AI Academy kursu için çalışma deposu. Yürüyen örnek: kafede çay servisi yapan **insansı robotun (Unitree G1) taşıdığı dört bardaklık tepsi**. Forenly AI'ın foi'si robotu işletmenin içinde otonom çalıştırır; robotun taşıdığı her parça **robotun yük sınırına** sığmalıdır. Bu kursta parçayı Fusion'da tasarlar, robot için hafifletir ve 3B baskıya hazırlarsınız.

| Adım | Dosya | Ne yapar | Ekibin ölçtüğü sonuç (11.10.2026, Fusion 2705.1.25) |
|---|---|---|---|
| 1 | `fusion/f1_tepsi.py` | Kullanıcı parametreleriyle tepsi: taban, 4 bardak yuvası, köşe yuvarlatma | 208 × 208 × 16 mm, Ø56 yuva; dolu tepsi 710 g (PLA) |
| 2 | `fusion/f2_hafiflet.py` | Alttan kabuk (Shell, 2,4 mm duvar); kütle ve ağırlık merkezi; robot yük bütçesi; parametre değişimi | 710 → 187 g (%−73,6); 4 bardakla 1.107 g, G1 kol sınırı ~2 kg → pay %44,6 |
| 3 | `fusion/f3_cikti.py` | STEP (CAD değişimi), STL ve 3MF (baskı), F3D (arşiv) dışa aktarımı | `beklenen/` içindeki dosyalar |
| 4 | `dilim/dilimle.py` | PrusaSlicer komut satırıyla dilimleme (PLA, 0,2 mm, %15 gyroid) | 80 katman, 142 g filament, ~13 sa 20 dk |

## Fusion adımları (1–3)

Betikler Fusion'ın içinde çalışır: **Utilities → Scripts and Add-Ins → +** ile betiği ekleyip **Run**. Ya da Fusion'ın resmi **MCP sunucusu** açıksa (Preferences → General → API → Fusion MCP Server) Claude Code'a "f1_tepsi.py'yi Fusion'da çalıştır" dersiniz. Fusion Codespace'te çalışmaz; bu adımlar kendi bilgisayarınızdaki Fusion'da yapılır.

## Dilimleme adımı (4) — Codespaces'te çalışır

**Code → Codespaces → Create**. Ortam PrusaSlicer'ı kendiliğinden kurar. Sonra:

```bash
python dilim/dilimle.py            # beklenen/g1_cay_tepsisi.stl'i dilimler
python dilim/dilimle.py benim.stl  # kendi Fusion çıktınızı dilimler
python kontrol.py
```

Codespace'teki PrusaSlicer sürümü bizimkinden farklı olabilir; `kontrol.py` süre ve filamentte %10 tolerans tanır.

## Görevler

1. **Parametre:** `bardak_cap`'ı 60 mm yapın (Fusion'da Modify → Change Parameters). Model kendini yeniden kuruyor mu, kütle ne oldu?
2. **Yük bütçesi:** tepsiyi 6 bardaklık yapın (`aralik` ve dizi). G1 temel modelin ~2 kg kol sınırı içinde kalıyor mu? EDU (~3 kg) ile karşılaştırın.
3. **Baskı:** duvarı 2,4'ten 1,6 mm'ye indirin, yeniden dilimleyin. Süre ve filament ne kadar düştü? Tepsi yeterince sağlam mı, neden ölçmeden bilemeyiz?
4. **Claude Code katmanı:** Claude Code'a "tepsinin altına 4 mm genişliğinde çapraz kaburga ekle, kütleyi yeniden ölç" deyin. Değişen satırları okuyun, Fusion'da zaman çizelgesine bakın, kütleyi kendiniz doğrulayın.

## Sınırlar

- Bardak kütlesi (230 g) ve G1 kol yükü (~2 kg temel, ~3 kg EDU; üretici: kol duruşuna göre çok değişir) **ÖRNEK/kaynak değeri**dir; gerçek görevde robotun güncel veri sayfası ve deneme kullanılır.
- Dayanım (gerilme) analizi bu kursta koşulmadı: Fusion Simulation çözücüsü bulut kredisi ister. Kabuk duvarının yeterliliği ölçülmeden "sağlam" denmez.
- Kütle Fusion'da katı (dolu) kabuk için, dilimleyicide %15 dolgulu baskı için hesaplanır; ikisi bu yüzden farklıdır (187 g ↔ 142 g).
