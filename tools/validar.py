#!/usr/bin/env python3
"""Valida os JSON gerados contra os dados oficiais do Minecraft 1.20.1.

Não substitui testar no jogo, mas pega a maioria dos erros que travariam o carregamento:
chave faltando ou sobrando, tipo inexistente, bloco/entidade/ruído com nome errado,
referência para arquivo que não existe.

Uso:
    python3 tools/validar.py --dados DIR_DATA_JSON --registros DIR_REGISTRIES

Onde baixar (público, espelho dos arquivos do jogo):
    git clone --depth 1 --branch 1.20.1-data-json   https://github.com/misode/mcmeta dados
    git clone --depth 1 --branch 1.20.1-registries  https://github.com/misode/mcmeta registros
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

MODID = "sistemasolar"
RAIZ = Path(__file__).resolve().parent.parent
MEU = RAIZ / "src" / "main" / "resources" / "data" / MODID

# registros cujos ids aparecem no campo "type" dos JSON de worldgen
REGISTROS_DE_TIPO = [
    "worldgen/density_function_type", "worldgen/material_condition", "worldgen/material_rule",
    "worldgen/placement_modifier_type", "worldgen/feature", "worldgen/carver",
    "worldgen/biome_source", "worldgen/block_state_provider_type", "worldgen/chunk_generator",
    "int_provider_type", "height_provider_type", "float_provider_type", "block_predicate_type",
]


def carregar_lista(registros, nome):
    for arq in ("data.min.json", "data.json"):
        p = registros / nome / arq
        if p.exists():
            return set(json.loads(p.read_text()))
    return set()


def andar(no, visita, caminho=()):
    visita(no, caminho)
    if isinstance(no, dict):
        for k, v in no.items():
            andar(v, visita, caminho + (k,))
    elif isinstance(no, list):
        for i, v in enumerate(no):
            andar(v, visita, caminho + (i,))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", required=True, help="pasta 'data' do espelho 1.20.1-data-json")
    ap.add_argument("--registros", required=True, help="pasta do espelho 1.20.1-registries")
    args = ap.parse_args()
    van = Path(args.dados) / "data" / "minecraft"
    reg = Path(args.registros)
    erros, avisos = [], []

    # ---- 1. todos os JSON carregam
    meus = {}
    for f in sorted(MEU.rglob("*.json")):
        try:
            meus[f] = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            erros.append(f"JSON inválido: {f.relative_to(RAIZ)}: {e}")
    print(f"{len(meus)} arquivos JSON lidos")

    # ---- 2. referências entre arquivos
    def existe(cat, ident):
        ns, nome = ident.split(":", 1)
        if ns == "minecraft":
            return (van / cat / f"{nome}.json").exists()
        return (MEU / cat / f"{nome}.json").exists()

    for f, d in meus.items():
        rel = f.relative_to(MEU).parts
        if rel[0] == "dimension":
            if not existe("dimension_type", d["type"]):
                erros.append(f"{f.name}: dimension_type {d['type']} não existe")
            if not existe("worldgen/noise_settings", d["generator"]["settings"]):
                erros.append(f"{f.name}: noise_settings não existe")
            for b in d["generator"]["biome_source"]["biomes"]:
                if not existe("worldgen/biome", b["biome"]):
                    erros.append(f"{f.name}: bioma {b['biome']} não existe")
        elif rel[:2] == ("worldgen", "biome"):
            for passo in d["features"]:
                for ident in passo:
                    if not existe("worldgen/placed_feature", ident):
                        erros.append(f"{f.name}: placed_feature {ident} não existe")
            for ident in d["carvers"].get("air", []):
                if not existe("worldgen/configured_carver", ident):
                    erros.append(f"{f.name}: carver {ident} não existe")
        elif rel[:2] == ("worldgen", "placed_feature"):
            if not existe("worldgen/configured_feature", d["feature"]):
                erros.append(f"{f.name}: configured_feature {d['feature']} não existe")
        elif rel[0] == "corpos":
            continue
        # todo bioma mencionado nas regras de superfície existe?
        if rel[:2] == ("worldgen", "noise_settings"):
            def checa_bioma(no, _):
                if isinstance(no, dict) and "biome_is" in no:
                    for b in no["biome_is"]:
                        if not existe("worldgen/biome", b):
                            erros.append(f"{f.name}: biome_is {b} não existe")
            andar(d["surface_rule"], checa_bioma)

    # ---- 3. ids de bloco / entidade / ruído / tipos
    blocos = carregar_lista(reg, "block")
    entidades = carregar_lista(reg, "entity_type")
    ruidos = {p.stem for p in (van / "worldgen" / "noise").glob("*.json")}
    tipos = set(entidades)
    for r in REGISTROS_DE_TIPO:
        tipos |= carregar_lista(reg, r)
    rule_tests = carregar_lista(reg, "rule_test")
    if not blocos or not entidades or not tipos:
        avisos.append("registros não carregados: pulei a checagem de ids")

    def curto(ident):
        ns, nome = ident.split(":", 1)
        return ns, nome

    def checa_ids(no, caminho):
        if not isinstance(no, dict):
            return
        for k, v in no.items():
            if k in ("Name", "block") and isinstance(v, str) and blocos:
                ns, n = curto(v)
                if ns == "minecraft" and n not in blocos:
                    erros.append(f"bloco inexistente: {v} em {'/'.join(map(str, caminho))}")
            elif k == "replaceable" and isinstance(v, list) and blocos:
                for b in v:
                    if curto(b)[1] not in blocos:
                        erros.append(f"bloco inexistente em replaceable: {b}")
            elif k == "noise" and isinstance(v, str) and ruidos:
                if curto(v)[1] not in ruidos:
                    erros.append(f"ruído inexistente: {v}")
            elif k == "predicate_type" and rule_tests:
                if curto(v)[1] not in rule_tests:
                    erros.append(f"predicate_type inexistente: {v}")
            elif k == "type" and isinstance(v, str) and v.startswith("minecraft:") and tipos:
                if curto(v)[1] not in tipos:
                    erros.append(f"type inexistente: {v}")

    for f, d in meus.items():
        andar(d, lambda n, c, f=f: checa_ids(n, (f.name,) + c))

    # ---- 4. chaves de cada objeto 'type' comparadas com o vanilla
    esq = defaultdict(list)
    pastas = ["worldgen/noise_settings", "worldgen/density_function", "worldgen/configured_feature",
              "worldgen/placed_feature", "worldgen/configured_carver", "worldgen/biome",
              "dimension_type", "worldgen/world_preset", "dimension"]
    for p in pastas:
        for f in (van / p).rglob("*.json"):
            andar(json.loads(f.read_text()), lambda n, c: esq[n["type"]].append(frozenset(n))
                  if isinstance(n, dict) and isinstance(n.get("type"), str)
                  and n["type"].startswith("minecraft:") else None)
    sem_ref = set()

    def checa_chaves(no, caminho, nome):
        if not (isinstance(no, dict) and isinstance(no.get("type"), str)
                and no["type"].startswith("minecraft:")):
            return
        t = no["type"]
        if t not in esq:
            sem_ref.add(t)
            return
        uniao = frozenset().union(*esq[t])
        comum = frozenset.intersection(*esq[t])
        chaves = frozenset(no)
        if chaves - uniao:
            erros.append(f"{nome}: '{t}' tem chave desconhecida {sorted(chaves - uniao)}")
        if comum - chaves:
            erros.append(f"{nome}: '{t}' sem chave obrigatória {sorted(comum - chaves)}")

    for f, d in meus.items():
        if f.relative_to(MEU).parts[0] != "corpos":
            andar(d, lambda n, c, f=f: checa_chaves(n, c, f.name))

    # ---- 5. objetos de topo (sem 'type'): biome, noise_settings, noise_router, dimension_type
    def compara_topo(pasta_vanilla, minha_pasta, extra_ok=(), caminho=()):
        ref = [json.loads(f.read_text()) for f in (van / pasta_vanilla).glob("*.json")]
        for f, d in meus.items():
            if f.relative_to(MEU).parts[:len(minha_pasta)] != tuple(minha_pasta):
                continue
            alvo = d
            vref = ref
            for k in caminho:
                alvo = alvo[k]
                vref = [r[k] for r in vref if k in r]
            uniao = set().union(*[set(r) for r in vref]) | set(extra_ok)
            comum = set.intersection(*[set(r) for r in vref])
            if set(alvo) - uniao:
                erros.append(f"{f.name}: chaves desconhecidas {sorted(set(alvo) - uniao)}")
            if comum - set(alvo):
                erros.append(f"{f.name}: chaves obrigatórias faltando {sorted(comum - set(alvo))}")

    compara_topo("worldgen/biome", ("worldgen", "biome"))
    compara_topo("worldgen/biome", ("worldgen", "biome"), caminho=("effects",))
    compara_topo("worldgen/biome", ("worldgen", "biome"), caminho=("spawners",))
    compara_topo("worldgen/noise_settings", ("worldgen", "noise_settings"))
    compara_topo("worldgen/noise_settings", ("worldgen", "noise_settings"), caminho=("noise",))
    compara_topo("worldgen/noise_settings", ("worldgen", "noise_settings"),
                 caminho=("noise_router",))
    compara_topo("dimension_type", ("dimension_type",), extra_ok=("fixed_time",))

    # ---- 6. verificações específicas
    for f, d in meus.items():
        rel = f.relative_to(MEU).parts
        if rel[:2] == ("worldgen", "biome"):
            if len(d["features"]) != 11:
                erros.append(f"{f.name}: precisa de 11 passos de features")
        if rel[:2] == ("worldgen", "configured_feature") and d["type"] == "minecraft:ore":
            if not 1 <= d["config"]["size"] <= 64:
                erros.append(f"{f.name}: tamanho de minério fora de 1..64")

    # ---- relatório
    if sem_ref:
        avisos.append("tipos sem exemplo no vanilla (conferir à mão): " + ", ".join(sorted(sem_ref)))
    for a in avisos:
        print("AVISO:", a)
    for e in erros:
        print("ERRO:", e)
    print(f"\n{len(erros)} erros, {len(avisos)} avisos")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
