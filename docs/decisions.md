# Decisiones

Solo las que alguien podría deshacer sin saber por qué. Si una cambia, se actualiza su entrada en el mismo commit.

## Stack y versiones (25 nov 2026)
- **Python 3.12 o superior, verificado en 3.12 y 3.15.** El dueño del curso pidió primero 3.11+ y aceptó subir el mínimo. Dos cosas que el curso usa existen solo desde 3.12, y se comprobó corriéndolas: la consola interactiva `python -m sqlite3` (en 3.11 da `No module named sqlite3.__main__`), que el lab 1.1 usa para explorar, y el atributo `Connection.autocommit`, del lab 5.5. Además, 3.11 deja de tener soporte en octubre de 2027, posiblemente durante el curso. 3.15 es la estable más reciente (soporte hasta octubre de 2031); el CI corre 3.12 y 3.15.
- **SQLite es el que trae Python; el curso no usa nada que falte en SQLite 3.45.** La versión depende de quién compiló Python. Medido en esta máquina: 3.45.3 en Anaconda (Python 3.12.7), 3.50.4 en el Python de la Microsoft Store (3.13.14) y en el de uv 3.14.4, y 3.53.1 en los de uv 3.11.18, 3.12.16, 3.13.18 y 3.15.2. En todas funcionaron las funciones de ventana, las CTE recursivas, `RETURNING`, las tablas `STRICT`, `RIGHT` y `FULL JOIN`, `->>`, el upsert, las columnas generadas y `ALTER TABLE … DROP COLUMN`, y en todas `PRAGMA foreign_keys` viene en 0.
- **No se comprobó qué SQLite traen los instaladores de python.org para Windows**, que es lo que la mayoría del grupo va a instalar. El mínimo de 3.45 sale de las builds medidas arriba, no de esas. Por eso `SETUP.md` pide comprobar `sqlite3.sqlite_version`, y el primer lab que se construya debe medirlo en un Python de python.org y corregir esta entrada.
- **pytest 9.2.0, fijado en `requirements.txt`.** Es la única biblioteca: licencia MIT, sin avisos en OSV para 9.2.0, configuración TOML nativa (`[tool.pytest]`). El aprendiz no escribe pruebas; solo las corre (lo aprende en el lab 1.2).
- **Cada dependencia fijada pasa por pip-audit en el CI** (`audit.yml`), en cada cambio y cada lunes.

## Dependencias
- **Estrategia `shared-parent`: un único entorno virtual en la raíz.** Todos los labs usan solo pytest y la biblioteca estándar; quien aprende instala una vez. Cada variante tiene su `pyproject.toml` solo con la configuración de pytest.
- **El proyecto declara sus propias dependencias.** Es atómico (regla de StudyForge): su `pyproject.toml` es completo y no usa código de los labs.

## Diseño del camino (25 nov 2026)
- **Cinco bloques, no cuatro.** El pedido era de unos cuatro bloques. Con cuatro, el último juntaba consultas analíticas y SQL desde una aplicación: dos focos y dos proyectos distintos. El dueño aceptó cinco.
- **Para el nivel más bajo del grupo:** nunca usaron una base de datos. Saben Python básico y Excel (filtros, alguna tabla dinámica), por eso el 3.P parte de una planilla y el 4.5 traduce tablas dinámicas a SQL. Quienes ya hicieron un `SELECT` pasan rápido por 1.2 y 1.3; no se marcan como saltables porque cada uno trae una trampa de entrevista.
- **Sin bloque 00.** El Python básico del grupo alcanza para el bloque 5. La terminal la usan poco: el primer lab que la necesita da un recordatorio y un enlace. pytest no es un prerrequisito: el aprendiz no escribe pruebas, y el 1.2 enseña a correrlas y a leer un fallo.
- **En los bloques 1 a 4 el aprendiz escribe archivos `.sql`, y las pruebas los ejecutan** contra una base nueva en memoria por prueba. Así se practica SQL puro, sin Python de por medio, y la verificación es automática.
- **SQL estándar primero.** Las particularidades de SQLite (tipos flexibles, fechas como texto, claves foráneas apagadas) se enseñan como trampas y se dice qué cambia en PostgreSQL y MySQL. Quedan fuera otros motores, los ORM, los triggers y JSON en SQL.
- **El 5.4 explota una inyección SQL solo contra el código local del lab.** Es un lab de defensa: el ataque muestra por qué los parámetros importan, y el lab dice al empezar que solo se ataca código propio.
- **Las pruebas sobre el plan de consulta buscan fragmentos** (`USING INDEX`, `SCAN`), porque el texto de `EXPLAIN QUERY PLAN` cambia entre versiones de SQLite.
