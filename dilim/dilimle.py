"""STL'i PrusaSlicer komut satırıyla dilimler ve baskı süresi / filament miktarını OLCUMLER.json'a yazar.
Kullanım:  python dilim/dilimle.py [stl yolu]      (varsayılan: beklenen/g1_cay_tepsisi.stl)
Fusion Y-yukarı dışa aktarır; dilimleyici Z-yukarı çalışır → model X ekseninde 90° döndürülür."""
import json, pathlib, re, subprocess, sys
B = pathlib.Path(__file__).resolve().parent.parent
stl = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else B / "beklenen/g1_cay_tepsisi.stl"
out = B / "dilim/tepsi_pla.gcode"
AYAR = ["--rotate-x", "90", "--max-print-height", "250", "--nozzle-diameter", "0.4", "--filament-diameter", "1.75",
        "--layer-height", "0.2", "--first-layer-height", "0.2", "--perimeters", "2", "--top-solid-layers", "4",
        "--bottom-solid-layers", "3", "--fill-density", "15%", "--fill-pattern", "gyroid", "--filament-type", "PLA",
        "--filament-density", "1.24", "--temperature", "210", "--bed-temperature", "60",
        "--bed-shape", "0x0,250x0,250x210,0x210", "--center", "125,105"]
subprocess.run(["prusa-slicer", "--export-gcode", *AYAR, "--output", str(out), str(stl)], check=True)
g = out.read_text(errors="ignore")
sure = re.search(r"estimated printing time \(normal mode\) = (.+)", g).group(1).strip()
h = sum(int(v) * {"d": 1440, "h": 60, "m": 1, "s": 1 / 60}[u] for v, u in re.findall(r"(\d+)([dhms])", sure))
yardim = subprocess.run(["prusa-slicer", "--help"], capture_output=True, text=True); m = re.search(r"PrusaSlicer-[\w.+-]+", yardim.stdout + yardim.stderr)
r = dict(surum=m.group(0) if m else "?",
         filament_g=float(re.search(r"filament used \[g\] = ([\d.]+)", g).group(1)),
         filament_m=round(float(re.search(r"filament used \[mm\] = ([\d.]+)", g).group(1)) / 1000, 2),
         baski_sure=sure, baski_dk=round(h), katman=g.count(";LAYER_CHANGE"))
(B / "dilim/OLCUMLER.json").write_text(json.dumps(r, indent=1, ensure_ascii=False))
print(json.dumps(r, ensure_ascii=False))
