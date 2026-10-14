"""Clasifica las fotos de cada desarrollo: 'fotos' (para portada y galería, sin fondo blanco ni formato de banner) y 'planos' (plantas sobre fondo blanco)."""
import json, os
from PIL import Image
def tipo(ruta):
    im = Image.open(ruta).convert("L"); w, h = im.size; r = w / h
    p = im.resize((80, max(1, int(80 * h / w)))).get_flattened_data()
    blanco = sum(1 for x in p if x > 235) / len(p)
    if blanco > 0.45: return "plano", 0
    if r > 2.15: return "banner", 0
    return "foto", (1 if 1.25 <= r <= 1.9 else 0.5) - blanco
salida = {}
for slug in sorted(os.listdir("fotos")):
    rutas = sorted(os.path.join("fotos", slug, f) for f in os.listdir(os.path.join("fotos", slug)) if f.endswith(".jpg"))
    cl = [(r, *tipo(r)) for r in rutas]
    fotos = [r for r, t, s in sorted((c for c in cl if c[1] == "foto"), key=lambda c: -c[2])] + [r for r, t, s in cl if t == "banner"]
    salida[slug] = {"fotos": fotos, "planos": [r for r, t, s in cl if t == "plano"], "portada": next((r for r, t, s in sorted(cl, key=lambda c: -c[2]) if t == "foto"), None)}
PREFERIDAS = {"celestia": "fotos/celestia/01.jpg", "ventana-sur": "fotos/ventana-sur/01.jpg"}  # el edificio como portada
for k, r in PREFERIDAS.items():
    if k in salida and os.path.exists(r):
        salida[k]["portada"] = r
        if r in salida[k]["planos"]: salida[k]["planos"].remove(r)
        if r not in salida[k]["fotos"]: salida[k]["fotos"].insert(0, r)
json.dump(salida, open("datos/fotos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (len(v["fotos"]), len(v["planos"]), bool(v["portada"])) for k, v in salida.items()})
