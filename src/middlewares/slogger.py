import sys
import logging
from pathlib import Path
from datetime import datetime
from functools import wraps
from typing import Any, Callable

from colorama import init

from src.constants.base import LOGS_PATH


class SafeLogger:
    """Logger seguro/robusto para manejar cualquier tipo de entrada y caracteres especiales."""

    def __init__(self, name: str):
        self._logger = self.__setup_logger(name)

    def _safe_str(self, obj: Any) -> str:
        """Convierte cualquier objeto a string de forma segura."""
        try:
            if isinstance(obj, (list, tuple, set, dict)):
                return str(obj)
            return str(obj).encode("utf-8", errors="replace").decode("utf-8")
        except Exception:
            return "[Objeto no representable]"

    def _safe_format(self, *args, **kwargs) -> str:
        """Formatea los argumentos de forma segura."""
        args_str = " ".join(self._safe_str(arg) for arg in args)
        if kwargs:
            kwargs_str = " ".join(f"{k}={self._safe_str(v)}" for k, v in kwargs.items())
            return f"{args_str} {kwargs_str}"
        return args_str

    def __setup_logger(self, name: str) -> logging.Logger:
        """Configura el logger con manejo de encodings y formateo personalizado."""
        # Crear estructura de directorios para logs detallados
        base_log_dir = Path(LOGS_PATH)
        base_log_dir.mkdir(exist_ok=True)

        current_time = datetime.now()
        date_dir = base_log_dir / current_time.strftime("%d_%m_%Y")
        date_dir.mkdir(exist_ok=True)

        hour_dir = date_dir / f"{current_time.strftime('%H')}hrs"
        hour_dir.mkdir(exist_ok=True)

        # Archivo para logs detallados (estructura anidada por fecha/hora)
        detailed_log_file = hour_dir / f"{name}.log"
        # Archivo para el último log (en la raíz, se sobrescribe en cada ejecución)
        last_log_file = base_log_dir / f"last_{name}.log"

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()

        # Formatter para archivos (sin colores)
        plain_formatter = logging.Formatter(
            "%(levelname)s (%(asctime)s):\n %(message)s", datefmt="time: %H:%M:%S"
        )
        # Formatter para consola (con colores)
        colored_formatter = ColorFormatter(datefmt="time: %H:%M:%S")

        # Handler para archivo detallado
        detailed_file_handler = logging.FileHandler(
            detailed_log_file, mode="w", encoding="utf-8"
        )
        detailed_file_handler.setLevel(logging.DEBUG)
        detailed_file_handler.setFormatter(plain_formatter)

        # Handler para el archivo "last" (última ejecución)
        last_file_handler = logging.FileHandler(
            last_log_file, mode="w", encoding="utf-8"
        )
        last_file_handler.setLevel(logging.DEBUG)
        last_file_handler.setFormatter(plain_formatter)

        # Handler para consola: se muestran solo mensajes ERROR o superiores
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(colored_formatter)

        logger.addHandler(detailed_file_handler)
        logger.addHandler(last_file_handler)
        logger.addHandler(console_handler)

        return logger

    def log(self, level: int, *args, **kwargs) -> None:
        """Método genérico de logging."""
        message = self._safe_format(*args, **kwargs)
        self._logger.log(level, message)

    def debug(self, *args, **kwargs) -> None:
        """Log a nivel DEBUG."""
        self.log(logging.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        """Log a nivel INFO."""
        self.log(logging.INFO, *args, **kwargs)

    def warn(self, *args, **kwargs) -> None:
        """Log a nivel WARNING."""
        self.log(logging.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        """Log a nivel ERROR."""
        self.log(logging.ERROR, *args, **kwargs)

    def critic(self, *args, **kwargs) -> None:
        """Log a nivel CRITICAL."""
        self.log(logging.CRITICAL, *args, **kwargs)


def get_logger(name: str) -> SafeLogger:
    """Función de conveniencia para obtener una instancia del logger."""
    return SafeLogger(name)


# Decorador opcional para logging automático
def log_execution(logger: SafeLogger):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(f"Iniciando {func.__name__}")
                result = func(*args, **kwargs)
                logger.debug(f"Completado {func.__name__}")
                return result
            except Exception as e:
                logger.error(f"Error en {func.__name__}: {e}")
                raise

        return wrapper

    return decorator


# Inicializa colorama para que se reinicien los colores automáticamente
init(autoreset=True)


# Formatter personalizado para consola con colores
class ColorFormatter(logging.Formatter):
    # Códigos ANSI para cada nivel:
    COLORS = {
        logging.DEBUG: "\033[90m",  # gris
        logging.INFO: "\033[34m",  # azul
        logging.WARNING: "\033[38;5;208m",  # naranja (si terminal soporta)
        logging.ERROR: "\033[31m",  # rojo
        logging.CRITICAL: "\033[31m",  # rojo
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        # Aplica color al nombre del nivel
        color = self.COLORS.get(record.levelno, "")
        timestamp = self.formatTime(record, self.datefmt)
        levelname = f"{color}{record.levelname}{self.RESET}"
        # Formato compacto: LEVEL (timestamp): mensaje
        formatted = f"{levelname} ({timestamp}): {record.getMessage()}"
        return formatted
