import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter import messagebox
from ventanaA import win
from ventanaB import ventanaB
from ventanaC import win2


class menu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Menu hotel trans")
        ctk.set_appearance_mode("light")
        
        self.mostrar_ventana_boton = tk.Button(self, text="Ingresar tipos de habitacion", command=self.mostrar_ventana)
        self.mostrar_ventana_boton.grid(row=0, column=0 , padx=10, pady=10)

        self.mostrar_ventana_boton = tk.Button(self, text="Cargar estadias", command=self.mostrar_segunda_ventana)
        self.mostrar_ventana_boton.grid(row=1, column=0, padx=10, pady=10)

        self.mostrar_ventana_boton = tk.Button(self, text="Visualizar ingresos", command=self.mostrar_tercera_ventana)
        self.mostrar_ventana_boton.grid(row=2, column=0, padx=10, pady=10)

    def mostrar_ventana(self):
        segunda_ventana = win(self)
        segunda_ventana.transient(self)
        segunda_ventana.grab_set()
        self.wait_window(segunda_ventana)

    def mostrar_segunda_ventana(self):
        segunda_ventana = ventanaB(self)  # Asegúrate de pasar la sesión correctamente
        segunda_ventana.transient(self)
        segunda_ventana.grab_set()
        self.wait_window(segunda_ventana)

    def mostrar_tercera_ventana(self):
        segunda_ventana = win2(self)
        segunda_ventana.transient(self)
        segunda_ventana.grab_set()
        self.wait_window(segunda_ventana)


if __name__ == "__main__":
    app = menu()
    app.mainloop()