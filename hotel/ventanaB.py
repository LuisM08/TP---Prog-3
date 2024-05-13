from entidades import conectar_bd,tipos_habitacion, estadias, ingresos
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import mysql.connector

#Base = declarative_base()
#session = conectar_bd()

class ventanaB(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Cargar estadias")

        self.session = conectar_bd()

        self.label = Label(self, text="Nro. Habitacion")
        self.label.grid(row=0, column=0, padx=5, pady=10)
          # Ajusta el espaciado aquí
        self.label = Label(self, text="Dias de estadia")
        self.label.grid(row=1, column=0, padx=5, pady=10)  # Ajusta el espaciado aquí

        self.caja1 = tk.Entry(self)
        self.caja1.grid(row=0, column=1, padx=5, pady=10)
          # Ajusta el espaciado aquí
        self.caja2 = tk.Entry(self)
        self.caja2.grid(row=1, column=1, padx=5, pady=10)  # Ajusta el espaciado aquí

        self.tabla_rooms = ttk.Treeview(self, columns=("id", "Tipo de Habitacion", "Costo por día"), show="headings")
        self.tabla_rooms.heading("id", text="ID")
        self.tabla_rooms.heading("Tipo de Habitacion", text="Tipo de Habitacion")
        self.tabla_rooms.heading("Costo por día", text="Costo por día")
        self.tabla_rooms.grid(row=0, column=2, columnspan=4, padx=1, pady=2)  # Ajusta el espaciado aquí

        self.obtener_datos_tipos_hab()

        self.agregar_btn = tk.Button(self, text="Cargar", command=self.cargar)
        self.agregar_btn.grid(row=6, column=0, padx=10, pady=5)  # Ajusta el espaciado aquí

        self.editar_btn = tk.Button(self, text="Modificar", command=self.modificar)
        self.editar_btn.grid(row=6, column=1, padx=10, pady=5)  # Ajusta el espaciado aquí

        self.borrar_btn = tk.Button(self, text="Borrar", command=self.borrar)
        self.borrar_btn.grid(row=6, column=2, padx=10, pady=5)  # Ajusta el espaciado aquí

        self.finalizar_btn = tk.Button(self, text="Finalizar", command=self.finalizar)
        self.finalizar_btn.grid(row=6, column=4, padx=10, pady=5)  # Ajusta el espaciado aquí

        self.tabla_habitaciones = ttk.Treeview(self, columns=("ID", "Número", "Tipo", "Costo", "Días", "Sub-Total", "Descuento", "Total"), show="headings")
        self.tabla_habitaciones.heading("ID", text="ID")
        self.tabla_habitaciones.heading("Número", text="Número")
        self.tabla_habitaciones.heading("Tipo", text="Tipo")
        self.tabla_habitaciones.heading("Costo", text="Costo")
        self.tabla_habitaciones.heading("Días", text="Días")
        self.tabla_habitaciones.heading("Sub-Total", text="Sub-Total")
        self.tabla_habitaciones.heading("Descuento", text="% Descuento")
        self.tabla_habitaciones.heading("Total", text="Total")
        self.tabla_habitaciones.grid(row=7, column=0, columnspan=10, padx=5, pady=5)  # Ajusta el espaciado aquí

        self.op1 = tk.IntVar()
        self.sm = tk.Radiobutton(self, text="Crédito", variable=self.op1, value=1)
        self.sm.grid(row=5, column=0, padx=5, pady=5)  # Ajusta el espaciado aquí
        self.sf = tk.Radiobutton(self, text="Contado", variable=self.op1, value=0)
        self.sf.grid(row=5, column=1, padx=5, pady=5)  # Ajusta el espaciado aquí

        self.obtener_datos_estadias()

    def obtener_datos_tipos_hab(self):
        rooms = self.session.query(tipos_habitacion).all()
        for room in rooms:
            self.tabla_rooms.insert("", "end", values=(room.id_tipo_habitacion, room.tipo_habitacion, room.costo_diario))

    def obtener_datos_estadias(self):
        Estadias = self.session.query(estadias).filter_by(estado="ocupado").all()
        for Estadia in Estadias:
            id_tipo = self.session.query(tipos_habitacion).filter_by(id_tipo_habitacion=Estadia.id_tipo_habitacion).first()
            self.tabla_habitaciones.insert("","end",values=(Estadia.id_estadia, Estadia.numero, id_tipo.tipo_habitacion, id_tipo.costo_diario, Estadia.dia_estadia, Estadia.subtot, Estadia.descuento, Estadia.total_monto ))

    def cargar(self):
        numero_habitacion = self.caja1.get()
        dias_estadia = float(self.caja2.get())
        item_seleccionado = self.tabla_rooms.focus()
        metodo_pago = self.op1.get()
        costo_diario = float(self.tabla_rooms.item(item_seleccionado)['values'][2])
        tipo_habitacion = self.tabla_rooms.item(item_seleccionado)['values'][0]
        

        Estadias = self.session.query(estadias).filter_by(numero=numero_habitacion).first()
        if Estadias:
            if Estadias.estado == "ocupado" or Estadias.estado == "libre":

                room_ingresos = self.session.query(ingresos).filter_by(id_tipo_habitacion=Estadias.id_tipo_habitacion).first()
                room_ingresos.ingresos = room_ingresos.ingresos + Estadias.total_monto
                room_ingresos.dias_ocupacion = room_ingresos.dias_ocupacion + Estadias.dia_estadia

                self.session.commit()

                Estadias.forma_pago = metodo_pago
                Estadias.dia_estadia = dias_estadia
                Estadias.id_tipo_habitacion = tipo_habitacion
                Estadias.estado = "ocupado"
                descuento = self.descuento()
                Estadias.descuento = descuento
                subtotal = costo_diario * dias_estadia
                Estadias.subtot = subtotal
                total = subtotal - (subtotal * descuento)
                Estadias.total_monto = total
                self.session.commit()
                filas = self.tabla_habitaciones.get_children()[0:]
                for fila in filas:
                    self.tabla_habitaciones.delete(filas)
                self.obtener_datos_estadias()
            


        elif numero_habitacion and dias_estadia and item_seleccionado and metodo_pago:
            
            estado = 'ocupado'
            
            subtotal = (costo_diario * dias_estadia)
            print(subtotal)
            subtotal = float (subtotal)
            print(subtotal)
            
            descuento = self.descuento()
            total = subtotal - (descuento * subtotal)
            nueva_estadia = estadias(numero=numero_habitacion, dia_estadia=dias_estadia, subtot=subtotal,
                                      descuento=descuento, total_monto=total, forma_pago=metodo_pago, estado=estado, id_tipo_habitacion=tipo_habitacion)
            self.session.add(nueva_estadia)
            self.session.commit()
            self.tabla_habitaciones.insert("", "end", values=(
                nueva_estadia.id_estadia, numero_habitacion, tipo_habitacion, costo_diario,
                dias_estadia, subtotal, descuento, total))
        else:
            messagebox.showerror("Error", "Verifique los datos para continuar.")

    def descuento(self):
        dias_estadia = int(self.caja2.get())
        metodo_pago = self.op1.get()
        descuento = 0.0
        if metodo_pago == 1:
            if dias_estadia > 5 :
                descuento += 0.05
        else:
            descuento += 0.10

        if dias_estadia >10:
            descuento += 0.02
        
        return descuento

    def modificar(self):
           
            item_seleccionado = self.tabla_habitaciones.focus()
            id_est = self.tabla_habitaciones.item(item_seleccionado)['values'][0]
            costo = self.tabla_habitaciones.item(item_seleccionado)['values'][3]
            new_day = self.caja2.get()
            estadias = self.session.query(estadias).filter_by(id_estadia=id_est).first()
            pay = estadias.forma_pago
            descuento = 0.0
            if pay == 1:
                if new_day > 5 :
                    descuento += 0.05
            else:
                descuento += 0.10
 
            if new_day > 10:
                descuento += 0.02
            
            subtotal = costo * new_day
            total = subtotal - (descuento * subtotal)
            
            estadias.dia_estadia = new_day
            estadias.descuento = descuento
            estadias.subtot = subtotal
            estadias.total_monto = total

            self.session.commit()



    def borrar(self):
        item_seleccionado = self.tabla_habitaciones.focus()
        if item_seleccionado:
            id_est = self.tabla_habitaciones.item(item_seleccionado)['values'][0]
            room_borrar = self.session.query(estadias).filter_by(id_estadia=id_est).first()

            self.session.delete(room_borrar)
            self.session.commit()
            self.tabla_habitaciones.delete(item_seleccionado)
        else:
            messagebox.showerror("Error", "Seleccione una habitacion para borrar.")


    def finalizar(self):
        item_seleccionado = self.tabla_habitaciones.focus()
        if item_seleccionado:
            id_est = self.tabla_habitaciones.item(item_seleccionado)['values'][0]
            room_finalizar = self.session.query(estadias).filter_by(id_estadia=id_est).first()
            room_finalizar.estado = "libre"

            self.session.commit()
            self.tabla_habitaciones.delete(item_seleccionado)

            room_ingresos = self.session.query(ingresos).filter_by(id_tipo_habitacion=room_finalizar.id_tipo_habitacion).first()
            room_ingresos.ingresos = room_ingresos.ingresos + room_finalizar.total_monto
            room_ingresos.dias_ocupacion = room_ingresos.dias_ocupacion + room_finalizar.dia_estadia

            self.session.commit()
        else:
            messagebox.showerror("Error", "Seleccione una habitacion para finalizar estadia.")

