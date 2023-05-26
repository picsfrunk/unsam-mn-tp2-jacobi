import numpy as np
from scipy.linalg import solve

MIN_VALUE = -3
MAX_VALUE = 7


def seleccionar_ingreso_data():
    o = 0
    while o != 1 and o != 2 and o != 3:
        o = int(input("Ingrese:\n"
                      "1: para llenar la matriz con valores aleatorios\n"
                      "2: para ingresar de manera manual\n"
                      "3: para trabajar con datos preestablecidos\n"
                      "Seleccione una opcion: "))
    return o


def verif_diagonal_dominante(M):
    diagonal = np.abs(np.diag(M))  # Extraer los elementos de la diagonal principal de la matriz
    suma_fila = np.sum(np.abs(M), axis=1)  # Sumar los valores absolutos de cada fila

    # Verificar si el valor absoluto de los elementos en la diagonal principal es mayor o igual que la suma
    # de los valores absolutos de los demás elementos en la misma fila
    return np.all(diagonal >= suma_fila - diagonal)


def ingreso_datos_aleatorio(n):
    es_diagonal_dominante = False
    it = 0
    max_it = 300

    while not es_diagonal_dominante and it < max_it:
        A = np.random.randint(MIN_VALUE, MAX_VALUE, size=(n, n))
        b = np.random.randint(MIN_VALUE, MAX_VALUE, size=n)
        A = np.where(A == 0, 1, A)
        es_diagonal_dominante = verif_diagonal_dominante(A)
        it += 1
        if it < max_it:
            print(f"En {it} intento(s)", end="\r")
    print()
    if es_diagonal_dominante:
        print("se genero una matriz con diagonal dominante")
    else:
        print("no se logro generar una matriz con diagonal dominante")
    return A, b


def ingreso_datos_manual(n):
    print()


def ingreso_datos_fijo():
    # Matriz de coeficientes
    A = np.array([[4, 1, -1],
                  [3, 5, 1],
                  [1, -2, 6]])

    # Vector de términos independientes
    b = [5, -2, 7]
    return A, b


def jacobi(A, b, k, tol):
    D = np.diag(np.diag(A))
    LpU = A - D
    n = len(A)
    x = np.zeros(n)
    H = []  # Se inicializa una lista H para guardar los valores de cada iteracion
    norm = []

    # Imprimir los datos iniciales del sistema de ecuaciones
    print("Método de Jacobi - Solución de un sistema de ecuaciones lineales")
    print("----------------------------------------------------------------")
    print("Matriz de coeficientes (A):")
    print(np.round(A, 6))
    print("\nVector de términos independientes (b):")
    print(np.round(b, 6))

    for i in range(k):
        D_inv = np.linalg.inv(D)
        x_temp = x
        e = 1

        x = np.dot(D_inv, np.dot(-LpU, x_temp)) + np.dot(D_inv, b)
        H.append(x)

        e = np.linalg.norm(x - x_temp)
        norm.append(e)

        if i == k - 1:
            message = f"Se llego al maximo de {k} iteraciones, lamentablemente no se logra converger a un resultado"

        if e < tol:
            message = f"Se logro converger en un resultado con sólo {i} iteracion(es)"
            break
    return H, norm, x, message


def mostrar_resultados(H, norm, v, message, tol, e, n):
    # exp_round = int(np.floor(np.log10(np.abs(tol))))
    exp_round = 6
    print("------------------------------ Emision de Resultados ------------------------------")
    print(message)
    print("Valores aproximados de las incógnitas obtenidas por método de Jacobi:")
    for i in range(n):
        print(f" x{i+1} = {np.round(v[i], exp_round)}", end="\t")
    print(f"\nCon un error absoluto de {norm[-1]}")
    print("\nSolucion exacta con solve():")
    for i in range(n):
        print(f" x{i+1} = {np.round(e[i], exp_round)}", end="\t")
    print("\n")
    print("Matrices de iteración obtenidas")
    for i in range(len(norm)):
        # print("\n")
        print("==================================================================================")
        print(f"Aproximación de las soluciones en iteración {i + 1}:")
        for j in range(n):
            print(f" x{j+1} = {np.round(H[i][j], exp_round)}", end="\t")
        print("\n")
        if i != 0:
            print("Norma: ", np.round(norm[i], exp_round))
    print("...")
    print("Proceso de emisión de resultados finalizado")
    print("-----------------------------------------------------------------------------------")


print("********************************************************")
print("* Trabajo Practico 2 - Metodos Numericos               *")
print("* Alumno: Nava, Alejandro Daniel                       *")
print("* DNI: 32956059                                        *")
print("********************************************************")

print("\nComenzamos!\n")

option = seleccionar_ingreso_data()
n = 0

if option == 1:
    print("Selecciono el modo Aleatorio")
    while n < 1:
        n = int(input("Ingrese una dimension (n) para la matriz de (n x n):"))
    A = np.zeros((n, n))
    b = np.zeros(n)
    A, b = ingreso_datos_aleatorio(n)

elif option == 2:
    print("Selecciono el modo Manual")

else:
    print("Selecciono trabajar con una matriz preestablecida")
    A, b = ingreso_datos_fijo()
    n = len(b)

k = 0
while k <= 0:
    k = int(input("Ingrese el número de iteraciones (k):"))

tol = 1e-4
print(f"Error absoluto definido en x < {tol}")

H, norm, v, message = jacobi(A, b, k, tol)  # Aplicar el método de Jacobi
solve_soluction = solve(A, b)
mostrar_resultados(H, norm, v, message, tol, solve_soluction, n)

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
