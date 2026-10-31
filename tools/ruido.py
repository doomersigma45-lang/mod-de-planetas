"""Estatística dos ruídos do Minecraft 1.20.1, para calibrar limiares sem abrir o jogo.

O gerador precisa dizer coisas como "crateras em 15% do terreno" ou "este bioma ocupa
os 30% mais frios". Para isso é preciso saber a distribuição dos valores de cada ruído
(a mesma para qualquer xz_scale: a escala só muda o tamanho das manchas).

Aqui reimplementamos o NormalNoise do vanilla (Perlin 3D melhorado, mesmas oitavas e
mesmo fator de normalização) e medimos os percentis por amostragem. A semente do
Minecraft não é reproduzida (não importa para a estatística).
Resultado em cache: tools/quantis.json
"""
import json
from pathlib import Path

import numpy as np

# firstOctave e amplitudes copiados de data/minecraft/worldgen/noise/<nome>.json (1.20.1)
RUIDOS = {
    "minecraft:continentalness": (-9, [1.0, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0]),
    "minecraft:erosion": (-9, [1.0, 1.0, 0.0, 1.0, 1.0]),
    "minecraft:temperature": (-10, [1.5, 0.0, 1.0, 0.0, 0.0, 0.0]),
    "minecraft:vegetation": (-8, [1.0, 1.0, 0.0, 0.0, 0.0, 0.0]),
    "minecraft:ridge": (-7, [1.0, 2.0, 1.0, 0.0, 0.0, 0.0]),
    "minecraft:ice": (-4, [1.0, 1.0, 1.0, 1.0]),
    "minecraft:cave_cheese": (-8, [0.5, 1.0, 2.0, 1.0, 2.0, 1.0, 0.0, 2.0, 0.0]),
    "minecraft:surface": (-6, [1.0, 1.0, 1.0]),
}

ARQ = Path(__file__).with_name("quantis.json")
N_AMOSTRAS = 400_000

_GRAD = np.array([
    (1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
    (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
    (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
], dtype=float)


def _fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


class _Perlin3D:
    def __init__(self, rng):
        self.p = np.concatenate([rng.permutation(256)] * 2)

    def __call__(self, x, y, z):
        xi, yi, zi = np.floor(x).astype(int), np.floor(y).astype(int), np.floor(z).astype(int)
        xf, yf, zf = x - xi, y - yi, z - zi
        xi, yi, zi = xi & 255, yi & 255, zi & 255
        u, v, w = _fade(xf), _fade(yf), _fade(zf)
        p = self.p

        def g(dx, dy, dz):
            h = p[p[p[xi + dx] + yi + dy] + zi + dz] % 12
            gr = _GRAD[h]
            return gr[:, 0] * (xf - dx) + gr[:, 1] * (yf - dy) + gr[:, 2] * (zf - dz)

        def lerp(t, a, b):
            return a + t * (b - a)

        return lerp(w,
                    lerp(v, lerp(u, g(0, 0, 0), g(1, 0, 0)), lerp(u, g(0, 1, 0), g(1, 1, 0))),
                    lerp(v, lerp(u, g(0, 0, 1), g(1, 0, 1)), lerp(u, g(0, 1, 1), g(1, 1, 1))))


def _perlin_octaves(rng, primeira, amps, x, y, z):
    n = len(amps)
    base = 2.0 ** (n - 1) / (2.0 ** n - 1)
    total = np.zeros_like(x)
    for i, a in enumerate(amps):
        if a == 0:
            continue
        f = 2.0 ** (primeira + i)
        ruido = _Perlin3D(rng)
        off = rng.uniform(0, 256, 3)
        total += a * (base / 2.0 ** i) * ruido(x * f + off[0], y * f + off[1], z * f + off[2])
    return total


def amostrar(nome, n=N_AMOSTRAS, semente=12345):
    primeira, amps = RUIDOS[nome]
    rng = np.random.default_rng(semente)
    amplo = 2.0 ** (-primeira) * 40  # domínio grande: amostras quase independentes
    x, z = rng.uniform(0, amplo, n), rng.uniform(0, amplo, n)
    y = np.zeros(n)
    idx = [i for i, a in enumerate(amps) if a != 0]
    desvio = 0.1 * (1.0 + 1.0 / (max(idx) - min(idx) + 1))
    fator = (1.0 / 6.0) / desvio
    k = 1.0181268882175227
    a = _perlin_octaves(rng, primeira, amps, x, y, z)
    b = _perlin_octaves(rng, primeira, amps, x * k, y * k, z * k)
    return (a + b) * fator


def calcular():
    pts = np.linspace(0, 1, 101)
    return {nome: [round(float(v), 4) for v in np.quantile(amostrar(nome), pts)]
            for nome in RUIDOS}


_cache = None


def quantis():
    global _cache
    if _cache is None:
        if ARQ.exists():
            _cache = json.loads(ARQ.read_text())
        else:
            _cache = calcular()
            ARQ.write_text(json.dumps(_cache, indent=1) + "\n")
    return _cache


def valor(nome, p):
    """Valor do ruído abaixo do qual ficam a fração p (0..1) das amostras.
    Nas pontas devolve ±2, que o multi_noise do Minecraft trata como 'sem limite'."""
    if p <= 0:
        return -2.0
    if p >= 1:
        return 2.0
    q = quantis()[nome]
    pos = p * 100
    i = int(pos)
    return q[i] + (q[i + 1] - q[i]) * (pos - i)


if __name__ == "__main__":
    ARQ.write_text(json.dumps(calcular(), indent=1) + "\n")
    for nome, q in json.loads(ARQ.read_text()).items():
        print(f"{nome:28s} p5={q[5]:+.2f} p25={q[25]:+.2f} p50={q[50]:+.2f} "
              f"p75={q[75]:+.2f} p95={q[95]:+.2f} min={q[0]:+.2f} max={q[100]:+.2f}")
