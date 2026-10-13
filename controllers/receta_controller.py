from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from config.database import get_db
from models.usuario_model import Usuario
from schemas.receta_schema import (
    IngredienteRecetaActualizar,
    IngredienteRecetaCrear,
    IngredienteRecetaRespuesta,
    RecetaActualizar,
    RecetaCrear,
    RecetaRespuesta,
)
from services.receta_service import RecetaService
from utils.auth_dependencies import get_current_user


router = APIRouter(prefix="/recetas", tags=["Recetas"])


@router.get("/", response_model=list[RecetaRespuesta])
def listar_recetas(
    busqueda: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RecetaService(db).listar_recetas(busqueda)


@router.get("/{receta_id}", response_model=RecetaRespuesta)
def obtener_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RecetaService(db).obtener_receta(receta_id)


@router.post(
    "/",
    response_model=RecetaRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def crear_receta(
    datos: RecetaCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RecetaService(db).crear_receta(datos, usuario_actual)


@router.get(
    "/{receta_id}/ingredientes",
    response_model=list[IngredienteRecetaRespuesta],
)
def listar_ingredientes(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RecetaService(db).listar_ingredientes(receta_id)


@router.post(
    "/{receta_id}/ingredientes",
    response_model=IngredienteRecetaRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def agregar_ingrediente(
    receta_id: int,
    datos: IngredienteRecetaCrear,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RecetaService(db).agregar_ingrediente(
        receta_id,
        datos,
        usuario_actual,
    )

@router.patch("/{receta_id}", response_model=RecetaRespuesta)
def actualizar_receta(
    receta_id: int,
    datos: RecetaActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RecetaService(db).actualizar_receta(
        receta_id,
        datos,
        usuario_actual,
    )


@router.delete("/{receta_id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    RecetaService(db).desactivar_receta(receta_id, usuario_actual)


@router.patch(
    "/{receta_id}/ingredientes/{ingrediente_id}",
    response_model=IngredienteRecetaRespuesta,
)
def actualizar_ingrediente(
    receta_id: int,
    ingrediente_id: int,
    datos: IngredienteRecetaActualizar,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    return RecetaService(db).actualizar_ingrediente(
        receta_id,
        ingrediente_id,
        datos,
        usuario_actual,
    )


@router.delete(
    "/{receta_id}/ingredientes/{ingrediente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def desactivar_ingrediente(
    receta_id: int,
    ingrediente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),
):
    RecetaService(db).desactivar_ingrediente(
        receta_id,
        ingrediente_id,
        usuario_actual,
    )