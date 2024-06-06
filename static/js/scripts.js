document.addEventListener('DOMContentLoaded', function () {
    // Validación de formularios
    const searchForm = document.querySelector('form');
    const searchInput = document.getElementById('palabra');
    const alertContainer = document.createElement('div');

    if (searchForm) {
        searchForm.prepend(alertContainer);

        searchForm.addEventListener('submit', function (event) {
            // Eliminar el mensaje de carga si existe
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }

            if (searchInput.value.trim() === '') {
                event.preventDefault();
                alertContainer.innerHTML = `
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Por favor, ingrese un producto para buscar.
                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                `;
            } else {
                // Mostrar mensaje de carga
                const loadingMessage = document.createElement('p');
                loadingMessage.textContent = 'Buscando productos...';
                loadingMessage.style.textAlign = 'center';
                loadingMessage.style.fontWeight = 'bold';
                loadingMessage.setAttribute('id', 'loading-message'); // Agrega un ID para eliminarlo más tarde
                searchForm.append(loadingMessage);
            }
        });
    }

    // Animación de tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseover', function () {
            this.style.transform = 'scale(1.05)';
        });
        card.addEventListener('mouseout', function () {
            this.style.transform = 'scale(1)';
        });
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;

    // Función para aplicar el tema basado en la preferencia del usuario o del sistema
    function applyTheme(theme) {
        if (theme === 'dark') {
            body.classList.add('dark-theme');
        } else {
            body.classList.remove('dark-theme');
        }
    }

    // Detectar y aplicar el tema al cargar la página
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        applyTheme('dark');
    }

    // Evento para el botón de alternancia de tema
    toggleButton.addEventListener('click', function () {
        if (body.classList.contains('dark-theme')) {
            applyTheme('light');
            localStorage.setItem('theme', 'light');
        } else {
            applyTheme('dark');
            localStorage.setItem('theme', 'dark');
        }
    });

    // Escuchar los cambios en la preferencia del sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) { // Solo aplicar si el usuario no ha seleccionado un tema
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
});