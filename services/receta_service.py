from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.ingrediente_receta_model import IngredienteReceta
from models.receta_model import Receta
from models.usuario_model import Usuario
from repositories.receta_repository import RecetaRepository
from schemas.receta_schema import IngredienteRecetaCrear, RecetaCrear
from schemas.receta_schema import (
    IngredienteRecetaActualizar,
    RecetaActualizar,
)


class RecetaService:
    def __init__(self, db: Session):
        self.repository = RecetaRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def _validar_personal_nutricion(self, usuario: Usuario):
        rol = self._obtener_rol(usuario)

        if rol not in {"administrador", "nutricionista"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un administrador o nutricionista puede gestionar recetas.",
            )

    def listar_recetas(self, busqueda: str | None = None):
        return self.repository.listar(busqueda)

    def obtener_receta(self, receta_id: int) -> Receta:
        receta = self.repository.obtener(receta_id)

        if not receta or not receta.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receta no encontrada o inactiva.",
            )

        return receta

    def crear_receta(
        self,
        datos: RecetaCrear,
        usuario_actual: Usuario,
    ) -> Receta:
        self._validar_personal_nutricion(usuario_actual)

        if self.repository.obtener_por_codigo(datos.codigo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una receta con ese código.",
            )

        receta = Receta(
            codigo=datos.codigo.strip().upper(),
            nombre=datos.nombre.strip(),
            tipo_comida=datos.tipo_comida,
            instrucciones=datos.instrucciones,
        )

        return self.repository.crear(receta)

    def listar_ingredientes(self, receta_id: int):
        self.obtener_receta(receta_id)
        return self.repository.listar_ingredientes(receta_id)

    def agregar_ingrediente(
        self,
        receta_id: int,
        datos: IngredienteRecetaCrear,
        usuario_actual: Usuario,
    ) -> IngredienteReceta:
        self._validar_personal_nutricion(usuario_actual)
        self.obtener_receta(receta_id)

        alimento = self.repository.obtener_alimento(datos.alimento_id)
        if not alimento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alimento no encontrado o inactivo.",
            )

        ingrediente_existente = self.repository.obtener_ingrediente(
            receta_id,
            datos.alimento_id,
        )

        if ingrediente_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ese alimento ya está agregado a esta receta.",
            )

        ingrediente = IngredienteReceta(
            receta_id=receta_id,
            alimento_id=datos.alimento_id,
            cantidad=datos.cantidad,
            unidad=datos.unidad.strip(),
        )

        return self.repository.crear_ingrediente(ingrediente)
    
    def actualizar_receta(
        self,
        receta_id: int,
        datos: RecetaActualizar,
        usuario_actual: Usuario,
    ) -> Receta:
        self._validar_personal_nutricion(usuario_actual)
        receta = self.obtener_receta(receta_id)
        cambios = datos.model_dump(exclude_unset=True)

        if "codigo" in cambios:
            if cambios["codigo"] is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="El código no puede ser null.",
                )

            codigo = cambios["codigo"].strip().upper()
            existente = self.repository.obtener_por_codigo(codigo)

            if existente and existente.id != receta.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ya existe otra receta con ese código.",
                )

            cambios["codigo"] = codigo

        for campo in ("nombre", "tipo_comida"):
            if campo in cambios and cambios[campo] is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"{campo} no puede ser null.",
                )

        for campo, valor in cambios.items():
            if campo == "nombre" and valor is not None:
                valor = valor.strip()
            setattr(receta, campo, valor)

        return self.repository.guardar_receta(receta)


    def desactivar_receta(
        self,
        receta_id: int,
        usuario_actual: Usuario,
    ):
        self._validar_personal_nutricion(usuario_actual)
        receta = self.obtener_receta(receta_id)
        self.repository.desactivar_receta(receta)


    def actualizar_ingrediente(
        self,
        receta_id: int,
        ingrediente_id: int,
        datos: IngredienteRecetaActualizar,
        usuario_actual: Usuario,
    ) -> IngredienteReceta:
        self._validar_personal_nutricion(usuario_actual)
        self.obtener_receta(receta_id)

        ingrediente = self.repository.obtener_ingrediente_por_id(
            receta_id,
            ingrediente_id,
        )

        if not ingrediente or not ingrediente.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente no encontrado o inactivo.",
            )

        cambios = datos.model_dump(exclude_unset=True)

        for campo, valor in cambios.items():
            if campo == "unidad" and valor is not None:
                valor = valor.strip()
            setattr(ingrediente, campo, valor)

        return self.repository.guardar_ingrediente(ingrediente)


    def desactivar_ingrediente(
        self,
        receta_id: int,
        ingrediente_id: int,
        usuario_actual: Usuario,
    ):
        self._validar_personal_nutricion(usuario_actual)
        self.obtener_receta(receta_id)

        ingrediente = self.repository.obtener_ingrediente_por_id(
            receta_id,
            ingrediente_id,
        )

        if not ingrediente or not ingrediente.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente no encontrado o inactivo.",
            )

        self.repository.desactivar_ingrediente(ingrediente)  