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