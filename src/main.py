"""
def iniciar():
    Punto de entrada principal
                    # ABCD #
    estado_inicial = "1000000000"  #Fragemento a tomar 
    condiciones =    "1111111111" #subconjunto de nodos
    alcance =        "1111111111" # T1
    mecanismo =      "1111111111"# T0

    gestor_sistema = Manager(estado_inicial)

    ### Ejemplo de solución mediante módulo de fuerza bruta ###
    analizador_fb = QNodes(gestor_sistema)
    sia_uno = analizador_fb.aplicar_estrategia(
        condiciones,
        alcance,
        mecanismo,
    )
    print(sia_uno)"""


from src.controllers.manager import Manager

from src.controllers.strategies.q_nodes import QNodes
from src.middlewares.limpiezaDatos import ControladorSubsistema
import time
import threading

# Prueba de Exceso de Tiempo
def ejecutar_con_tiempo_limite(func, args=(), timeout=1800):
    resultado = []
    # 1800 segundos = 30 minutos
    def target():
        resultado.append(func(*args))

    hilo = threading.Thread(target=target)
    hilo.start()
    hilo.join(timeout)  # Esperar hasta el tiempo límite

    if hilo.is_alive():
        print("Tiempo límite alcanzado, pasando a la siguiente iteración.")
        return None  # Indicar que no se completó
    return resultado[0] if resultado else None



""""
Función para ejecutar el subsistema automatizado
"""
# prueba de Ejecucion automatica (prueba de integracion)
# Prueba de captura de errores
def exec_automatica(URL, sistema_candidato, estado_inicio):
    INICIO = 10    # <-- Cambiar el valor de inicio
    # Prueba de Entrada de Datos y Objetos
    entrada_datos = ControladorSubsistema(URL, sistema_candidato, estado_inicio)
    entrada_datos.listaObjetos = entrada_datos.listaObjetos[INICIO:]


    print('Ya tiene los datos', len(entrada_datos.listaObjetos))

    for i in entrada_datos.listaObjetos:
        print('Los está procesando ..:..:..')
        print(i.ESTADO_INICIO, i.CONDICIONES, i.mechanismo, i.alcance)
        
        # Llamar a la función con tiempo límite
        lista = ejecutar_con_tiempo_limite(
            start_up_QNodes, #Prueba de lista llena con tiempo de ejecucion
            args=(i.ESTADO_INICIO, i.CONDICIONES, i.mechanismo, i.alcance)
        )

        if lista is not None:
            print(f'Procesando {INICIO} de {len(entrada_datos.listaObjetos)}')
            # Prueba de carga de valores
            entrada_datos.formateo.CargarValores(lista, ((INICIO+1)*2+2))
            print('Cargando en el archivo')
        else:
            print(f'La iteración {INICIO} se saltó debido a tiempo excedido.')

        INICIO += 1
    
    print('Terminado!!!!')



#Prueba de valores de lista != None
def start_up_QNodes(estado_inicio, condiciones, mechanismo, alcance):
    """Punto de entrada principal"""
                   # ABCD #
    estado_inicio = estado_inicio
    condiciones =   condiciones
    mechanismo =    mechanismo
    alcance =       alcance

    config_sistema = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante Pyphi ###

    start_time = time.time()
    analizador_fi = QNodes(config_sistema)
    sia_dos = analizador_fi.aplicar_estrategia(condiciones, alcance, mechanismo)
    end_time = time.time()
    #mi_logger.debug(sia_dos.particion)
    #print([sia_dos.particion_2,sia_dos.perdida, f'{end_time - start_time:.6f}seg'])
    return [sia_dos.particion_2,sia_dos.perdida, round(end_time - start_time,6)]

