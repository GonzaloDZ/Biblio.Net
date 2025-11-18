from models import db, Users, Books, Material, Course, Preceptor, Shift, Retiros

def create_tables():
    """
    Crea todas las tablas de la base de datos si no existen.
    """
    # Lista de todos los modelos que deben convertirse en tablas.
    TABLES = [Users, Books, Material, Course, Preceptor, Shift, Retiros]
    
    print("Conectando a la base de datos...")
    db.connect()
    print("Creando tablas...")
    db.create_tables(TABLES)
    print("Tablas creadas exitosamente: ", [table.__name__ for table in TABLES])
    db.close()

if __name__ == '__main__':
    create_tables()