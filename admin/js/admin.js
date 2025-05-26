// Admin Dashboard Scripts
document.addEventListener('DOMContentLoaded', function() {
  // Sidebar Toggle
  const sidebarToggle = document.querySelector('.sidebar-toggle');
  const sidebar = document.querySelector('.admin-sidebar');

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('show');
    });

    // Close sidebar when clicking outside
    document.addEventListener('click', function(event) {
      const isClickInside = sidebar.contains(event.target) || sidebarToggle.contains(event.target);
      
      if (!isClickInside && sidebar.classList.contains('show')) {
        sidebar.classList.remove('show');
      }
    });
  }

  // Responsive Tables
  const tables = document.querySelectorAll('.table-responsive');
  tables.forEach(table => {
    const headerCells = table.querySelectorAll('th');
    const dataCells = table.querySelectorAll('td');
    
    headerCells.forEach((cell, index) => {
      const label = cell.textContent;
      dataCells.forEach((dataCell, dataIndex) => {
        if (dataIndex % headerCells.length === index) {
          dataCell.setAttribute('data-label', label);
        }
      });
    });
  });

  // Dropdowns
  const dropdowns = document.querySelectorAll('.dropdown-toggle');
  dropdowns.forEach(dropdown => {
    dropdown.addEventListener('click', function(event) {
      event.stopPropagation();
      const dropdownMenu = this.nextElementSibling;
      dropdownMenu.classList.toggle('show');

      // Close other dropdowns
      dropdowns.forEach(other => {
        if (other !== this) {
          other.nextElementSibling.classList.remove('show');
        }
      });
    });
  });

  // Close dropdowns when clicking outside
  document.addEventListener('click', function() {
    dropdowns.forEach(dropdown => {
      dropdown.nextElementSibling.classList.remove('show');
    });
  });

  // Form Validation
  const forms = document.querySelectorAll('.needs-validation');
  forms.forEach(form => {
    form.addEventListener('submit', function(event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    });
  });
}); 