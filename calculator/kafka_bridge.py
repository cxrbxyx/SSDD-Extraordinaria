import json
import os

from kafka import KafkaConsumer, KafkaProducer
import Ice
import RemoteCalculator

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'
OPERACIONES_TOPIC = 'operaciones'
RESULTADOS_TOPIC = 'resultados'

slice_path = os.path.join(os.path.dirname(__file__), "remotecalculator.ice")
Ice.loadSlice(slice_path)

def validar_peticion(data):
    if not isinstance(data, dict):
        return False, "format error"
    if "id" not in data or not isinstance(data["id"], str):
        return False, "format error"
    if "operation" not in data or data["operation"] not in ("sum", "sub", "mult", "div"):
        return False, "operation not found"
    if "args" not in data or not isinstance(data["args"], dict):
        return False, "format error"
    if "op1" not in data["args"] or "op2" not in data["args"]:
        return False, "format error"
    try:
        float(data["args"]["op1"])
        float(data["args"]["op2"])
    except Exception:
        return False, "format error"
    return True, None

def main():
    consumer = KafkaConsumer(
        OPERACIONES_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: m.decode('utf-8'),
        auto_offset_reset='earliest',
        group_id='calculator-group'
    )
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda m: m.encode('utf-8')
    )

    with Ice.initialize() as communicator:
        proxy = communicator.stringToProxy("calculator:tcp -h localhost -p 10000")
        calculator = RemoteCalculator.CalculatorPrx.checkedCast(proxy)

        for msg in consumer:
            try:
                data = json.loads(msg.value)
            except Exception:
                continue

            id_ = data.get("id", None)
            valido, error = validar_peticion(data)
            respuesta = {"id": id_, "result": None}

            if not valido:
                respuesta["status"] = False
                respuesta["error"] = error
                producer.send(RESULTADOS_TOPIC, json.dumps(respuesta))
                continue

            op = data["operation"]
            op1 = float(data["args"]["op1"])
            op2 = float(data["args"]["op2"])

            try:
                if op == "sum":
                    result = calculator.sum(op1, op2)
                elif op == "sub":
                    result = calculator.sub(op1, op2)
                elif op == "mult":
                    result = calculator.mult(op1, op2)
                elif op == "div":
                    try:
                        result = calculator.div(op1, op2)
                    except RemoteCalculator.ZeroDivisionError:
                        respuesta["status"] = False
                        respuesta["error"] = "No se puede dividir entre 0"
                        producer.send(RESULTADOS_TOPIC, json.dumps(respuesta))
                        continue
                else:
                    raise Exception("operation not found")
                respuesta["status"] = True
                respuesta["result"] = result
                if "reason" in respuesta:
                    del respuesta["reason"]
            except Exception as e:
                respuesta["status"] = False
                respuesta["error"] = str(e)

            producer.send(RESULTADOS_TOPIC, json.dumps(respuesta))

if __name__ == "__main__":
    main()
