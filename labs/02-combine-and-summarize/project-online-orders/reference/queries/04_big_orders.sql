-- Sales whose products cost more than the average sale.
-- The inner query gives one row per sale; the average is over those rows.
SELECT s.order_id, ROUND(s.subtotal, 2) AS subtotal
FROM (
    SELECT o.id AS order_id, SUM(i.quantity * i.unit_price) AS subtotal
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.id
    WHERE o.status IN ('pagado', 'entregado')
    GROUP BY o.id
) AS s
WHERE s.subtotal > (
    SELECT AVG(t.subtotal)
    FROM (
        SELECT SUM(i.quantity * i.unit_price) AS subtotal
        FROM orders AS o
        JOIN order_items AS i ON i.order_id = o.id
        WHERE o.status IN ('pagado', 'entregado')
        GROUP BY o.id
    ) AS t
)
ORDER BY s.subtotal DESC, s.order_id;
