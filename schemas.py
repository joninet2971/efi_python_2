from app import ma

from marshmallow import validates, ValidationError

from models import User, Tipo, Marca, Vehiculo

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    password_hash = ma.auto_field()
    is_admin = ma.auto_field()

class UserMinimalSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field()

class TipoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tipo

    nombre=ma.auto_field()

class MarcaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Tipo

    nombre=ma.auto_field()

class VehiculoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Vehiculo

    id = ma.auto_field()
    modelo = ma.auto_field()
    anio_fabricacion = ma.auto_field()
    precio = ma.auto_field()
    marca_id = ma.auto_field()
    tipo_id = ma.auto_field()
    marca = ma.Nested(MarcaSchema)
    tipo = ma.Nested(TipoSchema)

    @validates('precio')
    def validate_precio(self, value):
        if int(value) > 2024:
            return ValidationError("El año es superior al actual")


