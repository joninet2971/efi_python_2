from flask import Blueprint, request, make_response, jsonify
from flask_jwt_extended import get_jwt, jwt_required

from app import db
from models import Modelo, Marca
from schemas import ModeloSchema  # Cambiamos MarcaSchema por ModeloSchema

modelo_bp = Blueprint('modelo', __name__)

@modelo_bp.route('/modelo', methods=['GET', 'POST'])
@jwt_required()
def modelo():
    data = request.get_json()
    id_marca = data.get('id_marca')
    marca = Marca.query.get_or_404(id_marca)
    
    additional_data = get_jwt()
    tipo_usuario = additional_data.get('tipo')
    administrador = additional_data.get('administrador')

    if request.method == 'POST':
        if tipo_usuario == 'crear' or administrador:
            errors = ModeloSchema().validate(data)
            if errors:
                return make_response(jsonify(errors), 400)
            
            nuevo_modelo = Modelo(
                nombre=data.get('nombre'),
                id_marca=id_marca
            )
            db.session.add(nuevo_modelo)
            db.session.commit()
            return ModeloSchema().dump(nuevo_modelo), 201
        else:
            return jsonify({"Mensaje": "Solo el admin puede crear nuevos modelos"})

    if tipo_usuario == 'visor' or administrador:
        modelos = Modelo.query.filter_by(activo=True).all()
        return jsonify(ModeloSchema(many=True).dump(modelos))

    return jsonify({"Mensaje": "El usuario no tiene permiso"})

@modelo_bp.route('/modelo/borrar', methods=['POST'])
@jwt_required()
def modelo_borrar():
    data = request.get_json()
    id_borrar = int(data.get('id'))
    modelo = Modelo.query.get_or_404(id_borrar)
    
    if modelo.activo is True:
        additional_data = get_jwt()
        tipo_usuario = additional_data.get('tipo')
        tipo_admin = additional_data.get('administrador')

        if tipo_usuario == 'borrar' or tipo_admin is True:
            
            """errors = MarcaSchema().validate(data)
            if errors:
                return make_response(jsonify(errors))"""
            modelo.activo = False
            db.session.commit()
            
            return jsonify(Mensaje= "El borrado fue exitoso",Marca=modelo.nombre)
        else:
            return jsonify(Mensaje= "Usted no tiene permiso de borrar modelo")
    else:
        return jsonify(Mensaje= "Esta marca fue borrada anteriormente", Marca=modelo.nombre)
    
@modelo_bp.route('/modelo/editar', methods=['POST'])
@jwt_required()
def modelo_editar():
    data = request.get_json()
    
    id_editar = int(data.get('id'))
    modelo = Modelo.query.get_or_404(id_editar)
    
    if modelo.activo is True:
        additional_data = get_jwt()
        tipo_usuario = additional_data.get('tipo')
        tipo_admin = additional_data.get('administrador')

        if tipo_usuario == 'editar' or tipo_admin is True:
            
            modelo.nombre = data.get('nombre', modelo.nombre)
            modelo.id_marca = data.get('id_marca', modelo.id_marca)
        
            db.session.commit()
            
            return jsonify(Mensaje="El modelo fue editado exitosamente", Modelo=modelo.nombre)
        else:
            return jsonify(Mensaje="Usted no tiene permiso de editar Modelos")
    else:
        return jsonify(Mensaje="El modelo fue borrado")
