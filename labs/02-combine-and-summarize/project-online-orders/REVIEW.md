# 🔍 Revisión · Pedidos de una tienda en línea

Verificado en Windows 11, en PowerShell 5.1, con Python 3.12.16 (SQLite 3.53.1); las mismas consultas dieron las mismas filas con Python 3.15.2 (SQLite 3.53.1), Python 3.14.4 (SQLite 3.50.4) y Python 3.12.7 de Anaconda (SQLite 3.45.3).

## Orden de lectura
1. [`BRIEF.md`](BRIEF.md): las reglas del dominio, las tablas y el contrato. Sin ellas, las consultas parecen arbitrarias.
2. [`reference/queries/06_customers.sql`](reference/queries/06_customers.sql): la pregunta del dominio. Junta casi todas las reglas; las otras cinco usan partes de ella.
3. [`reference/queries/01_order_totals.sql`](reference/queries/01_order_totals.sql) a [`05_best_sellers.sql`](reference/queries/05_best_sellers.sql), en orden: cada una agrega una idea.
4. [`acceptance/seed.sql`](acceptance/seed.sql): los datos. Fíjate en qué fila existe para qué error (ver [Trampas](#trampas-encontradas-al-construirlo)).
5. [`acceptance/tests/test_orders.py`](acceptance/tests/test_orders.py) y [`conftest.py`](acceptance/tests/conftest.py): qué se compara y cómo.

## Decisiones y por qué
| Decisión | Por qué | Se aprendió en |
|---|---|---|
| `o.status IN ('pagado', 'entregado')` en cada consulta, escrito igual | La regla nombra lo que sí es venta. `status <> 'cancelado'` deja entrar el pedido pendiente de Andrés Vega | [Lab 1.3](../../01-query-a-table/03-filter-rows/README.md) |
| `quantity * unit_price`, nunca `products.price` | El catálogo guarda el precio de hoy: la mochila del pedido 102 se vendió a 119 y hoy cuesta 129 | [Lab 2.2](../02-join-tables/README.md) |
| En la pregunta 1, `SUM(i.quantity * i.unit_price) + o.shipping_fee`, con el envío fuera del `SUM` | Después de unir con `order_items`, el pedido se repite una vez por línea: dentro del `SUM`, el envío se suma una vez por cada línea | [Lab 2.5](../05-filter-groups/README.md) |
| `LEFT JOIN customers` y `COALESCE(c.name, 'Invitado')` | El pedido 105 no tiene cliente: un `JOIN` lo deja fuera y sin `COALESCE` su nombre sale `None` | [Lab 2.3](../03-unmatched-rows/README.md), [lab 1.4](../../01-query-a-table/04-null-values/README.md) |
| `NOT EXISTS` con la regla de venta adentro, en la pregunta 2 | El *anti-join* sin la regla solo encuentra a quien no tiene ningún pedido (Pedro Salas). `NOT IN (SELECT customer_id …)` da 0 filas, porque el invitado pone un `NULL` en la lista. También pasan el *anti-join* con la regla en el `ON` y el `NOT IN` con `customer_id IS NOT NULL` | [Lab 2.6](../06-subqueries/README.md), [lab 2.3](../03-unmatched-rows/README.md) |
| `COUNT(DISTINCT o.id)` para las ventas de una categoría | El pedido 106 tiene dos cuadernos y el 107 dos productos de Escritura: `COUNT(o.id)` cuenta líneas, no ventas | [Lab 2.5](../05-filter-groups/README.md) |
| `HAVING SUM(…) >= 100`, no `WHERE` | El filtro es sobre el resumen de la categoría, que existe solo después del `GROUP BY`. Escritura suma justo 100.0 | [Lab 2.5](../05-filter-groups/README.md) |
| El promedio de la pregunta 4 sale de una subconsulta que agrupa por pedido | `AVG(quantity * unit_price)` promedia líneas (65.84), no ventas (115.22): con él entran 4 ventas de más | [Lab 2.5](../05-filter-groups/README.md), [lab 2.6](../06-subqueries/README.md) |
| `o.ordered_at >= DATE('2026-11-30', '-30 days')`, sin límite superior | Nada es posterior a hoy; `BETWEEN '2026-10-31' AND '2026-11-30'` sobre `ordered_at` (con hora) deja fuera la venta de hoy a las 09:30 | [Lab 1.6](../../01-query-a-table/06-transform-values/README.md), [proyecto 1.P](../../01-query-a-table/project-shop-catalog/REVIEW.md) |
| `LIMIT 4 OFFSET 4` | Página 2 de 4 por página: `OFFSET (2 − 1) × 4` | [Lab 1.5](../../01-query-a-table/05-sort-and-paginate/README.md) |
| En la pregunta 6, totalizar cada venta en una subconsulta y después unirla a `customers` con `LEFT JOIN` | Agregar antes de unir: cada venta llega como una fila, así que `COUNT` y `SUM` no se inflan, y el `LEFT JOIN` conserva a los tres clientes sin ventas. Una subconsulta correlacionada en el `SELECT` da lo mismo | [Lab 2.5](../05-filter-groups/README.md), [lab 2.6](../06-subqueries/README.md) |
| `GROUP BY c.id, c.name` y desempate `c.name, c.id` | Hay dos María López: agrupar por el nombre las junta en una | [Lab 2.4](../04-group-and-summarize/README.md) |
| `COUNT(s.order_id)` y `COALESCE(SUM(s.total), 0)` | Tras un `LEFT JOIN`, `COUNT(*)` cuenta 1 para quien no tiene ventas y `SUM` da `NULL` | [Lab 2.4](../04-group-and-summarize/README.md) |
| `ROUND(…, 2)` en cada monto | El brief pide 2 decimales. Con estos datos, `ROUND(x, 3)` y no redondear también pasan (todos los montos son exactos); `ROUND(x, 1)` falla en 153.75 y 481.25 | [Lab 1.2](../../01-query-a-table/02-first-queries/README.md) |

## Trampas encontradas al construirlo
- **Cada regla necesita una fila que la delate en cada consulta que la usa.** Antes de dar el proyecto por terminado, 78 variantes (55 equivocadas y 23 correctas pero distintas) corrieron contra los datos en los cuatro Python de arriba: cada equivocada dio otras filas y cada correcta, las mismas. Dos quedaron así por eso:
  - **El pedido 111 (Jorge Ríos, cancelado).** Sin él, «tiene un pedido que no es venta, o ninguno» daba los mismos tres clientes que «no tiene ninguna venta» en la pregunta 2, porque nadie tenía las dos cosas.
  - **La mochila del pedido 108 (2 unidades).** Con 1 unidad, contar líneas (`COUNT(*)`) en vez de sumar `quantity` daba la misma página 2 en la pregunta 5.
- **El promedio quedó entre dos ventas cercanas.** El subtotal promedio es 115.22: el pedido 105 (116) entra y el 106 (115) no. Así se nota un promedio calculado sobre líneas (65.84), sobre todos los pedidos sin la regla de venta (128.52) o sobre los totales con envío (123.84).
- **Los empates se guardan al revés de su desempate.** SQLite devolvió los grupos en el orden de su clave, así que un desempate que falta solo se ve si ese orden es el contrario: los tres clientes sin ventas (ids 5, 6, 7) van por nombre como 7, 6, 5; en la pregunta 5, Agenda (2), Lapicero (3), Mochila (5) y Cartuchera (6) empatan con 2 unidades y por nombre van Agenda, Cartuchera, Lapicero, Mochila.
- **La página 2 es la última, y corta.** Seis productos se vendieron en el último mes: la página 2 tiene 2 filas, y cualquier producto de más o de menos la cambia. El borde de la fecha tiene una venta a cada lado: el pedido 105 (2026-10-30, fuera) y el 106 (2026-10-31 20:15, dentro), más la venta de hoy con hora (110).
- **Un cambio a medias puede pasar.** Usar `p.price` solo en el `HAVING` de la pregunta 3 pasó (las mismas tres categorías superan los 100 soles con los dos precios); usarlo también en `revenue`, como haría quien confunde los precios, falla.

## 🔨 Rómpelo tú
Cambia una cosa en una copia de [`reference/queries/`](reference/queries/), corre desde `acceptance/` `python -m pytest --queries=<tu copia>` y compara con el fallo real de abajo. En cada fila falla solo la prueba nombrada; las otras 6 pasan.

| # | Cambio | Prueba que falla | Fallo real |
|---|---|---|---|
| 1 | En `01_order_totals.sql`, `LEFT JOIN customers` → `JOIN customers` | `TestTask1OrderTotals` | `Filas esperadas: 8; obtenidas: 7` … `Esperadas que no salieron: (105, 'Invitado', 131.0)` |
| 2 | En `01_order_totals.sql`, `SUM(i.quantity * i.unit_price) + o.shipping_fee` → `SUM(i.quantity * i.unit_price + o.shipping_fee)` | `TestTask1OrderTotals` | `Obtenidas que no se esperaban: (101, 'Lucía Torres', 88.0)` `(105, 'Invitado', 146.0)` `(106, 'María López', 135.0)` `(107, 'Lucía Torres', 70.0)` |
| 3 | En `02_no_purchases.sql`, el `NOT EXISTS (SELECT 1 … WHERE o.customer_id = c.id AND …)` → `c.id NOT IN (SELECT o.customer_id FROM orders AS o WHERE o.status IN ('pagado', 'entregado'))` | `TestTask2NoPurchases` | `Filas esperadas: 3; obtenidas: 0` |
| 4 | En `02_no_purchases.sql`, `AND o.status IN ('pagado', 'entregado')` → `AND o.status <> 'cancelado'` | `TestTask2NoPurchases` | `Filas esperadas: 3; obtenidas: 2` … `Esperadas que no salieron: (7, 'Andrés Vega', 'andres.vega@example.com')` |
| 5 | En `03_categories.sql`, `COUNT(DISTINCT o.id)` → `COUNT(o.id)` | `TestTask3Categories` | `Obtenidas que no se esperaban: ('Mochilas', 4, 6, 481.25)` `('Cuadernos', 4, 9, 177.5)` `('Escritura', 4, 6, 100.0)` |
| 6 | En `03_categories.sql`, `>= 100` → `> 100` | `TestTask3Categories` | `Filas esperadas: 3; obtenidas: 2` … `Esperadas que no salieron: ('Escritura', 3, 6, 100.0)` |
| 7 | En `04_big_orders.sql`, la subconsulta del promedio → `SELECT AVG(i.quantity * i.unit_price) FROM orders AS o JOIN order_items AS i ON i.order_id = o.id WHERE o.status IN ('pagado', 'entregado')` | `TestTask4BigOrders` | `Filas esperadas: 3; obtenidas: 7` … `Obtenidas que no se esperaban: (106, 115.0)` `(110, 82.0)` `(103, 79.0)` `(101, 68.0)` |
| 8 | En `05_best_sellers.sql`, `o.ordered_at >= DATE('2026-11-30', '-30 days')` → `o.ordered_at BETWEEN '2026-10-31' AND '2026-11-30'` | `TestTask5BestSellers` | `Filas esperadas: 2; obtenidas: 1` … `Esperadas que no salieron: (5, 'Mochila escolar', 2)` |
| 9 | En `05_best_sellers.sql`, `ORDER BY units DESC, p.name` → `ORDER BY units DESC, p.id` | `TestTask5BestSellers` | `Esperadas que no salieron: (5, 'Mochila escolar', 2)` `Obtenidas que no se esperaban: (6, 'Cartuchera doble', 2)` |
| 10 | En `06_customers.sql`, `GROUP BY c.id, c.name` → `GROUP BY c.name` | `TestTask6Customers` | `Filas esperadas: 8; obtenidas: 7` … `Obtenidas que no se esperaban: (2, 'María López', 3, 360.75)` |
| 11 | En `06_customers.sql`, agrega `WHERE s.order_id IS NOT NULL` después del `ON` del `LEFT JOIN` | `TestTask6Customers` | `Filas esperadas: 8; obtenidas: 5` … `Esperadas que no salieron: (7, 'Andrés Vega', 0, 0.0)` `(6, 'Pedro Salas', 0, 0.0)` `(5, 'Rosa Huamán', 0, 0.0)` |
| 12 | En `06_customers.sql`, `ORDER BY spent DESC, c.name, c.id` → `ORDER BY spent DESC, c.id` | `TestTask6Customers` | `las filas son las correctas, pero no están en el orden pedido.` `La primera fila fuera de lugar es la 6.` (sale primero `(5, 'Rosa Huamán', 0, 0.0)`) |

## Lo que falta a propósito
- **La regla «venta» en un solo lugar.** Está repetida en las seis consultas, y el total de cada venta, en dos. En un sistema real viviría en un solo sitio, para que un cambio de regla («los pedidos `'pagado'` aún no son venta hasta entregarse») no obligue a buscarla en cada archivo. Escribir una consulta por pasos con nombre es del lab 4.1.
- **Guardar el total del pedido.** Aquí se calcula cada vez desde las líneas. Guardarlo en `orders` lo haría más rápido de leer, pero entonces dos datos pueden contradecirse; es una decisión de diseño del [bloque 3](../../../SYLLABUS.md#bloque-3--diseñar-y-crear-una-base).
- **Que la base rechace los datos imposibles.** Nada impide hoy una cantidad negativa, un `status` mal escrito o un `customer_id` que no existe. Es del lab 3.3.
- **Muchos pedidos.** Con 11 pedidos todo es instantáneo; con millones, unir y agrupar sin índices empieza a costar. Es del [bloque 5](../../../SYLLABUS.md#bloque-5--sql-en-una-aplicación).

## Preguntas para discutir el diseño
1. La tienda decide que un pedido `'pagado'` no es venta hasta que se entrega. ¿Cuántos archivos cambias, y qué número de la pregunta 6 cambia primero?
2. El invitado del pedido 105 cuenta en las ventas por categoría, pero no en la pregunta 6. ¿Está bien? ¿Qué le preguntarías al equipo antes de decidirlo?
3. Si un cliente devuelve un producto, ¿dónde lo guardarías: un `status` nuevo en `orders`, una cantidad negativa en `order_items` o una tabla aparte? ¿Qué consulta de este proyecto se rompe con cada opción?
4. ¿Conviene guardar `unit_price` en cada línea, o basta con `products.price`? ¿Qué pregunta de este proyecto no se podría responder sin él?
5. La pregunta 4 compara con el promedio. ¿Qué cambia si la tienda tiene una sola venta enorme? ¿Qué otra medida le propondrías al equipo?
