#!/usr/bin/env python3
"""Gerador dos dados (JSON) dos 14 corpos do mod Sistema Solar — Forge 1.20.1 (pack_format 15).

Uso:   python3 tools/gerar_dimensoes.py

Lê os corpos de tools/corpos.py e (re)gera, em src/main/resources/data/sistemasolar/:
  dimension_type/  dimension/  corpos/ (dados físicos para o código Java futuro)
  worldgen/biome  worldgen/noise_settings  worldgen/configured_feature
  worldgen/placed_feature  worldgen/configured_carver
e a documentação em docs/CORPOS.md.
Tudo que o script gerou antes é apagado e refeito: edite o corpos.py, não os JSON.
"""
import json
import shutil
import sys
from functools import reduce
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ruido  # noqa: E402
from corpos import CORPOS  # noqa: E402

MODID = "sistemasolar"
RAIZ = Path(__file__).resolve().parent.parent
DADOS = RAIZ / "src" / "main" / "resources" / "data" / MODID
DOCS = RAIZ / "docs"
PASTAS_GERADAS = ["dimension", "dimension_type", "worldgen", "corpos"]

CONT = "minecraft:continentalness"
TEMP = "minecraft:temperature"
VEG = "minecraft:vegetation"
EROS = "minecraft:erosion"
CHEESE = "minecraft:cave_cheese"

CATEGORIAS_MOB = ["monster", "creature", "ambient", "axolotls",
                  "underground_water_creature", "water_creature", "water_ambient", "misc"]
PASSO_MINERIOS = 6  # GenerationStep.Decoration.UNDERGROUND_ORES


# ------------------------------------------------------------------ utilidades

def rgb(h):
    return int(h.lstrip("#"), 16)


def estado(nome, **props):
    d = {"Name": nome}
    if props:
        d["Properties"] = {k: str(v) for k, v in props.items()}
    return d


def estado_fluido(nome):
    return estado(nome, level=0)


def gravar(caminho, conteudo):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(conteudo, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def unicos(seq):
    visto, saida = set(), []
    for x in seq:
        if x not in visto:
            visto.add(x)
            saida.append(x)
    return saida


def id_bioma(cid, b):
    return f"{MODID}:{cid}_{b['nome']}"


def id_feat(cid, nome):
    return f"{MODID}:{cid}_{nome}"


def blocos_do_corpo(c):
    t = c["terreno"]
    blocos = [t["default"]]
    for b in c["biomas"]:
        blocos += [b["topo"], b["sub"]]
        blocos += [bl for _, bl in b.get("faixas", [])]
        blocos += [l["bloco"] for l in b.get("listras", [])]
    if t.get("fundo"):
        blocos.append(t["fundo"])
    if t.get("piso"):
        blocos += [t["piso"]["topo"], t["piso"]["sub"]]
    blocos += [a["bloco"] for a in t.get("aneis", [])]
    return unicos(blocos)


# -------------------------------------------------------- dimensão e bioma

def dimension_type(c):
    d = c["dimensao"]
    r = {
        "ultrawarm": d["quente"],
        "natural": True,
        "coordinate_scale": 1.0,
        "has_skylight": True,
        "has_ceiling": False,
        "ambient_light": d["luz_ambiente"],
        "monster_spawn_light_level": {"type": "minecraft:uniform",
                                      "value": {"min_inclusive": 0, "max_inclusive": 7}},
        "monster_spawn_block_light_limit": 0,
        "piglin_safe": d["quente"],
        "bed_works": False,
        "respawn_anchor_works": True,
        "has_raids": False,
        "logical_height": 384,
        "min_y": -64,
        "height": 384,
        "infiniburn": "#minecraft:infiniburn_overworld",
        "effects": "minecraft:overworld",
    }
    if d["tempo_fixo"] is not None:
        r["fixed_time"] = d["tempo_fixo"]
    return r


def faixa(nome_ruido, pf):
    return [round(ruido.valor(nome_ruido, pf[0]), 4), round(ruido.valor(nome_ruido, pf[1]), 4)]


def dimension(cid, c):
    biomas = []
    for b in c["biomas"]:
        biomas.append({
            "biome": id_bioma(cid, b),
            "parameters": {
                "temperature": faixa(TEMP, b["t"]),
                "humidity": faixa(VEG, b["h"]),
                "continentalness": faixa(CONT, b["c"]),
                "erosion": [-2.0, 2.0],
                "weirdness": [-2.0, 2.0],
                "depth": 0.0,
                "offset": 0.0,
            },
        })
    return {
        "type": f"{MODID}:{cid}",
        "generator": {
            "type": "minecraft:noise",
            "settings": f"{MODID}:{cid}",
            "biome_source": {"type": "minecraft:multi_noise", "biomes": biomas},
        },
    }


def spawners(mobs):
    r = {cat: [] for cat in CATEGORIAS_MOB}
    for cat, lista in mobs.items():
        assert cat in r, f"categoria de mob inválida: {cat}"
        r[cat] = [{"type": e, "weight": p, "minCount": mn, "maxCount": mx}
                  for e, p, mn, mx in lista]
    return r


def bioma_json(cid, c, b, features_por_passo, carvers):
    ceu, neblina, agua, nevoa = (rgb(x) for x in b.get("cores", c["cores"]))
    r = {
        "has_precipitation": bool(b.get("chuva", False)),
        "temperature": b.get("temp_bioma", c["dimensao"]["temp_bioma"]),
        "downfall": 0.8 if b.get("chuva") else 0.0,
        "effects": {"sky_color": ceu, "fog_color": neblina,
                    "water_color": agua, "water_fog_color": nevoa,
                    "mood_sound": {"sound": "minecraft:ambient.cave", "tick_delay": 6000,
                                   "block_search_extent": 8, "offset": 2.0}},
        "spawners": spawners(c["mobs"]),
        "spawn_costs": {},
        "carvers": {"air": carvers} if carvers else {},
        "features": features_por_passo,
    }
    if c.get("prob_criaturas") is not None:   # chance de nascerem criaturas na geração do chunk
        r["creature_spawn_probability"] = c["prob_criaturas"]
    return r


# ------------------------------------------------- funções de densidade (relevo)

def noise(nome, xz, y=0.0):
    return {"type": "minecraft:noise", "noise": nome, "xz_scale": xz, "y_scale": y}


def add(*a):
    return reduce(lambda p, q: {"type": "minecraft:add", "argument1": p, "argument2": q}, a)


def mul(a, b):
    return {"type": "minecraft:mul", "argument1": a, "argument2": b}


def dmin(a, b):
    return {"type": "minecraft:min", "argument1": a, "argument2": b}


def dmax(a, b):
    return {"type": "minecraft:max", "argument1": a, "argument2": b}


def clamp(x, lo, hi):
    return {"type": "minecraft:clamp", "input": x, "min": lo, "max": hi}


def lim(x):
    return clamp(x, -1.0, 1.0)


def grad(y0, y1, v0, v1):
    return {"type": "minecraft:y_clamped_gradient",
            "from_y": y0, "to_y": y1, "from_value": v0, "to_value": v1}


def camada(cam):
    """Laje horizontal de terreno (Júpiter, Saturno, anéis, crosta de Europa).
    Densidade 1 no meio da laje e -1 fora; com 'cob' ela vira ilhas (ruído 3D)."""
    y0, y1 = cam["y"]
    r = cam.get("rampa", max(2, min(10, (y1 - y0) // 2)))
    d = dmin(grad(y0, y0 + r, -1.0, 1.0), grad(y1 - r, y1, 1.0, -1.0))
    if cam.get("relevo"):
        d = add(d, mul(cam["relevo"], lim(noise(EROS, cam.get("xz", 3.0)))))
    if cam.get("cob") is not None:
        k = cam.get("k", 1.4)
        t = ruido.valor(CHEESE, 1 - cam["cob"])
        d = add(d, -1.0 - k * t, mul(k, noise(CHEESE, cam.get("xz", 3.0), cam.get("ys", 2.0))))
    return d


def regiao(t):
    return lim(noise(CONT, t.get("reg_xz", 1.4)))


def densidade_solida(t):
    base, H = t["base_y"], t.get("H", 48)
    reg = regiao(t)
    forca_mont = t["montanhas"][0] if t.get("montanhas") else 0.0
    assert t["amp"] + forca_mont <= 1.0 + 1e-9, "amp + montanhas > 1 criaria blocos flutuando"
    relevo = mul(t["amp"], lim(noise(EROS, t.get("xz", 3.0))))
    partes = [grad(base - H, base + H, 1.0, -1.0)]
    if t.get("planicie"):
        lim_p = ruido.valor(CONT, t["planicie"])
        baixa = clamp(mul(4.0, add(lim_p, mul(-1.0, reg))), 0.0, 1.0)
        relevo = mul(relevo, add(1.0, mul(-0.92, baixa)))   # relevo quase zero nas planícies
        partes.append(mul(-0.12, baixa))                    # e um pouco mais baixas
    partes.append(relevo)
    if t.get("montanhas"):
        k, cob = t["montanhas"]
        lim_m = ruido.valor(CONT, 1 - cob)
        partes.append(mul(k, clamp(mul(4.0, add(reg, -lim_m)), 0.0, 1.0)))
    for cr in t.get("crateras", []):
        lim_c = ruido.valor(cr["ruido"], 1 - cr["cob"])
        fundo = clamp(mul(6.0, add(noise(cr["ruido"], cr["xz"]), -lim_c)), 0.0, 1.0)
        partes.append(mul(-cr["prof"], fundo))
    d = add(*partes)
    for anel in t.get("aneis", []):
        d = dmax(d, camada(anel))
    return d


def densidade_camadas(t):
    return reduce(dmax, [camada(cam) for cam in t["camadas"]])


# ------------------------------------------------------------- regras de superfície

def blk(nome):
    return {"type": "minecraft:block", "result_state": estado(nome)}


def cond(se, entao):
    return {"type": "minecraft:condition", "if_true": se, "then_run": entao}


def seq(*regras):
    return {"type": "minecraft:sequence", "sequence": list(regras)}


def y_acima(y):
    return {"type": "minecraft:y_above", "anchor": {"absolute": y},
            "surface_depth_multiplier": 0, "add_stone_depth": False}


def nao(c):
    return {"type": "minecraft:not", "invert": c}


def profundidade(com_camada_de_superficie):
    return {"type": "minecraft:stone_depth", "offset": 0, "surface_type": "floor",
            "add_surface_depth": com_camada_de_superficie, "secondary_depth_range": 0}


def fora_da_agua():
    return {"type": "minecraft:water", "offset": 0, "surface_depth_multiplier": 0,
            "add_stone_depth": False}


def limiar(ruido_nome, a, b):
    return {"type": "minecraft:noise_threshold", "noise": ruido_nome,
            "min_threshold": a, "max_threshold": b}


def regra_solo(topo, sub, listras=(), fundo=None):
    cima = blk(topo) if not fundo else seq(cond(fora_da_agua(), blk(topo)), blk(fundo))
    if listras:
        cima = seq(*[cond(limiar(l["ruido"], l["min"], l["max"]), blk(l["bloco"]))
                     for l in listras], cima)
    return seq(cond(profundidade(False), cima), cond(profundidade(True), blk(sub)))


def regra_bioma(cid, c, b):
    t = c["terreno"]
    if b.get("faixas"):
        f = b["faixas"]
        interior = seq(*[cond(y_acima(y), blk(bl)) for y, bl in f[:-1]], blk(f[-1][1]))
    else:
        interior = regra_solo(b["topo"], b["sub"], b.get("listras", []), t.get("fundo"))
    return cond({"type": "minecraft:biome", "biome_is": [id_bioma(cid, b)]}, interior)


def noise_settings(cid, c):
    t = c["terreno"]
    if t["modo"] == "solido":
        bruta = densidade_solida(t)
    else:
        bruta = densidade_camadas(t)
    final = {"type": "minecraft:interpolated", "argument": bruta}
    clima = t.get("clima_xz", 2.2)
    roteador = {
        "barrier": 0.0, "fluid_level_floodedness": 0.0, "fluid_level_spread": 0.0, "lava": 0.0,
        "temperature": noise(TEMP, clima),
        "vegetation": noise(VEG, clima * 0.7),
        "continents": regiao(t),
        "erosion": 0.0, "depth": 0.0, "ridges": 0.0,
        "initial_density_without_jaggedness": bruta,
        "final_density": final,
        "vein_toggle": 0.0, "vein_ridged": 0.0, "vein_gap": 0.0,
    }
    regras = [{
        "type": "minecraft:condition",
        "if_true": {"type": "minecraft:vertical_gradient", "random_name": "minecraft:bedrock_floor",
                    "true_at_and_below": {"above_bottom": 0},
                    "false_at_and_above": {"above_bottom": 5}},
        "then_run": blk("minecraft:bedrock"),
    }]
    for anel in t.get("aneis", []):
        regras.append(cond(y_acima(anel["y"][0] - 2), blk(anel["bloco"])))
    if t.get("piso"):
        p = t["piso"]
        regras.append(cond(nao(y_acima(p["abaixo_de"])), regra_solo(p["topo"], p["sub"])))
    regras += [regra_bioma(cid, c, b) for b in c["biomas"]]
    return {
        "sea_level": t["nivel_mar"],
        "disable_mob_generation": False,
        "aquifers_enabled": False,
        "ore_veins_enabled": False,
        "legacy_random_source": False,
        "default_block": estado(t["default"]),
        "default_fluid": estado_fluido(f"minecraft:{t['fluido']}"),
        "noise": {"min_y": -64, "height": 384, "size_horizontal": 1, "size_vertical": 2},
        "noise_router": roteador,
        "spawn_target": [],
        "surface_rule": seq(*regras),
    }


# ----------------------------------------------------- minérios, manchas e carvers

def intervalo_y(c, f):
    y = f["y"]
    if y[0] == "rel":
        base = c["terreno"]["base_y"]
        return base + y[1], base + y[2]
    return y


def feature_ore(c, f):
    alvos = [a for a in (f.get("alvo") or blocos_do_corpo(c)) if a != f["bloco"]]
    assert alvos, f"feature {f['nome']} sem alvos"
    return {"type": "minecraft:ore", "config": {
        "discard_chance_on_air_exposure": f.get("descarte", 0.0),
        "size": f["tam"],
        "targets": [{"state": estado(f["bloco"]),
                     "target": {"predicate_type": "minecraft:block_match", "block": a}}
                    for a in alvos],
    }}


def feature_colocada(cid, f, y0, y1):
    return {"feature": id_feat(cid, f["nome"]), "placement": [
        {"type": "minecraft:count", "count": f["qtd"]},
        {"type": "minecraft:in_square"},
        {"type": "minecraft:height_range", "height": {
            "type": "minecraft:uniform",
            "min_inclusive": {"absolute": y0}, "max_inclusive": {"absolute": y1}}},
        {"type": "minecraft:biome"},
    ]}


def uniforme(a, b):
    return {"type": "minecraft:uniform", "value": {"min_inclusive": a, "max_exclusive": b}}


def carver_caverna(c, prob, y_max):
    return {"type": "minecraft:cave", "config": {
        "floor_level": uniforme(-1.0, -0.4),
        "horizontal_radius_multiplier": uniforme(0.7, 1.4),
        "lava_level": {"above_bottom": 8},
        "probability": prob,
        "replaceable": blocos_do_corpo(c),
        "vertical_radius_multiplier": uniforme(0.8, 1.3),
        "y": {"type": "minecraft:uniform", "max_inclusive": {"absolute": y_max},
              "min_inclusive": {"above_bottom": 8}},
        "yScale": uniforme(0.1, 0.9),
    }}


def carver_canion(c, prob, y0, y1):
    return {"type": "minecraft:canyon", "config": {
        "lava_level": {"above_bottom": 8},
        "probability": prob,
        "replaceable": blocos_do_corpo(c),
        "shape": {
            "distance_factor": uniforme(0.75, 1.0),
            "horizontal_radius_factor": uniforme(0.75, 1.0),
            "thickness": {"type": "minecraft:trapezoid",
                          "value": {"max": 6.0, "min": 0.0, "plateau": 2.0}},
            "vertical_radius_center_factor": 0.0,
            "vertical_radius_default_factor": 1.0,
            "width_smoothness": 3,
        },
        "vertical_rotation": uniforme(-0.125, 0.125),
        "y": {"type": "minecraft:uniform", "max_inclusive": {"absolute": y1},
              "min_inclusive": {"absolute": y0}},
        "yScale": 3.0,
    }}


# ------------------------------------------------------------------ dados físicos

def dados_fisicos(cid, c):
    d = {"id": cid, "nome": c["nome"], "tipo": c["tipo"], "dimensao": f"{MODID}:{cid}",
         "descricao": c["descricao"], "fisica": c["fisica"],
         "ceu": dict(zip(["ceu", "neblina", "agua", "nevoa_da_agua"], c["cores"])),
         "tempo_fixo": c["dimensao"]["tempo_fixo"],
         "biomas": [id_bioma(cid, b) for b in c["biomas"]],
         "minerios": [f["nome"] for f in c["features"]]}
    if c.get("lua_de"):
        d["lua_de"] = c["lua_de"]
    return d


def nome_do_bloco(bloco):
    return bloco.split(":", 1)[1].replace("_", " ")


def doc_corpo(cid, c):
    f = c["fisica"]
    t = c["terreno"]
    linhas = [f"### {c['nome']}  (`{MODID}:{cid}`)", "", c["descricao"], ""]
    linhas.append(f"- **Gravidade:** {f['gravidade_g']} g · **Temperatura média:** "
                  f"{f['temperatura_c']} °C · **Dia:** "
                  f"{('%g h' % f['dia_horas']) if f.get('dia_horas') else 'n/d'}")
    linhas.append(f"- **Atmosfera:** {f['atmosfera']} · **Respirável:** "
                  f"{'sim' if f['respiravel'] else 'não'}")
    linhas.append(f"- **Perigos:** {', '.join(f['perigos'])}")
    if t["modo"] == "solido":
        extra = []
        if t.get("montanhas"):
            extra.append(f"montanhas em {int(t['montanhas'][1] * 100)}% do mapa")
        if t.get("planicie"):
            extra.append(f"planícies achatadas em {int(t['planicie'] * 100)}%")
        if t.get("crateras"):
            extra.append("crateras (" + ", ".join(
                f"{int(cr['cob'] * 100)}% a {int(cr['prof'] * t.get('H', 48))} blocos"
                for cr in t["crateras"]) + ")")
        if t.get("cavernas"):
            extra.append("cavernas/tubos")
        if t.get("canions"):
            extra.append("cânions")
        if t["fluido"] and t["nivel_mar"] > -60:
            extra.append(f"{'lava' if t['fluido'] == 'lava' else 'água'} no nível {t['nivel_mar']}")
        linhas.append(f"- **Terreno:** sólido, altura média {t['base_y']}; " + "; ".join(extra))
    else:
        linhas.append("- **Terreno:** camadas flutuantes — " + "; ".join(
            f"y {cam['y'][0]}–{cam['y'][1]}" for cam in t["camadas"]))
    linhas.append("- **Biomas:** " + ", ".join(f"`{b['nome']}`" for b in c["biomas"]))
    linhas.append("- **Minérios/manchas:** " + ", ".join(
        f"{x['nome']} ({nome_do_bloco(x['bloco'])})" for x in c["features"]))
    mobs = [nome_do_bloco(e) for lista in c["mobs"].values() for e, *_ in lista]
    linhas.append("- **Criaturas:** " + (", ".join(mobs) if mobs else "nenhuma"))
    return "\n".join(linhas) + "\n"


def gerar_docs():
    grupos = [("Planetas", "planeta"), ("Planetas anões", "anao"), ("Luas", "lua")]
    out = ["# Corpos celestes do mod", "",
           "Arquivo **gerado** por `tools/gerar_dimensoes.py` a partir de `tools/corpos.py`. "
           "Não edite aqui.", "",
           "| Corpo | Tipo | Gravidade (g) | Temp. (°C) | Dia (h) | Respirável |",
           "|---|---|---|---|---|---|"]
    for cid, c in CORPOS.items():
        f = c["fisica"]
        out.append(f"| {c['nome']} | {c['tipo']} | {f['gravidade_g']} | {f['temperatura_c']} | "
                   f"{f.get('dia_horas') or 'n/d'} | {'sim' if f['respiravel'] else 'não'} |")
    out.append("")
    for titulo, tipo in grupos:
        out += [f"## {titulo}", ""]
        for cid, c in CORPOS.items():
            if c["tipo"] == tipo:
                out += [doc_corpo(cid, c)]
    DOCS.mkdir(exist_ok=True)
    (DOCS / "CORPOS.md").write_text("\n".join(out), encoding="utf-8")


# ------------------------------------------------------------------------- main

def gerar_corpo(cid, c):
    t = c["terreno"]
    # features por bioma
    por_bioma = {b["nome"]: [[] for _ in range(11)] for b in c["biomas"]}
    for f in c["features"]:
        y0, y1 = intervalo_y(c, f)
        gravar(DADOS / "worldgen" / "configured_feature" / f"{cid}_{f['nome']}.json",
               feature_ore(c, f))
        gravar(DADOS / "worldgen" / "placed_feature" / f"{cid}_{f['nome']}.json",
               feature_colocada(cid, f, y0, y1))
        for b in c["biomas"]:
            if f.get("biomas") is None or b["nome"] in f["biomas"]:
                por_bioma[b["nome"]][PASSO_MINERIOS].append(id_feat(cid, f["nome"]))
    # carvers
    carvers = []
    base = t.get("base_y", 70)
    if t.get("cavernas"):
        gravar(DADOS / "worldgen" / "configured_carver" / f"{cid}_caverna.json",
               carver_caverna(c, t["cavernas"], t.get("caverna_y_max", base + 20)))
        carvers.append(f"{MODID}:{cid}_caverna")
    if t.get("canions"):
        y0, y1 = t.get("canion_y", (base - 55, base - 3))
        gravar(DADOS / "worldgen" / "configured_carver" / f"{cid}_canion.json",
               carver_canion(c, t["canions"], y0, y1))
        carvers.append(f"{MODID}:{cid}_canion")
    # arquivos principais
    gravar(DADOS / "dimension_type" / f"{cid}.json", dimension_type(c))
    gravar(DADOS / "dimension" / f"{cid}.json", dimension(cid, c))
    gravar(DADOS / "worldgen" / "noise_settings" / f"{cid}.json", noise_settings(cid, c))
    for b in c["biomas"]:
        gravar(DADOS / "worldgen" / "biome" / f"{cid}_{b['nome']}.json",
               bioma_json(cid, c, b, por_bioma[b["nome"]], carvers))
    gravar(DADOS / "corpos" / f"{cid}.json", dados_fisicos(cid, c))
    print(f"gerado: {cid:8s} {len(c['biomas'])} biomas, {len(c['features'])} features, "
          f"{len(carvers)} carvers")


def main():
    for pasta in PASTAS_GERADAS:
        shutil.rmtree(DADOS / pasta, ignore_errors=True)
    for cid, c in CORPOS.items():
        gerar_corpo(cid, c)
    gerar_docs()
    print(f"{len(CORPOS)} corpos; docs em {DOCS / 'CORPOS.md'}")


if __name__ == "__main__":
    main()
