# Management Plan

## 1. Políticas de Control de Versiones
- **Repositorio Principal:** [URL del repositorio Git]
- **Modelo de Branching:**  
  - Rama `main`/`master`: Contiene la versión de producción estable.  
  - Rama `develop`: Integración de funcionalidades en curso.  
  - Ramas `feature/*`: Desarrollo de nuevas funcionalidades.  
  - Ramas `hotfix/*`: Corrección de errores críticos en producción.

## 2. Ramas y Etiquetado
- **Convenciones de Nombres:**  
  - Features: `feature/<número>-<descripción>`  
  - Hotfixes: `hotfix/<número>-<descripción>`  
  - Releases: `release/<versión>`
- **Etiquetas (Tags):**  
  - Formato: `v<major>.<minor>.<patch>` (ej: `v1.0.0`)
- **Procedimiento de Versionado:**  
  1. Crear rama `release` desde `develop` cuando se alcance la madurez necesaria.  
  2. Realizar pruebas finales en la rama `release`.  
  3. Merge de `release` a `main` y etiquetar con `vX.Y.Z`.  
  4. Merge de `main` a `develop` para sincronizar.

## 3. Procedimientos de Release
- **Preparación:**  
  1. Asegurar que todos los tests pasen en `develop`.  
  2. Crear rama `release/<versión>` y actualizar el archivo de versión en el proyecto.
- **Validación:**  
  - Realizar pruebas de integración y regresión en entorno de staging.  
  - Verificar checklist de QA y performance.
- **Despliegue a Producción:**  
  1. Hacer merge de `release/<versión>` a `main`.  
  2. Etiquetar el commit con `v<versión>`.  
  3. Desplegar artefactos al entorno de producción.  
  4. Verificar despliegue y sanity checks.

## 4. Procedimientos de Rollback
- **Criterios de Rollback:**  
  - Fallos críticos en producción que no pueden ser solucionados con un hotfix inmediato.  
- **Pasos de Rollback:**  
  1. Identificar la última etiqueta estable (`vX.Y.Z-1`).  
  2. En entorno de producción, revertir al commit etiquetado o redeplegar artefactos de la versión anterior.  
  3. Monitorear servicios y comprobar funcionalidad.  
  4. Informar a los stakeholders sobre el estado de rollback y plan de corrección.

## 5. Liberaciones y Mantenimiento
- **Frecuencia de Release:** Cada 2-4 semanas o según roadmap.  
- **Plan de Mantenimiento:**  
  - Soporte de versiones LTS: mantenimientos críticos hasta 12 meses.  
  - Actualizaciones menores de seguridad cada mes.  

## 6. Roles y Responsabilidades
- **Release Manager:** Coordina el proceso de release y rollback.  
- **Equipo de Desarrollo:** Realiza merge requests, pruebas de pre-lanzamiento.  
- **Equipo de QA:** Valida calidad y aprueba despliegues.  
- **Equipo de DevOps:** Automatiza despliegues y gestiona entornos.
