# 🏗️ 2.P · Proyecto: pedidos de una tienda en línea

| ⏱️ Duración | 🧪 Tipo | 🧱 Bloque | 🛠️ Stack |
|---|---|---|---|
| 4–6 h construyendo / 1 h revisando | 🏗️ `project` | Bloque 2 · Combinar y resumir | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Responder preguntas de negocio sobre cuatro tablas relacionadas usando todo lo del bloque 2: unir tablas (2.2), conservar las filas sin pareja y encontrar lo que falta (2.3), agrupar y resumir (2.4), filtrar grupos y sumar con varias tablas unidas (2.5) y subconsultas (2.6).
- Escribir una consulta que junta varias tablas y varias reglas sin que una deshaga a otra.
- Revisar un resultado con la cuenta a mano sobre los datos, antes de correr las pruebas.
- Comprobar tu trabajo contra un contrato fijo, como en una prueba técnica.
- **La pregunta del dominio:** ¿cuánto nos compró de verdad cada cliente?

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta de este proyecto. PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/02-combine-and-summarize/project-online-orders
```

Las pruebas se corren desde [`acceptance/`](acceptance/) (contra tus consultas) o desde [`reference/`](reference/) (contra la solución de referencia). Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🛣️ Dos formas de usar este proyecto
| Camino | Qué haces | Tiempo |
|---|---|---|
| 🔨 **Construir y comparar** | Lees [BRIEF.md](BRIEF.md), escribes tus seis consultas en `my-queries/`, corres `acceptance/` contra ellas y al final lees [REVIEW.md](REVIEW.md) | 4–6 h |
| 🔍 **Solo revisar** | Corres `reference/`, lees sus consultas guiado por [REVIEW.md](REVIEW.md), las rompes y discutes sus decisiones | 1 h |

**Te recomendamos construir.** En una prueba técnica de SQL te dan unas tablas relacionadas y preguntas como estas, y nadie te muestra la solución; este proyecto es el ensayo. Revisar solo sirve si ya resolviste los labs 2.2 a 2.6 con soltura y te falta tiempo.

### Construir: tus consultas y las pruebas
1. Lee [BRIEF.md](BRIEF.md) entero: las reglas del dominio, las tablas, los datos y el contrato.
2. Crea la carpeta `my-queries/` aquí, junto a `acceptance/` y `reference/` (en VS Code, o con este comando, igual en PowerShell y en Bash):

   ```bash
   mkdir my-queries
   ```

3. Crea en ella los seis archivos del contrato (`01_order_totals.sql` … `06_customers.sql`), cada uno con una sola consulta.
4. Corre las pruebas desde `acceptance/`:

   PowerShell o Bash:

   ```bash
   cd acceptance
   python -m pytest
   ```

   Con la carpeta vacía pasa 1 prueba (`TestSeed`, la guarda) y fallan 6, cada una con `no existe en …`. Para correr solo una pregunta: `python -m pytest -k task3`.

Trabaja en tu fork o en tu rama (`solutions/tu-nombre`, como dice el [README del repositorio](../../../README.md)), nunca en `master`. Si tus consultas están en otra carpeta, indícala con `--queries=` (con el `=` pegado; con un espacio, pytest no entiende la opción):

```bash
python -m pytest --queries=../otra-carpeta
```

### Revisar: correr la referencia
Desde `reference/`, sus pruebas corren las de `acceptance/` contra [`reference/queries/`](reference/queries/):

PowerShell o Bash:

```bash
cd reference
python -m pytest
```

Debe terminar con `1 passed`. Es una sola prueba porque corre todas las de `acceptance/` por dentro. Para verlas una por una, desde `acceptance/`: `python -m pytest -v --queries=../reference/queries`.

## 👥 Implementaciones de la comunidad
Todavía ninguna. Si resuelves el proyecto en tu fork, comparte el enlace con quien mantiene el curso (por ejemplo, en un issue): se enlaza aquí, no se copia.

## 🔁 Retrospectiva
- ¿Qué pregunta me costó más, y por qué regla del dominio?
- ¿Qué número revisé a mano antes de correr las pruebas, y cuál debí revisar?
- ¿Qué lab del bloque 2 debería repasar?
