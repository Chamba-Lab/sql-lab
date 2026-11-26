# 🗺️ Sílabo · SQL con SQLite: de cero a listo para el trabajo

**Meta:** consultar, diseñar y cuidar bases de datos relacionales con SQL, al nivel que piden un primer trabajo y sus pruebas técnicas.
**Público:** sabes Python básico (funciones, listas, diccionarios, abrir archivos) y nunca usaste una base de datos, o solo hiciste algún `SELECT` suelto → puedes escribir consultas de reportes, diseñar un esquema y usar SQL desde una aplicación en Python de forma segura.
**Stack:** Python 3.12 o superior, con su módulo `sqlite3` (trae SQLite adentro: no instalas nada más) · pytest 9.2.0 para las pruebas. Los labs se verifican en Python 3.12 y 3.15.
**Sesiones:** 1–2 h por lab

**Leyenda**
- Estado: ⬜ `pending` sin construir · 🟨 `built` construido y verificado, esperando a un aprendiz · ✅ `done` resuelto por un aprendiz y con su feedback aplicado
- Tipo de tema: 🎯 `core` el camino · 🔬 `deep-dive` más a fondo · 🔀 `alternative` otra tecnología · ➕ `elective` opcional · 🆕 `modern` pone el camino al día
- Tipo de lab: 🧩 `challenge` starter + solución · 🔭 `exploration` demo guiada · 💭 `concept` sin código · 🏗️ `project` cierra el bloque

## El camino de un vistazo
| Bloque | Al terminar podrás… | Estado |
|---|---|---|
| 1 · Consultar una tabla | Sacar de una tabla justo los datos que te piden: elegir, filtrar, ordenar y transformar | ⬜ `pending` |
| 2 · Combinar y resumir | Cruzar varias tablas y resumirlas en totales, promedios y conteos | ⬜ `pending` |
| 3 · Diseñar y crear una base | Diseñar tablas que no se contradigan y cambiar datos sin romper nada | ⬜ `pending` |
| 4 · Consultas analíticas | Resolver las consultas de reportes y de pruebas técnicas: rankings, acumulados y tablas dinámicas | ⬜ `pending` |
| 5 · SQL en una aplicación | Usar SQL desde Python de forma rápida y segura | ⬜ `pending` |

En los retos escribes consultas en archivos `.sql`, y las pruebas del lab las ejecutan contra una base de datos de ejemplo. Si ya hiciste algún `SELECT`, los labs 1.2 y 1.3 te van a resultar rápidos; no te los saltes, porque cada uno trae una trampa que sale en las entrevistas.

## Bloque 1 · Consultar una tabla
Sacar de una tabla justo los datos que te piden: elegir, filtrar, ordenar y transformar.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 1.1 | [Tu primera base de datos](labs/01-query-a-table/01-first-database/README.md) | 🎯 `core` | 🔭 `exploration` | Abrir una base de datos, recorrer sus tablas, hacer tu primera consulta y explicar qué son una tabla, una fila y una columna | ✅ `done` |
| 1.2 | [Primeras consultas](labs/01-query-a-table/02-first-queries/README.md) | 🎯 `core` | 🧩 `challenge` | Elegir columnas, calcular valores nuevos y darles nombre; correr las pruebas del curso y leer un fallo | ✅ `done` |
| 1.3 | [Filtrar filas](labs/01-query-a-table/03-filter-rows/README.md) | 🎯 `core` | 🧩 `challenge` | Quedarte solo con las filas que cumplen una o varias condiciones | 🟨 `built` |
| 1.4 | [El valor NULL](labs/01-query-a-table/04-null-values/README.md) | 🎯 `core` | 🧩 `challenge` | Tratar los datos que faltan sin que te den resultados equivocados | 🟨 `built` |
| 1.5 | Ordenar y paginar | 🎯 `core` | 🧩 `challenge` | Ordenar resultados, quitar repetidos y mostrarlos por páginas | ⬜ `pending` |
| 1.6 | Transformar valores | 🎯 `core` | 🧩 `challenge` | Limpiar textos, trabajar con fechas y clasificar filas según reglas | ⬜ `pending` |
| 1.P | Proyecto: catálogo de una tienda | 🎯 `core` | 🏗️ `project` | Responder desde cero las preguntas del equipo de ventas sobre el catálogo de una tienda, con todo lo del bloque 1 | ⬜ `pending` |

## Bloque 2 · Combinar y resumir
Cruzar varias tablas y resumirlas en totales, promedios y conteos.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 2.1 | Relaciones entre tablas | 🎯 `core` | 🔭 `exploration` | Seguir cómo una tabla apunta a otra y explicar por qué los datos se reparten en varias tablas | ⬜ `pending` |
| 2.2 | Unir tablas | 🎯 `core` | 🧩 `challenge` | Juntar en un solo resultado los datos de dos o más tablas relacionadas | ⬜ `pending` |
| 2.3 | Filas sin pareja | 🎯 `core` | 🧩 `challenge` | Incluir también lo que no tiene pareja en la otra tabla y encontrar lo que falta | ⬜ `pending` |
| 2.4 | Agrupar y resumir | 🎯 `core` | 🧩 `challenge` | Calcular totales, promedios y conteos por grupo | ⬜ `pending` |
| 2.5 | Filtrar grupos y no inflar totales | 🎯 `core` | 🧩 `challenge` | Quedarte con los grupos que cumplen una condición y sumar bien después de unir tablas | ⬜ `pending` |
| 2.6 | Subconsultas | 🎯 `core` | 🧩 `challenge` | Usar el resultado de una consulta dentro de otra | ⬜ `pending` |
| 2.7 | Unir y restar resultados | ➕ `elective` | 🧩 `challenge` | Juntar, comparar y restar los resultados de dos consultas | ⬜ `pending` |
| 2.P | Proyecto: pedidos de una tienda en línea | 🎯 `core` | 🏗️ `project` | Analizar desde cero los clientes, pedidos y productos de una tienda en línea, con todo lo del bloque 2 | ⬜ `pending` |

## Bloque 3 · Diseñar y crear una base
Diseñar tablas que no se contradigan y cambiar datos sin romper nada.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 3.1 | Modelar datos y normalizar | 🎯 `core` | 💭 `concept` | Pasar de una hoja de cálculo a tablas bien repartidas y reconocer los datos repetidos que terminan contradiciéndose | ⬜ `pending` |
| 3.2 | Crear tablas y tipos | 🎯 `core` 🆕 `modern` | 🧩 `challenge` | Crear tablas con los tipos correctos y ver qué hace SQLite cuando un dato no calza | ⬜ `pending` |
| 3.3 | Restricciones | 🎯 `core` | 🧩 `challenge` | Hacer que la base rechace por sí sola los datos inválidos | ⬜ `pending` |
| 3.4 | Insertar, actualizar y borrar | 🎯 `core` 🆕 `modern` | 🧩 `challenge` | Agregar, cambiar y borrar datos sin tocar filas de más | ⬜ `pending` |
| 3.5 | Transacciones | 🎯 `core` | 🧩 `challenge` | Hacer que varios cambios ocurran todos juntos o ninguno | ⬜ `pending` |
| 3.6 | Cambiar el diseño de una tabla con datos | ➕ `elective` | 🧩 `challenge` | Agregar, renombrar o quitar columnas de una tabla que ya tiene datos, sin perderlos | ⬜ `pending` |
| 3.P | Proyecto: la hoja de cálculo de una biblioteca | 🎯 `core` | 🏗️ `project` | Convertir desde cero la hoja de cálculo de Excel de una biblioteca en una base bien diseñada, con sus reglas y sus datos | ⬜ `pending` |

## Bloque 4 · Consultas analíticas
Resolver las consultas de reportes y de pruebas técnicas: rankings, acumulados y tablas dinámicas.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 4.1 | Consultas por pasos | 🎯 `core` | 🧩 `challenge` | Escribir una consulta larga como una serie de pasos con nombre, fácil de leer y de corregir | ⬜ `pending` |
| 4.2 | Consultas recursivas | 🔬 `deep-dive` | 🧩 `challenge` | Recorrer jerarquías, como un organigrama o categorías dentro de categorías | ⬜ `pending` |
| 4.3 | Rankings y top N por grupo | 🎯 `core` | 🧩 `challenge` | Numerar y rankear filas dentro de cada grupo y sacar los primeros de cada uno | ⬜ `pending` |
| 4.4 | Acumulados y comparar con la fila anterior | 🎯 `core` | 🧩 `challenge` | Calcular totales acumulados, promedios móviles y la variación respecto al periodo anterior | ⬜ `pending` |
| 4.5 | Tablas dinámicas en SQL | 🎯 `core` | 🧩 `challenge` | Armar en SQL las tablas dinámicas que harías en Excel, con totales y porcentajes | ⬜ `pending` |
| 4.P | Proyecto: prueba técnica de una app de delivery | 🎯 `core` | 🏗️ `project` | Resolver desde cero, como en una prueba técnica, las preguntas de negocio sobre los datos de una app de delivery | ⬜ `pending` |

## Bloque 5 · SQL en una aplicación
Usar SQL desde Python de forma rápida y segura.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 5.1 | Cómo busca la base | 🎯 `core` | 🔭 `exploration` | Ver por qué una consulta es lenta, cómo un índice la acelera y qué cuesta tenerlo | ⬜ `pending` |
| 5.2 | Elegir índices | 🎯 `core` | 🧩 `challenge` | Elegir qué índices crear para unas consultas lentas y comprobar que la base los usa | ⬜ `pending` |
| 5.3 | SQL desde Python | 🎯 `core` | 🧩 `challenge` | Consultar y guardar datos desde un programa en Python, pasando los valores como parámetros | ⬜ `pending` |
| 5.4 | Inyección SQL | 🎯 `core` | 🧩 `challenge` | Mostrar cómo se ataca una consulta armada pegando texto, en tu propio código, y blindarla | ⬜ `pending` |
| 5.5 | Transacciones y errores desde Python | 🎯 `core` | 🧩 `challenge` | Guardar varios cambios de forma segura desde Python y reaccionar cuando la base rechaza uno | ⬜ `pending` |
| 5.P | Proyecto: reservas de una cancha deportiva | 🎯 `core` | 🏗️ `project` | Construir desde cero el sistema de reservas de una cancha en Python: su base, sus consultas y sus reglas, rápido y seguro | ⬜ `pending` |

## Reglas de diseño
1. **Los datos más pequeños que hacen visible el tema.** Cada lab trae su propia base de ejemplo, creada por un script del lab; ninguna base crece lab tras lab.
2. **Ninguna aplicación crece lab tras lab:** la integración ocurre en el proyecto del bloque, que no hereda nada de los labs.
3. **Cada tema tiene un único lab dueño**, que lo enseña. Los labs siguientes lo usan y enlazan a su dueño.
4. **Escribes SQL; las pruebas lo ejecutan.** En los bloques 1 a 4, cada tarea es un archivo `.sql` del starter con un `TODO`. Las pruebas lo corren contra una base nueva, creada desde los datos del lab, y comparan el resultado. En el bloque 5 escribes Python.
5. **Primero la idea, después SQL.** Cada bloque abre con la idea sin la sintaxis, y cada lab presenta el concepto antes de la consulta que lo escribe.
6. **Nivel de entrevista.** Cada lab tiene una trampa típica de las pruebas técnicas (NULL, totales inflados por un JOIN, empates en un ranking…) y cierra con una autoevaluación de preguntas de entrevista.
7. **SQL estándar primero.** Lo que se enseña funciona igual en PostgreSQL y MySQL salvo donde el lab lo avisa. Las particularidades de SQLite (tipos flexibles, fechas como texto, claves foráneas apagadas por defecto) se enseñan como trampas, no como la forma normal.
8. **Sin contenedores y sin instalar SQLite.** Todo corre con el `sqlite3` que trae Python. Un lab no usa nada que falte en SQLite 3.45, la versión más antigua medida en las instalaciones de Python revisadas (ver `docs/decisions.md`).
9. **Atacar solo tu propio código.** El lab 5.4 explota una inyección SQL únicamente contra la aplicación local del lab, y lo dice al empezar.

## Mapa de construcción
| ID | Owns | Builds on | Starts from |
|---|---|---|---|
| 1.1 | Relational model basics (database, table, row, column, type), SQL as a declarative language, `SELECT * FROM` as a first query, the `python -m sqlite3` shell, listing tables via `sqlite_schema` and columns via `pragma_table_info` | — | Minimal app: a small demo database built by a script (`demo/build_db.py` → `jobs.db`) |
| 1.2 | `SELECT … FROM` (select list), expressions, arithmetic operators and parentheses, `AS` aliases (optional `AS`, an alias is not visible in its own `SELECT`), `ROUND`, `--` comments, single vs double quotes, floating-point results of `REAL`, how the course's tests run `.sql` files (`python -m pytest`, `-k`, `-v`, reading a failure) | 1.1 | Minimal app: one-table seed (`seed.sql`) + `.sql` files with TODO + the test harness (`tests/conftest.py`) |
| 1.3 | `WHERE` (condition, clause), comparison operators, `AND`/`OR`/`NOT` and precedence (`AND` before `OR`), `IN`, `BETWEEN` (both ends included, lower bound first), `LIKE` with `%` and `_`, `NOT IN`/`NOT BETWEEN`/`NOT LIKE`, case rules of `=` and `LIKE` in SQLite vs PostgreSQL and MySQL, alias in `WHERE` as a portability trap | 1.2 | Minimal app: one-table seed (`apartments`, 14 rows) + `.sql` files with TODO + the harness of 1.2, unchanged |
| 1.4 | `NULL` (not `0`, not `'`), `IS [NOT] NULL`, three-valued logic (comparisons with `NULL` are unknown, `NOT`/`<>` do not bring `NULL` rows back, the `AND`/`OR` table), `NULL` in arithmetic, `COALESCE`, `NULLIF`, `SELECT` without `FROM` to try an expression, `IS DISTINCT FROM`/`IFNULL` as portability notes | 1.3 | Minimal app: one-table seed (`members`, 10 rows, `NULL` and `'` on purpose) + `.sql` files with TODO + the harness of 1.2, unchanged |
| 1.5 | `ORDER BY` (several keys, direction, where NULLs sort), `DISTINCT`, `LIMIT`/`OFFSET` pagination | 1.3, 1.4 | Minimal app |
| 1.6 | Text functions (`lower`, `trim`, `substr`, `replace`, `\|\|`), dates as ISO-8601 text and `date`/`strftime`, `CASE` | 1.3, 1.4 | Minimal app |
| 1.P | — | 1.1–1.6 | From scratch (brief + seed data) |
| 2.1 | Primary and foreign keys as ideas, one-to-many and many-to-many (join table), reading an entity-relationship diagram | 1.1 | Minimal app: a small multi-table demo database |
| 2.2 | `INNER JOIN … ON`, table aliases, joining three tables and through a join table, self-join | 2.1 | Minimal app |
| 2.3 | `LEFT JOIN`, `ON` vs `WHERE` with outer joins, anti-join (rows with no match), a mention of `RIGHT`/`FULL`/`CROSS JOIN` | 2.2, 1.4 | Minimal app |
| 2.4 | Aggregate functions (`COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT)`, `SUM`, `AVG`, `MIN`, `MAX`), `GROUP BY`, integer division | 2.2 | Minimal app |
| 2.5 | `HAVING` vs `WHERE`, fan-out after a join (inflated totals), aggregating before joining | 2.4, 2.3 | Minimal app |
| 2.6 | Scalar subqueries, `IN`/`NOT IN` (and the NULL trap), `EXISTS`, correlated subqueries, subqueries in `FROM` | 2.4, 1.4 | Minimal app |
| 2.7 | `UNION` vs `UNION ALL`, `INTERSECT`, `EXCEPT` | 2.2 | Minimal app |
| 2.P | — | 2.1–2.6 | From scratch (brief + seed data) |
| 3.1 | Entities and relationships, natural vs surrogate keys, update/insert/delete anomalies, 1NF–3NF, when to denormalize | 2.1 | — (concept) |
| 3.2 | `CREATE TABLE`/`DROP TABLE`, SQLite type affinity, `STRICT` tables | 3.1 | Minimal app: empty database |
| 3.3 | `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `DEFAULT`, `FOREIGN KEY` with `ON DELETE`, `PRAGMA foreign_keys` (off by default) | 3.2 | Minimal app |
| 3.4 | `INSERT` (several rows, `INSERT … SELECT`), `UPDATE`, `DELETE`, upsert (`ON CONFLICT … DO UPDATE`), `RETURNING` | 3.3 | Minimal app |
| 3.5 | Transactions: `BEGIN`/`COMMIT`/`ROLLBACK`, atomicity, `SAVEPOINT`, ACID in plain words | 3.4 | Minimal app |
| 3.6 | `ALTER TABLE` (`ADD`/`RENAME`/`DROP COLUMN`), rebuilding a table to change what `ALTER` cannot, migration scripts | 3.5 | Minimal app |
| 3.P | — | 3.1–3.5 | From scratch (brief + a flat spreadsheet export) |
| 4.1 | Common table expressions (`WITH`), several CTEs in a row, CTE vs subquery | 2.6 | Minimal app |
| 4.2 | `WITH RECURSIVE`: hierarchies and generated series | 4.1 | Minimal app |
| 4.3 | Window functions: `OVER`, `PARTITION BY`, `ROW_NUMBER`, `RANK`, `DENSE_RANK`, ties, top N per group | 4.1, 2.4 | Minimal app |
| 4.4 | Running totals with `ORDER BY` in a window, frames (`ROWS` vs the default `RANGE`), moving averages, `LAG`/`LEAD` | 4.3 | Minimal app |
| 4.5 | Conditional aggregation (`SUM(CASE …)`, `FILTER`), pivoting rows into columns, percentage of total | 4.3, 1.6, 2.4 | Minimal app |
| 4.P | — | 4.1, 4.3–4.5 | From scratch (brief + seed data) |
| 5.1 | How a table is searched (full scan vs B-tree index), `EXPLAIN QUERY PLAN`, the write and space cost of an index | 3.3 | Minimal app: a large generated table |
| 5.2 | `CREATE INDEX`, composite index column order, covering indexes, why an index is not used (function on the column, leading `%`, `OR`) | 5.1 | Minimal app |
| 5.3 | `sqlite3.connect`, `execute`/`executemany`, `?` and named placeholders, `fetchone`/`fetchall`, `row_factory`, closing the connection | 3.4 | Minimal app (Python) |
| 5.4 | SQL injection: building SQL by pasting text, exploiting it locally, fixing it with parameters, allow-listing identifiers that cannot be parameters | 5.3 | Minimal app (Python, a deliberately vulnerable module) |
| 5.5 | Transactions from Python (`commit`/`rollback`, `with conn`, `autocommit`), `IntegrityError` and friends, `PRAGMA foreign_keys` per connection | 5.3, 3.5 | Minimal app (Python) |
| 5.P | — | 5.1–5.5 (and the schema skills of block 3) | From scratch (brief) |

## Notas para los siguientes labs
- **El 1.1 ya enseñó** (no lo repitas, enlázalo): tabla, fila, columna y tipo; SQL declarativo y el `;` final; `SELECT * FROM`; la consola `python -m sqlite3` (solo tiene `.help`, `.version` y `.quit`; imprime cada fila como una tupla de Python); `sqlite_schema` y `pragma_table_info`; que abrir un archivo mal escrito crea una base vacía. El 1.1 también da el recordatorio de la terminal y la comprobación con `pwd`; los labs siguientes solo nombran la carpeta.
- **El 1.2 ya enseñó** (no lo repitas, enlázalo): la lista del `SELECT`, expresiones y operadores aritméticos con paréntesis, alias con `AS` (que `AS` es opcional y que un alias no existe dentro de su propio `SELECT`), `ROUND`, los comentarios `--`, comillas simples para textos y dobles para nombres (y que SQLite toma un `"nombre"` mal escrito como texto), que un `REAL` no es exacto (`5.0 * 1.18` da `5.8999999999999995`), y cómo correr las pruebas (`python -m pytest`, `-k taskN` desde la tarea 2, `-v` en la tarea 4) y leer un fallo. Los labs siguientes solo dicen "corre las pruebas" (o `python -m pytest -k taskN`).
- **Los retos no usan la consola:** el aprendiz escribe archivos `.sql` y los corre con las pruebas. Si un lab la usa, recuerda que en Python 3.12 un comando desconocido como `.tables` deja la consola esperando `;`, y que en 3.13+ da error.
- **Los retos copian el arnés del 1.2 sin cambiarlo:** `starter/` y `solution/` con `seed.sql`, `queries/NN_<slug>.sql` (un `-- TODO: write the query of task N (see the lab's README).` en el starter), `tests/conftest.py` (los fixtures `db` y `check`) y `tests/test_queries.py` (una clase `TestTaskN…` por tarea, más la guarda `TestSeed`). `check(archivo, columns=[...], rows=[...])` compara nombres y orden de columnas y las filas sin importar el orden. Cuando un lab pida ordenar (1.5 en adelante), agrega al `conftest.py` una comparación que respete el orden, en vez de cambiar `check`, y cópiala igual a los labs siguientes.
- **Los mensajes del arnés están en español y empiezan con cuatro frases fijas** que el README del 1.2 explica en una tabla (`tu archivo no devolvió ningún resultado`, `tu consulta dio un error`, `las columnas no coinciden`, `las columnas están bien, pero las filas no coinciden`). Si cambias una, cambia esa tabla. Dos casos más se explican solos y no van en la tabla: un archivo con dos consultas sale como `tu consulta dio un error` con la explicación en español (no el `ProgrammingError` en inglés), y un archivo que no está en UTF-8 dice cómo volver a guardarlo. El arnés acepta UTF-8 con BOM y UTF-16 (PowerShell 5.1 escribe así con `>`); no lo cambies por `read_text(encoding="utf-8")`.
- **Cuando una predicción pone una consulta en el archivo de la tarea,** el paso siguiente dice "Reemplaza la consulta de la predicción por la de la tarea", no "Escribe": dejar las dos da el error de dos consultas.
- **Los pasos que siguen a un 🔮 no dan la respuesta.** El paso que corre las pruebas dice "compara lo que muestra con tu predicción", nunca "lee el fallo", "compara el fallo" ni "las filas que sobran o faltan": con una predicción de sí o no (¿devuelve los 3 o ninguno?, ¿pasa sin redondear?), la palabra "fallo" ya la responde. El paso siguiente es una meta ("Deja en el archivo una consulta que devuelva …, y vuelve a correr … hasta que la prueba pase"), nunca "Corrige …" ni el arreglo ("con paréntesis", "redondea", "cambia el patrón"). Lo mismo para los nombres de las pruebas, que salen en la lista `FAILED` de la primera corrida, antes de cualquier predicción: en el 1.3, `test_districts_not_starting_with_the_word_san` delataba el espacio de la tarea 5 y pasó a `test_districts_of_the_other_branch`. Un paso que cambia la consulta ya resuelta dice "En esa misma consulta, cambia … por …", no "Escríbela otra vez".
- **El 🔍 no repite las tablas de Conceptos:** en el 1.3 se quitaron los operadores de comparación, que ya tenían su tabla.
- **"📍 Dónde correr los comandos" lleva la señal del entorno equivocado,** copiada del 1.2 y el 1.3: si la salida de `python -m pytest` tiene una línea `plugins:` o termina con `warnings`, el aprendiz no usa el Python del entorno y va al paso 3 de `SETUP.md`. El prompt `(.venv)` no lo prueba: con Anaconda, Git Bash puede mostrarlo con el Python de Anaconda a cargo (pytest 9.2.0 incluido, así que la versión de pytest no sirve de señal).
- **Los datos con decimales separan la respuesta correcta de las casi correctas:** cada redondeo pedido necesita al menos una fila donde otro número de decimales da otro valor (en el 1.2, el alfajor a 3.7: 3.7 × 1.18 = 4.366 hace fallar `ROUND(…, 3)`). Antes de dar por buena una prueba con redondeo, corre las variantes `ROUND(x)`, `ROUND(x, n − 1)`, `ROUND(x, n + 1)` y sin redondear, y confirma que todas fallan. Fuera de eso, elige decimales que no traigan ruido donde la tarea no lo enseña (las restas que se comparan sin redondear deben dar el literal exacto: mídelo). La división entera sigue siendo del 2.4: hasta entonces, divide solo columnas `REAL`.
- **El 1.2 explica los dos errores de SQLite más comunes** (`near "X": syntax error`: el problema está justo antes de `X`; `no such column: X`). Los labs siguientes los enlazan; un error nuevo que la tarea provoca a propósito se explica en su lab.
- **El 1.3 ya enseñó** (no lo repitas, enlázalo): `WHERE` y la idea de condición y cláusula, los operadores de comparación (`=`, `<>`/`!=`, `<`, `<=`, `>`, `>=`), `AND`/`OR`/`NOT` y que `AND` va antes que `OR` (paréntesis o `IN`), `IN`, `BETWEEN` (incluye los extremos; al revés no devuelve nada), `LIKE` con `%` y `_`, y las formas `NOT IN`/`NOT BETWEEN`/`NOT LIKE`. También que `=` distingue mayúsculas y que `LIKE` de SQLite no las distingue salvo en letras con tilde y ñ (`'Ático' LIKE 'ático'` es 0), con lo que hacen PostgreSQL (`ILIKE`) y MySQL (*collation*), y, en 💼, que un alias en `WHERE` funciona en SQLite pero no en PostgreSQL ni en MySQL. Normalizar textos con `lower`/`trim` queda prometido para el 1.6.
- **Los datos del 1.3 no tienen `NULL` a propósito:** el 1.4 es dueño de lo que hace `NULL` en un `WHERE` (una fila con `NULL` no sale ni con `= 'x'` ni con `<> 'x'`, ni con `NOT LIKE`). El 1.4 puede partir de ahí: la tarea 5 del 1.3 con `NOT LIKE` sería otra si un distrito fuera `NULL`.
- **El 1.4 ya enseñó** (no lo repitas, enlázalo): qué es `NULL` (no es `0`, ni `''`, ni `'NULL'`), `IS NULL`/`IS NOT NULL`, que una comparación con `NULL` (también `NULL = NULL`) es desconocida y `WHERE` no deja pasar la fila, que `<>`, `NOT`, `NOT LIKE` y `NOT IN` tampoco la traen, la tabla de `AND`/`OR` con desconocido (lógica de tres valores), que una operación con `NULL` da `NULL`, `COALESCE` (y dónde va: `fee - COALESCE(discount, 0)`, no `COALESCE(fee - discount, 0)`), `NULLIF` para convertir un relleno (`''`, `'-'`) en `NULL`, y que en la salida de las pruebas `NULL` sale como `None`. También el `SELECT` sin `FROM` para probar una expresión, y en 💼 `IS DISTINCT FROM` (PostgreSQL y SQLite), `IS NOT` de SQLite, `<=>` de MySQL e `IFNULL`. No enseñó: dónde ordena `ORDER BY` los `NULL` (1.5), que las funciones de agregado ignoran `NULL` (2.4), ni `NOT IN` con un `NULL` en la lista o en una subconsulta (2.6; medido: `'x' NOT IN ('a', NULL)` da `NULL` en 3.45.3 y 3.53.1). Medido también: en SQLite, `100 / 0` da `NULL` sin error.
- **En los README, `NULL` se escribe `` `NULL` `` en las tablas de datos y `''` es un texto vacío**, como en el 1.4. Los Conceptos del 1.4 usan `SELECT` sin `FROM`, porque `jobs` no tiene `NULL`.
- **Cada filtro que una prueba revisa tiene datos en sus bordes**, como los redondeos del 1.2: un valor justo en cada límite (en el 1.3, alquileres de 1200, 1800 y 2000), un texto con otra mayúscula al comienzo (`Cochera …`), el texto buscado al comienzo, al medio y al final, y un nombre que empieza como otro (`San …` y `Santiago de Surco`). Antes de dar por buena una prueba, corre las respuestas equivocadas de un principiante (`<` por `<=`, sin paréntesis, sin un `%`) y algunas correctas pero distintas (`IN` en vez de `OR`, `>= AND <=` en vez de `BETWEEN`), y confirma que las primeras fallan y las segundas pasan.
- **La línea de versiones de ✔️ Respuestas verificadas** se escribe como en el 1.2: "Verificado en Windows 11, en PowerShell 5.1 y Git Bash, con Python … y con Python 3.12.7 de Anaconda (SQLite 3.45.3)."
- **Los ejemplos de Conceptos no muestran un resultado que responda una predicción posterior:** en el 1.2, `1200 * 3.7413` da `4489.5599999999995`, así que el ejemplo de `ROUND` muestra solo el valor redondeado.
- **Las pruebas sobre el plan de consulta (5.1, 5.2) buscan fragmentos** como `USING INDEX` o `SCAN`, nunca el texto completo, que cambia entre versiones de SQLite.
- **Mensajes que cambian según la versión:** cita solo el comienzo estable (`Error: unknown command`) y di que el resto puede variar, o cita cada versión por separado. Antes de citar un mensaje, córrelo en todas las versiones de Python que hay a mano (3.12 a 3.15), no solo en las del CI.
- **Tamaños de archivo:** si un paso depende del tamaño, da `ls` para PowerShell (columna `Length`) y `ls -l` para Bash (el número antes de la fecha); un `ls` sin `-l` en Bash muestra solo nombres.
- **El 🔮 va antes del comando que lo revela,** también cuando el comando solo abre algo (el `Connected to …` de la consola ya responde la predicción).
- **Explica cada palabra o archivo nuevo que el aprendiz ve,** aunque no lo use: un *pragma*, un `pyproject.toml`, el saludo de la consola. Una línea basta ("no lo toques, es para las pruebas").
- **En las exploraciones, la línea de versiones verificadas va al comienzo de 🧪 Experimentos,** y no hay sección ✔️ si cada 👀 ya responde su predicción (como en el 1.1).
- **Di "hoja de cálculo", no "planilla":** en Perú, "planilla" es la nómina de sueldos.
