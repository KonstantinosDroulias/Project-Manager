function toggleDropdown() {
        const dropdown = document.getElementById('user-dropdown-menu');
        dropdown.classList.toggle('hidden');
    }

    // Optional: Close dropdown if clicking outside of it
    window.onclick = function(event) {
        if (!event.target.closest('#user-menu-button')) {
            const dropdown = document.getElementById('user-dropdown-menu');
            if (!dropdown.classList.contains('hidden')) {
                dropdown.classList.add('hidden');
            }
        }
    }