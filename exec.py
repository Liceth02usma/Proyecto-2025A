from src.models.base.application import aplicacion
from src.main import exec_automatica


def main():
    """Inicializar el aplicativo."""

    aplicacion.profiler_habilitado = True
    # aplicacion.pagina_sample_network = "B"
    URL = "/home/liceth/Descargas/PruebasIniciales20 (1).xlsx" 
    exec_automatica(URL, 'ABCDEFGHIJ','1000000000')

    #iniciar()


if __name__ == "__main__":
    main()
