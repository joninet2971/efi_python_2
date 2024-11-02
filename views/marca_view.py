from flask import Blueprint, request, make_response, jsonify

from flask_jwt_extended import (
    get_jwt,
    jwt_required,
)

from app import db
from models import Marca


from schemas import MarcaSchema

marca_bp = Blueprint('marca', __name__)

@marca_bp.route('/marca', methods=['GET','POST'])
@jwt_required()
def marca():
    additional_data = get_jwt()
    tipo_usuario = additional_data.get('tipo')
    administrador = additional_data.get('administrador')
    marca = Marca.query.filter_by(activo=True).all()

    if request.method == 'POST':
        if tipo_usuario=='crear' or administrador is True:
            data = request.get_json()
            errors = MarcaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors))
            
            nueva_marca = Marca(
                nombre=data.get('nombre'),
            )
            db.session.add(nueva_marca)
            db.session.commit()
            return MarcaSchema().dump(nueva_marca)
        else:
            return jsonify(Mensaje= "Solo el admin puede crear nuevas marcas")
    if tipo_usuario=='visor' or administrador is True:
        return MarcaSchema().dump(marca, many=True)
    return jsonify(Mensaje="El usuario no tiene permiso")

@marca_bp.route('/marca/borrar', methods=['POST'])
@jwt_required()
def marca_borrar():
    data = request.get_json()
    id_borrar = int(data.get('id'))
    marca = Marca.query.get_or_404(id_borrar)
    
    if marca.activo is True:
        additional_data = get_jwt()
        tipo_usuario = additional_data.get('tipo')
        tipo_admin = additional_data.get('administrador')

        if tipo_usuario == 'borrar' or tipo_admin is True:
            
            
            """errors = MarcaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors))"""
            marca.activo = False
            db.session.commit()
            
            return jsonify(Mensaje= "El borrado fue exitoso",Marca=marca.nombre)
        else:
            return jsonify(Mensaje= "Usted no tiene permiso de borrar marca")
    else:
        return jsonify(Mensaje= "Esta marca fue borrada anteriormente", Marca=marca.nombre)
    
@marca_bp.route('/marca/editar', methods=['POST'])
@jwt_required()
def marca_editar():
    data = request.get_json()
    id_editar = int(data.get('id'))
    nombre_editar = data.get('nombre')
    marca = Marca.query.get_or_404(id_editar)
    
    if marca.activo is True:
        additional_data = get_jwt()
        tipo_usuario = additional_data.get('tipo')
        tipo_admin = additional_data.get('administrador')

        if tipo_usuario == 'editar' or tipo_admin is True:
            
            
            """errors = MarcaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors))"""
            marca.nombre = nombre_editar
            db.session.commit()
            
            return jsonify(Mensaje= "La marca fue editada extosamente",Marca=marca.nombre)
        else:
            return jsonify(Mensaje= "Usted no tiene permiso de editar marca")
    else:
        return jsonify(Mensaje= "Esta marca fue borrada")
     



