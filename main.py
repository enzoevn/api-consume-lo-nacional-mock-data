from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from app.database import Database, create_mock_data
from app.models import AccessDevice, ResourceAccess
from app.routers import blogs, forums, products, requests, users

security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejador de eventos del ciclo de vida de la aplicación."""
    # Inicializar datos mock al arrancar
    create_mock_data()
    yield


# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Consume Lo Nacional API Mock",
    description="API para registro de usuarios, gestión de productos y blogs, seguimiento de recursos y foros.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(blogs.router)
app.include_router(requests.router)
app.include_router(forums.router)

# Configurar seguridad global
app.swagger_ui_init_oauth = {"usePkceWithAuthorizationCodeGrant": True}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para registrar accesos a recursos."""
    # Determinar el tipo de dispositivo (simplificado)
    user_agent = request.headers.get("user-agent", "").lower()
    device_type = AccessDevice.MOBILE if "mobile" in user_agent else AccessDevice.WEB

    # Registrar el acceso
    access = ResourceAccess(
        user=None,  # En una implementación real, obtendríamos el usuario autenticado
        deviceType=device_type,
    )
    Database.resource_accesses.append(access)

    response = await call_next(request)
    return response
