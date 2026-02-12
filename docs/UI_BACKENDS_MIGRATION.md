# Migracion de UI por Backend

## Objetivo
Permitir que la aplicacion use distintos frameworks visuales sin duplicar controladores ni logica de negocio.

## Estructura base
- `src/views/tk/app.py`: entrada del backend Tkinter.
- `src/views/qt/app.py`: entrada del backend Qt/PySide6.
- `src/views/tk/frames/`: frames especificos de Tkinter.
- `src/views/qt/frames/`: widgets/paginas especificas de Qt.
- `src/views/tk/dialogs/`: dialogos Tkinter.
- `src/views/qt/dialogs/`: dialogos Qt.
- `src/views/shared/`: contratos/adaptadores reutilizables entre backends.

## Regla de separacion
- `models/controllers/*` no debe importar widgets concretos.
- Las vistas (Tk o Qt) invocan controladores, no al reves.
- La seleccion del backend se hace solo en `src/main.py` + `src/views/apps/factory.py`.

## Fases sugeridas
1. Mantener Tkinter operativo usando `views/tk/app.py` (proxy temporal).
2. Mover gradualmente cada frame/dialog Tk a `views/tk/...`.
3. Crear equivalentes Qt en `views/qt/...` reutilizando los mismos controladores.
4. En cada migracion, conservar nombres de acciones/metodos para facilitar pruebas.
