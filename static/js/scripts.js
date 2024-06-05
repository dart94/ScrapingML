document.addEventListener('DOMContentLoaded', function () {
    // Validación de formularios
    const searchForm = document.querySelector('form');
    const searchInput = document.getElementById('palabra');
    const spinner = document.getElementById('spinner');
    const alertContainer = document.createElement('div');

    if (searchForm) {
        searchForm.prepend(alertContainer);

        searchForm.addEventListener('submit', function (event) {
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
                spinner.style.display = 'block';
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

    // Mensaje de carga
    searchForm.addEventListener('submit', function () {
        const loadingMessage = document.createElement('p');
        loadingMessage.textContent = 'Buscando productos...';
        loadingMessage.style.textAlign = 'center';
        loadingMessage.style.fontWeight = 'bold';
        searchForm.append(loadingMessage);
    });
});
