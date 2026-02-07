# 🚀 INICIO RÁPIDO - Importación CSV

> **Tu guía de 5 minutos para importar capítulos y secciones**

## ⏱️ 5 Minutos para Comenzar

### 1️⃣ Prepara tu archivo CSV (2 min)

**Para Capítulos**, crea un archivo `capitulos.csv`:
```csv
numero_capitulo,titulo,pagina_inicio
1,Introducción,1
2,Marco Teórico,15
3,Metodología,45
```

**Para Secciones**, crea un archivo `secciones.csv`:
```csv
titulo,nivel,numero_pagina,id_padre
Antecedentes,1.1,15,
Estado del arte,1.2,20,
```

### 2️⃣ Abre BibliotecaTK (1 min)

```bash
python src/main.py
```

### 3️⃣ Importa Capítulos (1 min)

1. Ve a **Administrar Contenidos**
2. Selecciona un documento
3. Haz clic en **📥 Importar CSV** (sección Capítulos)
4. Selecciona tu archivo CSV
5. ¡Listo! 🎉

### 4️⃣ Importa Secciones (1 min)

1. Selecciona un capítulo en el árbol
2. Haz clic en **📥 Importar CSV** (sección Secciones)
3. Selecciona tu archivo CSV
4. ¡Listo! 🎉

---

## 📥 Usar Archivos de Ejemplo

Si prefieres no crear archivos, usa los ejemplos:

```bash
# Los archivos están en docs/
docs/ejemplo_capitulos.csv
docs/ejemplo_secciones.csv
```

Cópialos y adáptalos a tus necesidades.

---

## ✅ Checklist de Verificación

- [ ] Archivo CSV creado correctamente
- [ ] CSV está codificado en UTF-8
- [ ] Columnas tienen los nombres exactos
- [ ] No hay espacios extras en headers
- [ ] BibliotecaTK abierto
- [ ] Documento/Capítulo seleccionado
- [ ] Botón "📥 Importar CSV" visible
- [ ] Importación completada exitosamente

---

## 🆘 Si Algo Falla

### Error: "El archivo no existe"
→ Verifica la ruta del archivo

### Error: "Debe seleccionar un documento"
→ Haz clic en un documento de la lista

### Error: "numero_capitulo está vacío"
→ Revisa que ninguna celda esté vacía en el CSV

### Error: "número entero esperado"
→ Asegúrate de que `numero_capitulo` sean números (1, 2, 3...)

**Más ayuda**: Ver [docs/IMPORTACION_CSV.md#solución-de-problemas](docs/IMPORTACION_CSV.md#solución-de-problemas)

---

## 📊 Estructura CSV Mínima

### Capítulos (obligatorio)
```
numero_capitulo,titulo
1,Mi Capítulo
```

### Secciones (obligatorio)
```
titulo
Mi Sección
```

---

## 🎯 Próximos Pasos

1. **Conocer el formato**: [docs/IMPORTACION_CSV.md](docs/IMPORTACION_CSV.md)
2. **Entender la arquitectura**: [RESUMEN_VISUAL.txt](RESUMEN_VISUAL.txt)
3. **Ejecutar tests**: `pytest tests/controllers/test_controlar_importacion_csv.py -v`
4. **Ver cambios**: [CHANGELOG.md](CHANGELOG.md)

---

## 💡 Tips Útiles

- 💾 Guarda siempre una copia de seguridad
- 📝 Usa un editor que soporte UTF-8 (VS Code, Notepad++)
- 🔍 Valida tu CSV en [csvlint.io](https://csvlint.io/)
- 📊 Excel puede exportar a CSV (Guardar Como > CSV)
- 🔗 Para secciones padre, usa el título exacto

---

## 📚 Documentación Rápida

| Necesito... | Leo... |
|------------|--------|
| Empezar rápido | Este archivo |
| Guía detallada | [docs/IMPORTACION_CSV.md](docs/IMPORTACION_CSV.md) |
| Resolver problemas | [TESTING_GUIDE.md](TESTING_GUIDE.md) |
| Entender el código | [IMPORTACION_CSV.md](IMPORTACION_CSV.md) |
| Ver todo | [INDICE.md](INDICE.md) |

---

## 🎓 Ejemplo Práctico Completo

### Paso 1: Crear capitulos.csv
```csv
numero_capitulo,titulo,pagina_inicio
1,Introducción,1
2,Desarrollo,20
3,Conclusiones,50
```

### Paso 2: Crear secciones.csv
```csv
titulo,nivel,numero_pagina,id_padre
Antecedentes,1.1,1,
Marco teórico,1.2,5,
Metodología,2.1,20,
Recolección de datos,2.1.1,21,Metodología
Análisis,2.2,30,
```

### Paso 3: En BibliotecaTK
1. Documento → Seleccionar
2. 📥 Importar CSV (Capítulos) → capitulos.csv
3. Capítulo → Seleccionar uno en árbol
4. 📥 Importar CSV (Secciones) → secciones.csv

### Paso 4: Verificar
¡Tus datos están importados en la BD! ✅

---

## 🔒 Validaciones Automáticas

El sistema verifica automáticamente:
- ✅ Archivo es CSV válido
- ✅ Columnas requeridas presentes
- ✅ Tipos de datos correctos
- ✅ Campos requeridos no vacíos
- ✅ Referencias a secciones padre existen

---

## 📞 Ayuda Rápida

**¿Dónde están los ejemplos?**  
→ En `docs/` (ejemplo_capitulos.csv, ejemplo_secciones.csv)

**¿Cómo hago un CSV en Excel?**  
→ Abre Excel → Crea tabla → Guardar Como → Formato CSV UTF-8

**¿Qué pasa si me equivoco?**  
→ Los errores se reportan sin dañar los datos válidos

**¿Puedo importar miles de registros?**  
→ Sí, el sistema está optimizado para importación masiva

---

**¡Estás listo! Comienza a importar. 📥**

**Versión**: 1.1.0  
**Fecha**: 24 de Diciembre de 2025  
**Tiempo de lectura**: 5 minutos ⏱️
