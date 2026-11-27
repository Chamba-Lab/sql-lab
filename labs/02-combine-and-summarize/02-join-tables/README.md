# 🧩 2.2 · Unir tablas

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Juntar en una sola consulta los datos de dos tablas relacionadas con `JOIN … ON`.
- Escribir la condición del `ON` que sigue la clave foránea correcta, y decir de qué tabla es cada columna.
- Acortar una consulta con alias de tabla.
- Unir tres o cuatro tablas, también a través de una tabla intermedia.
- Unir una tabla consigo misma (*self-join*).

## 💡 Por qué importa
En el lab 2.1 repartiste los datos en varias tablas y seguiste cada referencia a mano, con una consulta por paso. Casi todas las preguntas reales cruzan tablas: qué empresa publicó cada oferta, quién postuló a qué, quién recomendó a quién. `JOIN` hace ese cruce en una sola consulta, para todas las filas a la vez, y es la palabra de SQL que más se pregunta en las entrevistas. Escribirlo bien pide saber qué columna apunta a cuál, y eso es lo que practicas aquí.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/02-combine-and-summarize/02-join-tables/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la base del [lab 2.1](../01-table-relationships/README.md), la misma de las tareas. No hace falta correrlos; si quieres probarlos, crea la base y abre la consola como en el experimento 1 de ese lab.

### Unir dos tablas (*JOIN*)
En el experimento 2 del lab 2.1, saber de qué empresa era la oferta 4 te tomó dos consultas: una para leer su `company_id` y otra para buscar ese `id` en `companies`. Para las 10 ofertas, sería una consulta más por cada oferta.

La idea: pedirle a la base que, para cada oferta, busque en `companies` la fila cuyo `id` es el `company_id` de la oferta, y ponga las dos juntas en una sola fila del resultado. En SQL se escribe con **`JOIN`** (unir) después de la primera tabla, y la condición que dice qué fila va con cuál, después de **`ON`**:

```sql
SELECT jobs.title, companies.name, companies.city
FROM jobs
JOIN companies ON jobs.company_id = companies.id
WHERE jobs.mode = 'remoto'
ORDER BY jobs.id;
```

| title | name | city |
|---|---|---|
| Desarrollador backend | Pago Fácil | Bogotá |
| Desarrolladora full stack | Pago Fácil | Bogotá |
| Analista de calidad (QA) | Clínica Central | Arequipa |

Cada fila trae el título de la oferta, de `jobs`, y el nombre y la ciudad de su empresa, de `companies`. La condición del `ON` es la que seguiste a mano: la clave foránea de una tabla igual a la clave primaria de la otra. El `WHERE` va después del `JOIN` y filtra el resultado ya unido, así que puede usar columnas de las dos tablas; el `ORDER BY` sigue al final, como en el [lab 1.5](../../01-query-a-table/05-sort-and-paginate/README.md).

Este `JOIN` se llama también **`INNER JOIN`** (unión interna): `JOIN` solo y `INNER JOIN` son lo mismo. Solo deja las filas que encontraron pareja: Nube Andina, que no tiene ofertas, no sale en ningún `JOIN` de `jobs` con `companies`. Recuperar las filas sin pareja es el tema del lab 2.3.

### De qué tabla es cada columna (`tabla.columna`)
`jobs.title` es la columna `title` de la tabla `jobs`. Con una sola tabla no hacía falta decirlo, pero ahora `jobs` y `companies` tienen las dos una columna `id`. Si escribes `id` solo, SQLite no sabe cuál quieres y da un error:

```text
ambiguous column name: id
```

*Ambiguous* es ambiguo: hay más de una columna con ese nombre. Una columna que existe en una sola de las tablas, como `title`, se puede escribir sin la tabla delante, pero ponerla siempre hace la consulta más fácil de leer.

Fíjate también en el nombre de la segunda columna del resultado: es `name`, sin la tabla. Si quieres otro, usa un alias de columna con `AS`, como en el [lab 1.2](../../01-query-a-table/02-first-queries/README.md).

### Alias de tabla (*table alias*)
Repetir `companies.` en cada columna alarga la consulta. Igual que una columna, una tabla puede llevar un alias, escrito con `AS` justo después de su nombre en el `FROM` o en el `JOIN`. Desde ahí, la consulta la nombra por el alias:

```sql
SELECT j.title, c.name, c.city
FROM jobs AS j
JOIN companies AS c ON j.company_id = c.id
WHERE j.mode = 'remoto'
ORDER BY j.id;
```

Devuelve lo mismo que la consulta anterior. Como con las columnas, `AS` es opcional (`FROM jobs j` también funciona), pero escrito se lee mejor. Una vez que le pones alias a una tabla, su nombre completo deja de servir en esa consulta: `jobs.title` con `FROM jobs AS j` da `no such column: jobs.title`.

### Más de dos tablas
Cada `JOIN` agrega una tabla con su propio `ON`, que la conecta con alguna de las que ya están. Las postulaciones a las ofertas de Banco Sur necesitan tres tablas: `applications` apunta a `jobs`, y `jobs` apunta a `companies`.

```sql
SELECT a.id, j.title, a.status
FROM applications AS a
JOIN jobs AS j ON a.job_id = j.id
JOIN companies AS c ON j.company_id = c.id
WHERE c.name = 'Banco Sur'
ORDER BY a.id;
```

| id | title | status |
|---|---|---|
| 10 | Administrador de bases de datos | entrevista |
| 15 | Administrador de bases de datos | enviada |

`companies` no aparece en el `SELECT`: está en la consulta solo para que el `WHERE` pueda filtrar por el nombre de la empresa. La oferta 10 de Banco Sur no sale porque nadie postuló a ella.

### Una tabla consigo misma (*self-join*)
A veces las dos filas que quieres juntar están en la misma tabla. ¿Qué otras ofertas tiene la empresa de la oferta 4? Hay que unir `jobs` con `jobs`. Para que la consulta distinga las dos, cada una lleva su propio alias, como si fueran dos copias de la tabla: `a` es la oferta 4 y `b`, las ofertas de su misma empresa.

```sql
SELECT b.id, b.title
FROM jobs AS a
JOIN jobs AS b ON b.company_id = a.company_id
WHERE a.id = 4
ORDER BY b.id;
```

| id | title |
|---|---|
| 1 | Analista de datos júnior |
| 4 | Analista de BI |
| 9 | Practicante de marketing digital |

La oferta 4 sale también, porque es de su misma empresa. Sin los alias, cada columna sería ambigua: las dos copias tienen las mismas columnas.

## 📚 Documentación
- [SQLite: la cláusula `FROM` y los `JOIN`](https://www.sqlite.org/lang_select.html#fromclause)
- [PostgreSQL: la cláusula `FROM` de `SELECT`](https://www.postgresql.org/docs/current/sql-select.html#SQL-FROM), con la condición que pide cada tipo de `JOIN`

## 🧭 Escenario
La bolsa de trabajo del lab 2.1 quiere sus primeros reportes que cruzan tablas: las ofertas con su empresa, las entrevistas, el historial de un postulante y la red de recomendaciones. Te pide cuatro consultas.

### La base
Son las cuatro tablas del [lab 2.1](../01-table-relationships/README.md#-escenario), con los mismos datos. Este es su diagrama en texto:

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
├── queries/                    tus cuatro consultas, una por tarea
│   ├── 01_jobs_with_company.sql
│   ├── 02_interviews.sql
│   ├── 03_candidate_history.sql
│   └── 04_referrals.sql
├── seed.sql                    crea las cuatro tablas y sus filas
├── tests/
│   ├── conftest.py             prepara la base y compara resultados
│   └── test_queries.py         las pruebas: una clase por tarea
└── pyproject.toml              le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../../01-query-a-table/02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). Ninguna tarea pide un orden: las filas pueden salir en cualquiera. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 4, una por tarea.

### Tarea 1 · Las ofertas con su empresa
**Objetivo:** cada oferta con el nombre y el sector de la empresa que la publicó. Columnas `id` (el de la oferta), `title`, `company` (el nombre de la empresa) y `sector`, con las 10 ofertas. **Lo valida:** [`TestTask1JobsWithCompany`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta y se olvidó del `ON`. ¿Crees que da un error o que devuelve filas? Si devuelve filas, ¿cuántas? Escribe tu predicción y después pon la consulta en [`queries/01_jobs_with_company.sql`](starter/queries/01_jobs_with_company.sql):

```sql
SELECT jobs.id, jobs.title, companies.name AS company, companies.sector
FROM jobs
JOIN companies;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva cada oferta con su empresa, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1JobsWithCompany` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 3 fallan.

### Tarea 2 · Las entrevistas
**Objetivo:** las postulaciones en estado `entrevista`, con el nombre de la persona y el título de la oferta. Columnas `candidate` (el nombre de la persona), `title` y `applied_on`. **Lo valida:** [`TestTask2Interviews`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Qué crees que devuelve: cuántas filas, y con qué personas? Escribe tu predicción y después pon la consulta en [`queries/02_interviews.sql`](starter/queries/02_interviews.sql):

```sql
SELECT c.name AS candidate, j.title, a.applied_on
FROM applications AS a
JOIN candidates AS c ON a.id = c.id
JOIN jobs AS j ON a.job_id = j.id
WHERE a.status = 'entrevista';
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva las 5 entrevistas que pide la tarea, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2Interviews` pasa. Con todas las pruebas, 3 pasan y 2 fallan.

### Tarea 3 · El historial de un postulante
**Objetivo:** las postulaciones del postulante con `id` 6, con el título de cada oferta, el nombre de su empresa y el estado. Columnas `title`, `company` y `status`. **Lo valida:** [`TestTask3CandidateHistory`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero buscó en `candidates` cómo se llama el postulante 6, unió las cuatro tablas y filtró por ese nombre. ¿Cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/03_candidate_history.sql`](starter/queries/03_candidate_history.sql):

```sql
SELECT j.title, co.name AS company, a.status
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
JOIN jobs AS j ON a.job_id = j.id
JOIN companies AS co ON j.company_id = co.id
WHERE c.name = 'Luis Ramírez';
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva solo el historial que pide la tarea, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3CandidateHistory` pasa. Con todas las pruebas, 4 pasan y 1 falla.

### Tarea 4 · Quién recomendó a quién
**Objetivo:** cada postulante que fue recomendado por alguien, con el nombre de quien lo recomendó. Columnas `candidate` (la persona recomendada) y `recommender` (quien la recomendó). Une `candidates` consigo misma. **Lo valida:** [`TestTask4Referrals`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿En qué columna crees que aparece Carmen Rojas, `candidate` o `recommender`, y qué nombre sale a su lado? Escribe tu predicción y después pon la consulta en [`queries/04_referrals.sql`](starter/queries/04_referrals.sql):

```sql
SELECT c.name AS candidate, r.name AS recommender
FROM candidates AS c
JOIN candidates AS r ON c.id = r.referred_by;
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva a cada persona recomendada con quien la recomendó, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask4Referrals` pasa: las 5 pruebas pasan.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `FROM a JOIN b ON <condición>` | Junta cada fila de `a` con las filas de `b` que cumplen la condición |
| `ON a.b_id = b.id` | La condición de siempre: la clave foránea de una tabla igual a la clave primaria de la otra |
| `INNER JOIN` | Lo mismo que `JOIN`: solo quedan las filas que tienen pareja |
| `tabla.columna` | Dice de qué tabla es la columna; obligatorio cuando el nombre está en las dos |
| `FROM jobs AS j` | Alias de tabla: desde ahí, la consulta escribe `j.title`, no `jobs.title` |
| `… JOIN b ON … JOIN c ON …` | Cada `JOIN` agrega una tabla con su propio `ON` |
| `FROM t AS x JOIN t AS y ON …` | *Self-join*: la misma tabla dos veces, con dos alias |
| `SELECT … FROM … JOIN … ON … WHERE … ORDER BY … LIMIT …` | El orden en que se escriben las partes |

## 💼 En proyectos reales
- **La forma antigua con comas.** Vas a ver consultas que unen así: `FROM jobs, companies WHERE jobs.company_id = companies.id`. Da el mismo resultado que el `JOIN … ON`, pero mezcla la condición de la unión con los filtros del `WHERE`, y si se olvida, pasa lo mismo que en la tarea 1. Escribe `JOIN … ON`: cada condición queda junto a la tabla que conecta.
- **Un `JOIN` sin `ON` no se trata igual en todos los motores de bases de datos** (los programas que guardan y consultan los datos, como SQLite, MySQL y PostgreSQL). SQLite y MySQL lo aceptan ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/join.html)); PostgreSQL exige una condición en todo `JOIN` interno o externo ([PostgreSQL](https://www.postgresql.org/docs/current/sql-select.html#SQL-FROM)): un `ON`, o bien `USING` o `NATURAL`, formas que no usas todavía.
- **El *self-join* es una pregunta clásica de entrevista:** «una tabla `employees` tiene `manager_id`; lista cada empleado con el nombre de su jefe». Es la tarea 4 con otros nombres.
- **Antes de unir, mira el diagrama de la base.** El `ON` correcto casi siempre es una clave foránea y la clave primaria a la que apunta. Si una consulta une dos `id` entre sí o dos columnas que no se apuntan, sospecha.

## 🆘 Pistas
<details><summary>Pista 1 · Salen muchas más filas que ofertas</summary>

Sin `ON`, ¿qué le dice la consulta a la base sobre qué empresa va con qué oferta? En Conceptos, ¿qué columna de `jobs` apunta a `companies`?
</details>

<details><summary>Pista 2 · <code>ambiguous column name</code></summary>

Una columna con ese nombre está en más de una de las tablas que uniste. Escribe delante la tabla, o su alias: `jobs.id` o `j.id`.
</details>

<details><summary>Pista 3 · Salen menos entrevistas, o con la persona equivocada</summary>

Mira el `ON` de `candidates`. ¿Qué columna de `applications` guarda a quién pertenece la postulación? ¿Es `id`?
</details>

<details><summary>Pista 4 · Salen postulaciones de más en el historial</summary>

¿Cuántas personas se llaman Luis Ramírez en `candidates`? ¿Qué dato distingue a la de Lima de la otra?
</details>

<details><summary>Pista 5 · Los nombres salen al revés</summary>

En la tabla de `candidates`, Carmen Rojas tiene `referred_by` 3. ¿Cuál de los dos alias es Carmen, y cuál es la persona 3? Escribe el `ON` como esa frase: «el `referred_by` de la persona recomendada es el `id` de quien la recomendó».
</details>

<details><summary>Pista 6 · <code>no such column</code> con el nombre de una tabla delante</summary>

Si le pusiste alias a esa tabla, usa el alias: con `FROM jobs AS j`, la columna es `j.title`.
</details>

## 🎤 Autoevaluación
1. Una tabla `orders` tiene 200 filas y `customers` tiene 50. ¿Cuántas filas devuelve `SELECT * FROM orders JOIN customers` en SQLite, y por qué es casi seguro un error?
2. `orders` y `customers` tienen las dos una columna `id`. ¿Qué pasa con `SELECT id, name FROM orders JOIN customers ON orders.customer_id = customers.id`, y cómo lo arreglas?
3. ¿Qué diferencia hay entre `JOIN` e `INNER JOIN`?
4. Tienes `students`, `courses` y la tabla intermedia `enrollments (student_id, course_id)`. Escribe la consulta que lista el nombre de cada alumno con el nombre de cada curso que lleva.
5. Una tabla `employees (id, name, manager_id)` guarda en `manager_id` el `id` del jefe. Escribe la consulta que lista a cada empleado con el nombre de su jefe. ¿Salen los empleados sin jefe?

<details><summary>Respuestas</summary>

1. 10 000 filas (200 × 50): sin `ON`, cada pedido se junta con cada cliente, el producto cartesiano. Casi nunca es lo que se quiere; lo correcto es `ON orders.customer_id = customers.id`, que da una fila por pedido. PostgreSQL ni siquiera lo acepta: exige una condición.
2. Da `ambiguous column name: id`, porque SQLite no sabe de qué tabla es ese `id`. Se arregla escribiendo la tabla delante: `orders.id` o `customers.id`, según cuál pide la pregunta.
3. Ninguna: `INNER` es opcional. Los dos dejan solo las filas que tienen pareja en la otra tabla.
4. `SELECT s.name, c.name FROM enrollments AS e JOIN students AS s ON e.student_id = s.id JOIN courses AS c ON e.course_id = c.id;` (también se puede empezar por `students`, siempre que cada `ON` siga una clave foránea).
5. `SELECT e.name AS employee, m.name AS manager FROM employees AS e JOIN employees AS m ON e.manager_id = m.id;`. Los empleados sin jefe (con `manager_id` en `NULL`) no salen: el `JOIN` solo deja las filas con pareja. Mostrarlos es el tema del lab 2.3.
</details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · Sin `ON`, cada oferta va con cada empresa
```text
01_jobs_with_company.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 10; obtenidas: 60
  Esperadas que no salieron:
    (ninguna)
  Obtenidas que no se esperaban:
    (1, 'Analista de datos júnior', 'Pago Fácil', 'fintech')
    (1, 'Analista de datos júnior', 'Clínica Central', 'salud')
    (1, 'Analista de datos júnior', 'Agro Norte', 'agroindustria')
    (1, 'Analista de datos júnior', 'Banco Sur', 'banca')
    (1, 'Analista de datos júnior', 'Nube Andina', 'tecnología')
    (2, 'Desarrollador backend', 'Andes Retail', 'retail')
    … (y 44 filas más, en el orden en que las devuelva la base)
```

Devuelve filas, sin error: 60, que son 10 ofertas × 6 empresas. Sin una condición, la base junta cada oferta con cada empresa, también con Nube Andina, que no tiene ofertas. A eso se le llama **producto cartesiano** (*cartesian product*): todas las parejas posibles. Así se define todo `JOIN` (la [documentación de SQLite](https://www.sqlite.org/lang_select.html#fromclause) dice que todos parten del producto cartesiano): conceptualmente, arma todas las parejas y el `ON` se queda con las que cumplen la condición. La base no llega a armar las 60 filas para eso; cómo busca de verdad se ve en el bloque 5. Las 10 filas correctas están entre las 60, por eso ninguna «esperada» falta. Con el `ON`:

```sql
SELECT jobs.id, jobs.title, companies.name AS company, companies.sector
FROM jobs
JOIN companies ON jobs.company_id = companies.id;
```

Si escribiste `id` sin la tabla delante, viste `ambiguous column name: id`: `jobs` y `companies` tienen las dos un `id`, y la tarea pide el de la oferta. Y `ON jobs.id = companies.id` tampoco sirve: devuelve 6 filas, cada oferta con la empresa que tiene su mismo número. Las ofertas 1, 2 y 3 salen con su empresa por casualidad, porque su `company_id` coincide con su `id`; las ofertas 4, 5 y 6 salen con otra empresa (la 4, con Agro Norte, aunque es de Andes Retail), y las ofertas 7 a 10 desaparecen.

### Tarea 2 · Unir por la columna equivocada no da error
```text
02_interviews.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 3
  Esperadas que no salieron:
    ('Luis Ramírez', 'Desarrollador backend', '2026-11-06')
    ('Jorge Huamán', 'Practicante de datos', '2026-11-12')
    ('Sofía Castro', 'Administrador de bases de datos', '2026-11-19')
    ('Valeria Paredes', 'Analista de BI', '2026-11-12')
  Obtenidas que no se esperaban:
    ('Jorge Huamán', 'Desarrollador backend', '2026-11-06')
    ('Valeria Paredes', 'Practicante de datos', '2026-11-12')
```

No: devuelve 3, y dos con la persona equivocada. `a.id = c.id` junta la postulación 4 con la persona 4 (Jorge), aunque la postulación 4 es de Luis Ramírez, y las postulaciones 10 y 14 desaparecen porque no hay personas con esos `id`. La única fila correcta, la de Ana, lo es por casualidad: la postulación 1 es de la persona 1. El `id` de una postulación no dice nada de quién la envió; lo dice su clave foránea, `candidate_id`:

```sql
SELECT c.name AS candidate, j.title, a.applied_on
FROM applications AS a
JOIN candidates AS c ON a.candidate_id = c.id
JOIN jobs AS j ON a.job_id = j.id
WHERE a.status = 'entrevista';
```

`applications` es la tabla intermedia del lab 2.1: une a cada persona con cada oferta, así que la consulta pasa por ella para llegar de `candidates` a `jobs`.

### Tarea 3 · Un nombre no identifica a una persona
```text
03_candidate_history.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 2; obtenidas: 4
  Esperadas que no salieron:
    (ninguna)
  Obtenidas que no se esperaban:
    ('Desarrollador backend', 'Pago Fácil', 'entrevista')
    ('Desarrolladora full stack', 'Pago Fácil', 'enviada')
```

4 filas: las 2 del Luis de Lima y las 2 del Luis de Bogotá. Los `JOIN` están bien; el problema es el filtro, porque el nombre se repite. Identifica a la persona por su clave primaria, como en el experimento 4 del lab 2.1:

```sql
SELECT j.title, co.name AS company, a.status
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
JOIN jobs AS j ON a.job_id = j.id
JOIN companies AS co ON j.company_id = co.id
WHERE c.id = 6;
```

`WHERE c.name = 'Luis Ramírez' AND c.city = 'Lima'` también pasa con estos datos, pero solo mientras no llegue otro Luis Ramírez de Lima. Y como `applications` ya guarda el `candidate_id`, puedes saltarte `candidates` y filtrar con `WHERE a.candidate_id = 6`.

### Tarea 4 · En un *self-join*, el `ON` dice quién es quién
```text
04_referrals.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 5
  Esperadas que no salieron:
    ('María Torres', 'Ana Quispe')
    ('Jorge Huamán', 'Ana Quispe')
    ('Luis Ramírez', 'Jorge Huamán')
    ('Carmen Rojas', 'María Torres')
    ('Valeria Paredes', 'Sofía Castro')
  Obtenidas que no se esperaban:
    ('Ana Quispe', 'María Torres')
    ('Ana Quispe', 'Jorge Huamán')
    ('Jorge Huamán', 'Luis Ramírez')
    ('María Torres', 'Carmen Rojas')
    ('Sofía Castro', 'Valeria Paredes')
```

Carmen sale en `recommender`, al lado de María Torres: al revés. Las 5 parejas son las correctas, pero cada pareja está invertida. `c.id = r.referred_by` dice que `r` es la persona recomendada por `c`, y el `SELECT` llama `candidate` a `c`. El `ON` tiene que decir lo que la tarea pide: el `referred_by` de la persona (`c`) es el `id` de quien la recomendó (`r`):

```sql
SELECT c.name AS candidate, r.name AS recommender
FROM candidates AS c
JOIN candidates AS r ON c.referred_by = r.id;
```

Las 4 personas sin `referred_by` no salen como `candidate`: su `NULL` no es igual a ningún `id`. Y sin los alias, `FROM candidates JOIN candidates` da `ambiguous column name`, porque las dos copias tienen las mismas columnas.
</details>

La solución completa está en [`solution/`](solution/).
