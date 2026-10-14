"""Trae del sitio oficial gruposancarlos.com las fotos y los datos (m², recámaras, amenidades) de cada desarrollo que comercializamos."""
import io, json, os, re, html, urllib.request, urllib.parse, unicodedata
from PIL import Image, ImageOps
BASE = "https://gruposancarlos.com/"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
NOMBRES = {"celestia": ["celestia"], "ventana-sur": ["ventana sur", "ventana-sur", "ventanasur"], "panorama-las-fuentes": ["panorama"], "colinas-de-san-isidro": ["colinas de san isidro", "colinas", "san isidro"],
           "parques-vallarta": ["parques vallarta", "parques-vallarta", "parquesvallarta"], "bosque-vii": ["bosque vii", "bosque-vii", "bosque 7"], "parques-del-bosque-2": ["parques del bosque", "parques-del-bosque", "bosque 2"],
           "gran-san-rafael": ["gran san rafael", "gran-san-rafael", "gransanrafael"], "coras-living": ["coras"]}
def get(u, b=False):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()
    return r if b else r.decode("utf-8", "ignore")
def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
os.makedirs("datos/oficial", exist_ok=True)
paginas = {"celestia": "https://celestiavertical.com/", "ventana-sur": "https://ventanasur.mx/", "panorama-las-fuentes": "https://panoramalasfuentes.com/",
           "colinas-de-san-isidro": "https://www.colinasdesanisidro.com/", "parques-vallarta": "https://www.parquesvallarta.com/", "bosque-vii": "https://cotocaoba.com/",
           "parques-del-bosque-2": "https://parquesdelbosque.com.mx/", "coras-living": "https://corasliving.com/"}
print("Páginas encontradas:", json.dumps(paginas, ensure_ascii=False, indent=1))
fotos_json = json.load(open("datos/fotos.json")) if os.path.exists("datos/fotos.json") else {}
for slug, u in paginas.items():
    try:
        h = get(u)
        dom = urllib.parse.urlparse(u).netloc
        for href in re.findall(r'href="([^"#]+)"', h)[:200]:
            v = urllib.parse.urljoin(u, href)
            if urllib.parse.urlparse(v).netloc == dom and re.search(r"galer|amenid|modelo|depa|casa|prototip|terreno|ubicac", v, re.I) and not re.search(r"\.(pdf|jpe?g|png|webp)$", v, re.I):
                try:
                    h += get(v)
                except Exception:
                    pass
        texto = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " | ", re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S))))
        claves = sorted(set(m.strip(" |") for m in re.findall(r"[^|]{0,90}(?:m²|m2|rec[aá]mara|baño|estacionamiento|cajones?|alberca|casa club|gimnasio|roof|terraza|amenidad|asador|parque|seguridad|acceso controlado|ludoteca|cowork|elevador)[^|]{0,90}", texto, re.I) if 8 < len(m.strip(" |")) < 180))
        imgs = []
        for src in re.findall(r'(?:src|data-src|href)="([^"]+\.(?:jpe?g|png|webp))"', h, re.I):
            s = urllib.parse.urljoin(u, src)
            if any(x in s.lower() for x in ("logo", "icon", "asesores", "slider/sliders", "banner_og")) or s in imgs:
                continue
            imgs.append(s)
        guardadas = []
        os.makedirs(f"fotos/{slug}", exist_ok=True)
        for f in os.listdir(f"fotos/{slug}"): os.remove(f"fotos/{slug}/{f}")
        for s in imgs[:40]:
            try:
                im = ImageOps.exif_transpose(Image.open(io.BytesIO(get(s, True)))).convert("RGB")
                if im.width * im.height < 300_000 or im.width / im.height > 3 or im.height / im.width > 2.2:
                    continue
                im.thumbnail((1600, 1600)); ruta = f"fotos/{slug}/{len(guardadas)+1:02d}.jpg"
                im.save(ruta, "JPEG", quality=78, optimize=True, progressive=True); guardadas.append(ruta)
                if len(guardadas) >= 14: break
            except Exception:
                pass
        if guardadas:
            fotos_json[slug] = guardadas
        json.dump({"url": u, "datos": claves[:80], "imagenes_encontradas": len(imgs), "guardadas": len(guardadas)}, open(f"datos/oficial/{slug}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"{slug}: {len(guardadas)} fotos de {len(imgs)} imágenes; {len(claves)} datos")
    except Exception as e:
        print(slug, "error", type(e).__name__, str(e)[:120])
# la clasificación (fotos/planos/portada) la hace herramientas/clasificar_fotos.py
