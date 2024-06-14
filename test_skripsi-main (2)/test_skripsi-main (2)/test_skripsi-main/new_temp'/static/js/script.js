document.addEventListener('DOMContentLoaded', function() {
    // Function to change text color on button click
    function changeTextColor() {
        var textColor = getRandomColor();
        document.getElementById('text-to-change').style.color = textColor;
    }

    // Helper function to generate a random color
    function getRandomColor() {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    // Attach the click event to the button
    document.getElementById('color-button').addEventListener('click', changeTextColor);
});
