SELECT id,
       name,
       stock,
       CASE
           WHEN stock IS NULL THEN 'sin contar'
           WHEN stock = 0 THEN 'agotado'
           ELSE 'bajo'
       END AS stock_status
FROM products
WHERE status = 'activo'
  AND (stock < 5 OR stock IS NULL)
ORDER BY stock NULLS LAST, name;
