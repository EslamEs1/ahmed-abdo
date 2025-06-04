// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
  // Initialize header scroll effect
  initHeaderScroll();
  
  // Initialize quantity selectors in modal
  initQuantitySelectors();
  
  // Initialize RTL-specific features
  initRTLFeatures();

  // Search Form Handler
  const searchForm = document.getElementById('searchForm');
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const searchInput = this.querySelector('input[type="search"]');
      const searchTerm = searchInput.value.trim();
      
      if (searchTerm) {
        // You can customize this to your search results page
        window.location.href = `search.html?q=${encodeURIComponent(searchTerm)}`;
      }
    });
  }
});

// Header scroll effect
function initHeaderScroll() {
  const header = document.getElementById('main-header');
  if (!header) return;

  window.addEventListener('scroll', function() {
    if (window.scrollY > 100) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

// Initialize quantity selectors
function initQuantitySelectors() {
  const decreaseBtn = document.getElementById('decreaseQuantity');
  const increaseBtn = document.getElementById('increaseQuantity');
  const quantityInput = document.querySelector('.quantity-input');
  
  if (decreaseBtn && increaseBtn && quantityInput) {
    decreaseBtn.addEventListener('click', function() {
      let value = parseInt(quantityInput.value);
      if (value > 1) {
        quantityInput.value = value - 1;
      }
    });
    
    increaseBtn.addEventListener('click', function() {
      let value = parseInt(quantityInput.value);
      if (value < 10) {
        quantityInput.value = value + 1;
      }
    });
    
    quantityInput.addEventListener('change', function() {
      let value = parseInt(this.value);
      if (isNaN(value) || value < 1) {
        this.value = 1;
      } else if (value > 10) {
        this.value = 10;
      }
    });
  }
}

// RTL-specific initializations
function initRTLFeatures() {
  // Adjust carousel controls for RTL
  const carousels = document.querySelectorAll('.carousel');
  
  carousels.forEach(carousel => {
    const prevButton = carousel.querySelector('.carousel-control-prev');
    const nextButton = carousel.querySelector('.carousel-control-next');
    
    if (prevButton && nextButton) {
      // Swap the positions of prev and next buttons for RTL
      prevButton.classList.remove('carousel-control-prev');
      prevButton.classList.add('carousel-control-next');
      
      nextButton.classList.remove('carousel-control-next');
      nextButton.classList.add('carousel-control-prev');
      
      // Swap the icons
      const prevIcon = prevButton.querySelector('.carousel-control-prev-icon');
      const nextIcon = nextButton.querySelector('.carousel-control-next-icon');
      
      if (prevIcon) {
        prevIcon.classList.remove('carousel-control-prev-icon');
        prevIcon.classList.add('carousel-control-next-icon');
      }
      
      if (nextIcon) {
        nextIcon.classList.remove('carousel-control-next-icon');
        nextIcon.classList.add('carousel-control-prev-icon');
      }
    }
  });
  
  // Add RTL-specific event listeners or adjustments here if needed
}

// Add to cart functionality
function addToCart(productId, quantity = 1) {
  // This is a placeholder for cart functionality
  // In a real application, you would implement logic to add items to cart
  console.log(`Added product ID ${productId} to cart with quantity ${quantity}`);
  
  // Show a toast notification
  showNotification('تمت إضافة المنتج إلى سلة التسوق');
}

// Wishlist functionality
function addToWishlist(productId) {
  // This is a placeholder for wishlist functionality
  console.log(`Added product ID ${productId} to wishlist`);
  
  // Show a toast notification
  showNotification('تمت إضافة المنتج إلى المفضلة');
}

// Show notification toast
function showNotification(message) {
  // Create toast element
  const toast = document.createElement('div');
  toast.className = 'notification-toast';
  toast.innerText = message;
  
  // Append to body
  document.body.appendChild(toast);
  
  // Show toast
  setTimeout(() => {
    toast.classList.add('show');
  }, 100);
  
  // Hide and remove toast after 3 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

// Add floating label effect to forms
function initFloatingLabels() {
  const formControls = document.querySelectorAll('.form-control');
  
  formControls.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('focused');
    });
    
    input.addEventListener('blur', function() {
      if (this.value === '') {
        this.parentElement.classList.remove('focused');
      }
    });
    
    // Check initial state
    if (input.value !== '') {
      input.parentElement.classList.add('focused');
    }
  });
}

// Handle search functionality
function initSearch() {
  const searchIcon = document.querySelector('.nav-icon .bi-search');
  if (!searchIcon) return;
  
  searchIcon.addEventListener('click', function(e) {
    e.preventDefault();
    
    // Create search overlay
    const searchOverlay = document.createElement('div');
    searchOverlay.className = 'search-overlay';
    searchOverlay.innerHTML = `
      <div class="search-modal">
        <button class="search-close"><i class="bi bi-x-lg"></i></button>
        <div class="search-form">
          <h3>البحث في المتجر</h3>
          <form>
            <div class="input-group">
              <input type="text" class="form-control" placeholder="ابحث عن منتجات...">
              <button class="btn btn-primary" type="submit"><i class="bi bi-search"></i></button>
            </div>
          </form>
        </div>
      </div>
    `;
    
    document.body.appendChild(searchOverlay);
    
    // Show overlay with animation
    setTimeout(() => {
      searchOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }, 10);
    
    // Focus on search input
    setTimeout(() => {
      searchOverlay.querySelector('input').focus();
    }, 300);
    
    // Close button functionality
    searchOverlay.querySelector('.search-close').addEventListener('click', function() {
      searchOverlay.classList.remove('active');
      document.body.style.overflow = '';
      
      // Remove overlay after animation
      setTimeout(() => {
        document.body.removeChild(searchOverlay);
      }, 300);
    });
  });
}