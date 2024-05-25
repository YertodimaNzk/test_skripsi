document.addEventListener("DOMContentLoaded", function() {
    // Function text to speak
    function speakText(text) {
        // kirim ke backend
        fetch('/synthesize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        })
        .then(response => response.arrayBuffer())
        .then(audioData => {
            const audioBlob = new Blob([audioData], { type: 'audio/mp3' });
            const audioUrl = URL.createObjectURL(audioBlob);

            // buat dan mainkan suaranya dari yang sudah di tembak ke endpoint
            const audio = new Audio(audioUrl);
            audio.play();
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    // Iterate setiap test dengan class 'speakable'
    const speakableElements = document.querySelectorAll('.speakable');
    speakableElements.forEach(element => {
        element.addEventListener('click', function() {
            const textToSpeak = element.innerText.trim();
            speakText(textToSpeak);
        });
    });

});
