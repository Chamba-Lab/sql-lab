SELECT DISTINCT LOWER(TRIM(brand)) AS brand
FROM products
WHERE status = 'activo'
  AND stock > 0
  AND brand IS NOT NULL
ORDER BY brand;
