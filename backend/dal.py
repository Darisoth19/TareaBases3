import pyodbc

# Configura estos datos según tu servidor y base de datos
SERVER = "25.39.62.157"  # Puede ser localhost\SQLEXPRESS
DATABASE = "EmpresaDB"
USERNAME = "sa"  # Si usas autenticación SQL
PASSWORD = "contrabases1234"  # Si usas autenticación SQL

def obtener_conexion():
    conn = pyodbc.connect(
        f"DRIVER={{SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD}",
        timeout=5,
        autocommit=True
    )
    return conn

def verificar_usuario(username, password):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("EXEC SP_VerificacionLogin ?, ?", username, password)

        row = cursor.fetchone()
        conn.close()


        if row and row[0] == 1:
            return True
        else:
            return False

    except Exception as e:
        print("Error en verificar usuario")
        return False


def eliminar_usuario(nombre):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_EliminacionLogica ?", (nombre,))
    conn.commit()
    conn.close()



def consultar_Usuario(nombre):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_Consultar ?", (nombre,))
    resultados = cursor.fetchall()
    conn.close()
    
    if not resultados:
        return None
    
    fila = resultados[0]
    return {
        "docId": fila[0], 
        "nombre": fila[1], 
        "idPuesto": fila[2], 
        "saldoVacaciones": fila[3]
    }

def obtener_usuarios():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM Usuario")  
    filas = cursor.fetchall()
    conn.close()
    return [{"name": fila[0]} for fila in filas]

def listaUsuario():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_ListaEmpleados")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": fila[0]} for fila in filas]

def eliminarUsuario(id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_EliminacionLogica ?", (id))
    conn.commit()

def insertar_usuario(nombre, id, idpuesto, valorDoc, fecha, saldo):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_InsertarEmpleado ?, ?, ?, ?, ?, ?", (nombre, id, idpuesto, valorDoc, fecha, saldo))
    conn.commit()
    conn.close()


def listadoFiltrado(filtro):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_ListadoFiltrado ?", (filtro))
    filas = cursor.fetchall()
    conn.commit()
    conn.close()
    return [{"nombre": fila[0]} for fila in filas]


def listadoPuestos():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("EXEC sp_ListadoPuestos")
    filas = cursor.fetchall()
    conn.close()
    return [{"nombre": fila[0], "id": fila[1]} for fila in filas]


def actualizacionEmpleado(docId, nombreViejo, nombre, idPuesto):
    conn = obtener_conexion()
    cursor = conn.cursor()
    
    
    cursor.execute("EXEC sp_ActualizacionUsuario ?, ?, ?, ?", (docId, nombreViejo, nombre, idPuesto))
    
    conn.commit()
    conn.close()
    return {"message": "Empleado actualizado correctamente"}