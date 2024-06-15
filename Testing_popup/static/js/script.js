document.addEventListener('DOMContentLoaded', function() {
    const searchBar = document.getElementById('search-bar');
    const micButton = document.getElementById('mic-button');
    const listeningPopup = document.getElementById('listening-popup');
    const resultContainer = document.getElementById('result');
    const diseaseNameElem = document.getElementById('disease-name');
    const descriptionElem = document.getElementById('description');
    const treatmentElem = document.getElementById('treatment');
    const medicationElem = document.getElementById('medication');

    const diseases = {
        "anemia": {
            "description": "Anemia is a condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues.",
            "treatment": "Treatment for anemia depends on the cause.",
            "medication": "Iron supplements, Vitamin B12 injections, and Folic acid supplements."
        },
        "diabetes": {
            "description": "Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high.",
            "treatment": "Healthy eating, regular exercise, and blood sugar monitoring.",
            "medication": "Insulin therapy, Metformin, and other oral medications."
        }
        // Tambahkan data penyakit lainnya di sini
    };

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
        displayResult(speechResult);
    };

    recognition.onspeechend = () => {
        recognition.stop();
        listeningPopup.classList.add('hidden');
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error);
        listeningPopup.classList.add('hidden');
    };

    function displayResult(query) {
        const result = diseases[query];
        if (result) {
            diseaseNameElem.textContent = query.charAt(0).toUpperCase() + query.slice(1);
            descriptionElem.textContent = result.description;
            treatmentElem.textContent = result.treatment;
            medicationElem.textContent = result.medication;
            resultContainer.classList.remove('hidden');
        } else {
            diseaseNameElem.textContent = "Not found";
            descriptionElem.textContent = "";
            treatmentElem.textContent = "";
            medicationElem.textContent = "";
            resultContainer.classList.remove('hidden');
        }
    }
});
