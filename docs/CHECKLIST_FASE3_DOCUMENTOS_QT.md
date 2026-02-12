# Checklist Fase 3 - Documentos Qt

## Objetivo
Validar que la feature `Documentos` en PySide6 esta estable antes de declarar la fase cerrada.

## Precondiciones
- Base de datos accesible en modo escritura.
- Entorno Qt operativo (`--ui pyside6`).
- Biblioteca con documentos de prueba.

## Checklist funcional
- [ ] La pestaña `Documentos` abre correctamente desde toolbar y panel lateral.
- [ ] La tabla carga documentos sin congelar la UI.
- [ ] Busqueda global filtra resultados correctamente.
- [ ] Ordenamiento por columnas funciona y se mantiene al refrescar.
- [ ] Abrir documento funciona para un registro valido.
- [ ] Abrir carpeta del documento funciona.
- [ ] Renombrar documento actualiza archivo y registro.
- [ ] Copiar documento funciona con validacion de destino existente.
- [ ] Mover documento funciona y elimina registro cuando corresponde.
- [ ] Enviar a papelera funciona y actualiza estado.
- [ ] Eliminar definitivo funciona con confirmacion.
- [ ] Menu contextual muestra acciones esperadas.
- [ ] Asociar a coleccion/grupo/categoria/etiqueta/palabra clave funciona.
- [ ] Desasociar de coleccion/grupo/categoria/etiqueta/palabra clave funciona.
- [ ] Operaciones por lote (copiar/mover/papelera/eliminar) funcionan.
- [ ] Cancelacion de lote detiene el procesamiento en curso.

## Checklist de estado/persistencia
- [ ] Se guarda busqueda actual al cerrar/reabrir.
- [ ] Se guarda columna de orden y direccion.
- [ ] Se guardan anchos de columnas.
- [ ] Se restaura documento seleccionado (si aun existe).
- [ ] Pestañas Qt restauran abiertas/cerradas, orden y activa.
- [ ] Ventana Qt restaura geometria y estado de panel lateral.

## Checklist de errores y UX
- [ ] Acciones destructivas muestran confirmacion.
- [ ] Errores de archivo se muestran con mensaje claro.
- [ ] Errores de BD se muestran con mensaje claro.
- [ ] Durante lote, botones se bloquean y progreso se actualiza.
- [ ] Al finalizar lote, se refresca la tabla.

## Cierre
- [ ] Checklist completada sin bloqueantes.
- [ ] Incidencias documentadas y priorizadas.
- [ ] Fase 3 marcada como cerrada y Fase 4 iniciada.
