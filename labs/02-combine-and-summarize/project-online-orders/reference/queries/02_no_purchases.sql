-- Registered customers with no sale: no order, or only pending or cancelled ones.
SELECT c.id, c.name, c.email
FROM customers AS c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.id
      AND o.status IN ('pagado', 'entregado')
)
ORDER BY c.id;
