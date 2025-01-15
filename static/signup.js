// Toggle between "Data Nasterii" and "Ani Experienta" based on the switch state
document.getElementById('switch').addEventListener('change', function() {
    const isChecked = this.checked;
    const dataNasteriiSpan = document.getElementById('dataNasteriiSpan');
    const aniExperientaSpan = document.getElementById('aniExperientaSpan');
    const dataNasteriiInput = document.getElementById('data_nasterii');
    const aniExperientaInput = document.getElementById('ani_experienta');

    if (isChecked) {
        dataNasteriiSpan.style.display = 'none';
        dataNasteriiInput.disabled = true;
        aniExperientaSpan.style.display = 'block';
        aniExperientaInput.disabled = false;
    } else {
        dataNasteriiSpan.style.display = 'block';
        dataNasteriiInput.disabled = false;
        aniExperientaSpan.style.display = 'none';
        aniExperientaInput.disabled = true;
    }
});
