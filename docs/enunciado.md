# Enunciado entrega extraordinaria del Laboratorio de Sistemas Distribuidos 24/25

El siguiente documento es el enunciado para la entrega de convocatoria extraordinaria
de la práctica de Sistemas Distribuidos del curso 2024/2025.

## Introducción

Se quiere implementar un servicio de cálculo remoto utilizando _remote method invocation_ usando **ZeroC Ice**.
Para el prototipo, únicamente se considerarán las operaciones aritméticas básicas.

Para garantizar un acceso regulado al servicio, se implementará además un mecanismo de serialización de
operaciones a través de canales de eventos implementados como _topics_ de **Apache Kafka**.

## Requisitos

### Servicio de calculadora

El servicio de calculadora permitirá realizar las operaciones de suma, resta, multiplicación y división, conforme
a lo especificado en la interfaz. Siempre se realizarán las operaciones sobre números reales (punto flotante).

### Serialización de operaciones

Se desarrollará un programa que sea capaz de recibir peticiones de operación a través de un _topic_ de Kafka. Dicho
programa se encargará de:

1. Deserializar la petición recibida conforme al formato especificado más adelante.
2. Si el formato **no es correcto**, se enviará una respuesta de error al _topic_ de respuestas. En ningún caso, un
   mensaje en formato desconocido debe provocar la interrupción de la ejecución del programa.
3. Si el formato **es correcto**, se enviará una petición al servicio de calculadora, devolviendo el resultado
    a través del _topic_ de respuestas.

El formato esperado para las peticiones serializadas consistirá en cadenas de caracteres con sintáxis JSON que
representarán el objeto _Peticion_, el cual tendrá los siguientes campos, todos ellos _obligatorios_ y nunca nulos:
- _id_: identificador único de petición. La respuesta asociada con esta operación tendrá el mismo _id_.
- _operation_: nombre de la operación que se quiere invocar en el servicio de calculadora.
- _operands_: lista de operandos que se deben pasar a la operación.

Una vez enviada la petición correspondiente al servicio de calculadora, en caso de poder ejecutarse la operación,
el programa recibirá un resultado que deberá serializar y enviar al _topic_ correspondiente. El formato de las respuestas
también consistirá en cadenas JSON resultantes de serializar objetos _Respuesta_, que son objetos con los siguientes
parámetros:
- _id_: obligatorio. Contiene el identificador único asociado al objeto _Peticion_.
- _result_: obligatorio aunque puede valer nulo (_null_ en notación JSON). Contendrá el resultado (si lo hubiera,
  si no, _null_) de la operación.
- _reason_: opcional. En caso de error (cuando _result_ sea nulo), el mensaje de error provocado por la petición.

### Formato de mensajes

#### Formato de mensaje de petición de operación

El programa consumirá mensajes de un _topic_ de Kafka donde llegarán las peticiones de operación, que cumplirán con
el formato siguiente:

- El mensaje será un objeto [JSON][1].
- El mensaje contendrá las siguientes claves de manera obligatoria:
    - "id": un "string" que especificará una identificación para la operación, para poderla correlacionar con
        el mensaje de respuesta.
    - "operation": un "string" dentro del siguiente enumerado: "sum", "sub", "mult", "div".
    - "args": será un "object" que contendrá las claves "op1" y "op2", ambas contendrán un valor "float".

Ejemplo de mensaje:

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

Cualquier mensaje que no cumpla éste formato, será rechazado. Si el formato es incorrecto, pero al menos tiene el
valor "id" definido correctamente, se utilizará para enviar un mensaje de respuesta con el error correspondiente
(_format error_).

#### Formato de mensaje de resultado de operación

Una vez procesada cada operación recibida a través del servicio remoto implementado en Ice, el programa enviará el
resultado a un _topic_ Kafka, con el siguiente formato:

- El mensaje será un objeto [JSON][1].
- Em mensaje contendrá las siguientes claves de manera obligatoria:
    - "id": un "string" que coincidirá con el identificador de la opeoración cuando se recibió.
    - "status": un valor booleano. "true" indicará que la operación se ha realizado correctamente, "false" que ha
        ocurrido algún error.
    - "result": un valor numérico con el resultado de la operación. En caso de error, puede no estar presente, al
        no existir resultado.
    - "error": un "string" con el error que ha sucedido. Puede no estar presente en caso de haber funcionado
        correctamente todo.

Ejemplos de mensaje de respuesta:

```json
{
    "id": "op1",
    "status": true,
    "result": 15.4
}
```

```json
{
    "id": "op2",
    "status": false,
    "error": "operation not found"
}
```

## Entregable

La práctica se deberá realizar y almacenar en un repositorio de Git privado. La entega consistirá en enviar
la URL a dicho repositorio, por lo que el alumno deberá asegurarse de que los profesores tengan acceso a
dicho repositorio. Si la práctica está en alguna rama diferente de la principal, también se debe indicar en la entrega.

El repositorio deberá contener al menos lo siguiente:

- `README.md` con una explicación mínima de cómo configurar y ejecutar el servicio, así como sus dependencias
    si las hubiera.

- El fichero o ficheros de configuración necesarios para la ejecución.
- Algún sistema de control de dependencias de Python: fichero `pyproject.toml`, `setup.cfg`, `setup.py`, Pipenv,
    Poetry, `requirements.txt`... Su uso debe estar también explicado en el fichero `README.md`
- Implementación del servicio de calculadora utilizando ZeroC Ice para crear la interfaz de invocación remota.
- El de-serializador de operaciones que las reenvíe al servicio de calculadora y serialice las respuestas.

### Fecha de entrega

## Repositorio plantilla

En CampusVirtual se compartirá un repositorio plantilla en GitHub que los alumnos podrán utilizar para crear
su propio repositorio o para clonarlo y comenzar uno nuevo desde "cero".

Dicho repositorio plantilla contiene todos los requisitos especificados en la sección anterior:

- Fichero `README.md`
- Fichero `pyproject.toml` con la configuración del proyecto y de algunas herramientas de evaluación de código.
- El fichero Slice.
- Un paquete Python llamado `calculator` con la utilería necesaria para cargar el Slice.
- Módulos dentro de dicho paquete para la implementación de la interfaz Slice del servicio.
- Módulo `server.py` con la implementación de una `Ice.Application` que permite la ejecución del servicio y añadir
    el objeto factoría existente (en la plantilla, sin implementar sus métodos).
- Módulo `command_handlers.py` con el manejador del comando principal (el equivalente a la función `main`).
- Fichero de configuración necesario para ejecutar el servicio.
- Directorio `.github/workflows` con la definición de algunas "Actions" de la integración continua de GitHub que
    realizan un análisis estático de tipos y de la calidad del código.

Se recomienda encarecidamente utilizar dicha plantilla y leer bien el `README.md` para entender el funcionamiento,
aunque no es obligatorio su uso.

[1]: https://es.wikipedia.org/wiki/JSON