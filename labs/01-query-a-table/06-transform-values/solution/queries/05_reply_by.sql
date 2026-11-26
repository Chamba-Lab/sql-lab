SELECT id,
       date(applied_at) AS applied_on,
       date(applied_at, '+7 days') AS reply_by
FROM applications;
