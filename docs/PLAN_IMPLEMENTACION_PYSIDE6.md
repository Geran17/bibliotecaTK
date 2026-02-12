# Plan de Ataque PySide6

## Objetivo

Construir una version PySide6 mas funcional y mantenible que la version Tkinter, con arquitectura propia de Qt, UX mas fluida y seleccion persistente de entorno visual.

## Principios de implementacion

- Separar UI de logica: controladores en `models/controllers`, vistas Qt en `views/qt`.
- Diseñar para escalabilidad: modulos por feature, no por tipo de widget.
- Priorizar experiencia de usuario: feedback, accesos rapidos, estados claros y operaciones no bloqueantes.
- Aprovechar capacidades Qt: `QMainWindow`, `QDockWidget`, `QTabWidget`, `QThreadPool`, `QSortFilterProxyModel`, `QStyle` icons, shortcuts.

## Arquitectura propuesta (PySide6)

Estructura recomendada:

```text
src/views/qt/
  app.py
  main_window.py
  shared/
    iconos.py
    actions.py
    mensajes.py
  features/
    documentos/
      page.py
      table_model.py
      toolbar.py
      dialogs/
    colecciones/
      page.py
      model.py
      dialogs/
    busqueda/
      page.py
    configuracion/
      page.py
```

Notas:

- `shared/` contiene utilidades transversales Qt.
- Cada feature encapsula su pagina, modelos y dialogos.
- Evitar un directorio global de `frames` gigantes.

## Estado actual (base ya disponible)

- Selector de entorno persistente (`tkinter`/`pyside6`) en configuracion.
- `main.py` ya arranca segun CLI/ENV/INI.
- Ventana principal Qt disponible.
- Pestaña de configuracion Qt creada.
- Iconos nativos Qt base integrados en toolbar y panel lateral:
  - `src/views/qt/shared/iconos.py`
  - `src/views/qt/main_window.py`
- Fase 2 iniciada con primera feature real:
  - `src/views/qt/features/colecciones/page.py` (CRUD + busqueda + tabla + navegacion)
  - pestaña `Colecciones` conectada en `src/views/qt/main_window.py`
- Segunda feature de Fase 2 ya operativa:
  - `src/views/qt/features/grupos/page.py` (CRUD + busqueda + tabla + navegacion)
  - pestaña `Grupos` conectada en `src/views/qt/main_window.py`
- Tercera feature de Fase 2 ya operativa:
  - `src/views/qt/features/categorias/page.py` (CRUD + busqueda + tabla + navegacion)
  - pestaña `Categorias` conectada en `src/views/qt/main_window.py`
- Cuarta feature de Fase 2 ya operativa:
  - `src/views/qt/features/etiquetas/page.py` (CRUD + busqueda + tabla + navegacion)
  - pestaña `Etiquetas` conectada en `src/views/qt/main_window.py`
- Quinta feature de Fase 2 ya operativa:
  - `src/views/qt/features/palabras_clave/page.py` (CRUD + busqueda + tabla + navegacion)
  - pestaña `Palabras clave` conectada en `src/views/qt/main_window.py`

## Roadmap por fases

### Fase 1: Shell de aplicacion (1 semana)

- Consolidar layout principal:
  - Toolbar superior de acciones.
  - Panel lateral navegable por modulos.
  - Tabs principales y barra de estado.
- Definir `QAction` centralizadas con shortcuts.
- Integrar mensajes de estado y errores consistentes.

Entregable:

- Shell navegable con acciones stub y UX consistente.

### Fase 2: Colecciones (1 semana)

- Implementar pagina `Colecciones` en Qt.
- CRUD completo usando `Consulta` + entidades actuales.
- Tabla con filtro y seleccion robusta.
- Formularios con validacion.

Entregable:

- Feature `Colecciones` operativa 100%.

### Fase 3: Documentos (2-3 semanas)

- Implementar pagina `Documentos` como prioridad funcional.
- Tabla escalable (`QAbstractTableModel` + `QSortFilterProxyModel`).
- Operaciones: abrir, abrir carpeta, renombrar, copiar, mover, eliminar/papelera.
- Menus contextuales y accion por lotes.
- Progreso no bloqueante con `QThreadPool`.

Entregable:

- Administracion de documentos estable y fluida.

Estado actual:

- Fase 3 completada (funcional):

  - `src/views/qt/features/documentos/model.py` (`QAbstractTableModel` + `QSortFilterProxyModel`)
  - `src/views/qt/features/documentos/page.py` (tabla, busqueda global, refresh, ordenamiento)
  - acciones base implementadas: abrir, abrir carpeta, renombrar, copiar, mover,
    papelera, eliminar y propiedades (toolbar + menu contextual)
  - operaciones por lote con `QThreadPool` + progreso:
    copiar/mover/papelera/eliminar sobre seleccion multiple
    (`src/views/qt/features/documentos/worker.py`)
  - cancelacion de lotes + bloqueo de acciones durante ejecucion
  - menu contextual con asociacion organizativa del documento:
    coleccion, grupo, categoria, etiqueta y palabra clave
  - menu contextual con desasociacion organizativa del documento:
    coleccion, grupo, categoria, etiqueta y palabra clave
  - simplificacion de interfaz: se removio el panel inferior de asociaciones/chips
    para priorizar tabla y operaciones
  - persistencia de estado de vista de documentos:
    busqueda, sort, ancho de columnas y documento seleccionado
  - pestaña `Documentos` integrada en `src/views/qt/main_window.py`
  - persistencia de pestañas Qt:
    abiertas/cerradas, orden y activa
  - persistencia de estado de ventana Qt:
    geometria, estado de docks/toolbars y visibilidad de panel lateral

### Cierre de Fase 3 (control de salida)

- Funcionalidad principal: completada.
- Pendiente de cierre tecnico:
  - ejecutar checklist manual de regresion de `Documentos` en entorno local writable
  - agregar pruebas minimas automatizadas para operaciones de documentos (DAO/controlador)
  - homogenizar textos de error/confirmacion en operaciones de archivo

### Fase 4: Importar + Metadatos + Contenido (2 semanas)

- Flujo de importacion masivo con progreso cancelable.
- Visor metadatos en panel/tab.
- Gestion de contenido bibliografico y secciones.

Entregable:

- Flujo de trabajo principal de biblioteca completo.

### Fase 5: Pulido UX y calidad (1-2 semanas)

- Atajos de teclado.
- Persistencia de estado de UI (ancho de columnas, tab activa, panel lateral, filtros).
- Manejo de errores unificado.
- Testing minimo de controladores y casos criticos de UI.

Entregable:

- Release candidate PySide6.

## Implementacion de iconos (Qt nativos)

- Mantener iconografia via `QStyle.StandardPixmap` para look nativo y cero dependencias.
- Reglas:
  - Action siempre con icono + texto.
  - Botones primarios con icono cuando aporte reconocimiento.
  - Reusar nombres semanticos (`importar`, `refrescar`, `configuracion`, etc.).
- Archivo base:
  - `src/views/qt/shared/iconos.py`

## Backlog funcional priorizado

Prioridad alta:

1. Importar: flujo completo con progreso cancelable.
2. Metadatos: visor y edicion operativa en Qt.
3. Contenido: capitulos/secciones con flujo completo.

Prioridad media:

1. Categorias, grupos, etiquetas, palabras clave.
2. Favoritos.
3. Visor metadatos.

Prioridad baja:

1. Estante visual.
2. Mejoras esteticas avanzadas.
3. Telemetria local de rendimiento.

## Lineamientos UX para PySide6

- No bloquear UI en operaciones de disco/BD.
- Mostrar feedback inmediato:
  - `statusBar` para eventos cortos.
  - dialogs para confirmaciones y errores de alto impacto.
- Confirmar acciones destructivas.
- Preservar contexto del usuario (seleccion actual, filtros, scroll).
- Atajos recomendados:
  - `Ctrl+F`: buscar
  - `Ctrl+R`: refrescar
  - `Ctrl+,`: configuracion
  - `Del`: enviar a papelera

## Criterios de aceptacion por feature

- CRUD funcional sin regresiones en BD.
- UI no se congela en operaciones costosas.
- Errores manejados con mensaje claro.
- Estado persistente de preferencias clave.
- Cobertura de pruebas basica en controladores involucrados.

## Estrategia de migracion desde Tkinter

1. Mantener ambos entornos activos.
2. Migrar por feature completa, no por widget aislado.
3. Cuando una feature Qt alcance paridad, marcar feature Tk como legacy.
4. Evitar duplicar logica: reutilizar `models/controllers` y entidades.

## Siguiente sprint recomendado (accionable)

1. Implementar feature `Importar` en Qt con cola, progreso y cancelacion.
2. Implementar feature `Metadatos` en Qt reutilizando controladores existentes.
3. Implementar feature `Contenido` (capitulos/secciones) con operaciones no bloqueantes.
4. Ejecutar checklist de cierre de Fase 3 y abrir Fase 4 formalmente.

Referencia detallada:

- `docs/PLAN_FASE4_PYSIDE6.md`
