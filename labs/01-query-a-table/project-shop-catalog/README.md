# 🏗️ 1.P · Proyecto: catálogo de una tienda

| ⏱️ Duración | 🧪 Tipo | 🧱 Bloque | 🛠️ Stack |
|---|---|---|---|
| 3–5 h construyendo / 1 h revisando | 🏗️ `project` | Bloque 1 · Consultar una tabla | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Responder preguntas de negocio sobre una tabla real, con datos que faltan y textos desordenados, usando todo lo del bloque 1: columnas calculadas (1.2), filtros (1.3), `NULL` (1.4), orden y páginas (1.5), textos, fechas y `CASE` (1.6).
- Escribir una consulta que junta varias reglas sin que una deshaga a otra.
- Comprobar tu trabajo contra un contrato fijo, como en una prueba técnica.
- **La pregunta del dominio:** ¿qué puede comprar hoy un cliente, y a qué precio?

## 📍 Dónde correr los comandos
Con el entorno virtual activo, desde la carpeta de este proyecto:

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/01-query-a-table/project-shop-catalog
```

Las pruebas se corren desde [`acceptance/`](acceptance/) (contra tus consultas) o desde [`reference/`](reference/) (contra la solución de referencia). Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🛣️ Dos formas de usar este proyecto
| Camino | Qué haces | Tiempo |
|---|---|---|
| 🔨 **Construir y comparar** | Lees [BRIEF.md](BRIEF.md), escribes tus seis consultas en `my-queries/`, corres `acceptance/` contra ellas y al final lees [REVIEW.md](REVIEW.md) | 3–5 h |
| 🔍 **Solo revisar** | Corres `reference/`, lees sus consultas guiado por [REVIEW.md](REVIEW.md), las rompes y discutes sus decisiones | 1 h |

**Te recomendamos construir.** En una prueba técnica de SQL te dan una tabla y preguntas como estas, y nadie te muestra la solución; este proyecto es el ensayo. Revisar solo sirve si ya resolviste los seis labs con soltura y te falta tiempo.

### Construir: tus consultas y las pruebas
1. Lee [BRIEF.md](BRIEF.md) entero: las reglas del dominio, los datos y el contrato.
2. Crea la carpeta `my-queries/` aquí, junto a `acceptance/` y `reference/` (en VS Code, o con este comando, igual en PowerShell y en Bash):

   ```bash
   mkdir my-queries
   ```

3. Crea en ella los seis archivos del contrato (`01_search.sql` … `06_catalog.sql`), cada uno con una sola consulta.
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
- ¿Qué lab del bloque 1 debería repasar?
- ¿Qué haría distinto si el catálogo tuviera diez mil productos?
