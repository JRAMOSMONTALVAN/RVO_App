import psycopg2

# Configuración de conexión
DB_CONFIG = {
    "dbname": "postgres",       # Nombre de tu base de datos
    "user": "postgres",         # Usuario de PostgreSQL
    "password": "admin123",     # Contraseña del usuario
    "host": "localhost",        # Dirección del host
    "port": "5432",             # Puerto de conexión
}

def verificar_conexion():
    try:
        # Intentar conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        print("¡Conexión exitosa a PostgreSQL!")

        # Crear un cursor para ejecutar comandos SQL
        cursor = conn.cursor()

        # Consultar las bases de datos disponibles
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        bases_de_datos = cursor.fetchall()
        print("Bases de datos disponibles:")
        for bd in bases_de_datos:
            print(f"- {bd[0]}")

        # Cerrar cursor y conexión
        cursor.close()
        conn.close()
        print("Conexión cerrada exitosamente.")

    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")

if __name__ == "__main__":
    verificar_conexion()
