from flask import Flask, request, jsonify

app = Flask(__name__)

data_buffer = []   # donde guardamos temporalmente los datos (en memoria)

@app.route("/")
def home():
    return "Gateway ESP32 ONLINE"

@app.route("/data", methods=["POST"])
def receive_data():
    content = request.get_json()
    print("Dato recibido:", content)
    # validación mínima
    if not content or "id" not in content:
        return jsonify({"status":"error","reason":"payload inválido"}), 400
    data_buffer.append(content)
    # mantenemos solo los últimos 200 registros para no crecer indefinidamente
    if len(data_buffer) > 200:
        data_buffer.pop(0)
    return jsonify({"status": "ok", "received": content})

@app.route("/datos", methods=["GET"])
def send_data():
    # devuelve los datos almacenados
    return jsonify(data_buffer)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
