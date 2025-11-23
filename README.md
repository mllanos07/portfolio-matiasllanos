# Portfolio Matias

Proyecto integrador de portfolio web para la materia **Laboratorio de programacion**.

Aplicación web full stack con:

- **Flask** (Python) como backend.
- **Jinja2** para plantillas.
- **Flask-WTF** para formularios (login y edición de la pagina).
- **Bootstrap 5**, Google Fonts y FontAwesome para el diseño responsive.
- Base de datos **MySQL** (script `schema.sql`).

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
