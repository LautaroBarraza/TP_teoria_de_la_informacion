import random
import numpy as np
import math
import pandas as pd
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

def montecarlo_vectorEstacionario(M, e, min_it):
    N = 0  # Contador de iteraciones
    v_actual = np.zeros(3)  # Vector de visitas (F,T,C)
    v_ant = np.zeros(3)  # Vector anterior
    v_est = np.zeros(3)
    estado = 0

    while not converge(v_est, v_ant, e) or N < min_it:
        # definimos el siguiente estado
        estado = sig_estado(estado, M)

        N += 1
        v_actual[estado] += 1# Incrementamos el contador de visitas al estado actual
        v_ant = v_est.copy()
        v_est[estado] = v_actual[estado] / N
    # Retornamos el vector estacionario
    return v_est

def entropia_orden_0(estados):
    frecuencias = [0, 0, 0]
    total = len(estados)

    # Contar frecuencia de cada símbolo
    for estado in estados:
        frecuencias[estado] += 1

    # Calcular probabilidad y entropía
    entropia = 0
    for f in frecuencias:
        if f > 0:
            p = f / total
            entropia -= p * math.log2(p)
    return round(entropia, 3)

def entropia_condicional_orden_1(M, v_est):
    """
    Calcula la entropía condicional H_cond usando un vector estacionario dado (v_est)
    y la matriz condicional M (p(i|j)).
    """
    n=len(M)
    H_cond = 0
    for j in range(n):
        hj = 0
        for i in range(n):
            p_ij = M[i][j]
            if p_ij > 0:
                hj -= p_ij * np.log2(p_ij)
        H_cond += v_est[j] * hj
    return round(H_cond, 3)

def matriz_orden2(M, v_est):
    M2 = [[0 for _ in range(len(M))] for _ in range(len(M))]
    n=len(M2)
    for i in range(n):
        for j in range(n):
            M2[i][j]=v_est[i]*M[j][i]
    return M2

def huffman_orden_2(M2):
    # Lista de nodos: cada nodo es [probabilidad, lista_de_pares]
    # donde cada par es [[i, j], código_parcial]
    nodos = []
    n = len(M2)
    for i in range(n):
        for j in range(n):
            p = M2[i][j]
            if p > 0:
                # Usamos listas para representar los pares y poder modificarlos
                nodos.append([p, [[[i, j], ""]]])

    # Ordenamos los nodos según la probabilidad (de menor a mayor)
    nodos.sort(key=lambda x: x[0])

    # Construcción del árbol de Huffman
    while len(nodos) > 1:
        # Extraer los dos nodos con menor probabilidad
        nodo_izquierdo = nodos.pop(0)
        nodo_derecho = nodos.pop(0)

        # Anteponer "0" a los códigos del nodo izquierdo y "1" al derecho
        for par in nodo_izquierdo[1]:
            par[1] = "0" + par[1]
        for par in nodo_derecho[1]:
            par[1] = "1" + par[1]

        # Combinar nodos: suma de probabilidades y unión de los pares
        nuevo_nodo = [nodo_izquierdo[0] + nodo_derecho[0],
                      nodo_izquierdo[1] + nodo_derecho[1]]

        # Insertar el nuevo nodo en la lista manteniendo el orden (ascendente)
        insertado = False
        for idx, nodo in enumerate(nodos):
            if nuevo_nodo[0] < nodo[0]:
                nodos.insert(idx, nuevo_nodo)
                insertado = True
                break
        if not insertado:
            nodos.append(nuevo_nodo)

    # Extraer los códigos asignados (ya que solo queda un nodo)
    codigos = {}
    for simbolo, codigo in nodos[0][1]:
        codigos[tuple(simbolo)] = codigo  # Convertimos a tupla para tener clave inmutable
    return codigos

def huffman_orden_1(v_est):
    # Cada nodo es una lista [probabilidad, lista_de_pares]
    # donde cada par es [símbolo, código_parcial]. Inicialmente, cada nodo es una hoja.
    nodos = []
    for i, p in enumerate(v_est):
        if p > 0:  # se consideran solo estados con probabilidad positiva
            nodos.append([p, [[i, ""]]])  # Usamos listas en lugar de tuplas

    # Ordenamos los nodos por probabilidad
    nodos.sort(key=lambda x: x[0])

    # Construimos el árbol de Huffman
    while len(nodos) > 1:
        # Extraemos los dos nodos de menor probabilidad
        nodo_izquierdo = nodos.pop(0)
        nodo_derecho = nodos.pop(0)

        # A la rama izquierda le anteponemos "0" y a la derecha "1"
        for par in nodo_izquierdo[1]:
            par[1] = "0" + par[1]
        for par in nodo_derecho[1]:
            par[1] = "1" + par[1]

        # Combinamos los dos nodos en uno nuevo
        nuevo_nodo = [nodo_izquierdo[0] + nodo_derecho[0],
                      nodo_izquierdo[1] + nodo_derecho[1]]

        # Insertamos el nuevo nodo en la lista de nodos, manteniendo el orden creciente
        insertado = False
        for idx, nodo in enumerate(nodos):
            if nuevo_nodo[0] < nodo[0]:
                nodos.insert(idx, nuevo_nodo)
                insertado = True
                break
        if not insertado:
            nodos.append(nuevo_nodo)

    # Extraemos los códigos asignados a cada símbolo
    codigos = {}
    for simbolo, codigo in nodos[0][1]:
        codigos[simbolo] = codigo

    return codigos

def longitud_media_huffman_orden_1(codigos, v_est):
    l = 0
    for simbolo in codigos:
        l += v_est[simbolo] * len(codigos[simbolo])
    return round(l, 3)

def imprimir_huffman_orden_2(codigos):
    # Mapeo de índices a etiquetas
    estados = {0: "Frío", 1: "Templado", 2: "Cálido"}

    for par, codigo in sorted(codigos.items()):
        i, j = par  # Desempaquetamos el par
        # Usamos el mapeo para mostrar etiquetas legibles
        print(f"({estados.get(i, i)}, {estados.get(j, j)}) -> {codigo}")

def longitud_media_huffman_orden_2(codigos, M2):
    l = 0
    for (i, j) in codigos:
        l += M2[i][j] * len(codigos[(i, j)])
    return round(l, 3)

def longitud_total_codificada_orden_1(estados,codificacion):
    bits=0
    for e in estados:
        bits+=len(codificacion[e])
    return bits

def longitud_total_codificada_orden_2(estados,codificacion_orden2):
    bits = 0
    for i in range(len(estados) - 1):
        par = (estados[i], estados[i + 1])
        bits += len(codificacion_orden2[par])
    return bits

def tasa_compresion(tamano_original_bits, tamano_codificado_bits):
    return round(tamano_original_bits / tamano_codificado_bits, 3)

def imprimir_huffman_orden_1(codigos):
    # Mapeamos los números a sus correspondientes etiquetas de estado
    estados = {0: "Frío", 1: "Templado", 2: "Cálido"}
    for estado in sorted(codigos.keys()):
        etiqueta = estados.get(estado, f"Estado {estado}")
        print(f"{etiqueta}: {codigos[estado]}")

def imprimir_matriz(M, nombre):
    df = pd.DataFrame(M, columns=['Frío', 'Templado', 'Cálido'], index=['Frío', 'Templado', 'Cálido'])
    print(f"\nMatriz de orden 2 - {nombre}:\n")
    print(df.to_string(float_format="{:.3f}".format))

def pausar():
    input("\nPresioná Enter para finalizar...")

# Archivos
archivo1 = "temperature_Oslo_celsius.csv"
archivo2 = "temperature_Melbourne_celsius.csv"
archivo3 = "temperature_Quito_celsius.csv"

# Tamaños originales en bits (leer tamaño real del archivo)
tamano_oslo_bits = os.path.getsize(archivo1) * 8
tamano_melbourne_bits = os.path.getsize(archivo2) * 8
tamano_quito_bits = os.path.getsize(archivo3) * 8

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

e=0.001
min_it=5000
v1=montecarlo_vectorEstacionario(M_oslo,e,min_it)
v2=montecarlo_vectorEstacionario(M_melbourne,e,min_it)
v3=montecarlo_vectorEstacionario(M_quito,e,min_it)

M2_oslo=matriz_orden2(M_oslo, v1)
M2_melbourne=matriz_orden2(M_melbourne,v2)
M2_quito=matriz_orden2(M_quito, v3)

imprimir_matriz(M2_oslo, "Oslo")
imprimir_matriz(M2_melbourne , "Melbourne")
imprimir_matriz(M2_quito, "Quito")

print("Entropia sin memoria:")
print("Oslo:",entropia_orden_0(estados_oslo))
print("Melbourne:",entropia_orden_0(estados_melbourne))
print("Quito:",entropia_orden_0(estados_quito))

print("Entropia orden 1:")
print("Oslo", entropia_condicional_orden_1(M_oslo, v1))
print("Melbourne", entropia_condicional_orden_1(M_melbourne, v2))
print("Quito:", entropia_condicional_orden_1(M_quito, v3))

print("Codigo de huffman para cada fuente orden 1:")
print("Oslo:")
c1 = huffman_orden_1(v1)
imprimir_huffman_orden_1(c1)
L1 = longitud_media_huffman_orden_1(c1, v1)
bits_oslo_cod1 = longitud_total_codificada_orden_1(estados_oslo,c1)
print("Longitud media:", L1)
print("Tamaño original en bits:",tamano_oslo_bits)
print("Tamaño de la codificacion:",bits_oslo_cod1)
print("Tasa de compresión:", tasa_compresion(tamano_oslo_bits,bits_oslo_cod1))

print("Melbourne:")
c2 = huffman_orden_1(v2)
imprimir_huffman_orden_1(c2)
L2 = longitud_media_huffman_orden_1(c2, v2)
bits_melb_cod1 = longitud_total_codificada_orden_1(estados_melbourne,c2)
print("Longitud media:", L2)
print("Tamaño original en bits:",tamano_melbourne_bits)
print("Tamaño de la codificacion:",bits_melb_cod1)
print("Tasa de compresión:", tasa_compresion(tamano_melbourne_bits,bits_melb_cod1))

print("Quito:")
c3 = huffman_orden_1(v3)
imprimir_huffman_orden_1(c3)
L3 = longitud_media_huffman_orden_1(c3, v3)
bits_quito_cod1 = longitud_total_codificada_orden_1(estados_quito,c3)
print("Longitud media:", L3)
print("Tamaño original en bits:",tamano_quito_bits)
print("Tamaño de la codificacion:",bits_quito_cod1)
print("Tasa de compresión:", tasa_compresion(tamano_quito_bits,bits_quito_cod1))


print("Codigo de huffman para cada fuente extendida a orden 2:")
print("Oslo:")
c1_2 = huffman_orden_2(M2_oslo)
imprimir_huffman_orden_2(c1_2)
L1_2 = longitud_media_huffman_orden_2(c1_2, M2_oslo)
bits_oslo_cod2 = longitud_total_codificada_orden_2(estados_oslo,c1_2)
print("Longitud media:", L1_2)
print("Tamaño original en bits:",tamano_oslo_bits)
print("Tamaño de la codificacion:",bits_oslo_cod2)
print("Tasa de compresión:", tasa_compresion(tamano_oslo_bits,bits_oslo_cod2))

print("Melbourne:")
c2_2 = huffman_orden_2(M2_melbourne)
imprimir_huffman_orden_2(c2_2)
L2_2 = longitud_media_huffman_orden_2(c2_2, M2_melbourne)
bits_melb_cod2 = longitud_total_codificada_orden_2(estados_melbourne,c2_2)
print("Longitud media:", L2_2)
print("Tamaño original en bits:",tamano_melbourne_bits)
print("Tamaño de la codificacion:",bits_melb_cod1)
print("Tasa de compresión:", tasa_compresion(tamano_melbourne_bits,bits_melb_cod2))

print("Quito:")
c3_2 = huffman_orden_2(M2_quito)
imprimir_huffman_orden_2(c3_2)
L3_2 = longitud_media_huffman_orden_2(c3_2, M2_quito)
bits_quito_cod2 = longitud_total_codificada_orden_2(estados_quito,c3_2)
print("Longitud media:", L3_2)
print("Tamaño original en bits:",tamano_quito_bits)
print("Tamaño de la codificacion:",bits_quito_cod2)
print("Tasa de compresión:", tasa_compresion(tamano_quito_bits,bits_quito_cod2))

pausar()