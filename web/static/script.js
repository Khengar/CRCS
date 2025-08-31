document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('result-modal');
    const closeBtn = document.getElementById('modal-close-btn');

    // Check if the modal has the 'data-show' attribute
    if (modal && modal.dataset.show === 'true') {
        showModal();
    }

    function showModal() {
        modal.classList.add('active');
    }

    function hideModal() {
        modal.classList.remove('active');
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', hideModal);
    }

    if (modal) {
        modal.addEventListener('click', function(event) {
            // Close the modal if the overlay (the dark background) is clicked
            if (event.target === modal) {
                hideModal();
            }
        });
    }
});