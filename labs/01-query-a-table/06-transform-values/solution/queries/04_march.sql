SELECT id, applied_at
FROM applications
WHERE strftime('%Y-%m', applied_at) = '2026-03';
