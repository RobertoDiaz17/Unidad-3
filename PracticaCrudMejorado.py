from tkinter import *
from tkinter import ttk
from Conexion import *

ventana=Tk()
ventana.title("ASNAKSDJASD")
ventana.geometry("600x500")

connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="colegio",
        )
db=connection
cursor=db.cursor()
modificar=False
dni=StringVar()
sexo=StringVar()
nombres=StringVar()
apellidos=StringVar()

marco=LabelFrame(ventana, text="Formulario De Gestion De Estudiantes")
marco.place(x=50, y=50, width=500, height=400)

#Labels y Entrys
lblDni=Label(marco, text="DNI").grid(column=0, row=0, padx=5, pady=5)
txtDni=Entry(marco, textvariable=dni)
txtDni.grid(column=1, row=0)

lblSexo=Label(marco, text="Sexo").grid(column=0, row=1, padx=5, pady=5)
txtSexo=ttk.Combobox(marco, values=["M", "F"],textvariable=sexo)
txtSexo.grid(column=1, row=1)
txtSexo.current(0)

lblNombres=Label(marco, text="Nombres").grid(column=2, row=0, padx=5, pady=5)
txtNombres=Entry(marco, textvariable=nombres)
txtNombres.grid(column=3, row=0)

lblApellidos=Label(marco, text="Apellidos").grid(column=2, row=1, padx=5, pady=5)
txtApellidos=Entry(marco, textvariable=apellidos)
txtApellidos.grid(column=3, row=1)

lblMensaje=Label(marco, text="Aqui van los mensajes", fg="red")
lblMensaje.grid(column=0, row=2, columnspan=4)

# Tabla De Estudiantes
tvEstudiantes=ttk.Treeview(marco, selectmode=NONE)
tvEstudiantes.grid(column=0, row=3, columnspan=4, padx=5)
tvEstudiantes["columns"]=("ID", "DNI", "SEXO", "NOMBRES", "APELLIDOS",)
tvEstudiantes.column("#0", width=0, stretch=NO)
tvEstudiantes.column("ID", width=50, anchor=CENTER)
tvEstudiantes.column("DNI", width=50, anchor=CENTER)
tvEstudiantes.column("SEXO", width=50, anchor=CENTER)
tvEstudiantes.column("NOMBRES", width=100, anchor=CENTER)
tvEstudiantes.column("APELLIDOS", width=100, anchor=CENTER)
tvEstudiantes.heading("#0", text="")
tvEstudiantes.heading("ID", text="ID", anchor=CENTER)
tvEstudiantes.heading("DNI", text="DNI", anchor=CENTER)
tvEstudiantes.heading("SEXO", text="SEXO", anchor=CENTER)
tvEstudiantes.heading("NOMBRES", text="NOMBRES", anchor=CENTER)
tvEstudiantes.heading("APELLIDOS", text="APELLIDOS", anchor=CENTER)


#Botones De Accion
btnEliminar=Button(marco, text="Eliminar", command=lambda:eliminar())
btnEliminar.grid(column=1, row=4)
btnNuevo=Button(marco, text="Guardar",command=lambda:agregar_alumno())
btnNuevo.grid(column=2, row=4)
btnModificar=Button(marco, text="Seleccionar", command=lambda:actualizar())
btnModificar.grid(column=3, row=4)


#Fucniones
def modificarFalse():
    global modificar
    modificar=False
    tvEstudiantes.config(selectmode=NONE)
    btnNuevo.config(text="Guardar")
    btnModificar.config(text="Seleccionar")
    btnEliminar.config(state=DISABLED)

def modificarTrue():
    global modificar
    modificar=True
    tvEstudiantes.config(selectmode=BROWSE)
    btnNuevo.config(text="Nuevo")
    btnModificar.config(text="Modificar")
    btnEliminar.config(state=NORMAL)    

def validar():
    return len(dni.get()) and len (nombres.get()) and len (apellidos.get())
            
def limpiar():
    dni.set("")
    nombres.set("")
    apellidos.set("")

def vaciar_tablar():
    filas=tvEstudiantes.get_children()
    for fila in filas:
        tvEstudiantes.delete(fila)

def llenar_tabla():
    vaciar_tablar()
    sql="SELECT * FROM estudiantes"
    cursor.execute(sql)
    filas=cursor.fetchall()
    for fila in filas:
        tvEstudiantes.insert("", END, id, text=id, values=fila)

def eliminar():
    id=tvEstudiantes.selection()[0]
    if int(id)>0:
        sql="delate from estudiantes where id="+id
        cursor.execute(sql)
        db.commit()
        tvEstudiantes.delate(id)
        lblMensaje.config(text="Se A Eliminado El Registro Correctamente")
    else:
        lblMensaje.config(text="Seleccione Un Registro Para Eliminar")

def nuevo(nombre, sexo, dni, apellidos):
    if modificar==False:
        if validar():
            sql='''INSERT INTO estudiantes (Sexo,Dni,Nombres,Apellidos) VALUES ('{}','{}','{}','{}')'''.format(sexo, dni, nombre,apellidos)
            cursor.execute(sql)
            db.commit()
            lblMensaje.config(text="Se A Guardado Un Registro", fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="Los Campos No Debes Estar Vacios", fg="red")
    else:
        modificarFalse()

def actualizar():
    if modificar==True:
        if validar():
            val=(dni.get(), sexo.get(), nombres.get(), apellidos.get())
            sql="update estudianes dni=%s, sexo=%s nombres=%s, apelldios=%s"
            cursor.execute(sql, val)
            db.commit()
            lblMensaje.config(text="Se A Actualizado Un Registro", fg="green")
            llenar_tabla()
            limpiar()
        else:
            lblMensaje.config(text="Los Campos No Debes Estar Vacios", fg="red")
    else:
        modificarTrue()

def agregar_alumno():
        tvEstudiantes.get_children()
        nombre:str=txtDni.get()
        sexo=str=txtSexo.get()
        dni =str=txtNombres.get()
        apellidos =str=txtApellidos.get()
        vas=""
        datos=(vas,nombre, sexo, dni, apellidos)
        if not nombre or not dni or not apellidos or not sexo:
         return
        else: 
         tvEstudiantes.insert('',0,text=vas,values=datos)
         nuevo(nombre, sexo, dni, apellidos,)
         txtDni.delete(0, END)
         txtSexo.delete(0, END)
         txtNombres.delete(0, END)
         txtApellidos.delete(0, END)











ventana.mainloop()