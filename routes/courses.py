from flask import Blueprint, render_template, redirect, url_for, flash, request
from .auth import login_required
from forms import CourseForm
from models import Course
from peewee import IntegrityError

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/')
@login_required
def list_courses():
    cursos = Course.select()
    return render_template('courses.html', cursos=cursos)

@courses_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        try:
            Course.create(curso=form.curso.data)
            flash('Curso agregado correctamente', 'success')
            return redirect(url_for('courses.list_courses'))
        except IntegrityError:
            flash('Error: El curso ya existe.', 'danger')
    return render_template('create_course.html', form=form)

@courses_bp.route('/<int:course_id>')
@login_required
def get_course(course_id):
    curso = Course.get_or_none(Course.id == course_id)
    return render_template('get_course.html', course=curso)

@courses_bp.route('/delete/<int:course_id>', methods=['POST'])
@login_required
def delete_course(course_id):
    curso = Course.get_or_none(Course.id == course_id)
    if curso:
        curso.delete_instance()
        flash('Curso eliminado correctamente', 'success')
    else:
        flash('No se encontró el curso', 'danger')
    return redirect(url_for('courses.list_courses'))