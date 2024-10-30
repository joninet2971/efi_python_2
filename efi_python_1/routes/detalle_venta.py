from flask import Blueprint,flash, render_template, redirect, request, url_for, session
from models import Marca, Venta, Modelo, Equipo, Detalle_Compra, Detalle_Venta
from app import db
from sqlalchemy import func
from decimal import Decimal

detalle_venta_bp = Blueprint('detalle_venta', __name__)

@detalle_venta_bp.route("/detalle_venta", methods=['POST', 'GET'])
def detalle_venta(): 
    venta_id = session.get('venta_id')
    venta_seleccionada = Venta.query.get(venta_id)

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
        
        
   
    if request.method == 'POST':
        
        equipo_seleccionado = request.form['equipo']
        id_equipo, cantidad_elegida = equipo_seleccionado.split('|')

        equipo_id = int(id_equipo)
        cantidad = int(request.form['cantidad'])
        precio_final = float(request.form['precio_final'])

        if cantidad <= int(cantidad_elegida):
            nueva_venta = Detalle_Venta(
                id_venta=venta_seleccionada.id,
                id_equipo=equipo_id,
                precio=precio_final,
                cantidad=cantidad
            )
            db.session.add(nueva_venta)
            db.session.commit()
        else:
            flash("Cantidad solicitada es mayor que la disponible, cargar nuevamente", "error")

        # Redirigir a la misma página para evitar reenvíos del formulario
        return redirect(url_for('detalle_venta.detalle_venta'))
    
    detalle_completo = Detalle_Venta.query.filter_by(id_venta=venta_seleccionada.id).all()

    total_costo = sum(detalle.precio * detalle.cantidad for detalle in detalle_completo)
    total_cantidad = sum(detalle.cantidad for detalle in detalle_completo)

    

    return render_template('detalle_venta.html',
                           total_costo=total_costo, 
                           total_cantidad=total_cantidad,
                           stock_disponible=stock_disponible,
                           detalle_completo=detalle_completo, 
                           venta_seleccionada=venta_seleccionada)
