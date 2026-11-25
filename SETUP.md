# 🧰 Preparación

Instala esto una sola vez, antes del lab 1.1. No hace falta instalar SQLite: viene dentro de Python.

| Herramienta | Versión | Comprobar |
|---|---|---|
| Python | 3.12 o superior (los labs se verifican en 3.12 y 3.15) | `python --version` |
| SQLite | la que trae tu Python; el curso necesita 3.45 o superior | `python -c "import sqlite3; print(sqlite3.sqlite_version)"` |
| Git | cualquiera reciente | `git --version` |
| pytest | la de `requirements.txt` (se instala abajo) | `python -m pytest --version` |

> [!NOTE]
> En Windows, si `python` abre la Microsoft Store o no existe, instala Python desde [python.org](https://www.python.org/downloads/) y marca *Add python.exe to PATH*. El lanzador `py` también sirve: usa `py -m venv .venv` para crear el entorno; una vez activo, `python` ya es el del entorno.

## 1. Haz tu fork y clónalo

Si tomas el curso con la comunidad, haz un **fork** del repositorio en GitHub (botón *Fork*) y clona tu fork:

```bash
git clone https://github.com/<tu-usuario>/sql-lab.git
cd sql-lab
```

## 2. Crea y activa el entorno virtual

Un solo entorno para todos los labs, en la raíz del repositorio.

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Bash (Linux, macOS o Git Bash en Windows):

```bash
python -m venv .venv
source .venv/bin/activate          # Git Bash en Windows: source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

> [!TIP]
> Si PowerShell dice que la ejecución de scripts está deshabilitada, permítela solo para esta ventana con `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a activar el entorno.

**Cada vez que abras una terminal nueva**, activa el entorno otra vez (la segunda línea de cada bloque). Sabrás que está activo porque el prompt empieza con `(.venv)`.

## 3. Comprueba todo

PowerShell o Bash, con el entorno activo:

```bash
python --version
python -c "import sqlite3; print(sqlite3.sqlite_version)"
python -m pytest --version
python -c "import sys; print(sys.prefix)"
```

Deberías ver Python 3.12 o superior, una versión de SQLite 3.45 o superior, `pytest 9.2.0` y una ruta que **termina en `.venv`**.

> [!WARNING]
> Si la última línea no termina en `.venv`, el entorno no está activo y estás usando otro Python, con otras versiones. Pasa, por ejemplo, con Git Bash en máquinas que tienen Anaconda. Usa PowerShell, o llama al Python del entorno directamente: `.venv/Scripts/python` en Windows o `.venv/bin/python` en Linux y macOS.

## 4. Guarda tus soluciones

Trabaja en tu fork. Si prefieres separar tus soluciones de la copia limpia, crea una rama:

```bash
git switch -c solutions/tu-nombre
```

Cuando el curso reciba mejoras, tráelas a tu fork con el botón *Sync fork* de GitHub, o desde la terminal con `git pull https://github.com/Chamba-Lab/sql-lab.git master`. Después, con el entorno activo, vuelve a correr `python -m pip install -r requirements.txt`: un bloque nuevo puede traer bibliotecas nuevas.

## Leer las guías

Las guías usan diagramas Mermaid, que GitHub muestra de forma nativa. En VS Code, las versiones recientes los muestran en la vista previa de Markdown; en versiones anteriores instala *Markdown Preview Mermaid Support*. En los IDE de JetBrains, activa Mermaid en la configuración de Markdown.
