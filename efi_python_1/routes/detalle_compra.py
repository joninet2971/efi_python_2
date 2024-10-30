from flask import Blueprint, render_template, redirect, request, url_for, session
from models import Proveedor, Compra, Equipo, Marca, Detalle_Compra
from app import db

detalle_compra_bp = Blueprint('detalle_compra', __name__)

@detalle_compra_bp.route("/detalle_compra", methods=['POST', 'GET'])
def detalle_compra(): 
    # Obtén el ID de la compra de la sesión
    compra_id = session.get('compra_id')

    if not compra_id:
        return redirect(url_for('carga_factura_compra.carga_factura'))

    compra_seleccionada = Compra.query.get(compra_id)
    equipos = Equipo.query.filter_by(activo=True).all()

    if request.method == 'POST':
        equipo = request.form['equipo']
        cantidad = request.form['cantidad']
      
        nueva_compra = Detalle_Compra(
            id_compra=compra_seleccionada.id,
            id_equipo=equipo,
            cantidad=cantidad
        )
        db.session.add(nueva_compra)
        db.session.commit()

    # Obtener el detalle de la compra
    detalle_completo = Detalle_Compra.query.filter_by(id_compra=compra_seleccionada.id).all()

    # Calcular los totales
    total_costo = sum(detalle.equipo.costo * detalle.cantidad for detalle in detalle_completo)
    total_cantidad = sum(detalle.cantidad for detalle in detalle_completo)

    return render_template('detalle_compra.html', 
                           detalle_completo=detalle_completo, 
                           equipos=equipos, 
                           compra_seleccionada=compra_seleccionada, 
                           total_costo=total_costo, 
                           total_cantidad=total_cantidad)
