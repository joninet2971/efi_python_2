from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func

def validarNombre(nombre, model, campo):
    try:
        existe = model.query.filter(func.lower(campo) == func.lower(nombre)).one_or_none()
        if existe:
            return False
        return True
    except NoResultFound:
        return True