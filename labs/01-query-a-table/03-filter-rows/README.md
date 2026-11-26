# 🧩 1.3 · Filtrar filas

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Quedarte solo con las filas que cumplen una condición, con `WHERE` y los operadores de comparación.
- Combinar varias condiciones con `AND`, `OR` y `NOT`, y usar paréntesis para decir cuáles van juntas.
- Escribir listas y rangos de valores con `IN` y `BETWEEN`.
- Buscar textos que siguen un patrón con `LIKE`, y saber cuándo distingue mayúsculas de minúsculas.
- Reconocer los filtros que devuelven filas de más o de menos sin dar ningún error, una trampa típica de las entrevistas.

## 💡 Por qué importa
En el lab 1.2 elegiste qué columnas mostrar, pero siempre de todas las filas. Un reporte casi nunca quiere todas: quiere los pedidos de esta semana, los clientes de una ciudad o los productos sin stock. Filtrar bien es lo que más vas a escribir en SQL, y un filtro mal escrito no avisa: devuelve otras filas y parece correcto.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/01-query-a-table/03-filter-rows/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Como en el lab 1.2, los ejemplos usan la tabla `jobs` de la bolsa de trabajo del [lab 1.1](../01-first-database/README.md). Esta vez se muestran todas las filas de cada resultado.

### Quedarte con algunas filas (*`WHERE` clause*)
Quieres ver solo las ofertas de Lima. Después del `FROM`, escribe `WHERE` y una **condición** (*condition*): una comparación que, para cada fila, es verdadera o falsa. El resultado tiene solo las filas donde es verdadera.

```sql
SELECT title, salary_usd
FROM jobs
WHERE city = 'Lima';
```

| title | salary_usd |
|---|---|
| Analista de datos júnior | 1200 |
| Analista de BI | 1500 |
| Analista de calidad (QA) | 1100 |

La parte `WHERE …` se llama **cláusula `WHERE`** (*`WHERE` clause*): una cláusula es cada parte de una consulta que empieza con su palabra clave, como `SELECT`, `FROM` o `WHERE`. La condición puede usar cualquier columna de la tabla, aunque no esté en la lista del `SELECT` (aquí, `city`). Los textos van entre comillas simples, como viste en el lab 1.2, y los números sin comillas. Estos son los **operadores de comparación** (*comparison operators*):

| Operador | Significa | Ejemplo |
|---|---|---|
| `=` | igual a | `city = 'Lima'` |
| `<>` o `!=` | distinto de | `city <> 'Lima'` |
| `<` · `<=` | menor que · menor o igual que | `salary_usd < 1000` |
| `>` · `>=` | mayor que · mayor o igual que | `salary_usd >= 1500` |

### Combinar condiciones (*`AND`, `OR`, `NOT`*)
Un filtro real suele tener más de una condición: ofertas de Lima *y* remotas, o de Bogotá *o* de Santiago. Las palabras `AND`, `OR` y `NOT` unen condiciones en una sola:

```sql
SELECT title, city, mode
FROM jobs
WHERE city = 'Lima' AND mode = 'remoto';
```

| title | city | mode |
|---|---|---|
| Analista de calidad (QA) | Lima | remoto |

- `A AND B` es verdadera cuando **las dos** lo son: la única oferta de Lima que además es remota.
- `A OR B` es verdadera cuando **al menos una** lo es: `city = 'Bogotá' OR city = 'Santiago'` devuelve las dos ofertas de esas ciudades.
- `NOT A` invierte la condición: `NOT mode = 'presencial'` devuelve las 5 ofertas híbridas o remotas.

Se llaman **operadores lógicos** (*logical operators*). Como en la aritmética del lab 1.2, los paréntesis agrupan: `(A OR B) AND C` primero resuelve lo que está adentro. Cuando mezcles `AND` y `OR`, usa paréntesis para dejar claro qué va junto.

### Una lista o un rango (*`IN`, `BETWEEN`*)
Escribir `city = 'Bogotá' OR city = 'Santiago' OR city = 'Arequipa'` es largo. `IN` compara con una lista de valores, entre paréntesis y separados por comas:

```sql
SELECT title, city
FROM jobs
WHERE city IN ('Bogotá', 'Santiago', 'Arequipa');
```

| title | city |
|---|---|
| Desarrollador backend | Bogotá |
| Soporte de TI | Arequipa |
| Administrador de bases de datos | Santiago |

Para un rango de números, `BETWEEN a AND b` es lo mismo que `>= a AND <= b`: los dos extremos entran.

```sql
SELECT title, salary_usd
FROM jobs
WHERE salary_usd BETWEEN 1500 AND 2000;
```

| title | salary_usd |
|---|---|
| Desarrollador backend | 1800 |
| Analista de BI | 1500 |
| Desarrolladora full stack | 2000 |

Los dos se pueden negar: `city NOT IN ('Lima', 'Bogotá')`, `salary_usd NOT BETWEEN 1500 AND 2000`.

### Buscar por un patrón (*`LIKE`*)
A veces no sabes el texto exacto: quieres todas las ofertas de analista, se llamen como se llamen. `LIKE` compara un texto con un **patrón** (*pattern*), un texto con **comodines** (*wildcards*) que reemplazan partes:

| Comodín | Reemplaza a | Ejemplo | Encuentra en `jobs` |
|---|---|---|---|
| `%` | cualquier cantidad de caracteres, incluso ninguno | `title LIKE 'Analista%'` | Analista de datos júnior, Analista de BI, Analista de calidad (QA) |
| `%` a los dos lados | el texto puede estar en cualquier parte | `title LIKE '%datos%'` | Analista de datos júnior, Practicante de datos, Administrador de bases de datos |
| `_` | exactamente un carácter | `title LIKE 'Analista de __'` | Analista de BI |

Sin comodines, `LIKE` compara el texto completo. `NOT LIKE` devuelve las filas que no siguen el patrón.

## 📚 Documentación
- [SQLite: la cláusula `WHERE`](https://www.sqlite.org/lang_select.html#where_clause_filtering_)
- [SQLite: los operadores y su orden](https://www.sqlite.org/lang_expr.html#operators_and_parse_affecting_attributes)
- [SQLite: `BETWEEN`](https://www.sqlite.org/lang_expr.html#the_between_operator)
- [SQLite: `LIKE`](https://www.sqlite.org/lang_expr.html#the_like_glob_regexp_match_and_extract_operators)

## 🧭 Escenario
Una inmobiliaria de Lima publica en su web departamentos en alquiler y te pide cinco consultas para su buscador y sus reportes.

### Los anuncios
La tabla `apartments` tiene una fila por departamento en alquiler.

| Columna | Tipo | Qué guarda |
|---|---|---|
| `id` | `INTEGER` | El número del anuncio |
| `district` | `TEXT` | El distrito de Lima donde está |
| `title` | `TEXT` | El título del anuncio |
| `rent` | `INTEGER` | El alquiler mensual, en soles |

Estos son todos sus datos:

| id | district | title | rent |
|---|---|---|---|
| 1 | Miraflores | Departamento con vista al mar | 2600 |
| 2 | Miraflores | Cochera y depósito incluidos | 1800 |
| 3 | Miraflores | A dos cuadras del parque Kennedy | 1500 |
| 4 | Barranco | Loft con terraza | 2000 |
| 5 | Barranco | Cerca al malecón, con cochera | 1750 |
| 6 | San Isidro | Con cochera para dos autos | 3100 |
| 7 | San Isidro | Frente al centro financiero | 2200 |
| 8 | San Borja | Amplio y con cochera techada | 1900 |
| 9 | San Miguel | Cerca a la universidad | 1200 |
| 10 | Santiago de Surco | Casa con jardín | 2400 |
| 11 | Santiago de Surco | Condominio con piscina | 1650 |
| 12 | Jesús María | Frente al Campo de Marte | 1350 |
| 13 | Lince | Minidepartamento amoblado | 1100 |
| 14 | Pueblo Libre | Primer piso, con patio | 1250 |

### Tus archivos
```text
starter/
├── queries/               tus cinco consultas, una por tarea
│   ├── 01_miraflores.sql
│   ├── 02_rent_range.sql
│   ├── 03_two_districts.sql
│   ├── 04_parking.sql
│   └── 05_other_branch.sql
├── seed.sql               crea la tabla y sus 14 filas
├── tests/
│   ├── conftest.py        prepara la base y compara resultados
│   └── test_queries.py    las pruebas: una clase por tarea
└── pyproject.toml         le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas funcionan igual que en el lab 1.2: cada una arma una base nueva en memoria con [`seed.sql`](starter/seed.sql), corre uno de tus archivos y compara columnas y filas. Si no recuerdas cómo leer un fallo, vuelve a [cómo se revisa tu trabajo](../02-first-queries/README.md#cómo-se-revisa-tu-trabajo) en el lab 1.2. [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 5, una por tarea.

### Tarea 1 · Los departamentos de Miraflores
**Objetivo:** el número, el título y el alquiler de los departamentos de Miraflores: columnas `id`, `title` y `rent`. **Lo valida:** [`TestTask1Miraflores`](starter/tests/test_queries.py)

🔮 **Predict first:** en el buscador de la web, la gente escribe el distrito como le sale, por ejemplo en minúsculas. ¿Qué crees que devuelve esta consulta: los 3 departamentos de Miraflores, o ninguno? Escribe tu predicción y después pon la consulta en [`queries/01_miraflores.sql`](starter/queries/01_miraflores.sql):

```sql
SELECT id, title, rent
FROM apartments
WHERE district = 'miraflores';
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Deja en el archivo una consulta que devuelva los departamentos de Miraflores, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1Miraflores` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 4 fallan.

### Tarea 2 · Un rango de precios
**Objetivo:** los departamentos con un alquiler desde 1200 hasta 1800 soles, los dos incluidos: columnas `id`, `district` y `rent`. **Lo valida:** [`TestTask2RentRange`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió los dos números de `BETWEEN` al revés, el mayor primero. ¿Da lo mismo? Escribe tu predicción y después pon su consulta en [`queries/02_rent_range.sql`](starter/queries/02_rent_range.sql):

```sql
SELECT id, district, rent
FROM apartments
WHERE rent BETWEEN 1800 AND 1200;
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Deja en el archivo una consulta que devuelva el rango que pide la tarea, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2RentRange` pasa. Con todas las pruebas, 3 pasan y 3 fallan.

### Tarea 3 · Dos distritos y un tope
**Objetivo:** los departamentos de Miraflores o de Barranco que cuestan menos de 2000 soles: columnas `id`, `district` y `rent`. **Lo valida:** [`TestTask3TwoDistricts`](starter/tests/test_queries.py)

🔮 **Predict first:** esta consulta dice, palabra por palabra, lo que pide la tarea. Mirando la tabla de datos, anota qué filas crees que devuelve. Después ponla en [`queries/03_two_districts.sql`](starter/queries/03_two_districts.sql):

```sql
SELECT id, district, rent
FROM apartments
WHERE district = 'Miraflores' OR district = 'Barranco' AND rent < 2000;
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con las filas que anotaste.
- [ ] Deja en el archivo una consulta que devuelva lo que pide la tarea, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.
- [ ] En esa misma consulta, cambia las dos comparaciones del distrito por un solo `IN`, y comprueba que la prueba sigue pasando.

**Criterio de éxito:** `TestTask3TwoDistricts` pasa. Con todas las pruebas, 4 pasan y 2 fallan.

### Tarea 4 · Buscar en el anuncio
**Objetivo:** los anuncios cuyo título menciona una cochera, en cualquier parte del título y con mayúscula o sin ella: columnas `id`, `district` y `title`. **Lo valida:** [`TestTask4Parking`](starter/tests/test_queries.py)

🔮 **Predict first:** en la tarea 1, `=` comparó `'miraflores'` con `'Miraflores'`. Esta consulta busca `cochera` en minúsculas. ¿Crees que encuentra el anuncio 2, «Cochera y depósito incluidos», que empieza con mayúscula? Escribe tu predicción y después pon la consulta en [`queries/04_parking.sql`](starter/queries/04_parking.sql):

```sql
SELECT id, district, title
FROM apartments
WHERE title LIKE '%cochera%';
```

- [ ] Corre `python -m pytest -k task4`. La prueba espera 4 anuncios, entre ellos el 2: si pasa, `LIKE` lo encontró. Compáralo con tu predicción.
- [ ] Cambia el patrón por `'cochera%'` y vuelve a correr `python -m pytest -k task4`. ¿Qué anuncios faltan ahora, y por qué esos?
- [ ] Vuelve al patrón `'%cochera%'` y comprueba que la prueba pasa otra vez.

**Criterio de éxito:** `TestTask4Parking` pasa. Con todas las pruebas, 5 pasan y 1 falla.

### Tarea 5 · La otra sucursal
**Objetivo:** la inmobiliaria tiene dos sucursales. La de San Isidro atiende los distritos cuyo nombre empieza con la palabra «San»; la otra, todos los demás. Te piden los departamentos de la otra sucursal: columnas `id` y `district`. **Lo valida:** [`TestTask5OtherBranch`](starter/tests/test_queries.py)

🔮 **Predict first:** ¿qué distritos crees que quita esta consulta? Revisa la tabla de datos, anota cuántas filas esperas y después pon la consulta en [`queries/05_other_branch.sql`](starter/queries/05_other_branch.sql):

```sql
SELECT id, district
FROM apartments
WHERE district NOT LIKE 'San%';
```

- [ ] Corre `python -m pytest -k task5` y compara lo que muestra con tu predicción.
- [ ] Deja en el archivo una consulta que siga la regla de la sucursal (cambia solo el patrón, si hace falta), y vuelve a correr `python -m pytest -k task5` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask5OtherBranch` pasa: las 6 pruebas pasan.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `SELECT … FROM t WHERE <condición>;` | Devuelve solo las filas de `t` donde la condición es verdadera |
| `A AND B` | Verdadera si las dos lo son |
| `A OR B` | Verdadera si al menos una lo es |
| `NOT A` | Verdadera si `A` es falsa |
| `( … )` | Agrupa condiciones: se resuelve primero lo que está adentro |
| `x IN (a, b, c)` | Verdadera si `x` es igual a alguno de los valores de la lista |
| `x BETWEEN a AND b` | Lo mismo que `x >= a AND x <= b` |
| `x LIKE 'patrón'` | Verdadera si el texto sigue el patrón: `%` es cualquier cantidad de caracteres, `_` es uno |
| `NOT IN` · `NOT BETWEEN` · `NOT LIKE` | Lo contrario de cada uno |

## 💼 En proyectos reales
- **Un alias en `WHERE` funciona en SQLite, pero no en PostgreSQL ni en MySQL.** En el lab 1.2 viste que un alias no existe dentro de su propio `SELECT`. En SQLite sí puedes usarlo en el `WHERE`: `SELECT title, salary_usd * 12 AS annual_salary_usd FROM jobs WHERE annual_salary_usd > 20000;` devuelve las 3 ofertas que pagan más de 20 000 dólares al año. El SQL estándar no lo permite, porque el motor filtra las filas (`WHERE`) antes de calcular las columnas del resultado (`SELECT`), y PostgreSQL y MySQL no lo aceptan ([PostgreSQL](https://www.postgresql.org/docs/current/sql-select.html#SQL-SELECT-LIST), [MySQL](https://dev.mysql.com/doc/refman/8.4/en/problems-with-alias.html)). Para que tu consulta funcione en cualquier motor, repite el cálculo: `WHERE salary_usd * 12 > 20000`.
- **Prueba los bordes de cada filtro.** Antes de entregar un reporte, prueba su filtro con los casos que lo pueden romper: el valor justo en el límite, un texto con otra mayúscula, un nombre que empieza igual que otro. Los datos de este lab traen uno de cada uno, y por eso las pruebas encuentran esos errores.
- **Un buscador real normaliza el texto antes de comparar.** La gente escribe «miraflores», «MIRAFLORES» o «Miraflores» con un espacio de más al final. En vez de depender de cómo compara `=` o `LIKE` cada motor, se suele comparar el texto ya pasado a minúsculas y sin espacios de sobra, con funciones que verás en el lab 1.6.

## 🆘 Pistas
<details><summary>Pista 1 · La consulta no da error, pero no devuelve ninguna fila</summary>

Lee la condición en voz alta y pregúntate si alguna fila de la tabla la cumple tal como está escrita: letra por letra, y número por número.
</details>

<details><summary>Pista 2 · Sobran filas al mezclar <code>AND</code> y <code>OR</code></summary>

Mira las filas que sobran. ¿Cumplen la condición del precio? Si no, el motor no unió las condiciones como tú pensabas: ponle paréntesis a las dos condiciones del distrito.
</details>

<details><summary>Pista 3 · <code>near ","</code>: syntax error con <code>IN</code></summary>

Como viste en el lab 1.2, el problema está justo antes de lo que aparece en `near`. Compara tu `IN` con el ejemplo de Conceptos: ¿qué rodea a la lista de valores?
</details>

<details><summary>Pista 4 · El patrón atrapa de más</summary>

`%` acepta cualquier cosa, incluso letras pegadas a las que escribiste. ¿Qué hay justo después de la palabra «San» en «San Isidro», y qué hay en «Santiago»?

Ojo: `_` no es un espacio. Es exactamente un carácter cualquiera, también una letra, así que `'San_%'` atrapa lo mismo que `'San%'`. Un espacio dentro del patrón es un espacio.
</details>

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1 y Git Bash, con Python 3.12.16, 3.13.14, 3.13.18, 3.14.4 y 3.15.2 (SQLite 3.50.4 y 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3). La salida fue la misma en todas las versiones.

### Tarea 1 · `=` distingue mayúsculas de minúsculas
```text
01_miraflores.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 3; obtenidas: 0
  Esperadas que no salieron:
    (1, 'Departamento con vista al mar', 2600)
    (2, 'Cochera y depósito incluidos', 1800)
    (3, 'A dos cuadras del parque Kennedy', 1500)
  Obtenidas que no se esperaban:
    (ninguna)
```

Ningún departamento y ningún error. **`=` compara los textos carácter por carácter**, y `m` no es lo mismo que `M`: ninguna fila dice `miraflores`, así que la condición es falsa en todas. Es una trampa silenciosa, porque una consulta sin resultados parece una respuesta válida («no hay departamentos»). La consulta de la tarea es `SELECT id, title, rent FROM apartments WHERE district = 'Miraflores';`.

PostgreSQL también distingue mayúsculas con `=` (su documentación muestra cómo [comparar sin distinguirlas](https://www.postgresql.org/docs/current/citext.html#CITEXT-RATIONALE)). MySQL no, por defecto: compara los textos con una *collation* (las reglas con que el motor compara textos) que ignora mayúsculas ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/case-sensitivity.html)). Si escribiste `"Miraflores"` con comillas dobles y la prueba pasó, es la rareza de SQLite del lab 1.2: como no hay una columna con ese nombre, lo toma como texto. En PostgreSQL, como en el SQL estándar, las comillas dobles siempre encierran un nombre ([PostgreSQL](https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS)), así que esa consulta busca una columna `Miraflores` y da error.

### Tarea 2 · `BETWEEN` necesita primero el menor
```text
02_rent_range.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 7; obtenidas: 0
  Esperadas que no salieron:
    (2, 'Miraflores', 1800)
    (3, 'Miraflores', 1500)
    (5, 'Barranco', 1750)
    (9, 'San Miguel', 1200)
    (11, 'Santiago de Surco', 1650)
    (12, 'Jesús María', 1350)
    (14, 'Pueblo Libre', 1250)
  Obtenidas que no se esperaban:
    (ninguna)
```

No da lo mismo. `rent BETWEEN 1800 AND 1200` es `rent >= 1800 AND rent <= 1200`, y ningún número es a la vez mayor que 1800 y menor que 1200: cero filas, sin error. La consulta de la tarea es `SELECT id, district, rent FROM apartments WHERE rent BETWEEN 1200 AND 1800;`. Fíjate en que salen San Miguel (1200) y el departamento 2 de Miraflores (1800): `BETWEEN` incluye los extremos. Con `rent > 1200 AND rent < 1800` faltarían esos dos.

### Tarea 3 · `AND` se resuelve antes que `OR`
```text
03_two_districts.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 3; obtenidas: 4
  Esperadas que no salieron:
    (ninguna)
  Obtenidas que no se esperaban:
    (1, 'Miraflores', 2600)
```

Sobra el departamento de 2600 soles. **`AND` se resuelve antes que `OR`**, igual que `*` antes que `+`, así que el motor leyó la consulta así:

```sql
WHERE district = 'Miraflores' OR (district = 'Barranco' AND rent < 2000)
```

El tope de precio quedó pegado solo a Barranco, y de Miraflores salen todos. Con paréntesis dices qué va junto: `WHERE (district = 'Miraflores' OR district = 'Barranco') AND rent < 2000`. Con `IN` ya no hay dos condiciones que agrupar, y se lee mejor: `WHERE district IN ('Miraflores', 'Barranco') AND rent < 2000`. Es una pregunta clásica de entrevista: ante la duda, paréntesis.

Otra forma de equivocarse sin error: `WHERE district = 'Miraflores' OR 'Barranco'`. SQLite toma el texto `'Barranco'` solo, sin comparación, como una condición falsa, y devuelve únicamente Miraflores. Cada lado de un `OR` necesita su comparación completa.

### Tarea 4 · En SQLite, `LIKE` ignora mayúsculas (solo sin tildes)
La consulta pasa: `LIKE` encontró «Cochera y depósito incluidos». **En SQLite, `LIKE` no distingue mayúsculas de minúsculas, y `=` sí.** La excepción son las letras con tilde y la ñ: `LIKE` solo iguala mayúsculas y minúsculas de las letras sin tilde (las del alfabeto inglés), así que `'Ático' LIKE 'ático'` es falso (`0`) ([SQLite](https://www.sqlite.org/lang_expr.html#the_like_glob_regexp_match_and_extract_operators)). Cada motor lo hace a su manera: en PostgreSQL, `LIKE` sí distingue mayúsculas, y para ignorarlas existe `ILIKE`, que no es estándar ([PostgreSQL](https://www.postgresql.org/docs/current/functions-matching.html#FUNCTIONS-LIKE)); en MySQL depende de la *collation*, como `=`.

Con el patrón `'cochera%'`:

```text
04_parking.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 4; obtenidas: 1
  Esperadas que no salieron:
    (5, 'Barranco', 'Cerca al malecón, con cochera')
    (6, 'San Isidro', 'Con cochera para dos autos')
    (8, 'San Borja', 'Amplio y con cochera techada')
  Obtenidas que no se esperaban:
    (ninguna)
```

Sin `%` al comienzo, el título tiene que *empezar* con «cochera»: solo queda el anuncio 2. Para buscar en cualquier parte, el `%` va a los dos lados.

### Tarea 5 · `%` también atrapa letras pegadas
```text
05_other_branch.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 10; obtenidas: 8
  Esperadas que no salieron:
    (10, 'Santiago de Surco')
    (11, 'Santiago de Surco')
  Obtenidas que no se esperaban:
    (ninguna)
```

Faltan los dos de Santiago de Surco. `'San%'` significa «empieza con las letras S, a, n», y **Santiago también empieza con esas letras**: el patrón no sabe dónde termina una palabra. La palabra «San» va seguida de un espacio, así que el patrón correcto lo incluye: `SELECT id, district FROM apartments WHERE district NOT LIKE 'San %';`.

`district NOT IN ('San Isidro', 'San Borja', 'San Miguel')` también pasa la prueba, pero no sigue la regla de la sucursal: si mañana llega un anuncio en San Juan de Miraflores, la lista no lo quita y el patrón sí.
</details>

## 🎤 Autoevaluación
1. Una consulta para un reporte devuelve cero filas y ningún error. ¿Qué revisarías antes de concluir que no hay datos?
2. En una entrevista te muestran `WHERE category = 'libros' OR category = 'música' AND price > 50`. ¿Qué filas devuelve, y cómo la escribirías si se pedían los libros y la música de más de 50?
3. ¿Qué devuelve `WHERE age BETWEEN 18 AND 25` para alguien de 18 y para alguien de 25? ¿Y `WHERE age BETWEEN 25 AND 18`?
4. Tu consulta usa `WHERE name LIKE 'ana%'` y en SQLite encuentra a «Ana Quispe». Tu equipo la pasa a PostgreSQL. ¿Qué cambia, y cómo lo resolverías?
5. Te piden los códigos de producto que tienen exactamente cuatro caracteres y empiezan con `A`. ¿Qué patrón usas, y por qué `'A%'` no sirve?

<details><summary>Respuestas</summary>

1. Que la condición coincida con los datos tal como están guardados: mayúsculas y minúsculas, espacios, el orden de los números de un `BETWEEN`. Cero filas puede ser la respuesta correcta, pero también es el síntoma de casi todos los filtros mal escritos.
2. Todos los libros, de cualquier precio, más la música de más de 50: `AND` se resuelve antes que `OR`. Para lo pedido: `WHERE category IN ('libros', 'música') AND price > 50`, o con paréntesis alrededor de las dos condiciones de la categoría.
3. Las dos personas entran: `BETWEEN` incluye los extremos (`age >= 18 AND age <= 25`). Al revés no entra nadie, porque ninguna edad es a la vez mayor o igual que 25 y menor o igual que 18.
4. En PostgreSQL, `LIKE` distingue mayúsculas, así que `'ana%'` ya no encuentra «Ana». Se puede usar `ILIKE`, que es solo de PostgreSQL, o comparar los dos textos pasados a minúsculas, que funciona en cualquier motor.
5. `'A___'`: una `A` y tres `_`, cada uno exactamente un carácter. `'A%'` acepta cualquier cantidad de caracteres después de la `A`, así que también trae `A1` o `A12345`. En SQLite, `'A___'` también trae `abcd`, porque `LIKE` ignora mayúsculas (tarea 4); si el código tiene que empezar con `A` mayúscula, esa diferencia importa.
</details>

La solución completa está en [`solution/`](solution/).

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?
