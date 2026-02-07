# 📦 BibliotecaTK - Compilación a Ejecutable

## ✅ Estado: COMPILADO EXITOSAMENTE

El proyecto BibliotecaTK ha sido compilado exitosamente en un **archivo ejecutable único** utilizando PyInstaller.

## 📂 Ubicación del Ejecutable

```
dist/bibliotecaTK
```

**Tamaño:** 36 MB  
**Tipo:** ELF 64-bit LSB executable (Linux x86-64)  
**Plataforma:** Linux 3.2.0+

## 🚀 Formas de Ejecutar

### Opción 1: Usar el script de ejecución (Recomendado)
```bash
./ejecutar.sh
```

### Opción 2: Ejecutar directamente
```bash
./dist/bibliotecaTK
```

### Opción 3: Desde cualquier directorio
```bash
/ruta/completa/a/bibliotecaTK/dist/bibliotecaTK
```

## 📋 Especificaciones de la Compilación

- **Herramienta:** PyInstaller 6.17.0
- **Python:** 3.12.3
- **Tipo:** OnFile (Ejecutable único)
- **Modo de Ventana:** Sin consola (modo gráfico)

## 🔧 Configuración Utilizada

Se utilizó el archivo de configuración `src/bibliotecaTK.spec` con los siguientes parámetros:

- **Punto de entrada:** main.py
- **Dependencias incluidas:** ttkbootstrap, PIL, NumPy, y todas las librerías del proyecto
- **Hooks automáticos:** Configurados para ttkbootstrap y PIL
- **Optimización:** Nivel 0 (sin optimización, máximo debugging si es necesario)

## 📚 Dependencias Compiladas

El ejecutable incluye todas las dependencias necesarias:
- ✅ ttkbootstrap (interfaz gráfica)
- ✅ PyMuPDF (fitz) - procesamiento PDF
- ✅ pdf2image - miniaturas PDF
- ✅ send2trash - eliminación segura
- ✅ requests - solicitudes HTTP
- ✅ pyexiftool - metadatos
- ✅ PIL/Pillow - procesamiento de imágenes

## 🛠️ Cómo Recompilar

Si necesitas hacer cambios y recompilar:

```bash
# Desde el directorio del proyecto
cd /home/geran/MEGA/Workspaces/proyectos/bibliotecaTK

# Limpiar compilación anterior
rm -rf build/ dist/

# Recompilar
pipenv run pyinstaller src/bibliotecaTK.spec
```

## ⚠️ Notas Importantes

1. **Primer inicio:** Puede tardar un poco en iniciar la primera vez
2. **Base de datos:** Se crea automáticamente en `~/.local/share/bibliotecaTK/`
3. **Configuración:** Se almacena en `~/.config/bibliotecaTK/`
4. **Directorios XDG:** Respeta los estándares de directorios Linux

## 🐛 Problemas Conocidos Resueltos

- ✅ Desinstalado paquete obsoleto `pathlib` que causaba conflictos con PyInstaller
- ✅ Configurados los hooks automáticos para ttkbootstrap
- ✅ Incluidas las dependencias de PIL para Tkinter

## 📊 Tamaño del Ejecutable

- **Ejecutable compilado:** 36 MB
- **Razón:** Incluye todas las dependencias (Python, librerías, etc.) en un solo archivo

## 🔐 Distribución

El ejecutable puede distribuirse a usuarios sin Python instalado:

1. Copiar `dist/bibliotecaTK` a una ubicación accesible
2. El usuario puede ejecutarlo directamente: `./bibliotecaTK`
3. No requiere instalación de dependencias

---

**Compilado:** 23 de diciembre de 2025  
**Versión:** 0.1.0  
**Estado:** ✅ LISTO PARA USAR
