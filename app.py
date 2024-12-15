from flask import Flask
from extensions import db, migrate
from modelos import Cliente, Vehiculo, Proforma, OrdenServicio

def create_app():
    # Inicializamos la aplicación Flask
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taller_mecanico.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializamos las extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Rutas principales
    @app.route("/")
    def home():
        return {"mensaje": "Bienvenido a la API del Taller Mecánico"}

    return app

# Creamos la instancia de la aplicación
app = create_app()

if __name__ == "__main__":
    app.run()
