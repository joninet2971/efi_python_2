from app import db


class Fabricante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_fabricante = db.Column(db.String(255), nullable=False ,unique=True)
    pais_origen = db.Column(db.String(255), nullable=False ,unique=True)

    activo = db.Column(db.Boolean, default=True, nullable=False)

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_marca = db.Column(db.String(255), nullable=False, unique=True)

    activo = db.Column(db.Boolean, default=True, nullable=False)

class Modelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_modelo = db.Column(db.String(255), nullable=False, unique=True)
    id_fabricante = db.Column(db.Integer, db.ForeignKey('fabricante.id'), nullable=False)
    id_marca = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

    activo = db.Column(db.Boolean, default=True, nullable=False)

    fabricante = db.relationship('Fabricante', backref=db.backref('modelos', lazy=True))
    marca = db.relationship('Marca', backref=db.backref('modelos', lazy=True))
    categoria = db.relationship('Categoria', backref=db.backref('modelos', lazy=True))


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(255), nullable=False ,unique=True)

    activo = db.Column(db.Boolean, default=True, nullable=False)

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_marca = db.Column(db.Integer, db.ForeignKey('marca.id'), nullable=False)
    id_modelo = db.Column(db.Integer, db.ForeignKey('modelo.id'), nullable=False)
    costo = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    color = db.Column(db.String(50), nullable=False) 
    tamano_pantalla = db.Column(db.String(50), nullable=False)  
    memoria = db.Column(db.String(50), nullable=False) 
    camara_delantera = db.Column(db.String(50), nullable=False)  
    camara_trasera = db.Column(db.String(50), nullable=False)  
    capacidad_bateria = db.Column(db.String(50), nullable=False) 
    
    marca = db.relationship('Marca', backref=db.backref('equipos', lazy=True))
    modelo = db.relationship('Modelo', backref=db.backref('equipos', lazy=True))

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_proveedor = db.Column(db.String(255), nullable=False, unique=True)
    condicion_fiscal = db.Column(db.String(255), nullable=False)
    contacto = db.Column(db.String(255), nullable=False)

    activo = db.Column(db.Boolean, default=True, nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(255), nullable=False, unique=True)
    condicion_fiscal = db.Column(db.String(255), nullable=False)
    contacto = db.Column(db.String(255), nullable=False)

    activo = db.Column(db.Boolean, default=True, nullable=False)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_comprobante = db.Column(db.String(255), nullable=False)
    numero_factura = db.Column(db.String(255), nullable=False, unique=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    
    proveedor = db.relationship('Proveedor', backref=db.backref('compras', lazy=True))

class Detalle_Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1, nullable=False)

    equipo = db.relationship('Equipo', backref=db.backref('detalles_compra', lazy=True))
    compra = db.relationship('Compra', backref=db.backref('detalles_compra', lazy=True))

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_comprobante = db.Column(db.String(255), nullable=False)
    numero_factura = db.Column(db.String(255), nullable=False, unique=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    
    cliente = db.relationship('Cliente', backref=db.backref('ventas', lazy=True))

class Detalle_Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipo.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1, nullable=False) 
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    
    equipo = db.relationship('Equipo', backref=db.backref('detalles_venta', lazy=True))
    venta = db.relationship('Venta', backref=db.backref('detalles_venta', lazy=True))

