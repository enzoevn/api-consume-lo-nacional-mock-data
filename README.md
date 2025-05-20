# API Mock Consume Lo Nacional

API REST basada en FastAPI que implementa los endpoints definidos en el archivo swagger.yaml.

## Requisitos

- Python 3.8+
- FastAPI

## Instalación

### Desarrollo Local

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Iniciar el servidor:

```bash
fastapi dev
```

### Despliegue con Docker

1. Construir y ejecutar con Docker Compose:

```bash
docker-compose up --build
```

2. Para ejecutar en segundo plano:

```bash
docker-compose up -d
```

3. Para detener los contenedores:

```bash
docker-compose down
```

## Características

- API REST completa con datos mock
- Autenticación simulada con tokens
- Gestión de usuarios
- Gestión de productos y blogs
- Solicitudes de productos y blogs
- Foros por regiones

## Documentación

Una vez iniciado el servidor, puedes acceder a la documentación interactiva en:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usuarios Mock

La aplicación viene con los siguientes usuarios preconfigurados:

### Usuario Administrador
- Email: admin@example.com
- Nickname: admin
- Rol: EMPLOYEE
- Token: `Bearer admin-token`
- Estado: Activo

### Usuario Normal
- Email: user1@example.com
- Nickname: user1
- Rol: USER
- Token: `Bearer user1-token`
- Estado: Activo

### Usuario Bloqueado
- Email: user2@example.com
- Nickname: user2
- Rol: USER
- Token: `Bearer user2-token`
- Estado: Bloqueado

## Autenticación

Para probar endpoints que requieren autenticación, puedes usar los siguientes tokens:

- Usuario administrador: `Bearer admin-token`
- Usuario normal: `Bearer user1-token`
- Usuario bloqueado: `Bearer user2-token`

Estos tokens deben incluirse en el encabezado de autorización de las solicitudes.