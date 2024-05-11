import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from ventanaA import ventanaA

Base = declarative_base()

class estadias(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = 'estadias'
    # Definición de las columnas de la tabla
    id_estadias = Column(Integer, primary_key=True)
    total_monto = Column(Integer(20))
    forma_pago = Column(Integer(20))
    dia_estadia = Column(Integer(20))
    estado = Integer((20))
    id_tipo_habitacion = Column(Integer, ForeignKey('tipos_habitacion.id_tipo_habitacion'))

class tipos_habitacion(Base):
    __tablename__ = 'tipos_habitacion'
    id_tipo_habitacion = Column(Integer(20))
    tipo_habitacion = Column(Integer(20))
    costo_diario = Column(Integer(20))
    estadias = relationship('estadias', cascade = 'all, delete, delete-orphan')
    ingresos = relationship('ingresos', cascade = 'all, delete, delete-orphan')

class ingresos(Base):
    id_ingreso = Column(Integer(20))
    ingresos = Column(Integer(20))  #acumulador de Ingresos
    dias_ocupacion = Column(Integer(20)) #total dias ocupados
    id_tipo_habitacion = Column(Integer, ForeignKey('tipos_habitacion.id_tipo_habitacion'))

class menu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Menu hotel trans")

        # Conexión a la base de datos
        engine = create_engine('mysql+pymysql://root@localhost/hotel')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def mostrar_ventanaA(self):
        segunda_ventana = ventanaA(self)
        segunda_ventana.transient(self)
        segunda_ventana.grab_set()
        self.wait_window(segunda_ventana)


if __name__ == "__main__":
    app = menu()
    app.mainloop()