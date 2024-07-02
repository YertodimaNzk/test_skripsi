// Fungsi untuk mengambil value input yang ada di search bar
document.getElementById("diseaseInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") { 
        event.preventDefault();
        var query = document.getElementById("diseaseInput").value.trim();
        if (query !== '') {
            // Melakukan redirection ke halaman result page
            window.location.href = "/result-page?query=" + encodeURIComponent(query);
        }
    }
});

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