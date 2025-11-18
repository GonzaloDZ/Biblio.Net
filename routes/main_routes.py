from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import Retiros, Users, Books
from .auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    """ Página principal que muestra los retiros activos. """
    retiros = (Retiros
                .select(Retiros, Users, Books)
                .join(Users)
                .switch(Retiros)
                .join(Books) 
                .where(Retiros.is_active == True))
    return render_template('retiros.html', retiros=retiros)

@main_bp.route('/retiros/devolver/<int:retiro_id>', methods=['POST'])
@login_required
def devolver(retiro_id):
    """ Marca un libro como devuelto (soft delete). """
    retiro = Retiros.get_or_none(Retiros.id == retiro_id)
    if retiro:
        retiro.is_active = False
        retiro.save()
        flash('Libro devuelto correctamente', 'success')
    else:
        flash('No se encontró el retiro', 'danger')
    return redirect(url_for('main.index'))

@main_bp.route('/search')
@login_required
def search():
    """ Busca retiros por usuario o libro. """
    query = request.args.get('q', '').strip()
    if not query:
        flash('Por favor, escribe algo para buscar.', 'warning')
        return redirect(url_for('main.index'))

    retiros = (Retiros.select(Retiros, Users, Books)
               .join(Users).switch(Retiros).join(Books)
               .where(
                   (Users.nombre.contains(query)) |
                   (Users.apellido.contains(query)) |
                   (Users.username.contains(query)) |
                   (Books.titulo.contains(query))
               ).where(Retiros.is_active == True))

    flash(f'Mostrando resultados para "{query}".', 'info')
    return render_template('retiros.html', retiros=retiros, query=query)

@main_bp.route('/contacto')
@login_required
def contacto():
    """ Muestra la página de contacto. """
    return render_template('contactos.html')