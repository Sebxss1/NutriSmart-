from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.condicion_schema import (
    CondicionMedicaCrear,
    CondicionMedicaRespuesta,
    PacienteCondicionCrear,
    PacienteCondicionRespuesta,
)
from services.condicion_service import CondicionService
from utils.auth_dependencies import get_current_user

router = APIRouter(tags=["Condiciones médicas"])


@router.get(
    "/condiciones-medicas",
    response_model=list[CondicionMedicaRespuesta],
)
def listar_condiciones(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CondicionService(db).listar_condiciones()


@router.post(
    "/condiciones-medicas",
    response_model=CondicionMedicaRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_condicion(
    datos: CondicionMedicaCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CondicionService(db).crear_condicion(datos, usuario_actual)


@router.get(
    "/pacientes/{paciente_id}/condiciones-medicas",
    response_model=list[PacienteCondicionRespuesta],
)
def listar_condiciones_de_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CondicionService(db).listar_condiciones_paciente(
        paciente_id,
        usuario_actual,
    )


@router.post(
    "/pacientes/{paciente_id}/condiciones-medicas",
    response_model=PacienteCondicionRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def asignar_condicion_a_paciente(
    paciente_id: int,
    datos: PacienteCondicionCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return CondicionService(db).agregar_condicion_a_paciente(
        paciente_id,
        datos,
        usuario_actual,
    )