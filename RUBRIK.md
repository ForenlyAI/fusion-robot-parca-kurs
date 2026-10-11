# Bitirme işi · ölçüt çizelgesi

Fusion ile Robot Parçası: Parametrik Tasarımdan Baskıya · Ders 4.4

**İş:** bir insansı robotun bir işletmede taşıyacağı ya da takacağı kendi parçanızı tasarlayın, robotun yük bütçesine göre hafifletin, baskıya hazırlayın ve doğrulayın.

**Teslim (tek ZIP):** F3D (parametreleri ve geçmişiyle) · STEP · 3MF ya da STL · tek sayfalık ölçüm tablosu · dilim özeti · `python kontrol.py` çıktısı · Claude Code'a yaptırdığınız bir değişiklik ve okuduğunuz satırlar.

Her ölçüt **yeterli** ya da **eksik** diye değerlendirilir. Beşi de yeterliyse iş tamamdır.

| # | Ölçüt | Yeterli | Eksik |
|---|---|---|---|
| 1 | Parametrik model | En az üç kullanıcı parametresi var; ana ölçüler ifadeye bağlı; bir parametre değiştirilip geri alındığında kütle birebir aynı çıkıyor (Ders 1.2, 2.4). | Ölçüler sayı olarak yazılmış ya da geri alınca kütle farklı. |
| 2 | Yük bütçesi | Parça kütlesi, taşınan yük, kol sınırı ve pay yazılı; ÖRNEK değerler "ÖRNEK", kaynaklı değerler kaynağıyla işaretli (Ders 2.2). | Pay hesaplanmamış ya da değerlerin nereden geldiği belirsiz. |
| 3 | Hafifletme | Önce ve sonra kütlesi Fusion'dan ölçülmüş, en az bir değer elle ya da dosyadan sağlanmış; açık bırakılan yüz gerekçeli (Ders 2.3). | Tek ölçüm var, sağlama yok. |
| 4 | Baskı | 3MF/STL doğru yönde dilimlenmiş; katman sayısı yükseklik ÷ katman kalınlığıyla tutuyor; filament ve süre yazılı (Ders 3.2, 3.4). | Yön yanlış ya da dilim sonucu yok. |
| 5 | Doğrulama | Fusion kütlesi ile dosyadan hesaplanan kütle karşılaştırılmış; `kontrol.py` çıktısı ekli; Claude Code değişikliğinin satırları okunup kütle yeniden ölçülmüş (Ders 4.1–4.3). | Yapay zekânın sonucu ölçülmeden kabul edilmiş. |

**Sınırlar bölümü (zorunlu):** dayanım (gerilme) bu kursta ölçülmedi; parçanıza "sağlam" demeyin, ölçmediğiniz her şeyi burada yazın.
