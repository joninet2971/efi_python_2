from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from models import Cliente, Venta, Detalle_Venta
from utils.validaciones import validarNombre
from app import db

carga_factura_venta_bp = Blueprint('carga_factura_venta', __name__)

comprobantes = ["Factura A","Factura B","Factura C"]

@carga_factura_venta_bp.route("/venta", methods=['POST', 'GET'])
def carga_factura(): 
    print('entre al primero')  
    clientes = Cliente.query.filter_by(activo=True).all()
    ventas = Detalle_Venta.query.all()

    total_precio_venta = 0
    total_cantidad = 0
    if request.method == 'POST':
        cliente_id = request.form['cliente']
        numero_factura = request.form['numero_factura']
        comprobante = request.form['comprobante']

        if not validarNombre(numero_factura, Venta, Venta.numero_factura):
            flash('El numero de la factura ya existe en nuestra base de datos', 'error')
            return redirect(url_for('carga_factura_venta.carga_factura'))  
      
        nueva_venta = Venta(
            tipo_comprobante=comprobante,
            numero_factura=numero_factura,
            id_cliente=cliente_id
        )
        db.session.add(nueva_venta)
        db.session.commit()

        
        # Guarda el ID de la compra en la sesión
        session['venta_id'] = nueva_venta.id

        # Redirige a la ruta donde se mostrará el detalle
        return redirect(url_for('detalle_venta.detalle_venta'))
    total_precio_venta = sum(detalle.equipo.costo * detalle.cantidad for detalle in ventas)
    total_cantidad = sum(detalle.cantidad for detalle in ventas)
    return render_template('carga_factura_venta.html',
                           ventas=ventas, 
                           comprobantes=comprobantes, 
                           clientes=clientes, 
                           total_costo=total_precio_venta, 
                           total_cantidad=total_cantidad)
