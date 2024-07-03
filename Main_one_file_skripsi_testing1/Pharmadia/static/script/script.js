// Fungsi untuk mengambil value input yang ada di search bar
document.getElementById("diseaseInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") { 
        event.preventDefault();
        performSearch();
    }
});

function performSearch() {
    var query = document.getElementById("diseaseInput").value.trim();
    if (query !== '') {
        // Melakukan redirection ke halaman result page
        window.location.href = "/result-page?query=" + encodeURIComponent(query);
    }
}

function startSpeechRecognition() {
    // Inisialisasi recognition object untuk speech-to-text
    var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'id-ID'; // Bahasa Indonesia, sesuaikan jika diperlukan

    // Event listener untuk hasil speech recognition
    recognition.onresult = function(event) {
        var result = event.results[0][0].transcript;
        document.getElementById('diseaseInput').value = result;
        console.log('Speech Recognition:', result);
        performSearch(); // Memanggil fungsi pencarian dengan hasil speech recognition
    }

    // Start recognition
    recognition.start();
}
