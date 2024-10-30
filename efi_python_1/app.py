from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/equipos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'python'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from routes.equipos import equipos_bp
from routes.stock import stock_bp
from routes.categorias import categorias_bp
from routes.proveedores import proveedores_bp
from routes.marcas import marcas_bp
from routes.fabricantes import fabricantes_bp
from routes.modelos import modelos_bp
from routes.index import index_bp
from routes.clientes import clientes_bp
from routes.carga_factura_compra import carga_factura_compra_bp  
from routes.carga_factura_venta import carga_factura_venta_bp  
from routes.detalle_compra import detalle_compra_bp 
from routes.detalle_venta import detalle_venta_bp 


app.register_blueprint(equipos_bp)
app.register_blueprint(stock_bp)
app.register_blueprint(categorias_bp)
app.register_blueprint(proveedores_bp)
app.register_blueprint(marcas_bp)
app.register_blueprint(fabricantes_bp)
app.register_blueprint(modelos_bp)
app.register_blueprint(index_bp)
app.register_blueprint(clientes_bp)
app.register_blueprint(carga_factura_compra_bp)
app.register_blueprint(detalle_compra_bp)
app.register_blueprint(carga_factura_venta_bp)
app.register_blueprint(detalle_venta_bp)

@app.route("/")
def index():
    return redirect(url_for('index.buscar'))

if __name__ == "__main__":
    app.run(debug=True)