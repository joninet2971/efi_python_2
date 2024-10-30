# Proyecto Flask con SQLAlchemy

Este es un proyecto desarrollado con Python Flask y SQLAlchemy. El proyecto utiliza una base de datos local con XAMPP y maneja migraciones de base de datos.

## Requisitos

- Python
- Flask
- SQLAlchemy
- XAMPP (para la base de datos local)

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/joninet2971/efi_python.git
   cd efi_python
   
2. Crear y activar un entorno virtual:
    
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    
3. Instalar las dependencias:

    pip install -r requirements.txt

4. Configurar la base de datos en XAMPP:

    ```bash
    Inicia XAMPP y asegúrate de que MySQL esté en funcionamiento.
    Crea una base de datos en MySQL para el proyecto llamada equipos_db

5. Configurar las variables de entorno:

    archivo app.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'url base de datos'
    
6. Realizar las migraciones de la base de datos:

    ```bash
    flask db init
    flask db migrate -m "Mensaje de migración"
    flask db upgrade

7. Ejecutar la aplicación:

    ```bash
    flask run --reload
    
8. Uso
Accede a la aplicación en http://localhost:5000


