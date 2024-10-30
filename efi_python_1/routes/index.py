from flask import Blueprint, render_template, redirect, request, url_for
from models import Equipo, Categoria, Marca, Modelo
from app import db

index_bp = Blueprint('index', __name__)

@index_bp.route("/buscar", methods=['GET', 'POST'])
def buscar():
    query = request.form.get('query', '')
    equipos = []
    if query:
        equipos = Equipo.query.join(Modelo).join(Marca).filter(
            # Inicia la consulta en la tabla Equipo y realiza joins con Modelo y Marca
            # Esto permite buscar en campos de las tres tablas

            (Equipo.descripcion.ilike(f'%{query}%')) |
            # Busca el término 'query' en el campo 'descripcion' de Equipo
            # ilike: búsqueda case-insensitive (ignora mayúsculas/minúsculas)
            # %: comodín que representa cualquier número de caracteres
            # | : operador OR en SQLAlchemy

            (Equipo.costo.ilike(f'%{query}%')) |
            # Busca 'query' en el campo 'costo' de Equipo
            # Nota: Usar ilike con un campo numérico no es óptimo
            # Sería mejor convertir 'query' a número y usar comparación numérica

            (Modelo.nombre_modelo.ilike(f'%{query}%')) |
            # Busca 'query' en el campo 'nombre_modelo' de la tabla Modelo

            (Marca.nombre_marca.ilike(f'%{query}%'))
            # Busca 'query' en el campo 'nombre_marca' de la tabla Marca

        ).all()
        # Ejecuta la consulta y devuelve todos los resultados que cumplen
        # con al menos uno de los criterios de búsqueda

    return render_template(
        'buscar.html',
        equipos=equipos,
        query=query
    )