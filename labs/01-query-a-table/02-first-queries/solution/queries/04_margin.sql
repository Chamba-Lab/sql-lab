SELECT name, ROUND((price - cost) * 100 / price, 1) AS margin_pct
FROM menu_items;
