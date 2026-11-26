-- Total of every sale: its lines at the price paid, plus its shipping fee once.
SELECT o.id AS order_id,
       COALESCE(c.name, 'Invitado') AS customer,
       ROUND(SUM(i.quantity * i.unit_price) + o.shipping_fee, 2) AS total
FROM orders AS o
LEFT JOIN customers AS c ON c.id = o.customer_id
JOIN order_items AS i ON i.order_id = o.id
WHERE o.status IN ('pagado', 'entregado')
GROUP BY o.id, c.name, o.shipping_fee
ORDER BY o.id;
