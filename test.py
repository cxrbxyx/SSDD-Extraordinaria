"""Script de pruebas para el sistema de calculadora distribuida usando Kafka."""

import json
from kafka import KafkaProducer, KafkaConsumer

KAFKA_BROKER = 'localhost:9092'
REQUEST_TOPIC = 'operaciones'
RESPONSE_TOPIC = 'resultados'

pruebas = [
    # Suma válida
    {"id": "t1", "operation": "sum", "args": {"op1": 1, "op2": 2}},
    # Resta válida
    {"id": "t2", "operation": "sub", "args": {"op1": 5, "op2": 3}},
    # Multiplicación válida
    {"id": "t3", "operation": "mult", "args": {"op1": 2, "op2": 4}},
    # División válida
    {"id": "t4", "operation": "div", "args": {"op1": 10, "op2": 2}},
    # División por cero
    {"id": "t5", "operation": "div", "args": {"op1": 10, "op2": 0}},
    # Operación inválida
    {"id": "t6", "operation": "foo", "args": {"op1": 1, "op2": 2}},
    # Mensaje mal formado (falta operation)
    {"id": "t7", "args": {"op1": 1, "op2": 2}},
    # Mensaje mal formado (falta args)
    {"id": "t8", "operation": "sum"},
    # Mensaje mal formado (falta id)
    {"operation": "sum", "args": {"op1": 1, "op2": 2}},
]

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

for request in pruebas:
    producer.send(REQUEST_TOPIC, request)
    producer.flush()
    print(f"Mensaje enviado: {request}")

consumer = KafkaConsumer(
    RESPONSE_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='test-consumer-group'
)

ids_esperados = {req["id"] for req in pruebas if "id" in req}
recibidos = set()
print("Esperando respuestas...")
for msg in consumer:
    if msg.value.get("id") in ids_esperados:
        print("Respuesta recibida:", msg.value)
        recibidos.add(msg.value.get("id"))
        if recibidos == ids_esperados:
            break

consumer.close()
