import numpy as np
from scipy.linalg import solve

MIN_VALUE = -10
MAX_VALUE = 10


def seleccionar_ingreso_data():
    o = 0
    while o != 1 and o != 2 and o != 3:
        o = int(input("Ingrese:\n"
                      "1: para llenar la matriz con valores aleatorios\n"
                      "2: para ingresar de manera manual\n"
                      "3: para trabajar con datos preestablecidos\n"
                      "Seleccione una opcion: "))
    return o


def ingreso_datos_aleatorio(n):
    m = np.random.randint(MIN_VALUE, MAX_VALUE, size=(n, n))
    v = np.random.randint(MIN_VALUE, MAX_VALUE, size=n)
    return m, v


def ingreso_datos_manual(n):
    print()


def ingreso_datos_fijo(n):
    # Matriz de coeficientes
    A = np.array([[4, 1, -1],
                  [3, 5, 1],
                  [1, -2, 6]])

    # Vector de términos independientes
    b = [5, -2, 7]
    return A, b


def jacobi(A, b, k):
    tolerance = 1e-3
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
        x_new = v[i + 1]  # Aproximación actualizada de las soluciones

        norm[i] = np.linalg.norm(x_new - x)  # Cálculo de la norma del error en cada iteración
        x = x_new  # Actualizar la aproximación de las soluciones

        if norm[i] < tolerance:
            break  # Detener las iteraciones si el error es menor que la tolerancia

    return H, norm, v


def mostrar_resultados(H, norm, v):
    for i in range(len(H)):
        print("\nMatriz de iteración H:")
        print(f"Iteración {i + 1}:")
        print(H[i])
        print()
        print("Norma de cada iteración:")
        print(f"Iteración {i + 1}: {norm[i]}")

    print(f"Solucion Jacobi:\n", v)


print("********************************************************")
print("* Trabajo Practico 2 - Metodos Numericos               *")
print("* Alumno: Nava, Alejandro Daniel                       *")
print("* DNI: 32956059                                        *")
print("********************************************************")

print("\nComenzamos!\n")
n = 0
while n < 2:
    n = int(input("Ingrese una dimension (n) mayor a 2 para la matriz de (n x n): "))
A = np.zeros((n, n))
b = np.zeros(n)
k = 0
while k <= 0:
    k = int(input("Ingrese el número de iteraciones (k): "))

option = seleccionar_ingreso_data()

if option == 1:
    print("Selecciono el modo Aleatorio")
    A, b = ingreso_datos_aleatorio(n)
elif option == 2:
    print("Selecciono el modo Manual")
else:
    print("Selecciono el modo Fijo")
    A, b = ingreso_datos_fijo(n)

print("La matriz es:\n", A)
print("El vector es:\n", b)

H, norm, v = jacobi(A, b, k)  # Aplicar el método de Jacobi

mostrar_resultados(H, norm, v)

print("Solucion exacta con solve():\n", solve(A, b))


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