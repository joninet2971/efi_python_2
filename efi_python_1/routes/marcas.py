from flask import Blueprint, render_template, redirect, request, url_for, flash
from models import Marca
from utils.validaciones import validarNombre
from app import db

marcas_bp = Blueprint('marcas', __name__)

@marcas_bp.route("/marcas", methods=['POST', 'GET'])
def agregar_marcas():   
    marcas = Marca.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        nueva_marca = Marca(nombre_marca=nombre)
        if not validarNombre(nombre, Marca, Marca.nombre_marca):
            flash('El nombre ya existe en nuestra base de datos','error')
            return redirect(url_for('marcas.agregar_marcas'))

        db.session.add(nueva_marca)
        db.session.commit()
        flash('El Ingreso fue exitoso','success')
        return redirect(url_for('marcas.agregar_marcas'))
    
    return render_template('lista_marcas.html', marcas=marcas)

@marcas_bp.route("/marca/<id>/editar", methods=['GET', 'POST'])
def marca_editar(id):
    marca = Marca.query.get_or_404(id)

    if request.method == 'POST':
        marca.nombre_marca = request.form['nombre']
        db.session.commit()
        return redirect(url_for('marcas.agregar_marcas'))

    return render_template('marca_edit.html', marca=marca)

@marcas_bp.route("/marca/<int:id>/eliminar")
def eliminar_marca(id):
    equipo = Marca.query.get_or_404(id)
    equipo.activo = False
    db.session.commit()
    return redirect(url_for('marcas.agregar_marcas'))