# 🧩 2.7 · Unir y restar resultados

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | ➕ `elective` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Juntar en un solo resultado las filas de dos consultas, con `UNION` y `UNION ALL`.
- Decidir cuándo usar `UNION` y cuándo `UNION ALL`.
- Encontrar las filas que están en los resultados de dos consultas, con `INTERSECT`.
- Restar el resultado de una consulta del de otra, con `EXCEPT`.
- Revisar una consulta compuesta corriendo sola cada una de sus partes.

## 💡 Por qué importa
A veces los datos que quieres ver juntos están en dos tablas que no se unen por una clave: las ciudades de las empresas y las de las personas, las fechas de las ofertas y las de las postulaciones. Un `JOIN` pone columnas una al lado de otra; los operadores de este lab ponen filas una debajo de otra, comparan dos listas o restan una de otra. «¿Qué diferencia hay entre `UNION` y `UNION ALL`?» es una pregunta frecuente en entrevistas.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/02-combine-and-summarize/07-set-operations/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la base de las tareas, que es la misma del [lab 2.1](../01-table-relationships/README.md) (ver [La base](#la-base)). No hace falta correrlos; si quieres probarlos, crea la base y abre la consola como en el [experimento 1 del lab 2.1](../01-table-relationships/README.md#experimento-1--crear-la-base-y-ver-sus-tablas): dan las mismas filas.

### Poner las filas de una consulta debajo de las de otra (`UNION`)
La bolsa quiere destacar dos grupos de ofertas: las remotas y las que pagan 2000 o más. Cada grupo sale con una consulta del bloque 1:

```sql
SELECT id, title FROM jobs WHERE mode = 'remoto';
SELECT id, title FROM jobs WHERE salary_usd >= 2000;
```

La primera devuelve las ofertas 2, 6 y 8; la segunda, la 6 y la 7. Se quiere una sola lista, sin correr dos consultas y copiar una debajo de la otra.

La idea: escribir las dos consultas, una después de otra, con una palabra en medio que junta sus filas en un solo resultado:

```sql
SELECT id, title FROM jobs WHERE mode = 'remoto'
UNION
SELECT id, title FROM jobs WHERE salary_usd >= 2000;
```

| id | title |
|---|---|
| 2 | Desarrollador backend |
| 6 | Desarrolladora full stack |
| 7 | Administrador de bases de datos |
| 8 | Analista de calidad (QA) |

`UNION` junta las filas de las dos consultas y quita las repetidas: la oferta 6 está en las dos y sale una vez. El punto y coma va solo al final, porque todo es una sola consulta. Las dos consultas devuelven el mismo número de columnas, aquí dos.

Si quieres todas las filas, también las repetidas, escribe `UNION ALL`:

```sql
SELECT id, title FROM jobs WHERE mode = 'remoto'
UNION ALL
SELECT id, title FROM jobs WHERE salary_usd >= 2000;
```

| id | title |
|---|---|
| 2 | Desarrollador backend |
| 6 | Desarrolladora full stack |
| 8 | Analista de calidad (QA) |
| 6 | Desarrolladora full stack |
| 7 | Administrador de bases de datos |

`UNION ALL` pone las filas de la segunda consulta debajo de las de la primera, sin comparar nada: salen 3 + 2 = 5 filas.

### Las filas que están en los dos resultados (`INTERSECT`)
¿Quiénes postularon a la oferta 1 y también a la oferta 5? Con `WHERE job_id = 1 AND job_id = 5` no sale nadie: cada fila de `applications` es una sola postulación, con un solo `job_id`, y no puede valer 1 y 5 a la vez. La pregunta compara dos listas de personas, la de cada oferta.

La idea: una consulta para cada lista, y una palabra que deja las filas que están en las dos:

```sql
SELECT candidate_id FROM applications WHERE job_id = 1
INTERSECT
SELECT candidate_id FROM applications WHERE job_id = 5;
```

| candidate_id |
|---|
| 1 |
| 4 |

A la oferta 1 postularon las personas 1, 4 y 6, y a la oferta 5, las personas 1, 4 y 7: `INTERSECT` deja las filas que están en los dos resultados (*intersect* es «cruzarse» en inglés).

### Las filas de un resultado que no están en el otro (`EXCEPT`)
¿Qué ofertas no recibieron ninguna postulación? En el lab 2.6 lo respondiste con `NOT EXISTS`. Con dos listas, la pregunta es: de todos los `id` de `jobs`, ¿cuáles no están entre los `job_id` de `applications`?

La idea: una consulta para cada lista, y una palabra que quita de la primera lo que está en la segunda:

```sql
SELECT id FROM jobs
EXCEPT
SELECT job_id FROM applications;
```

| id |
|---|
| 10 |

`EXCEPT` («excepto») devuelve las filas de la primera consulta que no están en la segunda: la misma oferta 10 que encontró `NOT EXISTS` en el lab 2.6.

`UNION`, `UNION ALL`, `INTERSECT` y `EXCEPT` se llaman **operadores de conjuntos** (*set operators*), y una consulta hecha de varias consultas unidas por ellos es una **consulta compuesta** (*compound query*). Para revisarla, corre sola cada parte y compara sus filas con las del resultado.

## 📚 Documentación
- [SQLite: consultas compuestas](https://www.sqlite.org/lang_select.html#compound), en inglés: `UNION`, `UNION ALL`, `INTERSECT` y `EXCEPT`, y cómo se ordena el resultado
- [PostgreSQL: combinar consultas](https://www.postgresql.org/docs/current/queries-union.html), en inglés, con las formas `INTERSECT ALL` y `EXCEPT ALL`

## 🧭 Escenario
La bolsa de trabajo prepara un directorio de contactos y un informe de actividad, y quiere comparar dónde están las empresas y dónde están las personas. Te pide cuatro consultas.

### La base
Son las cuatro tablas del [lab 2.1](../01-table-relationships/README.md#-escenario), con los mismos datos de los labs 2.2 a 2.4 y 2.6. Este es su diagrama en texto:

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
│   ├── 01_contact_directory.sql
│   ├── 02_total_events.sql
│   ├── 03_shared_cities.sql
│   └── 04_candidate_only_cities.sql
├── seed.sql                                  crea las cuatro tablas y sus filas
├── tests/
│   ├── conftest.py                           prepara la base y compara resultados
│   └── test_queries.py                       las pruebas: una clase por tarea
└── pyproject.toml                            le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Una consulta compuesta es una sola consulta, con un solo punto y coma al final. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../../01-query-a-table/02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). Ninguna tarea pide un orden: las filas pueden salir en cualquiera. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 4, una por tarea.

### Tarea 1 · Un directorio de empresas y personas
**Objetivo:** el nombre y la ciudad de cada empresa y de cada persona, en una sola lista. Columnas `name` y `city`. **Lo valida:** [`TestTask1ContactDirectory`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Qué crees que pasa: pasa la prueba, devuelve otras filas o da un error? Si devuelve otras filas, ¿cuántas filas devuelve? Escribe tu predicción y después pon la consulta en [`queries/01_contact_directory.sql`](starter/queries/01_contact_directory.sql):

```sql
SELECT name, city FROM companies
UNION
SELECT city, name FROM candidates;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1ContactDirectory` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 3 fallan.

### Tarea 2 · Cuántos eventos registró la bolsa
**Objetivo:** cada oferta publicada y cada postulación cuentan como un evento. Junta en una sola columna las fechas de publicación de las ofertas (`posted_on`) y las fechas de las postulaciones (`applied_on`), y cuenta las filas. Columna `events`, 1 fila. **Lo valida:** [`TestTask2TotalEvents`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta, con la consulta compuesta como subconsulta en el `FROM`, como en el [lab 2.5](../05-filter-groups/README.md#una-consulta-agrupada-dentro-del-from). ¿Crees que pasa la prueba? Si no pasa, ¿qué número crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/02_total_events.sql`](starter/queries/02_total_events.sql):

```sql
SELECT COUNT(*) AS events
FROM (
    SELECT posted_on FROM jobs
    UNION
    SELECT applied_on FROM applications
) AS e;
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2TotalEvents` pasa. Con todas las pruebas, 3 pasan y 2 fallan.

### Tarea 3 · Las ciudades con empresas y con personas
**Objetivo:** las ciudades donde hay al menos una empresa y al menos una persona, cada ciudad una vez. Columna `city`. **Lo valida:** [`TestTask3SharedCities`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero lo resolvió con `IN` y una subconsulta, como en el lab 2.6. ¿Crees que pasa la prueba? Si no pasa, ¿cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/03_shared_cities.sql`](starter/queries/03_shared_cities.sql):

```sql
SELECT city
FROM companies
WHERE city IN (SELECT city FROM candidates);
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que use un operador de conjuntos y dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3SharedCities` pasa. Con todas las pruebas, 4 pasan y 1 falla.

### Tarea 4 · Las ciudades con personas y sin empresas
**Objetivo:** las ciudades donde vive al menos una persona y no hay ninguna empresa. Columna `city`, 1 fila. **Lo valida:** [`TestTask4CandidateOnlyCities`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta. ¿Crees que pasa la prueba? Si no pasa, ¿cuántas filas crees que devuelve? Escribe tu predicción y después pon la consulta en [`queries/04_candidate_only_cities.sql`](starter/queries/04_candidate_only_cities.sql):

```sql
SELECT city FROM companies
EXCEPT
SELECT city FROM candidates;
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que use un operador de conjuntos y dé lo que pide el objetivo, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask4CandidateOnlyCities` pasa, y con todas las pruebas, pasan las 5.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `SELECT … UNION SELECT …` | Junta las filas de las dos consultas y quita las repetidas |
| `SELECT … UNION ALL SELECT …` | Junta todas las filas de las dos consultas, también las repetidas |
| `SELECT … INTERSECT SELECT …` | Deja las filas que están en los dos resultados |
| `SELECT … EXCEPT SELECT …` | Deja las filas de la primera consulta que no están en la segunda |
| `FROM (SELECT … UNION ALL SELECT …) AS e` | Usa el resultado de la consulta compuesta como una tabla (lab 2.5) |

## 💼 En proyectos reales
- **`ORDER BY` va una sola vez, al final, y ordena el resultado completo.** Escrito antes del `UNION`, SQLite responde `ORDER BY clause should come after UNION not before` ([SQLite](https://www.sqlite.org/lang_select.html#compound)).
- **Usa `UNION ALL` cuando las filas repetidas cuentan o no pueden existir.** `UNION` tiene que comparar todas las filas para quitar las repetidas; `UNION ALL` solo las pone una debajo de otra. Un informe que junta las ventas de dos tiendas usa `UNION ALL`: dos ventas iguales siguen siendo dos ventas.
- **Para estos operadores, dos `NULL` son iguales**, al revés que en un `WHERE` ([SQLite](https://www.sqlite.org/lang_select.html#compound)). `SELECT id FROM candidates EXCEPT SELECT referred_by FROM candidates` devuelve las 5 personas que no recomendaron a nadie, las mismas de la tarea 4 del lab 2.6, aunque la segunda consulta tiene cuatro `NULL`: el `NOT IN` de esa tarea devolvía 0 filas.
- **PostgreSQL también tiene `INTERSECT ALL` y `EXCEPT ALL`**, que no quitan las filas repetidas ([PostgreSQL](https://www.postgresql.org/docs/current/queries-union.html); no se corrió allí). SQLite no las tiene: `INTERSECT ALL` da `near "ALL": syntax error`.
- **Un operador de conjuntos compara filas completas.** Para saber qué personas viven en una ciudad sin empresas, primero `EXCEPT` da las ciudades, y después un `IN` con esa consulta compuesta como subconsulta trae a las personas.

## 🆘 Pistas
<details><summary>Pista 1 · Tarea 1</summary>

Corre sola cada una de las dos consultas del compañero: ¿qué columna devuelve primero cada una? Cuando `UNION` pone una fila de la segunda debajo de la primera, ¿cómo decide qué valor va en la columna `name`: por el nombre de la columna o por su lugar?
</details>

<details><summary>Pista 2 · Tarea 2</summary>

Corre sola la consulta compuesta de adentro, sin el `COUNT`: ¿cuántas filas devuelve? Busca en las tablas `jobs` y `applications` una fecha en la que pasó más de un evento. ¿Qué hace `UNION` con dos filas iguales?
</details>

<details><summary>Pista 3 · Tarea 3</summary>

Mira qué ciudad sale dos veces en el resultado del compañero. ¿Cuántas filas de `companies` tienen esa ciudad? El `WHERE` decide fila por fila de `companies`: ¿qué operador de Conceptos compara las dos listas de ciudades y devuelve cada fila una vez?
</details>

<details><summary>Pista 4 · Tarea 4</summary>

Lee la consulta del compañero en voz alta, con la definición de `EXCEPT` de Conceptos: «las ciudades de ___ que no están en las ciudades de ___». ¿Es la pregunta del objetivo?
</details>

## 🎤 Autoevaluación
1. ¿Qué diferencia hay entre `UNION` y `UNION ALL`? ¿Cuál usarías para juntar los pagos de dos meses y sumarlos?
2. En `clients_2025(email)` y `clients_2026(email)`, escribe la consulta de los correos que compraron en 2025 y no volvieron en 2026.
3. Con las mismas tablas, escribe la consulta de los correos que compraron los dos años.
4. `SELECT name, email FROM clients UNION SELECT email, name FROM suppliers;` no da ningún error. ¿Qué hay de raro en su resultado?
5. ¿Por qué `A EXCEPT B` y `B EXCEPT A` dan resultados distintos, y `A INTERSECT B` y `B INTERSECT A` no?

<details><summary>Respuestas</summary>

1. `UNION` quita las filas repetidas y `UNION ALL` las deja todas. Para sumar pagos, `UNION ALL`: dos pagos del mismo monto son dos pagos, y `UNION` dejaría uno.
2. `SELECT email FROM clients_2025 EXCEPT SELECT email FROM clients_2026;`
3. `SELECT email FROM clients_2025 INTERSECT SELECT email FROM clients_2026;`
4. Las columnas se juntan por su lugar: los correos de los proveedores quedan en la columna `name` y sus nombres en la columna `email`.
5. `EXCEPT` quita de la primera consulta lo que está en la segunda, así que importa cuál va primero; `INTERSECT` deja lo que está en las dos, y eso no depende del orden.
</details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · `UNION` junta las columnas por su lugar, no por su nombre
```text
01_contact_directory.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 15; obtenidas: 15
  Esperadas que no salieron:
    ('Ana Quispe', 'Lima')
    ('Luis Ramírez', 'Bogotá')
    ('María Torres', 'Arequipa')
    ('Jorge Huamán', 'Lima')
    ('Sofía Castro', 'Santiago')
    ('Luis Ramírez', 'Lima')
    ('Carmen Rojas', 'Trujillo')
    ('Diego Flores', 'Cusco')
    ('Valeria Paredes', 'Lima')
  Obtenidas que no se esperaban:
    ('Arequipa', 'María Torres')
    ('Bogotá', 'Luis Ramírez')
    ('Cusco', 'Diego Flores')
    ('Lima', 'Ana Quispe')
    ('Lima', 'Jorge Huamán')
    ('Lima', 'Luis Ramírez')
    ('Lima', 'Valeria Paredes')
    ('Santiago', 'Sofía Castro')
    ('Trujillo', 'Carmen Rojas')
```

15 filas, sin error, y las 9 personas con la ciudad en la columna `name`. `UNION` pone la primera columna de la segunda consulta debajo de la primera columna de la primera consulta, y así con cada una, sin mirar sus nombres; los nombres de las columnas del resultado salen de la primera consulta. Como las dos consultas devuelven dos columnas, SQLite no tiene nada que reclamar. Con las columnas en el mismo orden en las dos consultas:

```sql
SELECT name, city FROM companies
UNION
SELECT name, city FROM candidates;
```

También pasa `UNION ALL`, y aquí la elección no importa: la pregunta pide cada contacto, y ninguna pareja de nombre y ciudad se repite (los dos Luis Ramírez viven en ciudades distintas), así que las dos formas dan las mismas 15 filas. Si una empresa y una persona tuvieran el mismo nombre y la misma ciudad, `UNION ALL` las mostraría como los dos contactos que son, y `UNION` dejaría uno. También pasa escribir primero la consulta de `candidates`. Si una consulta devuelve más columnas que la otra, SQLite responde `SELECTs to the left and right of UNION do not have the same number of result columns`.

### Tarea 2 · `UNION` quita las fechas repetidas antes de contar
```text
02_total_events.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 1; obtenidas: 1
  Esperadas que no salieron:
    (26,)
  Obtenidas que no se esperaban:
    (18,)
```

18 en lugar de 26 (10 ofertas y 16 postulaciones). La subconsulta junta las fechas, y `UNION` quita las repetidas: el 2026-11-06 se publicó la oferta 3 y llegaron las postulaciones 4 y 11, tres eventos que quedan en una sola fila. Quedan 18 fechas distintas, y `COUNT(*)` cuenta fechas, no eventos. Dos eventos del mismo día siguen siendo dos eventos, así que aquí las filas repetidas cuentan:

```sql
SELECT COUNT(*) AS events
FROM (
    SELECT posted_on FROM jobs
    UNION ALL
    SELECT applied_on FROM applications
) AS e;
```

También pasa sumar dos subconsultas escalares, `SELECT (SELECT COUNT(*) FROM jobs) + (SELECT COUNT(*) FROM applications) AS events`. `UNION` con los `id` en lugar de las fechas tampoco pasa: da 16, porque los `id` 1 a 10 de `jobs` también están entre los de `applications`.

### Tarea 3 · `IN` revisa cada empresa, no cada ciudad
```text
03_shared_cities.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 6
  Esperadas que no salieron:
    (ninguna)
  Obtenidas que no se esperaban:
    ('Lima',)
```

6 filas: Lima sale dos veces. El `WHERE` revisa cada fila de `companies`, y Andes Retail y Nube Andina están las dos en Lima, así que las dos filas pasan el `IN`. `INTERSECT` compara las dos listas de ciudades y, como `UNION` y `EXCEPT`, devuelve cada fila una vez:

```sql
SELECT city FROM companies
INTERSECT
SELECT city FROM candidates;
```

Con las consultas al revés (`candidates` primero) da lo mismo: una ciudad que está en las dos listas está en las dos, se mire desde cualquier lado. El `IN` del compañero con `SELECT DISTINCT city` también pasa, igual que un `JOIN` por la ciudad con `DISTINCT`; sin `DISTINCT`, ese `JOIN` da 12 filas, una por cada pareja de empresa y persona de la misma ciudad.

### Tarea 4 · `EXCEPT` resta la segunda consulta de la primera
```text
04_candidate_only_cities.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 1; obtenidas: 0
  Esperadas que no salieron:
    ('Cusco',)
  Obtenidas que no se esperaban:
    (ninguna)
```

0 filas. La consulta del compañero responde otra pregunta: las ciudades con empresas y sin personas, y no hay ninguna, porque en las cinco ciudades de las empresas vive alguien. `INTERSECT` y `UNION` dan lo mismo con las consultas en cualquier orden; `EXCEPT` no, porque quita de la primera lo que está en la segunda. Con `candidates` primero:

```sql
SELECT city FROM candidates
EXCEPT
SELECT city FROM companies;
```

Sale Cusco, donde vive Diego Flores. También pasa `SELECT city FROM candidates WHERE city NOT IN (SELECT city FROM companies)`, porque una sola persona vive en Cusco (con dos, Cusco saldría dos veces), y `NOT EXISTS` con `SELECT DISTINCT`. `INTERSECT` no pasa: da las otras 5 ciudades.
</details>

La solución completa está en [`solution/`](solution/).
