# 🚀 DRF Tenancy API


## Descripción

Una API **multi-tenant** escalable construida con **Django REST Framework**, pensada como base para proyectos **SaaS**. Gestiona múltiples clientes de forma aislada, rápida y segura. Incluye configuraciones listas para desarrollo y producción, despliegue escalable, calidad de código garantizada y diseño para soportar miles de conexiones simultáneas sin degradar la latencia.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/github/v/release/hararec-dev/drf-tenancy-api)](https://github.com/hararec-dev/drf-tenancy-api/releases)
[![Last Commit](https://img.shields.io/github/last-commit/hararec-dev/drf-tenancy-api)](https://github.com/hararec-dev/drf-tenancy-api/commits/main)
[![Issues](https://img.shields.io/github/issues/hararec-dev/drf-tenancy-api)](https://github.com/hararec-dev/drf-tenancy-api/issues)
[![Language](https://img.shields.io/github/languages/top/hararec-dev/drf-tenancy-api)](https://github.com/hararec-dev/drf-tenancy-api)
[![Contributors](https://img.shields.io/github/contributors/hararec-dev/drf-tenancy-api)](https://github.com/hararec-dev/drf-tenancy-api/graphs/contributors)
[![Stars](https://img.shields.io/github/stars/hararec-dev/drf-tenancy-api)](https://github.com/hararec-dev/drf-tenancy-api)

---

## 🌟 Características Principales

* ✅ **Multi-Tenant**: Soporte nativo para múltiples inquilinos con aislamiento de datos.
* ✅ **PostgreSQL**: Esquema de base de datos normalizado y optimizado para arquitecturas multi-tenant.
* ✅ **Docker & Docker Compose**: Configuraciones dedicadas para entornos de desarrollo y producción.
* ✅ **Reverse Proxy y Balanceo de Carga**: Configuración robusta usando Nginx.
* ✅ **ASGI Server**: Uvicorn con Gunicorn para manejo eficiente de conexiones concurrentes y hot-reload opcional.
* ✅ **Caching**: Integración con Redis para almacenamiento en caché.
* ✅ **Rate Limiting y Throttling**: Control de acceso y uso de la API para proteger contra ataques DDoS.
* ✅ **Vistas basadas en clases (CBV)**: Organización escalable y reutilizable.
* ✅ **Permisos y control de acceso**: Basado en roles y policies personalizables.
* ✅ **Paginación, Búsqueda y Filtrado**: Soporte listo para integrarse con listas de resultados.
* ✅ **Versionado de la API**: Versiones futuras sin romper contratos existentes.
* ✅ **Manejo de Excepciones**: Sistema centralizado para respuestas coherentes.
* ✅ **CORS**: Configurable para acceso controlado desde frontends externos.
* ✅ **Documentación Automática**: Swagger/OpenAPI y ReDoc integrados.
* ✅ **Logging y Monitoreo**: Configuraciones para trazabilidad y debugging.
* ✅ **Configuración y Buenas Prácticas**: flake8, black, isort, pre-commit, Pipenv.
* ✅ **Registro de Datos**: Auditoría básica con logging persistente de acciones clave.
<!-- * ✅ **Tareas Asíncronas**: Uso de Celery con RabbitMQ para procesamiento en segundo plano. -->
<!-- * ✅ **Carga y Envió de Archivos**: Endpoints para subir y descargar archivos. -->

<!-- ---

## 📚 Tabla de Contenidos

1. [Requisitos Previos](#-requisitos-previos)
2. [Instalación Rápida](#-instalaci%C3%B3n-r%C3%A1pida)
3. [Uso](#-uso)

   * [Entorno de Desarrollo](#entorno-de-desarrollo)
   * [Entorno de Producción](#entorno-de-producci%C3%B3n)
4. [Documentación de la API](#-documentaci%C3%B3n-de-la-api)
5. [Testing](#-testing)
6. [CI/CD](#-cicd)
5. [Contribución](#-contribuci%C3%B3n)
6. [Licencia](#-licencia)
7. [Contacto](#-contacto) -->

---

## 🛠️ Requisitos Previos

* **Python** 3.13.4+ & `pipenv`
* **Docker** 24.0+
* **Docker Compose**  v2+

---

## ⚡ Instalación Rápida

### 1. Clonar y configurar

```bash
# Clonar el repositorio (es buena práctica usar SSH)
git clone git@github.com:hararec-dev/drf-tenancy-api.git
```

```bash
# Entrar al directorio del proyecto
cd drf-tenancy-api
```

```bash
# Crear archivo de entorno a partir del ejemplo
cp .env.example .env
```

> Personaliza variables en `.env` según tu entorno

---

### 2. Entorno de Desarrollo

```bash
# Instalar las dependencias del entorno virtual
pipenv install --dev
```

```bash
# Activar el entorno virtual
pipenv shell
```

```bash
# Instalar los hooks de pre-commit
pre-commit install
```

```bash
# Levantar los servicios (API, DB, Redis, etc.) en modo desarrollo
docker compose -f docker-compose.dev.yml up -d --build
```

```bash
# Crear archivos de migraciones
python manage.py makemigrations
```

```bash
# Aplicar migraciones a la base de datos
python manage.py migrate
```

```bash
# Iniciar el servidor de desarrollo
python manage.py runserver 0.0.0.0:8000
```

> API disponible en: [http://localhost:8000](http://localhost:8000)

---

### 3. Entorno de Producción

```bash
# Ejecutar la API con múltiples instancias (por ejemplo: n=2)
docker compose -f docker-compose.prod.yml up -d --build --scale api=2
```

```bash
# Acceder al contenedor de la API
docker exec -it $(docker ps -qf "name=drf-tenancy-api_api") bash
```

---

## 📄 Documentación de la API

Automáticamente generada con Swagger/OpenAPI:

* Swagger UI: `http://<host>/api/schema/swagger-ui`
* ReDoc: `http://<host>/api/schema/redoc`

<!-- ---

## 🚦 Testing

```bash
# Ejecutar tests y generar reporte de cobertura
docker compose -f docker-compose.dev.yml run --rm api pytest --cov=.
```

---

## 🤖 CI/CD

La carpeta `.github/workflows/ci.yml` incluye un pipeline que:

1. Instala dependencias
2. Ejecuta linters y formateo
3. Corre pruebas y verifica cobertura mínima
4. Publica badge de estado en el README -->

---

## 🤝 Contribución

1. Haz fork del repositorio
2. Crea tu rama: `git checkout -b feature/tu-mejora`
3. Realiza tus cambios y haz commit: `git commit -m "feat: descripción de tu mejora"`
4. Envía tu rama: `git push origin feature/tu-mejora`
5. Abre un Pull Request y describe tu contribución.

---

## 📜 Licencia

Este proyecto está licenciado bajo MIT License. Consulta el archivo [LICENSE](LICENSE) para más información.

---

## 📬 Contacto

* **Web**: [https://hararecdev.com](https://hararecdev.com)
* **Email**: [hararecdev@gmail.com](mailto:hararecdev@gmail.com)

> *Estado Actual: Desarrollo activo 🚧*
