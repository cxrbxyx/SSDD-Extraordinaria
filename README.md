## Instalación

Para instalar el paquete localmente, ejecuta:

```
pip install .
```

O, si quieres modificarlo durante el desarrollo:

```
pip install -e .
```

## Ejecución

### 1. Ejecutar el servidor de la calculadora (ZeroC Ice)

En una terminal, ejecuta:

```
ssdd-calculator --Ice.Config=config/calculator.config
```

Esto inicia el servidor remoto de la calculadora en el puerto 10000.

### 2. Ejecutar el bridge Kafka <-> Ice

En otra terminal, ejecuta:

```
ssdd-kafka-bridge
```

Esto lanzará el proceso que consume del topic `operaciones`, llama a la calculadora y produce en `resultados`.

### 3. Probar el sistema

Puedes probar el sistema ejecutando el script de pruebas:

```
python3 test.py
```

Esto enviará varias peticiones de ejemplo al topic `operaciones` y mostrará las respuestas recibidas en `resultados`.

## Configuración

Este proyecto solo permite configurar el endpoint del servidor. Para ello, debes modificar
el archivo `config/calculator.config` y cambiar la línea existente.

Por ejemplo, si quieres que tu servidor escuche siempre en el mismo puerto TCP, tu archivo
debería quedar así:

```
calculator.Endpoints=tcp -p 10000
```

## Uso del Slice

El archivo Slice se encuentra dentro del directorio `calculator`. Solo se carga una vez cuando el paquete
`calculator` es importado por Python. Esto facilita el desarrollo, ya que no necesitas cargar el Slice en cada módulo
o submódulo que definas.

El código que carga el Slice está en el archivo `__init__.py`.

## Ejemplo de petición

```json
{
    "id": "op1",
    "operation": "sum",
    "args": {
        "op1": 5.0,
        "op2": 10.4
    }
}
```

## Ejemplo de respuesta

```json
{
    "id": "op1",
    "status": true,
    "result": 15.4
}
```

## Ejemplo de respuesta de error

```json
{
    "id": "op2",
    "status": false,
    "error": "No se puede dividir entre 0"
}
```
