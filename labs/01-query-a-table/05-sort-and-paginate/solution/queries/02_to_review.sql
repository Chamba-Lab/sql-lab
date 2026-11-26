SELECT title, rating, students
FROM courses
ORDER BY rating NULLS LAST, students DESC;
