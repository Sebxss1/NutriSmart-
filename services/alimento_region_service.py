from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.alimento_region_model import AlimentoRegion
from models.usuario_model import Usuario
from repositories.alimento_region_repository import AlimentoRegionRepository
from schemas.alimento_region_schema import AlimentoRegionCrear


class AlimentoRegionService:
    def __init__(self, db: Session):
        self.repository = AlimentoRegionRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def listar_disponibles(self, municipio_divipola: str):
        return self.repository.listar_disponibles_por_municipio(
            municipio_divipola
        )

    def registrar_disponibilidad(
        self,
        alimento_id: int,
        datos: AlimentoRegionCrear,
        usuario_actual: Usuario,
    ) -> AlimentoRegion:
        rol = self._obtener_rol(usuario_actual)

        if rol not in {"administrador", "nutricionista"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un administrador o nutricionista puede registrar precios y disponibilidad.",
            )

        alimento = self.repository.obtener_alimento(alimento_id)
        if not alimento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado o inactivo.",
            )

        registro_existente = self.repository.obtener_registro(
            alimento_id=alimento_id,
            municipio_divipola=datos.municipio_divipola,
            fecha_referencia=datos.fecha_referencia,
        )

        if registro_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un registro de ese alimento para ese municipio y fecha.",
            )

        registro = AlimentoRegion(
            alimento_id=alimento_id,
            municipio_divipola=datos.municipio_divipola,
            precio_cop=datos.precio_cop,
            disponible=datos.disponible,
            fecha_referencia=datos.fecha_referencia,
            fuente=datos.fuente,
        )

        return self.repository.crear(registro)