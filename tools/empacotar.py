#!/usr/bin/env python3
"""Empacota o mod para download.

Uso:  python3 tools/empacotar.py VERSAO PASTA_SAIDA

Gera em PASTA_SAIDA:
  sistemasolar-<versao>.jar          mod Forge 1.20.1 só de dados (pasta mods/)
  sistemasolar-datapack-<versao>.zip datapack (pasta datapacks/ do mundo)
"""
import json
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
RES = RAIZ / "src" / "main" / "resources"


def arquivos(incluir_meta_inf):
    for f in sorted(RES.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(RES).as_posix()
        if rel.startswith("META-INF/") and not incluir_meta_inf:
            continue
        yield f, rel


def zipar(destino, incluir_meta_inf):
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for f, rel in arquivos(incluir_meta_inf):
            if rel.endswith(".json") or rel.endswith(".mcmeta"):
                json.loads(f.read_text(encoding="utf-8"))  # falha cedo se inválido
            info = zipfile.ZipInfo(rel, date_time=(2026, 10, 31, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, f.read_bytes())
    print(f"gerado: {destino}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    versao, saida = sys.argv[1], Path(sys.argv[2])
    saida.mkdir(parents=True, exist_ok=True)
    zipar(saida / f"sistemasolar-{versao}.jar", True)
    zipar(saida / f"sistemasolar-datapack-{versao}.zip", False)
