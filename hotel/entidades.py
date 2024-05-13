from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import mysql.connector

Base = declarative_base()

class estadias(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = 'estadias'
    # DefiniciÃ³n de las columnas de la tabla
    id_estadia = Column(Integer, primary_key=True)
    numero = Column(Integer)
    total_monto = Column(Float)
    forma_pago = Column(Integer)
    dia_estadia = Column(Integer)
    estado = Column(String(11))
    subtot = Column(Float)
    descuento = Column(Float)
    id_tipo_habitacion = Column(Integer, ForeignKey('tipos_habitacion.id_tipo_habitacion'))

class tipos_habitacion(Base):
    __tablename__ = 'tipos_habitacion'
    id_tipo_habitacion = Column(Integer, primary_key=True, autoincrement=True)
    tipo_habitacion = Column(String(11))
    costo_diario = Column(Integer)
    estadias = relationship('estadias')#, cascade = 'all, delete, delete-orphan')
    ingresos = relationship('ingresos')#, cascade = 'all, delete, delete-orphan')

class ingresos(Base):
    __tablename__ = 'ingresos'
    id_ingreso = Column(Integer, primary_key=True)
    ingresos = Column(Float)  #acumulador de Ingresos
    dias_ocupacion = Column(Integer) #total dias ocupados
    id_tipo_habitacion = Column(Integer, ForeignKey('tipos_habitacion.id_tipo_habitacion'))


def conectar_bd():
    engine = create_engine('mysql+pymysql://root@localhost/hotel')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

# Conectar a la base de datos
def conectar():
    conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="hotel"
                )
    return conexion

#nueva_ciudad = tipos_habitacion(tipo_habitacion='2', costo_diario='2')
#session.add(nueva_ciudad)
#session.commit()