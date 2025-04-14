from src.middlewares.profile import profiler_manager
from src.main import exec_automatica,start_up

def main():
    """Inicializar el aplicativo."""
    profiler_manager.enabled = True
    #URL = "/home/liceth/Documentos/Analisis y Diseno de Algoritmos/Pruebas de campo/pruebas25.xlsx" 
    #exec_automatica(URL, 'ABCDEFGHIJKLMNOPQRSTUVWXY','1000000000000000000000000')
    start_up()


if __name__ == "__main__":
    main()
