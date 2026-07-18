# -*- coding: utf-8 -*-
"""Traductor EN->ES de nombres de ejercicios del gym-dataset (uso personal).

Orden de resolucion:
  1) SPECIAL: match exacto del nombre completo (traducciones curadas).
  2) Composicional: <movimiento> [de <musculo>] [<mods>] [con/en <equipo>] (sufijo)
  3) Fallback token a token; lo desconocido se deja igual.
"""
import json, re

# ============ 1) TRADUCCIONES EXACTAS CURADAS ============
SPECIAL = {
    "3/4 sit-up": "Abdominal 3/4",
    "45° side bend": "Flexión lateral a 45°",
    "air bike": "Bicicleta en el aire",
    "all fours squad stretch": "Estiramiento de cuádriceps en cuatro apoyos",
    "alternate heel touchers": "Toques de talón alternos",
    "ankle circles": "Círculos de tobillo",
    "arm slingers hanging bent knee legs": "Balanceo de brazos colgado con rodillas flexionadas",
    "arm slingers hanging straight legs": "Balanceo de brazos colgado con piernas rectas",
    "assisted prone hamstring": "Femoral boca abajo asistido",
    "astride jumps": "Saltos a horcajadas",
    "back and forth step": "Paso adelante y atrás",
    "back lever": "Palanca dorsal (back lever)",
    "backward jump": "Salto hacia atrás",
    "balance board": "Tabla de equilibrio",
    "band assisted wheel rollerout": "Rueda abdominal asistida con banda",
    "band hip lift": "Elevación de cadera con banda",
    "band lying hip internal rotation": "Rotación interna de cadera tumbado con banda",
    "band seated hip internal rotation": "Rotación interna de cadera sentado con banda",
    "band y-raise": "Elevación en Y con banda",
    "barbell lying lifting": "Elevación tumbado con barra",
    "barbell pin presses": "Press desde pines con barra",
    "barbell reverse grip skullcrusher": "Rompecráneos con agarre invertido y barra",
    "barbell rollerout": "Rueda abdominal con barra",
    "barbell rollerout from bench": "Rueda abdominal con barra desde el banco",
    "barbell side bent v. 2": "Flexión lateral con barra v. 2",
    "barbell skier": "Esquiador con barra",
    "barbell standing ab rollerout": "Rueda abdominal de pie con barra",
    "battling ropes": "Cuerdas de batalla",
    "bear crawl": "Marcha del oso",
    "bench pull-ups": "Dominadas en banco",
    "biceps narrow pull-ups": "Dominadas cerradas para bíceps",
    "body-up": "Elevación de tronco",
    "bottoms-up": "Elevación de cadera invertida",
    "box jump down with one leg stabilization": "Salto al cajón con estabilización a una pierna",
    "butt-ups": "Elevaciones de glúteos",
    "butterfly yoga pose": "Postura de yoga de la mariposa",
    "cable cross-over variation": "Cruce en polea (variante)",
    "cable hip adduction": "Aducción de cadera en polea",
    "cable judo flip": "Giro de judo en polea",
    "cable one arm lateral bent-over": "Elevación lateral inclinado a un brazo en polea",
    "cable rear drive": "Empuje posterior en polea",
    "cable russian twists": "Giros rusos en polea",
    "cable seated shoulder internal rotation": "Rotación interna de hombro sentado en polea",
    "cable standing lift": "Elevación de pie en polea",
    "cable standing shoulder external rotation": "Rotación externa de hombro de pie en polea",
    "cable standing up straight crossovers": "Cruces de pie en polea",
    "cable upper chest crossovers": "Cruces de pecho superior en polea",
    "chin-ups": "Dominadas supinas",
    "cocoons": "Cocoons (rodillas al pecho)",
    "curl-up": "Encogimiento abdominal",
    "cycle cross trainer": "Elíptica",
    "dead bug": "Bicho muerto (dead bug)",
    "dumbbell finger curls": "Curl de dedos con mancuerna",
    "dumbbell hammer curls": "Curl martillo con mancuerna",
    "dumbbell incline breeding": "Apertura inclinado con mancuerna",
    "dumbbell incline t-raise": "Elevación en T inclinado con mancuerna",
    "dumbbell incline twisted flyes": "Aperturas con giro inclinado con mancuerna",
    "dumbbell incline y-raise": "Elevación en Y inclinado con mancuerna",
    "dumbbell iron cross": "Cruz de hierro con mancuerna",
    "dumbbell kickbacks on exercise ball": "Patada de tríceps con mancuerna sobre pelota",
    "dumbbell lying external shoulder rotation": "Rotación externa de hombro tumbado con mancuerna",
    "dumbbell lying femoral": "Femoral tumbado con mancuerna",
    "dumbbell lying one arm deltoid rear": "Deltoides posterior a un brazo tumbado con mancuerna",
    "dumbbell lying pronation": "Pronación tumbado con mancuerna",
    "dumbbell lying pronation on floor": "Pronación tumbado en el suelo con mancuerna",
    "dumbbell lying supination": "Supinación tumbado con mancuerna",
    "dumbbell lying supination on floor": "Supinación tumbado en el suelo con mancuerna",
    "dumbbell rear delt row_shoulder": "Remo de deltoides posterior con mancuerna",
    "dumbbell seated alternate shoulder": "Press de hombro alterno sentado con mancuerna",
    "dumbbell seated one arm rotate": "Rotación a un brazo sentado con mancuerna",
    "dumbbell single arm overhead carry": "Transporte por encima de la cabeza a un brazo con mancuerna",
    "dumbbell standing around world": "Círculos alrededor del cuerpo de pie con mancuerna",
    "dumbbell upright shoulder external rotation": "Rotación externa de hombro con mancuerna",
    "dumbbell w-press": "Press en W con mancuerna",
    "elbow-to-knee": "Codo a rodilla",
    "elevator": "Ascensor",
    "exercise ball alternating arm ups": "Elevación de brazos alterna sobre pelota",
    "exercise ball hug": "Abrazo a la pelota",
    "exercise ball one leg prone lower body rotation": "Rotación del tren inferior a una pierna boca abajo sobre pelota",
    "ez barbell seated curls": "Curl sentado con barra Z",
    "farmers walk": "Caminata del granjero",
    "finger curls": "Curl de dedos",
    "flag": "Bandera (human flag)",
    "flutter kicks": "Patadas de tijera",
    "forward jump": "Salto hacia adelante",
    "frog planche": "Plancha rana",
    "front lever": "Palanca frontal (front lever)",
    "front lever reps": "Repeticiones de palanca frontal",
    "full maltese": "Maltesa completa",
    "full planche": "Plancha completa",
    "gironda sternum chin": "Dominada al esternón de Gironda",
    "gorilla chin": "Dominada gorila",
    "half knee bends": "Media flexión de rodillas",
    "hands bike": "Bicicleta de brazos",
    "handstand": "Parada de manos",
    "hanging pike": "Elevación de piernas colgado en L",
    "hug keens to chest": "Rodillas al pecho",
    "inchworm": "Gusano (inchworm)",
    "inchworm v. 2": "Gusano (inchworm) v. 2",
    "isometric chest squeeze": "Contracción isométrica de pecho",
    "isometric wipers": "Limpiaparabrisas isométrico",
    "jack jump": "Salto de tijera",
    "jump rope": "Saltar la cuerda",
    "kettlebell advanced windmill": "Molino avanzado con kettlebell",
    "kettlebell double windmill": "Molino doble con kettlebell",
    "kettlebell figure 8": "Ocho con kettlebell",
    "kettlebell pirate supper legs": "Sentadilla pirata con kettlebell",
    "kettlebell turkish get up (squat style)": "Levantada turca con kettlebell (estilo sentadilla)",
    "kettlebell windmill": "Molino con kettlebell",
    "kick out sit": "Patada desde sentado",
    "kipping muscle up": "Muscle up con kipping",
    "l-pull-up": "Dominada en L",
    "l-sit on floor": "L-sit en el suelo",
    "landmine 180": "Landmine 180",
    "lean planche": "Plancha inclinada",
    "left hook. boxing": "Gancho de izquierda (boxeo)",
    "lever gripper hands": "Agarre de manos en máquina",
    "lever rotary calf": "Pantorrilla en máquina rotatoria",
    "lever seated hip abduction": "Abducción de cadera sentado en máquina",
    "lever seated hip adduction": "Aducción de cadera sentado en máquina",
    "lying elbow to knee": "Codo a rodilla tumbado",
    "march sit (wall)": "Marcha sentado contra la pared",
    "medicine ball catch and overhead throw": "Recepción y lanzamiento por encima de la cabeza con balón medicinal",
    "medicine ball chest pass": "Pase de pecho con balón medicinal",
    "medicine ball chest push from 3 point stance": "Empuje de pecho desde posición de 3 apoyos con balón medicinal",
    "medicine ball chest push multiple response": "Empuje de pecho de respuesta múltiple con balón medicinal",
    "medicine ball chest push single response": "Empuje de pecho de respuesta única con balón medicinal",
    "medicine ball chest push with run release": "Empuje de pecho con salida a la carrera y balón medicinal",
    "medicine ball overhead slam": "Lanzamiento al suelo por encima de la cabeza con balón medicinal",
    "medicine ball supine chest throw": "Lanzamiento de pecho boca arriba con balón medicinal",
    "monster walk": "Caminata del monstruo",
    "muscle up": "Muscle up",
    "muscle-up (on vertical bar)": "Muscle up (en barra vertical)",
    "oblique crunches floor": "Crunch oblicuo en el suelo",
    "one arm against wall": "Un brazo contra la pared",
    "one arm slam (with medicine ball)": "Lanzamiento a un brazo (con balón medicinal)",
    "otis up": "Otis up (abdominal con peso)",
    "pelvic tilt": "Inclinación pélvica",
    "posterior step to overhead reach": "Paso atrás con alcance por encima de la cabeza",
    "pull-in (on stability ball)": "Encogimiento de piernas sobre pelota",
    "push to run": "Empuje a la carrera",
    "quads": "Cuádriceps",
    "quick feet v. 2": "Pies rápidos v. 2",
    "reclining big toe pose with rope": "Postura del dedo gordo reclinado con cuerda",
    "resistance band hip thrusts on knees": "Empuje de cadera de rodillas con banda elástica",
    "resistance band seated hip abduction": "Abducción de cadera sentado con banda elástica",
    "reverse hyper on flat bench": "Hiperextensión inversa en banco plano",
    "roller body saw": "Sierra corporal con rueda",
    "roller seated shoulder flexor depresor retractor": "Flexor-depresor-retractor de hombro sentado con rueda",
    "roller seated single leg shoulder flexor depresor retractor": "Flexor-depresor-retractor de hombro a una pierna sentado con rueda",
    "rope climb": "Trepa de cuerda",
    "run": "Correr",
    "run (equipment)": "Correr (máquina)",
    "scissor jumps": "Saltos de tijera",
    "seated wide angle pose sequence": "Secuencia de postura de ángulo abierto sentado",
    "short stride run": "Carrera de zancada corta",
    "shoulder tap": "Toque de hombro",
    "side hip (on parallel bars)": "Cadera lateral (en paralelas)",
    "side hip abduction": "Abducción de cadera lateral",
    "side lying hip adduction": "Aducción de cadera tumbado de lado",
    "side-to-side chin": "Dominada de lado a lado",
    "single leg platform slide": "Deslizamiento en plataforma a una pierna",
    "skater hops": "Saltos de patinador",
    "ski ergometer": "Ergómetro de esquí",
    "ski step": "Paso de esquí",
    "skin the cat": "Skin the cat",
    "sledge hammer": "Mazo",
    "smith incline shoulder raises": "Elevaciones de hombro inclinado en máquina Smith",
    "smith reverse calf raises": "Elevación de talones invertida en máquina Smith",
    "spell caster": "Spell caster (giro con mancuerna)",
    "sphinx": "Esfinge",
    "split squats": "Sentadillas búlgaras",
    "standing archer": "Arquero de pie",
    "standing calves": "Pantorrillas de pie",
    "standing pelvic tilt": "Inclinación pélvica de pie",
    "standing wheel rollerout": "Rueda abdominal de pie",
    "star jump": "Salto de estrella",
    "stationary bike run v. 3": "Bicicleta fija (carrera) v. 3",
    "stationary bike walk": "Bicicleta fija (caminata)",
    "straddle maltese": "Maltesa con piernas abiertas",
    "straddle planche": "Plancha con piernas abiertas",
    "straight leg outer hip abductor": "Abducción de cadera con pierna recta",
    "suspended abdominal fallout": "Rueda abdominal en suspensión",
    "swimmer kicks v. 2": "Patadas de nadador v. 2",
    "tire flip": "Volteo de neumático",
    "upward facing dog": "Perro boca arriba",
    "v-sit on floor": "V-sit en el suelo",
    "walk elliptical cross trainer": "Caminata en elíptica",
    "walking on incline treadmill": "Caminata en cinta inclinada",
    "walking on stepmill": "Caminata en escaladora",
    "weighted cossack squats": "Sentadillas cosacas con peso",
    "weighted muscle up": "Muscle up con peso",
    "weighted muscle up (on bar)": "Muscle up con peso (en barra)",
    "weighted round arm": "Círculo de brazo con peso",
    "weighted standing hand squeeze": "Agarre de mano de pie con peso",
    "wheel rollerout": "Rueda abdominal",
    "wheel run": "Carrera con rueda",
    "wind sprints": "Sprints",
    "wrist circles": "Círculos de muñeca",
    "wrist rollerer": "Enrollador de muñeca",
    "quads ": "Cuádriceps",
    "cocoons ": "Cocoons",
}

# ============ 2) VOCABULARIO COMPOSICIONAL (con acentos) ============
EQUIPMENT = {
    "dumbbells": ("con", "mancuernas"), "dumbbell": ("con", "mancuerna"),
    "olympic barbell": ("con", "barra olímpica"), "ez barbell": ("con", "barra Z"),
    "ez-bar": ("con", "barra Z"), "trap bar": ("con", "barra hexagonal"),
    "barbell": ("con", "barra"),
    "resistance band": ("con", "banda elástica"), "cable": ("en", "polea"),
    "band": ("con", "banda"), "kettlebell": ("con", "kettlebell"),
    "medicine ball": ("con", "balón medicinal"),
    "stability ball": ("sobre", "pelota"), "exercise ball": ("sobre", "pelota"),
    "bosu ball": ("sobre", "Bosu"), "bosu": ("sobre", "Bosu"),
    "smith machine": ("en", "máquina Smith"), "smith": ("en", "máquina Smith"),
    "leverage machine": ("en", "máquina"), "leverage": ("en", "máquina"),
    "lever": ("en", "máquina"), "machine": ("en", "máquina"),
    "sled": ("en", "trineo"), "hammer": ("con", "mazo"), "rope": ("con", "cuerda"),
    "wheel": ("con", "rueda abdominal"), "roller": ("con", "rueda"),
    "suspension": ("en", "suspensión"),
}

MOVEMENT = {
    "reverse hyperextension": "hiperextensión inversa",
    "hyperextension": "hiperextensión",
    "bench press": "press de banca", "overhead press": "press militar",
    "shoulder press": "press de hombros", "chest press": "press de pecho",
    "floor press": "press en el suelo", "leg press": "prensa de piernas",
    "push press": "push press", "military press": "press militar",
    "preacher curl": "curl predicador", "hammer curl": "curl martillo",
    "concentration curl": "curl concentrado", "wrist curl": "curl de muñeca",
    "spider curl": "curl araña", "drag curl": "curl de arrastre",
    "leg curl": "curl femoral", "bicep curl": "curl de bíceps",
    "biceps curl": "curl de bíceps",
    "front squat": "sentadilla frontal", "hack squat": "sentadilla hack",
    "split squat": "sentadilla búlgara", "jump squat": "sentadilla con salto",
    "goblet squat": "sentadilla goblet", "sumo squat": "sentadilla sumo",
    "romanian deadlift": "peso muerto rumano",
    "stiff leg deadlift": "peso muerto con piernas rígidas",
    "sumo deadlift": "peso muerto sumo", "deadlift": "peso muerto",
    "upright row": "remo al mentón", "bent over row": "remo inclinado",
    "inverted row": "remo invertido", "seal row": "remo foca", "row": "remo",
    "lateral raise": "elevación lateral", "front raise": "elevación frontal",
    "calf raise": "elevación de talones", "leg raise": "elevación de piernas",
    "knee raise": "elevación de rodillas", "shoulder raise": "elevación de hombros",
    "raise": "elevación",
    "leg extension": "extensión de piernas", "triceps extension": "extensión de tríceps",
    "tricep extension": "extensión de tríceps", "back extension": "extensión de espalda",
    "extension": "extensión",
    "reverse fly": "apertura invertida", "rear delt fly": "apertura posterior",
    "fly": "apertura", "flyes": "aperturas", "flye": "apertura",
    "lat pulldown": "jalón al pecho", "pulldown": "jalón", "pull down": "jalón",
    "chin-up": "dominada supina", "chin up": "dominada supina",
    "pull-up": "dominada", "pull up": "dominada", "pullup": "dominada",
    "push-up": "flexión", "push up": "flexión", "pushup": "flexión",
    "push down": "extensión en polea", "pushdown": "extensión en polea",
    "chest dip": "fondo de pecho", "triceps dip": "fondo de tríceps",
    "dips": "fondos", "dip": "fondo",
    "reverse crunch": "crunch invertido", "bicycle crunch": "crunch bicicleta",
    "crunch": "crunch", "crunches": "crunch",
    "sit-up": "abdominal", "sit up": "abdominal", "situp": "abdominal",
    "lunge": "zancada", "lunges": "zancadas",
    "shoulder shrug": "encogimiento de hombros", "shrug": "encogimiento",
    "russian twist": "giro ruso", "twist": "giro",
    "stretch": "estiramiento",
    "kickback": "patada de tríceps", "kickbacks": "patadas de tríceps",
    "pullover": "pullover", "thruster": "thruster", "clean": "cargada",
    "snatch": "arrancada", "jerk": "envión", "bridge": "puente", "plank": "plancha",
    "good morning": "buenos días", "hip thrust": "empuje de cadera",
    "step-up": "subida al cajón", "step up": "subida al cajón",
    "toe touch": "toque de puntas", "mountain climber": "escalador",
    "wood chop": "leñador", "woodchop": "leñador", "chop": "leñador",
    "side bend": "flexión lateral", "v-up": "v-up", "v up": "v-up",
    "face pull": "face pull", "high pull": "tirón alto",
    "press": "press", "curl": "curl", "squat": "sentadilla",
    "pull": "jalón", "swing": "swing", "carry": "transporte",
    "rotation": "rotación", "abduction": "abducción", "adduction": "aducción",
    "windmill": "molino", "burpee": "burpee", "jumping jack": "salto de tijera",
    "high knee": "rodillas al pecho", "flutter kick": "patada de tijera",
    "scissor kick": "patada de tijera", "get up": "levantada", "sit": "sentadilla iso",
}

MUSCLE = {
    "biceps": "bíceps", "bicep": "bíceps", "triceps": "tríceps", "tricep": "tríceps",
    "pectorals": "pectorales", "pectoral": "pectoral", "chest": "pecho",
    "shoulders": "hombros", "shoulder": "hombro",
    "legs": "piernas", "leg": "pierna",
    "calves": "pantorrillas", "calf": "pantorrilla",
    "glutes": "glúteos", "gluteus": "glúteo", "glute": "glúteo",
    "hamstrings": "femorales", "hamstring": "femoral", "femoral": "femoral",
    "quadriceps": "cuádriceps", "quads": "cuádriceps", "quad": "cuádriceps",
    "abdominals": "abdominales", "abdominal": "abdominal", "abs": "abdominales", "ab": "abdominal",
    "lower back": "espalda baja", "upper back": "espalda alta", "back": "espalda",
    "forearms": "antebrazos", "forearm": "antebrazo",
    "wrists": "muñecas", "wrist": "muñeca",
    "lats": "dorsales", "lat": "dorsal",
    "traps": "trapecios", "trap": "trapecio", "neck": "cuello",
    "hips": "cadera", "hip": "cadera", "thighs": "muslos", "thigh": "muslo",
    "obliques": "oblicuos", "oblique": "oblicuo", "core": "core",
    "delts": "deltoides", "delt": "deltoides", "deltoid": "deltoides",
    "rear delt": "deltoides posterior",
}

MODIFIER = {
    "incline": "inclinado", "inclined": "inclinado", "decline": "declinado",
    "declined": "declinado", "seated": "sentado", "standing": "de pie",
    "lying": "tumbado", "prone": "boca abajo", "supine": "boca arriba",
    "kneeling": "arrodillado", "reverse": "inverso", "reversed": "inverso",
    "alternating": "alterno", "alternate": "alterno", "alternated": "alterno",
    "overhead": "por encima de la cabeza", "bent-over": "inclinado", "bent over": "inclinado",
    "bent": "flexionado", "straight": "recto", "side": "lateral", "front": "frontal",
    "rear": "posterior", "hanging": "colgado", "single arm": "a un brazo",
    "one arm": "a un brazo", "single leg": "a una pierna", "one leg": "a una pierna",
    "single": "a un lado", "twisting": "con giro", "explosive": "explosivo",
    "isometric": "isométrico", "weighted": "con peso", "assisted": "asistido",
    "high": "alto", "low": "bajo", "flat": "plano", "walking": "caminando",
    "jumping": "con salto", "crossover": "cruzado", "wide grip": "agarre abierto",
    "close grip": "agarre cerrado", "neutral grip": "agarre neutro",
    "reverse grip": "agarre invertido", "wide": "abierto", "narrow": "cerrado",
    "close": "cerrado", "internal": "interna", "external": "externa",
    "seated": "sentado", "on floor": "en el suelo", "on bench": "en banco",
}


def _sorted(d):
    return sorted(d.items(), key=lambda kv: -len(kv[0]))


_SUFFIX = {"male": "hombre", "female": "mujer", "kneeling": "arrodillado",
           "on bench": "en banco", "on knees": "de rodillas", "on floor": "en el suelo",
           "on stability ball": "sobre pelota", "on hip": "sobre la cadera",
           "on knee": "sobre la rodilla", "on vertical bar": "en barra vertical",
           "with barbell": "con barra", "with medicine ball": "con balón medicinal",
           "with rope": "con cuerda", "narrow parallel grip": "agarre paralelo cerrado",
           "wall": "pared", "female)": "mujer", "squat style": "estilo sentadilla",
           "on parallel bars": "en paralelas", "equipment": "máquina"}


def _cap(s):
    s = s.strip()
    return (s[0].upper() + s[1:]) if s else s


def _strip_suffix(orig):
    m = re.search(r"\s*\(([^)]*)\)\s*$", orig)
    if not m:
        return orig, ""
    inner = m.group(1).strip().lower()
    return orig[:m.start()], " (%s)" % _SUFFIX.get(inner, inner)


def translate(name):
    orig = name.strip()
    low = orig.lower()

    # 1) match exacto
    if low in SPECIAL:
        return SPECIAL[low], orig
    core_raw, suffix = _strip_suffix(orig)
    if core_raw.strip().lower() in SPECIAL:
        return SPECIAL[core_raw.strip().lower()] + suffix, orig

    # 2) composicional
    s = " " + core_raw.lower().strip() + " "
    mov = mus = eq = None
    mods = []
    for en, es in _sorted(MOVEMENT):
        if (" " + en + " ") in s:
            mov = es; s = s.replace(" " + en + " ", " ", 1); break
    for en, (prep, es) in _sorted(EQUIPMENT):
        if (" " + en + " ") in s:
            eq = (prep, es); s = s.replace(" " + en + " ", " ", 1); break
    for en, es in _sorted(MUSCLE):
        if (" " + en + " ") in s:
            mus = es; s = s.replace(" " + en + " ", " ", 1); break
    for en, es in _sorted(MODIFIER):
        if (" " + en + " ") in s:
            if es not in mods:
                mods.append(es)
            s = s.replace(" " + en + " ", " ", 1)

    if mov:
        out = [mov]
        if mus:
            out.append("de " + mus)
        out += mods
        if eq:
            prep, es = eq
            out.append((prep + " " if prep else "") + es)
        return _cap(" ".join(out)) + suffix, orig

    # 3) sin match -> None (marcar)
    return None, orig


if __name__ == "__main__":
    import sys, random
    d = json.load(open(sys.argv[1]))
    names = sorted({e["name"] for e in d})
    miss = [n for n in names if translate(n)[0] is None]
    random.seed(3)
    print("===== MUESTRA (40) =====")
    for n in random.sample(names, 40):
        print(f"  {n:48s} -> {translate(n)[0]}")
    print(f"\ncobertura: {len(names)-len(miss)}/{len(names)} ({100*(len(names)-len(miss))/len(names):.1f}%)")
    if miss:
        print("SIN TRADUCIR:", len(miss))
        for n in miss:
            print("  ", n)
