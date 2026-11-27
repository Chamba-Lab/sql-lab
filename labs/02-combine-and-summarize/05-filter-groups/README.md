# 🧩 2.5 · Filtrar grupos y no inflar totales

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Quedarte solo con los grupos que cumplen una condición, con `HAVING`.
- Usar `WHERE` y `HAVING` en la misma consulta, cada uno en su momento.
- Usar el resultado de una consulta agrupada dentro del `FROM` de otra.
- Contar y sumar datos de dos tablas relacionadas en una sola consulta.
- Comprobar cada total de un reporte contra los datos de las tablas.

## 💡 Por qué importa
En el lab 2.4 calculaste un resumen por grupo. Las preguntas que siguen piden escoger grupos: los clientes con más de cinco pedidos, los productos que se vendieron menos de diez veces, las ofertas con al menos dos postulaciones. Y los reportes de verdad juntan datos de varias tablas en una fila, donde un total mal calculado sale como un número creíble y equivocado. Las dos cosas son preguntas fijas de las entrevistas de SQL.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/02-combine-and-summarize/05-filter-groups/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la base de las tareas, que es la del [lab 2.1](../01-table-relationships/README.md) con una oferta más (la 11, ver [La base](#la-base)). No hace falta correrlos; si quieres probarlos, crea la base y abre la consola como en el experimento 1 del lab 2.1, sabiendo que allí no está la oferta 11 y algunas cuentas salen distintas.

### Quedarte con algunos grupos (*HAVING*)
¿Qué modalidades tienen 4 ofertas o más? Con lo del lab 2.4 sabes contar las ofertas de cada modalidad:

```sql
SELECT mode, COUNT(*) AS jobs
FROM jobs
GROUP BY mode;
```

| mode | jobs |
|---|---|
| híbrido | 3 |
| presencial | 5 |
| remoto | 3 |

Pero la pregunta pide solo las filas del resultado cuya cuenta llega a 4. La condición no es sobre una oferta: es sobre un grupo entero.

La idea: una segunda condición que se revisa después del `GROUP BY`, una vez por grupo, y que puede usar las funciones de agregado. Esa condición va en **`HAVING`**, justo después del `GROUP BY`:

```sql
SELECT mode, COUNT(*) AS jobs
FROM jobs
GROUP BY mode
HAVING COUNT(*) >= 4;
```

| mode | jobs |
|---|---|
| presencial | 5 |

Los otros dos grupos se armaron y se contaron igual, pero no cumplieron la condición y no salen.

### `WHERE` y `HAVING` en la misma consulta
¿En qué modalidades hay 2 ofertas o más que paguen 1500 o más? Aquí hay dos condiciones de distinto tipo: una mira cada oferta (su sueldo) y la otra mira cada grupo (cuántas ofertas quedaron en él).

Una consulta con `GROUP BY` trabaja en este orden: el `FROM` arma las filas, el `WHERE` decide cuáles de esas filas entran en los grupos, el `GROUP BY` las reparte en grupos, el `HAVING` decide qué grupos quedan, y al final el `SELECT` arma una fila por grupo. Cada condición va donde se puede revisar:

```sql
SELECT mode, COUNT(*) AS jobs
FROM jobs
WHERE salary_usd >= 1500
GROUP BY mode
HAVING COUNT(*) >= 2;
```

| mode | jobs |
|---|---|
| híbrido | 2 |
| remoto | 2 |

Paso a paso: el `WHERE` deja las 5 ofertas que pagan 1500 o más (la 9, sin sueldo, tampoco entra: `NULL >= 1500` no es verdadero). El `GROUP BY` las reparte en híbrido (2), presencial (1) y remoto (2), y el `HAVING` quita presencial. Las cuentas de `COUNT(*)` son las de las filas que dejó el `WHERE`, no las de toda la tabla.

El orden en que se escriben las partes es `SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY …`.

### Una consulta agrupada dentro del `FROM`
¿Cuántas personas hicieron una postulación, cuántas hicieron dos y cuántas tres? Primero hay que contar las postulaciones de cada persona, y después agrupar ese resultado por la cuenta: son dos agrupaciones, una encima de la otra.

La idea: escribir la primera consulta entre paréntesis en el `FROM` de la segunda, con un alias, y usar su resultado como si fuera una tabla. El alias es el nombre de esa tabla, y los alias de las columnas de adentro (`AS applications`) son los nombres de sus columnas:

```sql
SELECT applications, COUNT(*) AS candidates
FROM (
    SELECT candidate_id, COUNT(*) AS applications
    FROM applications
    GROUP BY candidate_id
) AS per_candidate
GROUP BY applications;
```

| applications | candidates |
|---|---|
| 1 | 1 |
| 2 | 6 |
| 3 | 1 |

La consulta de adentro devuelve una fila por persona con su cuenta (8 filas: Diego Flores no postuló). La de afuera agrupa esas 8 filas por la columna `applications`. Una consulta escrita dentro de otra es una **subconsulta** (*subquery*); el lab 2.6 muestra las demás formas.

Como cualquier tabla del `FROM`, la subconsulta se puede unir con otra tabla. Aquí, para ver el nombre de quien hizo 3 postulaciones:

```sql
SELECT c.name, per_candidate.applications
FROM candidates AS c
JOIN (
    SELECT candidate_id, COUNT(*) AS applications
    FROM applications
    GROUP BY candidate_id
) AS per_candidate ON per_candidate.candidate_id = c.id
WHERE per_candidate.applications >= 3;
```

| name | applications |
|---|---|
| Ana Quispe | 3 |

Afuera, `applications` ya es una columna de una tabla más, así que se filtra con `WHERE`.

## 📚 Documentación
- [PostgreSQL: funciones de agregado](https://www.postgresql.org/docs/current/tutorial-agg.html), en inglés: la diferencia entre `WHERE` y `HAVING`, con ejemplos
- [SQLite: cómo se arma el resultado de un `SELECT`](https://www.sqlite.org/lang_select.html#resultset), en inglés: el orden de `WHERE`, `GROUP BY` y `HAVING`
- [PostgreSQL: la cláusula `HAVING`](https://www.postgresql.org/docs/current/sql-select.html#SQL-HAVING), en inglés

## 🧭 Escenario
La bolsa de trabajo quiere un segundo tablero: las ofertas más buscadas, las personas con más postulaciones vigentes, y por empresa, cuántas ofertas y postulaciones tiene y cuánto suman los sueldos que ofrece. Te pide cuatro consultas.

### La base
Son las cuatro tablas del [lab 2.1](../01-table-relationships/README.md#-escenario), con los datos de los labs 2.2 a 2.4 y una oferta más, la 11. Este es su diagrama en texto:

| Tabla | Clave primaria | Claves foráneas |
|---|---|---|
| `companies` | `id` | ninguna |
| `jobs` | `id` | `company_id` → `companies (id)` |
| `candidates` | `id` | `referred_by` → `candidates (id)` |
| `applications` | `id` | `candidate_id` → `candidates (id)`, `job_id` → `jobs (id)` |

Y estos son todos sus datos.

`companies`:

| id | name | city | sector |
|---|---|---|---|
| 1 | Andes Retail | Lima | retail |
| 2 | Pago Fácil | Bogotá | fintech |
| 3 | Clínica Central | Arequipa | salud |
| 4 | Agro Norte | Trujillo | agroindustria |
| 5 | Banco Sur | Santiago | banca |
| 6 | Nube Andina | Lima | tecnología |

`jobs`:

| id | company_id | title | mode | salary_usd | posted_on |
|---|---|---|---|---|---|
| 1 | 1 | Analista de datos júnior | híbrido | 1200 | 2026-11-03 |
| 2 | 2 | Desarrollador backend | remoto | 1800 | 2026-11-05 |
| 3 | 3 | Soporte de TI | presencial | 825 | 2026-11-06 |
| 4 | 1 | Analista de BI | presencial | 1500 | 2026-11-10 |
| 5 | 4 | Practicante de datos | presencial | 600 | 2026-11-12 |
| 6 | 2 | Desarrolladora full stack | remoto | 2000 | 2026-11-14 |
| 7 | 5 | Administrador de bases de datos | híbrido | 2400 | 2026-11-18 |
| 8 | 3 | Analista de calidad (QA) | remoto | 1150 | 2026-11-20 |
| 9 | 1 | Practicante de marketing digital | presencial | `NULL` | 2026-11-21 |
| 10 | 5 | Analista de riesgos | híbrido | 1750 | 2026-11-24 |
| 11 | 4 | Practicante de operaciones | presencial | 600 | 2026-11-25 |

`candidates` (`referred_by` es el `id` de quien recomendó a esa persona):

| id | name | city | years_experience | referred_by |
|---|---|---|---|---|
| 1 | Ana Quispe | Lima | 0.5 | `NULL` |
| 2 | Luis Ramírez | Bogotá | 2.0 | `NULL` |
| 3 | María Torres | Arequipa | 1.0 | 1 |
| 4 | Jorge Huamán | Lima | 0.0 | 1 |
| 5 | Sofía Castro | Santiago | 3.5 | `NULL` |
| 6 | Luis Ramírez | Lima | 0.5 | 4 |
| 7 | Carmen Rojas | Trujillo | 1.5 | 3 |
| 8 | Diego Flores | Cusco | 4.0 | `NULL` |
| 9 | Valeria Paredes | Lima | 2.5 | 5 |

`applications`:

| id | candidate_id | job_id | applied_on | status |
|---|---|---|---|---|
| 1 | 1 | 1 | 2026-11-04 | entrevista |
| 2 | 1 | 4 | 2026-11-11 | enviada |
| 3 | 1 | 5 | 2026-11-13 | rechazada |
| 4 | 2 | 2 | 2026-11-06 | entrevista |
| 5 | 2 | 6 | 2026-11-15 | enviada |
| 6 | 3 | 3 | 2026-11-07 | contratada |
| 7 | 3 | 8 | 2026-11-21 | enviada |
| 8 | 4 | 1 | 2026-11-05 | enviada |
| 9 | 4 | 5 | 2026-11-12 | entrevista |
| 10 | 5 | 7 | 2026-11-19 | entrevista |
| 11 | 6 | 1 | 2026-11-06 | rechazada |
| 12 | 6 | 9 | 2026-11-22 | enviada |
| 13 | 7 | 5 | 2026-11-14 | enviada |
| 14 | 9 | 4 | 2026-11-12 | entrevista |
| 15 | 9 | 7 | 2026-11-20 | enviada |
| 16 | 5 | 6 | 2026-11-16 | rechazada |

### Tus archivos
```text
starter/
├── queries/                                     tus cuatro consultas, una por tarea
│   ├── 01_popular_jobs.sql
│   ├── 02_active_candidates.sql
│   ├── 03_jobs_and_applications_by_company.sql
│   └── 04_salary_and_applications_by_company.sql
├── seed.sql                                     crea las cuatro tablas y sus filas
├── tests/
│   ├── conftest.py                              prepara la base y compara resultados
│   └── test_queries.py                          las pruebas: una clase por tarea
└── pyproject.toml                               le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../../01-query-a-table/02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). Ninguna tarea pide un orden: las filas pueden salir en cualquiera. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 4, una por tarea.

### Tarea 1 · Las ofertas más buscadas
**Objetivo:** las ofertas que recibieron 2 postulaciones o más, cada una con cuántas recibió. Columnas `id` y `title` (de la oferta) y `applications`, 5 filas. **Lo valida:** [`TestTask1PopularJobs`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Qué crees que pasa: devuelve las 5 ofertas, devuelve todas las ofertas que tienen postulaciones, o da un error? Escribe tu predicción y después pon la consulta en [`queries/01_popular_jobs.sql`](starter/queries/01_popular_jobs.sql):

```sql
SELECT j.id, j.title, COUNT(*) AS applications
FROM jobs AS j
JOIN applications AS a ON a.job_id = j.id
WHERE COUNT(*) >= 2
GROUP BY j.id, j.title;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1PopularJobs` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 3 fallan.

### Tarea 2 · Las personas con más postulaciones vigentes
**Objetivo:** las personas con 2 postulaciones o más que no fueron rechazadas (`status` distinto de `'rechazada'`), cada una con cuántas de esas postulaciones tiene. Columnas `id` y `name` (de la persona) y `applications`, 5 filas. **Lo valida:** [`TestTask2ActiveCandidates`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió las dos condiciones juntas en el `HAVING`. ¿Crees que pasa la prueba? Si no pasa, ¿cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/02_active_candidates.sql`](starter/queries/02_active_candidates.sql):

```sql
SELECT c.id, c.name, COUNT(*) AS applications
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
GROUP BY c.id, c.name
HAVING COUNT(*) >= 2 AND a.status <> 'rechazada';
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2ActiveCandidates` pasa. Con todas las pruebas, 3 pasan y 2 fallan.

### Tarea 3 · Ofertas y postulaciones de cada empresa
**Objetivo:** las 6 empresas, cada una con cuántas ofertas publicó (`jobs`) y cuántas postulaciones recibieron sus ofertas, entre todas (`applications`). Una empresa sin ofertas sale igual, con `0` y `0`. Columnas `company` (el nombre de la empresa), `jobs` y `applications`, 6 filas. **Lo valida:** [`TestTask3JobsAndApplicationsByCompany`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero partió de la respuesta de la tarea 4 del lab 2.4 y le agregó la cuenta de ofertas. ¿Crees que pasa la prueba? Si no pasa, ¿en cuántas empresas crees que `jobs` sale con otro número? Escribe tu predicción y después pon la consulta en [`queries/03_jobs_and_applications_by_company.sql`](starter/queries/03_jobs_and_applications_by_company.sql):

```sql
SELECT c.name AS company, COUNT(j.id) AS jobs, COUNT(a.id) AS applications
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN applications AS a ON a.job_id = j.id
GROUP BY c.id, c.name;
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3JobsAndApplicationsByCompany` pasa. Con todas las pruebas, 4 pasan y 1 falla.

### Tarea 4 · Sueldos ofrecidos y postulaciones de cada empresa
**Objetivo:** cada empresa que tiene ofertas, con la suma de los sueldos de sus ofertas (`total_salary`; las que no dicen el sueldo no suman) y cuántas postulaciones recibieron sus ofertas, entre todas (`applications`). Columnas `company`, `total_salary` y `applications`, 5 filas. **Lo valida:** [`TestTask4SalaryAndApplicationsByCompany`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero adaptó a la suma su solución de la tarea 3. ¿Crees que pasa la prueba? Si no pasa, ¿en cuántas empresas sale otro `total_salary`? Escribe tu predicción y después pon la consulta en [`queries/04_salary_and_applications_by_company.sql`](starter/queries/04_salary_and_applications_by_company.sql):

```sql
SELECT c.name AS company, SUM(DISTINCT j.salary_usd) AS total_salary, COUNT(a.id) AS applications
FROM companies AS c
JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN applications AS a ON a.job_id = j.id
GROUP BY c.id, c.name;
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask4SalaryAndApplicationsByCompany` pasa, y con todas las pruebas, pasan las 5.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `WHERE condición` | Decide qué filas entran en los grupos; se revisa antes de agrupar, fila por fila |
| `GROUP BY a, b` | Reparte en grupos las filas que dejó el `WHERE` |
| `HAVING condición` | Decide qué grupos quedan; se revisa después de agrupar, una vez por grupo, y puede usar funciones de agregado |
| `FROM (SELECT …) AS nombre` | Usa el resultado de una consulta como una tabla más, con ese nombre |
| `SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY …` | El orden en que se escriben las partes |

## 💼 En proyectos reales
- **PostgreSQL rechaza la consulta de la predicción de la tarea 2:** toda columna que el `HAVING` nombra fuera de una función de agregado tiene que estar en el `GROUP BY` ([PostgreSQL](https://www.postgresql.org/docs/current/sql-select.html#SQL-HAVING)), la misma regla de la columna suelta del lab 2.4. SQLite la deja pasar y responde con datos equivocados.
- **SQLite acepta el alias en el `HAVING`** (`HAVING applications >= 2`); PostgreSQL no, y hay que repetir la expresión: `HAVING COUNT(*) >= 2` ([PostgreSQL](https://www.postgresql.org/docs/current/sql-select.html#SQL-SELECT-LIST)). Repetirla funciona en los dos.
- **Un total inflado no da error.** En un reporte que une pedidos con sus líneas, o clientes con sus pedidos y sus pagos, sumar una columna de la tabla de arriba después del `JOIN` la suma una vez por cada fila de abajo. Antes de entregar un reporte, compara un total con una consulta a una sola tabla: si `SUM(salary_usd)` de `jobs` no coincide con la suma de tu columna, algo se repitió.
- **Agregar antes de unir** es la solución de siempre: se resume la tabla de abajo en una subconsulta (o en un paso con nombre, que verás en el lab 4.1) y se une el resumen, que ya tiene una fila por cada fila de arriba.
- **«Los clientes con más de N pedidos»** es la pregunta de `HAVING` más común en entrevistas, y casi siempre la siguen con «y solo de este año», que va en el `WHERE`.

## 🆘 Pistas
<details><summary>Pista 1 · <code>misuse of aggregate</code></summary>

¿En qué momento se revisa el `WHERE`: antes o después de armar los grupos? ¿Existe ya la cuenta de cada grupo en ese momento? Repasa en Conceptos qué parte revisa una condición por grupo.
</details>

<details><summary>Pista 2 · Ana Quispe sale con 3, o Sofía Castro aparece</summary>

¿La condición sobre `status` mira una postulación o un grupo entero? Si un grupo tiene una postulación rechazada y dos que no, ¿cuál de las tres mira `a.status` en el `HAVING`? ¿Qué parte de la consulta decide qué filas entran en los grupos?
</details>

<details><summary>Pista 3 · Una empresa tiene más ofertas que las de la tabla <code>jobs</code></summary>

Andes Retail tiene 3 ofertas. ¿Cuántas filas hay para Andes Retail después de los dos `JOIN`, una por oferta o una por postulación? ¿Cuántas veces aparece la oferta 1 en esas filas? ¿Qué forma de `COUNT` del lab 2.4 cuenta cada valor una sola vez?
</details>

<details><summary>Pista 4 · El total de Agro Norte no coincide</summary>

Suma a mano los sueldos de las ofertas de Agro Norte en `jobs`. ¿Qué tienen en común? ¿Qué número da tu consulta, y qué parte de ella puede haber dejado fuera uno de los dos sueldos?
</details>

<details><summary>Pista 5 · Cómo sumar sin repetir</summary>

El problema es que cada oferta aparece una vez por cada postulación suya. ¿Y si las postulaciones llegaran ya contadas, una fila por oferta? Escribe primero una consulta que cuente las postulaciones de cada oferta, y después úsala dentro del `FROM` como en el último ejemplo de Conceptos. ¿Qué pasa con las ofertas que no tienen postulaciones si la unes con `JOIN`?
</details>

## 🎤 Autoevaluación
1. ¿Qué diferencia hay entre `WHERE` y `HAVING`?
2. En `orders(id, customer_id, total, ordered_on)`, escribe la consulta de los clientes con 3 pedidos o más en 2026, con cuántos tiene cada uno.
3. ¿Por qué `SELECT customer_id FROM orders WHERE COUNT(*) > 3 GROUP BY customer_id;` da error?
4. `orders` tiene 2 pedidos de 100 y 300, y `order_lines` tiene 3 líneas del primero y 1 del segundo. Al unirlas, ¿cuánto da `SUM(o.total)`?
5. ¿Por qué `SUM(DISTINCT o.total)` no arregla la pregunta 4 en general?

<details><summary>Respuestas</summary>

1. `WHERE` decide qué filas entran en los grupos y se revisa antes de agrupar; `HAVING` decide qué grupos quedan, se revisa después y puede usar funciones de agregado.
2. `SELECT customer_id, COUNT(*) AS orders FROM orders WHERE ordered_on >= '2026-01-01' AND ordered_on < '2027-01-01' GROUP BY customer_id HAVING COUNT(*) >= 3;`
3. Porque el `WHERE` se revisa fila por fila antes de agrupar, cuando todavía no hay grupos que contar. La condición va en `HAVING COUNT(*) > 3`.
4. 600: el primer pedido sale en 3 filas y suma 100 tres veces, más 300 del segundo. El total real es 400.
5. Porque dos pedidos distintos con el mismo total se sumarían una sola vez. Hay que resumir `order_lines` en una subconsulta y unir el resumen, o sumar `o.total` en una consulta sin el `JOIN`.
</details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · El `WHERE` se revisa antes de que existan los grupos
```text
01_popular_jobs.sql: tu consulta dio un error.
  OperationalError: misuse of aggregate: COUNT()
```

Un error: *misuse of aggregate* quiere decir «uso indebido de una función de agregado». El `WHERE` se revisa fila por fila, antes del `GROUP BY`, y en ese momento no hay grupos que contar. Una condición sobre la cuenta de cada grupo va en el `HAVING`:

```sql
SELECT j.id, j.title, COUNT(*) AS applications
FROM jobs AS j
JOIN applications AS a ON a.job_id = j.id
GROUP BY j.id, j.title
HAVING COUNT(*) >= 2;
```

`HAVING COUNT(*) > 1` también pasa: con números enteros, es la misma condición. `HAVING applications >= 2`, con el alias, también pasa en SQLite, pero PostgreSQL lo rechaza (ver 💼).

### Tarea 2 · En el `HAVING`, una columna sin agregar mira una sola fila del grupo
```text
02_active_candidates.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 6
  Esperadas que no salieron:
    (1, 'Ana Quispe', 2)
  Obtenidas que no se esperaban:
    (1, 'Ana Quispe', 3)
    (5, 'Sofía Castro', 2)
```

6 filas. No pasa porque el `HAVING` se revisa una vez por grupo, después de agrupar, y `a.status` no está en el `GROUP BY` ni dentro de una función de agregado: es una columna suelta, como la del lab 2.4, y SQLite toma el valor de una de las filas del grupo. Con estos datos, Ana Quispe sale con sus 3 postulaciones, la rechazada incluida, y Sofía Castro sale aunque una de sus dos postulaciones fue rechazada; Luis Ramírez (6), con la misma mezcla que Sofía, no sale. Qué fila mira SQLite no está garantizado: estas filas salieron en las tres versiones probadas, pero otra versión podría dar otras, igual de equivocadas. La condición sobre cada postulación tiene que quitar las rechazadas antes de agrupar, en el `WHERE`, y el `HAVING` cuenta lo que quedó:

```sql
SELECT c.id, c.name, COUNT(*) AS applications
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
WHERE a.status <> 'rechazada'
GROUP BY c.id, c.name
HAVING COUNT(*) >= 2;
```

`a.status != 'rechazada'` y `a.status IN ('enviada', 'entrevista', 'contratada')` también pasan. `GROUP BY c.name` no pasa: los dos Luis Ramírez quedan juntos con 3 postulaciones vigentes, como en la tarea 3 del lab 2.4.

### Tarea 3 · Después del `JOIN`, cada oferta se repite una vez por postulación
```text
03_jobs_and_applications_by_company.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 6; obtenidas: 6
  Esperadas que no salieron:
    ('Andes Retail', 3, 6)
    ('Pago Fácil', 2, 3)
    ('Agro Norte', 2, 3)
    ('Banco Sur', 2, 2)
  Obtenidas que no se esperaban:
    ('Andes Retail', 6, 6)
    ('Pago Fácil', 3, 3)
    ('Agro Norte', 4, 3)
    ('Banco Sur', 3, 2)
```

Cuatro empresas. El segundo `LEFT JOIN` arma una fila por postulación, y cada una lleva los datos de su oferta: la oferta 1 de Andes Retail aparece en 3 filas, una por cada postulación suya. `COUNT(j.id)` cuenta esas filas, no las ofertas. Que una fila de la tabla de arriba se repita una vez por cada fila relacionada de la tabla de abajo se llama abanico (*fan-out*). Clínica Central sale bien por casualidad: cada una de sus dos ofertas tiene una sola postulación. Nube Andina también, porque `COUNT(j.id)` no cuenta su fila con `NULL`. Para contar ofertas, cada `j.id` tiene que contar una vez:

```sql
SELECT c.name AS company, COUNT(DISTINCT j.id) AS jobs, COUNT(a.id) AS applications
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN applications AS a ON a.job_id = j.id
GROUP BY c.id, c.name;
```

`COUNT(DISTINCT a.id)` en `applications` también pasa: cada postulación ya sale una vez. `COUNT(*)` en `applications` no pasa, por la fila con `NULL` de la tarea 4 del lab 2.4.

### Tarea 4 · `DISTINCT` junta sueldos iguales de ofertas distintas: agrega antes de unir
```text
04_salary_and_applications_by_company.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 5
  Esperadas que no salieron:
    ('Agro Norte', 1200, 3)
  Obtenidas que no se esperaban:
    ('Agro Norte', 600, 3)
```

Una empresa: Agro Norte sale con 600 en lugar de 1200. `SUM(DISTINCT j.salary_usd)` suma cada sueldo distinto una vez, y las dos ofertas de Agro Norte pagan 600: `DISTINCT` no sabe que vienen de ofertas distintas. En las otras cuatro empresas no hay dos sueldos iguales y el error no se nota. Con `COUNT(DISTINCT j.id)` funcionaba porque `j.id` es distinto en cada oferta; un sueldo no. Y sin `DISTINCT` es peor: `SUM(j.salary_usd)` da 6600 para Andes Retail en lugar de 2700, porque suma el sueldo de cada oferta una vez por cada postulación.

La salida es agregar antes de unir: contar las postulaciones de cada oferta en una subconsulta, que devuelve una fila por oferta, y unir ese resumen con `jobs`. Así cada oferta aparece una sola vez y su sueldo se suma una vez:

```sql
SELECT c.name AS company, SUM(j.salary_usd) AS total_salary, SUM(per_job.applications) AS applications
FROM companies AS c
JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN (
    SELECT job_id, COUNT(*) AS applications
    FROM applications
    GROUP BY job_id
) AS per_job ON per_job.job_id = j.id
GROUP BY c.id, c.name;
```

`SUM(per_job.applications)` suma las cuentas de las ofertas de cada empresa. El `LEFT JOIN` hace falta: con `JOIN`, las ofertas 10 y 11, que no tienen postulaciones, se pierden con sus sueldos, y Banco Sur sale con 2400 en lugar de 4150. `COUNT(per_job.applications)` en lugar de `SUM` no pasa: cuenta ofertas con postulaciones, no postulaciones. También pasa la versión al revés: sumar los sueldos de cada empresa en una subconsulta sobre `jobs` y contar las postulaciones con los `LEFT JOIN` de la tarea 3.
</details>

La solución completa está en [`solution/`](solution/).
