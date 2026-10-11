"""Fusion ile Robot Parçası: Parametrik Tasarımdan Baskıya — lab ortak araçları.

Kursun iki tür ölçümü var:
  1) Fusion ölçümü: fusion/f1_tepsi.py, f2_hafiflet.py, f3_cikti.py betikleri gerçek Fusion'da (2705.1.25, ticari deneme)
     resmi Fusion MCP sunucusu üzerinden koşuldu; sonuçları OLCUMLER.json'un "f1", "f2", "f3" alanlarında (11.10.2026).
     Dilimleme PrusaSlicer 2.7.2 ile koşuldu: dilim/dilim_ozet.txt ve "dilim" alanı.
  2) Bu klasörün Python ölçümü: Fusion'ın dışa aktardığı STL dosyası (cikti/cay_tepsisi.stl) NumPy ile okunur;
     hacim, kütle, ağırlık merkezi, kutu ölçüsü, kesitler ve katman sayısı yeniden hesaplanır, Fusion'ın sayısıyla
     karşılaştırılır. Bu ekranlar "Gerçek koşum çıktısı" diye etiketlenir; Fusion ekranı DEĞİLDİR.
Kayıttan, Fusion ölçümünden ya da kaynaklar.py'deki belgelerden gelmeyen her değer ÖRNEK'tir (bardak kütlesi, kol sınırı).

  stl_oku(yol)                  : ikili STL → (n, 3, 3) üçgen dizisi (mm)
  hacim / agirlik_merkezi / kutu : kapalı yüzeyden hacim (mm³), ağırlık merkezi (mm), kutu ölçüsü (mm)
  kesit(tri, eksen, deger)      : düzlem kesiti → çizgi parçaları (kesit görünüşü için)
  oturum(ders, ad, kod)         : kodu Python etkileşimli oturumu gibi çalıştırır → ekran/<ders>/<ad>.txt
  ekran_kaydet(fig, ders, ad)   : Matplotlib çizimini 1920 × 1080 PNG'ye yazar ("Gerçek koşum çıktısı" şeridiyle)
  olc(anahtar=değer)            : ölçümü OLCUMLER.json'a ekler (Fusion alanlarına dokunmaz)
"""
import ast, contextlib, io, json, os, pathlib, struct
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAB = pathlib.Path(__file__).resolve().parent
OLC = LAB / "OLCUMLER.json"
CIKTI = LAB / "cikti"
STL = CIKTI / "cay_tepsisi.stl"
os.chdir(LAB)   # oturumlardaki göreli yollar (cikti/…) lab klasörüne göredir
np.set_printoptions(precision=2, suppress=True, linewidth=88)
plt.rcParams.update({"font.size": 22, "font.family": "DejaVu Sans"})

PLA_G_CM3 = 1.24      # NatureWorks Ingeo 4043D teknik veri sayfası, özgül ağırlık 1,24 g/cm³ (ASTM D792) — kaynaklar.py
BARDAK_G = 230        # ÖRNEK: ince belli çay bardağı + tabak + çay (f2_hafiflet.py ile aynı)
KOL_SINIR_G = 2000    # ÖRNEK: kol taşıma sınırı; üretici veri sayfasından alınır, kol duruşuna göre değişir


def fusion():
    """Fusion'da ölçülen değerler (Mac oturumu, 11.10.2026)."""
    return json.loads(OLC.read_text())


def stl_oku(yol=STL):
    b = pathlib.Path(yol).read_bytes()
    n = struct.unpack("<I", b[80:84])[0]
    d = np.frombuffer(b[84:84 + 50 * n], dtype=np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")]))
    return d["v"].reshape(-1, 3, 3).astype(float)


def hacim(tri):
    """Kapalı yüzeyin hacmi (mm³): her üçgen başlangıç noktasıyla bir dörtyüzlü kurar, işaretli hacimler toplanır."""
    return float(np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])).sum() / 6)


def agirlik_merkezi(tri):
    v = np.einsum("ij,ij->i", tri[:, 0], np.cross(tri[:, 1], tri[:, 2])) / 6
    m = tri.sum(axis=1) / 4          # dörtyüzlünün ağırlık merkezi (dördüncü köşe başlangıç noktası)
    return (v[:, None] * m).sum(axis=0) / v.sum()


def kutu(tri):
    p = tri.reshape(-1, 3)
    return p.max(axis=0) - p.min(axis=0)


def alan(tri):
    return float(np.linalg.norm(np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]), axis=1).sum() / 2)


def kesit(tri, eksen, deger):
    """Üçgenleri eksen = deger düzlemiyle keser; her üçgenden en çok bir çizgi parçası (öbür iki eksende) döner."""
    o = [i for i in range(3) if i != eksen]
    d = tri[:, :, eksen] - deger
    parcalar = []
    for t, s in zip(tri, d):
        nok = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            if (s[i] > 0) != (s[j] > 0):
                k = s[i] / (s[i] - s[j])
                p = t[i] + k * (t[j] - t[i])
                nok.append(p[o])
        if len(nok) == 2:
            parcalar.append(nok)
    return np.array(parcalar)


def _j(v):
    if isinstance(v, np.ndarray):
        return [_j(x) for x in v.tolist()]
    if isinstance(v, (list, tuple)):
        return [_j(x) for x in v]
    if isinstance(v, dict):
        return {k: _j(x) for k, x in v.items()}
    if isinstance(v, (float, np.floating)):
        return round(float(v), 4)
    if isinstance(v, (np.integer,)):
        return int(v)
    return v


def olc(**kw):
    d = json.loads(OLC.read_text()) if OLC.exists() else {}
    for k in kw:
        assert k not in ("f1", "f2", "f3", "dilim", "fusion", "tarih"), f"{k}: Fusion ölçümü alanı, değiştirilmez"
    d.update({k: _j(v) for k, v in kw.items()})
    OLC.write_text(json.dumps(d, ensure_ascii=False, indent=1))


def oturum(ders, ad, kod, ns=None):
    """Kodu etkileşimli Python oturumu gibi çalıştırır: ifadenin değeri yazdırılır, atama sessizdir."""
    ns = {} if ns is None else ns
    ns.setdefault("__name__", "__oturum__")
    kod = kod.strip("\n")
    agac = ast.parse(kod)
    satirlar = kod.splitlines()
    out = []
    for st in agac.body:
        parca = satirlar[st.lineno - 1: st.end_lineno]
        out.append(">>> " + parca[0])
        out += ["... " + l for l in parca[1:]]
        if len(parca) > 1:
            out.append("...")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            if isinstance(st, ast.Expr):
                v = eval(compile(ast.Expression(st.value), "<oturum>", "eval"), ns)
                if v is not None:
                    print(repr(v))
            else:
                exec(compile(ast.Module([st], []), "<oturum>", "exec"), ns)
        out += buf.getvalue().rstrip("\n").splitlines() if buf.getvalue() else []
    yol = LAB / "ekran" / ders / f"{ad}.txt"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("\n".join(out) + "\n", encoding="utf-8")
    return ns


def sekil(baslik):
    """1920 × 1080 boş çizim + üst şerit; çizim alanı döner."""
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor("white")
    fig.patches.append(matplotlib.patches.Rectangle((0, 0.925), 1, 0.075, transform=fig.transFigure, fc="#1f2a37", zorder=0))
    fig.text(0.016, 0.962, baslik, color="white", fontsize=26 if len(baslik) <= 58 else 21, va="center", ha="left")
    return fig


def ekran_kaydet(fig, ders, ad, kaynak):
    fig.text(0.984, 0.962, "Gerçek koşum çıktısı", color="#c7d7ea", fontsize=19, va="center", ha="right")
    fig.text(0.016, 0.885, f"Python · NumPy + Matplotlib · ders {ders} · kaynak: {kaynak}", color="#6B7280", fontsize=17, va="center", ha="left")
    yol = LAB / "ekran" / ders / f"{ad}.png"
    yol.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(yol, dpi=100, facecolor="white")
    plt.close(fig)
    return yol


def tr(x, basamak=1):
    return f"{x:,.{basamak}f}".replace(",", "X").replace(".", ",").replace("X", ".")
