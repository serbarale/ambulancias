# Sistema de Gestión de Ambulancias
**Trabajo ISW2/3**

## Descripción del Proyecto

Sistema web para la gestión integral de ambulancias de emergencia, desarrollado en Django. El sistema permite administrar las ambulancias, inventarios médicos, historiales de pacientes y reportes de emergencias.

## Funcionalidades Principales

### Módulo de Ambulancias
- Registro y gestión de ambulancias
- Control de averías y mantenimiento
- Seguimiento de combustible
- Listado y filtrado de vehículos

### Módulo de Emergencias
- Registro de informes de emergencia
- Gestión de consentimientos y revocaciones
- Reportes por prioridad y estado
- Asignación de ambulancias a emergencias

### Módulo de Inventarios
- Control de stock de insumos médicos
- Sistema de checklist para ambulancias
- Alertas de stock bajo y productos vencidos
- Solicitudes automáticas de reposición

### Módulo de Pacientes
- Registro de pacientes con validación de DNI
- Gestión de historiales médicos
- Búsqueda por DNI y nombre
- Actualización de información médica

## Tecnologías Utilizadas

- **Backend**: Django 4.2.7
- **Base de Datos**: SQLite (desarrollo)
- **Testing**: pytest 7.4.0, pytest-django 4.5.2
- **Frontend**: HTML, CSS, Bootstrap
- **Arquitectura**: Patrón DAO/Service