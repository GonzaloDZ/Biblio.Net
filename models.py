from peewee import Model, CharField, SqliteDatabase, ForeignKeyField, DateTimeField, BooleanField
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

db = SqliteDatabase('biblioteca.db')

class BaseModel(Model):

    class Meta:
        database = db

class Users(BaseModel):
    username = CharField(unique=True)
    nombre = CharField()
    apellido = CharField()
    email = CharField()
    password_hash = CharField()
    is_active = BooleanField(default=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Genera y guarda el hash de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña contra el hash almacenado."""
        return check_password_hash(self.password_hash, password)


class Books(BaseModel):
    titulo = CharField(unique=True)

    def __repr__(self):
        return f'<Book {self.titulo}>'

class Material(BaseModel):
    nombre = CharField(unique=True)

    def __repr__(self):
        return f'<Material {self.nombre}>'

class Course(BaseModel):
    curso = CharField(unique=True)

    def __repr__(self):
        return f'<Course {self.curso}>'

class Preceptor(BaseModel):
    nombre = CharField(unique=True)

    def __repr__(self):
        return f'<Preceptor {self.nombre}>'

class Shift(BaseModel):
    turno = CharField(unique=True)

    def __repr__(self):
        return f'<Shift {self.turno}>'

class Retiros(BaseModel):
    users = ForeignKeyField(Users)
    books = ForeignKeyField(Books)

    material = ForeignKeyField(Material, null=True)
    course = ForeignKeyField(Course, null=True)
    preceptor = ForeignKeyField(Preceptor, null=True)
    shift = ForeignKeyField(Shift, null=True)

    fecha_devolucion = DateTimeField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(null=True)
    is_active = BooleanField(default=True)  # 🔹 nuevo campo para soft delete