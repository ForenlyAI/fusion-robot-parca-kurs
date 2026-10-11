"""Fusion ile Robot Parçası: Parametrik Tasarımdan Baskıya — kursta anılan kaynaklar.

Her kaynak 11.10.2026'da açıldı ve okundu; doğrulama notu nasıl denetlendiğini söyler. Derste kaynağı olmayan ve
ölçümden gelmeyen her sayı ÖRNEK diye işaretlidir (bardak kütlesi 230 g, kol taşıma sınırı 2.000 g)."""

KAYNAKLAR = [
    dict(anahtar="ingeo4043d", yazar="NatureWorks LLC", yil=2015,
         baslik="Ingeo Biopolymer 4043D Technical Data Sheet — 3D Printing Monofilament, General Purpose Grade (NW4043DFILA_051815V1)",
         yer="NatureWorks teknik veri sayfası (PDF)",
         deger="özgül ağırlık 1,24 g/cm³ (ASTM D792); 3B baskı sıcaklığı 190–230 °C",
         dogrulama="PDF indirildi, 'Typical Material Properties' tablosu okundu: 'Specific Gravity, g/cc 1.24 D792'. Kurs PLA yoğunluğunu buradan alır."),
    dict(anahtar="fusion-mcp-claude", yazar="Anthropic", yil=2026,
         baslik="Autodesk Fusion connector",
         yer="https://claude.com/connectors/autodesk-fusion",
         deger="Fusion MCP sunucusu Claude'u çalışan bir Fusion oturumuna bağlar; Preferences > General > API > Fusion MCP Server; sunucu yerel makinede çalışır",
         dogrulama="Sayfa açılıp okundu (11.10.2026). Deneme ya da abonelik şartı bu sayfada yazmıyor."),
    dict(anahtar="fusion-mcp-aps", yazar="Autodesk Platform Services", yil=2026,
         baslik="Bringing Fusion to Claude for Creative Work",
         yer="https://aps.autodesk.com/blog/bringing-fusion-claude-creative-work",
         deger="28 Nisan 2026 duyurusu; Fusion MCP 'Fusion subscribers' için",
         dogrulama="Sayfa açılıp okundu (11.10.2026). Kurs ekibi Fusion'ı ticari deneme sürümüyle kullandı; abonelik şartı açık soru (planlama/ACIK-SORULAR.md)."),
    dict(anahtar="fusion-api", yazar="Autodesk", yil=2026,
         baslik="Fusion API Reference Manual (ExportManager, createSTEPExportOptions, Export to other formats örneği)",
         yer="https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/files/ExportManager.htm",
         deger="dışa aktarma seçeneği önce kurulur, sonra ExportManager.execute ile yazılır",
         dogrulama="Arama sonucundaki Autodesk sayfa özeti okundu; sayfa tarayıcıda istemci tarafında yüklendiği için düz istekle açılmadı. Asıl kanıt: f3_cikti.py Fusion 2705.1.25'te koşuldu, dört dosya yazıldı (OLCUMLER.json f3)."),
    dict(anahtar="iso10303-21", yazar="ISO/TC 184/SC 4", yil=2016,
         baslik="ISO 10303-21:2016 Industrial automation systems and integration — Product data representation and exchange — Part 21: Implementation methods: Clear text encoding of the exchange structure",
         yer="ISO kataloğu (https://www.iso.org/standard/63141.html)",
         deger="STEP dosyasının düz yazı biçimi; kursun STEP dosyası 'AUTOMOTIVE_DESIGN' (AP214) şemasıyla yazılmış",
         dogrulama="Katalog künyesi Kanada Standartlar Konseyi ve ISO kayıtlarından okundu (3. baskı, Mart 2016, 2022'de onaylandı). Standart metni ücretli, alıntılanmaz."),
    dict(anahtar="3mf-core", yazar="3MF Consortium", yil=2026,
         baslik="3MF Core Specification",
         yer="https://github.com/3MFConsortium/spec_core · https://3mf.io/spec/",
         deger="3MF bir ZIP paketidir, modeli birimiyle (unit=\"millimeter\") birlikte taşır",
         dogrulama="Depo ve sayfa açıldı (HTTP 200). Kursun 3MF dosyası açılıp 3D/3dmodel.model içinde unit=\"millimeter\" okundu (hafta3.py)."),
    dict(anahtar="prusaslicer-cli", yazar="Prusa Research", yil=2026,
         baslik="PrusaSlicer Command Line Interface (wiki) ve prusa-slicer(1) Debian kılavuz sayfası",
         yer="https://github.com/prusa3d/PrusaSlicer/wiki/Command-Line-Interface",
         deger="--export-gcode dilimler ve G-code yazar; --rotate-x modeli X ekseninde döndürür",
         dogrulama="Wiki sayfası açıldı (HTTP 200); Debian kılavuz özeti okundu. Asıl kanıt: dilimleme PrusaSlicer 2.7.2 ile koşuldu (dilim/dilim_ozet.txt) ve Codespace'te Debian paketiyle tekrarlandı."),
]

# Kaynağı olmayan, derste ÖRNEK diye işaretlenen değerler
ORNEK = {
    "bardak_g": (230, "ince belli çay bardağı + tabak + çay; tartılmadı"),
    "kol_siniri_g": (2000, "kol taşıma sınırı; üreticinin veri sayfasından alınır, kol duruşuna göre çok değişir — derste doğrulanmadı"),
    "tepsi_olculeri": ("Ø56, aralık 90, kalınlık 16, kenar 14, köşe R10, yuva derinliği 12, duvar 2,4 mm", "tasarım seçimi"),
}
