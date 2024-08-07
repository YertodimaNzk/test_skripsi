from flask import Flask, render_template, request, redirect, url_for, jsonify, session, render_template_string, flash
import mysql.connector
from datetime import datetime

#ini runapp.py

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Konfigurasi koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3306,
    password="Password_123",
    database="pharmadia_db3"
)

# Route untuk halaman utama (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman result-page
@app.route('/result-page')
def resultpage():
    # Mendapatkan query parameter
    query = request.args.get('query')

    logging.info(f"query penyakit: {query}")
    print(f"query penyakit: {query}")
    # Kembalikan halaman result page dengan isi kosong
    if not query:
        return render_template('result-page.html', error='Penyakit tidak ditemukan')
    cursor = db.cursor()
    query1 = "INSERT INTO keywordbank (keywordbank_nama) VALUES (%s)"
    cursor.execute(query1, (query,))
    db.commit()
    cursor.close()
    # Melakukan pencarian di database
    result = searchDiseaseByKeyword(query)
    if result == None:
        # Menampilkan result page dengan data error
        return render_template('result-page.html', error='Penyakit tidak ditemukan')
    # Menampilkan result page dengan data hasil pencarian database
    return render_template('result-page.html', disease=result)

# Route untuk halaman about us for user
@app.route('/aboutUsForUser')
def about_us():
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT deskripsi, nama, sosial_media, no_telepone FROM about_us")
        about_us_data = cursor.fetchone()

        if about_us_data:
            return render_template('aboutUs.html', about_us_data=about_us_data)
        else:
            return render_template('aboutUs.html', about_us_data=None)

    except Exception as e:
        print("Error fetching about us data:", str(e))
        return render_template('about_us.html', about_us_data=None)

# Route untuk halaman feedback
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# Route untuk menyimpan hasil feedback user
@app.route('/submitFeedback', methods=['POST'])
def submit_feedback():
    if db is None:
        return "Database connection failed", 500

    masukan = request.form['masukan']
    created_at = datetime.now()

    try:
        cursor = db.cursor()
        query = "INSERT INTO masukan (masukan, created_at) VALUES (%s, %s)"
        cursor.execute(query, (masukan, created_at))
        db.commit()
        cursor.close()
    except mysql.connector.Error as err:
        logging.error(f"Error: {err}")
        return "Database query failed", 500

    flash("Feedback sudah terkirim")
    return redirect(url_for('feedback'))

# Route untuk halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM authorization WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            if user['password'] == password:
                session['user_id'] = user['auth_id']
                session['username'] = user['username']
                return redirect(url_for('admin'))
            else:
                return render_template('login.html', error="Username dan password salah, silakan coba lagi.")
        else:
            return render_template('login.html', error="Username dan password salah, silakan coba lagi.")
    
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
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM authorization WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            error_message = 'Nama pengguna sudah ada. Silakan gunakan nama pengguna lain.'
            return render_template_string('''
                <script>
                function showErrorMessage(message) {
                    var overlay = document.createElement('div');
                    overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;';

                    var alertBox = document.createElement('div');
                    alertBox.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #EEEEEE; color: black; padding: 20px; border: 1px solid #176B87; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); z-index: 10000; font-family: "Open Sans", sans-serif; text-align: center;';

                    var messageElement = document.createElement('p');
                    messageElement.innerText = message;

                    var closeButton = document.createElement('button');
                    closeButton.innerText = 'OK';
                    closeButton.style.cssText = 'background-color: #176B87; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px; font-family: "Open Sans", sans-serif; width: fit-content; margin: 0 auto;';

                    closeButton.onclick = function() {
                        overlay.remove();
                        window.location.href = '/createAuthorization';
                    };

                    alertBox.appendChild(messageElement);
                    alertBox.appendChild(closeButton);

                    overlay.appendChild(alertBox);

                    document.body.appendChild(overlay);
                }

                window.onload = function() {
                    showErrorMessage('{{ error_message }}');
                };
            </script>
            ''', error_message=error_message)
        else:
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
@app.route('/createDisease', methods=['GET', 'POST'])
def adminCreateDisease():
    if request.method == 'POST':
        penyakit_nama = request.form['penyakit_nama']
        penyakit_penanganan = request.form['penyakit_penanganan']
        penyakit_obat = request.form['penyakit_obat']
        penyakit_deskripsi = request.form['penyakit_deskripsi']

        # Mengakses auth_id dari sesi yang telah diotentikasi
        auth_id = session.get('user_id')
        username = session.get('username')

        # Cek apakah nama penyakit sudah ada
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM penyakit WHERE penyakit_nama = %s", (penyakit_nama,))
        existing_disease = cursor.fetchone()
        cursor.execute("SELECT * FROM keyword WHERE keyword_nama = %s", (penyakit_nama,))
        existing_keyword = cursor.fetchone()

        db.commit()
        cursor.close()

        if existing_disease or existing_keyword:
            error_message = ''
            if (existing_disease):
                error_message = 'Nama penyakit sudah ada. Silakan gunakan nama penyakit lain.'
            if (existing_keyword):
                error_message = 'Nama penyakit sudah digunakan sebagai kata kunci penyakit lain. Silahkan gunakan nama penyakit lain'
            return render_template_string('''
                <script>
                    function showErrorMessage(message) {
                        var overlay = document.createElement('div');
                        overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;';

                        var alertBox = document.createElement('div');
                        alertBox.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #EEEEEE; color: black; padding: 20px; border: 1px solid #176B87; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); z-index: 10000; font-family: "Open Sans", sans-serif; text-align: center;';

                        var messageElement = document.createElement('p');
                        messageElement.innerText = message;

                        var closeButton = document.createElement('button');
                        closeButton.innerText = 'OK';
                        closeButton.style.cssText = 'background-color: #176B87; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px; font-family: "Open Sans", sans-serif; width: fit-content; margin: 0 auto;';

                        closeButton.onclick = function() {
                            overlay.remove();
                            window.location.href = '/createDisease';
                        };

                        alertBox.appendChild(messageElement);
                        alertBox.appendChild(closeButton);

                        overlay.appendChild(alertBox);

                        document.body.appendChild(overlay);
                    }

                    window.onload = function() {
                        showErrorMessage('{{ error_message }}');
                    };
                </script>
            ''', error_message=error_message)

        else:
            # Ambil koneksi
            cursor = db.cursor()

            # Memasukan penyakit ke table penyakit
            query = """
                INSERT INTO penyakit (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, auth_id, created_by, updated_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, auth_id, username, username))

            # Jika tidak berhasil memasukan data penyakit
            if cursor.rowcount <= 0:
                # Rollback transaksi
                db.rollback()
                return redirect(url_for('adminDisease'))

            penyakit_id = cursor.lastrowid
            query = """
                INSERT INTO keyword (penyakit_id, keyword_nama, auth_id, created_by, updated_by)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (penyakit_id, penyakit_nama, auth_id, username, username))

            # Jika tidak berhasil memasukan data penyakit
            if cursor.rowcount <= 0:
                # Rollback transaksi
                db.rollback()
                return redirect(url_for('adminDisease'))

            db.commit()
            cursor.close()

            return redirect(url_for('adminDisease'))

    return render_template('data_admin/createDisease.html')

# Route untuk menyimpan data penyakit yang diperbarui ke database
@app.route('/updateDisease', methods=['POST'])
def updateDisease():
    if request.method == 'POST':
        try:
            data = request.get_json()
            penyakit_id = data['id']
            penyakit_nama = data['penyakit_nama']
            penyakit_penanganan = data['penyakit_penanganan']
            penyakit_obat = data['penyakit_obat']
            penyakit_deskripsi = data['penyakit_deskripsi']

            cursor = db.cursor()
            query = """
                UPDATE penyakit
                SET penyakit_nama = %s, penyakit_penanganan = %s, penyakit_obat = %s, penyakit_deskripsi = %s
                WHERE penyakit_id = %s
            """
            cursor.execute(query, (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, penyakit_id))
            db.commit()
            cursor.close()

            response = {'status': 'success', 'message': 'Data berhasil diperbarui.'}
            return jsonify(response)

        except Exception as e:
            print("Error updating disease:", str(e))
            response = {'status': 'error', 'message': 'Gagal memperbarui data: ' + str(e)}
            return jsonify(response), 500

# Route untuk menghapus data penyakit
@app.route('/deleteDisease', methods=['POST'])
def deleteDisease():
    if request.method == 'POST':
        data = request.get_json()
        penyakit_id = data['penyakit_id']

        cursor = db.cursor()
        query = """
            DELETE FROM penyakit
            WHERE penyakit_id = %s
        """
        cursor.execute(query, (penyakit_id,))
        db.commit()
        cursor.close()

        response = {'status': 'success', 'message': 'Data berhasil dihapus.'}
        return jsonify(response)



# Route untuk halaman keyword
@app.route('/keyword')
def adminKeyword():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT keyword.keyword_id, penyakit.penyakit_nama, keyword.keyword_nama
        FROM keyword
        JOIN penyakit ON keyword.penyakit_id = penyakit.penyakit_id
    """)
    keyword_data = cursor.fetchall()
    print("keyword_data",keyword_data)
    cursor.close()
    return render_template('data_admin/adminKeyword.html', keyword_data=keyword_data)

# Route untuk halaman create keyword dengan method POST untuk menyimpan data
from flask import request, render_template, render_template_string, redirect, url_for
import logging

@app.route('/createKeyword', methods=['GET', 'POST'])
def adminCreateKeyword():
    if request.method == 'POST':
        penyakit_id = request.form['penyakit_id']
        keyword_nama = request.form['keyword_nama']

        # Mengakses auth_id dari sesi yang telah diotentikasi
        auth_id = session.get('user_id')
        username = session.get('username')

        # Debugging print statements
        print(f"penyakit_id: {penyakit_id}")
        logging.info(f"penyakit_id: {penyakit_id}")

        cursor = db.cursor(dictionary=True)
        # Handle 1 nama keyword hanya boleh 1 penyakit saja
        # (karena ui tidak mendukung nampilin atau memilih 2 atau lebih penyakit berbeda yang mau ditampilkan)
        cursor.execute("SELECT * FROM keyword WHERE keyword_nama = %s", (keyword_nama,))
        existing_keyword = cursor.fetchone()
        cursor.close()

        if existing_keyword:
            error_message = 'Kata kunci sudah digunakan. Silakan gunakan kata kunci lain.'
            return render_template_string('''
                <script>
                    function showErrorMessage(message) {
                        var overlay = document.createElement('div');
                        overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0, 0, 0, 0.5); z-index: 9999;';

                        var alertBox = document.createElement('div');
                        alertBox.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: #EEEEEE; color: black; padding: 20px; border: 1px solid #176B87; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); z-index: 10000; font-family: "Open Sans", sans-serif; text-align: center;';

                        var messageElement = document.createElement('p');
                        messageElement.innerText = message;

                        var closeButton = document.createElement('button');
                        closeButton.innerText = 'OK';
                        closeButton.style.cssText = 'background-color: #176B87; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px; font-family: "Open Sans", sans-serif; width: fit-content; margin: 0 auto;';

                        closeButton.onclick = function() {
                            overlay.remove();
                            window.location.href = '/createKeyword';
                        };

                        alertBox.appendChild(messageElement);
                        alertBox.appendChild(closeButton);

                        overlay.appendChild(alertBox);

                        document.body.appendChild(overlay);
                    }

                    window.onload = function() {
                        showErrorMessage('{{ error_message }}');
                    };
                </script>
            ''', error_message=error_message)
        else:
            cursor = db.cursor()
            query = """
                INSERT INTO keyword (penyakit_id, keyword_nama, auth_id, created_by, updated_by)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (penyakit_id, keyword_nama, auth_id, username, username))
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
            print("keyword_nama:", keyword_nama)

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

# Route untuk halaman about us
@app.route('/aboutUs')
def adminAboutUs():
    cursor = db.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM about_us")
    about_us_data = cursor.fetchone()
    cursor.close()
    return render_template('data_admin/adminAboutUs.html', about_us_data=about_us_data)

# Route untuk menyimpan data about us yang diperbarui ke database@app.route('/updateAboutUs', methods=['POST'])
@app.route('/updateAboutUs', methods=['POST'])
def updateAboutUs():
    data = request.get_json()
    deskripsi = data.get('deskripsi')
    nama = data.get('nama')
    no_telepone = data.get('no_telepone')
    sosial_media = data.get('sosial_media')

    if not deskripsi or not nama or not no_telepone or not sosial_media:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    try:
        cursor = db.cursor()
        update_query = """
            UPDATE about_us
            SET deskripsi = %s, no_telepone = %s, sosial_media = %s
            WHERE nama = %s
        """
        cursor.execute(update_query, (deskripsi, no_telepone, sosial_media, nama))
        db.commit()
        cursor.close()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to update data'}), 500

# Route untuk halaman keyword bank
@app.route('/keywordBank')
def adminKeywordBank():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM keywordbank")
    keyword_bank_data = cursor.fetchall()
    cursor.execute(""" SELECT * FROM penyakit """)
    penyakit_data = cursor.fetchall()
    cursor.execute(""" SELECT * FROM keyword """)
    keywords = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminKeywordBank.html', keyword_bank_data=keyword_bank_data, penyakit_data=penyakit_data, keywords=keywords)


# Route untuk menghapus data keyword bank
@app.route('/deleteKeywordBank', methods=['POST'])
def deleteKeywordBank():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(f"Received data: {data}")  # Log the received data
            keywordbank_id = data['id']
            print(f"Deleting keyword with ID: {keywordbank_id}")
            

            cursor = db.cursor()
            query = "DELETE FROM keywordbank WHERE keywordbank_id = %s"
            cursor.execute(query, (keywordbank_id,))
            db.commit()
            cursor.close()

            response = {'status': 'success', 'message': 'Kata kunci berhasil dihapus dari database.'}
            return jsonify(response)
        except Exception as e:
            print("Error deleting keyword from database:", str(e))
            response = {'status': 'error', 'message': 'Gagal menghapus data dari database: ' + str(e)}
            return jsonify(response), 500

@app.route('/moveToKeyword', methods=['POST'])
def moveKeywords():
    if request.method == 'POST':
        print(request.json)
        keyword_nama = request.json['keyword_nama']
        penyakit_id = request.json['penyakit_id']
        print(617, penyakit_id)
        cursor = db.cursor()
        cursor.execute("INSERT INTO keyword (keyword_nama, penyakit_id) VALUES (%s, %s)", (keyword_nama,penyakit_id,))
        cursor.execute("DELETE FROM keywordbank WHERE keywordbank_nama = %s", (keyword_nama,))

        cursor.close()
        db.commit()

        # cursor = db.cursor()
        # cursor.execute("SELECT * FROM keyword")
        # new_keywords = cursor.fetchall()
        # cursor.close()

        # return render_template('adminKeywordBank.html', keywords=new_keywords)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM keywordbank")
        keyword_bank_data = cursor.fetchall()
        print("keyword_bank_data",keyword_bank_data)
        cursor.execute(""" SELECT * FROM penyakit """)
        penyakit_data = cursor.fetchall()
        print("penyakit_data",penyakit_data)
        cursor.close()
        return render_template('data_admin/adminKeywordBank.html', keyword_bank_data=keyword_bank_data, penyakit_data=penyakit_data)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Fungsi untuk mencari penyakit berdasarkan keyword
def searchDiseaseByKeyword(keyword):
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT
            p.penyakit_nama AS name,
            p.penyakit_deskripsi AS description,
            p.penyakit_penanganan AS penanganan,
            p.penyakit_obat AS obat
        FROM keyword AS k
        JOIN penyakit AS p ON p.penyakit_id = k.penyakit_id
        WHERE k.keyword_nama LIKE %s;
    """
    cursor.execute(query, ('%' + keyword + '%',))
    # Mendapatkan semua hasil (karena menggunakan LIKE ada kemungkinan hasil lebih dari 1)
    result = cursor.fetchall()
    cursor.close()
    # Jika hasil yang didapat dari database tidak array kosong
    if len(result) != 0:
        # Ambil penyakit yang ditemukan pertama
        result = result[0]
    # Jika hasilnya array kosong
    else:
        # Kembalikan None
        result = None
    return result

if __name__ == '__main__':
    app.run(debug=True)
