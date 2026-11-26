# 🧩 1.5 · Ordenar y paginar

| ⏱️ Duración | 🧪 Tipo | 🏷️ Tipo de tema | 🛠️ Stack |
|---|---|---|---|
| 1–2 h | 🧩 `challenge` | 🎯 `core` | Python 3.12+ · `sqlite3` (SQLite 3.45+) · pytest 9.2.0 |

## 🎯 Objetivos
- Ordenar un resultado por una o varias columnas, de menor a mayor o de mayor a menor, y decidir qué pasa cuando dos filas empatan.
- Decidir dónde quedan los `NULL` al ordenar.
- Quitar las filas repetidas de un resultado con `DISTINCT`.
- Sacar los primeros N resultados y mostrarlos por páginas con `LIMIT` y `OFFSET`.
- Responder las preguntas de entrevista sobre el orden de un resultado y los empates en un top N.

## 💡 Por qué importa
Casi todo lo que muestra una aplicación está ordenado y partido en páginas: los productos del más barato al más caro, los 10 más vendidos, la página 3 de los resultados de una búsqueda. Si la consulta no fija el orden, la base no promete ninguno, y una página puede repetir o saltarse filas sin dar ningún error.

## 📍 Dónde correr los comandos
Con el entorno virtual activo, entra a la carpeta `starter/` de este lab. Todos los comandos del lab se corren desde ahí.

PowerShell o Bash, desde la raíz del repositorio:

```bash
cd labs/01-query-a-table/05-sort-and-paginate/starter
```

Si la salida de `python -m pytest` tiene una línea que empieza con `plugins:`, o termina con algo como `3 warnings`, no estás usando el Python del entorno, aunque el prompt diga `(.venv)`: sigue el [paso 3 de SETUP.md](../../../SETUP.md#3-comprueba-todo).

## 🧠 Conceptos
Los ejemplos usan la tabla `jobs` del [lab 1.1](../01-first-database/README.md). No hace falta correrlos; si quieres probarlos, abre su base con la consola de ese lab.

### Ordenar (*ORDER BY*)
Una tabla no tiene un orden propio: si la consulta no pide uno, la base devuelve las filas como le resulte más cómodo, aunque a veces parezca el orden en que se guardaron, y no promete que mañana salgan igual. Para fijar el orden, la consulta termina con **`ORDER BY`** y la columna que manda. `ASC` ordena de menor a mayor (los textos, de la A a la Z) y es lo que pasa si no escribes nada; `DESC` ordena de mayor a menor:

```sql
SELECT title, salary_usd
FROM jobs
ORDER BY salary_usd DESC;
```

| title | salary_usd |
|---|---|
| Administrador de bases de datos | 2400 |
| Desarrolladora full stack | 2000 |
| Desarrollador backend | 1800 |
| Analista de BI | 1500 |
| Analista de datos júnior | 1200 |
| Analista de calidad (QA) | 1100 |
| Soporte de TI | 800 |
| Practicante de datos | 600 |

Puedes ordenar por varias columnas, separadas por comas. La base ordena por la primera y solo mira la segunda cuando dos filas empatan en la primera:

```sql
SELECT company, title, salary_usd
FROM jobs
ORDER BY company, salary_usd;
```

| company | title | salary_usd |
|---|---|---|
| Agro Norte | Practicante de datos | 600 |
| Andes Retail | Analista de datos júnior | 1200 |
| Andes Retail | Analista de BI | 1500 |
| Banco Sur | Administrador de bases de datos | 2400 |
| Clínica Central | Soporte de TI | 800 |
| Clínica Central | Analista de calidad (QA) | 1100 |
| Pago Fácil | Desarrollador backend | 1800 |
| Pago Fácil | Desarrolladora full stack | 2000 |

Las empresas van de la A a la Z, y dentro de cada empresa, los sueldos de menor a mayor.

### Dónde quedan los NULL (*NULLS FIRST*, *NULLS LAST*)
Al ordenar una columna que tiene `NULL` (el dato que falta, del [lab 1.4](../04-null-values/README.md)), todos los `NULL` quedan juntos, al comienzo o al final. Si te importa dónde, dilo justo después de la columna: `ORDER BY discount NULLS LAST` los deja al final y `ORDER BY discount NULLS FIRST`, al comienzo.

### Quitar repetidos (*DISTINCT*)
¿Qué empresas publicaron ofertas? `SELECT company FROM jobs` devuelve 8 filas, una por oferta, con empresas repetidas. **`DISTINCT`**, justo después de `SELECT`, deja una sola copia de cada fila repetida:

```sql
SELECT DISTINCT company
FROM jobs
ORDER BY company;
```

| company |
|---|
| Agro Norte |
| Andes Retail |
| Banco Sur |
| Clínica Central |
| Pago Fácil |

### Los primeros y los siguientes (*LIMIT*, *OFFSET*)
Para un top 3 no quieres todo el resultado, solo sus primeras filas. **`LIMIT n`**, al final de la consulta, devuelve como mucho `n` filas:

```sql
SELECT title, salary_usd
FROM jobs
ORDER BY salary_usd DESC
LIMIT 3;
```

| title | salary_usd |
|---|---|
| Administrador de bases de datos | 2400 |
| Desarrolladora full stack | 2000 |
| Desarrollador backend | 1800 |

Una web que muestra los resultados de 3 en 3 necesita también los siguientes. **`OFFSET n`** salta las primeras `n` filas: `LIMIT 3 OFFSET 3` salta 3 y devuelve las 3 siguientes, la segunda página.

| title | salary_usd |
|---|---|
| Analista de BI | 1500 |
| Analista de datos júnior | 1200 |
| Analista de calidad (QA) | 1100 |

Mostrar un resultado por partes así se llama **paginar** (*pagination*).

## 📚 Documentación
- [SQLite: `ORDER BY`](https://www.sqlite.org/lang_select.html#orderby), con [`NULLS FIRST` y `NULLS LAST`](https://www.sqlite.org/lang_select.html#nullslast)
- [SQLite: `LIMIT` y `OFFSET`](https://www.sqlite.org/lang_select.html#limitoffset)
- [SQLite: `DISTINCT`](https://www.sqlite.org/lang_select.html#distinct)

## 🧭 Escenario
Una plataforma de cursos en línea quiere ordenar su catálogo de varias formas para su web: los más populares, los que hay que revisar, el menú de categorías, la portada y las páginas del listado. Te pide cinco consultas.

### Los cursos
La tabla `courses` tiene una fila por curso.

| Columna | Tipo | Qué guarda |
|---|---|---|
| `id` | `INTEGER` | El número del curso |
| `title` | `TEXT` | Su título |
| `category` | `TEXT` | Su categoría |
| `level` | `TEXT` | Su nivel: `básico`, `intermedio` o `avanzado` |
| `price` | `INTEGER` | Su precio, en soles |
| `year` | `INTEGER` | El año en que se publicó |
| `students` | `INTEGER` | Cuántas personas lo compraron |
| `rating` | `REAL` | El promedio de sus reseñas, de 1 a 5; `NULL` si todavía no tiene reseñas |

Estos son todos sus datos, en el orden en que se guardaron:

| id | title | category | level | price | year | students | rating |
|---|---|---|---|---|---|---|---|
| 1 | SQL desde cero | Datos | básico | 49 | 2023 | 1250 | 4.8 |
| 2 | JavaScript moderno | Programación | intermedio | 69 | 2024 | 760 | 4.6 |
| 3 | Excel avanzado | Negocios | avanzado | 39 | 2024 | 1250 | 4.5 |
| 4 | Figma para principiantes | Diseño | básico | 49 | 2025 | 430 | 4.2 |
| 5 | Python para análisis de datos | Datos | intermedio | 89 | 2023 | 980 | 4.6 |
| 6 | Power BI en la práctica | Datos | intermedio | 69 | 2026 | 120 | `NULL` |
| 7 | Git y GitHub | Programación | básico | 29 | 2023 | 1530 | 4.9 |
| 8 | Finanzas personales | Negocios | básico | 29 | 2026 | 85 | `NULL` |
| 9 | Diseño de logos | Diseño | intermedio | 59 | 2024 | 310 | 3.9 |
| 10 | Django para la web | Programación | avanzado | 99 | 2025 | 540 | 4.4 |
| 11 | Estadística para no estadísticos | Datos | básico | 59 | 2026 | 210 | `NULL` |
| 12 | Marketing digital | Negocios | intermedio | 49 | 2025 | 760 | 4.1 |

### Tus archivos
```text
starter/
├── queries/               tus cinco consultas, una por tarea
│   ├── 01_most_popular.sql
│   ├── 02_to_review.sql
│   ├── 03_categories.sql
│   ├── 04_top_rated.sql
│   └── 05_second_page.sql
├── seed.sql               crea la tabla y sus 12 filas
├── tests/
│   ├── conftest.py        prepara la base y compara resultados
│   └── test_queries.py    las pruebas: una clase por tarea
└── pyproject.toml         le dice a pytest dónde están las pruebas
```

Solo cambias los archivos de [`queries/`](starter/queries/), con **una sola** consulta cada uno. Las pruebas arman la base y comparan columnas y filas como en los labs anteriores (repásalo en [cómo se revisa tu trabajo](../02-first-queries/README.md#cómo-se-revisa-tu-trabajo), en el lab 1.2). [`TestSeed`](starter/tests/test_queries.py) es la prueba de guarda: pasa desde el comienzo.

### Ahora también importa el orden
Cada tarea pide un orden completo, que dice también qué hacer cuando dos filas empatan. Las pruebas lo revisan en dos pasos:
1. Comparan las filas sin mirar el orden, como siempre. Si sobran o faltan filas, ves el mensaje de siempre, `las columnas están bien, pero las filas no coinciden (el orden de las filas no importa)`: en este paso el orden todavía no cuenta.
2. Si las filas son las correctas, revisan el orden. Si no es el pedido, el mensaje empieza con `las filas son las correctas, pero no están en el orden pedido`, dice cuál es la primera fila fuera de lugar y muestra numerados el orden esperado y el tuyo.

## ✅ Tareas

Corre todas las pruebas con este comando, desde `starter/`:

PowerShell o Bash:

```bash
python -m pytest
```

Córrelo ahora, antes de escribir nada: pasa 1 prueba y fallan 5, una por tarea.

### Tarea 1 · Los más populares
**Objetivo:** los cursos del que tiene más alumnos al que tiene menos. Si dos tienen los mismos alumnos, primero el más nuevo (el de `year` más alto). Columnas `title`, `students` y `year`, con los 12 cursos. **Lo valida:** [`TestTask1MostPopular`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta, con un `DESC` al final. ¿Crees que el primer curso del resultado es el que tiene más alumnos? Escribe tu predicción y después pon la consulta en [`queries/01_most_popular.sql`](starter/queries/01_most_popular.sql):

```sql
SELECT title, students, year
FROM courses
ORDER BY students, year DESC;
```

- [ ] Corre `python -m pytest -k task1` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva los cursos en el orden que pide la tarea, y vuelve a correr `python -m pytest -k task1` hasta que la prueba pase.

**Criterio de éxito:** `TestTask1MostPopular` pasa. Con todas las pruebas (`python -m pytest`), 2 pasan y 4 fallan.

### Tarea 2 · Los cursos que hay que revisar
**Objetivo:** el equipo de calidad revisa primero los cursos peor calificados: del `rating` más bajo al más alto. Si dos tienen la misma calificación, primero el de más alumnos, porque afecta a más gente. Los cursos sin calificación van al final, también del que tiene más alumnos al que tiene menos. Columnas `title`, `rating` y `students`, con los 12 cursos. **Lo valida:** [`TestTask2ToReview`](starter/tests/test_queries.py)

🔮 **Predict first:** ¿dónde crees que quedan los 3 cursos sin calificación con esta consulta: al comienzo o al final? Escribe tu predicción y después pon la consulta en [`queries/02_to_review.sql`](starter/queries/02_to_review.sql):

```sql
SELECT title, rating, students
FROM courses
ORDER BY rating, students DESC;
```

- [ ] Corre `python -m pytest -k task2` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva los cursos en el orden que pide la tarea, y vuelve a correr `python -m pytest -k task2` hasta que la prueba pase.

**Criterio de éxito:** `TestTask2ToReview` pasa. Con todas las pruebas, 3 pasan y 3 fallan.

### Tarea 3 · El menú de categorías
**Objetivo:** el menú de la web muestra cada categoría una sola vez, en orden alfabético. Columna `category`. **Lo valida:** [`TestTask3Categories`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero quiso mostrar también los niveles de cada categoría y escribió esta consulta. ¿Crees que cada categoría sale una sola vez? Escribe tu predicción y después pon la consulta en [`queries/03_categories.sql`](starter/queries/03_categories.sql):

```sql
SELECT DISTINCT category, level
FROM courses
ORDER BY category, level;
```

- [ ] Corre `python -m pytest -k task3` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva el menú que pide la tarea, y vuelve a correr `python -m pytest -k task3` hasta que la prueba pase.

**Criterio de éxito:** `TestTask3Categories` pasa. Con todas las pruebas, 4 pasan y 2 fallan.

### Tarea 4 · La portada
**Objetivo:** la portada muestra los 3 cursos mejor calificados, del primero al tercero. Si dos tienen la misma calificación, va primero el de más alumnos. Columnas `title`, `rating` y `students`. **Lo valida:** [`TestTask4TopRated`](starter/tests/test_queries.py)

🔮 **Predict first:** *Python para análisis de datos* (980 alumnos) y *JavaScript moderno* (760) tienen los dos 4.6, la tercera mejor calificación. ¿Cuál crees que sale en el tercer lugar con esta consulta, y por qué? Escribe tu predicción y después pon la consulta en [`queries/04_top_rated.sql`](starter/queries/04_top_rated.sql):

```sql
SELECT title, rating, students
FROM courses
ORDER BY rating DESC
LIMIT 3;
```

- [ ] Corre `python -m pytest -k task4` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva la portada que pide la tarea, y vuelve a correr `python -m pytest -k task4` hasta que la prueba pase.

**Criterio de éxito:** `TestTask4TopRated` pasa. Con todas las pruebas, 5 pasan y 1 falla.

### Tarea 5 · La segunda página
**Objetivo:** el listado de la web va del curso más barato al más caro, y a igual precio, por título en orden alfabético. Muestra 4 cursos por página. Devuelve la página 2. Columnas `title` y `price`. **Lo valida:** [`TestTask5SecondPage`](starter/tests/test_queries.py)

🔮 **Predict first:** un compañero escribió esta consulta «porque es la página 2». ¿Crees que devuelve la página 2, es decir, los cursos 5 a 8 del listado? Escribe tu predicción y después pon la consulta en [`queries/05_second_page.sql`](starter/queries/05_second_page.sql):

```sql
SELECT title, price
FROM courses
ORDER BY price, title
LIMIT 4 OFFSET 2;
```

- [ ] Corre `python -m pytest -k task5` y compara lo que muestra con tu predicción.
- [ ] Reemplaza la consulta de la predicción por una que devuelva la página 2, y vuelve a correr `python -m pytest -k task5` hasta que la prueba pase.
- [ ] Corre todas las pruebas con `python -m pytest -v`.

**Criterio de éxito:** `TestTask5SecondPage` pasa: las 6 pruebas pasan.

## 🔍 Command dissection
| Parte | Qué hace |
|---|---|
| `ORDER BY a, b` | Ordena por `a`; solo mira `b` cuando dos filas empatan en `a` |
| `ASC` / `DESC` | De menor a mayor (si no escribes nada) / de mayor a menor |
| `NULLS FIRST` / `NULLS LAST` | Los `NULL` al comienzo / al final |
| `ORDER BY alias` | Ordena por un alias del `SELECT`; a diferencia de `WHERE`, funciona en todos los motores |
| `SELECT DISTINCT …` | Deja una sola copia de cada fila repetida del resultado |
| `LIMIT n` | Como mucho `n` filas |
| `OFFSET n` | Salta las primeras `n` filas; va después de `LIMIT` |
| `SELECT … FROM … WHERE … ORDER BY … LIMIT … OFFSET …` | El orden en que se escriben las partes |

## 💼 En proyectos reales
- **Cada página es una consulta aparte, así que el orden tiene que ser único.** Si dos filas empatan justo en el borde de una página, nada obliga a la base a ponerlas igual en las dos consultas: una fila puede salir en dos páginas y otra en ninguna. Termina el `ORDER BY` con una columna que no se repite, como el `id`: `ORDER BY price, id`.
- **`OFFSET` grande es lento.** Para devolver la página 5000, la base igual recorre las filas que salta. Las aplicaciones grandes paginan desde la última fila mostrada (`WHERE id > 120 ORDER BY id LIMIT 20`), lo que se llama *keyset pagination*.
- **`LIMIT` no es estándar.** SQLite, PostgreSQL y MySQL lo tienen; el estándar escribe `OFFSET 4 ROWS FETCH FIRST 4 ROWS ONLY`, que PostgreSQL acepta y SQLite no (`near "0": syntax error`). SQLite y MySQL aceptan también `LIMIT 4, 4`, con el salto primero; mejor escribe `OFFSET`, que no se presta a confusión.
- **El orden alfabético de SQLite compara códigos, no el idioma.** Mayúsculas antes que minúsculas, y las letras con tilde después de todas: `'Beto'`, `'Zoila'`, `'ana'`, `'Ángel'`. En PostgreSQL y MySQL depende de la *collation* (las reglas de comparación de textos del [lab 1.3](../03-filter-rows/README.md)), que suele seguir las del idioma.

## 🆘 Pistas
<details><summary>Pista 1 · El primer curso es el que tiene menos alumnos</summary>

¿A qué columna se aplica el `DESC` que escribiste? ¿Y qué dirección tiene la otra columna, donde no escribiste nada?
</details>

<details><summary>Pista 2 · Los cursos sin calificación quedan en el lugar equivocado</summary>

En Conceptos, ¿cómo se dice dónde quieres los `NULL`? Va justo después de la columna, antes de la coma.
</details>

<details><summary>Pista 3 · Las columnas no coinciden, o una categoría sale varias veces</summary>

¿Qué columnas pide la tarea? `DISTINCT` compara la fila entera, con todas sus columnas.
</details>

<details><summary>Pista 4 · <code>near "ORDER": syntax error</code>, o sale el curso equivocado en el tercer lugar</summary>

`ORDER BY` va antes que `LIMIT`: primero se ordena y después se cortan las primeras filas. Si sale el curso equivocado, ¿qué dice la tarea que pasa cuando dos cursos tienen la misma calificación? ¿Lo dice tu `ORDER BY`?
</details>

<details><summary>Pista 5 · La página no es la correcta</summary>

`OFFSET` cuenta filas, no páginas. Con 4 cursos por página, ¿cuántas filas hay antes de la página 2? ¿Y antes de la página 3?
</details>

## ✔️ Respuestas verificadas
<details><summary>Abre esta sección solo después de terminar las tareas</summary>

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

### Tarea 1 · Cada columna tiene su propia dirección
```text
01_most_popular.sql: las filas son las correctas, pero no están en el orden pedido.
  La primera fila fuera de lugar es la 1.
  Orden esperado:
     1. ('Git y GitHub', 1530, 2023)
     2. ('Excel avanzado', 1250, 2024)
     3. ('SQL desde cero', 1250, 2023)
     …
  Orden obtenido:
     1. ('Finanzas personales', 85, 2026)
     2. ('Power BI en la práctica', 120, 2026)
     3. ('Estadística para no estadísticos', 210, 2026)
     …
```

No: sale primero el que tiene menos alumnos. `DESC` se aplica solo a la columna que tiene justo antes, `year`; `students` no lleva nada, así que va de menor a mayor. No es un botón que dé vuelta todo el orden: cada columna del `ORDER BY` tiene su propia dirección, y cada una que deba ir de mayor a menor lleva su `DESC`: `SELECT title, students, year FROM courses ORDER BY students DESC, year DESC;`.

El segundo `DESC` importa: *Excel avanzado* (2024) y *SQL desde cero* (2023) empatan con 1250 alumnos, y sin él saldrían al revés.

### Tarea 2 · En SQLite, `NULL` va primero
```text
02_to_review.sql: las filas son las correctas, pero no están en el orden pedido.
  La primera fila fuera de lugar es la 1.
  …
  Orden obtenido:
     1. ('Estadística para no estadísticos', None, 210)
     2. ('Power BI en la práctica', None, 120)
     3. ('Finanzas personales', None, 85)
     4. ('Diseño de logos', 3.9, 310)
     …
```

Al comienzo. SQLite ordena un `NULL` como si fuera menor que cualquier valor: va primero con `ASC` y último con `DESC`. No todos los motores coinciden: MySQL hace lo mismo ([MySQL](https://dev.mysql.com/doc/refman/8.4/en/working-with-null.html)), y PostgreSQL al revés, último con `ASC` y primero con `DESC` ([PostgreSQL](https://www.postgresql.org/docs/current/queries-order.html)). Por eso, cuando importa, se escribe: `SELECT title, rating, students FROM courses ORDER BY rating NULLS LAST, students DESC;`.

MySQL no tiene `NULLS LAST`. La forma que funciona en todos ordena primero por una condición: `ORDER BY rating IS NULL, rating, students DESC`. `rating IS NULL` vale `0` para los cursos con calificación y `1` para los que no tienen, así que estos quedan al final.

### Tarea 3 · `DISTINCT` mira la fila entera
```text
03_categories.sql: las columnas no coinciden (importan el nombre y el orden).
  Esperadas: category
  Obtenidas: category, level
  Tus primeras filas:
    ('Datos', 'básico')
    ('Datos', 'intermedio')
    ('Diseño', 'básico')
```

No: `Datos` sale dos veces. `DISTINCT` no se aplica a una columna sino a la fila completa, y `('Datos', 'básico')` y `('Datos', 'intermedio')` son filas distintas. La consulta devuelve 10 filas, una por cada combinación de categoría y nivel que existe. Escribir `DISTINCT(category), level` no cambia nada: los paréntesis solo rodean la columna. Además, ¿qué nivel mostraría al lado de `Datos`, si tiene dos? La tarea pide solo la categoría: `SELECT DISTINCT category FROM courses ORDER BY category;`.

Para `DISTINCT`, dos `NULL` cuentan como iguales, aunque `NULL = NULL` no sea verdadera (lab 1.4): `SELECT DISTINCT rating FROM courses` devuelve un solo `None`.

### Tarea 4 · `LIMIT` corta los empates a ciegas
```text
04_top_rated.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 3; obtenidas: 3
  Esperadas que no salieron:
    ('Python para análisis de datos', 4.6, 980)
  Obtenidas que no se esperaban:
    ('JavaScript moderno', 4.6, 760)
```

Salió *JavaScript moderno*, el que está antes en la tabla, en las tres versiones probadas. Pero SQL no lo promete: si el `ORDER BY` no dice cómo desempatar, la base puede devolver los empatados en cualquier orden, y `LIMIT` corta donde caiga. La tarea da la regla, y la consulta tiene que escribirla: `SELECT title, rating, students FROM courses ORDER BY rating DESC, students DESC LIMIT 3;`.

Es una pregunta clásica de entrevista: «dame los 3 mejores». Antes de escribir, pregunta qué hacer con los empates: desempatar con otra columna, como aquí, o mostrar a todos los empatados, que se resuelve con las funciones de ranking del bloque 4. Y si la consulta pasa a PostgreSQL, `ORDER BY rating DESC` pone primero los cursos sin calificación: escribe `NULLS LAST` también ahí.

### Tarea 5 · `OFFSET` cuenta filas, no páginas
```text
05_second_page.sql: las columnas están bien, pero las filas no coinciden (el orden de las filas no importa).
  Filas esperadas: 4; obtenidas: 4
  Esperadas que no salieron:
    ('Diseño de logos', 59)
    ('Estadística para no estadísticos', 59)
  Obtenidas que no se esperaban:
    ('Excel avanzado', 39)
    ('Figma para principiantes', 49)
```

No: devuelve los cursos 3 a 6. `OFFSET 2` salta 2 filas, no 2 páginas. La página `n` de `k` filas salta las de las páginas anteriores: `OFFSET (n − 1) × k`. Para la página 2 de 4, `OFFSET 4`: `SELECT title, price FROM courses ORDER BY price, title LIMIT 4 OFFSET 4;`.

El `title` del `ORDER BY` también trabaja: tres cursos cuestan 49 soles, y la página 1 termina justo entre ellos. Sin desempate, la base decide cuál de los tres queda en cada página. Y una página después del final no da error: `LIMIT 4 OFFSET 20` devuelve cero filas, y así sabe la web que no hay más.
</details>

## 🎤 Autoevaluación
1. Una aplicación muestra «los últimos pedidos» con `SELECT * FROM orders LIMIT 10`, sin `ORDER BY`. En las pruebas siempre salieron los correctos. ¿Por qué es un error igual?
2. ¿En qué orden salen las filas de `ORDER BY department, salary DESC`? ¿Qué escribirías para que los departamentos también vayan de la Z a la A?
3. `SELECT DISTINCT city, district FROM clients` devuelve ciudades repetidas. ¿Es un error de la base? ¿Qué devuelve en realidad?
4. Te piden «los 3 vendedores con más ventas», y el tercero y el cuarto empatan. ¿Qué devuelve `ORDER BY sales DESC LIMIT 3`, y qué le preguntarías a quien lo pidió?
5. Pasaste una consulta de SQLite a PostgreSQL y su `ORDER BY rating DESC LIMIT 3` ahora devuelve cursos sin calificación. ¿Por qué, y cómo la escribirías para que dé lo mismo en los dos motores?

<details><summary>Respuestas</summary>

1. Sin `ORDER BY`, la base no promete ningún orden: devuelve las filas como le resulte cómodo, y eso puede cambiar con más datos, un índice nuevo u otra versión. Para «los últimos» hay que ordenar por la fecha, de mayor a menor, con un desempate único: `ORDER BY created_at DESC, id DESC LIMIT 10`.
2. Los departamentos de la A a la Z (sin dirección, `ASC`) y, dentro de cada uno, los sueldos de mayor a menor. Para invertir los departamentos: `ORDER BY department DESC, salary DESC`.
3. No. `DISTINCT` quita las filas repetidas, y cada fila tiene ciudad y distrito: Lima sale una vez por cada distrito distinto. Si solo quieres ciudades, pide solo `city`.
4. Tres filas, y cuál de los dos empatados entra no está definido. Preguntaría qué hacer con los empates: desempatar con otra columna (otra métrica, el nombre) o mostrar a los dos, que se resuelve con funciones de ranking.
5. PostgreSQL ordena los `NULL` como mayores que cualquier valor, así que con `DESC` van primero; SQLite, al revés. `ORDER BY rating DESC NULLS LAST` funciona en los dos (y `ORDER BY rating IS NULL, rating DESC` también en MySQL).
</details>

La solución completa está en [`solution/`](solution/).

## 🔁 Retrospectiva
- ¿Qué entendí?
- ¿Qué me costó?
- ¿Qué debería reforzar?
