# 🚀 Boilerplate - API Django REST Framework

**🔍 Descripción General** 
Boilerplate para API con Django REST Framework (Python) usando una arquitectura organizada (siguiendo las convenciones de Django y DRF), Docker y buenas prácticas. Está inspirado en las convenciones de Django y patrones comunes de la comunidad. 

> Incluye herramientas de calidad de código como Black para formateo, pre-commit para hooks de git, pytest y pytest-django para testing, coverage para medición de cobertura de código, y flake8 para análisis estático, asegurando así los más altos estándares de desarrollo.

## 📚 Tabla de Contenidos
1. [Requisitos Previos](#⚙️-requisitos-previos)
2. [Instalación](#🛠️-instalación)
3. [Contribución](#👥-contribución)
4. [Licencia](#📜-licencia)
5. [Documentación Extra](#📄-documentación-extra)

## ⚙️ Requisitos Previos
* Python 3.13.4+ y Pipenv
* Docker 24.0+ y Docker Compose

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone git@github.com:hararec-dev/boilerplate-api-drf.git
cd boilerplate-api-drf
cp .env.example .env
# (Opcional) Personaliza el archivo .env según tus necesidades
```

---

### 2. Configuración para desarrollo local

```bash
# Instala los hooks de pre-commit
pre-commit install

# (Opcional) Ejecuta todos los linters y formateadores manualmente
pre-commit run --all-files

# Levanta una base de datos local con Docker
docker compose -f docker-compose.dev.yml up -d --build

# Instala las dependencias del entorno virtual
pipenv install --dev
pipenv shell

# Aplica las migraciones
python manage.py makemigrations
python manage.py migrate

# Inicia el servidor de desarrollo
python manage.py runserver
```

> La API estará disponible en: [http://localhost:8000](http://localhost:8000)

---

### 3. Configuración para producción

```bash
# Ejecuta la API con múltiples instancias (por ejemplo: n=2)
docker compose -f docker-compose.prod.yml up -d --build --scale api=n

# Puedes acceder al contenedor de la API con:
docker exec -it boilerplate-api-drf-api-1 /bin/bash
```



## 👥 Contribución
1. Haz fork del proyecto (https://github.com/hararec-dev/boilerplate-api-drf.git)
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