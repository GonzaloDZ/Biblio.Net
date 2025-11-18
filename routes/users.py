from flask import Blueprint, render_template, request, redirect, url_for, flash
from peewee import IntegrityError
from datetime import datetime, timedelta

from models import Users, Books, Material, Course, Preceptor, Shift, Retiros
from forms import UsuarioForm
from .auth import login_required # Esta ya es correcta si auth.py está en /routes

users_bp = Blueprint('users', __name__, url_prefix='/users')

# -----------------------------------------------------------------------------
# Rutas de Usuarios
# -----------------------------------------------------------------------------

@users_bp.route('/')
@login_required
def list_users():
    usuarios = Users.select().where(Users.is_active == True)
    return render_template('list_users.html', usuarios=usuarios)

@users_bp.route('/create', methods=['GET', 'POST'])
@login_required
def users_create():
    form = UsuarioForm()

    # --- Cargar Opciones Dinámicas ---
    libros = Books.select()
    form.libro.choices = [(0, '--- Selecciona un Libro ---')] + [(libro.id, libro.titulo) for libro in libros]

    materiales = Material.select()
    form.material.choices = [(0, '--- Selecciona el Material ---')] + [(m.id, m.nombre) for m in materiales]

    cursos = Course.select()
    form.course.choices = [(0, '--- Selecciona un Curso ---')] + [(c.id, c.curso) for c in cursos]

    preceptores = Preceptor.select()
    form.preceptor.choices = [(0, '--- Selecciona un Preceptor ---')] + [(p.id, p.nombre) for p in preceptores]

    turnos = Shift.select()
    form.shift.choices = [(0, '--- Selecciona un Turno ---')] + [(t.id, t.turno) for t in turnos]
        
    if form.validate_on_submit(): 
        try:
            # 1. Crear el USUARIO
            usuario = Users(
                username=form.username.data,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                email=form.email.data,
            )
            usuario.set_password(form.password.data)
            usuario.save()

            # 2. Preparar fechas para el RETIRO
            fecha_actual = datetime.now()
            fecha_devolucion = fecha_actual + timedelta(weeks=2)

            # 3. Crear el RETIRO
            Retiros.create(
                users=usuario, 
                books=form.libro.data,
                material=form.material.data,
                course=form.course.data,
                preceptor=form.preceptor.data,
                shift=form.shift.data,
                fecha_devolucion=fecha_devolucion,
                created_at=fecha_actual
            )

            flash('Usuario y retiro creados correctamente', 'success')
            return redirect(url_for('main.index'))

        except IntegrityError as e:
            if 'users.username' in str(e):
                flash('El nombre de usuario ya existe. Elija otro.', 'warning')
            else:
                flash(f'Error al crear el usuario (datos duplicados o error de DB).', 'danger')
            
    return render_template('get_users.html', form=form)

@users_bp.route('/<int:user_id>')
@login_required
def get_user(user_id):
    user = Users.get_or_none(Users.id == user_id)
    return render_template('get_user.html', user=user)

@users_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = Users.get_or_none(Users.id == user_id)
    if user:
        user.is_active = False 
        user.save()
        flash('Usuario marcado como inactivo', 'success')
    else:
        flash('No se encontró el usuario', 'danger')
        
    return redirect(url_for('users.list_users'))