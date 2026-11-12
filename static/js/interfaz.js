document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-action="print"]').forEach(function (button) {
        button.addEventListener('click', function () { window.print(); });
    });
    var menu = document.getElementById('menuPrincipal');
    if (menu) {
        menu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                if (window.innerWidth < 992 && window.bootstrap && window.bootstrap.Collapse && menu.classList.contains('show')) {
                    window.bootstrap.Collapse.getOrCreateInstance(menu).hide();
                }
            });
        });
    }
});
