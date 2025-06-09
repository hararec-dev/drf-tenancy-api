# 🚀 Boilerplate - Microservicio Django REST Framework

**🔍 Descripción General** 
Boilerplate para API REST con Django REST Framework (Python) usando una arquitectura organizada (siguiendo las convenciones de Django y DRF), Docker y buenas prácticas. Está inspirado en las convenciones de Django y patrones comunes de la comunidad.

## 📚 Tabla de Contenidos
1. [Requisitos Previos](#⚙️-requisitos-previos)
2. [Instalación](#🛠️-instalación)
3. [Contribución](#👥-contribución)
4. [Licencia](#📜-licencia)
5. [Documentación Extra](#📄-documentación-extra)

## ⚙️ Requisitos Previos
* Python 3.12.3+
* Docker 24.0+ y Docker Compose

## 🛠️ Instalación
Clona el repositorio:
```bash
git clone https://github.com/hararec-dev/boilerplate-ms-drf.git
cd boilerplate-ms-drf
cp .env.example .env
```

Configuración Local (sin Docker)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/base.in
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### Configuración con Docker
```bash
docker-compose up --build
```
La API estará disponible en http://localhost:8000


## 👥 Contribución
1. Haz fork del proyecto (https://github.com/hararec-dev/boilerplate-ms-drf.git)
2. Crea tu branch: git checkout -b feature/nueva-funcionalidad
3. Realiza tus cambios y haz commit: git commit -m "Agrega nueva funcionalidad"
4. Push al branch: git push origin feature/nueva-funcionalidad
5. Abre un Pull Request.

## 📜 Licencia
MIT License - Ver [LICENSE](LICENCE) para más detalles.

* 🔄 Estado Actual: En desarrollo activo
* 🌐 ¡Visita mi web!: https://hararecdev.com

## 📄 Documentación Extra
Aquí puedes encontrar las plantillas de documentación utilizadas en este proyecto:
* [Documento de Especificación de Requisitos de Software (ERS)](./docs/ERS.md)
* [Documentación de Operaciones (OpsDocs)](./docs/OPS_DOCS.md)
* [Software Design Document (SDD)](./docs/SDD.md)
* [Documentación de Visión del Producto (Vision)](./docs/VISION.md)
* [Management Plan (Plan de Gestión)](./docs/MANAGEMENT_PLAN.md)