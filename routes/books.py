from flask import Blueprint, render_template, redirect, url_for, flash, request
from peewee import IntegrityError
from models import Books
from forms import LibroForm
from .auth import login_required

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route('/')
@login_required
def list_books():
    libros = Books.select()
    return render_template('libros.html', libros=libros)

@books_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_book():
    form = LibroForm()
    if form.validate_on_submit():
        try:
            Books.create(titulo=form.titulo.data)
            flash('Libro agregado correctamente', 'success')
            return redirect(url_for('books.list_books'))
        except IntegrityError:
            flash('Error: El libro ya existe.', 'danger')
            
    return render_template('create_libros.html', form=form)

@books_bp.route('/libros_agregar')
@login_required
def libros_agregar():
    return redirect(url_for('books.create_book'))

@books_bp.route('/<int:book_id>')
@login_required
def get_book(book_id):
    book = Books.get_or_none(Books.id == book_id)
    return render_template('get_libros.html', book=book)

@books_bp.route('/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Books.get_or_none(Books.id == book_id)
    if book:
        book.delete_instance()
        flash('Libro eliminado correctamente', 'success')
    else:
        flash('No se encontró el libro', 'danger')
    return redirect(url_for('books.list_books'))