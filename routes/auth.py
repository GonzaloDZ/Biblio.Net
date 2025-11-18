from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import Users
from forms import LoginForm

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """ Decorador para requerir inicio de sesión en una ruta. """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET'])
def login():
    """ Muestra el formulario de login. """
    return render_template("login.html", form=LoginForm())

@auth_bp.route('/login', methods=['POST'])
def post_login():
    """ Autentica al usuario. """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Users.get_or_none(Users.username == form.username.data, Users.is_active == True)

        if user and user.check_password(form.password.data):
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect(url_for('main.index'))


    return render_template("login.html", form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """ Cierra la sesión del usuario. """
    session.pop('username', None)
    session.pop('user_id', None)

    return redirect(url_for('auth.login'))