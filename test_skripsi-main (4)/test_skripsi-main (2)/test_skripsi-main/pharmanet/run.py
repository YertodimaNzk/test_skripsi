from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="pharmadia"
)

# Route untuk halaman utama (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman result-page
@app.route('/result-page')
def resultpage():
    return render_template('result-page.html')

# Route untuk halaman about us for user
@app.route('/aboutUsForUser')
def aboutUsForUser():
    return render_template('aboutUs.html')

# Route untuk halaman feedback
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Route untuk halaman login
@app.route('/login')
def login():
    return render_template('login.html')

# Route untuk halaman admin
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Route untuk halaman admin authorization
@app.route('/authorization')
def adminAuthorization():
    return render_template('data_admin/adminAuthorization.html')

# Route untuk halaman admin disease
@app.route('/disease')
def adminDisease():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM penyakit")
    penyakit_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminDisease.html', penyakit_data=penyakit_data)

# Route untuk halaman keyword
@app.route('/keyword')
def adminKeyword():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT keyword.id_penyakit, penyakit.penyakit_nama, keyword.keyword_nama 
        FROM keyword 
        JOIN penyakit ON keyword.id_penyakit = penyakit.id_penyakit
    """)
    keyword_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminKeyword.html', keyword_data=keyword_data)

# Route untuk halaman about us
@app.route('/aboutUs')
def adminAboutUs():
    return render_template('data_admin/adminAboutUs.html')

# Route untuk halaman slide fact
@app.route('/slideFact')
def adminSlideFact():
    return render_template('data_admin/adminSlideFact.html')

# Route untuk halaman keyword bank
@app.route('/keywordBank')
def adminKeywordBank():
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            keywordbank.keyword_id, 
            keywordbank.keyword_nama AS keyword_bank_nama, 
            keyword.keyword_nama AS keyword_nama
        FROM keywordbank 
        JOIN keyword ON keywordbank.keyword_id = keyword.keyword_id
    """
    cursor.execute(query)
    keyword_bank_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminKeywordBank.html', keyword_bank_data=keyword_bank_data)


# Route untuk halaman create disease dengan method POST untuk menyimpan data
@app.route('/createDisease', methods=['GET', 'POST'])
def adminCreateDisease():
    if request.method == 'POST':
        penyakit_nama = request.form['penyakit_nama']
        penyakit_penanganan = request.form['penyakit_penanganan']
        penyakit_obat = request.form['penyakit_obat']
        penyakit_deskripsi = request.form['penyakit_deskripsi']

        cursor = db.cursor()
        query = """
            INSERT INTO penyakit (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi))
        db.commit()
        cursor.close()

        return redirect(url_for('adminDisease'))
    
    return render_template('data_admin/createDisease.html')

# Route untuk halaman create keyword dengan method POST untuk menyimpan data
@app.route('/createKeyword', methods=['GET', 'POST'])
def adminCreateKeyword():
    if request.method == 'POST':
        id_penyakit = request.form['id_penyakit']
        keyword_nama = request.form['keyword_nama']

        cursor = db.cursor()
        query = """
            INSERT INTO keyword (id_penyakit, keyword_nama)
            VALUES (%s, %s)
        """
        cursor.execute(query, (id_penyakit, keyword_nama))
        db.commit()
        cursor.close()

        return redirect(url_for('adminKeyword'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id_penyakit, penyakit_nama FROM penyakit")
    penyakit_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/createKeyword.html', penyakit_data=penyakit_data)

# Route untuk halaman create keyword bank dengan method POST untuk menyimpan data
@app.route('/createKeywordBank', methods=['GET', 'POST'])
def adminCreateKeywordBank():
    if request.method == 'POST':
        keyword_nama = request.form['keyword_nama']

        cursor = db.cursor()
        query = """
            INSERT INTO keywordbank (keyword_nama)
            VALUES (%s)
        """
        cursor.execute(query, (keyword_nama,))
        db.commit()
        cursor.close()

        return redirect(url_for('adminKeywordBank'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT keyword_nama FROM keywordbank")
    keywordbank_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/createKeywordBank.html', keywordbank_data=keywordbank_data)


# Route untuk halaman create about us
@app.route('/createAboutUs')
def adminCreateAboutUs():
    return render_template('data_admin/createAboutUs.html')

# Route untuk halaman create slide fact
@app.route('/createSlideFact')
def adminCreateSlideFact():
    return render_template('data_admin/createSlideFact.html')

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
