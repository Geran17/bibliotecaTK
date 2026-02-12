# Guía de Microcopy UI

Esta guía define el estilo de texto para la interfaz de BibliotecaTK.

## Reglas generales

- Escribir en español claro y directo.
- Usar tildes y signos de apertura (`¿`, `¡`) cuando corresponda.
- Evitar mayúsculas innecesarias en títulos.
- Preferir frases cortas y accionables.
- Evitar emojis en mensajes de diálogo (`showinfo`, `showwarning`, `showerror`).

## Títulos y secciones

- Formato recomendado: oración con capitalización natural.
- Ejemplos:
  - `Configuración general`
  - `Documento seleccionado`
  - `Claves de metadatos`

## Botones

- Usar verbos en infinitivo o acción corta.
- Ejemplos:
  - `Abrir`, `Copiar`, `Mover`, `Eliminar`, `Acciones`
- Evitar variantes ambiguas como `Más` cuando el contexto no es obvio.

## Tooltips

- Explicar acción + contexto en una sola línea.
- Ejemplos:
  - `Abrir el documento seleccionado`
  - `Seleccionar una carpeta`
  - `Recargar resultados`

## Mensajes de confirmación

- Estructura recomendada:
  - Acción + alcance + pregunta final.
- Ejemplos:
  - `Se eliminará el registro de la base de datos. ¿Está seguro?`
  - `Se moverá a la papelera el siguiente archivo. ¿Está seguro?`

## Mensajes informativos y de error

- Terminar mensajes con punto.
- Mantener títulos consistentes:
  - `Error`
  - `Advertencia`
  - `Importación exitosa`
  - `Importación con errores`

## Nomenclatura interna

- Evitar typos en nombres públicos o parámetros.
- Usar nombres correctos y consistentes:
  - `documentos_seleccionados` (no `documetos_seleccionados`)
  - `administrar` (no `adminstrar`)

## Compatibilidad

- Si se corrige un nombre de módulo, mantener wrapper temporal para imports antiguos.
- Marcar wrappers con docstring de compatibilidad y usar el módulo correcto en código nuevo.
