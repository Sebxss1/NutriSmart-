from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.consentimiento_model import Consentimiento
from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.consentimiento_repository import ConsentimientoRepository
from schemas.consentimiento_schema import ConsentimientoCrear


class ConsentimientoService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = ConsentimientoRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.strip().lower()

    def _obtener_paciente(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ) -> Paciente:
        paciente = (
            self.db.query(Paciente)
            .filter(
                Paciente.id == paciente_id,
                Paciente.estado.is_(True),
            )
            .first()
        )

        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado.",
            )

        rol = self._obtener_rol(usuario_actual)

        if rol == "nutricionista":
            if paciente.nutricionista_id != usuario_actual.id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Paciente no encontrado o no está asignado a este nutricionista.",
                )
            return paciente

        if rol == "paciente" and paciente.usuario_id == usuario_actual.id:
            return paciente

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para consultar este consentimiento.",
        )

    def listar(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ):
        paciente = self._obtener_paciente(paciente_id, usuario_actual)
        return self.repository.listar_por_paciente(paciente.id)

    def crear(
        self,
        paciente_id: int,
        datos: ConsentimientoCrear,
        usuario_actual: Usuario,
    ) -> Consentimiento:
        if self._obtener_rol(usuario_actual) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede registrar consentimientos.",
            )

        paciente = self._obtener_paciente(paciente_id, usuario_actual)

        if not datos.version_texto.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="version_texto no puede estar vacío.",
            )

        if not datos.otorgado_por.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="otorgado_por no puede estar vacío.",
            )

        consentimiento = Consentimiento(
            paciente_id=paciente.id,
            version_texto=datos.version_texto.strip(),
            fecha_aceptacion=datos.fecha_aceptacion,
            otorgado_por=datos.otorgado_por.strip(),
            tipo_otorgante=datos.tipo_otorgante,
            registrado_por_id=usuario_actual.id,
            estado=True,
        )

        return self.repository.crear(consentimiento)

    def desactivar(
        self,
        paciente_id: int,
        consentimiento_id: int,
        usuario_actual: Usuario,
    ) -> Consentimiento:
        if self._obtener_rol(usuario_actual) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede desactivar consentimientos.",
            )

        paciente = self._obtener_paciente(paciente_id, usuario_actual)

        consentimiento = self.repository.buscar_activo(
            paciente.id,
            consentimiento_id,
        )

        if not consentimiento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Consentimiento no encontrado.",
            )

        return self.repository.desactivar(consentimiento)