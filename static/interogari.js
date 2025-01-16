function executeQuery(queryNumber) {
    fetch(`/simple-query/${queryNumber}`)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => console.error('Error:', error));
}

function executeComplexQuery(queryNumber) {
    fetch(`/complex-query/${queryNumber}`)
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => console.error('Error:', error));
}

function displayResults(data) {
    const resultDiv = document.getElementById('result');
    resultDiv.style.display = 'block'; // Show the result container

    if (data.length === 0) {
        resultDiv.innerHTML = '<p class="error">Nu s-au găsit rezultate.</p>';
        return;
    }

    let tableHTML = '<table><tr>';
    // Adaugă headerele
    Object.keys(data[0]).forEach(key => {
        tableHTML += `<th>${key}</th>`;
    });
    tableHTML += '</tr>';

    // Adaugă rândurile
    data.forEach(row => {
        tableHTML += '<tr>';
        Object.values(row).forEach(value => {
            tableHTML += `<td>${value}</td>`;
        });
        tableHTML += '</tr>';
    });

    tableHTML += '</table>';
    resultDiv.innerHTML = tableHTML;
}
