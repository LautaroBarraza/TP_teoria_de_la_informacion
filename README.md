# TP Teoría de la Información

**¡Bienvenidos!**

Este repositorio contiene la resolución del Trabajo Práctico de *Teoría de la Información*. Cada sección del TP está separada en archivos independientes (.py o .ipynb) para facilitar su ejecución y revisión de manera modular.
Tambien disponen del codigo en google colab para una ejecucion mas simple, el cual es https://colab.research.google.com/drive/1ZqonCr_oRBpJkRv35wvjl8pOKCqcc--p?usp=sharing.

---

## 📂 Estructura del Repositorio

```
TP_teoria_de_la_informacion/
│
├── README.md                # Documento de presentación y guía de uso
├── requirements.txt         # Lista de dependencias necesarias
├── src/                     # Directorio principal de código y notebooks
│   ├── notebooks
│   ├── parte1.py
│   ├── parte2.py
│   └── ...                  # Cada archivo corresponde a un enunciado o sección
└── data/                    # Datos de prueba
```

Cada archivo en `src/` está diseñado para funcionar de manera independiente

## 🛠️ Requisitos y Configuración

Para garantizar replicabilidad y aislar dependencias (evitando conflictos como en un sistema embebido), siga estos pasos:

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/LautaroBarraza/TP_teoria_de_la_informacion.git
   cd TP_teoria_de_la_informacion
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python3 -m venv venv   # Crear entorno virtual
   ```

   * **Linux/macOS**:

     ```bash
     source venv/bin/activate
     ```

   * **Windows (CMD)**:

     ```cmd
     venv\Scripts\activate.bat
     ```

   * **Windows (PowerShell)**:

     ```powershell
     .\venv\Scripts\Activate.ps1
     ```

   > Verá el prefijo `(venv)` en su prompt, indicando que está usando el entorno aislado.

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

   Esto garantiza que se instalen exactamente las versiones utilizadas en el desarrollo, evitando incompatibilidades.

---

## ▶️ Ejecución de las Secciones

### A) Jupyter Notebooks (.ipynb)

Cada notbook representa un enunciado diferente:

```bash
jupyter notebook
```

* Navegue a `src/` en la interfaz web.
* Abra el archivo deseado (por ejemplo, `parte1.ipynb`).
* En el menú **Cell**, seleccione **Run All** para ejecutar todo el análisis.

### B) Scripts Python (.py)

Los scripts se ejecutan de forma secuencial con el intérprete:

```bash
# Asegúrese de estar en el directorio raíz del proyecto y con el entorno activo:
python src/parte2.py
```

Repita este comando con cada archivo `.py` que corresponda a los enunciados deseados.

---

## 📋 Descripción de Archivos

| Archivo                             | Descripción                                                          |
| ----------------------------------- | -------------------------------------------------------------------- |
| `parte1.py`                         | Estadísticas para ingenieros que miran el cielo                      |
| `parte2.py`                         | Una fuente de calor… markoviana                                      |
| `parte3.py`                         | Entropía, Huffman y la batalla por los bits                          |
| `parte4.py`                         | El canal climático de Musk                                           |

---

## 🧪 Validación de Resultados

Para verificar el correcto funcionamiento, puede comparar las salidas impresas con los valores analisados en el informe.

---

## 🤝 Equipo de desarrollo
Santiago Orona:
Juan Manuel Vila:
Lautaro Barraza:

