from entidades import conectar_bd, conectar, tipos_habitacion, ingresos
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

session = conectar_bd()

class win(tk.Toplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Cargar Tipo de Habitacion")

        self.session = conectar_bd()

        self.label = Label(self, text="Tipo de Habitacion")
        self.label.grid(row=0, column=0, padx=10, pady=5)

        self.label1 = Label(self, text="Costo por día")
        self.label1.grid(row=0, column=1, padx=10, pady=5)

        self.tipo = tk.Entry(self)
        self.tipo.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.costo = tk.Entry(self)
        self.costo.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)

        self.cargar = tk.Button(self, text="Agregar", command=self.add)
        self.cargar.grid(row=1, column=2, padx=5, pady=5)

        self.borrar = tk.Button(self, text="Borrar", command=self.borrar)
        self.borrar.grid(row=1, column=3, padx=5, pady=5)

        self.tabla_rooms = ttk.Treeview(self, columns=("id", "Tipo de Habitacion", "Costo por día"), show = "headings")
        self.tabla_rooms.heading("id", text="ID")
        self.tabla_rooms.heading("Tipo de Habitacion", text="Tipo de Habitacion")
        self.tabla_rooms.heading("Costo por día", text="Costo por día")
        self.tabla_rooms.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        self.cargar_datos_desde_db()

    def cargar_datos_desde_db(self):
        rooms = self.session.query(tipos_habitacion).all()
        for room in rooms:
            self.tabla_rooms.insert("", "end", values=(room.id_tipo_habitacion, room.tipo_habitacion, room.costo_diario))

    def add(self):
        tipo = self.tipo.get()
        costo = self.costo.get()
        if tipo and costo:
            new_room = tipos_habitacion(tipo_habitacion=tipo, costo_diario=costo)
            self.session.add(new_room)
            self.session.commit()
            new_ingreso = ingresos(ingresos=0, dias_ocupacion=0, id_tipo_habitacion=new_room.id_tipo_habitacion)
            self.session.add(new_ingreso)
            self.session.commit()
            self.tabla_rooms.insert("", "end", values=(new_room.id_tipo_habitacion, tipo, costo))
            self.tipo.delete(0, tk.END)
            self.costo.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Ingrese un Tipo de Habitacion/Costo por dia valido.")

    def borrar(self):
        item_seleccionado = self.tabla_rooms.focus()
        if item_seleccionado:
            id_room = self.tabla_rooms.item(item_seleccionado)['values'][0]

            conexion = conectar()
            # room_borrar = self.session.query(tipos_habitacion).filter_by(id_tipo_habitacion=id_room).first()
            # room_borrar = self.session.query(tipos_habitacion).filter(tipos_habitacion.id_tipo_habitacion == id_room).first()
            # room_borrar = self.session.query(tipos_habitacion).get(id_room)

            # Crear un cursor
            cursor = conexion.cursor()

            sql = "DELETE FROM tipos_habitacion WHERE id_tipo_habitacion = %s"
            valores = (id_room, )
            cursor.execute(sql, valores)
            sql = "DELETE FROM ingresos WHERE id_tipo_habitacion = %s"
            valores = (id_room, )
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
            conexion.close()

            self.tabla_rooms.delete(item_seleccionado)
        else:
            messagebox.showerror("Error", "Seleccione un tipo de habitacion para borrar.")