# -*- coding: utf-8 -*-
"""
Cargador DEMO de ejercicios con animaciones de Gym Visual (dataset hasaneyldrm).

USO EXCLUSIVO DE DEMOSTRACION / LOCAL. Las animaciones son (c) Gym Visual
(https://gymvisual.com/) y NO pueden redistribuirse ni venderse. Este script es
solo para mostrar el modulo en una notebook propia.

-------------------------------------------------------------------------------
COMO CORRERLO
-------------------------------------------------------------------------------
1) Clonar el dataset (una vez) en la notebook:
       git clone --depth 1 https://github.com/pronexo-argentina/gym-dataset.git

2) Editar abajo DATASET_DIR con la ruta a esa carpeta.

3) Ejecutar dentro del shell de Odoo (con el server DETENIDO o no, da igual):
       /odoo-bin shell -c /ruta/odoo.conf -d TU_BASE --no-http < load_gymvisual_demo.py

       sudo -u odoo -s /opt/odoo19/venv/bin/python /opt/odoo19/odoo/odoo-bin shell -c /opt/odoo19/config/odoo19.conf -d odoo.goodwinds.net --no-http < load_gymvisual_demo.py

   (en el shell de Odoo la variable `env` ya existe; el script la usa)

4) Recargar la vista Ejercicios en el navegador (Cmd+R).
-------------------------------------------------------------------------------
"""
import base64
import glob
import json
import os
import re

# ======================= CONFIG — EDITAR ESTO =========================
DATASET_DIR = os.path.expanduser("/home/pronexo/gym-dataset")  # carpeta clonada
LIMIT = None          # None = todos (~1324). Pone p.ej. 200 para una demo rapida.
WIPE_EXISTING = True  # True = borra los ejercicios de biblioteca (sin empresa) antes de cargar
USE_VIDEOS = True     # True = GIF animado. False = imagen fija (jpg 180x180).
COMPANY_ID = False    # False = compartido (se ve en todas las empresas)
# ======================================================================

# body_part del dataset  ->  muscle_group del modelo
BODY_TO_MUSCLE = {
    "back": "back",
    "cardio": "cardio",
    "chest": "chest",
    "lower arms": "arms",
    "upper arms": "arms",
    "lower legs": "legs",
    "upper legs": "legs",
    "shoulders": "shoulders",
    "neck": "full_body",
    "waist": "core",
}


def _slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", (s or "")).strip("_")


def main(env):
    if not os.path.isdir(DATASET_DIR):
        raise SystemExit(
            "No existe DATASET_DIR=%r.\nCloná primero:\n"
            "  git clone --depth 1 https://github.com/pronexo-argentina/gym-dataset.git"
            % DATASET_DIR
        )

    json_path = os.path.join(DATASET_DIR, "data", "exercises.json")
    media_dir = os.path.join(DATASET_DIR, "videos" if USE_VIDEOS else "images")
    ext = "gif" if USE_VIDEOS else "jpg"
    mimetype = "image/gif" if USE_VIDEOS else "image/jpeg"

    with open(json_path, encoding="utf-8") as fh:
        entries = json.load(fh)

    # id ("0001")  ->  ruta del archivo ("videos/0001-XXXX.gif")
    media = {}
    for p in glob.glob(os.path.join(media_dir, "*." + ext)):
        media[os.path.basename(p).split("-", 1)[0]] = p

    Exercise = env["pronexo.gym.exercise"].with_context(active_test=False)
    Att = env["ir.attachment"].sudo()

    if WIPE_EXISTING:
        old = Exercise.search([("company_id", "=", COMPANY_ID)])
        # borrar tambien los adjuntos que hubieramos creado antes
        Att.search([
            ("res_model", "=", "pronexo.gym.exercise"),
            ("res_id", "in", old.ids),
        ]).unlink()
        print("Borrando %s ejercicios previos..." % len(old))
        old.unlink()

    created = skipped = 0
    for e in entries:
        if LIMIT and created >= LIMIT:
            break
        path = media.get(e["id"])
        if not path:
            skipped += 1
            continue

        with open(path, "rb") as fh:
            data = fh.read()

        ex = Exercise.create({
            "name": e["name"].title(),
            "company_id": COMPANY_ID,
            "muscle_group": BODY_TO_MUSCLE.get(e.get("body_part"), "full_body"),
            "level": "intermediate",
            "equipment_name": (e.get("equipment") or "").title(),
            "instructions": (e.get("instructions") or {}).get("en", "")
                            if isinstance(e.get("instructions"), dict)
                            else (e.get("instructions") or ""),
        })
        att = Att.create({
            "name": "%s.%s" % (_slug(e["name"]), ext),
            "type": "binary",
            "datas": base64.b64encode(data),
            "mimetype": mimetype,
            "public": True,
            "res_model": "pronexo.gym.exercise",
            "res_id": ex.id,
        })
        # cache-buster para que el navegador no muestre una version vieja
        ex.image_url = "/web/content/%d?v=%d" % (att.id, att.id)
        created += 1
        if created % 100 == 0:
            print("  ...%s cargados" % created)

    env.cr.commit()
    print("LISTO: %s ejercicios cargados (%s sin animacion, omitidos)." % (created, skipped))
    print("Recargá la vista Ejercicios en el navegador (Cmd+R).")


# En el shell de Odoo `env` ya existe; si se ejecuta de otra forma, avisamos.
try:
    env  # noqa: F821
except NameError:
    raise SystemExit("Correlo dentro de: ./odoo-bin shell -d TU_BASE < load_gymvisual_demo.py")
else:
    main(env)  # noqa: F821
