# Proyecto Flask con SQLAlchemy

Este es un proyecto desarrollado con Python Flask y SQLAlchemy. El proyecto utiliza una base de datos local con XAMPP y maneja migraciones de base de datos.

## Requisitos

- Python
- Flask
- SQLAlchemy
- XAMPP (para la base de datos local)

## Instalación

1. **Clonar el repositorio:**

   git clone https://github.com/joninet2971/efi_python_2.git
   cd efi_python
   
2. Crear y activar un entorno virtual:
    
    python3 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    
3. Instalar las dependencias:

    pip install -r requirements.txt

4. Configurar la base de datos en XAMPP:

    Inicia XAMPP y asegúrate de que MySQL esté en funcionamiento.
    Crea una base de datos en MySQL para el proyecto llamada equipos_db

5. Configurar las variables de entorno:

    archivo app.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'url base de datos'
    
6. Realizar las migraciones de la base de datos:

    flask db init
    flask db migrate -m "Mensaje de migración"
    flask db upgrade

7. Borrar la tabla Users desde la base de datos
8. Dentro del proyecto en el directorio versions/ buscar primera migracion, agregar las importaciones y el siguiente codigo

    from werkzeug.security import generate_password_hash
    from models import  User
    from app  import db

    existing_user = User.query.filter_by(username='admin').first()
    if not existing_user:
        admin_user = User(
            username = 'admin',
            password_hash = generate_password_hash('admin'),
            is_admin = True)
        db.session.add(admin_user)
        db.session.commit()

9. Repetir el punto 6

10. Ejecutar la aplicación:

    flask run --reload
    
8. Uso
Accede a tu gestor de API para usar el proyecto.


