# Trabajo Práctico 2 - Métodos Numéricos

Universidad Nacional de San Martín  
Escuela de Ciencia y Tecnología

Alumno: Nava, Alejandro Daniel  
DNI: 32956059  
Carrera: TPI

## Descripción del programa

El programa es una implementación de métodos numéricos para resolver sistemas de ecuaciones utilizando el método de Jacobi. A continuación se detalla su funcionamiento:

1. El programa comienza mostrando un menú inicial en el que el usuario puede elegir entre tres opciones para ingresar los datos del sistema de ecuaciones:
   - Llenar la matriz con valores aleatorios.
   - Ingresar manualmente la matriz y el vector de términos independientes.
   - Trabajar con una matriz predefinida de 3x3 y un vector de n=3.

2. Después de seleccionar la opción de ingreso de datos, se solicita al usuario ingresar la tolerancia deseada. La tolerancia determina la precisión de los decimales en el resultado y afecta la cantidad de iteraciones necesarias para converger a una solución.

3. A continuación, se le pide al usuario ingresar el número máximo de iteraciones permitidas.

4. Dependiendo de la opción seleccionada, el programa generará una matriz con valores aleatorios, solicitará al usuario que ingrese manualmente la matriz y el vector de términos independientes, o utilizará una matriz predefinida.

5. Antes de comenzar las iteraciones del método de Jacobi, se muestran los datos iniciales del sistema de ecuaciones, incluyendo:
   - La matriz ingresada.
   - El vector de términos independientes.
   - La tolerancia establecida.

6. A continuación, se ejecuta el método de Jacobi para estimar las soluciones del sistema de ecuaciones. Se realiza un bucle iterativo hasta que se cumpla alguna de las siguientes condiciones:
   - Se alcanza la cantidad máxima de iteraciones especificada.
   - La diferencia entre dos iteraciones consecutivas es menor que la tolerancia establecida.

7. Después de las iteraciones, se muestran los resultados obtenidos. Esto incluye:
   - Los vectores resultado obtenidos en cada iteración.
   - La norma correspondiente a cada iteración.
   - El vector solución final obtenido por el método de Jacobi.
   - El vector solución exacta calculado utilizando el método `linalg.solve()` de NumPy.

8. El programa también verifica si la diferencia entre el vector solución exacta y el vector solución obtenido por el método de Jacobi es igual a cero. Si es así, se muestra un mensaje indicando que los resultados coinciden.

9. Después de mostrar los resultados, se ofrece al usuario la opción de ejecutar el programa nuevamente o salir.

10. El programa valida todas las entradas de datos, es decir, se verifica que se solicite un número decimal, un entero o una opción válida, para evitar errores en el proceso.

## Modo aleatorio

- Se permite al usuario definir los valores mínimos y máximos para la generación de valores en la matriz. En caso de no querer redefinir, se utilizan valores por defecto de -10 y 10.
- El programa está diseñado para generar una matriz con diagonal dominante. En caso de no lograrlo después de una cantidad máxima de intentos, se informa al usuario.

## Modo manual

- Al ingresar la matriz, se verifican 2 condiciones:
  1. Que la matriz sea de diagonal dominante. Este caso no es excluyente, pero se informa al usuario.
  2. Que la matriz no sea singular. Se evalúa calculando que el determinante sea distinto de cero. En caso contrario, se obliga al usuario a volver a ingresar la matriz.

## Validación de entradas

El programa valida todas las entradas de datos para asegurarse de que sean números decimales, enteros u opciones válidas.

