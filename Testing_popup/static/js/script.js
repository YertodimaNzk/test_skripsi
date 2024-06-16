document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('search-bar');
    const micButton = document.getElementById('mic-button');
    const listeningPopup = document.getElementById('listening-popup');

    // Check if the browser supports Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert('Your browser does not support Speech Recognition. Please try another browser.');
        return;
    }

    const recognition = new SpeechRecognition();

    micButton.addEventListener('click', () => {
        recognition.start();
        listeningPopup.classList.remove('hidden');
    });

    recognition.onresult = (event) => {
        const speechResult = event.results[0][0].transcript.toLowerCase();
        searchBar.value = speechResult;
        listeningPopup.classList.add('hidden');
        window.location.href = `/result?query=${speechResult}`;
    };

    recognition.onspeechend = () => {
        recognition.stop();
        listeningPopup.classList.add('hidden');
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        listeningPopup.classList.add('hidden');
    };

    // Allow searching with the Enter key
    searchBar.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            const query = searchBar.value.trim().toLowerCase();
            if (query) {
                window.location.href = `/result?query=${query}`;
            }
        }
    });

    // Handle case where no speech is detected
    recognition.onaudiostart = () => {
        console.log('Audio capturing started');
    };

    recognition.onsoundstart = () => {
        console.log('Sound has been detected');
    };

    recognition.onsoundend = () => {
        console.log('Sound has stopped being detected');
    };

    recognition.onspeechstart = () => {
        console.log('Speech has been detected');
    };

    recognition.onspeechend = () => {
        console.log('Speech has stopped being detected');
        recognition.stop();
        listeningPopup.classList.add('hidden');
    };

    recognition.onaudioend = () => {
        console.log('Audio capturing ended');
        recognition.stop();
        listeningPopup.classList.add('hidden');
    };
});
