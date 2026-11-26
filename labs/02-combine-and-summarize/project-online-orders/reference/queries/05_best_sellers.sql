-- Best sellers of the last 30 days (2026-10-31 to today, 2026-11-30, any hour).
-- The shop shows 4 per page: this is page 2.
SELECT p.id AS product_id, p.name, SUM(i.quantity) AS units
FROM order_items AS i
JOIN orders AS o ON o.id = i.order_id
JOIN products AS p ON p.id = i.product_id
WHERE o.status IN ('pagado', 'entregado')
  AND o.ordered_at >= DATE('2026-11-30', '-30 days')
GROUP BY p.id, p.name
ORDER BY units DESC, p.name
LIMIT 4 OFFSET 4;
