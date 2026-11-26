SELECT id, name, monthly_fee - COALESCE(discount, 0) AS to_pay
FROM members;
