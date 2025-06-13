import sqlite3

# Crear la base de datos vacía
con = sqlite3.connect("electrodomesticos.db")
cur = con.cursor()

# Leer el archivo .sql
with open("electrodomesticos.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Ejecutar el script SQL
cur.executescript(sql_script)

# Confirmar cambios y cerrar
con.commit()
con.close()

print("✅ Base de datos creada: electrodomesticos.db")