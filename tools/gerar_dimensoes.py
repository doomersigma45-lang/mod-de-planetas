#!/usr/bin/env python3
"""Gera os JSON de dimensão (Forge 1.20.1, pack_format 15) do mod Sistema Solar.

Uso:  python3 tools/gerar_dimensoes.py [id_do_corpo ...]
Sem argumentos, gera todos os corpos definidos em CORPOS.

Para acrescentar um corpo (ChatGPT ou Claude), basta adicionar uma entrada em CORPOS.
Cada corpo gera 4 arquivos em src/main/resources/data/sistemasolar/:
  dimension_type/<id>.json, dimension/<id>.json,
  worldgen/biome/<id>_<bioma>.json, worldgen/noise_settings/<id>.json
"""
import json
import sys
from pathlib import Path

MODID = "sistemasolar"
RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "src" / "main" / "resources" / "data" / MODID


def rgb(hexa):
    return int(hexa.lstrip("#"), 16)


# Campos de cada corpo:
#   bioma        sufixo do bioma (<id>_<bioma>)
#   default      bloco base do terreno
#   topo / sub   bloco da superfície e da camada logo abaixo
#   fluido       "water" ou "lava"; nivel_mar = altura do fluido (-64 = sem fluido)
#   base_y       altura média do terreno; amp = quanto o relevo varia (0..1);
#   xz           escala horizontal do ruído (menor = relevo mais largo)
#   tempo_fixo   None = ciclo normal; número = hora fixa do dia (18000 = meia-noite)
#   luz_ambiente luz mínima da dimensão (0.0 a 1.0)
#   quente       True = ultrawarm (água evapora)
#   cores        céu, neblina, água, névoa da água
#   temp         temperatura do bioma
CORPOS = {
    "marte": dict(
        bioma="deserto", default="minecraft:red_sandstone",
        topo="sistemasolar:rocha_marciana", sub="sistemasolar:rocha_marciana",
        fluido="water", nivel_mar=-64, base_y=70, amp=0.45, xz=0.6,
        tempo_fixo=None, luz_ambiente=0.0, quente=False,
        cores=("#C98B5E", "#D9A07A", "#7A5C4A", "#4A3A30"), temp=0.8),
    "venus": dict(
        bioma="vulcanico", default="minecraft:basalt",
        topo="sistemasolar:basalto_venusiano", sub="sistemasolar:basalto_venusiano",
        fluido="lava", nivel_mar=40, base_y=64, amp=0.5, xz=0.5,
        tempo_fixo=6000, luz_ambiente=0.1, quente=True,
        cores=("#D8B24A", "#E3C770", "#7A5A2A", "#4A3515"), temp=2.0),
    "miller": dict(
        bioma="oceano", default="minecraft:stone",
        topo="sistemasolar:arenito_miller", sub="sistemasolar:arenito_miller",
        fluido="water", nivel_mar=64, base_y=58, amp=0.08, xz=0.4,
        tempo_fixo=None, luz_ambiente=0.0, quente=False,
        cores=("#7FA8C9", "#A9C4D9", "#2E6F8E", "#154256"), temp=0.5),
    "netuno": dict(
        bioma="gelo", default="minecraft:packed_ice",
        topo="sistemasolar:gelo_neptuniano", sub="sistemasolar:gelo_neptuniano",
        fluido="water", nivel_mar=-64, base_y=90, amp=0.6, xz=0.8,
        tempo_fixo=None, luz_ambiente=0.05, quente=False,
        cores=("#3F6FD8", "#6C93E6", "#2A56B8", "#12295C"), temp=-0.5),
    "plutao": dict(
        bioma="planicie", default="minecraft:calcite",
        topo="sistemasolar:gelo_plutoniano", sub="sistemasolar:gelo_plutoniano",
        fluido="water", nivel_mar=48, base_y=68, amp=0.12, xz=0.3,
        tempo_fixo=18000, luz_ambiente=0.05, quente=False,
        cores=("#05060A", "#10131C", "#3A4A6A", "#1B2538"), temp=-1.0),
    "ceres": dict(
        bioma="rochoso", default="minecraft:deepslate",
        topo="sistemasolar:rocha_ceresiana", sub="sistemasolar:rocha_ceresiana",
        fluido="water", nivel_mar=-64, base_y=70, amp=0.35, xz=0.7,
        tempo_fixo=18000, luz_ambiente=0.05, quente=False,
        cores=("#050505", "#101010", "#3A3F4A", "#1F2229"), temp=-0.2),
    "lua": dict(
        bioma="cratera", default="minecraft:stone",
        topo="sistemasolar:regolito_lunar", sub="sistemasolar:regolito_lunar",
        fluido="water", nivel_mar=-64, base_y=68, amp=0.3, xz=0.5,
        tempo_fixo=18000, luz_ambiente=0.1, quente=False,
        cores=("#000000", "#0A0A0A", "#3A4A5A", "#202A33"), temp=-0.3),
    "saturn": dict(
        bioma="bandas", default="minecraft:red_sandstone",
        topo="sistemasolar:rocha_saturiana", sub="sistemasolar:rocha_saturiana",
        fluido="water", nivel_mar=-64, base_y=74, amp=0.28, xz=0.8,
        tempo_fixo=None, luz_ambiente=0.02, quente=False,
        cores=("#D3A05B", "#B47D48", "#8B7355", "#5C4936"), temp=0.4),
    "jupiter": dict(
        bioma="tempestade", default="minecraft:granite",
        topo="sistemasolar:rocha_jupiteriana", sub="sistemasolar:rocha_jupiteriana",
        fluido="water", nivel_mar=-64, base_y=68, amp=0.7, xz=0.9,
        tempo_fixo=None, luz_ambiente=0.08, quente=False,
        cores=("#C98F58", "#D9A879", "#8B745F", "#594A3D"), temp=0.8),
    "urano": dict(
        bioma="gelo_azul", default="minecraft:packed_ice",
        topo="sistemasolar:gelo_uraniano", sub="sistemasolar:gelo_uraniano",
        fluido="water", nivel_mar=-64, base_y=84, amp=0.48, xz=0.75,
        tempo_fixo=None, luz_ambiente=0.02, quente=False,
        cores=("#5A9CC8", "#78B6D8", "#3B7197", "#24465F"), temp=-0.7),
    "haumea": dict(
        bioma="gelo", default="minecraft:packed_ice",
        topo="sistemasolar:gelo_haumeano", sub="sistemasolar:gelo_haumeano",
        fluido="water", nivel_mar=-64, base_y=82, amp=0.3, xz=0.5,
        tempo_fixo=None, luz_ambiente=0.03, quente=False,
        cores=("#9FC7E8", "#C4DDF2", "#6D9CBF", "#456C8C"), temp=-0.5),
    "sedna": dict(
        bioma="gelado", default="minecraft:packed_ice",
        topo="sistemasolar:gelo_vermelho_sedna", sub="sistemasolar:gelo_vermelho_sedna",
        fluido="water", nivel_mar=-64, base_y=76, amp=0.4, xz=0.65,
        tempo_fixo=18000, luz_ambiente=0.01, quente=False,
        cores=("#6E4652", "#8B5A60", "#45586C", "#283544"), temp=-1.0),
    "titan": dict(
        bioma="metano", default="minecraft:stone",
        topo="sistemasolar:rocha_titana", sub="sistemasolar:rocha_titana",
        fluido="water", nivel_mar=48, base_y=58, amp=0.15, xz=0.5,
        tempo_fixo=18000, luz_ambiente=0.04, quente=False,
        cores=("#B8783E", "#D19759", "#72543C", "#44352B"), temp=-0.3),
    "europa": dict(
        bioma="oceano", default="minecraft:packed_ice",
        topo="sistemasolar:gelo_europeano", sub="sistemasolar:gelo_europeano",
        fluido="water", nivel_mar=48, base_y=60, amp=0.16, xz=0.45,
        tempo_fixo=18000, luz_ambiente=0.03, quente=False,
        cores=("#83B6D5", "#A8CCDF", "#386E9A", "#1C3D60"), temp=-0.4),
    "io": dict(
        bioma="vulcanico", default="minecraft:basalt",
        topo="sistemasolar:rocha_vulcanica_io", sub="sistemasolar:rocha_vulcanica_io",
        fluido="lava", nivel_mar=42, base_y=64, amp=0.55, xz=0.7,
        tempo_fixo=6000, luz_ambiente=0.12, quente=True,
        cores=("#D97932", "#C56B32", "#7C3822", "#4D2118"), temp=1.5),
}

CATEGORIAS_MOB = ["monster", "creature", "ambient", "axolotls",
                  "underground_water_creature", "water_creature",
                  "water_ambient", "misc"]


def estado(nome, **props):
    d = {"Name": nome}
    if props:
        d["Properties"] = {k: str(v) for k, v in props.items()}
    return d


def dimension_type(c):
    d = {
        "ultrawarm": c["quente"],
        "natural": True,
        "coordinate_scale": 1.0,
        "has_skylight": True,
        "has_ceiling": False,
        "ambient_light": c["luz_ambiente"],
        "monster_spawn_light_level": 0,
        "monster_spawn_block_light_limit": 0,
        "piglin_safe": c["quente"],
        "bed_works": False,
        "respawn_anchor_works": True,
        "has_raids": False,
        "logical_height": 384,
        "min_y": -64,
        "height": 384,
        "infiniburn": "#minecraft:infiniburn_overworld",
        "effects": "minecraft:overworld",
    }
    if c["tempo_fixo"] is not None:
        d["fixed_time"] = c["tempo_fixo"]
    return d


def dimension(id_, c):
    return {
        "type": f"{MODID}:{id_}",
        "generator": {
            "type": "minecraft:noise",
            "settings": f"{MODID}:{id_}",
            "biome_source": {
                "type": "minecraft:fixed",
                "biome": f"{MODID}:{id_}_{c['bioma']}",
            },
        },
    }


def bioma(c):
    ceu, neblina, agua, nevoa = (rgb(x) for x in c["cores"])
    return {
        "has_precipitation": False,
        "temperature": c["temp"],
        "downfall": 0.0,
        "effects": {
            "sky_color": ceu,
            "fog_color": neblina,
            "water_color": agua,
            "water_fog_color": nevoa,
        },
        "spawners": {cat: [] for cat in CATEGORIAS_MOB},
        "spawn_costs": {},
        "carvers": {},
        "features": [[] for _ in range(11)],
    }


def ruido(nome, xz, y):
    return {"type": "minecraft:noise", "noise": nome, "xz_scale": xz, "y_scale": y}


def noise_settings(c):
    base, amp = c["base_y"], c["amp"]
    gradiente = {
        "type": "minecraft:y_clamped_gradient",
        "from_y": base - 24, "to_y": base + 24,
        "from_value": 1.0, "to_value": -1.0,
    }
    relevo = {
        "type": "minecraft:mul",
        "argument1": amp,
        "argument2": ruido("minecraft:erosion", c["xz"], 0.25),
    }
    densidade = {
        "type": "minecraft:interpolated",
        "argument": {"type": "minecraft:add", "argument1": gradiente, "argument2": relevo},
    }
    piso_bedrock = {
        "type": "minecraft:condition",
        "if_true": {
            "type": "minecraft:vertical_gradient",
            "random_name": "minecraft:bedrock_floor",
            "true_at_and_below": {"above_bottom": 0},
            "false_at_and_above": {"above_bottom": 5},
        },
        "then_run": {"type": "minecraft:block", "result_state": estado("minecraft:bedrock")},
    }

    def camada(add_surface_depth, bloco):
        return {
            "type": "minecraft:condition",
            "if_true": {
                "type": "minecraft:stone_depth",
                "offset": 0,
                "surface_type": "floor",
                "add_surface_depth": add_surface_depth,
                "secondary_depth_range": 0,
            },
            "then_run": {"type": "minecraft:block", "result_state": estado(bloco)},
        }

    return {
        "sea_level": c["nivel_mar"],
        "disable_mob_generation": False,
        "aquifers_enabled": False,
        "ore_veins_enabled": False,
        "legacy_random_source": False,
        "default_block": estado(c["default"]),
        "default_fluid": estado(f"minecraft:{c['fluido']}", level=0),
        "noise": {"min_y": -64, "height": 384, "size_horizontal": 1, "size_vertical": 2},
        "noise_router": {
            "barrier": 0, "fluid_level_floodedness": 0, "fluid_level_spread": 0,
            "lava": 0, "temperature": 0, "vegetation": 0, "continents": 0,
            "erosion": 0, "depth": 0, "ridges": 0,
            "initial_density_without_jaggedness": 0,
            "final_density": densidade,
            "vein_toggle": 0, "vein_ridged": 0, "vein_gap": 0,
        },
        "spawn_target": [],
        "surface_rule": {
            "type": "minecraft:sequence",
            "sequence": [piso_bedrock, camada(False, c["topo"]), camada(True, c["sub"])],
        },
    }


def gravar(caminho, conteudo):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(conteudo, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def gerar(id_):
    c = CORPOS[id_]
    gravar(DADOS / "dimension_type" / f"{id_}.json", dimension_type(c))
    gravar(DADOS / "dimension" / f"{id_}.json", dimension(id_, c))
    gravar(DADOS / "worldgen" / "biome" / f"{id_}_{c['bioma']}.json", bioma(c))
    gravar(DADOS / "worldgen" / "noise_settings" / f"{id_}.json", noise_settings(c))
    print(f"gerado: {id_}")


if __name__ == "__main__":
    alvos = sys.argv[1:] or list(CORPOS)
    for alvo in alvos:
        if alvo not in CORPOS:
            sys.exit(f"corpo desconhecido: {alvo} (opções: {', '.join(CORPOS)})")
        gerar(alvo)

