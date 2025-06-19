import math
import pandas as pd

def leer_temperaturas(nombre_archivo):
    with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()[1:]  # Ignorar primera línea
        temperaturas = []
        for linea in lineas:
            try:
                t = float(linea.strip())
                temperaturas.append(t)
            except ValueError:
                continue  # Ignora líneas que no se pueden convertir
    return temperaturas

def clasificar_estado(temp):
    if temp < 11:
        return 0  # Frío
    elif temp < 19:
        return 1  # Templado
    else:
        return 2  # Cálido

def matriz_canal(entradas,salidas):
    """
        Construye la matriz de canal a partir de dos secuencias:
          entradas: secuencia de estados transmitidos (T2),
          salidas : secuencia de estados recibidos (T4, con ruido).

        La función devuelve una matriz 3x3(ya que tenemos 3 estados) donde cada elemento
          canal[i][j] = P(salida = j / entrada = i)
        """
    # Inicializamos una matriz 3x3 con ceros donde las filas son salidas y columnas son entradas
    canal = [[0 for _ in range(3)] for _ in range(3)]

    # Contamos las ocurrencias de cada par (entrada, salida)
    for entrada, salida in zip(entradas, salidas):
        canal[salida][entrada] += 1

    # Normalizamos por columna, ya que cada columna corresponde a una entrada
    for entrada in range(3):
        suma_col = sum(canal[s][entrada] for s in range(3))
        if suma_col > 0:
            for salida in range(3):
                canal[salida][entrada] = round(canal[salida][entrada] / suma_col, 3)
        else:
            for salida in range(3):
                canal[salida][entrada] = 0.0

    return canal

def imprimir_matriz_canal(M):
    df = pd.DataFrame(M, columns=['Frío', 'Templado', 'Cálido'], index=['Frío', 'Templado', 'Cálido'])
    print(f"\nMatriz Del canal:\n")
    print(df.to_string(float_format="{:.3f}".format))

def calcular_p_x(estados):
    total = len(estados)
    counts = [0, 0, 0]
    for s in estados:
        counts[s] += 1
    p_x = [count / total for count in counts]
    return p_x

def ruido_canal(canal, p_x):
    base = 2
    H_Y_given_X = 0.0
    n = len(p_x)  # Número de estados de entrada
    for x in range(n):
        H_Y_given_x = 0.0
        # Para cada estado de salida
        for y in range(len(canal)):
            p_y_given_x = canal[y][x]
            if p_y_given_x > 0:
                H_Y_given_x -= p_y_given_x * math.log(p_y_given_x, base)
        # Ponderamos por la probabilidad de la entrada
        H_Y_given_X += p_x[x] * H_Y_given_x
    return H_Y_given_X

def info_mutua(canal, p_x):
    base = 2
    m = len(canal)  # Número de estados de salida
    n = len(p_x)  # Número de estados de entrada
    p_y = [0.0] * m
    # Calcular la distribución marginal de la salida p(y)
    for y in range(m):
        for x in range(n):
            p_y[y] += p_x[x] * canal[y][x]

    I = 0.0
    for x in range(n):
        for y in range(m):
            p_y_given_x = canal[y][x]
            if p_y_given_x > 0 and p_y[y] > 0:
                I += p_x[x] * p_y_given_x * math.log(p_y_given_x / p_y[y], base)
    return I

def pausar():
    input("\nPresioná Enter para finalizar...")


# Archivos
archivo2 = "data/temperature_Melbourne_celsius.csv"
archivo4=  "data/temperature_Melbourne_celsius_ruidoso.csv"

# Leer los datos
datos_melbourne = leer_temperaturas(archivo2)
datos_melbourne_ruidoso=leer_temperaturas(archivo4)

estados_melbourne = [clasificar_estado(t) for t in datos_melbourne]
estados_melbourne_ruidoso=[clasificar_estado(t) for t in datos_melbourne_ruidoso]

M_canal=matriz_canal(estados_melbourne,estados_melbourne_ruidoso)
imprimir_matriz_canal(M_canal)

p_x=calcular_p_x(estados_melbourne)
print("\nDistribución de la entrada p(x):")
print(f"Frío: {p_x[0]:.3f}, Templado: {p_x[1]:.3f}, Cálido: {p_x[2]:.3f}")
ruido = ruido_canal(M_canal, p_x)
I_mutua = info_mutua(M_canal, p_x)
print(f"\nRuido del canal (H(Y/X)): {ruido:.3f} bits")
print(f"Información mutua (I(X,Y)): {I_mutua:.3f} bits")
pausar()