document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.getElementById('sidebar');
    const collapseBtn = document.getElementById('sidebarCollapse');
    const closeBtn = document.getElementById('sidebarClose');

    if (collapseBtn && sidebar) {
        collapseBtn.addEventListener('click', function () {
            sidebar.classList.toggle('active');
        });
    }

    if (closeBtn && sidebar) {
        closeBtn.addEventListener('click', function () {
            sidebar.classList.add('active');
        });
    }
});
