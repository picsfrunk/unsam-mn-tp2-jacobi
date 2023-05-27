import math
import numpy as np
from scipy.linalg import solve


# Funciones auxiliares
def ingresar_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Error: Debes ingresar un número entero válido.")


def seleccionar_ingreso_data():
    o = 0
    while not 0 < o < 4:
        o = ingresar_entero("Ingrese:\n"
                            "1: para llenar la matriz con valores aleatorios\n"
                            "2: para ingresar de manera manual\n"
                            "3: para trabajar con datos preestablecidos\n"
                            "Seleccione una opcion: ")
    return o


def verif_diagonal_dominante(M):
    diagonal = np.abs(np.diag(M))  # Extraer los elementos de la diagonal principal de la matriz
    suma_fila = np.sum(np.abs(M), axis=1)  # Sumar los valores absolutos de cada fila

    # Verificar si el valor absoluto de los elementos en la diagonal principal es mayor o igual que la suma
    # de los valores absolutos de los demás elementos en la misma fila
    return np.all(diagonal >= suma_fila - diagonal)


def ingreso_datos_aleatorio(n):
    i_maxima = 500

    print()
    print("Selecciono el modo de ingreso con valores aleatorios")
    print(f"Para llenar la matriz de {n} x {n} elementos para iterar en el método Jacobi")
    print(f"se intentará, en lo posible, generar una matriz con diagonal dominante en {i_maxima} intentos.")
    print()

    MIN_VALUE = -5
    MAX_VALUE = 5
    print(f"Valores mínimos y máximos seteados por defecto en {MIN_VALUE} y {MAX_VALUE} respectivamente")
    if input("Ingrese 'ENTER' para mantenerlos o 'r' para redefinir").upper() == "R":
        MIN_VALUE = ingresar_entero("Ingrese un valor entero para el valor MÍNIMO del generador aleatorio")
        MAX_VALUE = ingresar_entero("Ingrese un valor entero para el valor MÁXIMO del generador aleatorio")

    i = 0
    es_diagonal_dominante = False
    while not es_diagonal_dominante and i < i_maxima:
        A = np.random.randint(MIN_VALUE, MAX_VALUE, size=(n, n))
        b = np.random.randint(MIN_VALUE, MAX_VALUE, size=n)
        A = np.where(A == 0, 1, A)
        es_diagonal_dominante = verif_diagonal_dominante(A)
        i += 1
        if i < i_maxima:
            print(f"En {i} intento(s)", end="\r")
    print()
    if es_diagonal_dominante:
        print("se generó una matriz con diagonal dominante")
    else:
        print("No se logró generar una matriz con diagonal dominante")
    return A, b


def ingreso_datos_manual(n):
    A = np.zeros((n, n))
    b = np.zeros(n)

    print("Ingreso de elementos de la matriz A:")
    for i in range(n):
        for j in range(n):
            A[i, j] = float(input(f"Ingrese el elemento A[{i + 1}, {j + 1}]: "))

    print("\nIngreso de elementos del vector b:")
    for i in range(n):
        b[i] = float(input(f"Ingrese el elemento b[{i + 1}]: "))

    return A, b


def ingreso_datos_fijo():
    # Matriz de coeficientes
    A = np.array([[4, 1, -1],
                  [3, 5, 1],
                  [1, -2, 6]])

    # Vector de términos independientes
    b = [5, -2, 7]
    return A, b


def jacobi(A, b, k, tol):
    # Asignacion e inicializacion de variables a utilizar para iterar en el proceso
    # de estimacion de los resultados de v
    D = np.diag(np.diag(A))  # D sera la matriz diagonal de A, la cual contendra unicamente los elementos
    # diagonal de A y el resto ceros

    LpU = A - D  # dada la fórmula de Jacobi puedo redefinir L + U = A - D
    # para luego utilizar en las operaciones como -LpU y trabajar en cada iteracion

    v = np.zeros(n)  # v será el vector solución

    redondeo_decimales = abs(int(math.log10(tol))) + 1

    H = []  # Se inicializa una lista para guardar los valores de cada iteracion
    norm = []  # Se inicializa una lista para guardar el valor de la norma en cada iteración
    # En ambas listas el índice será el numero de iteración

    message = ""  # esta funcion ademas de devolver resultados se diseñó para que recolecte un mensaje como string
    # para saber si se logro converger en un resultado o se llegó a la cantidad máxima de iteraciones dadas

    # Imprimir los datos iniciales del sistema de ecuaciones
    print("===========================================================================================")
    print("-------- Método de Jacobi - Solución de un sistema de ecuaciones lineales -----------------")
    print("-------------------------------------------------------------------------------------------")
    print("Matriz (A) ingresada:")
    for i in range(len(A)):
        print('\t\t\t\t\t\t', end='\t')
        for j in range(len(A)):
            print(np.round(A[i][j], redondeo_decimales), end='\t')
        print()
    print("\nVector de términos independientes (b) ingresado:")
    print('\t\t\t\t', end='\t')
    for j in range(len(b)):
        print(f" x{j + 1} = {np.round(b[j], redondeo_decimales)}", end="\t")
    print()
    print()
    print(f"Valor de tolerancia definido: {np.round(tol, redondeo_decimales)}")
    print()

    for i in range(k):
        D_inv = np.linalg.inv(D)
        x_temp = v
        e = 1

        v = np.dot(D_inv, np.dot(-LpU, x_temp)) + np.dot(D_inv, b)
        H.append(v)

        e = np.linalg.norm(v - x_temp)
        norm.append(e)

        if i == k - 1:
            message = f"Lamentablemente no se logra converger a un resultado con\n" \
                      f"la tolerancia definida de {tol} en {k} iteraciones"

        if e < tol:
            message = f"Se logró converger en un resultado con sólo {i + 1} de {k} iteraciones"
            return H, norm, v, message

    return H, norm, v, message


# Funcion mostrar_resultados:
# Recibira:
# H -> Lista de vectores resultados temporales
# norm -> lista de valores de la norma en cada iteracion
# v -> el vector resultado que se llego a obtener
# message -> el mensaje devuelto por la funcion jacobi()
# tol -> el valore de tolerancia o error abs seteado para calcular en cuantos decimales se formatearan los valores
# e -> la solucion exacta para mostrar
# n -> la dimension ingresada para los ciclos for para emitir los vectores
def mostrar_resultados(H, norm, v, message, tol, e, n):
    redondeo_decimales = abs(int(math.log10(tol))) + 1
    print("================================ Emision de Resultados ===================================")

    print("\n* Vectores resultados obtenidos *")
    for i in range(len(norm)):
        # print("--------------------------------------------------------------------------------")
        print(f"Aproximación de las soluciones en iteración {i + 1}:")
        for j in range(n):
            print(f" x{j + 1} = {np.round(H[i][j], redondeo_decimales)}", end="\t")
        if i != 0:
            print("\nNorma: ", np.round(norm[i], redondeo_decimales), end="\t")
        print("\n--------------------------------------------------------------------------------")
    print()
    print("* Valores aproximados de las incógnitas obtenidas por método de Jacobi *")
    print(message)
    print(f"\nCon un error absoluto menor a {np.round(norm[-1], redondeo_decimales + 1)}")
    print("El vector de resultados es:")
    for i in range(n):
        print(f" x{i + 1} = {np.round(v[i], redondeo_decimales)}", end="\t")
    print("\n--------------------------------------------------------------------------------")
    print("Solucion exacta con solve():")
    for i in range(n):
        print(f" x{i + 1} = {np.round(e[i], redondeo_decimales)}", end="\t")
    print("\n--------------------------------------------------------------------------------")
    print("Diferencia:")
    for i in range(n):
        print(f" x{i + 1} = {np.round(e[i] - v[i], redondeo_decimales)}", end="\t")
    print()

    print("********************** Proceso de emisión de resultados finalizado ************************")
    print("===========================================================================================")


print("********************************************************")
print("* Universidad Nacional de San Martin                   *")
print("* Escuela de Ciencia y Tecnologia                      *")
print("* Trabajo Practico 2 - Metodos Numericos               *")
print("* Alumno: Nava, Alejandro Daniel                       *")
print("* DNI: 32956059                                        *")
print("********************************************************")

print("\nComenzamos!\n")

again = True

while again:
    n = 0
    option = seleccionar_ingreso_data()
    print()

    if option == 1 or option == 2:
        while n < 1:
            n = ingresar_entero("Ingrese una dimension (n) para la matriz de (n x n):")
        A = np.zeros((n, n))
        b = np.zeros(n)
        if option == 1:
            A, b = ingreso_datos_aleatorio(n)

        elif option == 2:
            print("Selecciono el modo Manual")
            A, b = ingreso_datos_manual(n)

    else:
        print("Selecciono trabajar con una matriz preestablecida")
        A, b = ingreso_datos_fijo()
        n = len(b)

    set_tol = -1
    print(f"Ingrese la opción para el valor de precisión deseado")
    print("Nota: a mayor precisión se requerirán mayor cantidad de iteraciones")
    print("0 -> 0 (Precisión Baja)")
    print("1 -> 0.1")
    print("2 -> 0.01")
    print("3 -> 0.001")
    print(".....")
    print("9 -> 1e-9 (Precisión Alta)")

    while not (0 <= set_tol < 10):
        set_tol = ingresar_entero("Opción: ")

    tol = float(1 / (10 ** set_tol))

    k = 0
    while k <= 0:
        k = ingresar_entero("Ingrese el número de iteraciones (k): ")

    H, norm, v, message = jacobi(A, b, k, tol)  # Aplicar el método de Jacobi
    solve_solution = solve(A, b)
    mostrar_resultados(H, norm, v, message, tol, solve_solution, n)

    print()
    opc = str(input("Ingrese 'ENTER' para volver a empezar o 'x' para salir del programa").upper())
    if opc == "X":
        again = False

print("********************** Trabajo Practico No.2 Metodos Numericos Finalizado ************************")
print("==================================================================================================")
print("Muchas gracias por utilizar!")
print("Atte. Alejandro Daniel Nava")

# En el mismo lenguaje de programación que usaron para el mini TP 1 (preferentemente), implementar un programa
# o script que lea un número natural n >= 1, una matriz de números reales A de n x n, un vector b de n números
# reales y un número natural k >= 0. El programa deberá luego mostrar la matriz de iteración H, su norma y el
# vector v del método de Jacobi con el fin de buscar una solución aproximada del sistema de ecuaciones lineales Ax = b,
# y deberá hacer k iteraciones del método para este sistema lineal mostrando los vectores que resulten
# en los distintos pasos. Se informará cualquier error o eventualidad que impida calcular lo pedido.
# La entrada y la salida del programa podrán ser las estándares o bien archivos, a elección de Uds.
# (En forma opcional, comparar la solución numérica obtenida con la solución mediante algún método exacto,
# para lo cual se permite tomar este último de un módulo o biblioteca de métodos numéricos. Si se usa R,
# por ejemplo, se puede directamente usar Solve(A, b).)
# Entrega: código comentado y ejemplos capturados.
# (Esta tarea queda como opcional.)
