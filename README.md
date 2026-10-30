# Mod Sistema Solar — Forge 1.20.1

Projeto colaborativo com Claude. O mod cria dimensões próprias e localizadores para viajar entre os corpos celestes.

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

O traje espacial completo protege contra a falta de ar. O peitoral começa sem oxigênio; use um cilindro de oxigênio com ele equipado para recarregá-lo. O foguete interplanetário é reutilizável: agache e clique com o botão direito para escolher o destino, depois clique com o botão direito para lançar. Os itens também têm receitas de fabricação.

## Desenvolvimento

- Minecraft 1.20.1
- Forge 47.4.28
- Java 17
- ForgeGradle 6

Abra o projeto no IntelliJ IDEA ou Eclipse e execute a tarefa Gradle `build` para gerar o mod em `build/libs`.
