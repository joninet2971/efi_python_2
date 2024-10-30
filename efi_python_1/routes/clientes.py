from flask import Blueprint, render_template, redirect, request, url_for
from models import Cliente
from app import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route("/clientes", methods=['POST', 'GET'])
def agregar_clientes():
    print("aca")   
    clientes = Cliente.query.filter_by(activo=True).all()
    fiscal = ['Responsable inscripto','Consumidor Final','Monotributista']
    if request.method == 'POST':
        nombre = request.form['nombre']
        contacto = request.form['contacto']
        condicion_fiscal = request.form['condicion_fiscal']
        nuevo_cliente = Cliente(nombre_cliente=nombre,condicion_fiscal=condicion_fiscal, contacto=contacto)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return redirect(url_for('clientes.agregar_clientes'))
    print("aca")
    
    return render_template('lista_clientes.html',fiscal=fiscal, clientes=clientes)

@clientes_bp.route("/cliente/<int:id>/editar", methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        cliente.nombre_cliente = request.form['nombre']
        cliente.condicion_fiscal = request.form['condicion_fiscal']
        cliente.contacto = request.form['contacto']
        db.session.commit()
        return redirect(url_for('clientes.agregar_clientes')) 

    return render_template('cliente_edit.html', cliente=cliente)

@clientes_bp.route("/cliente/<int:id>/eliminar")
def eliminar_cliente(id):
    equipo = Cliente.query.get_or_404(id)
    equipo.activo = False
    db.session.commit()
    return redirect(url_for('clientes.agregar_clientes'))