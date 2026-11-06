import re
import unicodedata


def normalizar_nombre_rol(nombre: str | None) -> str:
    if not nombre:
        return ""
    sin_tildes = "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", nombre.strip().lower())
        if unicodedata.category(caracter) != "Mn"
    )
    return re.sub(r"[\s_-]+", "", sin_tildes)


def es_rol_administrador(nombre: str | None) -> bool:
    return normalizar_nombre_rol(nombre) in {
        "admin", "administrador", "superadmin", "superadministrador"
    }
