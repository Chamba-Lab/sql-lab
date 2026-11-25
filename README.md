# 🗃️ SQL con SQLite

Aprende SQL desde cero hasta el nivel que piden un primer trabajo y sus pruebas técnicas: consultar una tabla, cruzar y resumir varias, diseñar una base que no se contradiga, escribir consultas de reportes con rankings y acumulados, y usar SQL desde Python sin abrirle la puerta a una inyección. Es para quien sabe Python básico y nunca usó una base de datos, o solo hizo algún `SELECT` suelto.

Todo corre con el SQLite que ya trae Python: no instalas un servidor ni usas contenedores. **El plan completo está en el [sílabo](SYLLABUS.md); los labs se van construyendo bloque por bloque.**

| 🧱 Bloques | 🧪 Labs | ⏱️ Por lab | 🛠️ Stack |
|---|---|---|---|
| 5 | 29 + 5 proyectos | 1–2 h | Python 3.12+ · sqlite3 · pytest 9.2 |

## 🚀 Empieza
1. Instala todo con [SETUP.md](SETUP.md).
2. Trabaja en tu fork del repositorio, o en tu propia rama (`git switch -c solutions/tu-nombre`).
3. Abre el [SYLLABUS.md](SYLLABUS.md) y empieza por el lab 1.1.

> [!TIP]
> ¿No usas un agente de código? Estudia con Claude, ChatGPT o Gemini como tutor: mira [TUTOR.md](TUTOR.md).

## 🧭 Cómo funcionan los labs
- 🧩 **Reto:** cada tarea es un archivo `.sql` (o, en el bloque 5, una función de Python) con un `TODO`. Las pruebas ejecutan tu consulta contra una base de ejemplo y comparan el resultado: tu trabajo es ponerlas en verde. `solution/` está a la vista a propósito: tú decides cuándo mirar.
- 🔭 **Exploración:** una `demo/` terminada; predices, ejecutas y comparas.
- 💭 **Concepto:** lees, luego respondes la autoevaluación.
- 🏗️ **Proyecto:** al final de cada bloque; lo construyes desde `BRIEF.md` y lo comparas con `reference/`, o revisas la referencia con `REVIEW.md`.

Cada lab presenta primero la idea, con un ejemplo, y después el SQL que la escribe. Cada uno trae una trampa típica de las entrevistas y cierra con preguntas de entrevista. Los términos del oficio quedan en inglés, con su traducción la primera vez: así los vas a encontrar en el trabajo.

## 💬 Feedback
¿Terminaste un lab? Abre un issue **Feedback de lab**: qué fue claro, qué costó, qué cambiarías. Tu feedback mejora ese lab y los siguientes.

## 📖 Leer las guías
Se ven mejor en GitHub. En local, revisa la nota al final de [SETUP.md](SETUP.md) para ver los diagramas en tu editor.

---
Construido con [StudyForge](https://github.com/Chamba-Lab/studyforge) por la comunidad [Chamba Lab](https://chambalab.org).
