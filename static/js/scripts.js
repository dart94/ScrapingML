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

    eventListeners();

    darkMode();
});

function darkMode() {
    const prefiereDarkMode = window.matchMedia('(prefers-color-scheme: dark)');

    // console.log(prefiereDarkMode.matches);

    if (prefiereDarkMode.matches) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }

    prefiereDarkMode.addEventListener('change', function () {
        if (prefiereDarkMode.matches) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }

    });
    const botonDarkMode = document.querySelector('.dark-mode-boton');
    botonDarkMode.addEventListener('click', function () {
        document.body.classList.toggle('dark-mode');

        // Guardar el estado del modo oscuro en localStorage
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });
}