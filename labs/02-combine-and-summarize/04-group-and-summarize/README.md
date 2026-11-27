# 🧩 2.4 · Agrupar y resumir

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Resumir muchas filas en una con las funciones de agregado `COUNT`, `SUM`, `AVG`, `MIN` y `MAX`.
- Distinguir `COUNT(*)`, `COUNT(columna)` y `COUNT(DISTINCT columna)`, y saber qué hace cada función con un `NULL`.
- Calcular un resumen por cada grupo con `GROUP BY`, también sobre el resultado de un `JOIN`.
- Elegir las columnas del `GROUP BY`.
- Comprobar un resultado agrupado contra los datos de las tablas.

## 💡 Por qué importa
Hasta ahora, cada consulta devolvía filas de las tablas, una por oferta o por postulación. Las preguntas de un reporte suelen ser otras: cuántas postulaciones llegaron, cuánto paga en promedio cada empresa, cuántas postulaciones hizo cada persona. En una hoja de cálculo las responderías con una tabla dinámica; en SQL, con `GROUP BY`. Es de lo más usado en cualquier trabajo con datos, y casi toda entrevista de SQL tiene una pregunta de «cuántos por cada…».

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/02-combine-and-summarize/04-group-and-summarize/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la base del [lab 2.1](../01-table-relationships/README.md), la misma de las tareas. No hace falta correrlos; si quieres probarlos, crea la base y abre la consola como en el experimento 1 de ese lab.

### Resumir una tabla en una fila (funciones de agregado)
¿Cuántas personas hay en `candidates`, y cuánta experiencia tienen entre todas, la que menos, la que más y en promedio? Con lo que sabes, tendrías que traer las 9 filas y sacar las cuentas a mano.

La idea: pedirle a la consulta que junte todas las filas y devuelva solo el resultado de cada cuenta. Cada cuenta es una **función de agregado** (*aggregate function*): recibe los valores de muchas filas y devuelve uno solo.

```sql
SELECT COUNT(*) AS candidates, SUM(years_experience) AS total_years,
       MIN(years_experience) AS least, MAX(years_experience) AS most,
       ROUND(AVG(years_experience), 2) AS average
FROM candidates;
```

| candidates | total_years | least | most | average |
|---|---|---|---|---|
| 9 | 15.5 | 0.0 | 4.0 | 1.72 |

Las 9 filas se volvieron una. Las cinco funciones:

| Función | Devuelve |
|---|---|
| `COUNT(*)` | cuántas filas hay |
| `SUM(columna)` | la suma de los valores |
| `AVG(columna)` | el promedio (*average*) |
| `MIN(columna)` / `MAX(columna)` | el valor más chico / el más grande |

`MIN` y `MAX` también sirven con textos y con fechas: comparan como el `ORDER BY`, así que en `jobs`, `MIN(posted_on)` es `2026-11-03`, la fecha más antigua, y `MIN(title)` es `Administrador de bases de datos`, el primero en orden alfabético.

### Contar filas o contar valores
`COUNT` tiene dos formas. `COUNT(*)` cuenta filas, tengan lo que tengan. `COUNT(columna)` cuenta los valores de esa columna que no son `NULL`:

```sql
SELECT COUNT(*) AS candidates, COUNT(referred_by) AS referred
FROM candidates;
```

| candidates | referred |
|---|---|
| 9 | 5 |

Hay 9 personas, y 5 tienen a alguien en `referred_by`: las 4 con `NULL` no entran en la cuenta. Lo mismo hacen `SUM`, `AVG`, `MIN` y `MAX`: trabajan solo con los valores que no son `NULL`, como si esas filas no estuvieran.

### Contar cada valor una vez (*DISTINCT*)
¿En cuántas ciudades distintas viven los postulantes? Lima aparece en 4 filas, y para esta pregunta cuenta una vez. `DISTINCT` dentro del `COUNT` cuenta cada valor distinto una sola vez:

```sql
SELECT COUNT(DISTINCT city) AS cities
FROM candidates;
```

| cities |
|---|
| 6 |

Lima, Bogotá, Arequipa, Santiago, Trujillo y Cusco. Como `COUNT(columna)`, `COUNT(DISTINCT columna)` deja fuera el `NULL`.

### Un resumen por grupo (*GROUP BY*)
¿Cuántas ofertas tiene cada empresa en cada modalidad? Una sola fila para toda la tabla ya no alcanza: hace falta una fila por cada combinación de empresa y modalidad.

La idea: repartir las filas en grupos, uno por cada valor distinto de las columnas que elijas, y calcular las funciones de agregado dentro de cada grupo. Eso hace **`GROUP BY`**, que se escribe después del `FROM` (y del `WHERE`, si hay uno) y antes del `ORDER BY`:

```sql
SELECT company_id, mode, COUNT(*) AS jobs
FROM jobs
GROUP BY company_id, mode;
```

| company_id | mode | jobs |
|---|---|---|
| 1 | híbrido | 1 |
| 1 | presencial | 2 |
| 2 | remoto | 2 |
| 3 | presencial | 1 |
| 3 | remoto | 1 |
| 4 | presencial | 1 |
| 5 | híbrido | 2 |

Cada fila del resultado es un grupo: la empresa 1 tiene una oferta híbrida y dos presenciales. Con una sola columna en el `GROUP BY`, sale un grupo por cada valor de esa columna; con dos, uno por cada pareja de valores que aparece en la tabla. Las 7 cuentas suman 10, las ofertas de la tabla.

Cada fila de un grupo tiene su propio valor en cada columna, pero el grupo sale en una sola fila del resultado. Por eso, escribe en el `GROUP BY` cada columna del `SELECT` que no esté dentro de una función de agregado.

### Agrupar el resultado de un `JOIN`
El `GROUP BY` agrupa lo que deja el `FROM`, y el `FROM` puede ser un `JOIN`. Para contar las postulaciones por modalidad de la oferta, primero se une cada postulación con su oferta y después se agrupa por una columna de `jobs`:

```sql
SELECT j.mode, COUNT(*) AS applications
FROM applications AS a
JOIN jobs AS j ON a.job_id = j.id
GROUP BY j.mode;
```

| mode | applications |
|---|---|
| híbrido | 5 |
| presencial | 7 |
| remoto | 4 |

El `JOIN` arma las 16 filas de siempre, una por postulación con los datos de su oferta, y el `GROUP BY` las reparte en tres grupos.

## 📚 Documentación
- [SQLite: funciones de agregado](https://www.sqlite.org/lang_aggfunc.html#aggfunclist), con qué hace cada una con `NULL`
- [SQLite: columnas sueltas en una consulta con agregados](https://www.sqlite.org/lang_select.html#bareagg), en inglés (*bare columns*)
- [PostgreSQL: la cláusula `GROUP BY`](https://www.postgresql.org/docs/current/sql-select.html#SQL-GROUPBY)

## 🧭 Escenario
La bolsa de trabajo quiere un tablero de resumen: el total de postulaciones, el sueldo promedio de cada empresa, cuántas postulaciones hizo cada persona y cuántas recibió cada empresa. Te pide cuatro consultas.

### La base
Son las cuatro tablas del [lab 2.1](../01-table-relationships/README.md#-escenario), con los mismos datos que en los labs 2.2 y 2.3. Este es su diagrama en texto:

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
├── queries/                           tus cuatro consultas, una por tarea
│   ├── 01_application_summary.sql
│   ├── 02_salary_by_company.sql
│   ├── 03_applications_by_candidate.sql
│   └── 04_applications_by_company.sql
├── seed.sql                           crea las cuatro tablas y sus filas
├── tests/
│   ├── conftest.py                    prepara la base y compara resultados
│   └── test_queries.py                las pruebas: una clase por tarea
└── pyproject.toml                     le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../../01-query-a-table/02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). Ninguna tarea pide un orden: las filas pueden salir en cualquiera. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 4, una por tarea.

### Tarea 1 · El resumen de las postulaciones
**Objetivo:** una sola fila con cinco datos de `applications`: cuántas postulaciones hay (`applications`), cuántas personas postularon (`candidates`), a cuántas ofertas llegó al menos una postulación (`jobs`), y la fecha de la primera y de la última postulación (`first_applied` y `last_applied`). **Lo valida:** [`TestTask1ApplicationSummary`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Qué números crees que salen en `candidates` y en `jobs`? Escribe tu predicción y después pon la consulta en [`queries/01_application_summary.sql`](starter/queries/01_application_summary.sql):

```sql
SELECT COUNT(*) AS applications, COUNT(candidate_id) AS candidates, COUNT(job_id) AS jobs,
       MIN(applied_on) AS first_applied, MAX(applied_on) AS last_applied
FROM applications;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé las cifras que pide el objetivo, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1ApplicationSummary` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 3 fallan.

### Tarea 2 · El sueldo promedio de cada empresa
**Objetivo:** cada empresa que tiene ofertas, con cuántas ofertas tiene (`jobs`) y el promedio de sus sueldos (`avg_salary`), sin contar en el promedio las ofertas que no dicen el sueldo. Columnas `company` (el nombre de la empresa), `jobs` y `avg_salary`, 5 filas. **Lo valida:** [`TestTask2SalaryByCompany`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero no se acordaba de `AVG` y calculó el promedio como la suma de los sueldos entre cuántos sueldos hay. ¿Crees que pasa la prueba? Si no pasa, ¿en cuántas empresas sale otro promedio? Escribe tu predicción y después pon la consulta en [`queries/02_salary_by_company.sql`](starter/queries/02_salary_by_company.sql):

```sql
SELECT c.name AS company, COUNT(*) AS jobs, SUM(j.salary_usd) / COUNT(j.salary_usd) AS avg_salary
FROM companies AS c
JOIN jobs AS j ON j.company_id = c.id
GROUP BY c.id, c.name;
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2SalaryByCompany` pasa. Con todas las pruebas, 3 pasan y 2 fallan.

### Tarea 3 · Cuántas postulaciones hizo cada persona
**Objetivo:** cada persona que postuló al menos una vez, con cuántas postulaciones hizo. Columnas `id` y `name` (de la persona) y `applications`, una fila por persona. **Lo valida:** [`TestTask3ApplicationsByCandidate`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/03_applications_by_candidate.sql`](starter/queries/03_applications_by_candidate.sql):

```sql
SELECT c.id, c.name, COUNT(*) AS applications
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
GROUP BY c.name;
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3ApplicationsByCandidate` pasa. Con todas las pruebas, 4 pasan y 1 falla.

### Tarea 4 · Cuántas postulaciones recibió cada empresa
**Objetivo:** las 6 empresas, cada una con cuántas postulaciones recibieron sus ofertas, entre todas. Una empresa que no recibió ninguna sale igual, con `0`. Columnas `company` y `applications`, 6 filas. **Lo valida:** [`TestTask4ApplicationsByCompany`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero unió las tres tablas con `LEFT JOIN`, para que ninguna empresa se perdiera, y contó con `COUNT(*)`. ¿En cuántas empresas crees que la cuenta no coincide con las postulaciones que de verdad recibió? Escribe tu predicción y después pon la consulta en [`queries/04_applications_by_company.sql`](starter/queries/04_applications_by_company.sql):

```sql
SELECT c.name AS company, COUNT(*) AS applications
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN applications AS a ON a.job_id = j.id
GROUP BY c.id, c.name;
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask4ApplicationsByCompany` pasa, y con todas las pruebas, pasan las 5.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `COUNT(*)` | Cuenta filas, aunque tengan `NULL` |
| `COUNT(columna)` | Cuenta los valores de la columna que no son `NULL` |
| `COUNT(DISTINCT columna)` | Cuenta cada valor distinto una vez, sin el `NULL` |
| `SUM`, `AVG`, `MIN`, `MAX` | Suma, promedio, mínimo y máximo de los valores que no son `NULL` |
| `GROUP BY a, b` | Un grupo por cada combinación de valores de `a` y `b`; las funciones de agregado se calculan dentro de cada grupo |
| `SELECT … FROM … WHERE … GROUP BY … ORDER BY …` | El orden en que se escriben las partes |

## 💼 En proyectos reales
- **En SQLite y en PostgreSQL, un entero entre otro entero da un entero:** `7 / 2` es `3` en los dos, y los decimales se cortan, no se redondean ([PostgreSQL](https://www.postgresql.org/docs/current/functions-math.html)). En MySQL, `/` da decimales (`3.5000`) y la división entera se escribe `DIV` ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/arithmetic-functions.html)). Una consulta que calcula un porcentaje o un promedio a mano puede dar otro número al cambiar de motor; `AVG` da decimales en los tres.
- **PostgreSQL no acepta una columna suelta (*bare column*) en una consulta con `GROUP BY`:** si el `SELECT` tiene una columna que no está en el `GROUP BY` ni dentro de una función de agregado, da error, salvo que el `GROUP BY` tenga la clave primaria de su tabla ([PostgreSQL](https://www.postgresql.org/docs/current/sql-select.html#SQL-GROUPBY)). MySQL hace lo mismo con su configuración de fábrica (`ONLY_FULL_GROUP_BY`, [MySQL](https://dev.mysql.com/doc/refman/8.4/en/group-by-handling.html)). SQLite la deja pasar y elige el valor de una de las filas del grupo ([SQLite](https://www.sqlite.org/lang_select.html#bareagg)): una consulta que corre en SQLite puede fallar en el servidor.
- **Agrupa por la clave, no por el nombre.** En un reporte real hay clientes, productos y empleados con el mismo nombre. `GROUP BY c.id, c.name` agrupa por la persona y muestra su nombre; funciona igual en los tres motores.
- **«¿Cuántos pedidos tiene cada cliente, incluidos los que no tienen ninguno?»** es una pregunta de entrevista de siempre, y es la tarea 4 con otros nombres; su trampa es la de la tarea 4.

## 🆘 Pistas
<details><summary>Pista 1 · Las personas o las ofertas salen repetidas en la cuenta</summary>

Ana Quispe postuló tres veces. ¿Cuántas veces la cuenta `COUNT(candidate_id)`? Repasa en Conceptos cómo se cuenta cada valor una sola vez.
</details>

<details><summary>Pista 2 · Un promedio sale sin decimales</summary>

Calcula a mano el promedio de Clínica Central: (825 + 1150) / 2. ¿Qué número sale? ¿Qué número da la consulta? 1975 y 2 son enteros: ¿qué crees que hace SQLite con el resto de la división? ¿Qué función de Conceptos calcula el promedio sin que tengas que dividir?
</details>

<details><summary>Pista 3 · Andes Retail no tiene el promedio esperado</summary>

Andes Retail tiene tres ofertas, y una no dice el sueldo. Si dividiste entre `COUNT(*)`, ¿entre cuántas ofertas dividiste? ¿Cuántos sueldos hay de verdad?
</details>

<details><summary>Pista 4 · Falta una persona</summary>

Mira los nombres de `candidates`. ¿Hay dos personas con el mismo? ¿Qué columna identifica a cada persona sin confusión?
</details>

<details><summary>Pista 5 · Una empresa sin postulaciones sale con 1</summary>

¿Qué hace el `LEFT JOIN` con una empresa sin ofertas, o con una oferta sin postulaciones? ¿Qué cuenta `COUNT(*)` en esa fila completada con `NULL`? ¿Qué columna está en `NULL` justo cuando no hay postulación?
</details>

<details><summary>Pista 6 · Falta la empresa sin ofertas</summary>

¿Usaste `JOIN` en alguno de los dos pasos? Como en la tarea 2 del lab 2.3, un `JOIN` después de un `LEFT JOIN` quita la fila que este conservó.
</details>

## 🎤 Autoevaluación
1. `orders` tiene 200 filas; 30 tienen `discount` en `NULL`. ¿Cuánto da `COUNT(*)`? ¿Y `COUNT(discount)`?
2. ¿Qué diferencia hay entre `COUNT(customer_id)` y `COUNT(DISTINCT customer_id)` en la tabla `orders`?
3. ¿Cuánto da `SELECT 9 / 4;` en SQLite? ¿Y `SELECT 9 / 4.0;`?
4. Escribe la consulta que cuenta los pedidos de cada cliente, incluidos los que no tienen ninguno, con `customers(id, name)` y `orders(id, customer_id)`.
5. ¿Por qué `GROUP BY c.name` es una mala idea para contar los pedidos de cada cliente, si la consulta corre sin error?

<details><summary>Respuestas</summary>

1. 200 y 170: `COUNT(*)` cuenta filas, y `COUNT(discount)`, solo los valores que no son `NULL`.
2. `COUNT(customer_id)` cuenta los pedidos que tienen cliente: un cliente con 5 pedidos cuenta 5 veces. `COUNT(DISTINCT customer_id)` cuenta los clientes distintos que hicieron al menos un pedido.
3. `2`: los dos son enteros y la división descarta el resto. `2.25`: basta que uno tenga decimales.
4. `SELECT c.id, c.name, COUNT(o.id) AS orders FROM customers AS c LEFT JOIN orders AS o ON o.customer_id = c.id GROUP BY c.id, c.name;`
5. Porque dos clientes con el mismo nombre quedan en un solo grupo y sus pedidos se suman. Se agrupa por la clave, `c.id`, y se agrega el nombre para mostrarlo.
</details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · `COUNT(columna)` cuenta valores, no valores distintos
```text
01_application_summary.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 1; obtenidas: 1
  Esperadas que no salieron:
    (16, 8, 9, '2026-11-04', '2026-11-22')
  Obtenidas que no se esperaban:
    (16, 16, 16, '2026-11-04', '2026-11-22')
```

16 en las tres primeras columnas: `COUNT(candidate_id)` cuenta cada valor que no es `NULL`, y en `applications` hay 16, uno por postulación. Ana Quispe cuenta tres veces, una por cada postulación suya. Para contar personas, cada `candidate_id` tiene que contar una sola vez:

```sql
SELECT COUNT(*) AS applications, COUNT(DISTINCT candidate_id) AS candidates, COUNT(DISTINCT job_id) AS jobs,
       MIN(applied_on) AS first_applied, MAX(applied_on) AS last_applied
FROM applications;
```

8 personas, porque Diego Flores no postuló, y 9 ofertas, porque la 10 no recibió postulaciones. `COUNT(id)` en lugar de `COUNT(*)` también pasa: `id` es la clave primaria y nunca es `NULL`.

### Tarea 2 · Un entero entre otro entero pierde los decimales
```text
02_salary_by_company.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 5
  Esperadas que no salieron:
    ('Clínica Central', 2, 987.5)
  Obtenidas que no se esperaban:
    ('Clínica Central', 2, 987)
```

Una empresa: Clínica Central sale con 987 en lugar de 987.5. `SUM(j.salary_usd)` es 1975, un entero, y `COUNT(j.salary_usd)` es 2, otro entero. En SQLite, un entero dividido entre un entero da un entero (*integer division*): se queda con la parte entera y descarta el resto, sin avisar. `7 / 2` da `3`; `7 / 2.0` da `3.5`, porque basta que uno de los dos tenga decimales. En las otras cuatro empresas la división es exacta y el error no se nota. `AVG` divide con decimales y deja fuera los `NULL` por su cuenta:

```sql
SELECT c.name AS company, COUNT(*) AS jobs, AVG(j.salary_usd) AS avg_salary
FROM companies AS c
JOIN jobs AS j ON j.company_id = c.id
GROUP BY c.id, c.name;
```

`AVG` devuelve siempre un número con decimales, `1350.0` y no `1350`; las pruebas toman los dos como iguales. `SUM(j.salary_usd) * 1.0 / COUNT(j.salary_usd)` también pasa: multiplicar por `1.0` convierte la suma en un número con decimales antes de dividir. `SUM(j.salary_usd) / COUNT(*)` no pasa: Andes Retail sale con 900 y no con 1350, porque `COUNT(*)` cuenta también la oferta 9, que no tiene sueldo. Si escribiste `GROUP BY c.name`, también pasa con estos datos, porque no hay dos empresas con el mismo nombre; la tarea 3 muestra por qué conviene la clave.

### Tarea 3 · Agrupar por el nombre junta a las personas que se llaman igual
```text
03_applications_by_candidate.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 8; obtenidas: 7
  Esperadas que no salieron:
    (2, 'Luis Ramírez', 2)
    (6, 'Luis Ramírez', 2)
  Obtenidas que no se esperaban:
    (2, 'Luis Ramírez', 4)
```

7 filas: los dos Luis Ramírez, que son personas distintas, quedaron en un solo grupo con 4 postulaciones. `GROUP BY c.name` arma un grupo por cada nombre, no por cada persona. Además, `c.id` no está en el `GROUP BY` ni dentro de una función de agregado: SQLite no da error y pone el `id` de una de las filas del grupo, aquí el 2 en las tres versiones probadas. PostgreSQL rechaza esa consulta (ver 💼). Agrupa por lo que identifica a cada persona, su `id`, y agrega el nombre para poder mostrarlo:

```sql
SELECT c.id, c.name, COUNT(*) AS applications
FROM candidates AS c
JOIN applications AS a ON a.candidate_id = c.id
GROUP BY c.id, c.name;
```

`GROUP BY c.id` solo también pasa, y PostgreSQL también la acepta, porque `c.id` es la clave primaria. `GROUP BY c.name, c.city` pasa con estos datos, porque los dos Luis viven en ciudades distintas, pero dejaría de funcionar con dos personas del mismo nombre en la misma ciudad: agrupa por el `id`.

### Tarea 4 · `COUNT(*)` cuenta también la fila completada con `NULL`
```text
04_applications_by_company.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 6; obtenidas: 6
  Esperadas que no salieron:
    ('Banco Sur', 2)
    ('Nube Andina', 0)
  Obtenidas que no se esperaban:
    ('Banco Sur', 3)
    ('Nube Andina', 1)
```

Dos empresas: Nube Andina sale con 1 en lugar de 0, y Banco Sur con 3 en lugar de 2. Los `LEFT JOIN` conservan a Nube Andina, que no tiene ofertas, y a la oferta 10 de Banco Sur, que no tiene postulaciones, cada una en una fila con las columnas de `applications` en `NULL`. Esa fila existe, y `COUNT(*)` cuenta filas. Para contar postulaciones, cuenta una columna de `applications` que solo esté en `NULL` cuando no hubo postulación, como su clave primaria:

```sql
SELECT c.name AS company, COUNT(a.id) AS applications
FROM companies AS c
LEFT JOIN jobs AS j ON j.company_id = c.id
LEFT JOIN applications AS a ON a.job_id = j.id
GROUP BY c.id, c.name;
```

Es la misma regla del *anti-join* del lab 2.3: la columna que miras tiene que estar en `NULL` solo en la fila sin pareja. `COUNT(a.candidate_id)` y `COUNT(a.job_id)` también pasan, porque nunca son `NULL` en una postulación que existe. `COUNT(j.id)` no pasa: cuenta la fila de la oferta 10, que sí existe, y Banco Sur sale con 3.
</details>

La solución completa está en [`solution/`](solution/).
