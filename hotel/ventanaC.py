from entidades import conectar_bd, tipos_habitacion, ingresos
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

session = conectar_bd()

class win2(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.session = conectar_bd()

        self.title("Visualizar ingresos")

        # Obtener solo los nombres de los productos de la base de datos
        #tipo_select = session.query(tipos_habitacion).all()
        #tipo_select = [tipo_habitacion for tipo_habitacion in tipo_select]

        self.tipo_select = session.query(tipos_habitacion.id_tipo_habitacion, tipos_habitacion.tipo_habitacion).all()
        self.tipo_select = [(id_tipo, tipo_habitacion) for id_tipo, tipo_habitacion in self.tipo_select]

        # Crear la lista desplegable y agregar los productos
        self.opcion_seleccionada = tk.StringVar()
        self.lista_desplegable = ttk.Combobox(self, textvariable=self.opcion_seleccionada)
        self.lista_desplegable['values'] = [tipo[1] for tipo in self.tipo_select]
        self.lista_desplegable.grid(row=0, column=0)

        # BotÃ³n para mostrar el producto seleccionado
        boton = tk.Button(self, text="Mostrar producto seleccionado", command=self.cargar)
        boton.grid(row=1, column=0)

        self.tabla_rooms = ttk.Treeview(self, columns=( "Tipo de Habitacion", "Dias ocupados", "Total Ingresos"), show="headings")
        self.tabla_rooms.heading("Tipo de Habitacion", text="Tipo de Habitacion")
        self.tabla_rooms.heading("Dias ocupados", text="Dias ocupados")
        self.tabla_rooms.heading("Total Ingresos", text="Total Ingresos")
        self.tabla_rooms.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

    def cargar(self):
        seleccion = self.opcion_seleccionada.get()
        id_seleccionado = [tipo[0] for tipo in self.tipo_select if tipo[1] == seleccion][0]
        if seleccion and id_seleccionado:

            filas = self.tabla_rooms.get_children()[0:]
            for fila in filas:
                self.tabla_rooms.delete(filas)

            total = self.session.query(ingresos).filter_by(id_tipo_habitacion=id_seleccionado).first()

            self.tabla_rooms.insert("", "end", values=(seleccion, total.dias_ocupacion, total.ingresos))
        else:
            messagebox.showerror("Error", "Ingrese un Tipo de Habitacion/Costo por dia valido.")
