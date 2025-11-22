from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware  # 👈 Importa esto
from backend.dal import verificar_usuario,listaUsuario, listadoFiltrado, listadoPuestos, actualizacionEmpleado, insertar_usuario, consultar_Usuario, eliminar_usuario
import datetime

app = FastAPI()

# 👇 Agrega este bloque
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes cambiar "*" por tu dominio si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos y plantillas
app.mount("/static", StaticFiles(directory="frontend"), name="static")
templates = Jinja2Templates(directory="frontend")


def listaEmpleados():
    return listaUsuario()



# Ruta para la página de login
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    print("iniciandooo")
    return templates.TemplateResponse("login.html", {"request": request})



@app.get("/menu", response_class=HTMLResponse)
def index_page(request: Request):
    print("Ahora menu")
    return templates.TemplateResponse("menu.html", {"request": request})


@app.get("/insertar", response_class=HTMLResponse)
def index_page(request: Request):
    print("Ahora insertar")
    return templates.TemplateResponse("insertarEmpleado.html", {"request": request})


@app.get("/servicios", response_class=HTMLResponse)
def index_page(request: Request):
    print("Ahora movimientos")
    return templates.TemplateResponse("pedirServicios.html", {"request": request})

@app.get("/listaPersonas", response_class=HTMLResponse)
def index_page(request: Request):
    print("Ahora empleados")
    return templates.TemplateResponse("listaPersonas.html", {"request": request})

@app.get("/api/empleados")
def listar_empleados():
    return listaUsuario()

@app.get("/api/consulta")
def consultarUsuario(usuario: str):
    return consultar_Usuario(usuario)

@app.delete("/api/eliminar")
def eliminarUsuario(usuario: str):
    eliminar_usuario(usuario)

@app.get("/api/puestos")
def listar_empleados():
    return listadoPuestos()

@app.post("/api/actualizacionUsuario")
def actualizarUsuario(docId: str, viejoNombre: str, nombre: str, idPuesto: int):
    actualizacionEmpleado(docId, viejoNombre, nombre, idPuesto)


@app.post("/api/insertarUsuario")
def insertarUsuario(nombre: str, id: int, Puesto:str, valorDoc: str):
    insertar_usuario(nombre, id,Puesto, valorDoc, datetime.datetime.now(), 10)


@app.get("/api/empleadosConFiltro")
def listarFiltrado(filtro: str):
    print(filtro)
    return listadoFiltrado(filtro)

# Ruta POST para validar usuario
@app.post("/api/login")
def api_login(username: str = Form(...), password: str = Form(...)):
    valido = verificar_usuario(username, password)
    if valido:
        return JSONResponse(content={"success": True, "message": "Inicio de sesión exitoso"})
    else:
        return JSONResponse(content={"success": False, "message": "Usuario o contraseña incorrectos"})
