# 🧩 1.4 · El valor NULL

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Explicar qué es `NULL` y en qué se diferencia de un `0` o de un texto vacío.
- Encontrar las filas a las que les falta un dato, con `IS NULL` e `IS NOT NULL`.
- Predecir qué hace un `NULL` en una comparación, en un filtro y en un cálculo, con la lógica de tres valores.
- Reemplazar un dato que falta por un valor por defecto con `COALESCE`, y convertir en `NULL` un valor que significa «no hay dato» con `NULLIF`.
- Responder las preguntas sobre `NULL` que salen en las entrevistas.

## 💡 Por qué importa
Hasta ahora todas las tablas del curso tenían todos sus datos. Las reales no: un cliente no dejó su teléfono, un pedido todavía no tiene fecha de entrega, un producto no tiene descuento. SQL guarda esos huecos de una forma especial, y los filtros y los cálculos los tratan a su manera. Es uno de los temas favoritos de las entrevistas.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/01-query-a-table/04-null-values/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
La tabla `jobs` de los labs anteriores tiene todos sus datos, así que esta vez los ejemplos no usan una tabla: un `SELECT` sin `FROM` calcula sus expresiones una sola vez y devuelve una fila. Sirve para probar una expresión suelta, y también funciona en PostgreSQL y MySQL. Como el resultado no tiene alias, SQLite llama a cada columna como la expresión que la calculó (PostgreSQL, en cambio, la llama `?column?`). No hace falta correr estos ejemplos; si quieres probarlos, abre la consola del [lab 1.1](../01-first-database/README.md) (`python -m sqlite3`) y escribe el `SELECT` con su `;` al final.

### Un dato que falta (*NULL*)
Una persona se inscribe en un gimnasio y no da su teléfono. ¿Qué guardas en la columna `phone`? Un texto vacío (`''`) diría que su teléfono es un texto sin letras, y un `0` en una columna de descuento diría que su descuento es cero soles. Ninguno dice lo que pasó: **no hay dato**.

Para eso SQL tiene **`NULL`**: la marca de un valor que falta o que no se conoce. Cualquier columna puede tenerla, sea texto o número, y no es un valor como los demás: no es `0`, no es `''` y no es el texto `'NULL'`.

En las tablas de este lab, `NULL` es una celda sin valor y `''` es un texto vacío. Las pruebas muestran las filas como las escribe Python, que llama `None` al `NULL`.

### Preguntar si falta (*`IS NULL`*, *`IS NOT NULL`*)
Para saber si a una fila le falta un dato, se escribe `x IS NULL`; para saber si lo tiene, `x IS NOT NULL`. Las dos son condiciones, así que van en un `WHERE`, como las del [lab 1.3](../03-filter-rows/README.md):

```sql
SELECT NULL IS NULL, '' IS NULL, 0 IS NULL, 'Lima' IS NOT NULL;
```

| NULL IS NULL | '' IS NULL | 0 IS NULL | 'Lima' IS NOT NULL |
|---|---|---|---|
| 1 | 0 | 0 | 1 |

SQLite muestra una condición verdadera como `1` y una falsa como `0`. El texto vacío y el cero no son `NULL`: son datos.

### Reemplazar lo que falta (*`COALESCE`*)
En un reporte, una celda vacía parece un error. Mejor mostrar «sin dato». **`COALESCE(a, b, …)`** devuelve el primero de sus valores que no es `NULL`:

```sql
SELECT COALESCE(NULL, 'sin dato'), COALESCE('Lima', 'sin dato'), COALESCE(NULL, NULL, 'el tercero');
```

| COALESCE(NULL, 'sin dato') | COALESCE('Lima', 'sin dato') | COALESCE(NULL, NULL, 'el tercero') |
|---|---|---|
| sin dato | Lima | el tercero |

En una consulta, el primer valor suele ser una columna y el último, el valor por defecto: `COALESCE(city, 'sin dato') AS city`.

### Convertir un valor en NULL (*`NULLIF`*)
Algunos sistemas antiguos no guardaban `NULL`: escribían un valor de relleno, como `'-'`, cuando no había dato. Para la base, ese `'-'` es un dato más. **`NULLIF(a, b)`** hace lo contrario de `COALESCE`: devuelve `NULL` si `a` es igual a `b`, y `a` si no lo es:

```sql
SELECT NULLIF('-', '-'), NULLIF('Lima', '-');
```

| NULLIF('-', '-') | NULLIF('Lima', '-') |
|---|---|
| NULL | Lima |

Así el relleno vuelve a ser lo que significaba: un dato que falta.

## 📚 Documentación
- [SQLite: los operadores, entre ellos `IS` e `IS NOT`](https://www.sqlite.org/lang_expr.html#operators_and_parse_affecting_attributes)
- [SQLite: `coalesce`](https://www.sqlite.org/lang_corefunc.html#coalesce) y [`nullif`](https://www.sqlite.org/lang_corefunc.html#nullif)

## 🧭 Escenario
Un gimnasio de Lima pasó a una base de datos las fichas de inscripción de sus socios. Muchas fichas estaban incompletas, y el gimnasio te pide cuatro consultas para ordenar sus datos de contacto y sus cobros.

### Los socios
La tabla `members` tiene una fila por socio.

| Columna | Tipo | Qué guarda |
|---|---|---|
| `id` | `INTEGER` | El número de socio |
| `name` | `TEXT` | Su nombre |
| `district` | `TEXT` | El distrito donde vive, si lo dijo |
| `phone` | `TEXT` | Su teléfono |
| `email` | `TEXT` | Su correo electrónico |
| `monthly_fee` | `INTEGER` | La cuota mensual de su plan, en soles |
| `discount` | `INTEGER` | Los soles que se le descuentan de la cuota, si tiene un descuento |

Estos son todos sus datos:

| id | name | district | phone | email | monthly_fee | discount |
|---|---|---|---|---|---|---|
| 1 | Rosa Mendoza | Miraflores | 900 000 101 | rosa.mendoza@example.com | 120 | 20 |
| 2 | Carlos Vega | Surquillo | `NULL` | carlos.vega@example.com | 120 | `NULL` |
| 3 | Lucía Paredes | `NULL` | 900 000 103 | `''` | 100 | 0 |
| 4 | Miguel Ccori | Miraflores | `NULL` | `NULL` | 100 | `NULL` |
| 5 | Valeria Ríos | Barranco | 900 000 105 | valeria.rios@example.com | 150 | 30 |
| 6 | Diego Salas | `NULL` | `NULL` | diego.salas@example.com | 120 | 10 |
| 7 | Fiorella Chávez | San Isidro | 900 000 107 | `''` | 150 | `NULL` |
| 8 | Renzo Quispe | Miraflores | 900 000 108 | renzo.quispe@example.com | 100 | 15 |
| 9 | Camila Torres | Surquillo | 900 000 109 | `NULL` | 120 | 0 |
| 10 | Andrés Huamán | Barranco | 900 000 110 | andres.huaman@example.com | 150 | `NULL` |

### Tus archivos
```text
starter/
├── queries/               tus cuatro consultas, una por tarea
│   ├── 01_no_phone.sql
│   ├── 02_new_branch.sql
│   ├── 03_amount_to_pay.sql
│   └── 04_contact_list.sql
├── seed.sql               crea la tabla y sus 10 filas
├── tests/
│   ├── conftest.py        prepara la base y compara resultados
│   └── test_queries.py    las pruebas: una clase por tarea
└── pyproject.toml         le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas funcionan igual que en los labs 1.2 y 1.3: cada una arma una base nueva en memoria con [`seed.sql`](starter/seed.sql), corre uno de tus archivos y compara columnas y filas. Si no recuerdas cómo leer un fallo, vuelve a [cómo se revisa tu trabajo](../02-first-queries/README.md#cómo-se-revisa-tu-trabajo) en el lab 1.2. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 4, una por tarea.

### Tarea 1 · Los socios sin teléfono
**Objetivo:** el número y el nombre de los socios que no registraron su teléfono, para pedírselo en la recepción: columnas `id` y `name`. **Lo valida:** [`TestTask1NoPhone`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta, con el `=` de siempre. ¿Qué crees que devuelve: los 3 socios sin teléfono, o ninguno? Escribe tu predicción y después pon la consulta en [`queries/01_no_phone.sql`](starter/queries/01_no_phone.sql):

```sql
SELECT id, name
FROM members
WHERE phone = NULL;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva los socios sin teléfono, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1NoPhone` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 3 fallan.

### Tarea 2 · La nueva sede
**Objetivo:** el gimnasio está en Miraflores y abre una sede nueva en otro distrito. Quiere avisarles a todos los socios que no viven en Miraflores, y también a los que no dijeron su distrito, que pueden vivir en cualquier parte. Columnas `id`, `name` y `district`, con el distrito tal como está guardado. **Lo valida:** [`TestTask2NewBranch`](starter/tests/test_queries.py)

🔮 **Predict first:** ¿crees que esta consulta incluye a Lucía (3) y a Diego (6), que no dijeron su distrito? Escribe tu predicción y después pon la consulta en [`queries/02_new_branch.sql`](starter/queries/02_new_branch.sql):

```sql
SELECT id, name, district
FROM members
WHERE district <> 'Miraflores';
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva todos los socios que pide la tarea, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2NewBranch` pasa. Con todas las pruebas, 3 pasan y 2 fallan.

### Tarea 3 · Lo que paga cada socio
**Objetivo:** lo que paga cada socio al mes: su cuota menos su descuento. Un socio sin descuento paga la cuota completa. Columnas `id`, `name` y `to_pay`, con los 10 socios. **Lo valida:** [`TestTask3AmountToPay`](starter/tests/test_queries.py)

🔮 **Predict first:** ¿qué crees que muestra esta consulta en `to_pay` para Carlos (2), que no tiene descuento? Escribe tu predicción y después pon la consulta en [`queries/03_amount_to_pay.sql`](starter/queries/03_amount_to_pay.sql):

```sql
SELECT id, name, monthly_fee - discount AS to_pay
FROM members;
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva lo que paga cada socio, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3AmountToPay` pasa. Con todas las pruebas, 4 pasan y 1 falla.

### Tarea 4 · La lista de contacto
**Objetivo:** la recepción quiere la lista de correos de todos los socios para su boletín. Donde no hay correo quiere leer `sin correo`. Al pasar las fichas a la base, unos correos que faltaban quedaron como `NULL` y otros como texto vacío (`''`). Columnas `id`, `name` y `email`, con los 10 socios. **Lo valida:** [`TestTask4ContactList`](starter/tests/test_queries.py)

🔮 **Predict first:** esta consulta usa `COALESCE` como en Conceptos. Mirando la tabla de datos, ¿en cuántos socios crees que muestra `sin correo`? Escribe tu predicción y después pon la consulta en [`queries/04_contact_list.sql`](starter/queries/04_contact_list.sql):

```sql
SELECT id, name, COALESCE(email, 'sin correo') AS email
FROM members;
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que muestre `sin correo` en todos los socios sin correo, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask4ContactList` pasa: las 5 pruebas pasan.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `x IS NULL` | Verdadera si a `x` le falta el dato |
| `x IS NOT NULL` | Verdadera si `x` tiene un dato, aunque sea `0` o `''` |
| `COALESCE(a, b, …)` | El primero de sus valores que no es `NULL` |
| `NULLIF(a, b)` | `NULL` si `a` es igual a `b`; si no, `a` |
| `SELECT expresión;` | Sin `FROM`: calcula la expresión una vez, en una sola fila |

## 💼 En proyectos reales
- **Guarda `NULL` cuando no hay dato, no un relleno.** Un `''`, un `0` o un `'N/A'` en lugar de `NULL` obliga a cada consulta a acordarse de él, como en la tarea 4. Si una columna nunca debe quedar vacía, la base puede exigirlo: lo verás en el bloque 3, con las restricciones.
- **`COALESCE` es el estándar.** Muchos motores tienen además una función de dos valores con otro nombre, como `IFNULL` en SQLite y MySQL ([SQLite](https://www.sqlite.org/lang_corefunc.html#ifnull), [MySQL](https://dev.mysql.com/doc/refman/8.4/en/flow-control-functions.html#function_ifnull)). `COALESCE` funciona en todos y acepta más de dos valores.
- **Comparar contando el `NULL` como un valor más.** El SQL estándar tiene `a IS DISTINCT FROM b`: verdadera si los dos son distintos, y un `NULL` cuenta como distinto de cualquier texto. La condición de la tarea 2 se puede escribir `district IS DISTINCT FROM 'Miraflores'`, que funciona en PostgreSQL y en SQLite ([PostgreSQL](https://www.postgresql.org/docs/current/functions-comparison.html)). SQLite acepta además `IS NOT` con cualquier valor (`district IS NOT 'Miraflores'`), y MySQL usa `NOT (a <=> b)` ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/comparison-operators.html#operator_equal-to)). Como cada motor lo escribe distinto, `district <> 'Miraflores' OR district IS NULL` es la forma que funciona en todos.

## 🆘 Pistas
<details><summary>Pista 1 · La consulta no da error, pero no devuelve ninguna fila</summary>

En Conceptos, ¿con qué palabras se pregunta si a una fila le falta un dato? ¿Son las mismas que usa tu consulta?
</details>

<details><summary>Pista 2 · Faltan los socios sin distrito</summary>

La condición tiene que ser verdadera para ellos, y una comparación con un dato que falta no lo es. ¿Qué puedes agregar con `OR` para que los incluya?
</details>

<details><summary>Pista 3 · <code>to_pay</code> sale como <code>None</code></summary>

¿En qué socios pasa? Mira su descuento en la tabla de datos. Si para el cálculo un descuento que falta vale `0`, ¿qué función de Conceptos lo reemplaza?
</details>

<details><summary>Pista 4 · Algunos correos vacíos no salen como <code>sin correo</code></summary>

`COALESCE` solo reemplaza `NULL`. Antes de pasarle el correo, convierte el texto vacío en `NULL`: una función puede ir dentro de otra, como `ROUND(…)` en el lab 1.2.
</details>

## 🎤 Autoevaluación
1. En una entrevista te preguntan qué devuelven `NULL = NULL` y `NULL IS NULL`. ¿Qué respondes, y por qué son distintas?
2. Una tabla de pedidos tiene una columna `status` que a veces es `NULL`. ¿Qué pedidos faltan en el resultado de `WHERE status <> 'cancelado'`, y cómo los incluirías?
3. ¿Qué devuelve `price * quantity` en una fila donde `quantity` es `NULL`? ¿Cómo harías que esa fila cuente como cantidad cero?
4. Sin correr nada: ¿qué valen `NULL AND FALSE` y `NULL OR TRUE`? ¿Por qué no son desconocidas? (Usa la tabla de la tarea 2 en ✔️.)
5. ¿En qué se diferencian `COALESCE` y `NULLIF`? Da un caso para cada una.

<details><summary>Respuestas</summary>

1. `NULL = NULL` es desconocida (SQLite muestra `NULL`), porque comparar dos datos que faltan no dice si son iguales. `NULL IS NULL` es verdadera (`1`): `IS NULL` pregunta si falta el dato, y no compara valores.
2. Faltan los pedidos con `status` en `NULL`, porque la comparación es desconocida para ellos. Para incluirlos: `WHERE status <> 'cancelado' OR status IS NULL`, o `WHERE COALESCE(status, '') <> 'cancelado'`.
3. `NULL`. Con `price * COALESCE(quantity, 0)`, la fila da `0`. Antes de hacerlo, pregúntate si un dato que falta de verdad significa cero en ese negocio.
4. `NULL AND FALSE` es falsa: con un lado falso, el `AND` ya es falso, valga lo que valga el otro. `NULL OR TRUE` es verdadera: con un lado verdadero, el `OR` ya es verdadero.
5. `COALESCE` cambia un `NULL` por un valor (mostrar `sin dato`, contar un descuento que falta como `0`). `NULLIF` cambia un valor por `NULL` (un `''` o un `'-'` que significaba «no hay dato»). Juntas, `COALESCE(NULLIF(x, ''), 'sin dato')` trata igual los dos tipos de hueco.
</details>

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 y 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3). La salida fue la misma en todas las versiones.

### Tarea 1 · Nada es igual a `NULL`
```text
01_no_phone.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 3; obtenidas: 0
  Esperadas que no salieron:
    (2, 'Carlos Vega')
    (4, 'Miguel Ccori')
    (6, 'Diego Salas')
  Obtenidas que no se esperaban:
    (ninguna)
```

Ninguno, y ningún error. `NULL` significa «no sé», así que `phone = NULL` pregunta «¿el teléfono es igual a un valor que no conozco?», y la única respuesta honesta es «no sé». En SQL, una comparación con `NULL` no es verdadera ni falsa: es **desconocida** (*unknown*), y `WHERE` se queda solo con las filas donde la condición es verdadera. Ni siquiera `NULL = NULL` es verdadera: dos datos que faltan no son «iguales». Por eso existe `IS NULL`: `SELECT id, name FROM members WHERE phone IS NULL;`.

### Tarea 2 · `<>` tampoco ve el `NULL`: la lógica de tres valores
```text
02_new_branch.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 7; obtenidas: 5
  Esperadas que no salieron:
    (3, 'Lucía Paredes', None)
    (6, 'Diego Salas', None)
  Obtenidas que no se esperaban:
    (ninguna)
```

Faltan Lucía y Diego. Para ellos, `district <> 'Miraflores'` compara con un dato que falta: el resultado es desconocido, no verdadero, y la fila no sale. Lo mismo pasa con `NOT district = 'Miraflores'`, `NOT LIKE` y `NOT IN`: negar algo desconocido sigue siendo desconocido. Un `NULL` no sale ni con una condición ni con la contraria.

Esto se llama **lógica de tres valores** (*three-valued logic*): en SQL, una condición puede ser verdadera, falsa o desconocida. `AND` y `OR` siguen su sentido común, y lo desconocido solo se resuelve cuando el otro lado basta:

| `A` | `B` | `A AND B` | `A OR B` |
|---|---|---|---|
| desconocida | verdadera | desconocida | **verdadera** |
| desconocida | falsa | **falsa** | desconocida |
| desconocida | desconocida | desconocida | desconocida |

La consulta de la tarea es `SELECT id, name, district FROM members WHERE district <> 'Miraflores' OR district IS NULL;`. Para Lucía, el primer lado es desconocido y el segundo verdadero, así que el `OR` es verdadero (primera fila de la tabla). `COALESCE(district, '') <> 'Miraflores'` también pasa: cambia el dato que falta por un texto vacío antes de comparar. Es una pregunta clásica de entrevista: «¿por qué esta consulta no trae las filas con `NULL`?».

### Tarea 3 · Un cálculo con `NULL` da `NULL`
```text
03_amount_to_pay.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 10; obtenidas: 10
  Esperadas que no salieron:
    (2, 'Carlos Vega', 120)
    (4, 'Miguel Ccori', 100)
    (7, 'Fiorella Chávez', 150)
    (10, 'Andrés Huamán', 150)
  Obtenidas que no se esperaban:
    (2, 'Carlos Vega', None)
    (4, 'Miguel Ccori', None)
    (7, 'Fiorella Chávez', None)
    (10, 'Andrés Huamán', None)
```

`120 - NULL` es `NULL`: si no sabes cuánto restar, no sabes el resultado. Pasa con todas las operaciones (`150 + NULL` y `150 * NULL` también dan `NULL`), y el error es silencioso: en un reporte, los socios sin descuento aparecen sin monto. La tarea dice que un descuento que falta vale `0`, y eso lo escribe `COALESCE`: `SELECT id, name, monthly_fee - COALESCE(discount, 0) AS to_pay FROM members;`.

Fíjate en dónde va el `COALESCE`. `COALESCE(monthly_fee - discount, 0)` llega tarde: la resta ya dio `NULL` y la cambia por `0`, así que Carlos pagaría 0 soles. Lucía y Camila tienen descuento `0`, y con ellas no hay problema: `0` es un dato.

### Tarea 4 · Un texto vacío no es `NULL`
```text
04_contact_list.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 10; obtenidas: 10
  Esperadas que no salieron:
    (3, 'Lucía Paredes', 'sin correo')
    (7, 'Fiorella Chávez', 'sin correo')
  Obtenidas que no se esperaban:
    (3, 'Lucía Paredes', '')
    (7, 'Fiorella Chávez', '')
```

Solo Miguel (4) y Camila (9) muestran `sin correo`; Lucía (3) y Fiorella (7) muestran un texto vacío. `COALESCE` solo reemplaza `NULL`, y `''` es un dato: un texto sin letras. Primero `NULLIF` convierte el texto vacío en `NULL`, y después `COALESCE` reemplaza todos los `NULL`: `SELECT id, name, COALESCE(NULLIF(email, ''), 'sin correo') AS email FROM members;`. El orden importa: `NULLIF(COALESCE(email, ''), '')` deja `NULL` donde faltaba el correo, en vez de `sin correo`.
</details>

La solución completa está en [`solution/`](solution/).
