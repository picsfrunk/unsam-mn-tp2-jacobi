import numpy as np
from scipy.linalg import solve

MIN_VALUE = -2
MAX_VALUE = 2


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

def seleccionar_ingreso_data():
    o = ""
    while o != "A" and o != "M" and o != "F":
        print("Ingrese:\n"
              "'A' para llenar la matriz con valores aleatorios\n"
              "'M' para hacerlo de manera manual\n"
              "Seleccione una opcion: ")
        o = input().upper()
    return o


def ingreso_datos_aleatorio(n):
    m = np.round(np.random.uniform(MIN_VALUE, MAX_VALUE, size=(n, n)), 2)
    v = np.round(np.random.uniform(MIN_VALUE, MAX_VALUE, size=n), 2)
    return m, v


def ingreso_datos_manual():
    print()


def jacobi(A, b, k):
    n = len(b)
    x = np.zeros(n)  # Aproximación inicial de las soluciones
    H = np.zeros((k, n, n))  # Matriz de iteración H
    v = np.zeros((k + 1, n))  # Vector v del método de Jacobi en cada iteración
    norm = np.zeros(k)  # Norma de cada iteración

    for i in range(k):
        if i == 0:
            H[i] = np.diag(np.diag(A))  # Diagonal de la matriz A como primera matriz de iteración
        else:
            H[i] = -np.linalg.inv(np.diag(np.diag(A))) @ (A - np.diag(np.diag(A)))  # Matriz de iteración de Jacobi

        v[i + 1] = H[i] @ v[i] + np.linalg.inv(np.diag(np.diag(A))) @ b  # Cálculo del vector v en cada iteración
        x = v[i + 1]  # Actualización de la aproximación de las soluciones

        norm[i] = np.linalg.norm(A @ x - b)  # Cálculo de la norma de cada iteración

    return H, norm, v


def mostrar_resultados(k, H, norm, v, matriz, vector):
    print("\nMatriz de iteración H:")
    for i in range(k):
        print(f"Iteración {i + 1}:")
        print(H[i])
        print()
    print("Norma de cada iteración:")
    for i in range(k):
        print(f"Iteración {i + 1}: {norm[i]}")
    print("\nVector v del método de Jacobi en cada iteración:")
    for i in range(k + 1):
        print(f"Iteración {i}: {v[i]}")
    e = solve(matriz, vector)
    print("Solucion exacta", e)


print("********************************************************")
print("* Trabajo Practico 2 - Metodos Numericos               *")
print("* Alumno: Nava, Alejandro Daniel                       *")
print("* DNI: 32956059                                        *")
print("********************************************************")

print("\nComenzamos!\n")
n = 0
while n < 2:
    n = int(input("Ingrese una dimension (n) mayor a 2 para la matriz de (n x n): "))
matriz = np.zeros((n, n))
vector = np.zeros(n)
k = 0
while k <= 0:
    k = int(input("Ingrese el número de iteraciones (k): "))

option = seleccionar_ingreso_data()

if option == "A":
    print("Selecciono el modo Aleatorio")
    matriz, vector = ingreso_datos_aleatorio(n)
    print("La matriz es:\n", matriz)
    print("El vector es:\n", vector)
else:
    print("Selecciono el modo Manual")

H, norm, v = jacobi(matriz, vector, k)  # Aplicar el método de Jacobi

mostrar_resultados(k, H, norm, v, matriz, vector)

repetir = ""

while repetir == "S":

    repetir = input("Desea repetir el metodo Jacobi con otra cantidad de iteraciones? S/N: ")
    # if repetir == "N":
    #     break

    while k <= 0:
        k = int(input("Ingrese el número de iteraciones (k): "))

