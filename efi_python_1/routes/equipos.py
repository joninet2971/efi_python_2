from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from models import Equipo, Categoria, Marca, Modelo

from app import db

equipos_bp = Blueprint('equipos', __name__)

@equipos_bp.route("/equipos", methods=['GET', 'POST'])
def equipos():
    equipos = Equipo.query.filter_by(activo=True).all()
    
    categorias = Categoria.query.filter_by(activo=True).all()
    marcas = Marca.query.filter_by(activo=True).all()
    modelos = Modelo.query.filter_by(activo=True).all()

    caracteristicas = {
        'colores': [
            'Gris',
            'Azul',
            'Negro',
            'Blanco',
            'Rojo',
            'Verde',
            'Rosa',
            'Amarillo'
        ],
        'tamanos_pantalla': [
            '5.0 pulgadas',
            '5.5 pulgadas',
            '6.0 pulgadas',
            '6.5 pulgadas',
            '7.0 pulgadas'
        ],
        'memoria': [
            '16 GB',
            '32 GB',
            '64 GB',
            '128 GB',
            '256 GB',
            '512 GB'
        ],
        'camara_delantera': [
            '8 MP',
            '12 MP',
            '16 MP',
            '20 MP',
            '32 MP'
        ],
        'camara_trasera': [
            '12 MP',
            '48 MP',
            '64 MP',
            '108 MP',
            '50 MP + 12 MP (dual)'
        ],
        'capacidad_bateria': [
            '3000 mAh',
            '4000 mAh',
            '5000 mAh',
            '6000 mAh'
        ]
    }

    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        costo = float(request.form['costo'])
        descripcion = request.form['descripcion']
        color = request.form.get('color')
        tamano_pantalla = request.form.get('tamano_pantalla')
        memoria = request.form.get('memoria')
        camara_delantera = request.form.get('camara_delantera')
        camara_trasera = request.form.get('camara_trasera')
        capacidad_bateria = request.form.get('capacidad_bateria')

        nuevo_equipo = Equipo(
            id_marca=marca,
            id_modelo=modelo,
            costo=costo,
            descripcion=descripcion,
            color=color,
            tamano_pantalla=tamano_pantalla,
            memoria=memoria,
            camara_delantera=camara_delantera,
            camara_trasera=camara_trasera,
            capacidad_bateria=capacidad_bateria,

        )


        db.session.add(nuevo_equipo)
        db.session.commit()

        return redirect(url_for('equipos.equipos'))
   
    return render_template(
        'equipos.html',
        equipos=equipos,
        modelos=modelos,
        categorias=categorias,
        marcas=marcas,
        caracteristicas=caracteristicas
    )

@equipos_bp.route("/equipo/<id>/editar", methods=['GET', 'POST'])
def equipo_editar(id):
    equipo = Equipo.query.get_or_404(id)

    categorias = Categoria.query.all()
    marcas = Marca.query.all()
    modelos = Modelo.query.all()

    if request.method == 'POST':
        equipo.id_marca = request.form['marca']
        equipo.id_modelo = request.form['modelo']
        equipo.id_categoria = request.form['categoria']
        equipo.costo = request.form['costo']
        equipo.descripcion = request.form['descripcion']
        db.session.commit()
        return redirect(url_for('equipos.equipos'))

    return render_template('equipos_edit.html', 
        equipo=equipo,
        categorias=categorias, 
        marcas=marcas,
        modelos=modelos)

@equipos_bp.route("/equipo/<id>/eliminar", methods=['GET', 'POST'])
def eliminar_equipo(id):
    equipo = Equipo.query.get_or_404(id)
    equipo.activo = False
    db.session.commit()
    return redirect(url_for('equipos.equipos'))


@equipos_bp.route("/modelos/<marca_id>")
def get_modelos(marca_id):
    modelos = Modelo.query.filter_by(id_marca=marca_id, activo=True).all()
    modelos_data = [{'id': modelo.id, 'nombre_modelo': modelo.nombre_modelo} for modelo in modelos]
    print(modelos_data)  # Añade esta línea para depurar
    return jsonify(modelos_data)