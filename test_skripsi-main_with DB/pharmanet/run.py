from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# CORS settings
CORS(app)

# Konfigurasi koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="loladmit",
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

# Route untuk  halaman feedback
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Route untuk create feedback
@app.route('/feedback', methods=['POST'])
def createFeedback():
    feedbackInput = request.form['feedbackInput']
    cursor = db.cursor()
    query = """
        INSERT INTO masukan (masukan)
        VALUES (%s)
    """
    try:
        cursor.execute(query, [feedbackInput])
        db.commit()
        cursor.close()
        flash('Masukan berhasil ditambahkan', 'success')
        return redirect(url_for('feedback'))
    except Exception as e:
        flash('Gagal menambahkan masukan', 'danger')
        return redirect(url_for('feedback'))

# Route untuk halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Attempting login with username: {username}")

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM authorization WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            print(f"User found: {user['username']}")
            print(f"Stored password: {user['password']}")
            print(f"Entered password: {password}")
            if user['password'] == password:
                session['user_id'] = user['auth_id']
                session['username'] = user['username']
                return redirect(url_for('admin'))
            else:
                print("Password check failed")
                return render_template('login.html', error="Invalid username or password.")
        else:
            print("User not found")
            return render_template('login.html', error="Invalid username or password.")

    return render_template('login.html')

# Route untuk halaman admin
@app.route('/admin')
def admin():
    if 'user_id' in session:
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

# Route untuk halaman admin authorization
@app.route('/authorization')
def adminAuthorization():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM authorization")
    authorization_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminAuthorization.html', authorization_data=authorization_data)

# Route untuk halaman create authorization dengan method POST untuk menyimpan data
@app.route('/createAuthorization', methods=['GET', 'POST'])
def createAuthorization():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'];

        cursor = db.cursor()
        query = """
            INSERT INTO authorization (username, password)
            VALUES (%s, %s)
        """
        cursor.execute(query, (username, password))
        db.commit()
        cursor.close()

        return redirect(url_for('adminAuthorization'))
    
    return render_template('data_admin/createAuthorization.html')

# Route untuk menyimpan data autorisasi yang diperbarui ke database
@app.route('/updateAuthorization', methods=['POST'])
def updateAuthorization():
    if request.method == 'POST':
        data = request.get_json()
        auth_id = data['id']
        username = data['username']
        password = data['password']

        cursor = db.cursor()
        query = """
            UPDATE authorization
            SET username = %s, password = %s
            WHERE auth_id = %s
        """
        cursor.execute(query, (username, password, auth_id))
        db.commit()
        cursor.close()

        response = {'status': 'success', 'message': 'Data berhasil diperbarui.'}
        return jsonify(response)
    
# Route untuk menghapus data autorisasi
@app.route('/deleteAuthorization', methods=['POST'])
def deleteAuthorization():
    if request.method == 'POST':
        data = request.get_json()
        auth_id = data['id']

        cursor = db.cursor()
        query = """
            DELETE FROM authorization
            WHERE auth_id = %s
        """
        cursor.execute(query, (auth_id,))
        db.commit()
        cursor.close()

        response = {'status': 'success', 'message': 'Data berhasil dihapus.'}
        return jsonify(response)
    
# Route untuk halaman admin disease
@app.route('/disease')
def adminDisease():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM penyakit")
    penyakit_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminDisease.html', penyakit_data=penyakit_data)

# Route untuk halaman create disease dengan method POST untuk menyimpan data
# Route untuk halaman create disease dengan method POST untuk menyimpan data
@app.route('/createDisease', methods=['GET', 'POST'])
def adminCreateDisease():
    if request.method == 'POST':
        penyakit_nama = request.form['penyakit_nama']
        penyakit_penanganan = request.form['penyakit_penanganan']
        penyakit_obat = request.form['penyakit_obat']
        penyakit_deskripsi = request.form['penyakit_deskripsi']

        # Mengakses auth_id dari sesi yang telah diotentikasi
        auth_id = session.get('user_id')

        # Mengambil username dari tabel authorization
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT username FROM authorization WHERE auth_id = %s", (auth_id,))
        user = cursor.fetchone()
        cursor.close()

        # Pastikan user ditemukan dan username tidak kosong
        if user and 'username' in user:
            username = user['username']

            cursor = db.cursor()
            query = """
                INSERT INTO penyakit (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, created_by, updated_by, auth_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, username, username, auth_id))
            db.commit()
            cursor.close()

            return redirect(url_for('adminDisease'))
        else:
            return render_template('error.html', message="Failed to retrieve username from authorization table.")

    return render_template('data_admin/createDisease.html')

# Route untuk menyimpan data penyakit yang diperbarui ke database
@app.route('/updateDisease', methods=['POST'])
def updateDisease():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)

            penyakit_id = data['id']
            penyakit_nama = data['penyakit_nama']
            penyakit_penanganan = data['penyakit_penanganan']
            penyakit_obat = data['penyakit_obat']
            penyakit_deskripsi = data['penyakit_deskripsi']

            auth_id = session.get('user_id')

            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT username FROM authorization WHERE auth_id = %s", (auth_id,))
            user = cursor.fetchone()
            cursor.close()

            if user and 'username' in user:
                username = user['username']

                cursor = db.cursor()
                query = """
                    UPDATE penyakit
                    SET penyakit_nama = %s, penyakit_penanganan = %s, penyakit_obat = %s, penyakit_deskripsi = %s, 
                        created_at = NOW(), updated_by = %s, auth_id = %s
                    WHERE penyakit_id = %s
                """
                cursor.execute(query, (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, username, auth_id, penyakit_id))
                db.commit()
                cursor.close()

                response = {'status': 'success', 'message': 'Data berhasil diperbarui.'}
                return jsonify(response)
            else:
                response = {'status': 'error', 'message': 'Gagal memperbarui data: Username tidak ditemukan.'}
                return jsonify(response), 500

        except Exception as e:
            print("Error updating disease:", str(e))
            response = {'status': 'error', 'message': 'Gagal memperbarui data: ' + str(e)}
            return jsonify(response), 500

# Route untuk halaman keyword
@app.route('/keyword')
def adminKeyword():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT keyword.penyakit_id, penyakit.penyakit_nama, keyword.keyword_nama 
        FROM keyword 
        JOIN penyakit ON keyword.penyakit_id = penyakit.penyakit_id
    """)
    keyword_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminKeyword.html', keyword_data=keyword_data)

# Route untuk halaman create keyword dengan method POST untuk menyimpan data
@app.route('/createKeyword', methods=['GET', 'POST'])
def adminCreateKeyword():
    if request.method == 'POST':
        penyakit_id = request.form['penyakit_id']
        keyword_nama = request.form['keyword_nama']

        cursor = db.cursor()
        query = """
            INSERT INTO keyword (penyakit_id, keyword_nama)
            VALUES (%s, %s)
        """
        cursor.execute(query, (penyakit_id, keyword_nama))
        db.commit()
        cursor.close()

        return redirect(url_for('adminKeyword'))

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT penyakit_id, penyakit_nama FROM penyakit")
    penyakit_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/createKeyword.html', penyakit_data=penyakit_data)

# Route untuk menyimpan data kata kunci yang diperbarui ke database
@app.route('/updateKeyword', methods=['POST'])
def updateKeyword():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print("Received data:", data)

            keyword_id = data['id']
            keyword_nama = data['keyword_nama']

            cursor = db.cursor()
            query = """
                    UPDATE keyword
                    SET keyword_nama = %s
                    WHERE keyword_id = %s
                """
            cursor.execute(query, (keyword_nama, keyword_id))
            db.commit()
            cursor.close()

            response = {'status': 'success', 'message': 'Data berhasil diperbarui.'}
            return jsonify(response)

        except Exception as e:
            print("Error updating disease:", str(e)) 
            response = {'status': 'error', 'message': 'Gagal memperbarui data: ' + str(e)}
            return jsonify(response), 500

@app.route('/deleteKeyword', methods=['POST'])
def deleteKeyword():
    if request.method == 'POST':
        try:
            data = request.get_json()
            keyword_id = data['id']
            print("Received keyword_id:", keyword_id) 

            cursor = db.cursor()
            query = "DELETE FROM keyword WHERE keyword_id = %s"
            cursor.execute(query, (keyword_id,))
            db.commit()
            cursor.close()

            response = {'status': 'success', 'message': 'Kata kunci berhasil dihapus.'}
            return jsonify(response)
        except Exception as e:
            print("Error deleting keyword:", str(e))
            response = {'status': 'error', 'message': 'Gagal menghapus data: ' + str(e)}
            return jsonify(response), 500

# Route untuk halaman slide fact
@app.route('/slideFact')
def adminSlideFact():
    return render_template('data_admin/adminSlideFact.html')

# Route untuk halaman keyword bank
@app.route('/keywordBank')
def adminKeywordBank():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT keywordbank_nama FROM keywordbank")
    keyword_bank_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminKeywordBank.html', keyword_bank_data=keyword_bank_data)

# Route untuk menghapus data keyword bank
@app.route('/deleteKeywordBank', methods=['POST'])
def deleteKeywordBank():
    if request.method == 'POST':
        try:
            data = request.get_json()
            keywordbank_id = data['id']

            cursor = db.cursor()
            query = "DELETE FROM keywordbank WHERE keywordbank_id = %s"
            cursor.execute(query, (keywordbank_id,))
            db.commit()
            cursor.close()

            response = {'status': 'success', 'message': 'Kata kunci berhasil dihapus.'}
            return jsonify(response)
        except Exception as e:
            print("Error deleting keyword:", str(e))
            response = {'status': 'error', 'message': 'Gagal menghapus data: ' + str(e)}
            return jsonify(response), 500

# Route untuk logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Route untuk searching penyakit
@app.route('/search', methods=['GET'])
def search():
    nama_penyakit = request.args.get('query')
    query = """
        SELECT
            penyakit.penyakit_nama,
            penyakit.penyakit_penanganan,
            penyakit.penyakit_obat,
            penyakit.penyakit_deskripsi
        FROM penyakit
        WHERE LOWER(penyakit.penyakit_nama) = LOWER(%s)
    """
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, [nama_penyakit])

    row = cursor.fetchone();
    cursor.close()

    response = {
        'status': 'error',
        'message': 'Data tidak ditemukan'
    }
    responseStatus = 404

    if (row):
        response = {
            'status': 'success',
            'data': {
                'nama': row['penyakit_nama'],
                'penanganan': row['penyakit_penanganan'],
                'obat': row['penyakit_obat'],
                'deskripsi': row['penyakit_deskripsi']
            }
        }
        responseStatus = 200

    return jsonify(response), responseStatus

if __name__ == '__main__':
    app.run(debug=False)
