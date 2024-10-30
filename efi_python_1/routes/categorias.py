from flask import Blueprint, render_template, redirect, request, url_for, flash
from models import Categoria
from utils.validaciones import validarNombre
from app import db

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route("/categoria", methods=['POST', 'GET'])
def agregar_categoria():   
    categorias = Categoria.query.filter_by(activo=True).all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        if not validarNombre(nombre, Categoria, Categoria.nombre_categoria):
            flash('El nombre de la categoría ya existe', 'error')
            return redirect(url_for('categorias.agregar_categoria'))
        nueva_categoria = Categoria(nombre_categoria=nombre)
        db.session.add(nueva_categoria)
        db.session.commit()
        flash('Categoría agregada correctamente', 'success')
        return redirect(url_for('categorias.agregar_categoria'))
    
    return render_template('lista_categorias.html', categorias=categorias)

@categorias_bp.route("/categoria/<id>/editar", methods=['GET', 'POST'])
def categoria_editar(id):
    categoria = Categoria.query.get_or_404(id)

    if request.method == 'POST':
        categoria.nombre_categoria = request.form['nombre']
        db.session.commit()
        return redirect(url_for('categorias.agregar_categoria'))

    return render_template('categoria_edit.html', categorias=categoria)

@categorias_bp.route("/categoria/<int:id>/eliminar")
def eliminar_categoria(id):
    equipo = Categoria.query.get_or_404(id)
    equipo.activo = False
    db.session.commit()
    return redirect(url_for('categorias.agregar_categoria'))