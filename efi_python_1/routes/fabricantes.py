from flask import Blueprint, render_template, redirect, request, url_for, flash
from models import Fabricante
from utils.validaciones import validarNombre
from app import db

fabricantes_bp = Blueprint('fabricantes', __name__)

@fabricantes_bp.route("/fabricantes", methods=['POST', 'GET'])
def agregar_fabricante():   
    fabricantes = Fabricante.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre_fabricante = request.form['nombre_fabricante']
        pais_origen = request.form['pais_origen']
        nuevo_fabricante = Fabricante(nombre_fabricante=nombre_fabricante, pais_origen=pais_origen)
        if not validarNombre(nombre_fabricante, Fabricante, Fabricante.nombre_fabricante):
            flash('El nombre ya existe en la base de datos', 'error')
            return redirect(url_for('fabricantes.agregar_fabricante'))
        db.session.add(nuevo_fabricante)
        db.session.commit()
        flash('Fabricante agregado correctamente', 'success')
        return redirect(url_for('fabricantes.agregar_fabricante'))

    return render_template('lista_fabricantes.html', fabricantes=fabricantes)

@fabricantes_bp.route("/fabricante/<id>/editar", methods=['GET', 'POST'])
def fabricante_editar(id):
    fabricante = Fabricante.query.get_or_404(id)

    if request.method == 'POST':
        fabricante.nombre_fabricante = request.form['nombre']
        fabricante.pais_origen = request.form['pais']
        db.session.commit()
        return redirect(url_for('fabricantes.agregar_fabricante'))

    return render_template('fabricante_edit.html', fabricante=fabricante)

@fabricantes_bp.route("/fabricante/<int:id>/eliminar")
def eliminar_fabricante(id):
    equipo = Fabricante.query.get_or_404(id)
    equipo.activo = False
    db.session.commit()
    return redirect(url_for('fabricantes.agregar_fabricante'))