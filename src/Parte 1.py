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

def promedio(datos):
    suma = 0
    for x in datos:
        suma += x
    return suma / len(datos)

def varianza(datos):
    media = promedio(datos)
    suma = 0
    for x in datos:
        suma += (x - media) ** 2
    return suma / len(datos)

def desviacion_estandar(datos):
    return (varianza(datos)) ** 0.5

def correlacion_cruzada(X, Y, t1, t2):
    return X[t1] * Y[t2]

def covarianza_cruzada(X, Y, t1, t2):
    return (X[t1] * Y[t2]) - (promedio(X) * promedio(Y))

def coeficiente_correlacion_cruzada(X, Y, t1, t2):
    cov = covarianza_cruzada(X, Y, t1, t2)
    desv_X = desviacion_estandar(X)
    desv_Y = desviacion_estandar(Y)
    if desv_X == 0 or desv_Y == 0:
        return 0  # evitar división por cero
    return cov / (desv_X * desv_Y)

# mostrar estadísticas
def imprimir_estadisticas(nombre, datos):
    media = promedio(datos)
    desv = desviacion_estandar(datos)
    print(f"{nombre}:")
    print(f"  Promedio: {round(media, 3)}°C")
    print(f"  Desvío estándar: {round(desv, 3)}°C\n")

def generar_graficos(nombre_ciudad, datos):
    medias = []
    desvios = []
    dias = list(range(1, len(datos) + 1))

    for i in dias:
        subset = datos[:i]
        medias.append(promedio(subset))
        desvios.append(desviacion_estandar(subset))
    os.makedirs("Graficos", exist_ok=True)
    os.makedirs("Graficos/Medias", exist_ok=True)
    os.makedirs("Graficos/Desvios", exist_ok=True)

    # Gráfico de la media
    plt.figure()
    plt.plot(dias, medias, label="Media", color='blue')
    plt.xlabel("Cantidad de días")
    plt.ylabel("Temperatura promedio (°C)")
    plt.title(f"Media de temperatura acumulada - {nombre_ciudad}")
    plt.grid(True)
    plt.savefig(f"Graficos/Medias/media_{nombre_ciudad}.png")
    plt.close()

    # Gráfico del desvío
    plt.figure()
    plt.plot(dias, desvios, label="Desvío estándar", color='red')
    plt.xlabel("Cantidad de días")
    plt.ylabel("Desvío estándar (°C)")
    plt.title(f"Desvío estándar de temperatura acumulado - {nombre_ciudad}")
    plt.grid(True)
    plt.savefig(f"Graficos/Desvios/desvio_{nombre_ciudad}.png")
    plt.close()

def graficar_correlacion_cruzada_entre_pares(X, Y):
    N = len(X)
    matriz = []
    for t1 in range(N):
        fila = []
        for t2 in range(N):
            r = coeficiente_correlacion_cruzada(X, Y, t1, t2)
            fila.append(r)
        matriz.append(fila)
    return matriz

def generar_matriz_correlacion_cruzada(max_t):
    os.makedirs("Graficos", exist_ok=True)
    os.makedirs("Graficos/CorrelacionCruzada", exist_ok=True)

    # Limitar datos a max_t
    X1 = datos_oslo[:max_t]
    Y1 = datos_melbourne[:max_t]
    Y2 = datos_quito[:max_t]
    X3 = datos_melbourne[:max_t]

    # Calcular matrices
    matriz_OM = graficar_correlacion_cruzada_entre_pares(X1, Y1)
    matriz_OQ = graficar_correlacion_cruzada_entre_pares(X1, Y2)
    matriz_MQ = graficar_correlacion_cruzada_entre_pares(X3, Y2)

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # Oslo vs Melbourne
    im1 = axs[0].imshow(matriz_OM, cmap='coolwarm', aspect='auto', origin='lower')
    axs[0].set_title("Oslo vs Melbourne")
    axs[0].set_xlabel("t1 (Oslo)")
    axs[0].set_ylabel("t2 (Melbourne)")
    plt.colorbar(im1, ax=axs[0])

    # Oslo vs Quito
    im2 = axs[1].imshow(matriz_OQ, cmap='coolwarm', aspect='auto', origin='lower')
    axs[1].set_title("Oslo vs Quito")
    axs[1].set_xlabel("t1 (Oslo)")
    axs[1].set_ylabel("t2 (Quito)")
    plt.colorbar(im2, ax=axs[1])

    # Melbourne vs Quito
    im3 = axs[2].imshow(matriz_MQ, cmap='coolwarm', aspect='auto', origin='lower')
    axs[2].set_title("Melbourne vs Quito")
    axs[2].set_xlabel("t1 (Melbourne)")
    axs[2].set_ylabel("t2 (Quito)")
    plt.colorbar(im3, ax=axs[2])

    plt.suptitle("Coeficiente de correlación cruzada rₓᵧ(t₁, t₂)", fontsize=14)
    plt.tight_layout()
    plt.savefig("Graficos/CorrelacionCruzada/matriz_correlacion_cruzada.png")
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

# Mostrar estadísticas individuales
imprimir_estadisticas("Oslo", datos_oslo)
imprimir_estadisticas("Melbourne", datos_melbourne)
imprimir_estadisticas("Quito", datos_quito)

# Generar gráficos
generar_graficos("Oslo", datos_oslo)
generar_graficos("Melbourne", datos_melbourne)
generar_graficos("Quito", datos_quito)
print("Graficos de la media y desvio hechos")
max_t=300
generar_matriz_correlacion_cruzada(max_t)
print("Grafico de correlacion hecho")
pausar()