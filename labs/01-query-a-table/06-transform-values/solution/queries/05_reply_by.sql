SELECT id,
       DATE(applied_at) AS applied_on,
       DATE(applied_at, '+7 days') AS reply_by
FROM applications;
