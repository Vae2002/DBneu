function addReview() {
    const userName = document.getElementById('userName').value;
    const businessName = document.getElementById('businessName').value;
    const businessAddress = document.getElementById('businessAddress').value;
    const businessCity = document.getElementById('businessCity').value;
    const stars = document.getElementById('stars').value;
    const useful = document.getElementById('useful').value;
    const funny = document.getElementById('funny').value;
    const cool = document.getElementById('cool').value;
    const text = document.getElementById('text').value;

    // AJAX-Anfrage zum Hinzufügen einer Bewertung
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/add_review', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    // Fehlerbehandlung
    xhr.onerror = function () {
        displayMessage('Error during request');
    };

    xhr.onload = function () {
        if (xhr.status === 200) {
            displayMessage('Review added successfully');
        } else {
            displayMessage('Failed to add review');
        }
    };

    const data = {
        userName,
        businessName,
        businessAddress,
        businessCity,
        stars,
        useful,
        funny,
        cool,
        text
    };

    xhr.send(JSON.stringify(data));
}

function displayMessage(message) {
    // Erstelle ein neues Element für die Nachricht
    const messageElement = document.createElement('div');
    messageElement.textContent = message;

    // Füge die Nachricht dem HTML-Dokument hinzu (z.B. an das Ende des Body)
    document.body.appendChild(messageElement);

    // Schließe die Nachricht nach ein paar Sekunden
    setTimeout(function () {
        document.body.removeChild(messageElement);
    }, 5000);  // Nachricht bleibt 5 Sekunden sichtbar (5000 Millisekunden)
}
