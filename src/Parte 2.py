import pandas as pd
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

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

# Clasificación de temperaturas en estados F (0), T (1), C (2)
def clasificar_estado(temp):
    if temp < 11:
        return 0  # Frío
    elif temp < 19:
        return 1  # Templado
    else:
        return 2  # Cálido

def MatrizCondicional(estados, M):
    frecuencia = [0, 0, 0]  # llevo la frecuencia de cada estado
    # Contar transiciones entre estados (de orden 1)
    for i in range(len(estados) - 1):
        actual = estados[i]
        siguiente = estados[i + 1]
        M[siguiente][actual] += 1
        frecuencia[actual] += 1

    for j in range(3):  # Estado actual
        for i in range(3):  # Estado siguiente
            if frecuencia[j] > 0:
                # P(i/j)= veces que pase de j a i/veces que aparecio j
                M[i][j] = round(M[i][j] / frecuencia[j], 3)

def converge(v_est, v_ant, e):
    for i in range(len(v_est)):
        if abs(v_est[i] - v_ant[i]) >= e:
            return False
    return True

def sig_estado(estado_actual, M):
    r = random.random()
    acumulado = 0
    for siguiente in range(3):
        acumulado += M[siguiente][estado_actual]
        if r < acumulado:
            return siguiente
    return 2  # Por seguridad (caso extremo donde r ≈ 1)

# Función de Monte Carlo para encontrar el vector estacionario
def montecarlo_vectorEstacionario(M, e, min_it, it):
    N = 0  # Contador de iteraciones
    v_actual = np.zeros(3)  # Vector de visitas (F,T,C)
    v_ant = np.zeros(3)  # Vector anterior
    v_est = np.zeros(3)
    estado = 0
    it[0] = 0

    while not converge(v_est, v_ant, e) or N < min_it:
        # definimos el siguiente estado
        estado = sig_estado(estado, M)

        N += 1
        v_actual[estado] += 1# Incrementamos el contador de visitas al estado actual
        v_ant = v_est.copy()
        v_est[estado] = v_actual[estado] / N
        it[0] += 1
    # Retornamos el vector estacionario
    return v_est

def montecarlo_media_primera_recurrencia(estado, M, e, min_it, it):
    N = 0
    media = 0
    ant_media = 0
    pasos = 0
    it[0] = 0
    estado_aux=estado

    while (abs(ant_media - media) >= e or N < min_it) and it[0] < 10**6:
        estado_aux = sig_estado(estado_aux, M)
        pasos += 1

        if (estado_aux == estado):
            N += 1
            ant_media = media
            media = pasos / N
            pasos = 0
        it[0] += 1
    return media

def imprimir_matriz(M, nombre):
    df = pd.DataFrame(M, columns=['Frío', 'Templado', 'Cálido'], index=['Frío', 'Templado', 'Cálido'])
    print(f"\nMatriz condicional de transición de estados - {nombre}:\n")
    print(df.to_string(float_format="{:.3f}".format))

def grafico_mediaPrimeraRecurrencia(M, archivo, min_it):
    e_values = np.logspace(-7, -1, 25)  # Aumentamos la tolerancia para facilitar convergencia
    iteraciones = {0: [], 1: [], 2: []}
    medias = {0: [], 1: [], 2: []}

    for e in e_values:
        for estado in range(3):
            it = [0, min_it]
            r = montecarlo_media_primera_recurrencia(estado, M, e, min_it, it)
            iteraciones[estado].append(it[0])
            medias[estado].append(r)

    os.makedirs("Graficos", exist_ok=True)
    os.makedirs("Graficos/MonteCarlo media primera recurrencia", exist_ok=True)

    nombre = archivo.split("_")[1].capitalize()

    # Gráfico de Iteraciones vs Tolerancia para los 3 estados
    plt.figure(figsize=(8, 5))
    colores = ["b", "g", "r"]
    estados = ["Frío", "Templado", "Cálido"]

    for estado in range(3):
        plt.semilogx(e_values, iteraciones[estado], marker='o', linestyle='-', color=colores[estado],
                     label=f"Estado {estado} ({estados[estado]})")

    plt.xlabel("Tolerancia (ε)")
    plt.ylabel("Número de iteraciones")
    plt.title(f"Iteraciones vs Tolerancia en Monte Carlo - {nombre}")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Graficos/MonteCarlo media primera recurrencia/{nombre}_iteraciones_vs_tolerancia.png")
    plt.close()

    # Gráfico de Media obtenida vs Tolerancia para los 3 estados
    plt.figure(figsize=(8, 5))

    for estado in range(3):
        plt.semilogx(e_values, medias[estado], marker='x', linestyle='-', color=colores[estado],
                     label=f"Estado {estado} ({estados[estado]})")

    plt.xlabel("Tolerancia (ε)")
    plt.ylabel("Media calculada")
    plt.title(f"Media obtenida vs Tolerancia en Monte Carlo - {nombre}")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Graficos/MonteCarlo media primera recurrencia/{nombre}_media_vs_tolerancia.png")
    plt.close()

def grafico_vectorestacionario(M, archivo, min_it):
    e_values = np.logspace(-7, -2, 25)
    componentes = {0: [], 1: [], 2: []}
    iteraciones = []
    it = [0, min_it]

    for e in e_values:
        v_est = montecarlo_vectorEstacionario(M, e, min_it, it)
        iteraciones.append(it[0])
        for i in range(3):
            componentes[i].append(v_est[i])

    nombre = archivo.split("_")[1].capitalize()
    filename = f"{nombre}_Componentes_vector_estacionario.png"
    etiquetas = ["Frío", "Templado", "Cálido"]
    colores = ["blue", "orange", "green"]

    os.makedirs("Graficos", exist_ok=True)
    os.makedirs("Graficos/MonteCarlo Vector estacionario", exist_ok=True)

    # --------- GRÁFICO 1: COMPONENTES DEL VECTOR ESTACIONARIO ---------
    plt.figure(figsize=(9, 5))
    for i in range(3):
        plt.plot(e_values, componentes[i], label=etiquetas[i], color=colores[i], marker='o')

    plt.xscale("log")
    plt.xlabel("Valor de ε (Tolerancia)")
    plt.ylabel("Componente del vector estacionario")
    plt.title(f"Impacto de ε en el vector estacionario - {nombre}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"Graficos/MonteCarlo Vector estacionario/{nombre}_Componentes_vector_estacionario.png", dpi=300,
                bbox_inches='tight')
    plt.close()

    # --------- GRÁFICO 2: ITERACIONES NECESARIAS PARA CONVERGENCIA ---------
    plt.figure(figsize=(9, 5))
    plt.plot(e_values, iteraciones, marker='o', linestyle='-', color='purple', label="Iteraciones")
    plt.axhline(min_it, color='red', linestyle='--', label=f"min_it = {min_it}")

    plt.xscale("log")
    plt.xlabel("Valor de ε (Tolerancia)")
    plt.ylabel("Cantidad de iteraciones")
    plt.title(f"Convergencia según ε - {nombre}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"Graficos/MonteCarlo Vector estacionario/{nombre}_Iteraciones_vs_e.png", dpi=300, bbox_inches='tight')
    plt.close()

def pausar():
    input("\nPresioná Enter para finalizar...")


# Archivos
archivo1 = "data/temperature_Oslo_celsius.csv"
archivo2 = "data/temperature_Melbourne_celsius.csv"
archivo3 = "data/temperature_Quito_celsius.csv"

# Leer los datos
datos_oslo = leer_temperaturas(archivo1)
datos_melbourne = leer_temperaturas(archivo2)
datos_quito = leer_temperaturas(archivo3)

# Convertir temperaturas a estados
estados_oslo = [clasificar_estado(t) for t in datos_oslo]
estados_melbourne = [clasificar_estado(t) for t in datos_melbourne]
estados_quito = [clasificar_estado(t) for t in datos_quito]

# Inicializar matrices condicionales
M_oslo = np.zeros((3, 3))
M_melbourne = np.zeros((3, 3))
M_quito = np.zeros((3, 3))

# Calcular matrices
MatrizCondicional(estados_oslo, M_oslo)
MatrizCondicional(estados_melbourne, M_melbourne)
MatrizCondicional(estados_quito, M_quito)

imprimir_matriz(M_oslo,"Oslo")
imprimir_matriz(M_melbourne,"Melbourne")
imprimir_matriz(M_quito,"Quito")

min_it = 10000

grafico_vectorestacionario(M_oslo, archivo1, min_it)
grafico_vectorestacionario(M_melbourne, archivo2, min_it)
grafico_vectorestacionario(M_quito, archivo3, min_it)
print("Graficos de la simulacion montecarlo sobre el vector estacionario hechos")

grafico_mediaPrimeraRecurrencia(M_oslo,archivo1,min_it)
grafico_mediaPrimeraRecurrencia(M_melbourne,archivo2,min_it)
grafico_mediaPrimeraRecurrencia(M_quito,archivo3,min_it)
print("Graficos de la simulacion montecarlo sobre la media de la primera recurrencia por estado hechos")
pausar()