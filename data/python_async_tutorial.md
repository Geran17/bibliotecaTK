# Tutorial de Programación Asíncrona en Python

## ¿Qué es la Programación Asíncrona?

La programación asíncrona permite que tu programa ejecute múltiples tareas sin esperar a que cada una termine antes de comenzar la siguiente. Es especialmente útil para operaciones que tardan tiempo, como solicitudes web, lectura de archivos o consultas a bases de datos.

## Conceptos Clave

### 1. Coroutine (Corutina)
Una función definida con `async def` que puede pausarse y reanudarse.

### 2. `await`
Palabra clave que pausa la ejecución de una corutina hasta que se complete una operación asíncrona.

### 3. Event Loop
El motor que ejecuta y coordina las corutinas.

---

## Ejemplo 1: Primera Corutina Simple

```python
import asyncio

async def saludar():
    print("¡Hola!")
    await asyncio.sleep(1)  # Simula una operación que tarda 1 segundo
    print("¡Adiós!")

# Ejecutar la corutina
asyncio.run(saludar())
```

**Salida:**
```
¡Hola!
(espera 1 segundo)
¡Adiós!
```

---

## Ejemplo 2: Múltiples Tareas en Paralelo

```python
import asyncio

async def preparar_cafe():
    print("Preparando café...")
    await asyncio.sleep(2)
    print("☕ Café listo")
    return "Café"

async def tostar_pan():
    print("Tostando pan...")
    await asyncio.sleep(3)
    print("🍞 Pan listo")
    return "Pan"

async def cocinar_huevos():
    print("Cocinando huevos...")
    await asyncio.sleep(1)
    print("🍳 Huevos listos")
    return "Huevos"

async def preparar_desayuno():
    # Ejecutar todas las tareas al mismo tiempo
    resultados = await asyncio.gather(
        preparar_cafe(),
        tostar_pan(),
        cocinar_huevos()
    )
    print(f"\n¡Desayuno completo! {resultados}")

asyncio.run(preparar_desayuno())
```

**Salida:**
```
Preparando café...
Tostando pan...
Cocinando huevos...
🍳 Huevos listos
☕ Café listo
🍞 Pan listo

¡Desayuno completo! ['Café', 'Pan', 'Huevos']
```

**Tiempo total:** ~3 segundos (en lugar de 6 segundos si fuera secuencial)

---

## Ejemplo 3: Comparación Síncrono vs Asíncrono

### Versión Síncrona (Lenta)
```python
import time

def descargar_archivo(nombre, segundos):
    print(f"Descargando {nombre}...")
    time.sleep(segundos)
    print(f"✓ {nombre} descargado")

def main_sincrono():
    inicio = time.time()
    
    descargar_archivo("video.mp4", 3)
    descargar_archivo("imagen.jpg", 2)
    descargar_archivo("audio.mp3", 1)
    
    print(f"Tiempo total: {time.time() - inicio:.2f} segundos")

main_sincrono()
# Tiempo total: ~6 segundos
```

### Versión Asíncrona (Rápida)
```python
import asyncio

async def descargar_archivo_async(nombre, segundos):
    print(f"Descargando {nombre}...")
    await asyncio.sleep(segundos)
    print(f"✓ {nombre} descargado")

async def main_async():
    inicio = asyncio.get_event_loop().time()
    
    await asyncio.gather(
        descargar_archivo_async("video.mp4", 3),
        descargar_archivo_async("imagen.jpg", 2),
        descargar_archivo_async("audio.mp3", 1)
    )
    
    fin = asyncio.get_event_loop().time()
    print(f"Tiempo total: {fin - inicio:.2f} segundos")

asyncio.run(main_async())
# Tiempo total: ~3 segundos
```

---

## Ejemplo 4: Manejo de Excepciones

```python
import asyncio

async def tarea_con_error():
    await asyncio.sleep(1)
    raise ValueError("¡Algo salió mal!")

async def tarea_exitosa():
    await asyncio.sleep(2)
    return "Éxito"

async def main_con_errores():
    try:
        resultados = await asyncio.gather(
            tarea_con_error(),
            tarea_exitosa(),
            return_exceptions=True  # Captura excepciones sin detener otras tareas
        )
        
        for i, resultado in enumerate(resultados):
            if isinstance(resultado, Exception):
                print(f"Tarea {i} falló: {resultado}")
            else:
                print(f"Tarea {i} exitosa: {resultado}")
    
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main_con_errores())
```

---

## Ejemplo 5: Crear Tareas (Tasks)

```python
import asyncio

async def contar(nombre, n):
    for i in range(1, n + 1):
        print(f"{nombre}: {i}")
        await asyncio.sleep(1)

async def main_con_tasks():
    # Crear tareas que se ejecutan en segundo plano
    tarea1 = asyncio.create_task(contar("Tarea A", 3))
    tarea2 = asyncio.create_task(contar("Tarea B", 5))
    
    print("Tareas iniciadas...")
    
    # Esperar a que ambas terminen
    await tarea1
    await tarea2
    
    print("Todas las tareas completadas")

asyncio.run(main_con_tasks())
```

---

## Ejemplo 6: Uso Práctico con HTTP (aiohttp)

```python
import asyncio
import aiohttp

async def obtener_datos(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main_http():
    urls = [
        "https://api.github.com/users/python",
        "https://api.github.com/users/microsoft",
        "https://api.github.com/users/google"
    ]
    
    resultados = await asyncio.gather(*[obtener_datos(url) for url in urls])
    
    for resultado in resultados:
        print(f"Usuario: {resultado['login']}, Repos: {resultado['public_repos']}")

# asyncio.run(main_http())  # Requiere: pip install aiohttp
```

---

## Cuándo Usar Async

### ✅ Usa async cuando:
- Haces múltiples solicitudes HTTP
- Trabajas con bases de datos (con librerías async)
- Lees/escribes múltiples archivos
- Necesitas manejar muchas conexiones simultáneas

### ❌ No uses async cuando:
- Haces cálculos intensivos de CPU
- El código es simple y secuencial
- No hay operaciones de I/O (entrada/salida)

---

## Consejos Importantes

1. **Siempre usa `await`** dentro de funciones `async def`
2. **`asyncio.run()`** es el punto de entrada para código asíncrono
3. **`asyncio.gather()`** ejecuta múltiples corutinas en paralelo
4. **`asyncio.create_task()`** inicia una tarea en segundo plano
5. **`asyncio.sleep()`** en lugar de `time.sleep()` en código async

---

## Ejercicio Práctico

Intenta crear un script que simule el procesamiento de 5 pedidos en un restaurante, donde cada pedido tarda entre 1-3 segundos. Compara el tiempo entre hacerlo de forma síncrona vs asíncrona.

```python
import asyncio
import random

async def procesar_pedido(numero):
    tiempo = random.randint(1, 3)
    print(f"Pedido #{numero} iniciado (tardará {tiempo}s)")
    await asyncio.sleep(tiempo)
    print(f"Pedido #{numero} completado")
    return f"Pedido {numero}"

async def restaurante():
    pedidos = [procesar_pedido(i) for i in range(1, 6)]
    resultados = await asyncio.gather(*pedidos)
    print(f"\nTodos los pedidos listos: {resultados}")

asyncio.run(restaurante())
```

---

¡Ahora estás listo para empezar a usar programación asíncrona en Python! 🚀