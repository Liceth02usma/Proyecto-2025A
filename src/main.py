"""from controllers.manager import Manager

from src.models.logic.q_nodes import QNodes


def start_up():
    Punto de entrada principal
    # ABCD #
    estado_inicio = "1000"
    condiciones = "1110"
    alcance = "1110"
    mechanismo = "1110"

    sys_config = Manager(estado_inicial=estado_inicio)

    ### Ejemplo de solución mediante módulo de pyphi ###

    analizador_q = QNodes(sys_config)
    sia_uno = analizador_q.aplicar_estrategia(condiciones, alcance, mechanismo)
    # sia_uno = analizador_q.prueba_marginal(condiciones, alcance, mechanismo)
    print(sia_uno)



    def start_up_automatico(estado_inicio, condiciones, mechanismo, alcance):
    Punto de entrada principal
                   # ABCD #
    estado_inicio = estado_inicio
    condiciones =   condiciones
    mechanismo =    mechanismo
    alcance =       alcance

    config_sistema = Manager(estado_inicial=estado_inicio)
    ### Ejemplo de solución mediante Pyphi ###
    start_time = time.time()
    analizador_fi = Phi(config_sistema)
    sia_dos = analizador_fi.aplicar_estrategia(condiciones, alcance, mechanismo)
    end_time = time.time()
    return [sia_dos.particion_2,sia_dos.perdida, f'{end_time - start_time:.6f}seg']

"""

from controllers.manager import Manager

from src.subsistema.limpiezaDatos import ControladorSubsistema
import time
from src.models.logic.q_nodes import QNodes
from src.models.logic.phi import Phi
import threading


#from src.funcs.base import setup_logger


def start_up():
    """Punto de entrada principal"""
                   # ABCDEFGHIJ#
    estado_inicial = "1000"  #Fragemento a tomar 
    condiciones =    "1111" #subconjunto de nodos
    alcance =        "1111" # T1
    mecanismo =      "1111"# T0
    

    config_sistema = Manager(estado_inicial=estado_inicial)

    analizador_fi = Phi(config_sistema)
    start_time = time.time()
    sia_dos = analizador_fi.aplicar_estrategia(condiciones, alcance, mecanismo)
    end_time = time.time()
    print([sia_dos.particion_2,sia_dos.perdida, f'{end_time - start_time:.6f}seg'])
    #mi_logger.debug(sia_dos.particion)
    print(sia_dos)




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
        return None # Indicar que no se completó
    return resultado[0] if resultado else None



""""
Función para ejecutar el subsistema automatizado
"""
def exec_automatica(URL, sistema_candidato, estado_inicio):
    INICIO = 4

    entrada_datos = ControladorSubsistema(URL, sistema_candidato, estado_inicio)
    entrada_datos.listaObjetos = entrada_datos.listaObjetos[INICIO:]
    lista =[]

    print('Ya tiene los datos', len(entrada_datos.listaObjetos))
    for i in entrada_datos.listaObjetos:
        print('Los está procesando ..:..:..')
        print('estado de inicio',i.ESTADO_INICIO, i.CONDICIONES, i.mechanismo, i.alcance)
        print(len(i.ESTADO_INICIO) + len(i.CONDICIONES) +len(i.mechanismo) +len(i.alcance))
        lista = ejecutar_con_tiempo_limite(
            start_up_QNodes_automatizado, args=(i.ESTADO_INICIO, i.CONDICIONES, i.mechanismo, i.alcance)
        )
         
        if lista is not None:
            print(f'Procesando {INICIO} de {len(entrada_datos.listaObjetos)}')
            entrada_datos.formateo.CargarValores(lista, ((INICIO+1)*2+2))
            print('Cargando en el archivo')
        else:
            print(f'La iteración {INICIO} se saltó debido a tiempo excedido.')

        INICIO += 1
    
    print('Terminado!!!!')







def start_up_QNodes_automatizado(estado_inicio, condiciones, mechanismo, alcance):
    """Punto de entrada principal"""
                   # ABCD #
    estado_inicio = estado_inicio
    condiciones =   condiciones
    mechanismo =    mechanismo
    alcance =       alcance


    ### Ejemplo de solución mediante Pyphi ###
    config_sistema = Manager(estado_inicial=estado_inicio)
    analizador_fi = QNodes(config_sistema)
    start_time = time.time()
    sia_dos = analizador_fi.aplicar_estrategia(condiciones, alcance, mechanismo)
    end_time = time.time()
    #mi_logger.debug(sia_dos.particion)
    print([sia_dos.particion_2,sia_dos.perdida, f'{end_time - start_time:.6f}seg'])
    return [sia_dos.particion_2,sia_dos.perdida,round(end_time - start_time,6)]
    