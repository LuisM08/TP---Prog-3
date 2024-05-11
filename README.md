# TP---Prog-3


    Tablas:
        Tipos_de_Habitacion: Esta tabla contendría información sobre los diferentes tipos de habitaciones y su costo diario.
            Campos: ID (clave primaria), Tipo_Habitacion, Costo_Diario.
        Estadias: Esta tabla registraría las estadías de los huéspedes.
            Campos: ID (clave primaria), Numero_Habitacion (clave foránea que referencia a la tabla Tipos_de_Habitacion), Fecha_Inicio, Fecha_Fin, Forma_Pago, Estado.
        Ingresos: Esta tabla registraría los ingresos por tipo de habitación.
            Campos: ID (clave primaria), Tipo_Habitacion (clave foránea que referencia a la tabla Tipos_de_Habitacion), Ingresos, Dias_Ocupacion.

    Formularios:
        Formulario_Tipos_Habitacion: Este formulario permitiría ingresar nuevos tipos de habitación y sus costos diarios.
        Formulario_Estadias: Este formulario permitiría cargar las estadías de los huéspedes, calcular automáticamente los valores dependientes (descuentos, duración, etc.) y cambiar el estado de la habitación si es necesario.
        Formulario_Ingresos: Este formulario permitiría visualizar los ingresos por tipo de habitación y la cantidad de días de ocupación de cada una.

    Botones y controles adicionales:
        Menú de navegación: Incluir un menú que permita navegar fácilmente entre los diferentes formularios y funcionalidades del sistema.
        Botón Finalizar Estadía: Agregar un botón en el formulario de estadías para finalizar una estadía activa.
        Lista desplegable: Incluir una lista desplegable en el formulario de ingresos para seleccionar el tipo de habitación del que se desean conocer los totales.

    Procedimientos y validaciones:
        Implementar procedimientos que calculen automáticamente los descuentos y otros valores dependientes durante el ingreso o modificación de una estadía.
        Validar que al ingresar una nueva estadía, si la habitación ya está ocupada, se cambie automáticamente su estado a "Estadía Finalizada".
        Asegurarse de que solo se muestren estadías finalizadas en el formulario de ingresos.