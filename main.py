from app import app
from models import db, Users, Books, Material, Course, Preceptor, Shift, Retiros

def initialize_database():
    """
    Conecta a la base de datos, crea las tablas si no existen y
    asegura que exista un usuario 'admin' por defecto.
    """
    try:
        db.connect()
        TABLES = [Users, Books, Material, Course, Preceptor, Shift, Retiros]
        db.create_tables(TABLES)
        print("Tablas de la base de datos verificadas y/o creadas.")

        # Crear usuario 'admin' por defecto si no existe
        if not Users.get_or_none(Users.username == 'admin'):
            # 1. Instanciar el objeto sin guardarlo
            admin_user = Users(
                username='admin',
                nombre='Administrador',
                apellido='Principal',
                email='admin@biblioteca.local'
            )
            admin_user.set_password('admin')  # 2. Hashear y asignar la contraseña
            admin_user.save()                 # 3. Guardar el usuario en la DB
            print("Usuario 'admin' por defecto creado con contraseña 'admin'.")

    finally:
        if not db.is_closed():
            db.close()

if __name__ == '__main__':
    initialize_database()  # 👈 Se asegura de que la DB y las tablas existan
    app.run(debug=True, host="0.0.0.0", port=5000)
