from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route untuk halaman utama (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman result-page
@app.route('/result-page')
def resultpage():
    return render_template('result-page.html')

# Route untuk halaman login
@app.route('/login')
def login():
    return render_template('login.html')

# Route untuk melakukan pencarian penyakit
@app.route('/search', methods=['POST'])
def search_disease():
    if request.method == 'POST':
        disease_name = request.form['disease'].strip()

        # Cari penyakit berdasarkan nama (simulasi pencarian)
        result = searchDiseaseByName(disease_name)

        if result:
            response = {
                'status': 'success',
                'message': f'Penyakit ditemukan: {result["name"]}. Deskripsi: {result["description"]}'
            }
        else:
            response = {
                'status': 'error',
                'message': 'Penyakit tidak ditemukan.'
            }

        return jsonify(response)

# Data penyakit untuk simulasi pencarian
def searchDiseaseByName(query):
    diseases = [
        { 'name': 'Anemia', 'description': 'Anemia adalah kondisi kekurangan sel darah merah.' },
        { 'name': 'Flu', 'description': 'Flu adalah penyakit pernapasan yang disebabkan oleh virus.' },
        { 'name': 'Demam', 'description': 'Demam adalah kondisi kenaikan suhu tubuh di atas normal.' },
        { 'name': 'Hipertensi', 'description': 'Hipertensi atau tekanan darah tinggi adalah kondisi medis yang ditandai dengan tekanan darah tinggi.' }
    ]
    query = query.lower().strip()
    return next((disease for disease in diseases if disease['name'].lower() == query), None)

if __name__ == '__main__':
    app.run(debug=True)
