"""Dados dos 14 corpos celestes do mod Sistema Solar (Forge 1.20.1).

Para mexer num corpo basta editar a entrada aqui e rodar:
    python3 tools/gerar_dimensoes.py
Os JSON do jogo são gerados a partir deste arquivo (nunca edite os JSON à mão).

LEGENDA
  fisica      dados que o código Java vai usar depois (gravidade, ar, dano ambiental...)
  terreno     modo "solido" (terreno normal) ou "camadas" (ilhas flutuantes / crosta de gelo)
    base_y    altura média do terreno         H     meia-altura da transição (maior = mais suave)
    amp       relevo (0..1, em unidades de densidade; 1 unidade = H blocos)
    xz        escala do relevo (maior = morros menores)
    planicie  fração do mapa (0..1) que vira planície achatada (maria, coração de Plutão)
    montanhas (força, fração do mapa)
    crateras  lista de {ruido, xz, cob (fração do mapa), prof (densidade; blocos = prof*H)}
    cavernas / canions   probabilidade por chunk dos carvers (0 desliga)
  biomas      caixas disjuntas em percentis: t=temperatura, h=umidade, c=região (c alto = montanhas)
  features    manchas/minérios: y=(min,max) absoluto ou ("rel", min, max) relativo ao base_y
  mobs        categoria -> [(entidade, peso, mín, máx)]
  prob_criaturas  (opcional) creature_spawn_probability dos biomas do corpo (padrão do jogo: 0.1)
"""


def bioma(nome, topo, sub, t=(0, 1), h=(0, 1), c=(0, 1), **extra):
    return dict(nome=nome, topo=topo, sub=sub, t=t, h=h, c=c, **extra)


def feat(nome, bloco, tam, qtd, y, **extra):
    return dict(nome=nome, bloco=bloco, tam=tam, qtd=qtd, y=y, **extra)


def mob(entidade, peso, minimo=1, maximo=1):
    return (f"minecraft:{entidade}", peso, minimo, maximo)


M = "minecraft:"

CORPOS = {
    # ------------------------------------------------------------------ PLANETAS
    "marte": dict(
        nome="Marte", tipo="planeta",
        descricao="Deserto vermelho de poeira e ferro oxidado, com cânions gigantes, "
                  "vulcões enormes e gelo nos polos.",
        fisica=dict(gravidade_g=0.38, temperatura_c=-63, dia_horas=24.6,
                    atmosfera="CO2 muito rarefeita (1% da pressão da Terra)",
                    respiravel=False, perigos=["frio", "sem_oxigenio"]),
        dimensao=dict(luz_ambiente=0.0, tempo_fixo=None, quente=False, temp_bioma=0.8),
        cores=("#C98B5E", "#D9A07A", "#7A5C4A", "#4A3A30"),
        terreno=dict(modo="solido", default=M + "red_sandstone", base_y=72, H=48,
                     amp=0.45, xz=3.0, reg_xz=1.3, montanhas=(0.45, 0.14),
                     crateras=[dict(ruido="minecraft:ridge", xz=2.0, cob=0.10, prof=0.30),
                               dict(ruido="minecraft:surface", xz=2.5, cob=0.12, prof=0.18)],
                     fluido="water", nivel_mar=-64, cavernas=0.05, canions=0.035),
        biomas=[
            bioma("calotas_polares", M + "snow_block", M + "packed_ice", t=(0, 0.10)),
            bioma("montes_vulcanicos", M + "red_terracotta", M + "terracotta",
                  t=(0.10, 1), c=(0.86, 1)),
            bioma("planicies_escuras", M + "smooth_basalt", M + "basalt",
                  t=(0.10, 1), h=(0.62, 1), c=(0, 0.86)),
            bioma("planicies_de_poeira", M + "red_sand", M + "red_sandstone",
                  t=(0.10, 1), h=(0, 0.62), c=(0, 0.86)),
        ],
        features=[
            feat("ferro_oxidado", M + "raw_iron_block", 10, 8, ("rel", -20, 10)),
            feat("mirtilos_de_hematita", M + "blue_terracotta", 4, 14, ("rel", -6, 4),
                 biomas=["planicies_de_poeira"]),
            feat("gelo_subterraneo", M + "packed_ice", 14, 5, (-20, 50)),
            feat("ferro", M + "iron_ore", 9, 14, (-40, 60)),
            feat("cobre", M + "copper_ore", 9, 8, (-30, 60)),
        ],
        mobs=dict(monster=[mob("husk", 30, 2, 4)]),
    ),

    "venus": dict(
        nome="Vênus", tipo="planeta",
        descricao="Inferno de basalto e lava sob uma névoa amarela de ácido sulfúrico. "
                  "O calor é extremo e a água evapora.",
        fisica=dict(gravidade_g=0.90, temperatura_c=464, dia_horas=5832,
                    atmosfera="CO2 com nuvens de ácido sulfúrico (92x a pressão da Terra)",
                    respiravel=False, perigos=["calor_extremo", "acido", "pressao", "sem_oxigenio"]),
        dimensao=dict(luz_ambiente=0.1, tempo_fixo=6000, quente=True, temp_bioma=2.0),
        cores=("#D8B24A", "#E3C770", "#7A5A2A", "#4A3515"),
        terreno=dict(modo="solido", default=M + "basalt", base_y=64, H=48,
                     amp=0.45, xz=3.0, reg_xz=1.3, montanhas=(0.50, 0.12),
                     crateras=[dict(ruido="minecraft:surface", xz=2.5, cob=0.04, prof=0.25)],
                     fluido="lava", nivel_mar=54, cavernas=0.06, canions=0.01),
        biomas=[
            bioma("terras_altas_metalicas", M + "deepslate", M + "blackstone", c=(0.88, 1)),
            bioma("planicies_sulfurosas", M + "yellow_terracotta", M + "basalt",
                  h=(0.55, 1), c=(0, 0.88)),
            bioma("planicies_basalticas", M + "basalt", M + "blackstone",
                  h=(0, 0.55), c=(0, 0.88)),
        ],
        features=[
            feat("enxofre", M + "yellow_concrete", 14, 8, ("rel", -8, 6)),
            feat("magma", M + "magma_block", 8, 6, ("rel", -10, 4)),
            feat("geada_metalica", M + "raw_copper_block", 6, 6, ("rel", -6, 6),
                 biomas=["terras_altas_metalicas"]),
            feat("ouro", M + "gold_ore", 9, 6, (-60, 40)),
        ],
        mobs=dict(monster=[mob("magma_cube", 30, 1, 3), mob("blaze", 4, 1, 2)]),
    ),

    "miller": dict(
        nome="Planeta Miller", tipo="planeta",
        descricao="Oceano raso e sem fim sob gravidade enorme, com ilhas de rocha raras. "
                  "(Ondas gigantes e dilatação do tempo ficam para a fase de Java.)",
        fisica=dict(gravidade_g=1.30, temperatura_c=25, dia_horas=None,
                    atmosfera="respirável, muito úmida", respiravel=True,
                    perigos=["ondas_gigantes", "dilatacao_do_tempo"],
                    dilatacao_tempo="1 hora aqui = 7 anos fora (a implementar)"),
        dimensao=dict(luz_ambiente=0.0, tempo_fixo=None, quente=False, temp_bioma=0.6),
        cores=("#7FA8C9", "#A9C4D9", "#2E6F8E", "#154256"),
        terreno=dict(modo="solido", default=M + "stone", base_y=61, H=30,
                     amp=0.20, xz=3.0, reg_xz=1.6, montanhas=(0.25, 0.04),
                     crateras=[], fluido="water", nivel_mar=63, cavernas=0, canions=0),
        biomas=[
            bioma("ilhas_de_rocha", M + "granite", M + "stone", c=(0.96, 1), chuva=True),
            bioma("bancos_de_areia", M + "sand", M + "sandstone", h=(0, 0.5), c=(0, 0.96),
                  chuva=True),
            bioma("leito_de_cascalho", M + "gravel", M + "stone", h=(0.5, 1), c=(0, 0.96),
                  chuva=True),
        ],
        features=[
            feat("prismarina", M + "prismarine", 10, 6, ("rel", -6, 3)),
            feat("argila", M + "clay", 12, 6, ("rel", -4, 2)),
            feat("ferro", M + "iron_ore", 9, 10, (-40, 50)),
        ],
        mobs=dict(water_creature=[mob("squid", 10, 1, 3)],
                  water_ambient=[mob("cod", 15, 3, 6)],
                  monster=[mob("drowned", 40, 1, 3)]),
    ),

    "netuno": dict(
        nome="Netuno", tipo="planeta",
        descricao="Mundo de gelo azul sob um crepúsculo eterno, com picos de gelo, tempestades "
                  "escuras e diamantes presos no gelo (a 'chuva de diamantes' de Netuno).",
        fisica=dict(gravidade_g=1.14, temperatura_c=-214, dia_horas=16.1,
                    atmosfera="H2, He e metano; ventos de até 2100 km/h",
                    respiravel=False, perigos=["frio_extremo", "ventos", "sem_oxigenio"]),
        dimensao=dict(luz_ambiente=0.05, tempo_fixo=13000, quente=False, temp_bioma=-0.5),
        cores=("#3F6FD8", "#6C93E6", "#2A56B8", "#12295C"),
        terreno=dict(modo="solido", default=M + "packed_ice", base_y=80, H=48,
                     amp=0.50, xz=3.5, reg_xz=1.3, montanhas=(0.50, 0.18),
                     crateras=[dict(ruido="minecraft:ridge", xz=2.0, cob=0.06, prof=0.25)],
                     fluido="water", nivel_mar=-64, cavernas=0.08, canions=0.02),
        biomas=[
            bioma("picos_de_gelo", M + "blue_ice", M + "packed_ice", c=(0.82, 1), chuva=True),
            bioma("planicies_de_gelo", M + "snow_block", M + "packed_ice",
                  h=(0, 0.55), c=(0, 0.82), chuva=True),
            bioma("grande_mancha_escura", M + "blue_terracotta", M + "packed_ice",
                  h=(0.55, 1), c=(0, 0.82), chuva=True),
        ],
        features=[
            feat("diamante", M + "diamond_ore", 5, 5, (-50, 60)),
            feat("gelo_azul", M + "blue_ice", 20, 6, ("rel", -15, 10)),
            feat("lazuli", M + "lapis_ore", 8, 6, (-40, 60)),
        ],
        mobs=dict(monster=[mob("stray", 60, 2, 4)]),
    ),

    "saturno": dict(
        nome="Saturno", tipo="planeta",
        descricao="Gigante gasoso dourado: ilhas de nuvem flutuando em três camadas, um mar "
                  "dourado lá embaixo e um anel de blocos de gelo no alto.",
        fisica=dict(gravidade_g=1.07, temperatura_c=-178, dia_horas=10.7,
                    atmosfera="H2 e He (sem superfície sólida)",
                    respiravel=False, perigos=["queda_no_vazio", "frio", "sem_oxigenio"]),
        dimensao=dict(luz_ambiente=0.1, tempo_fixo=None, quente=False, temp_bioma=0.3),
        cores=("#E0C48A", "#EAD7A8", "#C9A24E", "#7A5F22"),
        terreno=dict(
            modo="camadas", default=M + "yellow_terracotta", fluido="water", nivel_mar=24,
            camadas=[
                dict(y=(64, 100), cob=0.50, k=1.4, xz=2.6, ys=2.0),
                dict(y=(112, 146), cob=0.42, k=1.4, xz=2.6, ys=2.0),
                dict(y=(156, 186), cob=0.34, k=1.4, xz=2.6, ys=2.0),
                dict(y=(200, 206), cob=0.12, k=2.0, xz=5.0, ys=5.0, rampa=3),  # anel
            ],
            clima_xz=2.2, reg_xz=1.4, cavernas=0, canions=0),
        biomas=[
            bioma("nuvens_douradas", M + "yellow_terracotta", M + "yellow_terracotta",
                  c=(0, 0.85),
                  faixas=[(198, M + "packed_ice"), (180, M + "white_terracotta"),
                          (168, M + "yellow_terracotta"), (156, M + "smooth_sandstone"),
                          (136, M + "light_gray_terracotta"), (126, M + "yellow_terracotta"),
                          (116, M + "white_terracotta"), (100, M + "orange_terracotta"),
                          (90, M + "brown_terracotta"), (82, M + "yellow_terracotta"),
                          (72, M + "smooth_sandstone"), (-64, M + "cut_sandstone")]),
            bioma("hexagono_polar", M + "light_blue_terracotta", M + "cyan_terracotta",
                  c=(0.85, 1),
                  faixas=[(198, M + "packed_ice"), (150, M + "light_blue_terracotta"),
                          (100, M + "cyan_terracotta"), (-64, M + "blue_terracotta")]),
        ],
        features=[
            feat("chuva_de_diamantes", M + "diamond_ore", 3, 3, (60, 190)),
            feat("gelo_de_amonia", M + "packed_ice", 8, 10, (70, 190)),
        ],
        mobs=dict(monster=[mob("ghast", 4, 1, 1)]),
    ),

    "jupiter": dict(
        nome="Júpiter", tipo="planeta",
        descricao="Gigante de tempestades: ilhas de nuvem listradas em três altitudes, a Grande "
                  "Mancha Vermelha e um oceano de lava (hidrogênio metálico) lá embaixo.",
        fisica=dict(gravidade_g=2.53, temperatura_c=-145, dia_horas=9.9,
                    atmosfera="H2 e He (sem superfície sólida)",
                    respiravel=False, perigos=["queda_na_lava", "raios", "radiacao", "sem_oxigenio"]),
        dimensao=dict(luz_ambiente=0.1, tempo_fixo=None, quente=False, temp_bioma=0.5),
        cores=("#D8B890", "#E6CFA8", "#8A5A2A", "#4A2E12"),
        terreno=dict(
            modo="camadas", default=M + "orange_terracotta", fluido="lava", nivel_mar=30,
            camadas=[
                dict(y=(60, 96), cob=0.55, k=1.5, xz=2.4, ys=2.0),
                dict(y=(108, 146), cob=0.48, k=1.5, xz=2.4, ys=2.0),
                dict(y=(158, 190), cob=0.40, k=1.5, xz=2.4, ys=2.0),
            ],
            clima_xz=2.2, reg_xz=1.4, cavernas=0, canions=0),
        biomas=[
            bioma("faixas_equatoriais", M + "orange_terracotta", M + "orange_terracotta",
                  c=(0, 0.88),
                  faixas=[(180, M + "white_terracotta"), (168, M + "yellow_terracotta"),
                          (158, M + "smooth_sandstone"), (140, M + "white_terracotta"),
                          (128, M + "orange_terracotta"), (116, M + "brown_terracotta"),
                          (100, M + "terracotta"), (90, M + "white_terracotta"),
                          (80, M + "orange_terracotta"), (70, M + "red_terracotta"),
                          (-64, M + "brown_terracotta")]),
            bioma("grande_mancha_vermelha", M + "red_terracotta", M + "red_terracotta",
                  c=(0.88, 1),
                  faixas=[(180, M + "red_terracotta"), (150, M + "orange_terracotta"),
                          (100, M + "red_terracotta"), (-64, M + "brown_terracotta")]),
        ],
        features=[
            feat("chuva_de_diamantes", M + "diamond_ore", 3, 3, (60, 190)),
        ],
        mobs=dict(monster=[mob("ghast", 8, 1, 1)]),
    ),

    # ------------------------------------------------------------ PLANETAS ANÕES
    "plutao": dict(
        nome="Plutão", tipo="anao",
        descricao="Crosta de gelo de nitrogênio com a região em forma de coração, terras escuras "
                  "de tolinas e montanhas de gelo, sob um céu escuro. Debaixo da crosta de gelo "
                  "há oceanos de água líquida. Na superfície crescem árvores de cristal e vivem "
                  "precursores e robôs (spawns e árvores vêm do mod Netherite Supremo).",
        fisica=dict(gravidade_g=0.063, temperatura_c=-229, dia_horas=153.3,
                    atmosfera="N2 quase inexistente", respiravel=False,
                    perigos=["frio_extremo", "sem_oxigenio"]),
        dimensao=dict(luz_ambiente=0.05, tempo_fixo=18000, quente=False, temp_bioma=-1.0),
        cores=("#05060A", "#10131C", "#3A4A6A", "#1B2538"),
        terreno=dict(
            modo="camadas", default=M + "packed_ice", fluido="water", nivel_mar=60,
            camadas=[
                dict(y=(-200, 14), rampa=14, relevo=0.8, xz=3.0),    # fundo rochoso do oceano
                dict(y=(56, 86), rampa=8, relevo=1.0, xz=2.6),       # crosta de gelo
            ],
            piso=dict(abaixo_de=40, topo=M + "stone", sub=M + "deepslate"),
            clima_xz=2.2, reg_xz=1.4, cavernas=0.02, canions=0),
        biomas=[
            bioma("coracao_tombaugh", M + "snow_block", M + "calcite", c=(0, 0.30)),
            bioma("terra_escura_cthulhu", M + "brown_terracotta", M + "terracotta",
                  c=(0.30, 0.90)),
            bioma("montanhas_de_gelo", M + "packed_ice", M + "stone", c=(0.90, 1)),
        ],
        features=[
            feat("gelo_de_metano", M + "blue_ice", 12, 6, (62, 86)),
            feat("tolinas", M + "red_terracotta", 8, 6, (70, 86),
                 biomas=["terra_escura_cthulhu"]),
            feat("ferro", M + "iron_ore", 9, 8, (0, 14),
                 alvo=[M + "stone", M + "deepslate"]),
        ],
        prob_criaturas=0.2,
        mobs=dict(monster=[mob("stray", 40, 1, 3)],
                  water_creature=[mob("squid", 10, 1, 3)],
                  underground_water_creature=[mob("glow_squid", 20, 2, 4)]),
    ),

    "ceres": dict(
        nome="Ceres", tipo="anao",
        descricao="Rocha escura toda cravada de crateras, com manchas brilhantes de sal "
                  "(Occator) e um criovulcão solitário (Ahuna Mons).",
        fisica=dict(gravidade_g=0.029, temperatura_c=-105, dia_horas=9.07,
                    atmosfera="nenhuma", respiravel=False, perigos=["vacuo", "frio"]),
        dimensao=dict(luz_ambiente=0.05, tempo_fixo=6000, quente=False, temp_bioma=-0.3),
        cores=("#050505", "#101010", "#3A3F4A", "#1F2229"),
        terreno=dict(modo="solido", default=M + "deepslate", base_y=70, H=40,
                     amp=0.40, xz=3.2, reg_xz=1.4, montanhas=(0.50, 0.04),
                     crateras=[dict(ruido="minecraft:ridge", xz=1.5, cob=0.16, prof=0.45),
                               dict(ruido="minecraft:surface", xz=2.6, cob=0.16, prof=0.22),
                               dict(ruido="minecraft:ice", xz=0.6, cob=0.12, prof=0.12)],
                     fluido="water", nivel_mar=-64, cavernas=0.03, canions=0),
        biomas=[
            bioma("criovulcao", M + "calcite", M + "tuff", c=(0.96, 1)),
            bioma("faculas_de_sal", M + "smooth_quartz", M + "calcite",
                  h=(0.93, 1), c=(0, 0.96)),
            bioma("terreno_escuro", M + "tuff", M + "deepslate", h=(0, 0.93), c=(0, 0.96)),
        ],
        features=[
            feat("sal", M + "calcite", 10, 8, ("rel", -8, 4)),
            feat("gelo", M + "packed_ice", 10, 5, ("rel", -20, 0)),
            feat("carbono", M + "coal_ore", 12, 10, (-40, 60)),
        ],
        mobs=dict(monster=[mob("enderman", 10, 1, 2)]),
    ),

    "haumea": dict(
        nome="Haumea", tipo="anao",
        descricao="Gelo cristalino branco com uma mancha vermelha escura e um anel de gelo "
                  "flutuando no alto. Gira tão rápido que o dia dura menos de 4 horas.",
        fisica=dict(gravidade_g=0.044, temperatura_c=-241, dia_horas=3.9,
                    atmosfera="nenhuma", respiravel=False, perigos=["vacuo", "frio_extremo"],
                    luas=["Hi'iaka", "Namaka"]),
        dimensao=dict(luz_ambiente=0.05, tempo_fixo=6000, quente=False, temp_bioma=-1.0),
        cores=("#020203", "#0B0D12", "#3A5A7A", "#1B2D3E"),
        terreno=dict(modo="solido", default=M + "packed_ice", base_y=70, H=40,
                     amp=0.35, xz=3.5, reg_xz=1.4, montanhas=(0.40, 0.08),
                     crateras=[dict(ruido="minecraft:surface", xz=2.5, cob=0.06, prof=0.20)],
                     aneis=[dict(y=(150, 156), cob=0.07, k=2.0, xz=4.0, ys=4.0, rampa=3,
                                 bloco=M + "packed_ice")],
                     fluido="water", nivel_mar=-64, cavernas=0.03, canions=0),
        biomas=[
            bioma("planicies_cristalinas", M + "snow_block", M + "calcite",
                  h=(0, 0.80), c=(0, 0.92)),
            bioma("mancha_vermelha_escura", M + "red_terracotta", M + "terracotta",
                  h=(0.80, 1), c=(0, 0.92)),
            bioma("picos_cristalinos", M + "blue_ice", M + "packed_ice", c=(0.92, 1)),
        ],
        features=[
            feat("cristais", M + "amethyst_block", 5, 4, ("rel", -10, 4)),
            feat("gelo_azul", M + "blue_ice", 14, 6, ("rel", -12, 6)),
        ],
        mobs=dict(monster=[mob("stray", 30, 1, 3)]),
    ),

    "sedna": dict(
        nome="Sedna", tipo="anao",
        descricao="Mundo vermelho-sangue de tolinas e gelo, quase sem luz, no limite do Sistema "
                  "Solar. O Sol é só uma estrela entre as outras.",
        fisica=dict(gravidade_g=0.03, temperatura_c=-261, dia_horas=10.0,
                    atmosfera="nenhuma", respiravel=False, perigos=["vacuo", "frio_extremo"],
                    nota="massa e rotação estimadas"),
        dimensao=dict(luz_ambiente=0.0, tempo_fixo=18000, quente=False, temp_bioma=-1.0),
        cores=("#000000", "#0A0508", "#3A2430", "#1F1218"),
        terreno=dict(modo="solido", default=M + "packed_ice", base_y=70, H=44,
                     amp=0.35, xz=3.2, reg_xz=1.4, montanhas=(0.40, 0.10),
                     crateras=[dict(ruido="minecraft:surface", xz=2.5, cob=0.06, prof=0.20)],
                     fluido="water", nivel_mar=-64, cavernas=0.02, canions=0),
        biomas=[
            bioma("picos_gelados", M + "packed_ice", M + "stone", c=(0.90, 1)),
            bioma("planicies_avermelhadas", M + "red_terracotta", M + "terracotta",
                  h=(0, 0.60), c=(0, 0.90)),
            bioma("geada_escura", M + "brown_terracotta", M + "terracotta",
                  h=(0.60, 1), c=(0, 0.90)),
        ],
        features=[
            feat("gelo", M + "packed_ice", 14, 6, ("rel", -14, 4)),
            feat("hidrocarbonetos", M + "coal_ore", 10, 10, (-40, 60)),
            feat("tolinas", M + "red_terracotta", 10, 8, ("rel", -6, 2)),
        ],
        mobs=dict(monster=[mob("stray", 40, 1, 3), mob("enderman", 8, 1, 1)]),
    ),

    # ---------------------------------------------------------------------- LUAS
    "lua": dict(
        nome="Lua", tipo="lua", lua_de="Terra",
        descricao="Cinza e sem ar: mares de basalto escuro, terras altas claras, crateras de "
                  "todos os tamanhos e a Terra no céu preto.",
        fisica=dict(gravidade_g=0.165, temperatura_c=-53, dia_horas=655.7,
                    atmosfera="nenhuma", respiravel=False, perigos=["vacuo", "frio"]),
        dimensao=dict(luz_ambiente=0.1, tempo_fixo=6000, quente=False, temp_bioma=-0.2),
        cores=("#000000", "#0A0A0A", "#3A4A5A", "#202A33"),
        terreno=dict(modo="solido", default=M + "stone", base_y=70, H=44,
                     amp=0.35, xz=3.0, reg_xz=1.4, planicie=0.28, montanhas=(0.40, 0.12),
                     crateras=[dict(ruido="minecraft:ridge", xz=1.4, cob=0.12, prof=0.40),
                               dict(ruido="minecraft:surface", xz=2.4, cob=0.14, prof=0.22),
                               dict(ruido="minecraft:ice", xz=0.7, cob=0.12, prof=0.10)],
                     fluido="water", nivel_mar=-64, cavernas=0.04, canions=0),
        biomas=[
            bioma("mares_basalticos", M + "smooth_basalt", M + "basalt", c=(0, 0.28)),
            bioma("planicies_de_regolito", M + "andesite", M + "stone", c=(0.28, 0.88)),
            bioma("terras_altas", M + "diorite", M + "andesite", c=(0.88, 1)),
        ],
        features=[
            feat("ilmenita", M + "iron_ore", 8, 8, (-40, 60)),
            feat("helio_3", M + "amethyst_block", 5, 2, (-30, 60)),
            feat("gelo_polar", M + "packed_ice", 10, 4, ("rel", -25, -8)),
        ],
        mobs=dict(monster=[mob("enderman", 8, 1, 1)]),
    ),

    "titan": dict(
        nome="Titã", tipo="lua", lua_de="Saturno",
        descricao="Lua laranja de névoa espessa, dunas escuras de hidrocarbonetos e lagos de "
                  "metano (a água do jogo ganha a cor do metano).",
        fisica=dict(gravidade_g=0.138, temperatura_c=-179, dia_horas=382.7,
                    atmosfera="N2 densa (1,45x a pressão da Terra), sem O2",
                    respiravel=False, perigos=["frio", "sem_oxigenio"],
                    nota="ar tão denso que seria possível voar batendo asas (a implementar)"),
        dimensao=dict(luz_ambiente=0.05, tempo_fixo=None, quente=False, temp_bioma=0.4),
        cores=("#C4813A", "#D9A066", "#7A4A1E", "#3A2410"),
        terreno=dict(modo="solido", default=M + "packed_ice", base_y=66, H=36,
                     amp=0.35, xz=3.0, reg_xz=1.4, montanhas=(0.35, 0.08),
                     crateras=[dict(ruido="minecraft:surface", xz=2.5, cob=0.03, prof=0.15)],
                     fluido="water", nivel_mar=62, cavernas=0, canions=0, fundo=M + "mud"),
        biomas=[
            bioma("montes_de_gelo", M + "packed_ice", M + "stone", c=(0.92, 1)),
            bioma("dunas_de_hidrocarbonetos", M + "coarse_dirt", M + "brown_terracotta",
                  t=(0, 0.5), c=(0, 0.92)),
            bioma("planicies_alaranjadas", M + "orange_terracotta", M + "terracotta",
                  t=(0.5, 1), c=(0, 0.92), chuva=True),
        ],
        features=[
            feat("gelo_de_agua", M + "packed_ice", 12, 6, ("rel", -14, 2)),
            feat("hidrocarbonetos", M + "coal_ore", 14, 12, (-40, 60)),
            feat("tolinas", M + "clay", 10, 6, ("rel", -4, 2)),
        ],
        mobs=dict(monster=[mob("stray", 30, 1, 3), mob("slime", 10, 1, 2)]),
    ),

    "europa": dict(
        nome="Europa", tipo="lua", lua_de="Júpiter",
        descricao="Crosta de gelo riscada de rachaduras marrons, com um oceano de água líquida "
                  "escondido por baixo e fontes hidrotermais no fundo.",
        fisica=dict(gravidade_g=0.134, temperatura_c=-160, dia_horas=85.2,
                    atmosfera="oxigênio quase inexistente", respiravel=False,
                    perigos=["frio", "sem_oxigenio", "radiacao"]),
        dimensao=dict(luz_ambiente=0.05, tempo_fixo=6000, quente=False, temp_bioma=-0.8),
        cores=("#05070D", "#0B1020", "#1C4E80", "#0A2744"),
        terreno=dict(
            modo="camadas", default=M + "packed_ice", fluido="water", nivel_mar=60,
            camadas=[
                dict(y=(-200, 16), rampa=14, relevo=0.9, xz=3.0),    # fundo rochoso
                dict(y=(56, 84), rampa=8, relevo=1.2, xz=2.5),       # crosta de gelo
            ],
            piso=dict(abaixo_de=40, topo=M + "stone", sub=M + "deepslate"),
            clima_xz=2.2, reg_xz=1.4, cavernas=0.03, canions=0.04, canion_y=(40, 82)),
        biomas=[
            bioma("crosta_estriada", M + "packed_ice", M + "blue_ice", h=(0, 0.55),
                  listras=[dict(ruido="minecraft:surface", min=-0.025, max=0.025,
                                bloco=M + "brown_terracotta"),
                           dict(ruido="minecraft:ice", min=-0.02, max=0.02,
                                bloco=M + "red_terracotta")]),
            bioma("terreno_caotico", M + "blue_ice", M + "packed_ice", h=(0.55, 0.85)),
            bioma("planicie_branca", M + "snow_block", M + "packed_ice", h=(0.85, 1)),
        ],
        features=[
            feat("sais_marrons", M + "brown_terracotta", 10, 8, (70, 84),
                 alvo=[M + "packed_ice", M + "blue_ice", M + "snow_block"]),
            feat("fontes_hidrotermais", M + "magma_block", 6, 6, (4, 18),
                 alvo=[M + "stone", M + "deepslate"]),
            feat("ferro_do_fundo", M + "iron_ore", 9, 10, (0, 16),
                 alvo=[M + "stone", M + "deepslate"]),
        ],
        mobs=dict(water_creature=[mob("squid", 10, 1, 3)],
                  underground_water_creature=[mob("glow_squid", 20, 2, 4)]),
    ),

    "io": dict(
        nome="Io", tipo="lua", lua_de="Júpiter",
        descricao="O mundo mais vulcânico: planícies de enxofre amarelo, patera (crateras) "
                  "cheias de lava, vulcões e rios de magma.",
        fisica=dict(gravidade_g=0.183, temperatura_c=-143, dia_horas=42.5,
                    atmosfera="dióxido de enxofre rarefeito", respiravel=False,
                    perigos=["lava", "radiacao", "sem_oxigenio"]),
        dimensao=dict(luz_ambiente=0.1, tempo_fixo=None, quente=True, temp_bioma=2.0),
        cores=("#2A1F0A", "#5A4414", "#7A4A10", "#3A2008"),
        terreno=dict(modo="solido", default=M + "basalt", base_y=66, H=44,
                     amp=0.40, xz=3.0, reg_xz=1.3, montanhas=(0.50, 0.10),
                     crateras=[dict(ruido="minecraft:ridge", xz=1.8, cob=0.09, prof=0.45),
                               dict(ruido="minecraft:surface", xz=2.5, cob=0.08, prof=0.25)],
                     fluido="lava", nivel_mar=58, cavernas=0.07, canions=0.015),
        biomas=[
            bioma("vulcoes", M + "smooth_basalt", M + "blackstone", c=(0.90, 1)),
            bioma("planicies_de_enxofre", M + "yellow_terracotta", M + "basalt",
                  h=(0, 0.55), c=(0, 0.90)),
            bioma("campos_de_cinza", M + "blackstone", M + "basalt",
                  h=(0.55, 1), c=(0, 0.90)),
        ],
        features=[
            feat("enxofre", M + "yellow_concrete", 16, 10, ("rel", -8, 6)),
            feat("magma", M + "magma_block", 10, 8, ("rel", -8, 4)),
            feat("obsidiana", M + "obsidian", 6, 4, (40, 70)),
            feat("ouro", M + "gold_ore", 9, 6, (-60, 40)),
            feat("quartzo", M + "nether_quartz_ore", 10, 6, (-40, 60)),
        ],
        mobs=dict(monster=[mob("magma_cube", 30, 1, 3), mob("blaze", 6, 1, 2)],
                  creature=[mob("strider", 30, 1, 2)]),
    ),
}
