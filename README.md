# Mod Sistema Solar — Forge 1.20.1

Projeto colaborativo com Claude. O mod cria dimensões próprias, blocos de superfície exclusivos e viagens espaciais entre corpos celestes.

## Corpos

Marte, Vênus, Planeta Miller, Netuno, Plutão, Ceres, Lua, Saturno, Júpiter, Haumea, Sedna, Titã, Europa e Io. **Urano** é o planeta extra escolhido para este projeto.

## Convenções do projeto

- `modid`: `sistemasolar`
- Pacote Java: `com.sistemasolar`
- Dimensão: `sistemasolar:<id>`
- IDs em minúsculas e sem acentos
- Dimensões geradas com `python tools/gerar_dimensoes.py <id>`

## Jogar

Os localizadores estão na aba **Ferramentas e utilidades** do modo Criativo. Use o localizador do destino com o botão direito para viajar; o Localizador da Terra retorna ao mundo normal.

O traje espacial completo usa armadura metálica e mostra a reserva de oxigênio na interface. O peitoral começa sem oxigênio; use um cilindro para recarregá-lo. Uma carga dura 2 minutos.

O foguete interplanetário constrói uma plataforma e um foguete antes do lançamento. Agache e clique com o botão direito para escolher o destino. Use o foguete na superfície para entrar no espaço e use-o novamente no espaço para pousar no destino. Também é possível alcançar o espaço subindo acima de Y=256 com o traje e oxigênio.

Plutão possui cidades futuristas, Io tem vulcões ativos, e Europa e Plutão escondem bolsões de oceano sob o gelo com fauna aquática. Alienígenas aparecem em alguns mundos. No espaço há asteroides, uma nave abandonada e representações visíveis dos planetas.

## Desenvolvimento

- Minecraft 1.20.1
- Forge 47.4.28
- Java 17
- ForgeGradle 6

Abra o projeto no IntelliJ IDEA ou Eclipse e execute a tarefa Gradle `jar` para gerar o mod em `build/libs`.
