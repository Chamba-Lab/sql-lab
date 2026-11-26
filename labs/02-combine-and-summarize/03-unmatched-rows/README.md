# 🧩 2.3 · Filas sin pareja

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Unir dos tablas sin perder las filas que no tienen pareja en la otra, con `LEFT JOIN`.
- Leer el `NULL` que completa una fila sin pareja.
- Encontrar lo que falta (las filas sin pareja) con un *anti-join*.
- Decidir si una condición va en el `ON` o en el `WHERE` de un `LEFT JOIN`.
- Reconocer `RIGHT JOIN`, `FULL JOIN` y `CROSS JOIN`.

## 💡 Por qué importa
En el lab 2.2, el `JOIN` dejaba fuera a quien no tenía pareja: Nube Andina no salía con ninguna oferta, y las personas que nadie recomendó no salían en la lista de recomendaciones. Muchas preguntas reales piden justo esas filas: todas las empresas, tengan o no ofertas; los postulantes que todavía no postularon a nada; los clientes que nunca compraron. Si la consulta las pierde sin avisar, el reporte se ve completo y no lo está. «Lista los clientes sin pedidos» es además una de las preguntas de SQL más comunes en las entrevistas.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/02-combine-and-summarize/03-unmatched-rows/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la base del [lab 2.1](../01-table-relationships/README.md), la misma de las tareas. No hace falta correrlos; si quieres probarlos, crea la base y abre la consola como en el experimento 1 de ese lab.

### Quedarse también con las filas sin pareja (*LEFT JOIN*)
En la tarea 4 del lab 2.2 listaste a cada persona con quien la recomendó, y salieron 5 de las 9: las personas con `referred_by` en `NULL` no encontraron pareja y el `JOIN` las dejó fuera. ¿Y si el reporte tiene que mostrar a las 9, con quien la recomendó cuando hay alguien?

La idea: que la consulta se quede con **todas** las filas de la primera tabla. A cada una le busca pareja en la segunda, como siempre; si no encuentra ninguna, la fila sale igual, y las columnas de la segunda tabla quedan vacías, en `NULL`. En SQL se escribe **`LEFT JOIN`** en lugar de `JOIN`, con el mismo `ON`:

```sql
SELECT c.name AS candidate, r.name AS recommender
FROM candidates AS c
LEFT JOIN candidates AS r ON c.referred_by = r.id
ORDER BY c.id;
```

| candidate | recommender |
|---|---|
| Ana Quispe | `NULL` |
| Luis Ramírez | `NULL` |
| María Torres | Ana Quispe |
| Jorge Huamán | Ana Quispe |
| Sofía Castro | `NULL` |
| Luis Ramírez | Jorge Huamán |
| Carmen Rojas | María Torres |
| Diego Flores | `NULL` |
| Valeria Paredes | Sofía Castro |

Las 9 personas salen. Las 5 que tienen pareja salen como en el lab 2.2; las otras 4 salen con `recommender` en `NULL`, porque no hay una fila `r` de donde sacar el nombre.

*Left* es izquierda: la tabla de la izquierda es la que se escribe antes del `LEFT JOIN` (aquí, `c`), y es la que conserva todas sus filas. La de la derecha, la que se escribe después, aporta lo que encuentre. Se llama también **`LEFT OUTER JOIN`** (unión externa izquierda): `OUTER` es opcional, como `INNER` en el `JOIN` del lab 2.2. Un `JOIN` que conserva filas sin pareja es un *outer join*; el `JOIN` de siempre, que solo deja las parejas, es el *inner join*.

En los mensajes de las pruebas, ese `NULL` se ve como `None`, igual que en el [lab 1.4](../../01-query-a-table/04-null-values/README.md).

### Encontrar lo que no tiene pareja (*anti-join*)
¿Qué ofertas no recibieron ninguna postulación? La respuesta son filas de `jobs` que no tienen pareja en `applications`, y un `JOIN` justo las quita.

La idea: unir con `LEFT JOIN`, para que las ofertas sin postulaciones queden en el resultado, y después quedarse solo con las filas donde la parte de `applications` salió vacía. En una fila sin pareja todas las columnas de `applications` son `NULL`, así que se pregunta con `IS NULL` por una columna de `applications` (aquí, `a.id`), como en el [lab 1.4](../../01-query-a-table/04-null-values/README.md):

```sql
SELECT j.id, j.title
FROM jobs AS j
LEFT JOIN applications AS a ON a.job_id = j.id
WHERE a.id IS NULL;
```

| id | title |
|---|---|
| 10 | Analista de riesgos |

La oferta 10, de Banco Sur, es la única a la que nadie postuló. A esta forma de buscar lo que falta se le llama ***anti-join***: las filas de una tabla que **no** tienen pareja en la otra. No es una palabra de SQL, es el nombre del patrón: `LEFT JOIN` más `WHERE … IS NULL`.

### Más de una condición en el `ON`
El `ON` es una condición como las del `WHERE`, así que puede llevar varias unidas con `AND`. Las postulaciones a ofertas remotas, emparejando cada postulación solo con su oferta si esa oferta es remota:

```sql
SELECT a.id, j.title
FROM applications AS a
JOIN jobs AS j ON a.job_id = j.id AND j.mode = 'remoto'
ORDER BY a.id;
```

| id | title |
|---|---|
| 4 | Desarrollador backend |
| 5 | Desarrolladora full stack |
| 7 | Analista de calidad (QA) |
| 16 | Desarrolladora full stack |

Con un `JOIN` de los de siempre, poner `j.mode = 'remoto'` en el `ON` o en un `WHERE` da las mismas 4 filas.

### Qué hace el `ON` y qué hace el `WHERE`
Con un `LEFT JOIN`, las dos partes trabajan en momentos distintos:

1. **El `ON` arma las parejas.** Para cada fila de la izquierda, busca las filas de la derecha que cumplen **toda** la condición del `ON`. Si ninguna la cumple, la fila de la izquierda sale igual, completada con `NULL`.
2. **El `WHERE` filtra después**, sobre ese resultado ya unido y completado, y deja solo las filas que cumplen su condición. Igual que en el lab 2.2, puede usar columnas de las dos tablas.

Ten presentes los dos pasos en las tareas: dónde escribes cada condición cambia qué filas quedan.

### Los otros `JOIN`
Vas a encontrar tres más. Los tres funcionan en las versiones de SQLite de este curso, pero no los necesitas para las tareas:

- **`RIGHT JOIN`** conserva todas las filas de la tabla de la **derecha**. `FROM applications AS a RIGHT JOIN jobs AS j ON a.job_id = j.id` da las mismas 17 filas que `FROM jobs AS j LEFT JOIN applications AS a ON a.job_id = j.id`: es un `LEFT JOIN` con las tablas escritas al revés.
- **`FULL JOIN`** (o `FULL OUTER JOIN`) conserva las filas sin pareja de los **dos** lados.
- **`CROSS JOIN`** junta cada fila de una tabla con cada fila de la otra, sin `ON`: es el producto cartesiano de la tarea 1 del lab 2.2, escrito a propósito. `FROM jobs CROSS JOIN companies` da 60 filas.

## 📚 Documentación
- [SQLite: la cláusula `FROM` y los `JOIN`](https://www.sqlite.org/lang_select.html#fromclause)
- [PostgreSQL: la cláusula `FROM` de `SELECT`](https://www.postgresql.org/docs/current/sql-select.html#SQL-FROM), con qué filas conserva cada tipo de `JOIN`

## 🧭 Escenario
La bolsa de trabajo quiere reportes que no se salten a nadie: todas las empresas con sus ofertas, todos los postulantes con sus postulaciones, las empresas que todavía no publican nada y las ofertas remotas de cada empresa. Te pide cuatro consultas.

### La base
Son las cuatro tablas del [lab 2.1](../01-table-relationships/README.md#-escenario), con los mismos datos que en el lab 2.2. Este es su diagrama en texto:

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
├── queries/                        tus cuatro consultas, una por tarea
│   ├── 01_companies_with_jobs.sql
│   ├── 02_candidates_with_jobs.sql
│   ├── 03_companies_without_jobs.sql
│   └── 04_remote_jobs_by_company.sql
├── seed.sql                        crea las cuatro tablas y sus filas
├── tests/
│   ├── conftest.py                 prepara la base y compara resultados
│   └── test_queries.py             las pruebas: una clase por tarea
└── pyproject.toml                  le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../../01-query-a-table/02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). Ninguna tarea pide un orden: las filas pueden salir en cualquiera. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 4, una por tarea.

### Tarea 1 · Todas las empresas con sus ofertas
**Objetivo:** cada empresa con los títulos de sus ofertas, una fila por oferta, y también las empresas sin ofertas, una vez cada una, con `title` en `NULL`. Columnas `company` (el nombre de la empresa) y `title`, 11 filas. **Lo valida:** [`TestTask1CompaniesWithJobs`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero usó `LEFT JOIN`, pero empezó por `jobs`. ¿Cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/01_companies_with_jobs.sql`](starter/queries/01_companies_with_jobs.sql):

```sql
SELECT c.name AS company, j.title
FROM jobs AS j
LEFT JOIN companies AS c ON j.company_id = c.id;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva las 11 filas que pide la tarea, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1CompaniesWithJobs` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 3 fallan.

### Tarea 2 · Todos los postulantes con sus postulaciones
**Objetivo:** cada postulante con el título de cada oferta a la que postuló, una fila por postulación, y también quienes no postularon a nada, una vez cada uno, con `title` en `NULL`. Columnas `id` y `name` (de la persona) y `title` (de la oferta), 17 filas. **Lo valida:** [`TestTask2CandidatesWithJobs`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero pasó de `candidates` a `applications` con un `LEFT JOIN` y de `applications` a `jobs` con un `JOIN`. ¿Cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/02_candidates_with_jobs.sql`](starter/queries/02_candidates_with_jobs.sql):

```sql
SELECT c.id, c.name, j.title
FROM candidates AS c
LEFT JOIN applications AS a ON a.candidate_id = c.id
JOIN jobs AS j ON a.job_id = j.id;
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva las 17 filas que pide la tarea, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2CandidatesWithJobs` pasa. Con todas las pruebas, 3 pasan y 2 fallan.

### Tarea 3 · Las empresas sin ofertas
**Objetivo:** las empresas que no publicaron ninguna oferta. Columnas `id` y `name`. **Lo valida:** [`TestTask3CompaniesWithoutJobs`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió este *anti-join*, preguntando por el sueldo. ¿Cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/03_companies_without_jobs.sql`](starter/queries/03_companies_without_jobs.sql):

```sql
SELECT c.id, c.name
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
WHERE j.salary_usd IS NULL;
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva solo las empresas sin ofertas, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3CompaniesWithoutJobs` pasa. Con todas las pruebas, 4 pasan y 1 falla.

### Tarea 4 · Las ofertas remotas de cada empresa
**Objetivo:** cada empresa con los títulos de sus ofertas **remotas**, una fila por oferta remota, y también las empresas sin ofertas remotas, una vez cada una, con `title` en `NULL`. Columnas `company` y `title`, 7 filas: las 6 empresas salen. **Lo valida:** [`TestTask4RemoteJobsByCompany`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero tomó la consulta de la tarea 1 y le agregó un `WHERE`. ¿Cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/04_remote_jobs_by_company.sql`](starter/queries/04_remote_jobs_by_company.sql):

```sql
SELECT c.name AS company, j.title
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
WHERE j.mode = 'remoto';
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva las 7 filas que pide la tarea, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask4RemoteJobsByCompany` pasa: las 5 pruebas pasan.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `FROM a LEFT JOIN b ON <condición>` | Junta cada fila de `a` con las de `b` que cumplen la condición, y conserva las filas de `a` sin pareja |
| `LEFT OUTER JOIN` | Lo mismo que `LEFT JOIN` |
| `NULL` en las columnas de `b` | Así sale una fila de `a` que no encontró pareja |
| `LEFT JOIN b ON … WHERE b.id IS NULL` | *Anti-join*: las filas de `a` que no tienen pareja en `b` |
| `ON <unión> AND <condición>` | La condición entra en el armado de las parejas, antes de completar con `NULL` |
| `WHERE <condición>` | Filtra después, sobre el resultado ya unido y completado |
| `RIGHT JOIN` / `FULL JOIN` | Conservan las filas sin pareja de la derecha / de los dos lados |
| `CROSS JOIN` | Todas las parejas posibles, sin `ON` |

## 💼 En proyectos reales
- **Casi todo el mundo escribe `LEFT JOIN`, no `RIGHT JOIN`.** Cualquier `RIGHT JOIN` se puede escribir como `LEFT JOIN` cambiando el orden de las tablas, y una consulta se lee mejor cuando la tabla que conserva todo va primero. La documentación de MySQL lo recomienda para que el código funcione en otros motores ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/join.html)).
- **MySQL no tiene `FULL JOIN`.** Su sintaxis de `JOIN` solo trae `LEFT` y `RIGHT` como uniones externas ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/join.html)); PostgreSQL y SQLite sí lo tienen ([PostgreSQL](https://www.postgresql.org/docs/current/sql-select.html#SQL-FROM)).
- **El `LEFT JOIN` con un filtro en el `WHERE` es un error clásico de los reportes:** la consulta corre, devuelve filas creíbles y pierde justo las que el reporte quería mostrar. Cuando un reporte con `LEFT JOIN` parece corto, mira dónde quedó cada condición sobre la tabla de la derecha.
- **«Los clientes que nunca hicieron un pedido» es una pregunta de entrevista de siempre**, y es la tarea 3 con otros nombres. Se puede responder también con `NOT EXISTS` y con `NOT IN`, formas que llegan en el lab 2.6; el *anti-join* con `LEFT JOIN` es la que se espera que sepas escribir.

## 🆘 Pistas
<details><summary>Pista 1 · Falta la empresa sin ofertas</summary>

¿Qué tabla conserva todas sus filas en un `LEFT JOIN`, la que se escribe antes o la que se escribe después? ¿Cuál de las dos tiene que conservar todas sus filas en esta tarea?
</details>

<details><summary>Pista 2 · Falta Diego Flores</summary>

Su fila sale del primer `LEFT JOIN` con todo `applications` en `NULL`. ¿Qué hace después un `JOIN` de los de siempre con una fila que no encuentra pareja en `jobs`?
</details>

<details><summary>Pista 3 · Sale una empresa que sí tiene ofertas</summary>

Mira en la tabla de `jobs` las ofertas de esa empresa. ¿Alguna tiene `NULL` en la columna por la que preguntas? ¿Qué columna de `jobs` nunca está en `NULL` en una oferta que existe?
</details>

<details><summary>Pista 4 · No sale ninguna fila en el <i>anti-join</i></summary>

¿Escribiste `= NULL` en vez de `IS NULL`? Lo viste en el [lab 1.4](../../01-query-a-table/04-null-values/README.md). ¿O usaste `JOIN` en vez de `LEFT JOIN`?
</details>

<details><summary>Pista 5 · Faltan las empresas sin ofertas remotas</summary>

Repasa en Conceptos qué hace el `WHERE` y en qué momento. En una fila completada con `NULL`, ¿cuánto vale `j.mode = 'remoto'`? ¿Dónde puede ir esa condición para que solo decida qué ofertas se emparejan?
</details>

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · `LEFT JOIN` conserva la tabla de la izquierda
```text
01_companies_with_jobs.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 11; obtenidas: 10
  Esperadas que no salieron:
    ('Nube Andina', None)
  Obtenidas que no se esperaban:
    (ninguna)
```

10 filas, una por oferta: la tabla de la izquierda es `jobs`, así que el `LEFT JOIN` conserva todas las ofertas, y todas tienen empresa. Nube Andina está a la derecha y no tiene ofertas, así que nadie la trae. Con estos datos, ese `LEFT JOIN` da lo mismo que un `JOIN`. La tabla que tiene que conservar todo es `companies`, y va primero:

```sql
SELECT c.name AS company, j.title
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id;
```

`FROM jobs AS j RIGHT JOIN companies AS c ON …` también pasa: es la misma consulta con las tablas al revés. Escribe la forma con `LEFT JOIN`.

### Tarea 2 · Un `JOIN` después de un `LEFT JOIN` quita lo que este conservó
```text
02_candidates_with_jobs.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 17; obtenidas: 16
  Esperadas que no salieron:
    (8, 'Diego Flores', None)
  Obtenidas que no se esperaban:
    (ninguna)
```

16 filas, una por postulación: Diego Flores desaparece. El primer `LEFT JOIN` lo conserva, con `a.job_id` en `NULL`; después, el `JOIN` con `jobs` busca una oferta con `id` igual a `NULL`, no la encuentra, y un `JOIN` de los de siempre quita la fila. Cada `JOIN` trabaja sobre lo que dejaron los anteriores, así que una fila conservada tiene que seguir conservándose en cada paso:

```sql
SELECT c.id, c.name, j.title
FROM candidates AS c
LEFT JOIN applications AS a ON a.candidate_id = c.id
LEFT JOIN jobs AS j ON a.job_id = j.id;
```

La tarea pide el `id` porque hay dos Luis Ramírez, como viste en el lab 2.2: sin él, no sabrías cuál de los dos postuló a cada oferta.

### Tarea 3 · En un *anti-join*, pregunta por una columna que nunca es `NULL`
```text
03_companies_without_jobs.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 1; obtenidas: 2
  Esperadas que no salieron:
    (ninguna)
  Obtenidas que no se esperaban:
    (1, 'Andes Retail')
```

2 filas: Nube Andina y Andes Retail. Andes Retail tiene tres ofertas, pero la 9 no dice el sueldo: su `salary_usd` es `NULL` en una fila real, con pareja, y el `WHERE` no puede distinguirla de una fila sin pareja. Un *anti-join* tiene que preguntar por una columna que solo es `NULL` cuando no hubo pareja: la clave primaria de la tabla de la derecha, que nunca es `NULL`, o la columna del `ON`.

```sql
SELECT c.id, c.name
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
WHERE j.id IS NULL;
```

`WHERE j.company_id IS NULL` y `WHERE j.title IS NULL` también pasan con estos datos; la primera es igual de segura, porque es la columna del `ON`, y la segunda solo mientras ninguna oferta llegue sin título. Si escribiste `WHERE j.id = NULL`, no salió ninguna fila: una comparación con `NULL` nunca es verdadera ([lab 1.4](../../01-query-a-table/04-null-values/README.md)).

### Tarea 4 · Un filtro de la tabla derecha va en el `ON`
```text
04_remote_jobs_by_company.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 7; obtenidas: 3
  Esperadas que no salieron:
    ('Andes Retail', None)
    ('Agro Norte', None)
    ('Banco Sur', None)
    ('Nube Andina', None)
  Obtenidas que no se esperaban:
    (ninguna)
```

3 filas, solo las ofertas remotas: las empresas sin ofertas remotas desaparecen. El `LEFT JOIN` arma las 11 filas de la tarea 1 y después el `WHERE` se queda con las que tienen `j.mode = 'remoto'`. Las ofertas no remotas no lo cumplen, y en la fila de Nube Andina `j.mode` es `NULL`, y `NULL = 'remoto'` no es verdadero. El `WHERE` deshizo lo que el `LEFT JOIN` había conservado: el resultado es el de un `JOIN`. La condición sobre la tabla de la derecha va en el `ON`, donde solo decide qué ofertas se emparejan; la empresa que no empareja ninguna sale igual, con `NULL`:

```sql
SELECT c.name AS company, j.title
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id AND j.mode = 'remoto';
```

`WHERE j.mode = 'remoto' OR j.id IS NULL` tampoco sirve: recupera a Nube Andina, que no tiene ofertas, pero no a Andes Retail, Agro Norte ni Banco Sur, que tienen ofertas, ninguna remota. La regla práctica: en un `LEFT JOIN`, una condición sobre la tabla de la izquierda va en el `WHERE`, y una sobre la tabla de la derecha va en el `ON`, salvo el `IS NULL` de un *anti-join*.
</details>

## 🎤 Autoevaluación
1. `customers` tiene 50 filas y `orders` tiene 200, todas de clientes que existen; 10 clientes nunca compraron. ¿Cuántas filas devuelve `SELECT * FROM customers AS c LEFT JOIN orders AS o ON o.customer_id = c.id`? ¿Y con `JOIN`?
2. Escribe la consulta que lista los clientes que nunca hicieron un pedido.
3. ¿Qué diferencia hay entre `LEFT JOIN` y `LEFT OUTER JOIN`? ¿Y entre `FROM a LEFT JOIN b` y `FROM b LEFT JOIN a`?
4. Quieres todos los clientes con sus pedidos de 2026, incluidos los que no compraron en 2026. ¿Dónde va la condición sobre la fecha del pedido, y qué pasa si la pones en el otro lugar?
5. ¿Por qué `WHERE o.discount IS NULL` es un mal *anti-join*, si `discount` puede estar vacío en un pedido real?

<details><summary>Respuestas</summary>

1. 210 con `LEFT JOIN`: una fila por pedido (200) más una por cada cliente sin pedidos (10), con las columnas de `orders` en `NULL`. Con `JOIN`, 200: los 10 clientes sin pedidos no salen.
2. `SELECT c.id, c.name FROM customers AS c LEFT JOIN orders AS o ON o.customer_id = c.id WHERE o.id IS NULL;`
3. Ninguna: `OUTER` es opcional. El orden de las tablas sí importa: `LEFT JOIN` conserva todas las filas de la tabla escrita antes, así que `FROM a LEFT JOIN b` conserva las de `a` y `FROM b LEFT JOIN a`, las de `b`.
4. En el `ON`: `LEFT JOIN orders AS o ON o.customer_id = c.id AND o.ordered_on >= '2026-01-01'`. En el `WHERE`, los clientes sin pedidos de 2026 desaparecen, porque su fila completada con `NULL` no cumple la condición.
5. Porque devuelve también a los clientes que sí tienen pedidos, si alguno de esos pedidos no tiene descuento. Un *anti-join* pregunta por una columna que solo es `NULL` cuando no hubo pareja, como `o.id`.
</details>

La solución completa está en [`solution/`](solution/).

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?
