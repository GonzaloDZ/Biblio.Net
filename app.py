from flask import Flask
from models import db

# Importar Blueprints
from routes.main_routes import main_bp
from routes.auth import auth_bp
from routes.users import users_bp
from routes.books import books_bp
from routes.materials import materials_bp
from routes.courses import courses_bp
from routes.preceptors import preceptors_bp
from routes.shifts import shifts_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Registrar Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(books_bp)
app.register_blueprint(materials_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(preceptors_bp)
app.register_blueprint(shifts_bp)

# -----------------------------------------------------------------------------
# Database setup and cleanup (Hooks de Peewee/Flask)
# -----------------------------------------------------------------------------
@app.before_request
def _db_connect():
    """Conecta la base de datos antes de cada solicitud."""
    if db.is_closed():
        db.connect()
    # 💡 Nota: Puedes iniciar una transacción aquí si quieres manejar la unidad de trabajo

@app.teardown_request
def _db_close(exc):
    """Cierra la base de datos después de cada solicitud."""
    if not db.is_closed():
        db.close()