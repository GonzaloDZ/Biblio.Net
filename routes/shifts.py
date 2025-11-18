from flask import Blueprint, render_template, redirect, url_for, flash, request
from .auth import login_required
from forms import ShiftForm
from models import Shift
from peewee import IntegrityError

shifts_bp = Blueprint('shifts', __name__, url_prefix='/shifts')

@shifts_bp.route('/')
@login_required
def list_shifts():
    turnos = Shift.select()
    return render_template('shift.html', turnos=turnos)

@shifts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_shift():
    form = ShiftForm()
    if form.validate_on_submit():
        try:
            Shift.create(turno=form.turno.data)
            flash('Turno agregado correctamente', 'success')
            return redirect(url_for('shifts.list_shifts'))
        except IntegrityError:
            flash('Error: El turno ya existe.', 'danger')
    return render_template('create_shift.html', form=form)


@shifts_bp.route('/<int:shift_id>')
@login_required
def get_shift(shift_id):
    turno = Shift.get_or_none(Shift.id == shift_id)
    return render_template('get_shift.html', shift=turno)

@shifts_bp.route('/delete/<int:shift_id>', methods=['POST'])
@login_required
def delete_shift(shift_id):
    turno = Shift.get_or_none(Shift.id == shift_id)
    if turno:
        turno.delete_instance()
        flash('Turno eliminado correctamente', 'success')
    else:
        flash('No se encontró el turno', 'danger')
    return redirect(url_for('shifts.list_shifts'))