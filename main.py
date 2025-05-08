from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Cargar el CSV
df = pd.read_csv("productos.csv", sep="\t")

# Función para buscar productos
def buscar_producto(nombre_busqueda, top_n=3):
    nombre_busqueda = nombre_busqueda.lower()
    df['match_score'] = df['title'].str.lower().apply(
        lambda x: sum(1 for palabra in nombre_busqueda.split() if palabra in x)
    )
    resultados = df[df['match_score'] > 0].sort_values(by='match_score', ascending=False).head(top_n)
    if resultados.empty:
        return "😕 Lo siento, no encontré productos con esas características."

    respuesta = "🛒 Tenemos estas opciones:\n\n"
    for i, row in enumerate(resultados.itertuples(), 1):
        respuesta += f"{i}. {row.title}\n💰 Precio: L{row.price:.2f}\n🔗 {row.link}\n\n"
    return respuesta

# Ruta de la API
@app.route("/buscar-producto", methods=["POST"])
def api_buscar():
    data = request.json
    print("📩 Mensaje recibido:", data)
    pregunta = data.get("pregunta", "")
    respuesta = buscar_producto(pregunta)
    return jsonify({"respuesta": respuesta})

# Iniciar la app (Render usará esta parte)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

