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

| Categoria | Claude | ChatGPT |
|---|---|---|
| Planetas | Marte, Vênus, Planeta Miller, Netuno (extra escolhido por mim) | Saturno, Júpiter |
| Planetas anões | Plutão, Ceres | Haumea, Sedna |
| Luas | Lua | Titã, Europa, Io |

Total: 7 para o Claude, 7 para o ChatGPT.

## Ideia de cada corpo do Claude

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
