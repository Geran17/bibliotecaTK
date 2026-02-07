# Funcionalidad de Importación CSV en BibliotecaTK

## Overview

Se han agregado dos nuevos botones en la sección **Administrar Contenidos** que permiten importar capítulos y secciones desde archivos CSV:

- **📥 Importar CSV** (en la sección de Capítulos)
- **📥 Importar CSV** (en la sección de Secciones)

## Archivos Modificados

### 1. **src/views/frames/frame_administrar_contenido.py**
   - Agregados imports: `messagebox` de ttkbootstrap, `filedialog` de tkinter, `ControlarImportacionCSV`
   - Agregados botones: `btn_importar_capitulos`, `btn_importar_secciones`
   - Agregados métodos: `importar_capitulos()`, `importar_secciones()`
   - Actualizado `map_widgets` para incluir los nuevos botones

### 2. **src/models/controllers/controlar_administrar_contenido.py**
   - Agregadas referencias a los botones de importación en el constructor
   - Agregados comandos para los botones: `.config(command=...)`
   - Agregados métodos delegadores: `on_importar_capitulos()`, `on_importar_secciones()`

### 3. **src/models/controllers/controlar_importacion_csv.py** (Nuevo)
   - Nuevo controlador para la lógica de importación
   - Métodos:
     - `importar_capitulos_csv()`: Importa capítulos desde CSV
     - `importar_secciones_csv()`: Importa secciones desde CSV
   - Validación robusta de datos
   - Manejo de errores y reportes detallados

### 4. **tests/controllers/test_controlar_importacion_csv.py** (Nuevo)
   - Tests unitarios para el controlador de importación
   - Cubre casos válidos e inválidos

### 5. **docs/IMPORTACION_CSV.md** (Nuevo)
   - Guía completa de uso con ejemplos
   - Solución de problemas

### 6. **docs/ejemplo_capitulos.csv** (Nuevo)
   - Archivo CSV de ejemplo para capítulos

### 7. **docs/ejemplo_secciones.csv** (Nuevo)
   - Archivo CSV de ejemplo para secciones

## Características Principales

### Validación de Datos
- ✅ Verifica que los campos requeridos no estén vacíos
- ✅ Convierte automáticamente tipos de datos (números)
- ✅ Detecta y reporta errores de tipo
- ✅ Valida que el archivo sea un CSV válido

### Manejo de Errores
- ✅ Mensajes claros sobre qué falló y en qué fila
- ✅ Importación parcial: continúa con las siguientes filas si hay errores
- ✅ Reporte final con número de registros importados y errores encontrados

### Interfaz de Usuario
- ✅ Diálogo de selección de archivo con filtro CSV
- ✅ Mensajes informativos con resultados
- ✅ Validación de precondiciones (documento/capítulo seleccionado)

## Flujo de Uso

### Para Importar Capítulos:
1. Ir a **Administrar Contenidos**
2. Seleccionar un documento de la lista
3. Hacer clic en **📥 Importar CSV** (sección Capítulos)
4. Seleccionar archivo CSV con capítulos
5. Revisar mensaje de resultado

### Para Importar Secciones:
1. Ir a **Administrar Contenidos**
2. Seleccionar un capítulo en el árbol
3. Hacer clic en **📥 Importar CSV** (sección Secciones)
4. Seleccionar archivo CSV con secciones
5. Revisar mensaje de resultado

## Formato de Archivos CSV

### Capítulos (capitulos.csv)
```csv
numero_capitulo,titulo,pagina_inicio
1,Introducción,1
2,Marco Teórico,15
3,Metodología,45
```

### Secciones (secciones.csv)
```csv
titulo,nivel,numero_pagina,id_padre
Antecedentes,1.1,15,
Estado del arte,1.2,20,
Planteamiento de hipótesis,2.1,45,
Variables independientes,2.1.1,46,Planteamiento de hipótesis
```

Para más detalles, consulta [IMPORTACION_CSV.md](IMPORTACION_CSV.md)

## Validación y Pruebas

Los tests están en `tests/controllers/test_controlar_importacion_csv.py` y cubren:
- ✅ Importación válida de capítulos y secciones
- ✅ Detección de campos faltantes
- ✅ Validación de tipos de datos
- ✅ Manejo de archivos inexistentes
- ✅ Limpieza de errores

Ejecutar pruebas:
```bash
pytest tests/controllers/test_controlar_importacion_csv.py -v
```

## Ejemplos de Archivos

En la carpeta `docs/` se encuentran:
- `ejemplo_capitulos.csv`: Ejemplo de capítulos listos para importar
- `ejemplo_secciones.csv`: Ejemplo de secciones listos para importar

Puedes usarlos como plantilla o punto de partida.

## Notas Técnicas

### Arquitectura
- Patrón **MVC**: La vista (`FrameAdministrarContenido`) abre diálogos y delega a controladores
- El controlador de dominio (`ControlarAdministrarContenido`) maneja eventos de UI
- El controlador de CSV (`ControlarImportacionCSV`) maneja la lógica de importación

### Dependencias
- `csv`: Módulo estándar de Python para lectura de CSV
- `pathlib.Path`: Para manipulación de rutas
- `logging`: Para registros de errores
- DAOs existentes: `CapituloDAO`, `SeccionDAO`

### Base de Datos
- Las inserciones respetan las claves foráneas
- Se usa context manager en los DAOs para garantizar la integridad transaccional
- Los IDs se generan automáticamente (AUTOINCREMENT)

## Mejoras Futuras

Posibles mejoras para versiones futuras:
- [ ] Importación asíncrona para archivos grandes
- [ ] Barra de progreso visual durante importación
- [ ] Modo "Dry Run" para validar sin importar
- [ ] Exportación de capítulos y secciones a CSV
- [ ] Actualización de registros existentes (no solo inserción)
- [ ] Validación de unicidad (evitar duplicados)
