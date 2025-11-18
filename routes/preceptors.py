from flask import Blueprint, render_template, redirect, url_for, flash, request
from .auth import login_required
from forms import PreceptorForm
from models import Preceptor
from peewee import IntegrityError

preceptors_bp = Blueprint('preceptors', __name__, url_prefix='/preceptors')

@preceptors_bp.route('/')
@login_required
def list_preceptors():
    preceptores = Preceptor.select()
    return render_template('preceptors.html', preceptores=preceptores)

@preceptors_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_preceptor():
    form = PreceptorForm()
    if form.validate_on_submit():
        try:
            Preceptor.create(nombre=form.nombre.data)
            flash('Preceptor agregado correctamente', 'success')
            return redirect(url_for('preceptors.list_preceptors'))
        except IntegrityError:
            flash('Error: El preceptor ya existe.', 'danger')
    return render_template('create_preceptor.html', form=form)

@preceptors_bp.route('/<int:preceptor_id>')
@login_required
def get_preceptor(preceptor_id):
    preceptor = Preceptor.get_or_none(Preceptor.id == preceptor_id)
    return render_template('get_preceptor.html', preceptor=preceptor)

@preceptors_bp.route('/delete/<int:preceptor_id>', methods=['POST'])
@login_required
def delete_preceptor(preceptor_id):
    preceptor = Preceptor.get_or_none(Preceptor.id == preceptor_id)
    if preceptor:
        preceptor.delete_instance()
        flash('Preceptor eliminado correctamente', 'success')
    else:
        flash('No se encontró el preceptor', 'danger')
    return redirect(url_for('preceptors.list_preceptors'))