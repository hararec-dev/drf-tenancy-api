# 🚀 Boilerplate - Microservicio Django REST Framework

**🔍 Descripción General** 
Boilerplate para API REST con Django REST Framework (Python) usando una arquitectura organizada (siguiendo las convenciones de Django y DRF), Docker y buenas prácticas. Está inspirado en las convenciones de Django y patrones comunes de la comunidad.

## 📚 Tabla de Contenidos
1. [Requisitos Previos](#⚙️-requisitos-previos)
2. [Instalación](#🛠️-instalación)
3. [Uso de la API](#📡-uso-de-la-api)
4. [Contribución](#👥-contribución)
5. [Licencia](#📜-licencia)

## ⚙️ Requisitos Previos
* Python 3.12.3+
* Docker 24.0+ y Docker Compose

## 🛠️ Instalación
Configuración Local (sin Docker)
```bash
# Clonar repositorio
git clone https://github.com/hararec-dev/boilerplate-ms-drf.git
cd boilerplate-ms-drf
# Crear y activar un entorno virtual (recomendado)
python -m venv venv
# En Linux/macOS:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate
# Instalar dependencias
pip install -r requirements/base.in
# Configurar entorno (copiar variables de entorno)
cp .env.example .env
# (Asegúrate de configurar las variables en .env, especialmente la base de datos si no usas Docker)
# Aplicar migraciones de la base de datos
python manage.py migrate
# Crear un superusuario (opcional, para acceder al admin de Django)
python manage.py createsuperuser
# Iniciar el servidor de desarrollo
python manage.py runserver
# La API estará disponible en http://localhost:8000
```

#### Configuración con Docker
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/boilerplate-drf.git
cd boilerplate-drf
# Configurar entorno (Docker Compose usará .env por defecto)
cp .env.example .env
# (Ajusta las variables en .env si es necesario, especialmente las credenciales de la BD que usará Docker)
# Iniciar contenedores con Docker Compose
docker-compose up --build
# O si tu versión de docker es más reciente:
# docker compose up --build
# La API estará disponible en http://localhost:8000 (o el puerto que hayas mapeado en docker-compose.yml)
# Para ejecutar comandos de manage.py dentro del contenedor de Docker (ej. crear superusuario):
# docker-compose exec web python manage.py createsuperuser
```

## 📡 Uso de la API
La API base se encuentra en http://localhost:8000/api/v1/ (o el puerto que hayas configurado).
🔑 Autenticación (Ejemplo con Token - Simple JWT)
Si estás usando djangorestframework-simplejwt o similar:
```bash
# Ejemplo de login para obtener un token JWT con curl
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "tu_usuario", "password": "tu_password"}'
# Respuesta esperada:
# {
#   "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
# }
# Luego, para acceder a rutas protegidas:
curl -X GET http://localhost:8000/api/v1/tu-endpoint-protegido/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

## 👥 Contribución
1. Haz fork del proyecto (https://github.com/hararec-dev/boilerplate-ms-drf.git)
2. Crea tu branch: git checkout -b feature/nueva-funcionalidad
3. Realiza tus cambios y haz commit: git commit -m "Agrega nueva funcionalidad"
4. Push al branch: git push origin feature/nueva-funcionalidad
5. Abre un Pull Request.

## 📜 Licencia
MIT License - Ver [LICENSE](LICENCE) para más detalles.

* 🔄 Estado Actual: En desarrollo activo
* 📧 Contacto: hararecdev@ejemplo.com
