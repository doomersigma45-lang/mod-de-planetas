# Mod Sistema Solar — Forge 1.20.1

Mod feito em parceria entre Claude e ChatGPT. Minecraft 1.20.1, Forge 47.x, Java 17.

## Convenções compartilhadas (as duas IAs seguem isto)

- **modid:** `sistemasolar`
- **Pacote Java:** `com.sistemasolar`
- **Dimensões:** `sistemasolar:<corpo>` (ex.: `sistemasolar:marte`)
- **Arquivos de dados:** `src/main/resources/data/sistemasolar/...`
  - `dimension_type/<corpo>.json`
  - `dimension/<corpo>.json`
  - `worldgen/biome/<corpo>_<bioma>.json`
  - `worldgen/noise_settings/<corpo>.json`
- **Ids dos corpos em minúsculo, sem acento:** marte, venus, miller, netuno, plutao, ceres, lua, saturno, jupiter, haumea, sedna, titan, europa, io
- **Gravidade/atmosfera:** definidas por corpo na classe `CorpoCeleste` (gravidade, oxigênio, temperatura, dano ambiental)

## Divisão

Divisão original: 7 corpos para cada IA. O ChatGPT ficou fora por tempo indeterminado
(limite de uso), então o Claude assumiu os 14 corpos.

| Categoria | Feitos |
|---|---|
| Planetas | Marte, Vênus, Planeta Miller, Netuno (extra), Saturno, Júpiter |
| Planetas anões | Plutão, Ceres, Haumea, Sedna |
| Luas | Lua, Titã, Europa, Io |

Os dados de cada corpo ficam em `tools/corpos.py`; `python3 tools/gerar_dimensoes.py`
gera todos os JSON e o `docs/CORPOS.md`. Para conferir contra os dados oficiais do 1.20.1,
veja o cabeçalho de `tools/validar.py`.

## Ideia inicial dos primeiros 7 corpos (a versão detalhada de todos está em `docs/CORPOS.md`)

- **Marte:** deserto vermelho, céu alaranjado, poeira, cânions, gelo nos polos.
- **Vênus:** calor extremo, névoa densa e amarelada, chuva ácida, lava e basalto.
- **Planeta Miller:** oceano raso e infinito, gravidade alta, ondas gigantes, lua escura no céu.
- **Netuno (extra):** planeta gelado e azul, ventos fortes, ilhas de gelo azul e diamante.
- **Plutão:** planície de gelo de nitrogênio com a região em forma de coração, céu escuro.
- **Ceres:** rocha escura com manchas brilhantes de sal e gelo, gravidade baixa.
- **Lua:** cinza, crateras, gravidade baixa, sem ar, céu preto com a Terra visível.

## Ainda a fazer (depois dos dados das dimensões)

1. Classe Java `CorpoCeleste` + registro das dimensões
2. Foguete e forma de viajar entre corpos
3. Traje espacial e sistema de oxigênio
4. Minérios e itens exclusivos de cada corpo

## Plutão (v0.2.0) e integração com o Netherite Supremo

- Plutão agora é uma **crosta de gelo sobre oceanos** (mesmo esquema de camadas de Europa): fundo rochoso, água
  no meio e crosta de gelo na superfície, com coração de Tombaugh, terras escuras de tolinas e montanhas de gelo.
- As **árvores de cristal** e os spawns de **Aldeão Precursor e Robô** vêm do mod *Netherite Supremo* (repositório
  `repositorio-pro-meu-mano-cloud-2`), que liga isso aos biomas `sistemasolar:plutao_*` por tags opcionais.
  Sem o Netherite Supremo instalado, Plutão funciona normalmente, só sem as árvores e os mobs.
- O boss de Plutão fica para depois.
