from .auth_views import auth_bp
from .marca_view import marca_bp
from .modelo_view import modelo_bp



def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(marca_bp)
    app.register_blueprint(modelo_bp)


