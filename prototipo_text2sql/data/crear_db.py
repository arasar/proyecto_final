import sqlite3

# Ruta de la base de datos
DB_PATH = "empresa.db"

# Crear conexión
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit(1)

# Crear tablas de ejemplo
cursor.execute("""
CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    edad INTEGER,
    puesto TEXT,
    salario REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS departamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    ubicacion TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    presupuesto REAL,
    id_departamento INTEGER,
    FOREIGN KEY (id_departamento) REFERENCES departamentos (id)
);
""")

# Insertar datos de ejemplo
cursor.executemany("""
INSERT INTO empleados (nombre, edad, puesto, salario) VALUES (?, ?, ?, ?);
""", [
    ("Agustina", 28, "Ingeniera de datos", 850000),
    ("Juan", 35, "Analista funcional", 720000),
    ("Lucía", 30, "Data scientist", 950000),
    ("Pedro", 45, "Gerente de TI", 1200000)
])

cursor.executemany("""
INSERT INTO departamentos (nombre, ubicacion) VALUES (?, ?);
""", [
    ("IT", "Buenos Aires"),
    ("Finanzas", "Rosario"),
    ("RRHH", "Córdoba")
])

cursor.executemany("""
INSERT INTO proyectos (nombre, presupuesto, id_departamento) VALUES (?, ?, ?);
""", [
    ("Automatización de reportes", 2500000, 1),
    ("Optimización de costos", 1800000, 2),
    ("Capacitación 2025", 800000, 3)
])

# Guardar y cerrar
conn.commit()
conn.close()

print("✅ Base de datos 'empresa.db' creada y cargada con éxito.")
