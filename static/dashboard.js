// Ensure menu state persists
document.addEventListener('DOMContentLoaded', function() {
    const menuBar = document.getElementById('menuBar');
    const menuIcon = document.querySelector('.menu__icon');
    
    // Check if menu was previously active
    if (localStorage.getItem('menuActive') === 'true') {
        menuBar.classList.add('active');
        menuIcon.classList.add('active');
    }
    
    menuIcon.addEventListener('click', function() {
        toggleMenu();
        // Store menu state
        localStorage.setItem('menuActive', menuBar.classList.contains('active'));
    });
});

document.getElementById('tabel').addEventListener('change', function() {
    var tabel = this.value;
    var coloaneDiv = document.getElementById('coloane');
    coloaneDiv.innerHTML = '';

    var coloane = {
        'Elevi': ['cnp_elev', 'nume', 'prenume', 'data_nasterii', 'telefon', 'email'],
        'Instructori': ['cnp_instructor', 'nume', 'prenume', 'telefon', 'email', 'ani_experienta'],
        'Lectii': ['id_lectie', 'cnp_elev', 'cnp_instructor', 'data_lectie', 'ora_lectie', 'durata_minute', 'status_lectie'],
        'Plati': ['id_plata', 'cnp_elev', 'suma', 'data_plata', 'metoda_plata'],
        'Recenzii': ['id_recenzii', 'cnp_elev', 'cnp_instructor', 'rating', 'feedback', 'data_recenzii'],
        'Vehicule': ['serie_sasiu', 'marca', 'model', 'an_fabricatie', 'nr_inmatriculare', 'combustibil', 'tip_transmisie']
    };

    coloane[tabel].forEach(function(col) {
        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = 'coloane';
        checkbox.value = col;
        checkbox.id = col;

        var label = document.createElement('label');
        label.htmlFor = col;
        label.appendChild(document.createTextNode(col));

        coloaneDiv.appendChild(checkbox);
        coloaneDiv.appendChild(label);
        coloaneDiv.appendChild(document.createElement('br'));
    });
});

document.getElementById('resetButton').addEventListener('click', function() {
    document.getElementById('tabel').selectedIndex = 0;
    document.getElementById('coloane').innerHTML = '';
});

window.onload = function() {
    document.getElementById('tabel').selectedIndex = 0;
};

// hamburger button script
function toggleMenu() {
    const menuBar = document.getElementById('menuBar');
    const menuIcon = document.querySelector('.menu__icon');
    
    if (menuBar && menuIcon) {
        // Make an AJAX call to the server
        fetch('/toggle-menu', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                menuBar.classList.toggle('active');
                menuIcon.classList.toggle('active');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

// Ensure menu state persists
document.addEventListener('DOMContentLoaded', function() {
    const menuBar = document.getElementById('menuBar');
    const menuIcon = document.querySelector('.menu__icon');
    
    // Check if menu was previously active
    if (localStorage.getItem('menuActive') === 'true') {
        menuBar.classList.add('active');
        menuIcon.classList.add('active');
    }
    
    menuIcon.addEventListener('click', function() {
        toggleMenu();
        // Store menu state
        localStorage.setItem('menuActive', menuBar.classList.contains('active'));
    });
});

document.getElementById('dashboardForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('/dashboard', {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success' && data.rezultate && data.coloane) {
            const rezultateDiv = document.getElementById('rezultate');
            let tableHTML = '<table><tr>';
            
            // Adaugă headerele
            data.coloane.forEach(col => {
                tableHTML += `<th>${col}</th>`;
            });
            tableHTML += '</tr>';
            
            // Adaugă rândurile
            data.rezultate.forEach(row => {
                tableHTML += '<tr>';
                data.coloane.forEach(col => {
                    tableHTML += `<td>${row[col]}</td>`;
                });
                tableHTML += '</tr>';
            });
            
            tableHTML += '</table>';
            rezultateDiv.innerHTML = tableHTML;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('rezultate').innerHTML = '<p class="error">A apărut o eroare la încărcarea datelor.</p>';
    });
});

function navigateToLogin() {
    window.location.href = '/login';
}

function navigateToHome() {
    window.location.href = '/';
}
function navigateToDelete() {
    window.location.href = "/delete";
}
function navigateToInterogari() {
    window.location.href = "/interogari";
}