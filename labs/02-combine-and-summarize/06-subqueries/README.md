# 🧩 2.6 · Subconsultas

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Comparar cada fila con un valor que calcula otra consulta.
- Filtrar filas según una lista que devuelve otra consulta, con `IN` y `NOT IN`.
- Escribir una subconsulta que usa los datos de cada fila de la consulta de afuera.
- Preguntar si existe alguna fila relacionada, con `EXISTS` y `NOT EXISTS`.
- Leer una consulta con subconsultas de adentro hacia afuera, corriendo cada parte sola.

## 💡 Por qué importa
Muchas preguntas se responden en dos pasos: primero un dato (el sueldo más alto, el promedio, la lista de ofertas remotas) y después las filas que se comparan con ese dato. Con una subconsulta escribes los dos pasos en una sola consulta, sin copiar a mano el resultado del primero. Las preguntas de entrevista «los que ganan más que el promedio», «los que nunca compraron» y «el segundo sueldo más alto» se resuelven así.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/02-combine-and-summarize/06-subqueries/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la base de las tareas, que es la misma del [lab 2.1](../01-table-relationships/README.md) (ver [La base](#la-base)). No hace falta correrlos; si quieres probarlos, crea la base y abre la consola como en el [experimento 1 del lab 2.1](../01-table-relationships/README.md#experimento-1--crear-la-base-y-ver-sus-tablas): dan las mismas filas.

En el [lab 2.5](../05-filter-groups/README.md#una-consulta-agrupada-dentro-del-from) escribiste una consulta entre paréntesis dentro del `FROM` de otra, y la llamaste subconsulta (*subquery*). Una subconsulta también puede ir en el `WHERE` o en el `SELECT`, y según dónde va, su resultado se usa como un valor, como una lista o como una respuesta de sí o no.

### Un valor calculado por otra consulta (*scalar subquery*)
¿Quiénes tienen más años de experiencia que el promedio? Con lo del lab 2.4 calculas el promedio:

```sql
SELECT AVG(years_experience) FROM candidates;
```

| AVG(years_experience) |
|---|
| 1.7222222222222223 |

Podrías copiar ese número en un `WHERE`, pero cambiaría con cada persona nueva y tendrías que copiarlo otra vez. La idea: escribir la consulta del promedio entre paréntesis en el lugar donde iría el número. La base corre primero la de adentro y compara cada fila con su resultado:

```sql
SELECT name, years_experience
FROM candidates
WHERE years_experience > (SELECT AVG(years_experience) FROM candidates);
```

| name | years_experience |
|---|---|
| Luis Ramírez | 2.0 |
| Sofía Castro | 3.5 |
| Diego Flores | 4.0 |
| Valeria Paredes | 2.5 |

La subconsulta de este ejemplo devuelve una fila con una columna, es decir, un solo valor, y el `WHERE` la usa como si fuera un número escrito a mano. Una subconsulta que se usa como un valor se llama **subconsulta escalar** (*scalar subquery*; escalar quiere decir «un solo valor»).

### Una lista calculada por otra consulta (`IN` y `NOT IN`)
¿Qué empresas tienen alguna oferta remota? En el [lab 1.3](../../01-query-a-table/03-filter-rows/README.md) usaste `IN` con una lista escrita a mano, como `city IN ('Lima', 'Bogotá')`. Aquí la lista son los `company_id` de las ofertas remotas, y está en otra tabla:

```sql
SELECT company_id FROM jobs WHERE mode = 'remoto';
```

| company_id |
|---|
| 2 |
| 2 |
| 3 |

La idea: poner esa consulta entre paréntesis en lugar de la lista. `IN` pregunta, para cada empresa, si su `id` está en lo que devuelve la subconsulta:

```sql
SELECT name
FROM companies
WHERE id IN (SELECT company_id FROM jobs WHERE mode = 'remoto');
```

| name |
|---|
| Pago Fácil |
| Clínica Central |

Con `NOT IN` la pregunta es la contraria. Con estos datos, salen las 4 empresas cuyo `id` no está en esa lista:

```sql
SELECT name
FROM companies
WHERE id NOT IN (SELECT company_id FROM jobs WHERE mode = 'remoto');
```

| name |
|---|
| Andes Retail |
| Agro Norte |
| Banco Sur |
| Nube Andina |

La subconsulta de un `IN` devuelve una sola columna, con las filas que salgan.

### Una subconsulta que mira la fila de afuera (*correlated subquery*)
¿Cuántas postulaciones hizo cada persona? Las subconsultas de arriba se calculan una sola vez, porque no dependen de qué fila se está revisando afuera. Esta pregunta necesita una cuenta distinta para cada persona.

La idea: dentro de la subconsulta, usar una columna de la tabla de afuera. Aquí la subconsulta va en el `SELECT`, `c` es el alias de la tabla de afuera y `a` el de la de adentro:

```sql
SELECT c.name,
       (SELECT COUNT(*) FROM applications AS a WHERE a.candidate_id = c.id) AS applications
FROM candidates AS c;
```

| name | applications |
|---|---|
| Ana Quispe | 3 |
| Luis Ramírez | 2 |
| María Torres | 2 |
| Jorge Huamán | 2 |
| Sofía Castro | 2 |
| Luis Ramírez | 2 |
| Carmen Rojas | 1 |
| Diego Flores | 0 |
| Valeria Paredes | 2 |

`c.id` viene de la consulta de afuera: para la fila de Ana Quispe vale 1, y la subconsulta cuenta las postulaciones con `candidate_id` 1; para la fila de Luis Ramírez vale 2, y así con cada persona. La subconsulta se calcula una vez por cada fila de afuera. Una subconsulta que usa columnas de la consulta de afuera se llama **subconsulta correlacionada** (*correlated subquery*). Diego Flores sale con 0, sin el `LEFT JOIN` que necesitó la tarea 4 del lab 2.4: la subconsulta cuenta y no encuentra filas.

### ¿Existe alguna fila? (`EXISTS` y `NOT EXISTS`)
¿Qué ofertas no recibieron ninguna postulación? Para cada oferta, la pregunta es de sí o no: ¿hay al menos una fila en `applications` con su `job_id`?

La idea: una subconsulta correlacionada que busca esas filas, y una palabra que responde solo si encontró alguna. `EXISTS (subconsulta)` es verdadero si la subconsulta devuelve una fila o más, y `NOT EXISTS (subconsulta)` si no devuelve ninguna:

```sql
SELECT j.id, j.title
FROM jobs AS j
WHERE NOT EXISTS (
    SELECT 1
    FROM applications AS a
    WHERE a.job_id = j.id
);
```

| id | title |
|---|---|
| 10 | Analista de riesgos |

`SELECT 1` es una costumbre: a `EXISTS` no le importan las columnas que devuelve la subconsulta, solo si devuelve filas, así que se escribe un valor cualquiera. Con `EXISTS` en lugar de `NOT EXISTS` salen las otras 9 ofertas.

## 📚 Documentación
- [SQLite: subconsultas](https://www.sqlite.org/lang_expr.html#subq), en inglés: qué devuelve una subconsulta usada como valor
- [SQLite: `IN` y `NOT IN`](https://www.sqlite.org/lang_expr.html#in_op), en inglés, con la tabla de resultados de cada caso
- [SQLite: `EXISTS`](https://www.sqlite.org/lang_expr.html#exists_op), en inglés
- [PostgreSQL: expresiones con subconsultas](https://www.postgresql.org/docs/current/functions-subquery.html), en inglés: `EXISTS`, `IN` y `NOT IN`, con ejemplos

## 🧭 Escenario
La bolsa de trabajo quiere comparar ofertas y personas: las ofertas que pagan más que la competencia, quiénes buscan trabajo remoto, qué ofertas pagan bien dentro de su empresa y quiénes todavía no recomendaron a nadie. Te pide cuatro consultas.

### La base
Son las cuatro tablas del [lab 2.1](../01-table-relationships/README.md#-escenario), con los mismos datos de los labs 2.2 a 2.4. Este es su diagrama en texto:

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
├── queries/                                  tus cuatro consultas, una por tarea
│   ├── 01_jobs_above_andes_retail.sql
│   ├── 02_remote_applicants.sql
│   ├── 03_jobs_above_company_average.sql
│   └── 04_candidates_who_referred_nobody.sql
├── seed.sql                                  crea las cuatro tablas y sus filas
├── tests/
│   ├── conftest.py                           prepara la base y compara resultados
│   └── test_queries.py                       las pruebas: una clase por tarea
└── pyproject.toml                            le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Una subconsulta va dentro de esa consulta, así que sigue siendo una sola. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../../01-query-a-table/02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). Ninguna tarea pide un orden: las filas pueden salir en cualquiera. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 4, una por tarea.

### Tarea 1 · Las ofertas que pagan más que Andes Retail
**Objetivo:** las ofertas que pagan más que la oferta mejor pagada de Andes Retail (la empresa 1). Columnas `id`, `title` y `salary_usd`, 4 filas. **Lo valida:** [`TestTask1JobsAboveAndesRetail`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Qué crees que pasa: pasa la prueba, devuelve otras filas o da un error? Si devuelve otras filas, ¿cuántas? Escribe tu predicción y después pon la consulta en [`queries/01_jobs_above_andes_retail.sql`](starter/queries/01_jobs_above_andes_retail.sql):

```sql
SELECT id, title, salary_usd
FROM jobs
WHERE salary_usd > (SELECT salary_usd FROM jobs WHERE company_id = 1);
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1JobsAboveAndesRetail` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 3 fallan.

### Tarea 2 · Quiénes postularon a una oferta remota
**Objetivo:** las personas que postularon a alguna oferta remota (`mode` igual a `'remoto'`). Columnas `id` y `name` (de la persona), 3 filas. **Lo valida:** [`TestTask2RemoteApplicants`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero lo resolvió con dos `JOIN`, como en el lab 2.2. ¿Crees que pasa la prueba? Si no pasa, ¿cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/02_remote_applicants.sql`](starter/queries/02_remote_applicants.sql):

```sql
SELECT c.id, c.name
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
JOIN jobs AS j ON j.id = a.job_id
WHERE j.mode = 'remoto';
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que use una subconsulta y dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2RemoteApplicants` pasa. Con todas las pruebas, 3 pasan y 2 fallan.

### Tarea 3 · Las ofertas que pagan más que el promedio de su empresa
**Objetivo:** las ofertas que pagan más que el promedio de las ofertas de su propia empresa, calculado con `AVG`. Columnas `id`, `title` y `salary_usd`, 4 filas. **Lo valida:** [`TestTask3JobsAboveCompanyAverage`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Crees que pasa la prueba? Si no pasa, ¿cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/03_jobs_above_company_average.sql`](starter/queries/03_jobs_above_company_average.sql):

```sql
SELECT id, title, salary_usd
FROM jobs
WHERE salary_usd > (
    SELECT AVG(salary_usd)
    FROM jobs
    WHERE company_id = company_id
);
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3JobsAboveCompanyAverage` pasa. Con todas las pruebas, 4 pasan y 1 falla.

### Tarea 4 · Quiénes no recomendaron a nadie
**Objetivo:** las personas que no recomendaron a nadie: su `id` no aparece en el `referred_by` de ninguna persona. Columnas `id` y `name`, 5 filas. **Lo valida:** [`TestTask4CandidatesWhoReferredNobody`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Crees que pasa la prueba? Si no pasa, ¿cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/04_candidates_who_referred_nobody.sql`](starter/queries/04_candidates_who_referred_nobody.sql):

```sql
SELECT id, name
FROM candidates
WHERE id NOT IN (SELECT referred_by FROM candidates);
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que use una subconsulta (sin `JOIN`) y dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask4CandidatesWhoReferredNobody` pasa, y con todas las pruebas, pasan las 5.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `WHERE x > (SELECT …)` | Compara cada fila con el valor que devuelve la subconsulta (subconsulta escalar) |
| `WHERE x IN (SELECT col …)` | Deja las filas cuyo `x` está en la columna que devuelve la subconsulta |
| `WHERE x NOT IN (SELECT col …)` | La pregunta contraria a `IN` |
| `… WHERE a.col = c.col` dentro de la subconsulta | La correlaciona: usa una columna de la fila de afuera y se calcula una vez por cada fila |
| `WHERE EXISTS (SELECT 1 …)` | Verdadero si la subconsulta devuelve al menos una fila |
| `WHERE NOT EXISTS (SELECT 1 …)` | Verdadero si la subconsulta no devuelve ninguna fila |
| `FROM (SELECT …) AS nombre` | Usa el resultado como una tabla más (lab 2.5) |

## 💼 En proyectos reales
- **PostgreSQL rechaza la consulta de la predicción de la tarea 1:** una subconsulta escalar que devuelve más de una fila es un error ([PostgreSQL](https://www.postgresql.org/docs/current/sql-expressions.html#SQL-SYNTAX-SCALAR-SUBQUERIES)); SQLite toma la primera fila sin avisar ([SQLite](https://www.sqlite.org/lang_expr.html#subq)). No se corrió en PostgreSQL: lo dice su documentación. En los dos, una subconsulta con `MAX`, `MIN` o `AVG` y sin `GROUP BY` devuelve siempre una fila.
- **`NOT IN` con un `NULL` en la lista da lo mismo en PostgreSQL** que en SQLite ([PostgreSQL](https://www.postgresql.org/docs/current/functions-subquery.html#FUNCTIONS-SUBQUERY-NOTIN); no se corrió allí). Por eso muchos equipos escriben `NOT EXISTS` por costumbre cuando la columna de la subconsulta admite `NULL`.
- **Califica siempre las columnas de una subconsulta correlacionada** con el alias de su tabla (`o.company_id = j.company_id`): como mostró la tarea 3, una columna sin alias se busca primero en la tabla de adentro, y la consulta no avisa si eso no era lo que querías.
- **Subconsulta o `JOIN`:** si la pregunta pide columnas de la otra tabla, es un `JOIN`; si solo pide saber si hay filas relacionadas, `IN` o `EXISTS` no repiten filas. Cuando las dos formas dan lo mismo, elige la que se lee mejor; cuál es más rápida lo dice el plan de ejecución (*query plan*), que verás en el lab 5.1.
- **«El segundo sueldo más alto»** es una pregunta clásica de entrevista: `SELECT MAX(salary_usd) FROM jobs WHERE salary_usd < (SELECT MAX(salary_usd) FROM jobs);` (aquí da 2000).

## 🆘 Pistas
<details><summary>Pista 1 · Tarea 1</summary>

Corre sola la subconsulta del compañero: ¿cuántas filas devuelve? ¿Con cuál de ellas compara SQLite el sueldo de cada oferta? ¿Qué función del lab 2.4 convierte esas filas en un solo valor, el más alto?
</details>

<details><summary>Pista 2 · Tarea 2</summary>

Mira las postulaciones de cada persona que sale: ¿a cuántas ofertas remotas postuló cada una? ¿Cuántas filas arma el `JOIN` para una persona que postuló a dos? La pregunta solo quiere saber si postuló: ¿qué forma de Conceptos pregunta si un valor está en una lista?
</details>

<details><summary>Pista 3 · Tarea 3</summary>

Corre sola la subconsulta: ¿da el promedio de una empresa o el de todas? Dentro de la subconsulta, ¿`company_id` es de la oferta de afuera o de la de adentro? ¿Cómo distingue el ejemplo de la subconsulta correlacionada en Conceptos una tabla de la otra?
</details>

<details><summary>Pista 4 · Tarea 4</summary>

Corre sola la subconsulta del compañero y mira todos los valores que devuelve. ¿Qué resultado da `2 NOT IN` con esa lista, si uno de los valores es desconocido? Repasa qué hace `NULL` en una comparación en el [lab 1.4](../../01-query-a-table/04-null-values/README.md#un-dato-que-falta-null). ¿Qué forma de Conceptos pregunta si existe una fila, sin armar una lista?
</details>

## 🎤 Autoevaluación
1. ¿Qué diferencia hay entre una subconsulta escalar y una correlacionada?
2. En `products(id, name, price)`, escribe la consulta de los productos que cuestan más que el promedio.
3. En `customers(id, name)` y `orders(id, customer_id, total)`, escribe la consulta de los clientes que nunca hicieron un pedido, sin `JOIN`.
4. ¿Por qué `WHERE id NOT IN (SELECT manager_id FROM employees)` puede devolver 0 filas aunque haya empleados que no son jefes de nadie?
5. ¿Cuándo usarías `IN` en lugar de un `JOIN`?

<details><summary>Respuestas</summary>

1. La escalar devuelve un solo valor y no depende de la fila de afuera, así que se calcula una vez; la correlacionada usa columnas de la fila de afuera y se calcula una vez por cada fila. Una correlacionada también puede ser escalar, como la del `SELECT` en Conceptos.
2. `SELECT id, name, price FROM products WHERE price > (SELECT AVG(price) FROM products);`
3. `SELECT c.id, c.name FROM customers AS c WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.id);`
4. Porque quien no tiene jefe tiene `manager_id` `NULL`, y con un `NULL` en la lista `NOT IN` nunca es verdadero. Se usa `NOT EXISTS` o se quitan los `NULL` en la subconsulta.
5. Cuando solo necesito saber si hay filas relacionadas y no quiero columnas de la otra tabla: `IN` no repite la fila cuando hay varias relacionadas.
</details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · SQLite toma la primera fila de la subconsulta
```text
01_jobs_above_andes_retail.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 4; obtenidas: 5
  Esperadas que no salieron:
    (ninguna)
  Obtenidas que no se esperaban:
    (4, 'Analista de BI', 1500)
```

5 filas, sin error. La subconsulta devuelve los sueldos de las 3 ofertas de Andes Retail (1200, 1500 y `NULL`), pero se usa como un solo valor, y SQLite toma la primera fila: 1200, la oferta 1. La consulta compara con la oferta 1, no con la mejor pagada, y la oferta 4, que paga 1500, entra. `MAX` convierte las tres filas en un solo valor:

```sql
SELECT id, title, salary_usd
FROM jobs
WHERE salary_usd > (
    SELECT MAX(salary_usd)
    FROM jobs
    WHERE company_id = 1
);
```

También pasa buscar la empresa por su nombre con otra subconsulta (`WHERE company_id = (SELECT id FROM companies WHERE name = 'Andes Retail')`), y también `ORDER BY salary_usd DESC LIMIT 1` en lugar de `MAX`, aunque `MAX` dice mejor lo que pides. `>=` no pasa: la oferta 4 empata con el máximo.

### Tarea 2 · Un `JOIN` repite a quien postuló a dos ofertas remotas
```text
02_remote_applicants.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 3; obtenidas: 4
  Esperadas que no salieron:
    (ninguna)
  Obtenidas que no se esperaban:
    (2, 'Luis Ramírez')
```

4 filas: Luis Ramírez (2) sale dos veces, porque postuló a las ofertas 2 y 6, las dos remotas, y el `JOIN` arma una fila por postulación. La pregunta solo pide saber si una persona postuló, y `IN` responde eso una vez por persona, aunque su `id` esté dos veces en la lista:

```sql
SELECT id, name
FROM candidates
WHERE id IN (
    SELECT a.candidate_id
    FROM applications AS a
    JOIN jobs AS j ON j.id = a.job_id
    WHERE j.mode = 'remoto'
);
```

También pasan dos `IN` uno dentro del otro (`WHERE id IN (SELECT candidate_id FROM applications WHERE job_id IN (SELECT id FROM jobs WHERE mode = 'remoto'))`), `EXISTS` con una subconsulta correlacionada, y el `JOIN` del compañero con `SELECT DISTINCT`. `WHERE id IN (SELECT id FROM jobs WHERE mode = 'remoto')` no pasa: compara el `id` de una persona con el `id` de una oferta.

### Tarea 3 · Una columna sin alias se busca primero en la subconsulta
```text
03_jobs_above_company_average.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 4; obtenidas: 5
  Esperadas que no salieron:
    (8, 'Analista de calidad (QA)', 1150)
  Obtenidas que no se esperaban:
    (2, 'Desarrollador backend', 1800)
    (10, 'Analista de riesgos', 1750)
```

5 filas. Dentro de la subconsulta, `company_id` sin tabla se busca primero en el `FROM` de la subconsulta, así que los dos lados de `company_id = company_id` son la misma oferta de adentro, y la condición se cumple en todas. La subconsulta no está correlacionada: calcula el promedio de todas las ofertas (13225 / 9 = 1469.4…) y compara cada oferta con ese número. La oferta 8 (1150) supera el promedio de Clínica Central (987.5) pero no el de todas, y las ofertas 2 y 10 superan el de todas pero no el de su empresa. Con un alias para cada tabla, la condición une la oferta de adentro con la de afuera:

```sql
SELECT j.id, j.title, j.salary_usd
FROM jobs AS j
WHERE j.salary_usd > (
    SELECT AVG(o.salary_usd)
    FROM jobs AS o
    WHERE o.company_id = j.company_id
);
```

`WHERE company_id = j.company_id` también pasa (el `company_id` sin alias es el de adentro), igual que unir con `jobs` una subconsulta en el `FROM` con el promedio de cada empresa, como en el lab 2.5. `>=` no pasa: la única oferta de Agro Norte es igual a su propio promedio. `SUM(o.salary_usd) / COUNT(*)` tampoco: la oferta 9, sin sueldo, baja el promedio de Andes Retail a 900 y entra la oferta 1.

### Tarea 4 · `NOT IN` con un `NULL` en la lista no deja pasar ninguna fila
```text
04_candidates_who_referred_nobody.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 0
  Esperadas que no salieron:
    (2, 'Luis Ramírez')
    (6, 'Luis Ramírez')
    (7, 'Carmen Rojas')
    (8, 'Diego Flores')
    (9, 'Valeria Paredes')
  Obtenidas que no se esperaban:
    (ninguna)
```

0 filas. Es lo que el bloque 1 dejó pendiente sobre `NOT IN`: la subconsulta devuelve los `referred_by` de las 9 personas, y 4 son `NULL`. `2 NOT IN (…, NULL)` quiere decir «2 no es ninguno de estos valores», y la base no puede asegurar que 2 no sea el valor desconocido: el resultado es `NULL`, no verdadero, y el `WHERE` deja fuera la fila. Pasa con cada persona. Con una lista sin `NULL`, como la del ejemplo de Conceptos, `NOT IN` funciona; basta un `NULL` para que no salga nada. `NOT EXISTS` pregunta otra cosa, si hay una persona recomendada por esta, y un `NULL` no la cambia:

```sql
SELECT c.id, c.name
FROM candidates AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM candidates AS r
    WHERE r.referred_by = c.id
);
```

También pasa `NOT IN` con los `NULL` quitados (`SELECT referred_by FROM candidates WHERE referred_by IS NOT NULL`). Fuera de lo que pide la tarea, el *anti-join* del [lab 2.3](../03-unmatched-rows/README.md), `LEFT JOIN candidates AS r ON r.referred_by = c.id WHERE r.id IS NULL`, también funciona y pasa la prueba. `NOT EXISTS` sin alias (`WHERE referred_by = id`) no pasa, por lo mismo que en la tarea 3: devuelve las 9 personas.
</details>

La solución completa está en [`solution/`](solution/).
