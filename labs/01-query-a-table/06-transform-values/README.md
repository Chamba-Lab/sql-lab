# 🧩 1.6 · Transformar valores

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Unir textos con `||` y limpiar los que llegan desordenados con `LOWER`, `UPPER` y `TRIM`.
- Sacar una parte de un texto con `SUBSTR` y cambiar un pedazo por otro con `REPLACE`.
- Trabajar con fechas guardadas como texto: quedarte con el día, sumar días y filtrar un mes sin perder filas.
- Clasificar filas según reglas con `CASE`.
- Responder las preguntas de entrevista sobre fechas como texto, `NULL` en un texto unido y el orden de un `CASE`.

## 💡 Por qué importa
Los datos casi nunca llegan como los necesitas. Un formulario web guarda correos con espacios y mayúsculas, un código escrito de dos formas, una fecha con su hora. Si los comparas tal como vienen, la consulta pierde filas sin dar ningún error. Limpiarlos y transformarlos dentro de la consulta es parte de casi todo reporte, y de casi toda prueba técnica.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/01-query-a-table/06-transform-values/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la tabla `jobs` del [lab 1.1](../01-first-database/README.md) o un `SELECT` sin `FROM` (del [lab 1.4](../04-null-values/README.md)). No hace falta correrlos; si quieres probarlos, abre su base con la consola de ese lab. Los nombres de las funciones van en mayúscula, como `ROUND` y `COALESCE` en los labs anteriores; SQLite los acepta también en minúscula (`lower`), como los escribe su documentación.

### Unir textos (*concatenar*)
Para armar un texto con varias columnas, se pegan con **`||`**, dos barras verticales. Unir textos así se llama **concatenar**:

```sql
SELECT title || ' en ' || company AS offer
FROM jobs
WHERE city = 'Lima';
```

| offer |
|---|
| Analista de datos júnior en Andes Retail |
| Analista de BI en Andes Retail |
| Analista de calidad (QA) en Clínica Central |

El espacio no aparece solo: va dentro del texto `' en '`.

### Mayúsculas y espacios (*lower*, *upper*, *trim*)
Una **función** recibe valores entre paréntesis y devuelve otro valor, como `ROUND` del [lab 1.2](../02-first-queries/README.md). Tres funciones ordenan un texto desprolijo: **`LOWER`** lo pasa a minúsculas, **`UPPER`** a mayúsculas y **`TRIM`** le quita los espacios del comienzo y del final (no los del medio):

```sql
SELECT UPPER('remoto'), LOWER('Banco Sur'), TRIM('  Lima  ');
```

| UPPER('remoto') | LOWER('Banco Sur') | TRIM('  Lima  ') |
|---|---|---|
| REMOTO | banco sur | Lima |

Una función puede ir dentro de otra: `UPPER(TRIM(x))` primero quita los espacios y después pasa a mayúsculas. Ojo: en SQLite, `LOWER` y `UPPER` solo cambian las letras sin tilde (`LOWER('ÑANDÚ')` da `'ÑandÚ'`); para correos y códigos alcanza.

### Partes de un texto (*substr*, *replace*)
**`SUBSTR(texto, inicio, cuántos)`** devuelve un pedazo del texto: desde la posición `inicio`, `cuántos` caracteres. Las posiciones se cuentan desde la primera letra, que es la posición 1. Sin el tercer valor, devuelve hasta el final:

```sql
SELECT company, SUBSTR(company, 1, 4) AS start, SUBSTR(company, 6) AS rest
FROM jobs
WHERE city = 'Lima';
```

| company | start | rest |
|---|---|---|
| Andes Retail | Ande | ` Retail` |
| Andes Retail | Ande | ` Retail` |
| Clínica Central | Clín | ca Central |

`rest` de *Andes Retail* empieza con un espacio: la posición 6 es el espacio después de *Andes*.

**`REPLACE(texto, buscado, nuevo)`** cambia cada aparición de `buscado` por `nuevo`, distinguiendo mayúsculas: `REPLACE('Analista de BI', 'BI', 'datos')` da `'Analista de datos'`.

### Fechas como texto (*ISO-8601*, *date*, *strftime*)
SQLite no tiene un tipo de dato para fechas: las guarda como texto. Para que funcionen, se escriben en el formato **ISO-8601**: año, mes y día con ceros a la izquierda, y la hora después de un espacio, si la hay: `'2026-11-20'` o `'2026-11-20 18:45'`. Así, comparar dos fechas como textos, carácter por carácter, da el mismo resultado que compararlas como fechas, y también funcionan `ORDER BY` y `BETWEEN`.

Dos funciones leen ese texto:

- **`DATE(fecha)`** devuelve solo el día, `'AAAA-MM-DD'`. Después de la fecha acepta **modificadores** (*modifiers*), textos que la mueven: `'+15 days'` suma 15 días y `'start of month'` va al primer día del mes.
- **`STRFTIME(formato, fecha)`** escribe la fecha con el formato que le das: `%Y` es el año, `%m` el mes y `%d` el día, siempre con dos cifras.

```sql
SELECT DATE('2026-11-20 18:45'),
       STRFTIME('%Y-%m', '2026-11-20 18:45'),
       DATE('2026-11-20', '+15 days'),
       DATE('2026-11-20', 'start of month');
```

| DATE('2026-11-20 18:45') | STRFTIME('%Y-%m', '2026-11-20 18:45') | DATE('2026-11-20', '+15 days') | DATE('2026-11-20', 'start of month') |
|---|---|---|---|
| 2026-11-20 | 2026-11 | 2026-12-05 | 2026-11-01 |

`DATE` sabe cuántos días tiene cada mes: 20 de noviembre más 15 días cae en diciembre.

### Clasificar según reglas (*CASE*)
En una hoja de cálculo lo harías con `SI(…)`. En SQL, **`CASE`** revisa condiciones y devuelve el valor de la que se cumple, como una columna más:

```sql
SELECT title, mode,
       CASE
           WHEN mode = 'remoto' THEN 'desde casa'
           WHEN mode = 'híbrido' THEN 'mixto'
           ELSE 'en oficina'
       END AS place
FROM jobs
WHERE city = 'Lima';
```

| title | mode | place |
|---|---|---|
| Analista de datos júnior | híbrido | mixto |
| Analista de BI | presencial | en oficina |
| Analista de calidad (QA) | remoto | desde casa |

Cada `WHEN` lleva una condición, como las del `WHERE`, y su `THEN` el valor que devuelve. Si no se cumple ninguna, `CASE` devuelve lo del `ELSE`, y sin `ELSE`, `NULL`. Termina siempre con `END`.

## 📚 Documentación
- [SQLite: funciones de texto](https://www.sqlite.org/lang_corefunc.html) (`LOWER`, `UPPER`, `TRIM`, `SUBSTR`, `REPLACE`) y [el operador `||`](https://www.sqlite.org/lang_expr.html#operators_and_parse_affecting_attributes)
- [SQLite: funciones de fecha y hora](https://www.sqlite.org/lang_datefunc.html), con sus modificadores y los formatos de `STRFTIME`
- [SQLite: `CASE`](https://www.sqlite.org/lang_expr.html#the_case_expression)

## 🧭 Escenario
Una bolsa de trabajo junta las postulaciones que llegan por su formulario web. Antes de pasarlas a las empresas, el equipo quiere ordenarlas: nombres completos, correos limpios, el área de cada puesto, las postulaciones de marzo, el plazo para responder y el rango de sueldo que pide cada persona. Te pide seis consultas.

### Las postulaciones
La tabla `applications` tiene una fila por postulación.

| Columna | Tipo | Qué guarda |
|---|---|---|
| `id` | `INTEGER` | El número de la postulación |
| `first_name` | `TEXT` | El nombre de quien postula |
| `last_name` | `TEXT` | Su apellido; `NULL` si no lo escribió |
| `email` | `TEXT` | Su correo, tal como lo escribió; `NULL` si no lo dejó |
| `job_code` | `TEXT` | El código del puesto: tres letras del área y un número |
| `applied_at` | `TEXT` | La fecha y la hora de la postulación, en ISO-8601 |
| `expected_salary` | `INTEGER` | El sueldo que pide, en soles al mes; `NULL` si no lo dijo |

Estos son todos sus datos. Los correos van entre comillas para que se vean sus espacios:

| id | first_name | last_name | email | job_code | applied_at | expected_salary |
|---|---|---|---|---|---|---|
| 1 | Ana | Torres | `' Ana.Torres@Example.com'` | DAT-104 | 2026-03-12 10:30 | 1800 |
| 2 | Luis | Quispe | `'luis.quispe@example.net '` | DEV 310 | 2026-02-28 23:50 | 2500 |
| 3 | Rosa | Mamani | `'ROSA.MAMANI@EXAMPLE.COM'` | SOP-007 | 2026-03-01 08:15 | 1200 |
| 4 | Diego | `NULL` | `'diego.r@example.com'` | DAT 221 | 2026-04-01 00:05 | `NULL` |
| 5 | Carla | Huamán | `'carla.huaman@example.org'` | DEV-118 | 2026-03-31 18:20 | 3200 |
| 6 | Jorge | Salazar | `NULL` | SOP 015 | 2025-03-20 09:00 | 1500 |
| 7 | Valeria | Ríos | `' vale.rios@example.com '` | DAT-104 | 2026-01-15 14:00 | 1450 |
| 8 | Miguel | Paredes | `'Miguel.Paredes@example.com'` | DEV-310 | 2026-03-20 16:45 | 2200 |
| 9 | Lucía | Fernández | `'lucia.fdz@example.org'` | DAT-221 | 2026-03-05 09:10 | 1000 |
| 10 | Pedro | Vargas | `'pedro.vargas@example.com '` | SOP-007 | 2026-02-10 11:00 | 2800 |

### Tus archivos
```text
starter/
├── queries/               tus seis consultas, una por tarea
│   ├── 01_full_name.sql
│   ├── 02_clean_emails.sql
│   ├── 03_job_area.sql
│   ├── 04_march.sql
│   ├── 05_reply_by.sql
│   └── 06_salary_band.sql
├── seed.sql               crea la tabla y sus 10 filas
├── tests/
│   ├── conftest.py        prepara la base y compara resultados
│   └── test_queries.py    las pruebas: una clase por tarea
└── pyproject.toml         le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). Ninguna tarea pide un orden: las filas se comparan sin mirarlo. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 6, una por tarea.

### Tarea 1 · El nombre completo
**Objetivo:** el nombre completo de cada persona: su nombre, un espacio y su apellido. Si no tiene apellido, solo su nombre, sin espacio al final. Columnas `id` y `full_name`, con las 10 postulaciones. **Lo valida:** [`TestTask1FullName`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero que viene de Python unió los textos con `+`. ¿Qué crees que sale en `full_name` para Ana Torres? Escribe tu predicción y después pon la consulta en [`queries/01_full_name.sql`](starter/queries/01_full_name.sql):

```sql
SELECT id, first_name + ' ' + last_name AS full_name
FROM applications;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva el nombre completo que pide la tarea, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1FullName` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 5 fallan.

### Tarea 2 · Los correos limpios
**Objetivo:** cada correo en minúsculas y sin espacios al comienzo ni al final, listo para comparar. Si no hay correo, queda `NULL`. Columnas `id` y `email`, con las 10 postulaciones. **Lo valida:** [`TestTask2CleanEmails`](starter/tests/test_queries.py)

🔮 **Predict first:** ¿crees que la prueba pasa con esta consulta? Escribe tu predicción y después pon la consulta en [`queries/02_clean_emails.sql`](starter/queries/02_clean_emails.sql):

```sql
SELECT id, LOWER(email) AS email
FROM applications;
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva los correos que pide la tarea, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2CleanEmails` pasa. Con todas las pruebas, 3 pasan y 4 fallan.

### Tarea 3 · El área del puesto
**Objetivo:** el formulario dejó escribir el código del puesto con un espacio (`DEV 310`) o con un guion (`DEV-310`). Devuelve cada código con guion, y en otra columna el área, sus tres primeras letras. Columnas `id`, `job_code` y `area`, con las 10 postulaciones. **Lo valida:** [`TestTask3JobArea`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero que viene de Python, donde se cuenta desde 0, escribió esta consulta (todavía sin arreglar los códigos). ¿Qué área crees que sale para `DAT-104`? Escribe tu predicción y después pon la consulta en [`queries/03_job_area.sql`](starter/queries/03_job_area.sql):

```sql
SELECT id, job_code, SUBSTR(job_code, 0, 3) AS area
FROM applications;
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva los códigos y las áreas que pide la tarea, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3JobArea` pasa. Con todas las pruebas, 4 pasan y 3 fallan.

### Tarea 4 · Las postulaciones de marzo
**Objetivo:** todas las postulaciones de marzo de 2026, a cualquier hora. Columnas `id` y `applied_at`. **Lo valida:** [`TestTask4March`](starter/tests/test_queries.py)

🔮 **Predict first:** ¿cuántas postulaciones crees que devuelve esta consulta? Escribe tu predicción y después pon la consulta en [`queries/04_march.sql`](starter/queries/04_march.sql):

```sql
SELECT id, applied_at
FROM applications
WHERE applied_at BETWEEN '2026-03-01' AND '2026-03-31';
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva todas las postulaciones de marzo de 2026, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.

**Criterio de éxito:** `TestTask4March` pasa. Con todas las pruebas, 5 pasan y 2 fallan.

### Tarea 5 · El plazo para responder
**Objetivo:** la bolsa promete responder cada postulación en 7 días. Devuelve el día de la postulación, sin la hora, y el día límite para responder: 7 días después. Columnas `id`, `applied_on` y `reply_by`, con las 10 postulaciones. **Lo valida:** [`TestTask5ReplyBy`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero sumó los 7 días con `+ 7`. ¿Qué crees que sale en `reply_by` para la postulación del 31 de marzo? Escribe tu predicción y después pon la consulta en [`queries/05_reply_by.sql`](starter/queries/05_reply_by.sql):

```sql
SELECT id,
       DATE(applied_at) AS applied_on,
       DATE(applied_at) + 7 AS reply_by
FROM applications;
```

- [ ] Corre `python -m pytest -k task5` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva el día límite que pide la tarea, y vuelve a correr `python -m pytest -k task5` hasta que la prueba pase.

**Criterio de éxito:** `TestTask5ReplyBy` pasa. Con todas las pruebas, 6 pasan y 1 falla.

### Tarea 6 · El rango de sueldo
**Objetivo:** clasifica el sueldo que pide cada persona: `'bajo'` si es menos de 1500, `'medio'` de 1500 a 2499, `'alto'` desde 2500, y `'sin dato'` si no lo dijo. Columnas `id`, `expected_salary` y `salary_band`, con las 10 postulaciones. **Lo valida:** [`TestTask6SalaryBand`](starter/tests/test_queries.py)

🔮 **Predict first:** ¿cuántas personas crees que salen como `'alto'` con esta consulta? Escribe tu predicción y después pon la consulta en [`queries/06_salary_band.sql`](starter/queries/06_salary_band.sql):

```sql
SELECT id,
       expected_salary,
       CASE
           WHEN expected_salary >= 1500 THEN 'medio'
           WHEN expected_salary >= 2500 THEN 'alto'
           WHEN expected_salary < 1500 THEN 'bajo'
           ELSE 'sin dato'
       END AS salary_band
FROM applications;
```

- [ ] Corre `python -m pytest -k task6` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que clasifique los sueldos como pide la tarea, y vuelve a correr `python -m pytest -k task6` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask6SalaryBand` pasa: las 7 pruebas pasan.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `a \|\| b` | Une dos textos en uno |
| `LOWER(x)` / `UPPER(x)` | `x` en minúsculas / en mayúsculas (solo letras sin tilde) |
| `TRIM(x)` | Quita los espacios del comienzo y del final de `x` |
| `SUBSTR(x, inicio, n)` | `n` caracteres de `x` desde la posición `inicio`; la primera es la 1 |
| `REPLACE(x, buscado, nuevo)` | Cambia cada `buscado` por `nuevo`, distinguiendo mayúsculas |
| `DATE(fecha, '+7 days')` | El día de `fecha`, `'AAAA-MM-DD'`, movido por los modificadores que siguen |
| `STRFTIME('%Y-%m', fecha)` | La fecha escrita con ese formato: `'2026-03'` |
| `CASE WHEN … THEN … ELSE … END` | El valor del `THEN` de la condición que se cumple; si ninguna, el del `ELSE` (o `NULL`) |

## 💼 En proyectos reales
- **Fechas que no están en ISO-8601 no funcionan.** `DATE('2026-3-05')` y `DATE('15/03/2026')` dan `NULL`, sin error, y como texto `'2026-12-01' < '2026-3-05'` es verdadero. Si importas datos de una hoja de cálculo, conviértelos a `'AAAA-MM-DD'` antes de guardarlos.
- **PostgreSQL y MySQL tienen tipos de fecha de verdad** (PostgreSQL: `DATE` y `TIMESTAMP`; MySQL: `DATE`, `DATETIME` y `TIMESTAMP`) y sus propias funciones para sumar días o sacar el mes. El razonamiento es el mismo, pero las funciones de fechas son lo que más cambia de un motor a otro; las funciones `DATE(…)` y `STRFTIME(…)` de este lab son de SQLite.
- **`||` no une textos en MySQL:** ahí es el `OR` lógico, salvo que se active el modo `PIPES_AS_CONCAT`. MySQL usa `CONCAT(a, b)`. PostgreSQL acepta `||`, como SQLite.
- **`CONCAT` existe también en SQLite (en todas las versiones que pide el curso), pero trata `NULL` como un texto vacío:** `CONCAT('Ana', ' ', NULL)` da `'Ana '`, con el espacio al final. Cada motor decide qué hace `CONCAT` con `NULL`; comprueba el tuyo antes de confiar en él.
- **Limpia al guardar, no solo al consultar.** Si los correos se guardan ya en minúsculas y sin espacios, ninguna consulta tiene que acordarse de limpiarlos. Lo que se guarda y cómo se valida es del bloque 3.

## 🆘 Pistas
<details><summary>Pista 1 · Diego sale como <code>None</code></summary>

¿Qué da una operación con `NULL`, según el [lab 1.4](../04-null-values/README.md)? Unir textos también es una operación. ¿Qué función del 1.4 da otro valor cuando el primero es `NULL`?
</details>

<details><summary>Pista 2 · Algunos correos siguen sin coincidir</summary>

Mira las comillas de los correos en la salida: ¿hay algo entre la comilla y la primera letra? Una función puede ir dentro de otra.
</details>

<details><summary>Pista 3 · El área tiene dos letras, o el código sigue con espacio</summary>

En SQLite, ¿cuál es la posición de la primera letra? Para el código, ¿qué carácter quieres cambiar, y por cuál?
</details>

<details><summary>Pista 4 · Falta una postulación de marzo, o sobra una de otro mes</summary>

Las fechas son textos que se comparan carácter por carácter. ¿Es `'2026-03-31 18:20'` menor o mayor que `'2026-03-31'`? Y si comparas solo el mes, ¿qué pasa con marzo de 2025? Puedes comparar solo el día, con `DATE`, o el año y el mes juntos, con `STRFTIME`. `STRFTIME` devuelve texto: compáralo con `'2026'` o `'03'`, entre comillas.
</details>

<details><summary>Pista 5 · El día límite sale como un número</summary>

`+` suma números, y la fecha es un texto. ¿Qué modificador de `DATE` suma días?
</details>

<details><summary>Pista 6 · Un sueldo cae en el rango equivocado, o sale <code>near "FROM": syntax error</code></summary>

`CASE` devuelve el valor del primer `WHEN` que se cumple y no mira los siguientes: ¿en qué orden conviene escribirlos? ¿Y qué rango le toca a quien no dijo su sueldo? Si sale `near "FROM"`, revisa que el `CASE` termine con `END`.
</details>

## 🎤 Autoevaluación
1. Una búsqueda por correo, `WHERE email = 'ana@example.com'`, no encuentra a una persona que sí está en la tabla. ¿Qué revisarías primero, y cómo escribirías la búsqueda?
2. ¿Qué devuelve `'Ana' || ' ' || last_name` cuando `last_name` es `NULL`? ¿Cómo lo evitas?
3. Una columna guarda fecha y hora, como `'2026-03-31 18:20'`. ¿Por qué `WHERE fecha <= '2026-03-31'` pierde filas, y cómo pedirías todo marzo?
4. ¿Por qué SQLite puede comparar y ordenar fechas guardadas como texto? ¿Qué pasa si una se guardó como `'5/3/2026'`?
5. En un `CASE` con `WHEN nota >= 11 THEN 'aprobado' WHEN nota >= 18 THEN 'excelente'`, ¿alguien sale como excelente? ¿Cómo lo arreglas?

<details><summary>Respuestas</summary>

1. Que el correo esté guardado tal cual se escribió: con espacios o mayúsculas. Limpiando los dos lados: `WHERE LOWER(TRIM(email)) = 'ana@example.com'`. Mejor aún, guardarlo ya limpio.
2. `NULL`: unir con `NULL` da `NULL`. Con `COALESCE`, por ejemplo `COALESCE('Ana' || ' ' || last_name, 'Ana')`.
3. Porque `'2026-03-31 18:20'` es mayor que `'2026-03-31'` como texto. Desde el primer día del mes hasta antes del primero del siguiente: `fecha >= '2026-03-01' AND fecha < '2026-04-01'`.
4. Porque en ISO-8601 van del dato más grande al más chico (año, mes, día, hora), con ceros a la izquierda, y así el orden de los textos es el de las fechas. `'5/3/2026'` se compara por su primer carácter, `'5'`, y queda después de todas las fechas que empiezan con `'2'`; `DATE('5/3/2026')` da `NULL`.
5. No: toda nota de 18 o más ya cumple `>= 11` y sale como aprobado. Se pone primero el `WHEN` más exigente: `WHEN nota >= 18 THEN 'excelente' WHEN nota >= 11 THEN 'aprobado'`.
</details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · `+` suma números, y `NULL` contagia
```text
01_full_name.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  …
  Obtenidas que no se esperaban:
    (1, 0)
    (2, 0)
    (3, 0)
    (4, None)
    …
```

`0`. En SQLite, `+` solo suma números: SQLite convierte cada texto en número, y un texto que no empieza con un número vale `0`, así que `'Ana' + ' ' + 'Torres'` da `0`, sin error. Para unir textos se usa `||`.

Con `first_name || ' ' || last_name` queda un error más: Diego sale como `None`. Unir un texto con `NULL` da `NULL`, como cualquier operación con `NULL` (lab 1.4). Si falta el apellido, el nombre completo es solo el nombre: `SELECT id, COALESCE(first_name || ' ' || last_name, first_name) AS full_name FROM applications;`. También pasan `first_name || COALESCE(' ' || last_name, '')` y `TRIM(first_name || ' ' || COALESCE(last_name, ''))`.

### Tarea 2 · Los espacios no se ven, pero cuentan
```text
02_clean_emails.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 10; obtenidas: 10
  Esperadas que no salieron:
    (1, 'ana.torres@example.com')
    (2, 'luis.quispe@example.net')
    (7, 'vale.rios@example.com')
    (10, 'pedro.vargas@example.com')
  Obtenidas que no se esperaban:
    (1, ' ana.torres@example.com')
    (2, 'luis.quispe@example.net ')
    (7, ' vale.rios@example.com ')
    (10, 'pedro.vargas@example.com ')
```

No. `LOWER` arregló las mayúsculas, pero cuatro correos traen espacios, y `' ana.torres@example.com'` no es igual a `'ana.torres@example.com'`: una búsqueda con `=` no los encontraría. Hace falta también `TRIM`: `SELECT id, LOWER(TRIM(email)) AS email FROM applications;`. El orden de las dos funciones no importa aquí (`TRIM(LOWER(email))` da lo mismo). El correo de Jorge sigue siendo `NULL`: `LOWER` y `TRIM` de `NULL` dan `NULL`, que es lo que pide la tarea.

### Tarea 3 · En SQLite se cuenta desde 1
```text
03_job_area.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  …
  Obtenidas que no se esperaban:
    (1, 'DAT-104', 'DA')
    (2, 'DEV 310', 'DE')
    (3, 'SOP-007', 'SO')
    …
```

`'DA'`, dos letras. La primera letra es la posición 1, y la posición 0 está antes del texto: `SUBSTR(job_code, 0, 3)` toma 3 posiciones desde ahí, y la primera está vacía. No da error, solo un carácter menos. Para las tres primeras letras: `SUBSTR(job_code, 1, 3)`. El código se arregla cambiando el espacio por un guion:

```sql
SELECT id,
       REPLACE(job_code, ' ', '-') AS job_code,
       SUBSTR(job_code, 1, 3) AS area
FROM applications;
```

`SUBSTR(job_code, 0, 4)` también da `'DAT'` y pasa la prueba, pero se lee como un error: escribe la posición real.

### Tarea 4 · Una fecha con hora es mayor que el mismo día sin hora
```text
04_march.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 5; obtenidas: 4
  Esperadas que no salieron:
    (5, '2026-03-31 18:20')
  Obtenidas que no se esperaban:
    (ninguna)
```

4, no 5: falta la del 31 de marzo a las 18:20. Las fechas son textos, y `'2026-03-31 18:20'` es más largo que `'2026-03-31'` con el mismo comienzo, así que es mayor y queda fuera del `BETWEEN`. Es una trampa clásica también en otros motores: donde la columna es `TIMESTAMP` o `DATETIME`, la fecha sola vale las 00:00 de ese día. Compara el año y el mes: `SELECT id, applied_at FROM applications WHERE STRFTIME('%Y-%m', applied_at) = '2026-03';`.

También pasan `DATE(applied_at) BETWEEN '2026-03-01' AND '2026-03-31'`, `applied_at LIKE '2026-03%'` y `applied_at >= '2026-03-01' AND applied_at < '2026-04-01'` (desde el primer día del mes hasta antes del primero del siguiente, la forma que más se usa en proyectos reales). `STRFTIME('%m', applied_at) = '03'` no pasa: trae también la de marzo de 2025.

### Tarea 5 · Para sumar días, un modificador
```text
05_reply_by.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  …
  Obtenidas que no se esperaban:
    (1, '2026-03-12', 2033)
    (2, '2026-02-28', 2033)
    …
    (6, '2025-03-20', 2032)
    …
```

`2033`, un número. Como en la tarea 1, `+` convierte el texto en número: SQLite lee el comienzo, `2026`, ignora el resto y suma 7. La fecha se mueve con un modificador: `SELECT id, DATE(applied_at) AS applied_on, DATE(applied_at, '+7 days') AS reply_by FROM applications;`. `DATE` sabe dónde termina cada mes: el 31 de marzo más 7 días es el `2026-04-07`, y el 28 de febrero de 2026, el `2026-03-07`. Con `DATETIME` en vez de `DATE` sale también la hora, y la prueba no pasa.

### Tarea 6 · `CASE` se queda con el primer `WHEN` que se cumple
```text
06_salary_band.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 10; obtenidas: 10
  Esperadas que no salieron:
    (2, 2500, 'alto')
    (5, 3200, 'alto')
    (10, 2800, 'alto')
  Obtenidas que no se esperaban:
    (2, 2500, 'medio')
    (5, 3200, 'medio')
    (10, 2800, 'medio')
```

Ninguna. `CASE` revisa los `WHEN` en orden y se queda con el primero que se cumple: 3200 ya es `>= 1500`, así que sale `'medio'` y el `WHEN` de `'alto'` nunca se revisa. Con rangos que se tocan, empieza por el más exigente, o escribe cada rango con sus dos bordes:

```sql
SELECT id,
       expected_salary,
       CASE
           WHEN expected_salary IS NULL THEN 'sin dato'
           WHEN expected_salary >= 2500 THEN 'alto'
           WHEN expected_salary >= 1500 THEN 'medio'
           ELSE 'bajo'
       END AS salary_band
FROM applications;
```

Cuidado con el `NULL`: sin el primer `WHEN`, Diego cae en el `ELSE` y sale como `'bajo'`, porque `NULL >= 2500` es desconocido y ningún `WHEN` se cumple (lab 1.4). Tampoco sirve `WHEN expected_salary = NULL`, que nunca se cumple: va `IS NULL`.
</details>

La solución completa está en [`solution/`](solution/).
