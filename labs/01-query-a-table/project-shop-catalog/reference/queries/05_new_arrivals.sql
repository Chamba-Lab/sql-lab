SELECT id, name, DATE(added_at) AS added_on
FROM products
WHERE status = 'activo'
  AND stock > 0
  AND added_at >= DATE('2026-11-20', '-30 days')
ORDER BY added_at DESC
LIMIT 3 OFFSET 3;
