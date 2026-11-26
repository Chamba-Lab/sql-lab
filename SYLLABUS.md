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
| 1 · Consultar una tabla | Sacar de una tabla justo los datos que te piden: elegir, filtrar, ordenar y transformar | 🟨 `built` |
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
| 1.3 | [Filtrar filas](labs/01-query-a-table/03-filter-rows/README.md) | 🎯 `core` | 🧩 `challenge` | Quedarte solo con las filas que cumplen una o varias condiciones | ✅ `done` |
| 1.4 | [El valor NULL](labs/01-query-a-table/04-null-values/README.md) | 🎯 `core` | 🧩 `challenge` | Tratar los datos que faltan sin que te den resultados equivocados | 🟨 `built` |
| 1.5 | [Ordenar y paginar](labs/01-query-a-table/05-sort-and-paginate/README.md) | 🎯 `core` | 🧩 `challenge` | Ordenar resultados, quitar repetidos y mostrarlos por páginas | 🟨 `built` |
| 1.6 | [Transformar valores](labs/01-query-a-table/06-transform-values/README.md) | 🎯 `core` | 🧩 `challenge` | Limpiar textos, trabajar con fechas y clasificar filas según reglas | 🟨 `built` |
| 1.P | [Proyecto: catálogo de una tienda](labs/01-query-a-table/project-shop-catalog/README.md) | 🎯 `core` | 🏗️ `project` | Responder desde cero las preguntas del equipo de ventas sobre el catálogo de una tienda, con todo lo del bloque 1 | 🟨 `built` |

## Bloque 2 · Combinar y resumir
Cruzar varias tablas y resumirlas en totales, promedios y conteos.

| ID | Tema | Tipo de tema | Tipo de lab | Podrás… | Estado |
|---|---|---|---|---|---|
| 2.1 | [Relaciones entre tablas](labs/02-combine-and-summarize/01-table-relationships/README.md) | 🎯 `core` | 🔭 `exploration` | Seguir cómo una tabla apunta a otra y explicar por qué los datos se reparten en varias tablas | 🟨 `built` |
| 2.2 | [Unir tablas](labs/02-combine-and-summarize/02-join-tables/README.md) | 🎯 `core` | 🧩 `challenge` | Juntar en un solo resultado los datos de dos o más tablas relacionadas | 🟨 `built` |
| 2.3 | [Filas sin pareja](labs/02-combine-and-summarize/03-unmatched-rows/README.md) | 🎯 `core` | 🧩 `challenge` | Incluir también lo que no tiene pareja en la otra tabla y encontrar lo que falta | 🟨 `built` |
| 2.4 | [Agrupar y resumir](labs/02-combine-and-summarize/04-group-and-summarize/README.md) | 🎯 `core` | 🧩 `challenge` | Calcular totales, promedios y conteos por grupo | 🟨 `built` |
| 2.5 | [Filtrar grupos y no inflar totales](labs/02-combine-and-summarize/05-filter-groups/README.md) | 🎯 `core` | 🧩 `challenge` | Quedarte con los grupos que cumplen una condición y sumar bien después de unir tablas | 🟨 `built` |
| 2.6 | [Subconsultas](labs/02-combine-and-summarize/06-subqueries/README.md) | 🎯 `core` | 🧩 `challenge` | Usar el resultado de una consulta dentro de otra | 🟨 `built` |
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
| 1.1 | Relational model basics (database, table, row, column, type), SQL as a declarative language, `SELECT * FROM` as a first query, the `python -m sqlite3` shell, listing tables via `sqlite_schema` and columns via `pragma_table_info` | — | Minimal app: `demo/build_db.py` → `jobs.db` |
| 1.2 | `SELECT … FROM` (select list), expressions, arithmetic operators and parentheses, `AS` aliases (optional `AS`, an alias is not visible in its own `SELECT`), `ROUND`, `--` comments, single vs double quotes, floating-point results of `REAL`, how the course's tests run `.sql` files (`python -m pytest`, `-k`, `-v`, reading a failure), the errors `near "X": syntax error` and `no such column` | 1.1 | Minimal app: one-table seed + the harness (fixed here) |
| 1.3 | `WHERE` (condition, clause), comparison operators, `AND`/`OR`/`NOT` and precedence (`AND` before `OR`), `IN`, `BETWEEN` (both ends included, lower bound first), `LIKE` with `%` and `_`, `NOT IN`/`NOT BETWEEN`/`NOT LIKE`, case rules of `=` and `LIKE` in SQLite vs PostgreSQL and MySQL, alias in `WHERE` as a portability trap | 1.2 | Minimal app: one-table seed + the harness of 1.2 |
| 1.4 | `NULL` (not `0`, not `''`), `IS [NOT] NULL`, three-valued logic (comparisons with `NULL` are unknown, `NOT`/`<>` do not bring `NULL` rows back, the `AND`/`OR` table), `NULL` in arithmetic, `COALESCE` (`fee - COALESCE(discount, 0)`), `NULLIF`, `SELECT` without `FROM` to try an expression, `IS DISTINCT FROM`/`IFNULL` as portability notes | 1.3 | Minimal app: one-table seed + the harness of 1.2 |
| 1.5 | `ORDER BY` (several keys, one direction per key, `ASC` by default, ties), where NULLs sort (`NULLS FIRST`/`NULLS LAST`, SQLite vs PostgreSQL and MySQL, `x IS NULL` as the portable form), `DISTINCT` (whole row, NULLs count as equal), `LIMIT`/`OFFSET` pagination (`OFFSET (n − 1) × k`), top N with ties | 1.3, 1.4 | Minimal app: one-table seed + the harness of 1.2 plus `check_ordered` |
| 1.6 | Text functions (`LOWER`, `UPPER`, `TRIM`, `SUBSTR` counting from 1, `REPLACE`), `\|\|` (and `NULL` in it), `+` on text as a trap, dates as ISO-8601 text (date-time text compared with a day, `DATE` and its modifiers, `STRFTIME`), searched `CASE` (first true `WHEN` wins, `NULL` falls to `ELSE`) | 1.3, 1.4 | Minimal app: one-table seed + the harness of 1.5 |
| 1.P | Combining the rules of 1.2–1.6 in one query; `DISTINCT` over an expression and `DATE(…, '-30 days')` | 1.1–1.6 | From scratch: `BRIEF.md` + `acceptance/` (the pattern of the SQL projects) |
| 2.1 | Primary and foreign keys as ideas, one-to-many and many-to-many (join table), reading an entity-relationship diagram | 1.1 | Minimal app: the block-2 seed (`demo/seed.sql`) |
| 2.2 | `JOIN … ON` (= `INNER JOIN`), `table.column` and `ambiguous column name`, table aliases (the full name stops working), joining three and four tables and through a join table, self-join; the cartesian product of a `JOIN` without `ON` (SQLite and MySQL accept it, PostgreSQL does not), the old comma syntax as a note | 2.1 | Minimal app: the block-2 seed, unchanged + the harness of 1.5 |
| 2.3 | `LEFT JOIN` (= `LEFT OUTER JOIN`; the table written first keeps its rows), `NULL` in the columns of an unmatched row, a `JOIN` after a `LEFT JOIN` drops what it kept, anti-join with `LEFT JOIN … WHERE <right PK> IS NULL` (a nullable column catches real rows), several conditions in `ON`, `ON` vs `WHERE` with outer joins; `RIGHT`/`FULL`/`CROSS JOIN` mentioned (MySQL has no `FULL`) | 2.2, 1.4 | Minimal app: the block-2 seed, unchanged + the harness of 1.5 |
| 2.4 | Aggregate functions (`COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT)`, `SUM`, `AVG`, `MIN`, `MAX`; all but `COUNT(*)` skip `NULL`), `GROUP BY` (one or several columns, over a `JOIN`; group by the key, not the name), bare columns (SQLite allows them, PostgreSQL rejects them), integer division, `COUNT(<right PK>)` after a `LEFT JOIN` | 2.2, 2.3 | Minimal app: the block-2 seed, unchanged + the harness of 1.5 |
| 2.5 | `HAVING` vs `WHERE` (both in one query; a bare column in `HAVING`), fan-out after a join (`COUNT(DISTINCT pk)` fixes counts, `SUM(DISTINCT)` does not fix sums), aggregating before joining with a grouped subquery in `FROM` | 2.4, 2.3 | Minimal app: the block-2 seed + job 11 (a second 600 at Agro Norte) + the harness of 1.5 |
| 2.6 | Scalar subqueries (SQLite takes the first row of a multi-row one), `IN`/`NOT IN` with a subquery (and the NULL trap), `EXISTS`/`NOT EXISTS`, correlated subqueries (an unqualified column resolves to the inner table), links subqueries in `FROM` to 2.5 | 2.5, 1.4 | Minimal app: the 2.1 seed (10 jobs) + the harness of 1.5 |
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
Brief del bloque 2. Las reglas generales (datos de prueba, predicciones, shells, versiones) están en `docs/lessons.md`, y el porqué del arnés en `docs/decisions.md`; aquí va solo lo que un lab del bloque 2 necesita saber antes de empezar.

### Convenciones
- **Un reto copia la estructura del 2.2:** `starter/` y `solution/` con `seed.sql`, `queries/NN_<slug>.sql` (en el starter, solo `-- TODO: write the query of task N (see the lab's README).`), `pyproject.toml`, `tests/conftest.py` (el del 1.5: fixtures `db`, `check` y `check_ordered`, sin cambios) y `tests/test_queries.py` (una clase `TestTaskN…` por tarea, más la guarda `TestSeed`). `check(archivo, columns=[...], rows=[...])` compara nombres y orden de columnas y las filas sin orden. Usa `check_ordered` en toda tarea que pida un orden, y escribe en la tarea el orden completo con su desempate.
- **Los mensajes del arnés no se explican otra vez:** las cuatro frases fijas están en la tabla del README del 1.2 y la quinta (`check_ordered`) en «Ahora también importa el orden» del 1.5; enlázalas. Si cambias una, cambia esa tabla.
- **Enlaza, no repitas:** los labs solo dicen "corre las pruebas" o `python -m pytest -k taskN`; `near "X": syntax error` y `no such column` los explica el 1.2. Un error nuevo que la tarea provoca a propósito se explica en su lab.
- **"📍 Dónde correr los comandos" se copia del 2.2**, con la señal del entorno equivocado (línea `plugins:` o `warnings` al final de `python -m pytest` → paso 3 de `SETUP.md`).
- **Palabras clave y funciones en mayúscula** en el README, en `solution/` y en los encabezados de las tablas de ejemplo (SQLite nombra la columna con el texto tal como se escribió). En las tablas de datos, `NULL` se escribe `` `NULL` `` y `''` es un texto vacío. El 🔍 no repite las tablas de Conceptos.
- **Los retos no usan la consola:** el aprendiz escribe `.sql` y los corre con las pruebas.

### El 2.2 como modelo de reto
Copia del 2.2: la forma del README (problema → idea → ejemplo mínimo → nombre en Conceptos, una trampa medida por tarea, 💼 con lo que cambia en PostgreSQL y MySQL y la fuente cuando no se corrió allí), las pruebas con `check`, y su verificación: una batería de variantes (29 en el 2.2) corrida con `sqlite3` en Python 3.12 y 3.15 (SQLite 3.53.1) y en Anaconda 3.12.7 (SQLite 3.45.3), antes de escribir las predicciones.

### Lo que ya se enseñó (no lo repitas, enlaza al dueño)
- **Bloque 1:** lo de la columna *Owns* del mapa. Quedó prometido y no se enseñó: que las funciones de agregado ignoran `NULL` y la división entera (2.4; hasta entonces solo se dividen columnas `REAL`), `NOT IN` con un `NULL` en la lista o en una subconsulta (2.6), las funciones de ranking (4.3), `SUM(CASE …)` (4.5), la normalización (3.1). Tampoco se enseñó `CASE` simple (`CASE x WHEN …`), `LENGTH`, `INSTR`, `JULIANDAY` ni restar fechas, ni ordenar textos según el idioma (`LOWER` solo cambia letras ASCII).
- **El 2.1:** por qué repartir los datos (el nombre de la empresa repetido en cada oferta del 1.1), clave primaria (*primary key*, PK), clave foránea (*foreign key*, FK) con `REFERENCES` y la costumbre `<tabla en singular>_id`, una FK hacia su propia tabla (`referred_by`), uno a muchos (la FK va del lado de los muchos), muchos a muchos con tabla intermedia (*join table*) que guarda datos de la pareja, y leer un diagrama ER de Mermaid (pata de gallo: `||`, `o|`, `o{`, `|{`). Siguió cada referencia a mano con dos `WHERE`, mostró que una empresa puede no tener ofertas (las filas sin pareja son del 2.3), que una PK repetida da `IntegrityError (SQLITE_CONSTRAINT_PRIMARYKEY): UNIQUE constraint failed: candidates.id`, que una FK hacia una fila que no existe entra sin error (`PRAGMA foreign_keys` es del 3.3), `pragma_foreign_key_list` (con `"table"`, `"from"`, `"to"` entre comillas dobles) e `INSERT INTO … VALUES` en una línea (prometido para el bloque 3).
- **El 2.2:** `JOIN … ON` e `INNER JOIN` como lo mismo, que el `ON` sigue una FK hasta la PK, que un `JOIN` sin `ON` da el producto cartesiano (*cartesian product*: 10 ofertas × 6 empresas = 60; así trabaja todo `JOIN` por dentro y el `ON` filtra las parejas), `tabla.columna` y `ambiguous column name: id`, alias de tabla (con `FROM jobs AS j`, `jobs.title` da `no such column: jobs.title`), unir tres y cuatro tablas pasando por `applications`, el *self-join* con dos alias (`ON c.referred_by = r.id`; al revés, las parejas salen invertidas), que unir por la columna equivocada (`a.id = c.id`) da filas creíbles sin error, y que un nombre repetido no identifica a una persona (se filtra por `id`). Dijo, y dejó para el 2.3, que el `JOIN` deja fuera las filas sin pareja (Nube Andina, las personas con `referred_by` `NULL`). En 💼: la sintaxis con comas, que PostgreSQL exige una condición en todo `JOIN` y el *self-join* de empleados y jefes. No enseñó `USING`, `NATURAL JOIN` ni `CROSS JOIN` (el 2.3 menciona este último).
- **El 2.3:** `LEFT JOIN` y `LEFT OUTER JOIN` como lo mismo (la tabla escrita antes conserva todas sus filas; *outer join* frente a *inner join*), el `NULL` en las columnas de la otra tabla (`None` en las pruebas), que un `JOIN` después de un `LEFT JOIN` quita lo que este conservó (Diego Flores), el *anti-join* `LEFT JOIN … WHERE j.id IS NULL` (preguntar por `salary_usd` trae también a Andes Retail por la oferta 9), varias condiciones en el `ON` con `AND`, y que en un `LEFT JOIN` el `ON` arma las parejas y el `WHERE` filtra después (un filtro de la tabla derecha en el `WHERE` lo vuelve un `JOIN`). Mencionó `RIGHT JOIN` (un `LEFT JOIN` con las tablas al revés), `FULL JOIN` y `CROSS JOIN` (60 filas), medidos en SQLite 3.45.3 y 3.53.1; en 💼, que MySQL recomienda `LEFT` sobre `RIGHT` y no tiene `FULL`, y que `NOT EXISTS`/`NOT IN` llegan en el 2.6. Las filas sembradas del 2.3 ya se usaron: Nube Andina (tareas 1, 3 y 4), la oferta 10 (sin usar: el ejemplo de *anti-join* de Conceptos busca a quienes no recomendaron a nadie), Diego Flores (tarea 2).
- **El 2.4:** las funciones de agregado `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` (estas dos también con textos y fechas), `COUNT(*)` frente a `COUNT(columna)` (todas salvo `COUNT(*)` ignoran `NULL`), `COUNT(DISTINCT …)`, `GROUP BY` con una y dos columnas y sobre un `JOIN`, la regla de escribir en el `GROUP BY` cada columna del `SELECT` que no está en una función de agregado, y el orden `SELECT … FROM … WHERE … GROUP BY … ORDER BY`. En ✔️ y 💼: la división entera (`7 / 2` = `3`, `* 1.0`; MySQL usa `/` con decimales y `DIV`), la columna suelta (*bare column*: SQLite toma el valor de una fila del grupo, PostgreSQL y MySQL con `ONLY_FULL_GROUP_BY` la rechazan salvo con la PK en el `GROUP BY`), agrupar por la clave y no por el nombre (los dos Luis Ramírez), y `COUNT(a.id)` en lugar de `COUNT(*)` tras un `LEFT JOIN`. No enseñó `HAVING` (2.5), `GROUP_CONCAT`, `TOTAL` ni `ORDER BY` con agregados. Filas sembradas usadas: la oferta 9 (tarea 2, `SUM / COUNT(*)`), Clínica Central 987.5 (tarea 2), los dos Luis Ramírez (tarea 3), Nube Andina y la oferta 10 (tarea 4: `COUNT(*)` da 1 y 3).
- **El 2.5:** `HAVING` (después del `GROUP BY`, puede usar agregados), `WHERE` y `HAVING` en la misma consulta con el orden FROM → WHERE → GROUP BY → HAVING → SELECT, y el orden escrito `… GROUP BY … HAVING … ORDER BY`. Presentó la subconsulta en el `FROM` con alias (*subquery*) solo para agrupar dos veces y para unir un resumen; el 2.6 es dueño de las demás formas (escalar, `IN`, `EXISTS`, correlacionada) y puede enlazar este uso. En ✔️ y 💼: `misuse of aggregate: COUNT()` (un agregado en el `WHERE`), la columna suelta en el `HAVING` (SQLite la acepta y mira una fila del grupo; PostgreSQL la rechaza), el alias en el `HAVING` (SQLite sí, PostgreSQL no), el abanico (*fan-out*: `COUNT(j.id)` tras unir postulaciones), que `SUM(DISTINCT)` junta sueldos iguales de ofertas distintas, y agregar antes de unir (con `LEFT JOIN` para no perder ofertas sin postulaciones). Su seed agrega la oferta 11 (Agro Norte, 600, sin postulaciones), así que tiene 11 ofertas; los labs siguientes copian el seed del 2.1 (10 ofertas) salvo que necesiten esa fila. Filas usadas: Ana Quispe, Sofía Castro y Luis Ramírez (6) en la tarea 2, Clínica Central como coincidencia en la tarea 3, Agro Norte y las ofertas 10 y 11 en la tarea 4.
- **El 2.6:** la subconsulta escalar (*scalar subquery*: en el `WHERE`, un solo valor), `IN` y `NOT IN` con una subconsulta, la subconsulta correlacionada (*correlated subquery*: en el `SELECT` con `COUNT`, una vez por fila de afuera, Diego Flores con 0 sin `LEFT JOIN`), `EXISTS`/`NOT EXISTS` con `SELECT 1`, y enlaza la del `FROM` al 2.5. En ✔️ y 💼: SQLite toma la primera fila de una subconsulta escalar con varias (PostgreSQL da error, según su documentación; no se corrió), que un `JOIN` repite a quien tiene dos filas relacionadas (`IN` no), que una columna sin alias en la subconsulta se busca primero adentro (`company_id = company_id` es siempre verdadero), y `NOT IN` con un `NULL` en la lista: 0 filas (lo prometido en el bloque 1; arreglos: `NOT EXISTS`, `IS NOT NULL` en la subconsulta o el *anti-join* del 2.3). Mencionó el plan de ejecución (5.1) y «el segundo sueldo más alto». No enseñó `ANY`/`ALL`, `WITH` (4.1) ni subconsultas en `HAVING`. Usa el seed del 2.1 (10 ofertas). Filas usadas: las 3 ofertas de Andes Retail con la 1 (1200) primero (tarea 1), Luis Ramírez (2) con dos ofertas remotas (tarea 2), Clínica Central y Agro Norte con una sola oferta (tarea 3), los cuatro `referred_by` `NULL` (tarea 4).

### La base del bloque 2
La bolsa de trabajo del 1.1, crecida, en `labs/02-combine-and-summarize/01-table-relationships/demo/seed.sql`. Los retos 2.3 a 2.7 copian ese archivo como su `seed.sql` (usa comillas simples para textos, así que funciona con el arnés del 1.5, que apaga las comillas dobles como texto) y pueden agregarle filas; si cambian una fila existente, revisen que los README del 2.1 y el 2.2 no la citen.
- **Esquema:** `companies(id PK, name, city, sector)`, `jobs(id PK, company_id → companies, title, mode, salary_usd INTEGER, posted_on)`, `candidates(id PK, name, city, years_experience REAL, referred_by → candidates)`, `applications(id PK, candidate_id → candidates, job_id → jobs, applied_on, status)`, con 6, 10, 9 y 16 filas, sin huérfanos (`PRAGMA foreign_key_check` vacío). Estados de `applications`: `enviada`, `entrevista`, `rechazada`, `contratada`.
- **Filas sembradas para los labs siguientes:** 2.3: Nube Andina (empresa 6) sin ofertas, la oferta 10 sin postulaciones, Diego Flores (8) sin postulaciones. 2.4: la oferta 9 con `salary_usd` `NULL` (Andes Retail: `AVG` da 1350, `SUM / COUNT(*)` da 900) y Clínica Central con 825 + 1150 = 1975 (división entera 987 contra 987.5). 2.5: Andes Retail con 3 ofertas y 6 postulaciones, para el abanico (*fan-out*). 2.7: Cusco solo en `candidates`; Arequipa, Bogotá, Lima, Santiago y Trujillo en las dos tablas, para `EXCEPT` e `INTERSECT`.
- **Propiedades que separan las respuestas equivocadas; mantenlas si agregas filas:** las ofertas 1 a 3 coinciden con su `company_id` y las 4 a 6 no (así `ON jobs.id = companies.id` falla), los `id` de `applications` difieren de su `candidate_id` (salvo la 1, a propósito: la coincidencia cubre algunas filas), los dos Luis Ramírez (ids 2 y 6) tienen postulaciones, y cada pareja de recomendaciones (cadena 7 → 3 → 1) es asimétrica.

### Trampas conocidas
- **Antes de una predicción que ofrece "un error", busca en el README de arriba "error" y "avisa":** en el 2.2, el 💡 decía que un `JOIN` mal escrito «no avisa» y respondía la tarea 1. En el bloque 2 casi toda consulta equivocada devuelve filas; solo una columna compartida sin calificar da error.
- **Lee también el `seed.sql` antes de una predicción:** en el 2.1, un comentario del seed respondía el experimento 6. No pongas en el seed comentarios sobre lo que una tarea pregunta.
- **2.4 es el primero que divide enteros;** sus pruebas de `AVG` necesitan la oferta con `NULL` y una división que no sea exacta.
- **2.P:** sigue el patrón del 1.P (`acceptance/` + `reference/`, ver `docs/decisions.md`), con una fila que delate cada regla en cada consulta que la usa, la página pedida como la última y corta, y "hoy" fijo y dicho junto a la fecha.
