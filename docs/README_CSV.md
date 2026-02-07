# 📥 Funcionalidad de Importación CSV - BibliotecaTK

> **Importa capítulos y secciones masivamente desde archivos CSV**

## 🎯 ¿Qué es?

BibliotecaTK ahora permite importar **capítulos** y **secciones** de documentos directamente desde archivos CSV. Esta funcionalidad facilita la importación masiva de contenidos estructurados sin necesidad de ingresarlos manualmente uno a uno.

## ⚡ Inicio Rápido

### Para Importar Capítulos
1. Abre BibliotecaTK
2. Ve a **Administrar Contenidos**
3. Selecciona un documento
4. Haz clic en **📥 Importar CSV** (sección Capítulos)
5. Selecciona tu archivo CSV
6. ¡Listo! Los capítulos se importarán automáticamente

### Para Importar Secciones
1. Abre BibliotecaTK
2. Ve a **Administrar Contenidos**
3. Selecciona un capítulo en el árbol
4. Haz clic en **📥 Importar CSV** (sección Secciones)
5. Selecciona tu archivo CSV
6. ¡Listo! Las secciones se importarán automáticamente

## 📋 Formato de Archivos

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
Planteamiento,2.1,45,
Variables,2.1.1,46,Planteamiento
```

## 🔍 Validaciones

✅ Campos requeridos no vacíos  
✅ Tipos de datos correctos (números)  
✅ Formato CSV válido  
✅ Codificación UTF-8  
✅ Secciones padre existentes  

## 💾 Ejemplos Listos

En la carpeta `docs/` encontrarás:
- `ejemplo_capitulos.csv` - Archivo listo para importar (6 capítulos)
- `ejemplo_secciones.csv` - Archivo listo para importar (13 secciones)

Puedes usar estos como plantilla o punto de partida.

## 🚀 Funcionalidades Principales

- 📥 **Importación Masiva**: Importa múltiples registros en un clic
- ✔️ **Validación Automática**: Detecta y reporta errores
- 📊 **Importación Parcial**: Continúa aunque haya errores
- 🔗 **Secciones Jerárquicas**: Soporte para relaciones padre-hijo
- 📈 **Reporte Detallado**: Ve exactamente qué pasó
- 🎯 **Interfaz Intuitiva**: Botones claros y mensajes en español

## 📚 Documentación

| Documento | Para Quién |
|-----------|-----------|
| [docs/IMPORTACION_CSV.md](docs/IMPORTACION_CSV.md) | Usuarios finales |
| [IMPLEMENTACION_RESUMEN.md](IMPLEMENTACION_RESUMEN.md) | Desarrolladores |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | QA / Testers |
| [INDICE.md](INDICE.md) | Todos (índice completo) |

## ❓ Preguntas Frecuentes

**¿Qué pasó si hay errores?**  
La importación continúa con los registros válidos. Verás un mensaje con los primeros 10 errores.

**¿Cómo hago referencia a una sección padre?**  
Puedes usar el ID numérico o el título exacto de la sección padre.

**¿Qué codificación debe tener el CSV?**  
UTF-8 (recomendado para caracteres especiales).

**¿Puedo importar en orden desordenado?**  
Sí, el sistema ordena automáticamente por las claves foráneas.

## 🆘 Solución de Problemas

**El botón no aparece**  
→ Reinicia BibliotecaTK

**El archivo no se carga**  
→ Verifica que sea CSV con extensión `.csv`

**Los datos no se guardan**  
→ Revisa los permisos de la carpeta de datos

**Tengo errores de importación**  
→ Consulta el mensaje de error con los detalles por fila

Ver [Solución de Problemas Completa](docs/IMPORTACION_CSV.md#solución-de-problemas)

## 💻 Requisitos Técnicos

- Python 3.8+
- BibliotecaTK v1.1.0+
- Archivo CSV con codificación UTF-8

## 🧪 Testing

Ejecuta los tests para verificar que todo funciona:

```bash
pytest tests/controllers/test_controlar_importacion_csv.py -v
```

## 📖 Guía Completa

Para una guía detallada con ejemplos, casos de uso y solución de problemas:  
→ Ver [docs/IMPORTACION_CSV.md](docs/IMPORTACION_CSV.md)

## 🎓 Ejemplo Completo

### Paso 1: Crear tu CSV
```csv
numero_capitulo,titulo,pagina_inicio
1,Introducción,1
2,Desarrollo,20
3,Conclusiones,50
```

### Paso 2: Guardar el archivo
Guarda como `mis_capitulos.csv` con encoding UTF-8

### Paso 3: Importar en BibliotecaTK
1. Selecciona un documento
2. Haz clic en "📥 Importar CSV"
3. Selecciona `mis_capitulos.csv`
4. Recibirás un mensaje confirmando la importación

### Paso 4: Verificar
Los capítulos aparecerán en el árbol de contenidos

## 📞 Soporte

Para más información:
- 📚 Documentación: [Guía de Usuario](docs/IMPORTACION_CSV.md)
- 🔧 Técnico: [Documentación Técnica](IMPORTACION_CSV.md)
- ✅ Testing: [Guía de Testing](TESTING_GUIDE.md)
- 📋 Cambios: [Changelog](CHANGELOG.md)

## ✨ Características Implementadas

✅ Botón de importación de capítulos  
✅ Botón de importación de secciones  
✅ Validación robusta de datos  
✅ Manejo inteligente de errores  
✅ Interfaz amigable con diálogos  
✅ Mensajes en español  
✅ Logging completo  
✅ Tests unitarios  
✅ Documentación exhaustiva  
✅ Archivos de ejemplo  

## 🚀 Versión

**Versión**: 1.1.0  
**Fecha**: 24 de Diciembre de 2025  
**Estado**: ✅ Completado y documentado  

---

**¿Listo para importar tus contenidos? ¡Adelante! 📥**
