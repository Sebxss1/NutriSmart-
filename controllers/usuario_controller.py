from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.paciente_schema import PacienteCrear, PacienteRespuesta
from services.paciente_service import PacienteService
from utils.auth_dependencies import get_current_user

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"],
)


@router.post(
    "/",
    response_model=PacienteRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_paciente(
    datos: PacienteCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    servicio = PacienteService(db)
    return servicio.crear_paciente(datos, usuario_actual)


@router.get(
    "/",
    response_model=list[PacienteRespuesta],
)
def listar_pacientes(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    servicio = PacienteService(db)
    return servicio.listar_pacientes(usuario_actual)


@router.get(
    "/{paciente_id}",
    response_model=PacienteRespuesta,
)
def obtener_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    servicio = PacienteService(db)
    return servicio.obtener_paciente(paciente_id, usuario_actual)