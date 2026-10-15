from contextlib import asynccontextmanager

from fastapi import FastAPI


from config.database import Base, engine

from models.rol_model import Rol
from models.usuario_model import Usuario
from models.paciente_model import Paciente
from models.modulo_model import Modulo
from models.moduloxrol_model import ModuloPorRol
from models.consentimiento_model import Consentimiento
from models.condicion_medica_model import CondicionMedica
from models.paciente_condicion_model import PacienteCondicion
from models.restriccion_alimentaria_model import RestriccionAlimentaria
from models.alimento_model import Alimento
from models.alimento_region_model import AlimentoRegion
from models.receta_model import Receta
from models.ingrediente_receta_model import IngredienteReceta
from models.objetivo_nutricional_model import ObjetivoNutricional
from models.plan_nutricional_model import PlanNutricional
from models.version_plan_model import VersionPlan
from models.detalle_plan_model import DetallePlan
from models.control_nutricional_model import ControlNutricional
from models.cita_model import Cita


from controllers.alimento_region_controller import (
    router as alimento_region_router,
)
from controllers.alimento_controller import router as alimento_router
from controllers.usuario_controller import router as usuario_router
from controllers.paciente_controller import router as paciente_router
from controllers.rol_controller import router as rol_router
from controllers.auth_controller import router as auth_router
from controllers.condicion_controller import router as condicion_router
from controllers.restriccion_controller import router as restriccion_router
from controllers.receta_controller import router as receta_router
from controllers.objetivo_controller import router as objetivo_router
from controllers.plan_nutricional_controller import (
    router as plan_nutricional_router,
)
from controllers.modulo_controller import router as modulo_router
from controllers.detalle_plan_controller import router as detalle_plan_router
from controllers.control_nutricional_controller import (
    router as control_nutricional_router,
)
from controllers.cita_controller import router as cita_router
from controllers.consentimiento_controller import (
    router as consentimiento_router,
)



@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    

app = FastAPI(
    title="Nutri API",
    description="API principal de Nutri con PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(rol_router)
app.include_router(auth_router)
app.include_router(paciente_router)
app.include_router(usuario_router)
app.include_router(condicion_router)
app.include_router(restriccion_router)
app.include_router(alimento_router)
app.include_router(alimento_region_router)
app.include_router(receta_router)
app.include_router(objetivo_router)
app.include_router(plan_nutricional_router)
app.include_router(modulo_router)
app.include_router(detalle_plan_router)
app.include_router(control_nutricional_router)
app.include_router(cita_router)
app.include_router(consentimiento_router)
