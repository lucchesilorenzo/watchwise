document.addEventListener('DOMContentLoaded', function() {
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

  function resetStars() {
    document.querySelectorAll('.rating-stars .star').forEach(function(star) {
      star.classList.remove('rated');
    });
  }

  function updateStars(starsContainer, ratingValue) {
    resetStars();
    starsContainer.querySelectorAll('.star').forEach(function(star) {
      if (parseInt(star.getAttribute('data-value')) <= ratingValue) {
        star.classList.add('rated');
      }
    });
  }

  document.querySelectorAll('.rating-stars').forEach(function(starsContainer) {
    starsContainer.querySelectorAll('.star').forEach(function(star) {
      star.addEventListener('click', function() {
        const ratingValue = parseInt(this.getAttribute('data-value'));
        const form = starsContainer.closest('form');
        form.querySelector('input[name="rating"]').value = ratingValue;

        updateStars(starsContainer, ratingValue);
      });
    });
  });
});