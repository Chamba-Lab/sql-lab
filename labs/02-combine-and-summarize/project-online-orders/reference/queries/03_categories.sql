-- Sales by category, keeping the categories that sold 100 soles or more.
SELECT p.category,
       COUNT(DISTINCT o.id) AS orders,
       SUM(i.quantity) AS units,
       ROUND(SUM(i.quantity * i.unit_price), 2) AS revenue
FROM order_items AS i
JOIN orders AS o ON o.id = i.order_id
JOIN products AS p ON p.id = i.product_id
WHERE o.status IN ('pagado', 'entregado')
GROUP BY p.category
HAVING SUM(i.quantity * i.unit_price) >= 100
ORDER BY revenue DESC, p.category;
