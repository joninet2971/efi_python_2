from flask import Blueprint, render_template, redirect, request, url_for
from models import Modelo, Fabricante, Marca, Equipo, Detalle_Compra, Detalle_Venta
from app import db
from sqlalchemy import func
from decimal import Decimal

stock_bp = Blueprint('stock', __name__)

@stock_bp.route("/stock", methods=['GET', 'POST'])
def stock():       

     # Consulta la cantidad total de equipos comprados, incluyendo el id del equipo
    resultados_compras = db.session.query(
        Equipo.id.label('id_equipo'),
        Marca.nombre_marca,
        Modelo.nombre_modelo,
        func.sum(Detalle_Compra.cantidad).label('cantidad_total_compras'),
        Equipo.costo.label('costo_promedio')
    ).join(Detalle_Compra, Detalle_Compra.id_equipo == Equipo.id) \
    .join(Modelo, Equipo.id_modelo == Modelo.id) \
    .join(Marca, Equipo.id_marca == Marca.id) \
    .group_by(Equipo.id, Marca.nombre_marca, Modelo.nombre_modelo) \
    .all()


    # Consulta la cantidad total de equipos vendidos, incluyendo el id del equipo
    resultados_ventas = db.session.query(
        Equipo.id.label('id_equipo'),
        Marca.nombre_marca,
        Modelo.nombre_modelo,
        func.sum(Detalle_Venta.cantidad).label('cantidad_total_ventas')
    ).join(Detalle_Venta, Detalle_Venta.id_equipo == Equipo.id) \
    .join(Modelo, Equipo.id_modelo == Modelo.id) \
    .join(Marca, Equipo.id_marca == Marca.id) \
    .group_by(Equipo.id, Marca.nombre_marca, Modelo.nombre_modelo) \
    .all()

    # Convertir resultados a diccionarios para facilitar el procesamiento
    compras_dict = {
        (id_equipo, marca, modelo): (cantidad_total_compras, costo_promedio)
        for id_equipo, marca, modelo, cantidad_total_compras, costo_promedio in resultados_compras
    }

    ventas_dict = {(id_equipo, marca, modelo): cantidad_total_ventas for id_equipo, marca, modelo, cantidad_total_ventas in resultados_ventas}

    # Calcular el stock disponible y armar el diccionario final
    stock_disponible = []
    for (id_equipo, marca, modelo), (cantidad_comprada, costo_promedio) in compras_dict.items():
        cantidad_vendida = ventas_dict.get((id_equipo, marca, modelo), Decimal('0'))
        cantidad_stock = cantidad_comprada - cantidad_vendida
        stock_disponible.append({
            'id_equipo': id_equipo,
            'marca': marca,
            'modelo': modelo,
            'cantidad': int(cantidad_stock),  # Convertir a entero si es necesario
            'costo': float(costo_promedio)  # Convertir a float si es necesario
    })
        
    return render_template('stock.html',
                           stock_disponible=stock_disponible)