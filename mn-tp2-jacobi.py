import numpy as np


# Funciones auxiliares
def ingresar_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Error: Debes ingresar un número entero válido.")


def ingresar_decimal(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Error: Debes ingresar un número decimal válido.")


def seleccionar_ingreso_data():
    o = 0
    while not 0 < o < 4:
        o = ingresar_entero("Ingrese:\n"
                            "1: para llenar la matriz con valores aleatorios\n"
                            "2: para ingresar de manera manual\n"
                            "3: para trabajar con una matriz predefinida de 3x3 y un vector de n=3\n"
                            "Seleccione una opcion: ")
    return o


def ingresar_tolerancia():
    t = -1
    print(f"Ingrese el valor de precisión de decimales deseados del 0 a 9")
    print("Nota: a mayor precisión se requerirán mayor cantidad de iteraciones")
    print("Ejemplos:")
    print("0 -> 0 (Precisión Baja)")
    print("1 -> 0.1")
    print("2 -> 0.01")
    print("3 -> 0.001")
    print(".....")
    print("9 -> 1e-9 (Precisión Alta)")
    while not (0 <= t < 10):
        t = ingresar_entero("Opción: ")
    return float(1 / (10 ** t))


def es_matriz_con_diagonal_dominante(m):
    diagonal = np.abs(np.diag(m))  # Extraer los elementos de la diagonal principal de la matriz
    suma_fila = np.sum(np.abs(m), axis=1)  # Sumar los valores absolutos de cada fila

    # Verificar si el valor absoluto de los elementos en la diagonal principal es mayor o igual que la suma
    # de los valores absolutos de los demás elementos en la misma fila
    return np.all(diagonal >= suma_fila - diagonal)


def es_matriz_singular(m):
    return np.linalg.det(m) != 0


def ingreso_datos_aleatorio(n):
    i_maxima = 1000

    print()
    print("Selecciono el modo de ingreso con valores aleatorios")
    print(f"Para llenar la matriz de {n} x {n} elementos para iterar en el método Jacobi")
    print(f"se generará, en lo posible, una matriz con diagonal dominante en {i_maxima} intentos como máximo.")
    print()

    MIN_VALUE = -10
    MAX_VALUE = 10
    print(f"Valores mínimos y máximos seteados por defecto en {MIN_VALUE} y {MAX_VALUE} respectivamente")
    if input("Ingrese 'ENTER' para mantenerlos o 'R' para redefinir").upper() == "R":
        it_minmax = 0
        ok_minmax = False
        while not ok_minmax:
            if it_minmax > 0:
                print("Error: el valor mínimo debe ser menor al máximo!")
            MIN_VALUE = ingresar_entero("Ingrese un valor entero para el valor MÍNIMO del generador aleatorio")
            MAX_VALUE = ingresar_entero("Ingrese un valor entero para el valor MÁXIMO del generador aleatorio")
            it_minmax += 1
            ok_minmax = MIN_VALUE < MAX_VALUE

    i = 0
    es_diagonal_dominante = False
    while not es_diagonal_dominante and i < i_maxima:
        A = np.random.randint(MIN_VALUE, MAX_VALUE, size=(n, n))
        b = np.random.randint(MIN_VALUE, MAX_VALUE, size=n)
        A = np.where(A == 0, MAX_VALUE, A)
        es_diagonal_dominante = es_matriz_con_diagonal_dominante(A)
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
    print("Selecciono el modo de ingreso manual")
    ingreso = "N"

    while ingreso == "N":
        ingreso = ""
        A = np.zeros((n, n))
        print("\nIngreso de elementos de la matriz A:")
        print("Notas: no se permite ingresar ningún valor en 0. Además luego de ingresar la matriz se verificara\n"
              "que su determinante no sea 0")
        for i in range(n):
            for j in range(n):
                while A[i, j] == 0:
                    A[i, j] = ingresar_decimal(f"Ingrese el elemento de la matriz: [fila {i + 1} / columna {j + 1}]: ")
                    if A[i, j] == 0:
                        print("DEBE INGRESAR UN VALOR DISTINTO DE CERO!\nIntente nuevamente!")

        # Validacion de matriz
        if not es_matriz_singular(A):
            print("*** Error ***\nNo se puede continuar con la matriz ingresada debido a que el determinante es 0")
            print("Ingrese la matriz nuevamente")
            ingreso = "N"
        else:
            if not es_matriz_con_diagonal_dominante(A):
                print("\n*** Atención: la matriz ingresada no contiene una diagonal dominante ***")
                print("*** Es posible que el método Jacobi no converga en un resultado ***\n")
            else:
                print("\nLa matriz ingresada tiene diagonal dominante, es ideal para iterar en Jacobi\n")

        # Muestra matriz ingresada y permite reingresar
        print("La matriz ingresada es:")
        print(A, "\n")
        if ingreso != "N":
            print("Presiones ENTER para continuar o 'N' para ingresar nuevamente")
            ingreso = str(input()).upper()

    b = np.zeros(n)
    print("\nIngreso de elementos del vector b:")
    for i in range(n):
        b[i] = ingresar_decimal(f"Ingrese el valor {i + 1} para el vector b: ")

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
    # Imprimir los datos iniciales del sistema de ecuaciones
    print("===========================================================================================")
    print("-------- Método de Jacobi - Solución de un sistema de ecuaciones lineales -----------------")
    print("-------------------------------------------------------------------------------------------")
    print("Matriz (A) ingresada:")
    print(A, "\n")
    print("Vector de términos independientes (b) ingresado:")
    for j in range(len(b)):
        print(f" x{j + 1} = {b[j]}", end="\t")
    print()
    print()
    print(f"Valor de tolerancia definido: {tol}")
    input("\nPresione ENTER para comenzar las iteraciones\n")

    # Asignacion e inicializacion de variables a utilizar para iterar en el proceso
    # de estimacion de los resultados de v

    # Inicializacion de variables a retornar
    H = []  # Se inicializa una lista para guardar los valores de cada iteracion
    norm = []  # Se inicializa una lista para guardar el valor de la norma en cada iteración
    # En ambas listas el índice será el numero de iteración
    v = np.zeros(len(b))  # v será el vector solución
    msg = ""  # esta funcion ademas de devolver resultados se diseñó para que recolecte un mensaje como string
    # para saber si se logro converger en un resultado o se llegó a la cantidad máxima de iteraciones dadas

    # Juego de datos para utilizar en la fórmula de Jacobi
    D = np.diag(np.diag(A))  # D sera la matriz diagonal de A, la cual contendra unicamente los elementos
    # diagonal de A y el resto ceros
    LpU = A - D  # dada la fórmula de Jacobi puedo redefinir L + U = A - D
    # para luego utilizar en las operaciones como -LpU y trabajar en cada iteracion
    D_inv = np.linalg.inv(D)  # Genero la matriz diagonal inversa

    for i in range(k):
        x_temp = v
        e = 1

        # Calculo con la formula de Jacobi la solucion temporal
        v = np.dot(D_inv, np.dot(-LpU, x_temp)) + np.dot(D_inv, b)
        # Guardo en la lista
        H.append(v)

        # Calculo norma y guardo en la lista
        e = np.linalg.norm(v - x_temp)
        norm.append(e)

        if i == k - 1:
            msg = f"Lamentablemente no se logra converger a un resultado dentro\n" \
                  f"de la tolerancia definida en {tol} en {k} iteraciones"

        if e < tol:
            msg = f"Se logró converger en un resultado con sólo {i + 1} de {k} iteraciones"
            return H, norm, v, msg

    return H, norm, v, msg


def mostrar_resultados(H, norm, v, message, tol, A, b):
    # Funcion mostrar_resultados:
    # Recibira:
    # H -> Lista de vectores resultados temporales
    # norm -> lista de valores de la norma en cada iteracion
    # v -> el vector resultado que se llego a obtener
    # message -> el mensaje devuelto por la funcion jacobi()
    # tol -> el valore de tolerancia o error abs seteado para calcular en cuantos decimales se formatearan los valores
    # e -> la solucion exacta para mostrar
    redondeo_decimales = abs(int(np.log10(tol)))  # n decimales para usar en redondeo para mostrar resultados
    n = len(v)
    e = np.linalg.solve(A, b)
    print("================================ Emision de Resultados ===================================")

    print("\n\t\t\t* * * * * * Vectores resultado obtenidos * * * * * *\t\t\t")
    print("Aproximación de las soluciones")
    for i in range(len(norm)):
        print(f"Iteración {i + 1}")
        for j in range(n):
            print(f" x{j + 1} = {round(H[i][j], redondeo_decimales)}", end="\t")
        if i != 0:
            print("\nNorma: ", round(norm[i], redondeo_decimales), end="\t")
        print("\n--------------------------------------------------------------------------------")
    print()
    print("* * * * * * Valores aproximados de las incógnitas obtenidas por método de Jacobi * * * * * *")
    print(message)
    print("\nEl vector de resultados es:")
    for i in range(n):
        print(f" x{i + 1} = {round(v[i], redondeo_decimales)}", end="\t")
    print("\nSolucion exacta con solve():")
    for i in range(n):
        print(f" x{i + 1} = {round(e[i], redondeo_decimales)}", end="\t")
    dif_prom = 0
    for i in range(n):
        dif_prom += e[i] - v[i]
    if dif_prom == float(0):
        print("\n\nEl resultado de iterar con Jacobi coincide con la solución exacta con solve()")
    else:
        print("\n\nDiferencia promedio: ", dif_prom / n)
    print("\n********************** Proceso de emisión de resultados finalizado ************************")
    print("===========================================================================================")


# Menu del programa
def menu():
    n = 0
    option = seleccionar_ingreso_data()
    print()
    if 0 < option <= 2:
        while n < 1:
            n = ingresar_entero("Ingrese una dimension (n) para la matriz de (n x n) para trabajar:")
        A = np.zeros((n, n))
        b = np.zeros(n)

        if option == 1:
            A, b = ingreso_datos_aleatorio(n)

        elif option == 2:
            A, b = ingreso_datos_manual(n)

    else:
        print("Selecciono trabajar con una matriz preestablecida de 3 x 3")
        A, b = ingreso_datos_fijo()
        n = len(b)
    tol = ingresar_tolerancia()
    k = 0
    while not k > 0:
        k = ingresar_entero("Ingrese el número de iteraciones (k): ")
    H, norm, v, message = jacobi(A, b, k, tol)  # Aplica el método de Jacobi con los datos ingresados
    mostrar_resultados(H, norm, v, message, tol, A, b)


print("********************************************************")
print("* Universidad Nacional de San Martin                   *")
print("* Escuela de Ciencia y Tecnologia                      *")
print("* Trabajo Practico 2 - Métodos Numericos               *")
print("* Alumno: Nava, Alejandro Daniel                       *")
print("* DNI: 32956059                                        *")
print("* Carrera: TPI                                         *")
print("********************************************************")

print("\nComenzamos!\n")

again = True
while again:
    menu()
    opc = str(input("\nIngrese 'ENTER' para volver a empezar o 'X' para salir del programa").upper())
    if opc == "X":
        again = False

print("********************** Trabajo Practico No.2 Metodos Numericos Finalizado ************************")
print("==================================================================================================")
print("Muchas gracias por utilizar!")
print("Atte. Alejandro Daniel Nava")