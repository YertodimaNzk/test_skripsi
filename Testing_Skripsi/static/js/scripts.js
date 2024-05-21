const searchBar = document.getElementById('search-bar');
const resultDiv = document.getElementById('result-container');
let voices = [];

function loadVoices() {
    voices = speechSynthesis.getVoices();
}

function getMaleVoice() {
    // Mencari suara laki-laki dalam bahasa Indonesia
    return voices.find(voice => voice.lang.includes("id") && voice.name.includes("Google") && voice.name.includes("male"));
}

function searchDisease() {
    const query = searchBar.value;
    if (query) {
        window.location.href = `/result?query=${query}`;
    }
}

function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'id-ID';
    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        searchBar.value = transcript;
        searchDisease();
    };
}

function speakText(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'id-ID'; // Mengatur bahasa menjadi Indonesia
    speech.rate = 0.9;  // Kecepatan sedikit lebih lambat dari default (1)
    speech.pitch = 1;  // Nada normal
    speech.volume = 1;  // Volume penuh

    // Menetapkan suara laki-laki dalam bahasa Indonesia jika tersedia
    const maleVoice = getMaleVoice();
    if (maleVoice) {
        speech.voice = maleVoice;
    }

    speech.onstart = function() {
        console.log('Speech started');
    };

    speech.onend = function() {
        console.log('Speech ended');
    };

    speech.onerror = function(event) {
        console.error('Speech error: ' + event.error);
    };

    window.speechSynthesis.speak(speech);
}

// Memuat suara saat halaman dimuat
window.onload = function() {
    loadVoices();
    // Beberapa browser memerlukan waktu untuk memuat suara
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }
};
