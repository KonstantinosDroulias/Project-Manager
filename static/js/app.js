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

document.addEventListener('DOMContentLoaded', function() {
    const toasts = document.querySelectorAll('.msg-toast');

    toasts.forEach((toast, index) => {
        // Stagger the disappearance slightly if there are multiple messages
        setTimeout(() => {
            // Add a fade-out effect before removing
            toast.style.transition = 'opacity 0.5s ease-out, transform 0.5s ease-in';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-10px)';

            // Remove from DOM after transition finishes
            setTimeout(() => {
                toast.remove();
            }, 500);
        }, 4000 + (index * 500)); // 4 seconds base time
    });
});