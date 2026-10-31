# Corpos celestes do mod

Arquivo **gerado** por `tools/gerar_dimensoes.py` a partir de `tools/corpos.py`. Não edite aqui.

| Corpo | Tipo | Gravidade (g) | Temp. (°C) | Dia (h) | Respirável |
|---|---|---|---|---|---|
| Marte | planeta | 0.38 | -63 | 24.6 | não |
| Vênus | planeta | 0.9 | 464 | 5832 | não |
| Planeta Miller | planeta | 1.3 | 25 | n/d | sim |
| Netuno | planeta | 1.14 | -214 | 16.1 | não |
| Saturno | planeta | 1.07 | -178 | 10.7 | não |
| Júpiter | planeta | 2.53 | -145 | 9.9 | não |
| Plutão | anao | 0.063 | -229 | 153.3 | não |
| Ceres | anao | 0.029 | -105 | 9.07 | não |
| Haumea | anao | 0.044 | -241 | 3.9 | não |
| Sedna | anao | 0.03 | -261 | 10.0 | não |
| Lua | lua | 0.165 | -53 | 655.7 | não |
| Titã | lua | 0.138 | -179 | 382.7 | não |
| Europa | lua | 0.134 | -160 | 85.2 | não |
| Io | lua | 0.183 | -143 | 42.5 | não |

## Planetas

### Marte  (`sistemasolar:marte`)

Deserto vermelho de poeira e ferro oxidado, com cânions gigantes, vulcões enormes e gelo nos polos.

- **Gravidade:** 0.38 g · **Temperatura média:** -63 °C · **Dia:** 24.6 h
- **Atmosfera:** CO2 muito rarefeita (1% da pressão da Terra) · **Respirável:** não
- **Perigos:** frio, sem_oxigenio
- **Terreno:** sólido, altura média 72; montanhas em 14% do mapa; crateras (10% a 14 blocos, 12% a 8 blocos); cavernas/tubos; cânions
- **Biomas:** `calotas_polares`, `montes_vulcanicos`, `planicies_escuras`, `planicies_de_poeira`
- **Minérios/manchas:** ferro_oxidado (raw iron block), mirtilos_de_hematita (blue terracotta), gelo_subterraneo (packed ice), ferro (iron ore), cobre (copper ore)
- **Criaturas:** husk

### Vênus  (`sistemasolar:venus`)

Inferno de basalto e lava sob uma névoa amarela de ácido sulfúrico. O calor é extremo e a água evapora.

- **Gravidade:** 0.9 g · **Temperatura média:** 464 °C · **Dia:** 5832 h
- **Atmosfera:** CO2 com nuvens de ácido sulfúrico (92x a pressão da Terra) · **Respirável:** não
- **Perigos:** calor_extremo, acido, pressao, sem_oxigenio
- **Terreno:** sólido, altura média 64; montanhas em 12% do mapa; crateras (4% a 12 blocos); cavernas/tubos; cânions; lava no nível 54
- **Biomas:** `terras_altas_metalicas`, `planicies_sulfurosas`, `planicies_basalticas`
- **Minérios/manchas:** enxofre (yellow concrete), magma (magma block), geada_metalica (raw copper block), ouro (gold ore)
- **Criaturas:** magma cube, blaze

### Planeta Miller  (`sistemasolar:miller`)

Oceano raso e sem fim sob gravidade enorme, com ilhas de rocha raras. (Ondas gigantes e dilatação do tempo ficam para a fase de Java.)

- **Gravidade:** 1.3 g · **Temperatura média:** 25 °C · **Dia:** n/d
- **Atmosfera:** respirável, muito úmida · **Respirável:** sim
- **Perigos:** ondas_gigantes, dilatacao_do_tempo
- **Terreno:** sólido, altura média 61; montanhas em 4% do mapa; água no nível 63
- **Biomas:** `ilhas_de_rocha`, `bancos_de_areia`, `leito_de_cascalho`
- **Minérios/manchas:** prismarina (prismarine), argila (clay), ferro (iron ore)
- **Criaturas:** squid, cod, drowned

### Netuno  (`sistemasolar:netuno`)

Mundo de gelo azul sob um crepúsculo eterno, com picos de gelo, tempestades escuras e diamantes presos no gelo (a 'chuva de diamantes' de Netuno).

- **Gravidade:** 1.14 g · **Temperatura média:** -214 °C · **Dia:** 16.1 h
- **Atmosfera:** H2, He e metano; ventos de até 2100 km/h · **Respirável:** não
- **Perigos:** frio_extremo, ventos, sem_oxigenio
- **Terreno:** sólido, altura média 80; montanhas em 18% do mapa; crateras (6% a 12 blocos); cavernas/tubos; cânions
- **Biomas:** `picos_de_gelo`, `planicies_de_gelo`, `grande_mancha_escura`
- **Minérios/manchas:** diamante (diamond ore), gelo_azul (blue ice), lazuli (lapis ore)
- **Criaturas:** stray

### Saturno  (`sistemasolar:saturno`)

Gigante gasoso dourado: ilhas de nuvem flutuando em três camadas, um mar dourado lá embaixo e um anel de blocos de gelo no alto.

- **Gravidade:** 1.07 g · **Temperatura média:** -178 °C · **Dia:** 10.7 h
- **Atmosfera:** H2 e He (sem superfície sólida) · **Respirável:** não
- **Perigos:** queda_no_vazio, frio, sem_oxigenio
- **Terreno:** camadas flutuantes — y 64–100; y 112–146; y 156–186; y 200–206
- **Biomas:** `nuvens_douradas`, `hexagono_polar`
- **Minérios/manchas:** chuva_de_diamantes (diamond ore), gelo_de_amonia (packed ice)
- **Criaturas:** ghast

### Júpiter  (`sistemasolar:jupiter`)

Gigante de tempestades: ilhas de nuvem listradas em três altitudes, a Grande Mancha Vermelha e um oceano de lava (hidrogênio metálico) lá embaixo.

- **Gravidade:** 2.53 g · **Temperatura média:** -145 °C · **Dia:** 9.9 h
- **Atmosfera:** H2 e He (sem superfície sólida) · **Respirável:** não
- **Perigos:** queda_na_lava, raios, radiacao, sem_oxigenio
- **Terreno:** camadas flutuantes — y 60–96; y 108–146; y 158–190
- **Biomas:** `faixas_equatoriais`, `grande_mancha_vermelha`
- **Minérios/manchas:** chuva_de_diamantes (diamond ore)
- **Criaturas:** ghast

## Planetas anões

### Plutão  (`sistemasolar:plutao`)

Planície branca de gelo de nitrogênio em forma de coração, terras escuras de tolinas e montanhas de gelo de água, sob um céu escuro.

- **Gravidade:** 0.063 g · **Temperatura média:** -229 °C · **Dia:** 153.3 h
- **Atmosfera:** N2 quase inexistente · **Respirável:** não
- **Perigos:** frio_extremo, sem_oxigenio
- **Terreno:** sólido, altura média 68; montanhas em 10% do mapa; planícies achatadas em 30%; crateras (5% a 7 blocos); cavernas/tubos
- **Biomas:** `coracao_tombaugh`, `terra_escura_cthulhu`, `montanhas_de_gelo`
- **Minérios/manchas:** gelo_de_metano (blue ice), tolinas (red terracotta), ferro (iron ore)
- **Criaturas:** stray

### Ceres  (`sistemasolar:ceres`)

Rocha escura toda cravada de crateras, com manchas brilhantes de sal (Occator) e um criovulcão solitário (Ahuna Mons).

- **Gravidade:** 0.029 g · **Temperatura média:** -105 °C · **Dia:** 9.07 h
- **Atmosfera:** nenhuma · **Respirável:** não
- **Perigos:** vacuo, frio
- **Terreno:** sólido, altura média 70; montanhas em 4% do mapa; crateras (16% a 18 blocos, 16% a 8 blocos, 12% a 4 blocos); cavernas/tubos
- **Biomas:** `criovulcao`, `faculas_de_sal`, `terreno_escuro`
- **Minérios/manchas:** sal (calcite), gelo (packed ice), carbono (coal ore)
- **Criaturas:** enderman

### Haumea  (`sistemasolar:haumea`)

Gelo cristalino branco com uma mancha vermelha escura e um anel de gelo flutuando no alto. Gira tão rápido que o dia dura menos de 4 horas.

- **Gravidade:** 0.044 g · **Temperatura média:** -241 °C · **Dia:** 3.9 h
- **Atmosfera:** nenhuma · **Respirável:** não
- **Perigos:** vacuo, frio_extremo
- **Terreno:** sólido, altura média 70; montanhas em 8% do mapa; crateras (6% a 8 blocos); cavernas/tubos
- **Biomas:** `planicies_cristalinas`, `mancha_vermelha_escura`, `picos_cristalinos`
- **Minérios/manchas:** cristais (amethyst block), gelo_azul (blue ice)
- **Criaturas:** stray

### Sedna  (`sistemasolar:sedna`)

Mundo vermelho-sangue de tolinas e gelo, quase sem luz, no limite do Sistema Solar. O Sol é só uma estrela entre as outras.

- **Gravidade:** 0.03 g · **Temperatura média:** -261 °C · **Dia:** 10 h
- **Atmosfera:** nenhuma · **Respirável:** não
- **Perigos:** vacuo, frio_extremo
- **Terreno:** sólido, altura média 70; montanhas em 10% do mapa; crateras (6% a 8 blocos); cavernas/tubos
- **Biomas:** `picos_gelados`, `planicies_avermelhadas`, `geada_escura`
- **Minérios/manchas:** gelo (packed ice), hidrocarbonetos (coal ore), tolinas (red terracotta)
- **Criaturas:** stray, enderman

## Luas

### Lua  (`sistemasolar:lua`)

Cinza e sem ar: mares de basalto escuro, terras altas claras, crateras de todos os tamanhos e a Terra no céu preto.

- **Gravidade:** 0.165 g · **Temperatura média:** -53 °C · **Dia:** 655.7 h
- **Atmosfera:** nenhuma · **Respirável:** não
- **Perigos:** vacuo, frio
- **Terreno:** sólido, altura média 70; montanhas em 12% do mapa; planícies achatadas em 28%; crateras (12% a 17 blocos, 14% a 9 blocos, 12% a 4 blocos); cavernas/tubos
- **Biomas:** `mares_basalticos`, `planicies_de_regolito`, `terras_altas`
- **Minérios/manchas:** ilmenita (iron ore), helio_3 (amethyst block), gelo_polar (packed ice)
- **Criaturas:** enderman

### Titã  (`sistemasolar:titan`)

Lua laranja de névoa espessa, dunas escuras de hidrocarbonetos e lagos de metano (a água do jogo ganha a cor do metano).

- **Gravidade:** 0.138 g · **Temperatura média:** -179 °C · **Dia:** 382.7 h
- **Atmosfera:** N2 densa (1,45x a pressão da Terra), sem O2 · **Respirável:** não
- **Perigos:** frio, sem_oxigenio
- **Terreno:** sólido, altura média 66; montanhas em 8% do mapa; crateras (3% a 5 blocos); água no nível 62
- **Biomas:** `montes_de_gelo`, `dunas_de_hidrocarbonetos`, `planicies_alaranjadas`
- **Minérios/manchas:** gelo_de_agua (packed ice), hidrocarbonetos (coal ore), tolinas (clay)
- **Criaturas:** stray, slime

### Europa  (`sistemasolar:europa`)

Crosta de gelo riscada de rachaduras marrons, com um oceano de água líquida escondido por baixo e fontes hidrotermais no fundo.

- **Gravidade:** 0.134 g · **Temperatura média:** -160 °C · **Dia:** 85.2 h
- **Atmosfera:** oxigênio quase inexistente · **Respirável:** não
- **Perigos:** frio, sem_oxigenio, radiacao
- **Terreno:** camadas flutuantes — y -200–16; y 56–84
- **Biomas:** `crosta_estriada`, `terreno_caotico`, `planicie_branca`
- **Minérios/manchas:** sais_marrons (brown terracotta), fontes_hidrotermais (magma block), ferro_do_fundo (iron ore)
- **Criaturas:** squid, glow squid

### Io  (`sistemasolar:io`)

O mundo mais vulcânico: planícies de enxofre amarelo, patera (crateras) cheias de lava, vulcões e rios de magma.

- **Gravidade:** 0.183 g · **Temperatura média:** -143 °C · **Dia:** 42.5 h
- **Atmosfera:** dióxido de enxofre rarefeito · **Respirável:** não
- **Perigos:** lava, radiacao, sem_oxigenio
- **Terreno:** sólido, altura média 66; montanhas em 10% do mapa; crateras (9% a 19 blocos, 8% a 11 blocos); cavernas/tubos; cânions; lava no nível 58
- **Biomas:** `vulcoes`, `planicies_de_enxofre`, `campos_de_cinza`
- **Minérios/manchas:** enxofre (yellow concrete), magma (magma block), obsidiana (obsidian), ouro (gold ore), quartzo (nether quartz ore)
- **Criaturas:** magma cube, blaze, strider
