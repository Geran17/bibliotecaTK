# 🚀 BibliotecaTK - Ejecutable Compilado

## ¿Qué es esto?

BibliotecaTK v1.1.0 ha sido compilado en un **único archivo ejecutable** usando PyInstaller. No necesitas instalar Python ni dependencias - ¡simplemente ejecuta!

## 📦 Archivo Ejecutable

- **Nombre**: `BibliotecaTK`
- **Tamaño**: ~47 MB
- **Tipo**: ELF 64-bit executable (Linux)
- **Ubicación**: Raíz del proyecto

## 🚀 Cómo Ejecutar

### Opción 1: Script bash (Recomendado)
```bash
./run.sh
```

### Opción 2: Ejecutable directo
```bash
./BibliotecaTK
```

### Opción 3: Desde cualquier lugar
```bash
/ruta/absoluta/a/BibliotecaTK
```

## 📋 Requisitos

- **Sistema Operativo**: Linux 64-bit
- **CPU**: x86-64 compatible
- **RAM**: Mínimo 512 MB (recomendado 2 GB+)
- **Espacio en disco**: ~100 MB

## ✨ Características Incluidas

✅ Importación de capítulos desde CSV  
✅ Importación de secciones desde CSV  
✅ Interfaz gráfica completa  
✅ Base de datos SQLite integrada  
✅ Gestión de documentos  
✅ Visor de metadatos  
✅ Y más...

## 📝 Ejemplos de Uso

### Ejecutar y esperar a que se abra
```bash
./run.sh &
```

### Ejecutar en segundo plano
```bash
nohup ./run.sh &
```

### Ver si está funcionando
```bash
ps aux | grep BibliotecaTK
```

## 🔧 Si Necesitas Recompilar

Si realizas cambios en el código y necesitas regenerar el ejecutable:

```bash
cd src
pipenv install  # Si agregaste nuevas dependencias
pipenv run pyinstaller bibliotecaTK.spec
cp dist/BibliotecaTK ..
```

## 📊 Información Técnica

- **Compilador**: PyInstaller 6.17.0
- **Python**: 3.12.3
- **Método**: One-file (todo en un ejecutable)
- **Compresión**: Sí (UPX habilitado)
- **Interfaz**: GUI (sin consola)

## 🐛 Solución de Problemas

### "Permiso denegado"
```bash
chmod +x BibliotecaTK
chmod +x run.sh
```

### "No se puede ejecutar"
Verifica que sea un ejecutable de 64 bits:
```bash
file BibliotecaTK
# Debería mostrar: ELF 64-bit LSB executable
```

### "Librerias faltantes"
En muy raras ocasiones, puede necesitar:
```bash
sudo apt-get install libxcb1 libxkbcommon0 libdbus-1-3
```

## 📚 Documentación

Para más información sobre las nuevas funcionalidades:
- [QUICKSTART.md](QUICKSTART.md) - Guía rápida (5 minutos)
- [docs/IMPORTACION_CSV.md](docs/IMPORTACION_CSV.md) - Guía de importación
- [INDICE.md](INDICE.md) - Índice completo

## ✅ Verificación

Para verificar que el ejecutable funciona correctamente:

1. Ejecuta: `./run.sh`
2. Espera a que se abra la ventana de BibliotecaTK
3. Navega a "Administrar Contenidos"
4. Prueba los botones "📥 Importar CSV"
5. ¡Listo!

## 📞 Soporte

Si encuentras problemas:
1. Verifica que tienes permisos de ejecución: `ls -l BibliotecaTK`
2. Intenta ejecutar directamente: `./BibliotecaTK`
3. Revisa la documentación en `docs/`

## 🎯 Próximos Pasos

1. **Probar la aplicación**: Ejecuta `./run.sh`
2. **Crear archivos CSV**: Usa los ejemplos en `docs/`
3. **Importar datos**: Usa los nuevos botones de importación
4. **Explorar funciones**: Revisa la documentación

---

**Versión**: 1.1.0  
**Fecha**: 24 de Diciembre de 2025  
**Estado**: ✅ Listo para usar
