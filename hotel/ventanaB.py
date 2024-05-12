from entidades import tipos_habitacion, estadias
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey,CHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import mysql.connector

Base = declarative_base()

class Estadia(Base):
    __tablename__ = 'estadias'

    id_estadia = Column(Integer, primary_key=True)
    total_monto = Column(Float)
    forma_pago = Column(Integer)
    dia_estadia = Column(Integer)
    estado = Column(CHAR(10))
    id_tipo_habitacion = Column(Integer, ForeignKey('tipos_habitacion.id_tipo_habitacion'))
    numero = Column(Integer)

## Conectar a la base de datos
#conexion = mysql.connector.connect(
#                host="localhost",
#                user="root",
#                password="",
#                database="hotel"
#            )
#
#engine = create_engine('mysql+pymysql://root@localhost/hotel')
#Base.metadata.create_all(engine)
#Session = sessionmaker(bind=engine)

class ventanaB(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Cargar estadias")
        ctk.set_appearance_mode("light")

        ctk.CTkLabel(self, text="Nro. Habitacion").grid(row=3, column=0, padx=10, pady=5)
        ctk.CTkLabel(self, text="Dias de estadia").grid(row=4, column=0, padx=10, pady=5)

        self.caja1 = ctk.CTkEntry(self)
        self.caja1.grid(row=3, column=1, padx=10, pady=10)
        self.caja2 = ctk.CTkEntry(self)
        self.caja2.grid(row=4, column=1, padx=10, pady=10)

        self.agregar_btn = tk.Button(self, text="Cargar", command=self.cargar)
        self.agregar_btn.grid(row=6, column=0, padx=5, pady=5)

        self.editar_btn = tk.Button(self, text="Modificar", command=self.modificar)
        self.editar_btn.grid(row=6, column=1, padx=5, pady=5)

        self.borrar_btn = tk.Button(self, text="Borrar", command=self.borrar)
        self.borrar_btn.grid(row=6, column=2, padx=5, pady=5)

        self.tabla_habitaciones = ttk.Treeview(self, columns=("ID", "Número de Habitación", "Tipo de Habitación", "Costo Diario", "Días de Estadía", "Sub-Total", "Descuento", "Total"), show="headings")
        self.tabla_habitaciones.heading("ID", text="ID")
        self.tabla_habitaciones.heading("Número de Habitación", text="Número de Habitación")
        self.tabla_habitaciones.heading("Tipo de Habitación", text="Tipo de Habitación")
        self.tabla_habitaciones.heading("Costo Diario", text="Costo Diario")
        self.tabla_habitaciones.heading("Días de Estadía", text="Días de Estadía")
        self.tabla_habitaciones.heading("Sub-Total", text="Sub-Total")
        self.tabla_habitaciones.heading("Descuento", text="% Descuento")
        self.tabla_habitaciones.heading("Total", text="Total")
        self.tabla_habitaciones.grid(row=0, column=0, columnspan=7, padx=5, pady=5,)

        self.op1 = tk.StringVar()
        self.op1.set("a")
        self.sm = tk.Radiobutton(self, text="Crédito", variable=self.op1, value="a")
        self.sm.grid(row=3, column=2)
        self.sf = tk.Radiobutton(self, text="Contado", variable=self.op1, value="b")
        self.sf.grid(row=4, column=2)

        self.obtener_datos()

    def obtener_datos(self):
        habitaciones = self.session.query(estadias).filter_by(estado="en uso")
        for habitacion in habitaciones:
            self.tabla_habitaciones.insert("","end",values=(habitacion.id_estadia, habitacion.numero, habitacion.tipo, habitacion.costo, habitacion.dias,
                habitacion.subtotal, habitacion.descuento, habitacion.total))

    def cargar(self):
        numero_habitacion = self.caja1.get()
        dias_estadia = int(self.caja2.get())
        tipo_habitacion = self.session.query(tipos_habitacion).filter_by(tipo_habitacion=self.tipo.get()).first()
        costo_diario = tipo_habitacion.costo_diario
        subtotal = costo_diario * dias_estadia
        descuento = 0.0
        if dias_estadia > 5:
            descuento += 0.05
        if dias_estadia > 10:
            descuento += 0.02
        metodo_pago = self.op1.get()

        if metodo_pago == "a":  # Crédito
            descuento += 0.05
        else:  # Contado
            descuento += 0.1

        total = subtotal * (1 - descuento)

        nueva_estadia = estadias(numero=numero_habitacion, tipo=tipo_habitacion.tipos_habitacion, costo=costo_diario, dias=dias_estadia, subtotal=subtotal,
                                      descuento=descuento, total=total)
        self.session.add(nueva_estadia)
        self.session.commit()
        self.tabla_habitaciones.insert("", "end", values=(
            nueva_estadia.id, nueva_estadia.numero, nueva_estadia.tipo, nueva_estadia.costo,
            nueva_estadia.dias, nueva_estadia.subtotal, nueva_estadia.descuento, nueva_estadia.total))

    def modificar(self):
        n = int(self.caja1.get())   

    def borrar(self):
        n = int(self.caja1.get())

if __name__ == "__main__":
    app = ventanaB()
    app.mainloop()
