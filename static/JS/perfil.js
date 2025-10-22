document.addEventListener('DOMContentLoaded', function () {
  const profileBtn = document.getElementById('profileMenuBtn');
  const dropdown = document.getElementById('profileDropdown');

  if (profileBtn && dropdown) {
    profileBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      dropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', function (e) {
      if (!profileBtn.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.add('hidden');
      }
    });
  }
});
