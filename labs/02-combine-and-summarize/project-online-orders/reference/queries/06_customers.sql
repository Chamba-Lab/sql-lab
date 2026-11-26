-- The domain question: how much did each registered customer really buy?
-- Total each sale first (lines plus its shipping fee once), then add the sales
-- of each customer; the LEFT JOIN keeps the customers with no sale.
SELECT c.id AS customer_id,
       c.name,
       COUNT(s.order_id) AS orders,
       ROUND(COALESCE(SUM(s.total), 0), 2) AS spent
FROM customers AS c
LEFT JOIN (
    SELECT o.id AS order_id,
           o.customer_id,
           SUM(i.quantity * i.unit_price) + o.shipping_fee AS total
    FROM orders AS o
    JOIN order_items AS i ON i.order_id = o.id
    WHERE o.status IN ('pagado', 'entregado')
    GROUP BY o.id, o.customer_id, o.shipping_fee
) AS s ON s.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY spent DESC, c.name, c.id;
