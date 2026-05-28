(function () {
  const html = document.documentElement;
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) html.setAttribute('data-theme', savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      toast('Тема переключена');
    });
  }

  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    let timer;
    searchInput.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        if (searchInput.value.length < 2) return;
        fetch('/catalog/search/?term=' + encodeURIComponent(searchInput.value))
          .then((r) => r.json())
          .then((data) => {
            const first = data.results && data.results[0];
            if (first) searchInput.setAttribute('title', 'Подсказка: ' + first.title);
          })
          .catch(() => {});
      }, 300);
    });
  }

  const filterForm = document.getElementById('catalogFilterForm');
  if (filterForm) {
    filterForm.addEventListener('change', function (e) {
      if (e.target.id === 'categorySelect') filterForm.submit();
    });
  }

  document.querySelectorAll('img').forEach((img) => {
    img.addEventListener('error', () => {
      img.src = '/static/img/banner_img_03.jpg';
    });
  });

  const numbersOnly = document.querySelectorAll('input[name="year"]');
  numbersOnly.forEach((input) => {
    input.addEventListener('input', () => {
      input.value = input.value.replace(/[^\d]/g, '').slice(0, 4);
    });
  });

  const cards = document.querySelectorAll('.product-card');
  cards.forEach((card, index) => {
    card.style.animation = `fadeUp .4s ease ${index * 0.04}s both`;
  });

  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    const hero = document.querySelector('.hero-block');
    if (hero) hero.style.transform = `translateY(${Math.min(y * 0.05, 18)}px)`;
  });

  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', (e) => {
      const requiredInputs = form.querySelectorAll('input[required], textarea[required]');
      let valid = true;
      requiredInputs.forEach((el) => {
        if (!el.value.trim()) {
          valid = false;
          el.classList.add('is-invalid');
        }
      });
      if (!valid) {
        e.preventDefault();
        toast('Заполните обязательные поля');
      }
    });
  });

  function toast(message) {
    let node = document.querySelector('.toast-lite');
    if (!node) {
      node = document.createElement('div');
      node.className = 'toast-lite';
      document.body.appendChild(node);
    }
    node.textContent = message;
    node.classList.add('show');
    setTimeout(() => node.classList.remove('show'), 1500);
  }

  window.toast = toast;
})();
