from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo

class LoginForm(FlaskForm):
    """ Login Form """
    username = StringField(
            'Nombre de Usuario',
            validators=[
                DataRequired()
            ]
    )
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Logearse')

class RegistrationForm(FlaskForm):
    password = PasswordField('Contraseña', validators=[DataRequired()])
    
    password2 = PasswordField(
        'Repetir Contraseña', 
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')]
    )
    submit = SubmitField('Registrarse')

class UsuarioForm(FlaskForm):
    username = StringField(
        'Nombre de Usuario',
        validators=[
            DataRequired(message='El nombre de usuario es requerido'),
            Length(min=3, max=20, message='El nombre de usuario debe tener entre 3 y 20 caracteres')
        ]
    )
    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message='El nombre es requerido'),
            Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
        ]
    )
    apellido = StringField(
        'Apellido',
        validators=[
            DataRequired(message='El apellido es requerido'),
            Length(min=2, max=50, message='El apellido debe tener entre 2 y 50 caracteres')
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='El email es requerido'),
            Length(min=2, max=50, message='El email no puede superar los 50 caracteres')
        ]
    )
    password = StringField(
        'Contraseña',
        validators=[
            DataRequired(message='La contraseña es requerida'),
            Length(min=2, max=50, message='La contraseña debe tener entre 2 y 50 caracteres')
        ]
    )

    libro = SelectField(
        'Libro',
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message='Selecciona un libro')
        ]
    )
    material = SelectField(
        'Materiales a Retirar',
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message='Selecciona el Material')
        ]
    )
    course = SelectField(
        'Curso del alumno',
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message='Selecciona un curso')
        ]
    )
    preceptor = SelectField(
        'Preceptor del alumno',
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message='Selecciona un preceptor')
        ]
    )
    shift = SelectField(
        'Turno del alumno',
        choices=[],
        coerce=int,
        validators=[
            DataRequired(message='Selecciona un turno')
        ]
    )

    submit = SubmitField('Crear Usuario')

class LibroForm(FlaskForm):
    titulo = StringField(
        'Nombre del libro',
        validators=[
            DataRequired(message='El título del libro es requerido'),
            Length(min=1, max=100, message='El título del libro debe tener entre 1 y 100 caracteres')
        ]
    )
    submit = SubmitField('Agregar Libro')

class MaterialForm(FlaskForm):
    nombre = StringField(
        'Material',
        validators=[
            DataRequired(message='El Material es requerido'),
            Length(min=1, max=100, message='El Material debe tener entre 1 y 100 caracteres')
        ]
    )
    submit = SubmitField('Agregar Material') 

class CourseForm(FlaskForm):
    curso = StringField(
        'Curso',
        validators=[
            DataRequired(message='El curso es requerido'),
            Length(min=1, max=100, message='El nombre del curso debe tener entre 1 y 100 caracteres')
        ]
    )
    submit = SubmitField('Guardar')

class PreceptorForm(FlaskForm):
    nombre = StringField(
        'Nombre del Preceptor',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Crear Preceptor')

class ShiftForm(FlaskForm):
    turno = StringField(
        'Nombre del Turno',
         validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Agregar Turno')