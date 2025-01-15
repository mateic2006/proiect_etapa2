document.getElementById('verifyEmail').addEventListener('click', async function() {
    const email = document.getElementById('email').value;
    const spinner = document.querySelector('.dot-spinner');
    const emailSection = document.getElementById('emailSection');
    const passwordSection = document.getElementById('passwordSection');

    try {
        // Show spinner and hide email section
        emailSection.style.display = 'none';
        spinner.style.display = 'block';

        // Verify email
        const response = await fetch('/verify-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `email=${encodeURIComponent(email)}`
        });
        const data = await response.json();

        // Wait for 2 seconds
        await new Promise(resolve => setTimeout(resolve, 2000));

        if (data.exists) {
            // Hide spinner and show password section
            spinner.style.display = 'none';
            passwordSection.style.display = 'block';
        } else {
            alert('Email not found in database');
            emailSection.style.display = 'block';
            spinner.style.display = 'none';
        }
    } catch (error) {
        alert('An error occurred');
        emailSection.style.display = 'block';
        spinner.style.display = 'none';
    }
});
