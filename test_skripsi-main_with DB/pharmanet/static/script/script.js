// Data penyakit untuk simulasi pencarian
var diseases = [
    { name: 'Anemia', description: 'Anemia adalah kondisi kekurangan sel darah merah.' },
    { name: 'Flu', description: 'Flu adalah penyakit pernapasan yang disebabkan oleh virus.' },
    { name: 'Demam', description: 'Demam adalah kondisi kenaikan suhu tubuh di atas normal.' },
    { name: 'Hipertensi', description: 'Hipertensi atau tekanan darah tinggi adalah kondisi medis yang ditandai dengan tekanan darah tinggi.' }
];

// Fungsi untuk melakukan pencarian penyakit berdasarkan nama
function searchDiseaseByName(query) {
    query = query.toLowerCase().trim();
    // Cari penyakit berdasarkan nama (exact match)
    return diseases.find(disease => disease.name.toLowerCase() === query);
}

// Fungsi untuk melakukan pencarian penyakit
function searchDisease() {
    var input = document.getElementById('diseaseInput').value.trim();
    if (input !== '') {
        var result = searchDiseaseByName(input);
        if (result) {
            displaySearchResult(result.name, result.description);
        } else {
            displaySearchResult('Penyakit tidak ditemukan', '');
        }
    }
}

// Untuk menampilkan hasil pencarian menggunakan enter
document.getElementById("diseaseInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        var query = document.getElementById("diseaseInput").value.trim();
        if (query !== '') {
            window.location.href = "/result-page?query=" + encodeURIComponent(query);
        }
    }
});

// Fungsi untuk menampilkan hasil pencarian
function displaySearchResult(name, drug, handle, description) {
    var resultDiv = document.getElementById('searchResult');
    resultDiv.innerHTML = `
        <strong>Penyakit : ${name}</strong>
        <br>
        <strong>Penanganan : ${handle}</strong>
        <br>
        <strong>Obat : ${drug}</strong>
        <br>
        <strong>Deskripsi :</strong>
        <p>${description}</p>`;
}

// Fungsi untuk menampilkan pesan error
function displayErrorResult(message) {
    var resultDiv = document.getElementById('searchResult');
    resultDiv.innerHTML = `<strong>${message}</strong>`;
}


// Inisialisasi recognition object untuk speech-to-text
var recognition = new webkitSpeechRecognition() || new SpeechRecognition();
recognition.lang = 'id-ID'; // Bahasa Indonesia, sesuaikan jika diperlukan

// Event listener untuk hasil speech recognition
recognition.onresult = function(event) {
    var result = event.results[0][0].transcript;
    document.getElementById('diseaseInput').value = result;
    console.log('Speech Recognition:', result);
    searchDisease(); // Memanggil fungsi pencarian dengan hasil speech recognition
}

// Fungsi untuk memulai speech recognition
function startSpeechRecognition() {
    recognition.start();
}