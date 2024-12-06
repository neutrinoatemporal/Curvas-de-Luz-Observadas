import numpy as np
import os
import matplotlib.pyplot as plt
import sympy as sp
import pandas as pd
from scipy.optimize import fsolve
from sympy import *
from sympy.plotting import plot
from sympy.abc import x

def asas(nombre_archivo, periodo):  #Función para generar las curvas Magnitud vs Fase

    ruta_base = os.path.dirname(__file__)  # Carpeta donde está la data
    archivo_txt = os.path.join(ruta_base, '..', 'data', f'{nombre_archivo}.txt')

    if not os.path.exists(archivo_txt):   # Verificar si el archivo existe
        print(f"El archivo {archivo_txt} no existe.")
        return

    datos = pd.read_csv(archivo_txt, delimiter='\t', header=0) # Leer los datos desde el archivo de texto

    magnitud = datos['MAG']
    tiempos = datos['HJD']

    top_10_indices = magnitud.nlargest(10).index  # Encontrar los índices de las diez magnitudes más grandes
    top_10_tiempos = tiempos.loc[top_10_indices]  # Obtener los tiempos correspondientes a esas magnitudes

    for i, t0 in enumerate(top_10_tiempos): 
        nuevos_tiempos = (tiempos - t0) / periodo - np.floor((tiempos - t0) / periodo) #Pasar de tiempos a fase
        datos_fase = pd.DataFrame({  # Crear un nuevo DataFrame con los tiempos en fase y las magnitudes
            'Tiempo en fase': nuevos_tiempos,
            'Magnitud': magnitud
        })

        datos_fase_ordenados = datos_fase.sort_values(by='Tiempo en fase')

        print(f'Opción {i+1}')
        print(f"t0 = {t0}")

        plt.figure(i) # Graficar
        plt.plot(datos_fase_ordenados['Tiempo en fase'], datos_fase_ordenados['Magnitud'],
                 'x', markersize=5, markeredgewidth=1)
        plt.gca().invert_yaxis()
        plt.xlim(0, 1)
        plt.title(f'ASAS {nombre_archivo} , t0 = {t0} , Periodo={periodo} d')
        plt.xlabel('Fase')
        plt.ylabel('Magnitud')
        plt.grid(True)
        plt.show()


def flujo(nombre_archivo, periodo, opcion): #Función para generar las curvas Flujo relativo vs Fase

    ruta_base = os.path.dirname(__file__)  
    archivo_txt = os.path.join(ruta_base, '..', 'data', f'{nombre_archivo}.txt')

    if not os.path.exists(archivo_txt):
        print(f"El archivo {archivo_txt} no existe.")
        return

    datos = pd.read_csv(archivo_txt, delimiter='\t', header=0)
    magnitud = datos['MAG']
    tiempos = datos['HJD']

    top_10_indices = magnitud.nlargest(10).index
    top_10_tiempos = tiempos.loc[top_10_indices]

    for i, t0 in enumerate(top_10_tiempos):
      if (i+1==opcion):
        nuevos_tiempos = (tiempos - t0) / periodo - np.floor((tiempos - t0) / periodo)
        flujo = 10**(-magnitud / 2.5) * 10**4 # Pasar de magnitud a flujo
        datos_fase = pd.DataFrame({  
            'Tiempo en fase': nuevos_tiempos,
            'Magnitud': flujo
        })

        datos_fase_ordenados = datos_fase.sort_values(by='Tiempo en fase')

        # Filtrar las magnitudes para tiempos de fase cercanos a 0.25 y 0.75
        magnitudes_fase_025 = datos_fase_ordenados[
            (datos_fase_ordenados['Tiempo en fase'] >= 0.24) &
            (datos_fase_ordenados['Tiempo en fase'] <= 0.26)
        ]
        magnitudes_fase_075 = datos_fase_ordenados[
            (datos_fase_ordenados['Tiempo en fase'] >= 0.74) &
            (datos_fase_ordenados['Tiempo en fase'] <= 0.76)
        ]

        # Calcular el promedio de los flujos
        promedio_025 = magnitudes_fase_025['Magnitud'].mean()
        promedio_075 = magnitudes_fase_075['Magnitud'].mean()
        factor_escalar = (promedio_025 + promedio_075) / 2

        print(f"t0 = {t0}")
        print(f"Promedio de magnitudes en fase 0.25 para t0={t0}: {promedio_025}")
        print(f"Promedio de magnitudes en fase 0.75 para t0={t0}: {promedio_075}")
        print(f"Factor de escala (K) = {factor_escalar}")

        plt.figure()
        plt.plot(datos_fase_ordenados['Tiempo en fase'], datos_fase_ordenados['Magnitud'],
              'x', markersize=5, markeredgewidth=1, label= 'Experimental')
        plt.xlim(0, 1)
        plt.xlabel('Fase')
        plt.ylabel('Flujo Relativo (x10^-4)')
        plt.show()