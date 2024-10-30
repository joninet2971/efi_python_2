from flask import Blueprint, render_template, redirect, request, url_for
from models import Proveedor
from app import db

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route("/proveedores", methods=['POST', 'GET'])
def agregar_proveedores():   
    
    proveedores = Proveedor.query.filter_by(activo=True).all()
    fiscal = ['Responsable inscripto','Exento','Monotributista']
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        condicion_fiscal = request.form['condicion_fiscal']
        nuevo_proveedor = Proveedor(nombre_proveedor=nombre,condicion_fiscal=condicion_fiscal, contacto=contacto)
        db.session.add(nuevo_proveedor)
        db.session.commit()
        return redirect(url_for('proveedores.agregar_proveedores'))
    
    return render_template('lista_proveedores.html', fiscal=fiscal,proveedores=proveedores)

@proveedores_bp.route("/proveedor/<int:id>/editar", methods=['GET', 'POST'])
def proveedor_editar(id):
    proveedor = Proveedor.query.get_or_404(id)

    if request.method == 'POST':
        proveedor.nombre_proveedor = request.form['nombre']
        proveedor.condicion_fiscal = request.form['condicion_fiscal']
        proveedor.contacto = request.form['contacto']
        db.session.commit()
        return redirect(url_for('proveedores.agregar_proveedores'))  # Ajusta la ruta de redirección según corresponda

    return render_template('proveedor_edit.html', proveedor=proveedor)

@proveedores_bp.route("/proveedor/<int:id>/eliminar")
def eliminar_proveedor(id):
    equipo = Proveedor.query.get_or_404(id)
    equipo.activo = False
    db.session.commit()
    return redirect(url_for('proveedores.agregar_proveedores'))