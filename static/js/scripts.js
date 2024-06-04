document.addEventListener('DOMContentLoaded', function () {
    // Validación de formularios
    const searchForm = document.querySelector('form');
    const searchInput = document.getElementById('palabra');

    searchForm.addEventListener('submit', function (event) {
        if (searchInput.value.trim() === '') {
            event.preventDefault();
            alert('Por favor, ingrese un producto para buscar.');
        }
    });

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


document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('search-form');
    const loader = document.getElementById('loader');

    if (searchForm) {
        searchForm.addEventListener('submit', function () {
            loader.style.display = 'block';
        });
    }
});
