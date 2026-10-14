"""Datos de gruposancarlos.pro: coordenadas (desde las ligas oficiales de Google Maps) e inventario del KRM (hoja de Google)."""
import json, os, re, urllib.request, statistics
os.makedirs("datos", exist_ok=True)
UBIC = {  # desarrollo: liga oficial de ubicación (archivo UBICACIONES MAPS de Grupo San Carlos)
 "colinas-de-san-isidro": "https://maps.app.goo.gl/PLZpjUfgvCwgGXNY7", "gran-san-rafael": "https://maps.app.goo.gl/vuBVfHD31cjw8rhFA",
 "panorama-las-fuentes": "https://maps.app.goo.gl/o1WvAcEx66NzaqiPA", "parques-del-bosque-2": "https://maps.app.goo.gl/HGWTkN1QczGLPk6t6",
 "parques-del-bosque": "https://maps.app.goo.gl/SaZDHFT1F2H1JHvy8", "parques-vallarta": "https://maps.app.goo.gl/UhRUXQayKBg24LcN9",
 "coto-nogal": "https://bit.ly/UbicaCotoNogal", "coras": "https://maps.app.goo.gl/3rrs6TLB6cpBosRQ7", "celestia": "https://maps.app.goo.gl/hFroa46wLH74PszNA",
 "ventana-sur": "https://bit.ly/UbicaVentanaSur", "oficinas-gsc": "https://maps.app.goo.gl/hKXF9UWG7Wfoj3hk6"}
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

def coords(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            final, html = r.geturl(), r.read(400000).decode("utf-8", "ignore")
        for texto in (final, html):
            for pat in (r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", r"@(-?\d+\.\d+),(-?\d+\.\d+)", r"[?&](?:q|ll|query)=(-?\d+\.\d+),\s*(-?\d+\.\d+)", r"center=(-?\d+\.\d+)%2C(-?\d+\.\d+)"):
                m = re.search(pat, texto)
                if m:
                    la, lo = float(m.group(1)), float(m.group(2))
                    if 19.5 < la < 21.5 and -104.5 < lo < -102.5:
                        return {"lat": la, "lon": lo, "fuente": final[:200]}
        return {"error": "sin coordenadas", "final": final[:200]}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {str(e)[:120]}"}

ubic = {k: coords(v) for k, v in UBIC.items()}
json.dump(ubic, open("datos/ubicaciones.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Ubicaciones:", {k: ("OK" if "lat" in v else v.get("error")) for k, v in ubic.items()})

# Inventario del KRM (hoja "Grupo San Carlos – Inventario oficial", compartida con la cuenta de MAX)
try:
    import gspread
    from google.oauth2.service_account import Credentials
    cr = Credentials.from_service_account_info(json.loads(os.environ["GOOGLE_CREDENTIALS"]), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly", "https://www.googleapis.com/auth/drive.readonly"])
    libro = gspread.authorize(cr).open_by_key(os.environ["HOJA_KRM"])
    filas = libro.worksheets()[0].get_all_records()
    json.dump(filas, open("datos/inventario.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("Inventario:", len(filas), "filas; columnas:", list(filas[0].keys()) if filas else [])
except Exception as e:
    print("Inventario no disponible todavía:", type(e).__name__, str(e)[:200])
# 2026-10-14T03:41:35
