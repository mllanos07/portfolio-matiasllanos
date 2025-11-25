# Portfolio Matias

Proyecto integrador de portfolio web para la materia **Laboratorio de programacion**.

Aplicación web full stack con:

- **Flask** (Python) como backend.
- **Jinja2** para plantillas.
- **Flask-WTF** para formularios (login y edición de la pagina).
- **Bootstrap 5**, Google Fonts y FontAwesome para el diseño responsive.
- Base de datos **MySQL** (script `schema.sql`).

## Pasos rapidos
1. Copiar `.env.example` a `.env` y completar la configuracion
2. Configurar entorno (solo primera vez)

Windows (powershell)
```bash
# crear y activar virtualenv (opcional)
python -m venv .venv
.venv\Scripts\Activate.ps1

# instalar dependencias
pip install -r requirements.txt
```

Linux
```bash
# crear y activar virtualenv (opcional)
python -m venv .venv
source .venv/bin/activate

# instalar dependencias
pip install -r requirements.txt
```

3. Ejecutar aplicacion

declarar la app y usar flask CLI (esto carga .env automáticamente)

Windows (Powershell)

```bash
$env:FLASK_APP = "app.py"
flask run
```

Linux
```bash
export FLASK_APP=app.py
flask run
```
## Estructura

```text
portafolio-matias/
├── app.py
├── config.py
├── db.py
├── models.py
├── forms.py
├── schema.sql
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── about_edit.html
└── static/
    ├── css/styles.css
    ├── img/matias-logo.png
    └── uploads/Modern Professional CV Resume.pdf
