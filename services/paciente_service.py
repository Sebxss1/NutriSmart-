from fastapi import HTTPException, status

from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.auth_repository import AuthRepository
from repositories.paciente_repository import PacienteRepository
from schemas.paciente_schema import PacienteActualizar, PacienteCrear
from utils.seguridad import hash_password


class PacienteService:
    def __init__(self, db):
        self.paciente_repository = PacienteRepository(db)
        self.auth_repository = AuthRepository(db)

    def crear_paciente(
        self,
        datos: PacienteCrear,
        nutricionista: Usuario,
    ) -> Paciente:
        self._verificar_nutricionista(nutricionista)

        correo = datos.correo.strip().lower()

        if self.auth_repository.buscar_por_correo(correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario con ese correo.",
            )

        rol_paciente = self.paciente_repository.buscar_rol_por_nombre("paciente")

        if not rol_paciente:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No existe un rol activo llamado 'paciente'.",
            )

        usuario = Usuario(
            rol_id=rol_paciente.id,
            nombre=f"{datos.nombres.strip()} {datos.apellidos.strip()}",
            correo=correo,
            password_hash=hash_password(datos.password),
            estado=True,
        )

        paciente = Paciente(
            nutricionista_id=nutricionista.id,
            nombres=datos.nombres.strip(),
            apellidos=datos.apellidos.strip(),
            fecha_nacimiento=datos.fecha_nacimiento,
            sexo=datos.sexo,
            municipio_divipola=datos.municipio_divipola,
            zona=datos.zona,
            estrato=datos.estrato,
            presupuesto_semanal_cop=datos.presupuesto_semanal_cop,
            estado=True,
        )

        return self.paciente_repository.crear(usuario, paciente)

    def listar_pacientes(self, nutricionista: Usuario) -> list[Paciente]:
        self._verificar_nutricionista(nutricionista)
        return self.paciente_repository.listar_de_nutricionista(
            nutricionista.id
        )

    def obtener_paciente(
        self,
        paciente_id: int,
        nutricionista: Usuario,
    ) -> Paciente:
        self._verificar_nutricionista(nutricionista)

        paciente = self.paciente_repository.buscar_asignado(
            paciente_id,
            nutricionista.id,
        )

        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado.",
            )

        return paciente

    def actualizar_paciente(
        self,
        paciente_id: int,
        datos: PacienteActualizar,
        nutricionista: Usuario,
    ) -> Paciente:
        self._verificar_nutricionista(nutricionista)

        paciente = self.paciente_repository.buscar_asignado(
            paciente_id,
            nutricionista.id,
        )

        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado.",
            )

        cambios = datos.model_dump(exclude_unset=True)

        if not cambios:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Envía al menos un campo para actualizar.",
            )

        for campo in ("nombres", "apellidos", "fecha_nacimiento", "municipio_divipola"):
            if campo in cambios and cambios[campo] is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"El campo '{campo}' no puede quedar vacío.",
                )

        for campo in ("nombres", "apellidos"):
            if campo in cambios:
                cambios[campo] = cambios[campo].strip()

        for campo, valor in cambios.items():
            setattr(paciente, campo, valor)

        if paciente.usuario and (
            "nombres" in cambios or "apellidos" in cambios
        ):
            paciente.usuario.nombre = (
                f"{paciente.nombres} {paciente.apellidos}".strip()
            )

        return self.paciente_repository.guardar_cambios(paciente)

    def _verificar_nutricionista(self, usuario: Usuario) -> None:
        if not usuario.rol or usuario.rol.nombre.lower() != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede realizar esta acción.",
            )