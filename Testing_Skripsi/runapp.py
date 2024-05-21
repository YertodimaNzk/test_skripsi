from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulasi database penyakit
penyakit_data = {
    "anemia": {
        "pengertian": "Anemia adalah kondisi di mana Anda tidak memiliki cukup sel darah merah yang sehat untuk membawa oksigen yang cukup ke jaringan tubuh Anda.",
        "penanganan": "Penanganan anemia melibatkan peningkatan asupan zat besi, vitamin B12, dan folat.",
        "obat": "Beberapa obat yang digunakan termasuk suplemen zat besi dan vitamin B12."
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result')
def result():
    query = request.args.get('query')
    result = penyakit_data.get(query.lower(), None)
    return render_template('result.html', query=query, result=result)

@app.route('/search', methods=['POST'])
def search():
    query = request.json.get('query')
    result = penyakit_data.get(query.lower(), None)
    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Penyakit tidak ditemukan"}), 404

if __name__ == '__main__':
    app.run(debug=True)
