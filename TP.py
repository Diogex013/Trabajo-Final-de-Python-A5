# Variables de Alcance Global (Scope Global)
# Estructura de datos: Listas (Arreglos) que contienen diccionarios
catalogo_libros = [
    {"id": 101, "titulo": "El Aleph", "autor": "Borges", "disponible": True, "cant_prestamos": 0},
    {"id": 102, "titulo": "1984", "autor": "Orwell", "disponible": True, "cant_prestamos": 0},
    {"id": 103, "titulo": "Fahrenheit 451", "autor": "Bradbury", "disponible": True, "cant_prestamos": 0}
]

usuarios_registrados = [] 

# Variables especiales (Módulo 2 - Pág 35)
contador_prestamos_global = 0  # Contador
acumulador_multas_global = 0.0 # Acumulador

def registrar_usuario():
    """
    Esta función registra un nuevo usuario en el sistema.
    
    Args:
        Ninguno.
        
    Returns:
        Nada.
    """
    print("\n--- REGISTRO DE USUARIO ---")
    dni = int(input("Ingrese el DNI (número mayor a 0): "))
    
    # Estructura repetitiva while para VALIDACIÓN (Módulo 2 - Pág 58)
    while dni <= 0:
        print("¡Ha escrito un número negativo o cero! Inténtelo de nuevo.")
        dni = int(input("Ingrese el DNI (número mayor a 0): "))
        
    # Uso de Bandera para controlar si el usuario ya existe (Módulo 2 - Pág 39)
    bandera_existe = False
    for usuario in usuarios_registrados:
        if usuario["dni"] == dni:
            bandera_existe = True
            break # Sentencia loop control (Módulo 2 - Pág 74)
            
    if bandera_existe == True:
        print("El usuario ya se encuentra registrado.")
    else:
        nombre = input("Ingrese el nombre del usuario: ")
        nuevo_usuario = {
            "dni": dni,
            "nombre": nombre,
            "tiene_libro": False,
            "id_libro_prestado": 0,
            "multa_total": 0.0
        }
        usuarios_registrados.append(nuevo_usuario)
        print("Usuario registrado exitosamente.")

def mostrar_catalogo():
    """
    Esta función muestra el catálogo de libros y su estado.
    
    Args:
        Ninguno.
        
    Returns:
        Nada.
    """
    print("\n--- CATÁLOGO DISPONIBLE ---")
    # Estructura repetitiva for in (Módulo 2 - Pág 60)
    for libro in catalogo_libros:
        estado = "Prestado"
        if libro["disponible"] == True:
            estado = "Disponible"
            
        print(f"ID: {libro['id']} | Título: {libro['titulo']} | Autor: {libro['autor']} | Estado: {estado}")

def prestar_libro():
    """
    Gestiona el préstamo validando disponibilidad y multas.
    
    Args:
        Ninguno.
        
    Returns:
        Nada.
    """
    # Declaramos el uso de la variable global (Guía Funciones - Pág 8)
    global contador_prestamos_global 
    
    dni = int(input("\nIngrese el DNI del usuario para el préstamo: "))
    
    # Algoritmo de Búsqueda de usuario
    usuario_actual = None
    for u in usuarios_registrados:
        if u["dni"] == dni:
            usuario_actual = u
            break
            
    # Condicionales anidados (Módulo 2 - Pág 18)
    if usuario_actual == None:
        print("Usuario no encontrado. Debe registrarse primero.")
    else:
        if usuario_actual["tiene_libro"] == True:
            print("El usuario ya tiene un libro sin devolver.")
        elif usuario_actual["multa_total"] > 0:
            print("El usuario tiene multas impagas y no puede pedir libros.")
        else:
            mostrar_catalogo()
            id_solicitado = int(input("\nIngrese el ID del libro que desea llevar: "))
            
            # Bandera para saber si el bucle encontró el libro
            bandera_libro_encontrado = False
            for libro in catalogo_libros:
                if libro["id"] == id_solicitado:
                    bandera_libro_encontrado = True
                    if libro["disponible"] == True:
                        # Efectuamos el préstamo
                        libro["disponible"] = False
                        libro["cant_prestamos"] += 1 # Contador interno
                        
                        usuario_actual["tiene_libro"] = True
                        usuario_actual["id_libro_prestado"] = libro["id"]
                        
                        contador_prestamos_global += 1 # Contador global
                        print(f"Préstamo exitoso. Se entregó: {libro['titulo']}")
                    else:
                        print("El libro seleccionado ya se encuentra prestado.")
                    break
                    
            if bandera_libro_encontrado == False:
                print("El ID ingresado no corresponde a ningún libro del catálogo.")

def devolver_libro():
    """
    Procesa la devolución de un libro y calcula multas.
    
    Args:
        Ninguno.
        
    Returns:
        Nada.
    """
    global acumulador_multas_global
    
    dni = int(input("\nIngrese el DNI del usuario que devuelve el libro: "))
    
    usuario_actual = None
    for u in usuarios_registrados:
        if u["dni"] == dni:
            usuario_actual = u
            break
            
    if usuario_actual == None:
        print("Usuario no encontrado.")
    else:
        if usuario_actual["tiene_libro"] == False:
            print("Este usuario no tiene ningún libro prestado actualmente.")
        else:
            id_prestado = usuario_actual["id_libro_prestado"]
            
            dias_atraso = int(input("Ingrese cantidad de días de atraso (0 si está en fecha): "))
            
            # Validación con while
            while dias_atraso < 0: 
                print("Los días de atraso no pueden ser negativos.")
                dias_atraso = int(input("Ingrese cantidad de días de atraso (0 si está en fecha): "))
            
            # Proceso de multa
            if dias_atraso > 0:
                multa = dias_atraso * 50.0
                usuario_actual["multa_total"] += multa # Acumulador del usuario
                acumulador_multas_global += multa # Acumulador global
                print(f"Se aplicó una multa de ${multa} por atraso.")
            
            # Actualizar estados
            usuario_actual["tiene_libro"] = False
            usuario_actual["id_libro_prestado"] = 0
            
            for libro in catalogo_libros:
                if libro["id"] == id_prestado:
                    libro["disponible"] = True
                    print(f"El libro '{libro['titulo']}' fue devuelto correctamente.")
                    break

def guardar_estadisticas():
    """
    Guarda las estadísticas en un archivo de texto y busca el libro más leído.
    
    Args:
        Ninguno.
        
    Returns:
        Nada.
    """
    # Algoritmo de Búsqueda del Mayor (Maximo)
    max_prestamos = -1
    libro_top = ""
    
    for libro in catalogo_libros:
        if libro["cant_prestamos"] > max_prestamos:
            max_prestamos = libro["cant_prestamos"]
            libro_top = libro["titulo"]
            
    print("\n--- ESTADÍSTICAS ---")
    print(f"Préstamos totales realizados: {contador_prestamos_global}")
    print(f"Recaudación total por multas: ${acumulador_multas_global}")
    if contador_prestamos_global > 0:
        print(f"Libro más solicitado: {libro_top} ({max_prestamos} préstamos)")
    else:
        print("Aún no se han prestado libros.")
            
    # Manejo de archivos txt (Guía Archivos - Pág 5)
    with open("informe_biblioteca.txt", "w") as archivo:
        archivo.write("ESTADISTICAS DE LA BIBLIOTECA\n")
        archivo.write("-----------------------------\n")
        archivo.write(f"Total de prestamos historicos: {contador_prestamos_global}\n")
        archivo.write(f"Total de dinero recaudado por multas: ${acumulador_multas_global}\n")
        if contador_prestamos_global > 0:
            archivo.write(f"Libro mas solicitado: {libro_top} ({max_prestamos} prestamos)\n")
            
    print("\n(Las estadísticas han sido guardadas en el archivo 'informe_biblioteca.txt')")

def menu_principal():
    """
    Despliega el menú principal y gestiona las opciones.
    
    Args:
        Ninguno.
        
    Returns:
        Nada.
    """
    # Bucle infinito controlado por un break (Módulo 2 - Pág 75)
    while True:
        print("\n======================================")
        print("       SISTEMA DE BIBLIOTECA UTN")
        print("======================================")
        print("1. Registrar Usuario")
        print("2. Ver Catálogo")
        print("3. Prestar Libro")
        print("4. Devolver Libro")
        print("5. Mostrar y Generar Informe de Estadísticas (TXT)")
        print("6. Salir")
        
        opcion = input("Elija una opción (1-6): ")
        
        # Condicional Alternativo Múltiple (Módulo 2 - Pág 24)
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            mostrar_catalogo()
        elif opcion == "3":
            prestar_libro()
        elif opcion == "4":
            devolver_libro()
        elif opcion == "5":
            guardar_estadisticas()
        elif opcion == "6":
            print("Saliendo del programa. ¡Hasta luego!")
            break 
        else:
            print("Opción inválida. Intente de nuevo.")

# Punto de inicio del programa
menu_principal()