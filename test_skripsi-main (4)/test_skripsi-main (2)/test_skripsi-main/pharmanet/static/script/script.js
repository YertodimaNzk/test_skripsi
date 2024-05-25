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

// Fungsi untuk menampilkan hasil pencarian menggunakan enter
document.getElementById("diseaseInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        searchDisease();
    }
});

// Fungsi untuk menampilkan hasil pencarian
function displaySearchResult(name, description) {
    var resultDiv = document.getElementById('searchResult');
    resultDiv.innerHTML = `<strong>${name}</strong>: ${description}`;
    window.location.href = "/result-page?query=" + encodeURIComponent(name);
}

// optimasi speech recognition 
function startListening(){
    const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'id-ID';
    recognition.start();

    recognition.onresult = function(event) {
        var result = event.results[0][0].transcript;
        document.getElementById('diseaseInput').value = result;
        console.log('Speech Recognition:', result);
        searchDisease(); 
    }
}

// Inisialisasi recognition object untuk speech-to-text
function startSpeechRecognition() {
    startListening();
}
