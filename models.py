from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    is_admin = db.Column(db.Boolean)
    tipo = db.Column(db.String(50), nullable=False)


    def to_dict(self):
        return dict(
            username=self.username,
            password=self.password_hash
        )

class Marca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False, unique=True)

    activo = db.Column(db.Boolean, default=True, nullable=False)