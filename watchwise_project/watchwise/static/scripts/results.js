document.addEventListener('DOMContentLoaded', function() {
  // Gestisce l'espansione e la compressione delle descrizioni "More/Less"
  document.querySelectorAll('.overview-wrapper').forEach(function(wrapper) {
    const overview = wrapper.querySelector('.overview');
    const originalText = overview.textContent;
    const moreTextSpan = document.createElement('span');
    moreTextSpan.className = 'overview-more';
    moreTextSpan.textContent = 'More...';
    moreTextSpan.style.display = 'none';

    wrapper.after(moreTextSpan);

    if (originalText.length > 100) {
      overview.textContent = originalText.substring(0, 100) + '...';
      moreTextSpan.style.display = 'inline';

      moreTextSpan.addEventListener('click', function() {
        const isExpanded = wrapper.classList.toggle('expanded');
        if (isExpanded) {
          overview.textContent = originalText;
          moreTextSpan.textContent = 'Less...';
        } else {
          overview.textContent = originalText.substring(0, 100) + '...';
          moreTextSpan.textContent = 'More...';
        }
      });
    }
  });

  // Funzione per resettare tutte le stelle a non selezionate
  function resetStars() {
    document.querySelectorAll('.rating-stars .star').forEach(function(star) {
      star.classList.remove('rated');
    });
  }

  // Funzione per aggiornare le stelle in base al valore di valutazione nella card corrente
  function updateStars(starsContainer, ratingValue) {
    resetStars(); // Assicurati di resettare le stelle prima di applicare il nuovo rating
    starsContainer.querySelectorAll('.star').forEach(function(star) {
      if (parseInt(star.getAttribute('data-value')) <= ratingValue) {
        star.classList.add('rated');
      }
    });
  }

  // Gestisce la selezione del rating con le stelle per ogni card
  document.querySelectorAll('.rating-stars').forEach(function(starsContainer) {
    starsContainer.querySelectorAll('.star').forEach(function(star) {
      star.addEventListener('click', function() {
        const ratingValue = parseInt(this.getAttribute('data-value'));
        const form = starsContainer.closest('form'); // Trova il form più vicino che contiene le stelle
        form.querySelector('input[name="rating"]').value = ratingValue; // Aggiorna il campo nascosto del form

        updateStars(starsContainer, ratingValue); // Aggiorna solo le stelle nella card corrente
      });
    });
  });
});