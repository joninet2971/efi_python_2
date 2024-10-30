from flask import Blueprint, render_template, redirect, request, url_for, session, flash
from models import Proveedor, Compra, Detalle_Compra, Venta
from utils.validaciones import validarNombre
from app import db

carga_factura_compra_bp = Blueprint('carga_factura_compra', __name__)

comprobantes = ["Factura A","Factura B","Factura C"]

@carga_factura_compra_bp.route("/compra", methods=['POST', 'GET'])
def carga_factura(): 
    print('entre al primero')  
    proveedores = Proveedor.query.filter_by(activo=True).all()
    compras = Detalle_Compra.query.all()
    
    total_costo = 0
    total_cantidad = 0
    if request.method == 'POST':
        proveedor_id = request.form['proveedor']
        numero_factura = request.form['numero_factura']
        comprobante = request.form['comprobante']

        if not validarNombre(numero_factura, Compra, Compra.numero_factura):
            flash('El numero de la factura ya existe en nuestra base de datos', 'error')
            return redirect(url_for('carga_factura_compra.carga_factura'))  
      
        nueva_compra = Compra(
            tipo_comprobante=comprobante,
            numero_factura=numero_factura,
            id_proveedor=proveedor_id
        )
        db.session.add(nueva_compra)
        db.session.commit()

        # Guarda el ID de la compra en la sesión
        session['compra_id'] = nueva_compra.id

        # Redirige a la ruta donde se mostrará el detalle
        return redirect(url_for('detalle_compra.detalle_compra'))

    total_costo = sum(detalle.equipo.costo * detalle.cantidad for detalle in compras)
    total_cantidad = sum(detalle.cantidad for detalle in compras)
    return render_template('carga_factura_compra.html',
                           compras=compras, 
                           comprobantes=comprobantes, 
                           proveedores=proveedores, 
                           total_costo=total_costo, 
                           total_cantidad=total_cantidad)

