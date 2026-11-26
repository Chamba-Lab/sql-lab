SELECT id,
       expected_salary,
       CASE
           WHEN expected_salary IS NULL THEN 'sin dato'
           WHEN expected_salary >= 2500 THEN 'alto'
           WHEN expected_salary >= 1500 THEN 'medio'
           ELSE 'bajo'
       END AS salary_band
FROM applications;
