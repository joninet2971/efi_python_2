from .auth_views import auth_bp
from .vehiculos_view import vehiculo_bp

def register_bp(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(vehiculo_bp)
