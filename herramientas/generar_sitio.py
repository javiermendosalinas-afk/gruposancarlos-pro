"""Genera gruposancarlos.pro desde datos oficiales: inventario del KRM (datos/inventario.json) y ubicaciones (datos/ubicaciones.json).

Se ejecuta cada mañana después de la tarea de datos, así precios y disponibilidad siempre son los del desarrollador."""
# Medición de Google Ads y Analytics (igual que bellavittoria.vip): clic a WhatsApp o llamada = conversión
MEDICION = '<script async src="https://www.googletagmanager.com/gtag/js?id=AW-741016611"></script>\n<script>\nwindow.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}\ngtag(\'js\',new Date());gtag(\'config\',\'AW-741016611\');gtag(\'config\',\'G-NXLF42YLWF\');\nwindow.ACIERTA_CONV_LABEL=\'AXCuCP-hrZ0dEKOIrOEC\';/* cuando exista la conversion "Clic en WhatsApp", va aqui su etiqueta */\ndocument.addEventListener(\'click\',function(e){var a=e.target.closest&&e.target.closest(\'a[href*="wa.me/"],a[href^="tel:"]\');if(!a)return;\n var wa=a.href.indexOf(\'wa.me/\')>=0;gtag(\'event\',wa?\'clic_whatsapp\':\'clic_llamada\',{sitio:location.hostname,destino:a.href.slice(0,120)});\n if(wa&&window.ACIERTA_CONV_LABEL)gtag(\'event\',\'conversion\',{send_to:\'AW-741016611/\'+window.ACIERTA_CONV_LABEL});},true);\n</script>'
import json, os, re, math, html, urllib.parse, collections, datetime
E = lambda s: html.escape(str(s), quote=True)
WA = "523333777337"
INV = json.load(open("datos/inventario.json", encoding="utf-8"))
UB = json.load(open("datos/ubicaciones.json", encoding="utf-8"))
FOTOS = json.load(open("datos/fotos.json", encoding="utf-8")) if os.path.exists("datos/fotos.json") else {}
num = lambda s: float(re.sub(r"[^\d.]", "", str(s)) or 0)
din = lambda v: "$" + f"{v:,.0f}"
mill = lambda v: f"${v/1e6:,.2f} millones"
def wa(t): return f"https://wa.me/{WA}?text=" + urllib.parse.quote(t)
HITOS = {"ITESO": (20.6085, -103.4153), "Plaza del Sol": (20.6497, -103.4012), "Andares": (20.7101, -103.4122), "la Glorieta Minerva": (20.6745, -103.3878),
         "el Centro de Guadalajara": (20.6767, -103.3475), "el Aeropuerto": (20.5218, -103.3111), "Plaza Galerías": (20.6814, -103.4378)}
def km(a, b):
    R = 6371; la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    return 2 * R * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
MESES = ["", "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
def fecha(s):
    m = re.match(r"(\d{2})-(\d{2})-(\d{4})", str(s or ""))
    return (int(m.group(3)), int(m.group(2))) if m else None
HOY = datetime.date.today()
from especificaciones import SPECS

# Perfil editorial de cada desarrollo: solo hechos verificables (desarrollador, notas de prensa, coordenadas oficiales).
DES = {
 "CELESTIA": {"slug": "celestia", "nombre": "Celestia Atmósfera Vertical", "zona": "Jardines del Bosque, Guadalajara", "ub": "celestia", "tipo": "Departamentos",
   "gancho": "Despierta cada día con la ciudad a tus pies, a pasos de la Minerva.",
   "historia": "Imagina llegar a casa y que la vista te cambie el día. Celestia es la torre que Grupo San Carlos diseñó con Tacher Arquitectos sobre Avenida Niños Héroes, en Jardines del Bosque: a menos de un kilómetro de la Glorieta Minerva y a minutos de Plaza del Sol, sin renunciar a la tranquilidad de una colonia consolidada. Cada departamento lleva el nombre de un planeta y está pensado para aprovechar cada metro, con terrazas para tu café de la mañana o tu reunión de los viernes. Comprar hoy, en preventa, es asegurar tu lugar a precio de etapa temprana.",
   "puntos": ["Diseño de Tacher Arquitectos", "Avenida Niños Héroes, en Jardines del Bosque", "Departamento modelo y showroom en calle Firmamento", "Comprar en preventa permite apartar a precio de etapa temprana"],
   "tours": [("Departamento Luna", "https://bit.ly/LunaCelestia")]},
 "VENTANA SUR": {"slug": "ventana-sur", "nombre": "Ventana Sur", "zona": "Av. del Tesoro, Tlaquepaque", "ub": "ventana-sur", "tipo": "Departamentos",
   "gancho": "Tu primer hogar, o tu mejor inversión, en el sur de la ciudad.",
   "historia": "Hay decisiones que cambian la manera en que vives tu semana. En Ventana Sur, sobre Av. del Tesoro, en Tlaquepaque, tienes cerca Periférico, el corredor López Mateos, universidades, comercios y servicios. Sus departamentos de 65 a 86 m² tienen una recámara principal con baño y un espacio flexible que puedes convertir en oficina, estar o recámara, y algunos suman un roof top privado para tus tardes al aire libre. Es el lugar ideal para empezar, o para que tu dinero trabaje por ti.",
   "puntos": ["Cerca de Periférico y del corredor López Mateos", "Departamentos en varios niveles con vista", "Entrega programada para 2027"], "tours": []},
 "PANORAMA": {"slug": "panorama-las-fuentes", "nombre": "Panorama las Fuentes", "zona": "Las Fuentes, Tlaquepaque", "ub": "panorama-las-fuentes", "tipo": "Departamentos",
   "gancho": "Vive dentro de Periférico, con un parque para tu familia junto a tu puerta.",
   "historia": "Piensa en tus hijos jugando en un parque de más de 640 m², mientras tú haces ejercicio en la zona de calistenia o trabajas con wifi al aire libre. Panorama las Fuentes, en Prolongación Av. Las Fuentes 1296, Tlaquepaque, reúne torres de departamentos dentro de Periférico, con modelos Verano y Primavera, y roof garden privado en los niveles altos. Es la comodidad de vivir cerca de todo, con espacio para respirar.",
   "puntos": ["Modelos Verano y Primavera", "Niveles altos con roof garden", "Entregas escalonadas por torre"],
   "tours": [("Departamento Verano", "https://bit.ly/DepaVeranoPanorama"), ("Departamento Primavera", "https://bit.ly/DepaPrimaveraPanorama")]},
 "SAN ISIDRO": {"slug": "colinas-de-san-isidro", "nombre": "Colinas de San Isidro", "zona": "San Isidro, Zapopan", "ub": "colinas-de-san-isidro", "tipo": "Casas y departamentos",
   "gancho": "Vuelve a casa rodeado de naturaleza, sin alejarte de la ciudad.",
   "historia": "Hay un momento del día en que todo se calma: cuando llegas a casa. En Colinas de San Isidro, en el norte de Zapopan, ese momento te espera entre más de 5,000 m² de áreas verdes, con alberca, casa club y vistas al bosque, a minutos de Costco San Isidro y de los servicios del norte de la ciudad. Elige entre casas de varios modelos o departamentos, y recorre la casa modelo para imaginar tu vida ahí.",
   "puntos": ["Casas y departamentos en un mismo desarrollo", "Casa club", "A minutos del Costco San Isidro", "Casa modelo para recorrer"],
   "tours": [("Casa club", "https://bit.ly/CasaClubCS"), ("Departamento", "https://bit.ly/DepartamentoCSI"), ("Modelo Cordillera", "https://bit.ly/ModeloCordillera"), ("Modelo Cañada", "https://bit.ly/ModeloCanada"), ("Modelo Prado", "https://bit.ly/ModeloPrado")]},
 "PARQUES VALLARTA": {"slug": "parques-vallarta", "nombre": "Parques Vallarta", "zona": "Zapopan, con acceso por Av. Inglaterra", "ub": "parques-vallarta", "tipo": "Terrenos",
   "gancho": "Construye exactamente la casa que siempre has imaginado.",
   "historia": "Tu casa ideal no está en un catálogo: está en tu cabeza. En Parques Vallarta Residencial, en Zapopan, con acceso por Av. Inglaterra, tienes el terreno para hacerla realidad, alrededor de un gran parque central de 34,000 m², con alberca, asoleadero y la seguridad de una urbanización de Grupo San Carlos. Lotes desde 165 m², para construir a tu medida o para proteger tu patrimonio como inversión.",
   "puntos": ["Terrenos urbanizados en cotos", "Listos para construir", "Ideal para construir a tu medida o invertir"], "tours": []},
 "BOSQUE VII": {"slug": "bosque-vii", "nombre": "Coto Caoba (Bosque VII)", "zona": "Parques del Bosque, Tlaquepaque", "ub": "parques-del-bosque", "tipo": "Departamentos",
   "gancho": "Tu departamento propio, en una comunidad que ya está viva.",
   "historia": "Pocas cosas dan tanta tranquilidad como saber que tu familia vive en un lugar seguro y con vecinos. Coto Caoba (Bosque VII), en Independencia 3342, Parques del Bosque, Tlaquepaque, te ofrece departamentos de 2 recámaras y 2 baños dentro de una comunidad establecida, con caseta de control de ingreso y un parque lineal con áreas verdes. Elige planta baja con patio, un nivel intermedio o el tercer nivel con un roof garden de casi 55 m² solo para ti.",
   "puntos": ["Planta baja, niveles intermedios y tercer nivel con roof garden", "Dentro de una comunidad establecida", "Entregas en 2027"],
   "tours": [("Departamento Bosque", "http://bit.ly/DepartamentoPBosque")]},
 "BOSQUE 2DA SECCION": {"slug": "parques-del-bosque-2", "nombre": "Parques del Bosque 2ª Sección", "zona": "Parques del Bosque, Tlaquepaque", "ub": "parques-del-bosque-2", "tipo": "Casas",
   "gancho": "Una casa de tres recámaras para que cada quien tenga su espacio.",
   "historia": "Cuando la familia crece, el espacio importa. En Parques del Bosque 2ª Sección, en el sur de Tlaquepaque, tus hijos tendrán su recámara y tú, la tranquilidad de una comunidad con áreas verdes y acceso controlado. Sus casas Fresno y CAP, de 101 a 122 m² de construcción, se entregan a fines de 2026: el tiempo justo para planear tu mudanza.",
   "puntos": ["Casas Fresno y CAP", "Entrega programada para el 31 de octubre de 2026", "Venta de contado"], "tours": [("Casa Fresno 102", "http://bit.ly/CasaFresno102")]},
 "GRAN SAN RAFAEL": {"slug": "gran-san-rafael", "nombre": "Gran San Rafael", "zona": "Oriente de Guadalajara", "ub": "gran-san-rafael", "tipo": "Casas",
   "gancho": "Mudarte ya es posible: casas terminadas, listas para estrenar.",
   "historia": "No todos pueden esperar una preventa, y no tienes por qué hacerlo. En Gran San Rafael, en el oriente de Guadalajara, las casas Magnolia de Grupo San Carlos están terminadas y listas para que te mudes. Quedan pocas unidades.",
   "puntos": ["Casas Magnolia", "Listas para habitar", "Últimas unidades disponibles"], "tours": [("Casa Magnolia", "https://bit.ly/RecorridoMagnolia")]},
 "CORAS": {"slug": "coras-living", "nombre": "Coras Living", "zona": "Av. Las Palmas, Puerto Vallarta", "ub": "coras", "tipo": "Departamentos",
   "gancho": "Tu departamento frente al encanto de Puerto Vallarta.", "historia": "Imagina tus fines de semana, o tus ingresos por renta, en Puerto Vallarta. Coras Living, en Av. Las Palmas 253, es el desarrollo de Grupo San Carlos en la costa: departamentos terminados de 2 recámaras y 2 baños, con aire acondicionado y área de camastros. Quedan muy pocas unidades.",
   "puntos": ["Departamentos terminados", "En Puerto Vallarta", "Últimas unidades"], "tours": [("Departamento Coras", "https://bit.ly/DepaCoras")], "vallarta": True},
}
# ---- datos por desarrollo desde el KRM
G = collections.defaultdict(list)
for r in INV:
    if "valle imperial" in str(r.get("Desarrollo", "")).lower():
        continue
    G[str(r.get("Desarrollo", "")).strip().upper()].append(r)
def resumen(k):
    v = [r for r in G.get(k, []) if str(r.get("Estatus (disponible/apartado/vendido)", "")).lower().startswith("disp")]
    ps = sorted(num(r.get("Precio")) for r in v if num(r.get("Precio")) > 100000)
    mods = collections.Counter(re.sub(r"[-_ ](E|S|N)$", "", str(r.get("Modelo", "")).split("-E")[0]) for r in v)
    fs = sorted(f for f in (fecha(r.get("Fecha promesa de entrega (portal)")) for r in v) if f)
    cond = str(v[0].get("Condiciones o promociones vigentes", "")) if v else ""
    desc = any(num(re.sub(r".*Descuento vigente:", "", str(r.get("Condiciones o promociones vigentes", "")))) > 0 for r in v if "Descuento" in str(r.get("Condiciones o promociones vigentes", "")))
    ent = "Inmediata" if fs and fs[-1] <= (HOY.year, HOY.month) else (f"desde {MESES[fs[0][1]]} de {fs[0][0]}" if fs and fs[0] > (HOY.year, HOY.month) else (f"inmediata y hasta {MESES[fs[-1][1]]} de {fs[-1][0]}" if fs else "Consultar"))
    return {"n": len(v), "min": ps[0] if ps else 0, "max": ps[-1] if ps else 0, "modelos": mods, "entrega": ent, "contado": "SOLO CONTADO" in cond.upper(), "descuento": desc,
            "lista": str(v[0].get("Fecha de la lista de precios", "")) if v else ""}
R = {k: resumen(k) for k in DES}
def opciones(k, slug):
    sp = SPECS.get(slug, {}); reglas = sp.get("reglas", [])
    v = [r for r in G.get(k, []) if str(r.get("Estatus (disponible/apartado/vendido)", "")).lower().startswith("disp")]
    grupos = collections.OrderedDict()
    for r in v:
        mod = str(r.get("Modelo", "")).upper()
        regla = next((x for x in reglas if re.search(x[0], mod)), None) or ("", mod.replace("-", " ").title(), "", "", False)
        g = grupos.setdefault(regla[1], {"m2": regla[2], "dist": regla[3], "aprox": regla[4], "precios": [], "fechas": []})
        if num(r.get("Precio")) > 100000: g["precios"].append(num(r.get("Precio")))
        f = fecha(r.get("Fecha promesa de entrega (portal)"))
        if f: g["fechas"].append(f)
    filas = []
    for n, g in sorted(grupos.items(), key=lambda x: min(x[1]["precios"] or [0])):
        ps = sorted(g["precios"]); fs = sorted(g["fechas"])
        ent = "Inmediata" if fs and fs[-1] <= (HOY.year, HOY.month) else (f"{MESES[fs[0][1]].capitalize()} {fs[0][0]}" if fs else "Consultar")
        filas.append((n, g["m2"] + ("*" if g["aprox"] and g["m2"] else ""), g["dist"], ps[0] if ps else 0, ps[-1] if ps else 0, len(ps), ent))
    return filas, any(g["aprox"] for g in grupos.values())

def cercanias(ubk):
    u = UB.get(ubk, {})
    if "lat" not in u:
        return []
    p = (u["lat"], u["lon"]); d = sorted(((km(p, h), n) for n, h in HITOS.items()))
    return [(n, x) for x, n in d[:4]]

CSS = """:root{--noche:#1E2340;--jacaranda:#6B4E9B;--jacaranda-claro:#EDE6F6;--cantera:#D9A88F;--cal:#F8F6F2;--tinta:#1B1D26;--suave:#5D6070;--wa:#1FA855;
--serif:"Newsreader",Georgia,serif;--sans:"Archivo",system-ui,-apple-system,"Segoe UI",sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:64px}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--cal);color:var(--tinta);font:400 17px/1.6 var(--sans)}a{color:inherit}img{max-width:100%;display:block}
:focus-visible{outline:3px solid var(--cantera);outline-offset:3px}
.c{max-width:1180px;margin:0 auto;padding:0 22px}h1,h2,h3{font-family:var(--serif);font-weight:500;line-height:1.08;margin:0}
h2{font-size:clamp(2rem,4.6vw,3.2rem)}h3{font-size:1.5rem}p{margin:0 0 1em}
.btn{display:inline-flex;align-items:center;justify-content:center;border-radius:6px;padding:14px 22px;font:600 1rem var(--sans);text-decoration:none;border:0;cursor:pointer}
.btn-wa{background:var(--wa);color:#fff}.btn-j{background:var(--jacaranda);color:#fff}.btn-l{box-shadow:inset 0 0 0 1.5px currentColor;background:transparent}
.barra{position:sticky;top:0;z-index:1000;background:var(--noche);color:#fff}.barra .c{display:flex;align-items:center;justify-content:space-between;height:60px;gap:12px}
.marca{text-decoration:none;font-weight:700;letter-spacing:.01em}.marca span{color:var(--cantera);font-weight:500}
.sello{display:inline-block;background:var(--cantera);color:var(--noche);font-weight:700;border-radius:999px;padding:6px 14px;font-size:.9rem}
.tabs{background:#fff;border-bottom:1px solid #E5E1EA;position:sticky;top:60px;z-index:999;overflow-x:auto;white-space:nowrap}
.tabs .c{display:flex;gap:4px}.tabs a{display:inline-block;padding:14px 14px;text-decoration:none;font-weight:600;color:var(--suave);border-bottom:3px solid transparent}
.tabs a[aria-current]{color:var(--jacaranda);border-color:var(--jacaranda)}
.hero{background:var(--noche);color:#fff;padding:48px 0 0}.hero .c{display:grid;grid-template-columns:.9fr 1.1fr;gap:36px;align-items:stretch}
.hero h1{font-size:clamp(2.4rem,5vw,4rem);margin:16px 0 14px}.hero p{color:#C9CBDA;font-size:1.1rem;max-width:32em}
#mapa{min-height:470px;border-radius:14px 14px 0 0}.leyenda{color:#C9CBDA;font-size:.9rem;margin-top:10px}
@media(max-width:900px){.hero .c{grid-template-columns:1fr}#mapa{min-height:380px}}
.sec{padding:84px 0}.intro{max-width:42em;color:var(--suave);font-size:1.1rem;margin-top:14px}
.trayectoria{display:grid;grid-template-columns:repeat(4,1fr);gap:0;margin-top:44px;border-top:2px solid var(--noche)}
.trayectoria div{padding:18px 16px 0 0}.trayectoria b{display:block;font-family:var(--serif);font-weight:500;font-size:2.6rem;line-height:1;color:var(--jacaranda)}.trayectoria span{color:var(--suave)}
@media(max-width:760px){.trayectoria{grid-template-columns:1fr 1fr}.trayectoria div{padding-bottom:16px}}
.porque{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:40px}.porque div{border-left:3px solid var(--cantera);padding:4px 0 4px 16px}
.porque h3{font-size:1.3rem;margin-bottom:6px}.porque p{color:var(--suave);font-size:.98rem;margin:0}@media(max-width:900px){.porque{grid-template-columns:1fr}}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px;margin-top:36px}
.tarj{background:#fff;border:1px solid #E5E1EA;border-radius:14px;overflow:hidden;text-decoration:none;display:flex;flex-direction:column}
.tarj .img{aspect-ratio:16/9;background:linear-gradient(135deg,var(--jacaranda),var(--noche)) center/cover;display:flex;align-items:flex-end;padding:12px}
.tarj .img span{background:rgba(30,35,64,.85);color:#fff;font-size:.85rem;border-radius:999px;padding:4px 10px}
.tarj .tx{padding:16px}.tarj h3{font-size:1.4rem;margin-bottom:4px}.tarj .z{color:var(--suave);font-size:.95rem}.tarj .p{font-weight:700;margin-top:10px}
.autorizada{background:var(--jacaranda-claro)}.autorizada .c{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}
.autorizada ul{margin:0;padding-left:20px;line-height:1.9}@media(max-width:900px){.autorizada .c{grid-template-columns:1fr}}
.d-hero{background:var(--noche);color:#fff;padding:54px 0 60px}.d-hero .c{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.d-hero h1{font-size:clamp(2.4rem,5.4vw,4.2rem);margin:14px 0}.d-hero .gancho{font-family:var(--serif);font-size:1.5rem;color:#E4DDF0;margin-bottom:18px}
.d-precio{display:flex;gap:28px;flex-wrap:wrap;margin:16px 0 24px}.d-precio span{display:block;color:#B9BCCE;font-size:.95rem}.d-precio b{font-family:var(--serif);font-weight:500;font-size:2.1rem}
.d-hero .foto{aspect-ratio:4/3;border-radius:14px;background:linear-gradient(135deg,var(--jacaranda),#2A2F55) center/cover}
@media(max-width:900px){.d-hero .c{grid-template-columns:1fr}}
.dos{display:grid;grid-template-columns:1.1fr .9fr;gap:48px}@media(max-width:900px){.dos{grid-template-columns:1fr}}
.puntos{list-style:none;padding:0;margin:20px 0 0}.puntos li{padding:12px 0;border-bottom:1px solid #E5E1EA}
.cerca{background:#fff;border:1px solid #E5E1EA;border-radius:14px;padding:22px}.cerca li{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #EEE}
.cerca ul{list-style:none;padding:0;margin:10px 0 0}.mini{height:240px;border-radius:12px;margin-top:14px}
.mods{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:10px;margin-top:20px}.mods div{background:#fff;border:1px solid #E5E1EA;border-radius:10px;padding:12px}
.mods b{display:block}.mods span{color:var(--suave);font-size:.9rem}
.tours{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}.tours a{background:var(--jacaranda-claro);color:var(--jacaranda);font-weight:600;border-radius:999px;padding:9px 16px;text-decoration:none}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:8px;margin-top:20px}.gal img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:10px}
.aviso{font-size:.88rem;color:var(--suave);margin-top:14px}
.cierre{background:var(--jacaranda);color:#fff;text-align:center}.cierre p{max-width:36em;margin:10px auto 24px;color:#EDE6F6}
footer{background:var(--tinta);color:#A9ABB8;font-size:.87rem;line-height:1.6;padding:40px 0 100px}footer b{color:#fff}
.tabla-env{overflow-x:auto;margin-top:26px;border:1px solid #E5E1EA;border-radius:14px;background:#fff}
.opciones{width:100%;border-collapse:collapse;min-width:720px}.opciones th,.opciones td{padding:14px 16px;text-align:left;border-bottom:1px solid #EEEAF2;vertical-align:top}
.opciones thead th{background:var(--noche);color:#fff;font-weight:600;font-size:.92rem}.opciones tbody th{font-family:var(--serif);font-weight:500;font-size:1.15rem}
.opciones tbody tr:last-child th,.opciones tbody tr:last-child td{border-bottom:0}.opciones td b{white-space:nowrap}
.puntos li::before{content:"";display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--cantera);margin-right:10px;vertical-align:middle}
.flot{position:fixed;left:12px;right:12px;bottom:calc(12px + env(safe-area-inset-bottom));z-index:1001;display:none}.flot .btn{width:100%}@media(max-width:760px){.flot{display:block}}"""

def pagina(titulo, desc, cuerpo, canon, raiz="", activo="", extra_head="", jsld=None):
    tabs = "".join(f'<a href="{raiz}desarrollos/{d["slug"]}.html"{" aria-current=page" if activo == d["slug"] else ""}>{E(d["nombre"].replace(" Atmósfera Vertical",""))}</a>' for k, d in DES.items() if R[k]["n"])
    ld = f'<script type="application/ld+json">{json.dumps(jsld, ensure_ascii=False)}</script>' if jsld else ""
    return f"""<!DOCTYPE html><html lang="es-MX"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(titulo)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="https://gruposancarlos.pro/{canon}"><meta name="robots" content="index,follow">
<meta property="og:title" content="{E(titulo)}"><meta property="og:description" content="{E(desc)}"><meta name="theme-color" content="#1E2340">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500&family=Archivo:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">{extra_head}{ld}<style>{CSS}</style>{MEDICION}</head><body>
<header class="barra"><div class="c"><a class="marca" href="{raiz}index.html">Grupo San Carlos <span>· con Acierta Max</span></a>
<a class="btn btn-wa" style="padding:9px 16px" href="{wa('Hola, vengo de gruposancarlos.pro y quiero información')}" target="_blank" rel="noopener">WhatsApp</a></div></header>
<nav class="tabs" aria-label="Desarrollos"><div class="c"><a href="{raiz}index.html"{" aria-current=page" if activo == "inicio" else ""}>Inicio</a>{tabs}</div></nav>
{cuerpo}
<section class="sec cierre"><div class="c"><h2>No tienes que decidir solo</h2><p>Te ayudamos a comparar, a calcular tu crédito y a elegir con calma. Somos inmobiliaria autorizada de Grupo San Carlos: pagas el mismo precio que con el desarrollador, y la asesoría no te cuesta.</p>
<a class="btn btn-wa" href="{wa('Hola, vengo de gruposancarlos.pro. Quiero que un asesor me ayude a elegir desarrollo')}" target="_blank" rel="noopener">Hablar con un asesor</a></div></section>
<footer><div class="c"><p><b>Acierta Max, S.A. de C.V. · Inmobiliaria autorizada para la comercialización de desarrollos de Grupo San Carlos</b> (excepto Valle Imperial). Profesionales inmobiliarios, miembros de AMPI y NAR. WhatsApp 33 3377 7337 · <a href="https://acierta.pro">acierta.pro</a> · <a href="https://acierta.pro/aviso-privacidad.html">Aviso de privacidad</a></p>
<p>Precios de lista, disponibilidad y fechas promesa de entrega tomados del portal oficial de Grupo San Carlos y actualizados diariamente; sujetos a cambio y a confirmación por escrito antes de apartar. Distancias en línea recta, calculadas con la ubicación oficial de cada desarrollo. Imágenes proporcionadas por el desarrollador; pueden ser ilustrativas. Grupo San Carlos es marca de su titular.</p></div></footer>
<div class="flot"><a class="btn btn-wa" href="{wa('Hola, vengo de gruposancarlos.pro y quiero información')}" target="_blank" rel="noopener">Escríbenos por WhatsApp</a></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script></body></html>"""

def foto_de(slug, i=0):
    f = FOTOS.get(slug, {})
    if isinstance(f, list):
        return f[i] if len(f) > i else None
    return f.get("portada") if i == 0 else (f.get("fotos", [])[i] if len(f.get("fotos", [])) > i else None)
def lista_fotos(slug, clave="fotos"):
    f = FOTOS.get(slug, {})
    return f if isinstance(f, list) and clave == "fotos" else (f.get(clave, []) if isinstance(f, dict) else [])

def main():
    os.makedirs("desarrollos", exist_ok=True)
    puntos = []
    tarjetas = []
    for k, d in DES.items():
        r = R[k]
        if not r["n"]:
            continue
        u = UB.get(d["ub"], {})
        if "lat" in u and not d.get("vallarta"):
            puntos.append({"n": d["nombre"].replace(" Atmósfera Vertical", ""), "lat": u["lat"], "lon": u["lon"], "t": d["tipo"], "p": f"desde {mill(r['min'])}", "u": f"desarrollos/{d['slug']}.html"})
        f0 = foto_de(d["slug"])
        bg = f' style="background-image:url(\'{f0}\')"' if f0 else ""
        tarjetas.append(f'<a class="tarj" href="desarrollos/{d["slug"]}.html"><div class="img"{bg}><span>{E(d["tipo"])} · {r["n"]} disponibles</span></div><div class="tx"><h3>{E(d["nombre"])}</h3><div class="z">{E(d["zona"])}</div><div class="p">Desde {din(r["min"])}</div><div class="z">Entrega {E(r["entrega"])}</div></div></a>')
        # página del desarrollo
        cer = cercanias(d["ub"])
        cer_html = "".join(f"<li><span>{E(n[:1].upper()+n[1:])}</span><b>{x:.1f} km</b></li>" for n, x in cer) if cer else "<li><span>Puerto Vallarta, Jalisco</span><b>Costa</b></li>"
        filas, aprox = opciones(k, d["slug"])
        tabla = "".join(f'<tr><th scope="row">{E(n)}</th><td>{E(m2) or "—"}</td><td>{E(di) or "—"}</td><td><b>{din(lo)}</b>{(" a " + din(hi)) if hi > lo else ""}</td><td>{c}</td><td>{E(en)}</td></tr>' for n, m2, di, lo, hi, c, en in filas)
        sp = SPECS.get(d["slug"], {})
        incluye = "".join(f"<li>{E(x)}</li>" for x in sp.get("incluye", []))
        tours = "".join(f'<a href="{E(u_)}" target="_blank" rel="noopener">▶ Recorrido 360° {E(n)}</a>' for n, u_ in d["tours"])
        gal = "".join(f'<img src="../{E(x)}" alt="{E(d["nombre"])}, imagen oficial {i+1}" loading="lazy">' for i, x in enumerate(lista_fotos(d["slug"])[:12]))
        planos = "".join(f'<img src="../{E(x)}" alt="{E(d["nombre"])}, planta arquitectónica {i+1}" loading="lazy" style="object-fit:contain;background:#fff">' for i, x in enumerate(lista_fotos(d["slug"], "planos")[:8]))
        mini = f'<div id="mini" class="mini" data-lat="{u["lat"]}" data-lon="{u["lon"]}"></div>' if "lat" in u else ""
        f1 = foto_de(d["slug"])
        notas = []
        if r["descuento"]: notas.append("Hay descuentos vigentes en unidades seleccionadas; pregunta por ellos.")
        if r["contado"]: notas.append("Venta de contado.")
        cuerpo = f"""<section class="d-hero"><div class="c"><div><span class="sello">✅ Inmobiliaria autorizada Grupo San Carlos</span><h1>{E(d['nombre'])}</h1><p class="gancho">{E(d['gancho'])}</p>
<div class="d-precio"><div><span>Precio de lista desde</span><b>{din(r['min'])}</b></div><div><span>Disponibles hoy</span><b>{r['n']}</b></div><div><span>Entrega</span><b style="font-size:1.4rem">{E(r['entrega'].capitalize())}</b></div></div>
<a class="btn btn-wa" href="{wa(f"Hola, vengo de gruposancarlos.pro. Me interesa {d['nombre']} y quiero agendar una visita")}" target="_blank" rel="noopener">Agendar una visita</a></div>
<div class="foto"{f' style="background-image:url(&quot;../{f1}&quot;)"' if f1 else ''} role="img" aria-label="{E(d['nombre'])}"></div></div></section>
<section class="sec" id="opciones"><div class="c"><h2>Elige tu opción</h2><p class="intro">{E(sp.get('intro', ''))}</p>
<div class="tabla-env"><table class="opciones"><thead><tr><th scope="col">Tipo</th><th scope="col">Superficie</th><th scope="col">Distribución</th><th scope="col">Precio de lista</th><th scope="col">Disponibles</th><th scope="col">Entrega</th></tr></thead><tbody>{tabla}</tbody></table></div>
<p class="aviso">Precios de lista y disponibilidad del portal oficial de Grupo San Carlos, actualizados hoy; el precio varía por nivel, orientación y ubicación de la unidad.{' *Superficie indicada en la clave oficial del modelo; confírmala con tu asesor.' if aprox else ''}</p>
<p><a class="btn btn-wa" href="{wa(f"Hola, vengo de gruposancarlos.pro. Quiero ver las opciones disponibles de {d['nombre']} y sus planos")}" target="_blank" rel="noopener">Quiero planos y precios exactos</a></p></div></section>
<section class="sec" style="padding-top:0"><div class="c dos"><div><h2>{E(d['tipo'])} en {E(d['zona'])}</h2><p class="intro">{E(d['historia'])}</p>
<h3 style="margin-top:26px">Lo que incluye</h3><ul class="puntos">{incluye or ''.join(f'<li>{E(p)}</li>' for p in d['puntos'])}</ul>{('<p class="aviso">' + ' '.join(notas) + '</p>') if notas else ''}

{('<h3 style="margin-top:30px">Recórrelo desde tu casa</h3><div class="tours">' + tours + '</div>') if tours else ''}</div>
<aside><div class="cerca"><h3>Qué tan cerca te queda</h3><ul>{cer_html}</ul>{mini}<p class="aviso">Distancias en línea recta desde la ubicación oficial del desarrollo.</p></div></aside></div></section>
{('<section class="sec" style="padding-top:0"><div class="c"><h2>Galería oficial</h2><div class="gal">' + gal + '</div></div></section>') if gal else ''}
{('<section class="sec" style="padding-top:0"><div class="c"><h2>Conoce la distribución</h2><p class="intro">Plantas arquitectónicas oficiales de los modelos.</p><div class="gal">' + planos + '</div></div></section>') if planos else ''}
<script>window.addEventListener("load",function(){{var e=document.getElementById("mini");if(!e||!window.L)return;var m=L.map(e,{{scrollWheelZoom:false}}).setView([+e.dataset.lat,+e.dataset.lon],13);L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",{{attribution:"© OpenStreetMap"}}).addTo(m);L.marker([+e.dataset.lat,+e.dataset.lon]).addTo(m);}});</script>"""
        ld = {"@context": "https://schema.org", "@type": "Residence", "name": d["nombre"], "description": d["historia"], "url": f"https://gruposancarlos.pro/desarrollos/{d['slug']}.html",
              "offers": {"@type": "AggregateOffer", "lowPrice": int(r["min"]), "highPrice": int(r["max"]), "priceCurrency": "MXN", "offerCount": r["n"]}}
        if "lat" in u: ld["geo"] = {"@type": "GeoCoordinates", "latitude": u["lat"], "longitude": u["lon"]}
        open(f"desarrollos/{d['slug']}.html", "w", encoding="utf-8").write(pagina(f"{d['nombre']} · {d['tipo']} de Grupo San Carlos desde {din(r['min'])} · Acierta Max",
            f"{d['nombre']}: {d['tipo'].lower()} de Grupo San Carlos en {d['zona']}, desde {din(r['min'])}. {r['n']} disponibles. Acierta Max, inmobiliaria autorizada.", cuerpo, f"desarrollos/{d['slug']}.html", "../", d["slug"], jsld=ld))
    total = sum(R[k]["n"] for k in DES)
    cuerpo = f"""<section class="hero"><div class="c"><div style="padding-bottom:40px"><span class="sello">✅ Acierta Max · Inmobiliaria autorizada</span>
<h1>El hogar que tu familia merece, con quien lleva 60 años construyéndolos</h1><p>Hoy hay {total} departamentos, casas y terrenos de Grupo San Carlos esperando a alguien como tú. Busca tu zona en el mapa, compara opciones y da el paso con la confianza de comprar al desarrollador correcto.</p>
<p style="margin-top:22px"><a class="btn btn-j" href="#desarrollos">Ver desarrollos</a> <a class="btn btn-l" style="color:#fff;margin-left:6px" href="#trayectoria">Por qué Grupo San Carlos</a></p></div>
<div><div id="mapa" role="region" aria-label="Mapa de desarrollos de Grupo San Carlos en la Zona Metropolitana de Guadalajara"></div></div></div></section>
<section class="sec" id="trayectoria"><div class="c"><h2>60 años construyendo Guadalajara</h2>
<p class="intro">Cuando compras una casa, compras también la palabra de quien la construyó. Grupo San Carlos es una empresa tapatía, familiar y con capital local, fundada en 1965 por el ingeniero Salvador Ibarra Álvarez del Castillo. Seis décadas después, miles de familias tapatías celebran sus cumpleaños, sus logros y sus domingos en un hogar hecho por ellos.</p>
<div class="trayectoria"><div><b>1965</b><span>Año de fundación, en Guadalajara</span></div><div><b>60 mil</b><span>viviendas construidas y comercializadas</span></div><div><b>240 mil</b><span>personas con un hogar de Grupo San Carlos</span></div><div><b>16</b><span>desarrollos activos en la Zona Metropolitana</span></div></div>
<div class="porque"><div><h3>Reconocimiento</h3><p>Una de las 50 empresas más destacadas de Jalisco en 2024; su fundador fue reconocido por la Cámara Mexicana de la Industria de la Construcción.</p></div>
<div><h3>Calidad que se garantiza</h3><p>Materiales con certificado de calidad y NOM, y garantía extendida en todas sus casas y departamentos.</p></div>
<div><h3>Comunidades, no solo casas</h3><p>Promueve la organización vecinal para que tu colonia cuide su calidad de vida y la plusvalía de tu patrimonio.</p></div></div></div></section>
<section class="sec" id="desarrollos" style="padding-top:0"><div class="c"><h2>¿Dónde te imaginas viviendo?</h2><p class="intro">Cada desarrollo es una forma distinta de vivir. Precios de lista y disponibilidad del portal oficial de Grupo San Carlos, actualizados cada día.</p><div class="grid">{''.join(tarjetas)}</div></div></section>
<section class="sec autorizada"><div class="c"><div><h2>Por qué comprar con Acierta Max</h2><p class="intro">Somos inmobiliaria autorizada para comercializar los desarrollos de Grupo San Carlos. Compras al mismo precio y con las mismas condiciones del desarrollador, con más acompañamiento.</p></div>
<ul><li>Mismo precio y condiciones que con el desarrollador</li><li>Comparamos desarrollos para que elijas con datos</li><li>Calculamos tu crédito bancario o Infonavit sin costo</li><li>Acierta Verifica: revisión antes de firmar</li><li>Atención por WhatsApp las 24 horas</li></ul></div></section>
<script>var PUNTOS={json.dumps(puntos, ensure_ascii=False)};window.addEventListener("load",function(){{if(!window.L)return;var m=L.map("mapa",{{scrollWheelZoom:false}}).setView([20.66,-103.39],11);
L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",{{attribution:"© OpenStreetMap"}}).addTo(m);var b=[];
PUNTOS.forEach(function(p){{var mk=L.circleMarker([p.lat,p.lon],{{radius:10,color:"#fff",weight:2,fillColor:"#6B4E9B",fillOpacity:1}}).addTo(m);mk.bindPopup("<b>"+p.n+"</b><br>"+p.t+" · "+p.p+"<br><a href='"+p.u+"'>Ver desarrollo</a>");b.push([p.lat,p.lon]);}});
if(b.length)m.fitBounds(b,{{padding:[40,40]}});}});</script>"""
    ld = {"@context": "https://schema.org", "@type": "RealEstateAgent", "name": "Acierta Max", "url": "https://gruposancarlos.pro", "telephone": "+52 33 3377 7337",
          "description": "Inmobiliaria autorizada para la comercialización de desarrollos de Grupo San Carlos en Guadalajara."}
    open("index.html", "w", encoding="utf-8").write(pagina("Desarrollos de Grupo San Carlos en Guadalajara · Acierta Max, inmobiliaria autorizada",
        f"{total} departamentos, casas y terrenos de Grupo San Carlos en la Zona Metropolitana de Guadalajara. Mapa, precios oficiales y asesoría sin costo con Acierta Max.", cuerpo, "", "", "inicio", jsld=ld))
    urls = [""] + [f"desarrollos/{d['slug']}.html" for k, d in DES.items() if R[k]["n"]]
    open("sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://gruposancarlos.pro/{u}</loc></url>" for u in urls) + "</urlset>\n")
    open("robots.txt", "w").write("User-agent: *\nAllow: /\nSitemap: https://gruposancarlos.pro/sitemap.xml\n")
    print(f"Sitio generado: portada + {len(urls)-1} desarrollos; {total} unidades")

if __name__ == "__main__":
    main()
