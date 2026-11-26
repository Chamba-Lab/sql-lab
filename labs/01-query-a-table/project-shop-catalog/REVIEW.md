# 🔍 Revisión · Catálogo de una tienda

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1) y con Python 3.12.7 de Anaconda (SQLite 3.45.3).

## Orden de lectura
1. [`BRIEF.md`](BRIEF.md): las reglas del dominio y el contrato. Sin ellas, las consultas parecen arbitrarias.
2. [`reference/queries/06_catalog.sql`](reference/queries/06_catalog.sql): la pregunta del dominio. Junta todas las reglas; las otras cinco consultas usan partes de ella.
3. [`reference/queries/01_search.sql`](reference/queries/01_search.sql) a [`05_new_arrivals.sql`](reference/queries/05_new_arrivals.sql), en orden: cada una agrega una idea.
4. [`acceptance/seed.sql`](acceptance/seed.sql): los datos. Fíjate en qué fila existe para qué error (ver [Trampas](#trampas-encontradas-al-construirlo)).
5. [`acceptance/tests/test_catalog.py`](acceptance/tests/test_catalog.py) y [`conftest.py`](acceptance/tests/conftest.py): qué se compara y cómo.

## Decisiones y por qué
| Decisión | Por qué | Se aprendió en |
|---|---|---|
| `stock > 0` para «hay stock», sin tratar el `NULL` aparte | Una comparación con `NULL` es desconocida y `WHERE` no deja pasar la fila: el stock sin contar queda fuera solo, como pide la regla | [Lab 1.4](../04-null-values/README.md) |
| `promo_ends IS NULL OR promo_ends >= '2026-11-20'`, entre paréntesis | Sin el `IS NULL` se pierden las promociones sin fin; sin los paréntesis, el `OR` se escapa del resto del `WHERE` | [Lab 1.3](../03-filter-rows/README.md), [lab 1.4](../04-null-values/README.md) |
| `promo_price IS NOT NULL` dentro del `CASE` del precio final | Un producto sin promoción también tiene `promo_ends` en `NULL`: sin esa condición, su precio final sería `NULL` | [Lab 1.4](../04-null-values/README.md), [lab 1.6](../06-transform-values/README.md) |
| `COALESCE(NULLIF(category, ''), 'Otros')` | `COALESCE` solo reemplaza `NULL`; el texto vacío primero se convierte en `NULL` con `NULLIF` | [Lab 1.4](../04-null-values/README.md) |
| `SELECT DISTINCT LOWER(TRIM(brand))` | `DISTINCT` compara los valores tal como salen: hay que limpiarlos antes, en la misma expresión | [Lab 1.5](../05-sort-and-paginate/README.md), [lab 1.6](../06-transform-values/README.md) |
| `ROUND((price - promo_price) * 100 / price, 1)` | Los paréntesis hacen la resta antes de dividir; `price` es `REAL`, así que la división no corta decimales | [Lab 1.2](../02-first-queries/README.md) |
| `ORDER BY stock NULLS LAST, name` | SQLite pone los `NULL` primero en un orden ascendente; `ORDER BY stock IS NULL, stock, name` da lo mismo y es la forma que el lab 1.5 da por portable (MySQL no tiene `NULLS LAST`, según ese lab; no se volvió a comprobar en su documentación para este proyecto) | [Lab 1.5](../05-sort-and-paginate/README.md) |
| `ORDER BY discount_pct DESC, name` y `ORDER BY category, final_price, name`, con los alias | El orden es sobre lo que se muestra (el descuento redondeado, la categoría con `'Otros'`), y cada orden termina en un desempate | [Lab 1.5](../05-sort-and-paginate/README.md) |
| `added_at >= DATE('2026-11-20', '-30 days')`, sin límite superior | Nada en el catálogo es posterior a hoy; un `BETWEEN … AND '2026-11-20'` sobre `added_at` (sin `DATE()`) dejaría fuera lo agregado hoy con hora | [Lab 1.6](../06-transform-values/README.md) |
| `LIMIT 3 OFFSET 3` | Página 2 de 3 por página: `OFFSET (2 − 1) × 3` | [Lab 1.5](../05-sort-and-paginate/README.md) |
| Hoy es `'2026-11-20'`, escrito en cada consulta | Con `DATE('now')` las respuestas cambiarían cada día y las pruebas no podrían fijarlas | Este proyecto |

## Trampas encontradas al construirlo
- **Cada error de principiante necesita una fila que lo delate.** Antes de dar el proyecto por terminado, 60 variantes (49 equivocadas y 11 correctas pero distintas) corrieron contra los datos en los tres Python de arriba: cada equivocada falló y cada correcta pasó. Una equivocada pasó al principio: `WHERE status = 'activo' AND stock < 5 OR stock IS NULL` en la pregunta 3, porque el único stock `NULL` era de un producto activo. Ahora la cámara web (descontinuada) también tiene el stock sin contar, y esa variante trae una fila de más.
- **Los empates se guardan al revés de su desempate.** SQLite devolvió las filas empatadas en el orden en que se guardaron (lab 1.5), así que un desempate que falta solo se ve si ese orden es el contrario: el hub (id 3) va antes que el adaptador (id 4), los dos a 79.9; el mouse (id 6) antes que el monitor (id 8), los dos con 11.1 %; el parlante (id 2) antes que el cargador (id 12), los dos agotados.
- **La página 2 tiene que ser la última, y corta.** Con 6 novedades, la página 2 serían las filas 4 a 6, y una séptima que se colara por el borde de la fecha quedaría en la página 3, donde la prueba no mira. Con 5, la página 2 tiene 2 filas y cualquier fila de más o de menos la cambia.
- **Una consulta con `DATE('now')` falla sin decir por qué** (lo encontró la validación): el día real no es el 20 de noviembre y faltan filas en las preguntas 4 a 6. El arnés ahora agrega `Recuerda: hoy es '2026-11-20'…` cuando la consulta usa `'now'`, y el brief lo dice junto a la fecha.
- **El descuento redondeado y el sin redondear no ordenan igual.** El monitor tiene 11.09 % y el mouse 11.12 %: los dos se muestran como 11.1, y el orden por nombre pone primero al monitor. Ordenar por la expresión sin redondear pone primero al mouse.
- **`--queries` con un espacio rompe pytest.** `python -m pytest --queries ../reference/queries` da `error: unrecognized arguments: --queries`: pytest lee `../reference/queries` como una carpeta de pruebas antes de cargar la opción, y busca su configuración allí. Con `--queries=../reference/queries` funciona. Por eso el README usa siempre la forma con `=`, y la carpeta por defecto, `my-queries/`, no necesita la opción.

## 🔨 Rómpelo tú
Cambia una cosa en una copia de [`reference/queries/`](reference/queries/), corre desde `acceptance/` `python -m pytest --queries=../reference/queries` y compara con el fallo real de abajo. En cada fila falla solo la prueba nombrada; las otras 6 pasan.

| # | Cambio | Prueba que falla | Fallo real |
|---|---|---|---|
| 1 | En `01_search.sql`, quita los paréntesis del `OR` | `TestTask1Search` | `las columnas están bien, pero las filas no coinciden` … `Obtenidas que no se esperaban: (5, 'Memoria USB 64 GB')` |
| 2 | En `02_brands.sql`, `LOWER(TRIM(brand))` → `LOWER(brand)` | `TestTask2Brands` | `Filas esperadas: 6; obtenidas: 8` … `(' anker',)` `('xiaomi ',)` |
| 3 | En `03_restock.sql`, `ORDER BY stock NULLS LAST, name` → `ORDER BY stock, name` | `TestTask3Restock` | `las filas son las correctas, pero no están en el orden pedido.` `La primera fila fuera de lugar es la 1.` (sale primero `(8, 'Monitor 24 pulgadas', None, 'sin contar')`) |
| 4 | En `03_restock.sql`, `AND (stock < 5 OR stock IS NULL)` → `AND stock < 5` | `TestTask3Restock` | `Filas esperadas: 6; obtenidas: 5` … `Esperadas que no salieron: (8, 'Monitor 24 pulgadas', None, 'sin contar')` |
| 5 | En `04_promotions.sql`, `promo_ends >= '2026-11-20'` → `promo_ends > '2026-11-20'` | `TestTask4Promotions` | `Filas esperadas: 7; obtenidas: 5` … `(5, 'Memoria USB 64 GB', 39.9, 34.9, 12.5)` `(13, 'Celular Redmi 13', 899.0, 849.0, 5.6)` |
| 6 | En `04_promotions.sql`, quita `, name` del `ORDER BY` | `TestTask4Promotions` | `las filas son las correctas, pero no están en el orden pedido.` `La primera fila fuera de lugar es la 5.` |
| 7 | En `05_new_arrivals.sql`, `added_at >= DATE('2026-11-20', '-30 days')` → `added_at BETWEEN '2026-10-21' AND '2026-11-20'` | `TestTask5NewArrivals` | `Filas esperadas: 2; obtenidas: 1` … `Esperadas que no salieron: (11, 'Soporte para celular', '2026-11-05')` |
| 8 | En `06_catalog.sql`, `COALESCE(NULLIF(category, ''), 'Otros')` → `COALESCE(category, 'Otros')` | `TestTask6Catalog` | `Esperadas que no salieron: (10, 'Funda para laptop 14', 'Otros', 49.9)` `Obtenidas que no se esperaban: (10, 'Funda para laptop 14', '', 49.9)` |
| 9 | En `06_catalog.sql`, deja el `WHEN` del precio final solo como `WHEN promo_ends >= '2026-11-20' THEN promo_price` | `TestTask6Catalog` | `Esperadas que no salieron: (6, 'Mouse inalámbrico M3', 'Cómputo', 79.9)` `Obtenidas que no se esperaban: (6, 'Mouse inalámbrico M3', 'Cómputo', 89.9)` |
| 10 | En `06_catalog.sql`, `ORDER BY category, final_price, name` → `ORDER BY category, price, name` | `TestTask6Catalog` | `las filas son las correctas, pero no están en el orden pedido.` `La primera fila fuera de lugar es la 3.` (los audífonos con cable, a 159.0, pasan antes que los Bluetooth en promoción a 149.9) |

## Lo que falta a propósito
- **Contar y sumar** («¿cuántos productos se pueden vender por categoría?»): las funciones de agregado son del [bloque 2](../../../SYLLABUS.md#bloque-2--combinar-y-resumir).
- **La regla «se puede vender hoy» en un solo lugar.** Está repetida en cuatro consultas. En un sistema real viviría en un solo sitio (una vista, o una columna calculada), para que un cambio de regla no obligue a buscarla en cada archivo.
- **Corregir los datos en la tabla.** Las marcas se limpian al consultar, cada vez. Lo sano es guardarlas ya limpias y que la base rechace las sucias: es del [bloque 3](../../../SYLLABUS.md#bloque-3--diseñar-y-crear-una-base).
- **Un catálogo grande.** Con 17 productos todo es instantáneo; con cientos de miles, `LIKE '%usb%'` y `OFFSET` empiezan a costar. Es del [bloque 5](../../../SYLLABUS.md#bloque-5--sql-en-una-aplicación).

## Preguntas para discutir el diseño
1. Ventas decide que los productos `'pausado'` también se pueden vender. ¿Cuántos archivos cambias, y cómo evitarías tener que buscarlos?
2. El stock sin contar se trata como «no se vende». ¿Es la mejor decisión para la tienda? ¿Qué le preguntarías al equipo antes de decidirlo?
3. Un cliente está en la página 1 de Novedades y, antes de pasar a la 2, se agrega un producto nuevo. ¿Qué ve en la página 2? ¿Qué cambiarías? (Repasa el 💼 del [lab 1.5](../05-sort-and-paginate/README.md).)
4. ¿Conviene calcular `discount_pct` en la consulta o en la página web que lo muestra? ¿Qué ganas y qué pierdes en cada caso?
5. La pregunta 4 muestra promociones de productos que hoy no se pueden vender. ¿Para quién es útil eso, y para quién sería un error?
