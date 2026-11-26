SELECT id,
       name,
       price,
       promo_price,
       ROUND((price - promo_price) * 100 / price, 1) AS discount_pct
FROM products
WHERE promo_price IS NOT NULL
  AND (promo_ends IS NULL OR promo_ends >= '2026-11-20')
ORDER BY discount_pct DESC, name;
