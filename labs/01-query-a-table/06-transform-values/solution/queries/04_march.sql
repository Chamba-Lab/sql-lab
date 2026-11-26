SELECT id, applied_at
FROM applications
WHERE STRFTIME('%Y-%m', applied_at) = '2026-03';
