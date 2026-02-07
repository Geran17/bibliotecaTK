# Backlog Tecnico (Issue List)

Estado: propuesto  
Alcance: mejoras funcionales sin cambios en la estructura de base de datos  
Escala de esfuerzo: `S` (1-2 dias), `M` (3-5 dias), `L` (1-2 semanas)

## Fase 1 (Alta prioridad)

- [x] `BUG` Guardado incorrecto de ruta de portadas en configuracion
  - Impacto: alto
  - Esfuerzo: `S`
  - Referencia: `src/models/controllers/configuracion_controller.py:95`
  - Criterio de aceptacion: al configurar biblioteca, `obtener_ubicacion_biblioteca()` y `obtener_ubicacion_portadas()` devuelven rutas distintas y validas.

- [x] `MEJORA` Implementar refresco real en pestanas con `actualizar_tabla()`
  - Impacto: alto
  - Esfuerzo: `M`
  - Referencias: `src/views/frames/frame_visualizar_documentos.py:178`, `src/views/frames/frame_visualizar_biblioteca.py:92`, `src/views/frames/frame_visualizar_estante.py:136`
  - Criterio de aceptacion: boton "Refrescar" en `FrameCentral` actualiza datos visibles en todas las pestanas activas.

- [x] `BUG` Refresco global silencia errores y dificulta soporte
  - Impacto: alto
  - Esfuerzo: `S`
  - Referencia: `src/views/frames/frame_central.py:421`
  - Criterio de aceptacion: errores de refresco quedan logueados y se muestra mensaje resumido al usuario cuando falle una pestana.

- [x] `QUALITY` Alinear tests DAO con arquitectura de conexion actual
  - Impacto: alto
  - Esfuerzo: `L`
  - Referencias: `tests/daos/test_coleccion_dao.py:20`, `src/models/daos/dao.py:31`
  - Criterio de aceptacion: tests no dependen de `dao._db`; pasan con la estrategia de conexion vigente.

- [x] `QUALITY` Corregir estrategia de tests SQLite en memoria por operacion
  - Impacto: alto
  - Esfuerzo: `M`
  - Referencia: `src/models/daos/dao.py:36`
  - Criterio de aceptacion: fixtures usan BD temporal en archivo o conexion compartida; desaparecen errores `no such table`.

## Fase 2 (Producto y UX)

- [x] `FEATURE` Completar accion "Comparar existentes" en importacion
  - Impacto: alto
  - Esfuerzo: `M`
  - Referencia: `src/views/frames/frame_importar_documento.py:243`
  - Criterio de aceptacion: muestra diferencias por nombre/hash/ruta entre seleccion y biblioteca, sin alterar BD.

- [x] `FEATURE` Integrar acceso funcional a "Metadatos" desde panel lateral
  - Impacto: medio
  - Esfuerzo: `M`
  - Referencia: `src/views/frames/frame_central.py:124`
  - Criterio de aceptacion: boton abre dialogo/pestana funcional para ver metadatos del documento seleccionado.

- [x] `FEATURE` Integrar "Contenido" en administrar documentos
  - Impacto: medio
  - Esfuerzo: `M`
  - Referencia: `src/views/frames/frame_administrar_documentos.py:271`
  - Criterio de aceptacion: boton abre flujo real de capitulos/secciones para documentos seleccionados.

- [x] `MEJORA UX` Estante con carga inicial util (no vacio)
  - Impacto: alto
  - Esfuerzo: `M`
  - Referencia: `src/models/controllers/controlar_visualizar_estante.py:100`
  - Criterio de aceptacion: al abrir estante se ven documentos recientes o catalogo paginado por defecto.

- [x] `MEJORA UX` Busqueda "Todo" con termino vacio debe mostrar catalogo
  - Impacto: medio
  - Esfuerzo: `S`
  - Referencia: `src/models/controllers/controlar_visualizar_estante.py:113`
  - Criterio de aceptacion: con campo `Todo` y termino vacio se carga listado paginado.

## Fase 3 (Confiabilidad y mantenimiento)

- [x] `MEJORA` Operaciones en lote con vista previa y confirmacion
  - Impacto: alto
  - Esfuerzo: `M`
  - Referencia: `src/models/controllers/controlar_operaciones_documentos.py:89`
  - Criterio de aceptacion: antes de ejecutar copiar/mover/eliminar muestra resumen (cantidad/ruta destino) y confirma.

- [x] `REFACTOR FUNCIONAL` Unificar apertura de documentos en una sola utilidad de flujo
  - Impacto: medio
  - Esfuerzo: `M`
  - Referencias: `src/models/controllers/controlar_favoritos.py`, `src/models/controllers/controlar_visualizar_biblioteca.py`, `src/models/controllers/controlar_visualizar_contenido.py`
  - Criterio de aceptacion: comportamiento consistente de abrir documento y manejo de errores.

- [x] `BUG` Metodo duplicado `on_abrir_carpeta` en controlador de documento seleccionado
  - Impacto: medio
  - Esfuerzo: `S`
  - Referencia: `src/models/controllers/controlar_documento_seleccionado.py:183`
  - Criterio de aceptacion: queda una unica implementacion, probada desde UI.

- [x] `MEJORA` Reemplazar `print()` por logging estructurado en controladores/DAO
  - Impacto: medio
  - Esfuerzo: `M`
  - Referencias: `src/views/frames/frame_menu.py:124`, `src/models/daos/dao.py:94`
  - Criterio de aceptacion: errores criticos quedan en log con contexto y nivel (`info/warn/error`).

- [x] `QUALITY` Pipeline minimo de smoke tests de flujos criticos
  - Impacto: medio
  - Esfuerzo: `M`
  - Alcance: importar, buscar, abrir, favoritos, asociaciones
  - Criterio de aceptacion: suite rapida (< 3 min) para validar release sin tocar esquema BD.

## Orden recomendado de implementacion

1. Fase 1: `#1 #2 #3 #4 #5`
2. Fase 2: `#6 #7 #8 #9 #10`
3. Fase 3: `#11 #12 #13 #14 #15`

## Plantilla corta para crear issues

```md
## Objetivo
[Descripcion breve]

## Contexto
- Tipo: BUG / FEATURE / MEJORA / QUALITY
- Impacto: alto/medio/bajo
- Esfuerzo: S/M/L
- Referencias: [archivo:linea]

## Criterios de aceptacion
- [ ] Criterio 1
- [ ] Criterio 2

## Notas tecnicas
- Restriccion: no cambiar estructura de BD
```
