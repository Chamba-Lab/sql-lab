SELECT id,
       name,
       COALESCE(NULLIF(category, ''), 'Otros') AS category,
       CASE
           WHEN promo_price IS NOT NULL
                AND (promo_ends IS NULL OR promo_ends >= '2026-11-20') THEN promo_price
           ELSE price
       END AS final_price
FROM products
WHERE status = 'activo'
  AND stock > 0
ORDER BY category, final_price, name;
