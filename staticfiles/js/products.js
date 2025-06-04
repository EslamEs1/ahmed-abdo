

// Function to render products
function renderProducts(container, productsList) {
  const productsContainer = document.querySelector(container);
  if (!productsContainer) return;
  
  let productsHTML = '';
  
  productsList.forEach(product => {
    productsHTML += `
      <div class="col-6 col-md-4 col-lg-3">
        <div class="product-card">
          ${product.badge ? `<div class="product-badge">${product.badge}</div>` : ''}
          <div class="product-img-container">
            <img src="${product.image}" alt="${product.name}" class="product-img">
            <div class="product-actions">
              <button class="action-btn quick-view-btn" data-id="${product.id}">
                <i class="bi bi-eye"></i>
              </button>
              <button class="action-btn">
                <i class="bi bi-heart"></i>
              </button>
              <button class="action-btn">
                <i class="bi bi-bag-plus"></i>
              </button>
            </div>
          </div>
          <div class="product-info">
            <div class="product-category">${product.category}</div>
            <h3 class="product-title">
              <a href="#" class="product-link">${product.name}</a>
            </h3>
            <div class="product-price">
              <span class="current-price">${product.price} ج.م</span>
              ${product.oldPrice ? `<span class="old-price">${product.oldPrice} ج.م</span>` : ''}
            </div>
          </div>
        </div>
      </div>
    `;
  });
  
  productsContainer.innerHTML = productsHTML;
  
  // Add event listeners to quick view buttons
  document.querySelectorAll('.quick-view-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      const productId = parseInt(this.getAttribute('data-id'));
      openQuickViewModal(productId);
    });
  });
}

// Function to open quick view modal
function openQuickViewModal(productId) {
  const product = products.find(p => p.id === productId);
  if (!product) return;
  
  // Set modal content
  document.getElementById('modalProductName').textContent = product.name;
  document.getElementById('modalProductImage').src = product.image;
  document.getElementById('modalProductImage').alt = product.name;
  document.getElementById('modalProductPrice').textContent = `${product.price} ج.م`;
  
  if (product.oldPrice) {
    document.getElementById('modalProductOldPrice').textContent = `${product.oldPrice} ج.م`;
    document.getElementById('modalProductOldPrice').style.display = 'inline';
  } else {
    document.getElementById('modalProductOldPrice').style.display = 'none';
  }
  
  document.getElementById('modalProductDescription').textContent = product.description;
  
  // Open modal
  const quickViewModal = new bootstrap.Modal(document.getElementById('quickViewModal'));
  quickViewModal.show();
}

// Filter products by category
function filterProducts(category) {
  if (category === 'all') {
    return products;
  } else {
    return products.filter(product => product.categoryEn === category);
  }
}

// Initialize tabs functionality
function initProductTabs() {
  document.querySelectorAll('#productTabs .nav-link').forEach(tab => {
    tab.addEventListener('click', function() {
      const category = this.getAttribute('data-bs-target').replace('#', '');
      const filteredProducts = filterProducts(category);
      renderProducts(`#${category} .row`, filteredProducts);
    });
  });
}

// Export functions for use in main.js
window.appProducts = {
  products,
  renderProducts,
  filterProducts,
  initProductTabs
};