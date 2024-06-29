from flask import Flask, render_template, request, redirect, url_for, jsonify, session, render_template_string
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Konfigurasi koneksi ke database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Password_123",
    database="pharmadia_db"
)

# Route untuk halaman utama (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman result-page
@app.route('/result-page')
def resultpage():
    query = request.args.get('query')
    if query:
        result = searchDiseaseByName(query)
        if result:
            disease_name = result['name']
            disease_description = result['description']
        else:
            disease_name = 'Penyakit tidak ditemukan'
            disease_description = ''
        return render_template('result-page.html', disease_name=disease_name, disease_description=disease_description)
    return render_template('result-page.html', disease_name=None, disease_description=None)

# Route untuk halaman about us for user
@app.route('/aboutUsForUser')
def aboutUsForUser():
    return render_template('aboutUs.html')

# Route untuk halaman feedback
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

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

        # Cek apakah nama penyakit sudah ada
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM penyakit WHERE penyakit_nama = %s", (penyakit_nama,))
        existing_disease = cursor.fetchone()
        cursor.close()

        if existing_disease:
            error_message = 'Nama penyakit sudah ada. Silakan gunakan nama penyakit lain.'
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
            cursor = db.cursor()
            query = """
                INSERT INTO penyakit (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, auth_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (penyakit_nama, penyakit_penanganan, penyakit_obat, penyakit_deskripsi, auth_id))
            db.commit()
            cursor.close()

            return redirect(url_for('adminDisease'))

    return render_template('data_admin/createDisease.html')

# Route untuk menyimpan data penyakit yang diperbarui ke database
@app.route('/updateDisease', methods=['POST'])
def updateDisease():
    if request.method == 'POST':
        data = request.get_json()
        penyakit_id = data['penyakit_id']
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

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM keyword WHERE penyakit_id = %s AND keyword_nama = %s", (penyakit_id, keyword_nama))
        existing_keyword = cursor.fetchone()
        cursor.close()

        if existing_keyword:
            error_message = 'Kombinasi nama penyakit dan kata kunci sudah ada. Silakan gunakan kombinasi lain.'
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
    
# Route untuk halaman about us
@app.route('/aboutUs')
def adminAbousUs():
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM about_us
    """)
    aboutus_data = cursor.fetchall()
    cursor.close()
    return render_template('data_admin/adminAboutUs.html', aboutus_data=aboutus_data)

# Route untuk menyimpan data about us yang diperbarui ke database@app.route('/updateAboutUs', methods=['POST'])
@app.route('/updateAboutUs', methods=['POST'])
def updateAboutUs():
    if request.method == 'POST':
        data = request.get_json()
        deskripsi = data['deskripsi']
        nama = data['nama']
        no_telephone = data['no_telephone']
        sosial_media = data['sosial_media']

        cursor = db.cursor()
        query = """
            UPDATE about_us
            SET deskripsi = %s, nama = %s, no_telephone = %s, sosial_media = %s
            WHERE id = 1 
        """
        cursor.execute(query, (deskripsi, nama, no_telephone, sosial_media))
        db.commit()
        cursor.close()

        response = {'status': 'success', 'message': 'Data berhasil diperbarui.'}
        return jsonify(response)

# Route untuk halaman keyword bank
@app.route('/keywordBank')
def adminKeywordBank():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM keywordbank")
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

            response = {'status': 'success', 'message': 'Kata kunci berhasil dihapus dari database.'}
            return jsonify(response)
        except Exception as e:
            print("Error deleting keyword from database:", str(e))
            response = {'status': 'error', 'message': 'Gagal menghapus data dari database: ' + str(e)}
            return jsonify(response), 500

@app.route('/moveToKeyword', methods=['POST'])
def moveKeywords():
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute("SELECT * FROM keywordbank")
        keywords = cursor.fetchall()
        
        for keyword in keywords:
            keyword_id = keyword[0]
            keyword_nama = keyword[1]
            cursor.execute("INSERT INTO keyword (keyword_id, keyword_nama) VALUES (%s, %s)", (keyword_id, keyword_nama))
        
        cursor.execute("DELETE FROM keywordbank")
        
        cursor.close()
        db.commit()
        
        cursor = db.cursor()
        cursor.execute("SELECT * FROM keyword")
        new_keywords = cursor.fetchall()
        cursor.close()
        
        return render_template('keyword.html', keywords=new_keywords)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# Fungsi untuk mencari penyakit berdasarkan nama
def searchDiseaseByName(name):
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT penyakit_nama AS name, penyakit_deskripsi AS description
        FROM penyakit
        WHERE penyakit_nama LIKE %s
    """
    cursor.execute(query, ('%' + name + '%',))
    result = cursor.fetchone()
    cursor.close()
    return result

if __name__ == '__main__':
    app.run(debug=True)
