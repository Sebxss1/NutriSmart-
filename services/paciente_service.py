from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.auth_repository import AuthRepository
from repositories.paciente_repository import PacienteRepository
from schemas.paciente_schema import PacienteActualizar, PacienteCrear
from utils.seguridad import hash_password


MUNICIPIOS_ATLANTICO = {
    "08001": "Barranquilla",
    "08078": "Baranoa",
    "08137": "Campo de la Cruz",
    "08141": "Candelaria",
    "08296": "Galapa",
    "08372": "Juan de Acosta",
    "08421": "Luruaco",
    "08433": "Malambo",
    "08436": "Manatí",
    "08520": "Palmar de Varela",
    "08549": "Piojó",
    "08558": "Polonuevo",
    "08560": "Ponedera",
    "08573": "Puerto Colombia",
    "08606": "Repelón",
    "08634": "Sabanagrande",
    "08638": "Sabanalarga",
    "08675": "Santa Lucía",
    "08685": "Santo Tomás",
    "08758": "Soledad",
    "08770": "Suan",
    "08832": "Tubará",
    "08849": "Usiacurí",
}


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
        documento = datos.documento.strip()
        ciudad_esperada = MUNICIPIOS_ATLANTICO.get(datos.municipio_divipola)

        if not ciudad_esperada or ciudad_esperada != datos.ciudad.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "La ciudad debe ser un municipio del Atlántico "
                    "y coincidir con su código DIVIPOLA."
                ),
            )

        if not documento:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El documento no puede estar vacío.",
            )

        if self.auth_repository.buscar_por_correo(correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario con ese correo.",
            )

        if self.paciente_repository.buscar_por_documento(documento):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un paciente con ese documento.",
            )

        rol_paciente = self.paciente_repository.buscar_rol_por_nombre(
            "paciente"
        )

        if not rol_paciente:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No existe un rol activo llamado 'paciente'.",
            )

        nombre_completo = (
            f"{datos.nombres.strip()} {datos.apellidos.strip()}"
        )

        usuario = Usuario(
            rol_id=rol_paciente.id,
            nombre=nombre_completo,
            correo=correo,
            password_hash=hash_password(datos.password),
            estado=True,
        )

        tipo_documento = (
            datos.tipo_documento.strip()
            if datos.tipo_documento and datos.tipo_documento.strip()
            else None
        )

        paciente = Paciente(
            nutricionista_id=nutricionista.id,
            nombres=datos.nombres.strip(),
            apellidos=datos.apellidos.strip(),
            tipo_documento=tipo_documento,
            documento=documento,
            telefono=(datos.telefono.strip() if datos.telefono else None),
            departamento="Atlántico",
            ciudad=datos.ciudad.strip(),
            fecha_nacimiento=datos.fecha_nacimiento,
            sexo=datos.sexo,
            municipio_divipola=datos.municipio_divipola,
            zona=datos.zona,
            estrato=datos.estrato,
            presupuesto_semanal_cop=datos.presupuesto_semanal_cop,
            estado=True,
        )

        try:
            return self.paciente_repository.crear(usuario, paciente)
        except IntegrityError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo o el documento ya están registrados.",
            ) from error

    def listar_pacientes(
        self,
        nutricionista: Usuario,
    ) -> list[Paciente]:
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

    def obtener_perfil_propio(self, usuario_actual: Usuario) -> Paciente:
        rol = usuario_actual.rol.nombre.strip().lower() if usuario_actual.rol else ""

        if rol != "paciente":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esta ruta está disponible únicamente para pacientes.",
            )

        paciente = self.paciente_repository.buscar_por_usuario(usuario_actual.id)

        if not paciente or not paciente.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró un perfil de paciente activo para este usuario.",
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

        campos_obligatorios = (
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "municipio_divipola",
            "documento",
        )

        for campo in campos_obligatorios:
            if campo in cambios and cambios[campo] is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"El campo '{campo}' no puede quedar vacío.",
                )

        for campo in ("nombres", "apellidos"):
            if campo in cambios:
                cambios[campo] = cambios[campo].strip()

        if "documento" in cambios:
            documento = cambios["documento"].strip()

            if not documento:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="El documento no puede estar vacío.",
                )

            paciente_con_documento = (
                self.paciente_repository.buscar_por_documento(documento)
            )

            if (
                paciente_con_documento
                and paciente_con_documento.id != paciente.id
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe otro paciente con ese documento.",
                )

            cambios["documento"] = documento

        if "ciudad" in cambios or "municipio_divipola" in cambios:
            codigo = cambios.get(
                "municipio_divipola",
                paciente.municipio_divipola,
            )
            ciudad = cambios.get("ciudad", paciente.ciudad)
            ciudad_esperada = MUNICIPIOS_ATLANTICO.get(codigo)

            if not ciudad_esperada or ciudad_esperada != ciudad:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=(
                        "La ciudad debe ser un municipio del Atlántico "
                        "y coincidir con su código DIVIPOLA."
                    ),
                )

        if "telefono" in cambios and cambios["telefono"] is not None:
            cambios["telefono"] = cambios["telefono"].strip() or None

        if "departamento" in cambios:
            cambios["departamento"] = "Atlántico"

        if "ciudad" in cambios and cambios["ciudad"] is not None:
            cambios["ciudad"] = cambios["ciudad"].strip()

        if "tipo_documento" in cambios and cambios["tipo_documento"]:
            cambios["tipo_documento"] = cambios["tipo_documento"].strip() or None

        for campo, valor in cambios.items():
            setattr(paciente, campo, valor)

        if paciente.usuario and (
            "nombres" in cambios or "apellidos" in cambios
        ):
            paciente.usuario.nombre = (
                f"{paciente.nombres} {paciente.apellidos}".strip()
            )

        try:
            return self.paciente_repository.guardar_cambios(paciente)
        except IntegrityError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El documento ya está registrado para otro paciente.",
            ) from error

    def _verificar_nutricionista(self, usuario: Usuario) -> None:
        rol = usuario.rol.nombre.strip().lower() if usuario.rol else ""

        if rol != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede realizar esta acción.",
            )
