# Plan Detallado - Fase 4 PySide6

## Objetivo de Fase 4
Completar el flujo principal de uso en Qt con tres features:
- Importar (masivo y no bloqueante)
- Metadatos (visualizacion/edicion)
- Contenido (capitulos y secciones)

## Estado actual de implementacion
- Bloque Importar:
  - `src/views/qt/features/importar/page.py` implementado
  - `src/views/qt/features/importar/worker.py` implementado (`QThreadPool`, progreso, cancelacion)
  - persistencia de estado (`modo`, `ultima_ruta`) en configuracion INI
- Bloque Metadatos:
  - `src/views/qt/features/metadatos/page.py` implementado (documentos + CRUD de metadatos)
- Bloque Contenido:
  - `src/views/qt/features/contenido/page.py` implementado (capitulos/secciones CRUD)
- Integracion UI:
  - tabs y acciones conectadas en `src/views/qt/main_window.py`

## Alcance funcional
- Migrar funcionalidades clave existentes de Tkinter a PySide6 sin duplicar logica de negocio.
- Reutilizar controladores/entidades actuales desde `models/controllers` y `models/entities`.
- Mantener consistencia UX con el backend Qt ya implementado (tabs, iconos, persistencia, feedback).

## Estructura propuesta
- `src/views/qt/features/importar/page.py`
- `src/views/qt/features/importar/worker.py`
- `src/views/qt/features/metadatos/page.py`
- `src/views/qt/features/contenido/page.py`
- Integracion de tabs y acciones en `src/views/qt/main_window.py`

## Plan por semanas

### Semana 1 - Importar + Base de Metadatos
Entregables:
- Feature `Importar` operativa en Qt:
  - seleccion de archivos/carpeta
  - cola de importacion
  - barra de progreso
  - cancelacion
  - reporte de resultados (ok/error)
- Operacion no bloqueante con `QThreadPool`.
- Persistencia minima de estado de Importar (ultima carpeta usada y modo de importacion).
- Tab inicial de `Metadatos`:
  - carga de metadatos por documento seleccionado
  - tabla/listado editable basico (clave/valor)

Criterios de aceptacion:
- La UI no se congela durante importacion masiva.
- Cancelar detiene nuevos items y marca estado de la corrida.
- Errores de importacion quedan visibles por item.
- Metadatos abre y muestra datos reales del documento.

### Semana 2 - Contenido + Cierre Metadatos + Integracion
Entregables:
- Feature `Contenido` operativa en Qt:
  - listado de capitulos por documento
  - listado de secciones por capitulo
  - CRUD basico (crear/editar/eliminar) de capitulos y secciones
- Metadatos cerrado:
  - crear/editar/eliminar metadatos
  - validaciones basicas
- Integracion de tabs/acciones en `main_window.py`.
- Persistencia de estado de vistas nuevas (filtros/seleccion basica donde aplique).

Criterios de aceptacion:
- Flujos CRUD de contenido funcionan sin regresiones de BD.
- Metadatos se persiste correctamente en BD.
- Navegacion y acciones desde toolbar/panel lateral estables.
- Errores y confirmaciones consistentes con Documentos.

## Backlog tecnico (orden recomendado)
1. Crear skeleton UI de `Importar` con stubs.
2. Implementar worker de importacion por lote y señalizacion de progreso.
3. Conectar importacion con controladores existentes.
4. Crear `MetadatosPageQt` con lectura/edicion basica.
5. Crear `ContenidoPageQt` con maestro-detalle (capitulos/secciones).
6. Integrar nuevas tabs en `MainWindowQt`.
7. Añadir persistencia de estado para nuevas vistas.
8. Ajustar textos y manejo de errores unificado.

## Riesgos y mitigacion
- Riesgo: bloqueo UI por operaciones de disco/BD.
  - Mitigacion: ejecutar cargas masivas en `QThreadPool`, actualizar UI por signals.
- Riesgo: divergencia funcional respecto a Tkinter.
  - Mitigacion: validar cada feature con checklist de paridad funcional.
- Riesgo: regresiones en operaciones destructivas.
  - Mitigacion: confirmaciones explicitas y pruebas manuales dirigidas.

## Checklist de cierre Fase 4
- [ ] Importar masivo con progreso y cancelacion validado.
- [ ] Metadatos CRUD validado con datos reales.
- [ ] Contenido CRUD validado (capitulos/secciones).
- [ ] Integracion en tabs Qt y navegacion lateral completada.
- [ ] Persistencia minima de estado en vistas nuevas.
- [ ] Errores y confirmaciones unificados.
- [ ] Checklist manual ejecutada en entorno writable.

## Definition of Done (Fase 4)
- Features `Importar`, `Metadatos` y `Contenido` funcionales en Qt.
- Sin bloqueos perceptibles de UI en operaciones largas.
- Sin errores de bindings SQL en flujos principales.
- Documentacion actualizada en `docs/PLAN_IMPLEMENTACION_PYSIDE6.md`.
