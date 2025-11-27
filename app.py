from flask import (
    Flask, render_template, redirect, url_for,
    session, flash, request, send_from_directory
)
from functools import wraps
from config import Config
from forms import LoginForm, AboutForm
from models import (
    User, About, Experience, Education,
    Skill, Project, SocialLink
)
import os

app = Flask(__name__)
app.config.from_object(Config)


# decorador simple para proteger rutas de edicion
def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Tenés que iniciar sesión para editar el portfolio.", "warning")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper


@app.context_processor
def inject_globals():
    """
    Variables que quiero tener en todas las plantillas.
    """
    return {
        "is_logged_in": "username" in session,
        "current_user": session.get("username")
    }


@app.route("/")
def index():
    about = About.get_single()
    experiences = Experience.all()
    education = Education.all()
    skills = Skill.all()
    projects = Project.all()
    social_links = SocialLink.all()

    # separo skills por tipo para mostrarlas mas lindo
    hard_skills = [s for s in skills if s.type == "hard"]
    soft_skills = [s for s in skills if s.type == "soft"]
    languages = [s for s in skills if s.type == "language"]

    return render_template(
        "index.html",
        about=about,
        experiences=experiences,
        education=education,
        hard_skills=hard_skills,
        soft_skills=soft_skills,
        languages=languages,
        projects=projects,
        social_links=social_links,
        skills=skills,  # lista completa para los modales de edicion
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            session["username"] = user.username
            flash("Login correcto. Modo edición activado.", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Sesión cerrada.", "info")
    return redirect(url_for("index"))


@app.route("/download_cv")
def download_cv():
    # descarga del CV en PDF
    uploads_dir = os.path.join(app.root_path, "static", "uploads")
    filename = "Modern Professional CV Resume.pdf"
    return send_from_directory(uploads_dir, filename, as_attachment=True)


# Rutas de edicion

@app.route("/admin/about", methods=["GET", "POST"])
@login_required
def edit_about():
    about = About.get_single()
    if not about:
        flash("No se encontró la sección de 'Acerca de mí'.", "danger")
        return redirect(url_for("index"))

    form = AboutForm(obj=about)
    if form.validate_on_submit():
        try:
            about.full_name = form.full_name.data
            about.title = form.title.data
            about.summary = form.summary.data
            about.email = form.email.data
            about.phone = form.phone.data
            about.address = form.address.data
            about.profile_image = form.profile_image.data
            about.update()
            flash("Se actualizó la sección Acerca de mí.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            print("Error actualizando About:", e)
            flash("Hubo un error guardando los cambios en 'Acerca de mí'.", "danger")
            return redirect(url_for("edit_about"))

    return render_template("about_edit.html", form=form, about=about)


# Experiencia

@app.route("/admin/experience/add", methods=["POST"])
@login_required
def add_experience():
    role = request.form.get("role")
    company = request.form.get("company")
    description = request.form.get("description")
    year_start = request.form.get("year_start", type=int)
    year_end = request.form.get("year_end", type=int)
    is_current = request.form.get("is_current") == "on"
    if role and company:
        Experience.create(role, company, description, year_start, year_end, is_current)
        flash("Experiencia agregada.", "success")
    else:
        flash("Faltan datos para crear la experiencia.", "danger")
    return redirect(url_for("index"))


@app.route("/admin/experience/<int:exp_id>/edit", methods=["POST"])
@login_required
def edit_experience(exp_id):
    exp = Experience.from_id(exp_id)
    if not exp:
        flash("Experiencia no encontrada.", "danger")
        return redirect(url_for("index"))
    exp.role = request.form.get("role")
    exp.company = request.form.get("company")
    exp.description = request.form.get("description")
    exp.year_start = request.form.get("year_start", type=int)
    exp.year_end = request.form.get("year_end", type=int)
    exp.is_current = request.form.get("is_current") == "on"
    exp.update()
    flash("Experiencia actualizada.", "success")
    return redirect(url_for("index"))


@app.route("/admin/experience/<int:exp_id>/delete", methods=["POST"])
@login_required
def delete_experience(exp_id):
    Experience.delete(exp_id)
    flash("Experiencia eliminada.", "info")
    return redirect(url_for("index"))


# Educación

@app.route("/admin/education/add", methods=["POST"])
@login_required
def add_education():
    institution = request.form.get("institution")
    degree = request.form.get("degree")
    description = request.form.get("description")
    year_start = request.form.get("year_start", type=int)
    year_end = request.form.get("year_end", type=int)
    if institution and degree:
        Education.create(institution, degree, description, year_start, year_end)
        flash("Estudio agregado.", "success")
    else:
        flash("Faltan datos para crear el registro de educación.", "danger")
    return redirect(url_for("index"))


@app.route("/admin/education/<int:edu_id>/edit", methods=["POST"])
@login_required
def edit_education(edu_id):
    edu = Education.from_id(edu_id)
    if not edu:
        flash("Registro de educación no encontrado.", "danger")
        return redirect(url_for("index"))
    edu.institution = request.form.get("institution")
    edu.degree = request.form.get("degree")
    edu.description = request.form.get("description")
    edu.year_start = request.form.get("year_start", type=int)
    edu.year_end = request.form.get("year_end", type=int)
    edu.update()
    flash("Educación actualizada.", "success")
    return redirect(url_for("index"))


@app.route("/admin/education/<int:edu_id>/delete", methods=["POST"])
@login_required
def delete_education(edu_id):
    Education.delete(edu_id)
    flash("Registro de educación eliminado.", "info")
    return redirect(url_for("index"))


# Skills

@app.route("/admin/skill/add", methods=["POST"])
@login_required
def add_skill():
    name = request.form.get("name")
    level = request.form.get("level", type=int)
    skill_type = request.form.get("type")

    if not name:
        flash("El nombre de la skill es obligatorio.", "danger")
        return redirect(url_for("index"))

    if skill_type not in ("hard", "soft", "language"):
        skill_type = "hard"

    if level is None:
        level = 0
    if level < 0:
        level = 0
    if level > 100:
        level = 100

    Skill.create(name, level, skill_type)
    flash("Skill agregada.", "success")
    return redirect(url_for("index"))


@app.route("/admin/skill/<int:skill_id>/edit", methods=["POST"])
@login_required
def edit_skill(skill_id):
    skill = Skill.from_id(skill_id)
    if not skill:
        flash("Skill no encontrada.", "danger")
        return redirect(url_for("index"))

    skill.name = request.form.get("name")
    skill.level = request.form.get("level", type=int)
    skill_type = request.form.get("type")  # hard / soft / language
    if skill_type in ("hard", "soft", "language"):
        skill.type = skill_type

    # sanitizar nivel
    if skill.level is None:
        skill.level = 0
    if skill.level < 0:
        skill.level = 0
    if skill.level > 100:
        skill.level = 100

    skill.update()
    flash("Skill actualizada.", "success")
    return redirect(url_for("index"))


@app.route("/admin/skill/<int:skill_id>/delete", methods=["POST"])
@login_required
def delete_skill(skill_id):
    Skill.delete(skill_id)
    flash("Skill eliminada.", "info")
    return redirect(url_for("index"))


# Proyectos

@app.route("/admin/project/add", methods=["POST"])
@login_required
def add_project():
    name = request.form.get("name")
    date_label = request.form.get("date_label")
    description = request.form.get("description")
    link = request.form.get("link")
    image = request.form.get("image") or ""  # evitar None

    if not name:
        flash("Falta el nombre del proyecto.", "danger")
        return redirect(url_for("index"))

    try:
        Project.create(name, date_label, description, link, image)
        flash("Proyecto agregado.", "success")
    except Exception as e:
        print("Error creando proyecto:", e)
        flash("Hubo un error al crear el proyecto.", "danger")

    return redirect(url_for("index"))


@app.route("/admin/project/<int:proj_id>/edit", methods=["POST"])
@login_required
def edit_project(proj_id):
    proj = Project.from_id(proj_id)
    if not proj:
        flash("Proyecto no encontrado.", "danger")
        return redirect(url_for("index"))

    try:
        proj.name = request.form.get("name")
        proj.date_label = request.form.get("date_label")
        proj.description = request.form.get("description")
        proj.link = request.form.get("link")
        proj.image = request.form.get("image") or ""  

        proj.update()
        flash("Proyecto actualizado.", "success")
    except Exception as e:
        print("Error actualizando proyecto:", e)
        flash("Hubo un error al actualizar el proyecto.", "danger")

    return redirect(url_for("index"))


@app.route("/admin/project/<int:proj_id>/delete", methods=["POST"])
@login_required
def delete_project(proj_id):
    try:
        Project.delete(proj_id)
        flash("Proyecto eliminado.", "info")
    except Exception as e:
        print("Error eliminando proyecto:", e)
        flash("Hubo un error al eliminar el proyecto.", "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
