import json
import os
from datetime import datetime
from typing import Any, Dict


class LoggerService:
    def __init__(self, base_dir: str = "logs"):
        """
        Inicializa el servicio de logs.

        Args:
            base_dir (str): Directorio base donde se guardarán los logs
        """
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def log(self, entry: Dict[str, Any], filename: str) -> None:
        """
        Registra una entrada en el archivo de log especificado.

        Args:
            entry (Dict[str, Any]): Diccionario con la información a registrar
            filename (str): Nombre del archivo de log (sin extensión)
        """
        # Asegurar que la entrada tenga timestamp
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().isoformat()

        # Construir la ruta completa del archivo
        filepath = os.path.join(self.base_dir, f"{filename}.txt")

        # Escribir en el archivo
        with open(filepath, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_access(
        self, path: str, method: str, device_type: str, user_agent: str
    ) -> None:
        """
        Método específico para registrar accesos a la API.

        Args:
            path (str): Ruta accedida
            method (str): Método HTTP
            device_type (str): Tipo de dispositivo
            user_agent (str): User-Agent del cliente
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "path": path,
            "method": method,
            "device_type": device_type,
            "user_agent": user_agent,
        }
        self.log(entry, "access")
