from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Ingresar")


class AboutForm(FlaskForm):
    full_name = StringField("Nombre completo", validators=[DataRequired(), Length(max=100)])
    title = StringField("Título", validators=[DataRequired(), Length(max=100)])
    summary = TextAreaField("Resumen profesional", validators=[DataRequired()])
    email = StringField("Email", validators=[Email()])
    phone = StringField("Teléfono")
    address = StringField("Dirección")
    profile_image = StringField("Ruta imagen (archivo o URL)")
    submit = SubmitField("Guardar cambios")
