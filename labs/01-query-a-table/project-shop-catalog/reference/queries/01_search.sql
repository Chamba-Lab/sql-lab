SELECT id, name
FROM products
WHERE (name LIKE '%usb%' OR name LIKE '%bluetooth%')
  AND status = 'activo'
  AND stock > 0
ORDER BY name;
