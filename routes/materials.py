from flask import Blueprint, render_template, redirect, url_for, flash, request
from .auth import login_required
from forms import MaterialForm
from models import Material
from peewee import IntegrityError

materials_bp = Blueprint('materials', __name__, url_prefix='/materials')

@materials_bp.route('/')
@login_required
def list_materials():
    materiales = Material.select()
    return render_template('material.html', materiales=materiales)

@materials_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_material():
    form = MaterialForm()
    if form.validate_on_submit():
        try:
            Material.create(nombre=form.nombre.data)
            flash('Material agregado correctamente', 'success')
            return redirect(url_for('materials.list_materials'))
        except IntegrityError:
            flash('Error: El material ya existe.', 'danger')
    return render_template('create_materiales.html', form=form)

@materials_bp.route('/<int:material_id>')
@login_required
def get_material(material_id):
    material = Material.get_or_none(Material.id == material_id)
    return render_template('get_material.html', material=material)

@materials_bp.route('/delete/<int:material_id>', methods=['POST'])
@login_required
def delete_material(material_id):
    material = Material.get_or_none(Material.id == material_id)
    if material:
        material.delete_instance()
        flash('Material eliminado correctamente', 'success')
    else:
        flash('No se encontró el material', 'danger')
    return redirect(url_for('materials.list_materials'))