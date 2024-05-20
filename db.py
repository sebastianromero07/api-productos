import psycopg2

# Conectar a la base de datos postgres por defecto para comprobar si la base de datos 'productos' existe
default_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password=12345,  # Tu contraseña de postgres
    host="localhost"
)
default_conn.autocommit = True  # Necesario para crear una base de datos fuera de una transacción
default_cursor = default_conn.cursor()

# Comprobar si la base de datos 'productos' existe
default_cursor.execute("SELECT 1 FROM pg_database WHERE datname='productos'")
db_exists = default_cursor.fetchone()

# Crear la base de datos 'productos' si no existe
if not db_exists:
    default_cursor.execute("CREATE DATABASE productos")

# Cerrar la conexión inicial
default_cursor.close()
default_conn.close()

# Conectar a la base de datos 'productos'
conn = psycopg2.connect(
    dbname="productos",
    user="postgres",
    password=12345,  # Tu contraseña de postgres
    host="localhost"
)

cursor = conn.cursor()

# Comprobar si la tabla 'products' existe
cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'products')")
table_exists = cursor.fetchone()[0]

# Crear la tabla 'products' si no existe
if not table_exists:
    sql_query = """
        CREATE TABLE products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            quantity INTEGER NOT NULL
        )
    """
    cursor.execute(sql_query)
    conn.commit()

def commit():
    conn.commit()
