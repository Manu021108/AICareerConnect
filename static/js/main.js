/**
 * AICareerConnect — Global JavaScript
 * Shared utilities loaded on every page.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss flash messages after 5 seconds
    document.querySelectorAll('.flash').forEach(el => {
        setTimeout(() => el.style.display = 'none', 5000);
    });
});
