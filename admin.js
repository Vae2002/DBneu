// admin.js
function addAdmin() {
    var businessName = document.getElementById('businessName').value;
    var businessAddress = document.getElementById('businessAddress').value;
    var businessCity = document.getElementById('businessCity').value;
    var adminName = document.getElementById('adminName').value;
    var adminUsername = document.getElementById('adminUsername').value;
    var adminEmail = document.getElementById('adminEmail').value;
    var adminPassword = document.getElementById('adminPassword').value;
    var adminPasswordConfirm = document.getElementById('adminPasswordConfirm').value;
    var thresholdPercentage = document.getElementById('thresholdPercentage').value;
    var lastNReviews = document.getElementById('lastNReviews').value;

    // AJAX-Anfrage zum Hinzufügen eines Admins
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/add_admin', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            displayMessage('Admin added successfully');
        } else {
            displayMessage('Failed to add admin');
        }
    };

    xhr.onerror = function () {
        displayMessage('Error during request');
    };

    var data = {
        businessName: businessName,
        businessAddress: businessAddress,
        businessCity: businessCity,
        adminName: adminName,
        adminUsername: adminUsername,
        adminEmail: adminEmail,
        adminPassword: adminPassword,
        adminPasswordConfirm: adminPasswordConfirm,
        thresholdPercentage: thresholdPercentage,
        lastNReviews: lastNReviews
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
