"""Configuración centralizada del registro de eventos y errores."""
import logging
from pathlib import Path

def configurar_logger():
    """Crea un logger que escribe eventos y errores en logs/software_fj.log."""
    carpeta = Path("logs")
    carpeta.mkdir(exist_ok=True)
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    archivo = logging.FileHandler(carpeta / "software_fj.log", encoding="utf-8")
    archivo.setFormatter(formato)
    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    logger.addHandler(archivo)
    logger.addHandler(consola)
    return logger
