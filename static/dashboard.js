document.getElementById('tabel').addEventListener('change', function() {
    var tabel = this.value;
    var coloaneDiv = document.getElementById('coloane');
    coloaneDiv.innerHTML = '';

    var coloane = {
        'Elevi': ['cnp_elev', 'nume', 'prenume', 'data_nasterii', 'telefon', 'email'],
        'Instructori': ['cnp_instructor', 'nume', 'prenume', 'telefon', 'email', 'ani_experienta'],
        'Lectii': ['id_lectie', 'cnp_elev', 'cnp_instructor', 'data_lectie', 'ora_lectie', 'durata_minute', 'status_lectie'],
        'Plati': ['id_plata', 'cnp_elev', 'suma', 'data_plata', 'metoda_plata'],
        'Recenzii': ['id_recenzii', 'cnp_elev', 'cnp_instructor', 'rating', 'feedback', 'data_recenzie'],
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