document.getElementById('deleteForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const identifier = document.getElementById('identifier').value;
    fetch('/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ identifier: identifier })
    })
    .then(response => response.json())
    .then(data => {
        const messageDiv = document.getElementById('message');
        if (data.success) {
            messageDiv.textContent = 'Account deleted successfully.';
            messageDiv.style.color = 'green';
        } else {
            messageDiv.textContent = 'Error: ' + data.error;
            messageDiv.style.color = 'red';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
