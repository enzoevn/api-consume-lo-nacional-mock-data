import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

# from app.database import Database, create_mock_data
from app.models import AccessDevice
from app.routers import blogs, forums, products, requests, users
from app.services.logger_service import LoggerService

security = HTTPBearer()

# Inicializar el servicio de logs
logger = LoggerService()

# Asegurar que el directorio logs existe
os.makedirs("logs", exist_ok=True)


# Esto solo se usa para inicializar datos mock al arrancar, ahora se usa la base de datos
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejador de eventos del ciclo de vida de la aplicación."""
    # Inicializar datos mock al arrancar
    # create_mock_data()
    yield


# Inicializar la aplicación FastAPI
app = FastAPI(
    title="Consume Lo Nacional API REST",
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
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(blogs.router, prefix="/api/v1")
app.include_router(requests.router, prefix="/api/v1")
app.include_router(forums.router, prefix="/api/v1")

# Configurar seguridad global
app.swagger_ui_init_oauth = {"usePkceWithAuthorizationCodeGrant": True}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para registrar accesos a recursos."""
    # Determinar el tipo de dispositivo (simplificado)
    user_agent = request.headers.get("user-agent", "").lower()
    device_type = AccessDevice.MOBILE if "mobile" in user_agent else AccessDevice.WEB

    # Registrar el acceso usando el servicio de logs
    logger.log_access(
        path=request.url.path,
        method=request.method,
        device_type=device_type,
        user_agent=user_agent,
    )

    response = await call_next(request)
    return response
