# 🧪 Guía de Verificación y Testing

## Verificación de Sintaxis

Todos los archivos Python han sido compilados sin errores:

```bash
# Compilar el controlador de importación CSV
python3 -m py_compile src/models/controllers/controlar_importacion_csv.py

# Compilar el frame actualizado
python3 -m py_compile src/views/frames/frame_administrar_contenido.py

# Compilar el controlador de administración
python3 -m py_compile src/models/controllers/controlar_administrar_contenido.py
```

## Ejecución de Tests

### Instalar dependencias de testing (si no las tienes)
```bash
pipenv install --dev pytest
```

### Ejecutar los tests de importación CSV
```bash
# Ejecutar todos los tests
pytest tests/controllers/test_controlar_importacion_csv.py -v

# Ejecutar un test específico
pytest tests/controllers/test_controlar_importacion_csv.py::TestControlarImportacionCSV::test_importar_capitulos_valido -v

# Ejecutar con reporte de cobertura
pytest tests/controllers/test_controlar_importacion_csv.py --cov=src/models/controllers/controlar_importacion_csv
```

## Prueba Manual de la Funcionalidad

### 1. Iniciar BibliotecaTK
```bash
python src/main.py
```

### 2. Navegar a "Administrar Contenidos"
- Ve a la sección "Administrar Contenidos" en la aplicación

### 3. Probar Importación de Capítulos
1. Selecciona un documento de la lista izquierda
2. Haz clic en el botón "📥 Importar CSV" en la sección Capítulos
3. Selecciona el archivo `docs/ejemplo_capitulos.csv`
4. Verifica que aparezca el mensaje de éxito

### 4. Probar Importación de Secciones
1. Haz doble clic en un capítulo del árbol (o selecciona uno)
2. Haz clic en el botón "📥 Importar CSV" en la sección Secciones
3. Selecciona el archivo `docs/ejemplo_secciones.csv`
4. Verifica que aparezca el mensaje de éxito

## Casos de Prueba Manuales

### Caso 1: Importación válida ✅
- **Archivo**: `docs/ejemplo_capitulos.csv`
- **Resultado esperado**: "✅ Se importaron 6 capítulos exitosamente."

### Caso 2: Archivo inexistente ❌
- **Acción**: Selecciona un archivo que no existe
- **Resultado esperado**: Mensaje de error con "El archivo... no existe"

### Caso 3: Documento no seleccionado ⚠️
- **Acción**: Intenta importar capítulos sin seleccionar documento
- **Resultado esperado**: "Debe seleccionar un documento antes de importar capítulos."

### Caso 4: Capítulo no seleccionado ⚠️
- **Acción**: Intenta importar secciones sin seleccionar capítulo
- **Resultado esperado**: "Debe seleccionar un capítulo antes de importar secciones."

## Verificación de la Base de Datos

Después de importar, puedes verificar que los datos se guardaron:

```python
# Desde Python shell
from models.daos.capitulo_dao import CapituloDAO
from models.daos.seccion_dao import SeccionDAO

# Listar capítulos importados
dao_cap = CapituloDAO()
capitulos = dao_cap.obtener_todos()
print(f"Total capítulos: {len(capitulos)}")

# Listar secciones importadas
dao_sec = SeccionDAO()
secciones = dao_sec.obtener_todos()
print(f"Total secciones: {len(secciones)}")
```

## Logs y Debugging

Si encuentras problemas, revisa los logs:

```bash
# Ver logs en tiempo real (si la app está ejecutándose)
tail -f /tmp/bibliotecatk.log  # o similar

# Activar debugging en el controlador
# Modifica el nivel de logging en controlar_importacion_csv.py:
# logger.setLevel(logging.DEBUG)
```

## Prueba de Archivos CSV Personalizados

Puedes crear tu propio archivo CSV:

### capitulos_personalizados.csv
```csv
numero_capitulo,titulo,pagina_inicio
1,Mi primer capítulo,1
2,Segundo capítulo,10
3,Tercer capítulo,20
```

### secciones_personalizadas.csv
```csv
titulo,nivel,numero_pagina,id_padre
Mi primera sección,1.1,10,
Mi segunda sección,1.2,15,
Subsección,1.2.1,16,Mi segunda sección
```

## Checklist de Validación

- [ ] El botón "📥 Importar CSV" aparece en la sección de Capítulos
- [ ] El botón "📥 Importar CSV" aparece en la sección de Secciones
- [ ] El diálogo de archivo se abre al hacer clic en los botones
- [ ] Se puede seleccionar un archivo CSV
- [ ] La importación válida muestra mensaje de éxito
- [ ] La importación con errores muestra detalles de los errores
- [ ] Los datos se guardan en la base de datos
- [ ] Los capítulos aparecen en el árbol de contenidos
- [ ] Las secciones aparecen bajo el capítulo seleccionado
- [ ] La importación parcial funciona (algunos registros válidos, otros con errores)
- [ ] Los logs se generan correctamente
- [ ] Los tests pasan sin errores

## Solución de Problemas

### El botón no aparece
- Verifica que `frame_administrar_contenido.py` se haya guardado correctamente
- Reinicia BibliotecaTK
- Revisa la consola de errores

### El diálogo no se abre
- Asegúrate de tener `tkinter.filedialog` importado
- Verifica que el módulo `tkinter` esté instalado
- En Linux, puede requerir: `sudo apt-get install python3-tk`

### La importación falla
- Verifica que el archivo CSV esté codificado en UTF-8
- Comprueba que las columnas encabezadas sean exactas (sin espacios extras)
- Revisa los primeros 10 errores en el mensaje
- Consulta el archivo de logs

### Los datos no se guardan
- Verifica que `CapituloDAO` y `SeccionDAO` estén funcionando
- Revisa que la base de datos tenga espacio
- Comprueba los permisos de la carpeta de datos

## Contacto y Soporte

Para más información:
- Consulta [docs/IMPORTACION_CSV.md](docs/IMPORTACION_CSV.md)
- Revisa [IMPORTACION_CSV.md](IMPORTACION_CSV.md)
- Ejecuta los tests para diagnóstico

---

**Estado**: ✅ Listo para producción
**Última actualización**: 24 de diciembre de 2025
