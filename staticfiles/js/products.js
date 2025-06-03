// Sample product data with Arabic content
const products = [
  {
    id: 1,
    name: "قميص قطني كلاسيكي",
    category: "رجالي",
    categoryEn: "men",
    price: 450,
    oldPrice: 600,
    image: "https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: "جديد",
    description: "قميص كلاسيكي من القطن المصري الفاخر، مناسب لجميع المناسبات الرسمية وغير الرسمية."
  },
  {
    id: 2,
    name: "بنطلون كتان أنيق",
    category: "رجالي",
    categoryEn: "men",
    price: 550,
    oldPrice: null,
    image: "https://images.pexels.com/photos/6764007/pexels-photo-6764007.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: null,
    description: "بنطلون كتان عالي الجودة بقصة مريحة ولون عصري، مثالي للمناسبات المختلفة."
  },
  {
    id: 3,
    name: "فستان مزخرف",
    category: "نسائي",
    categoryEn: "women",
    price: 750,
    oldPrice: 950,
    image: "https://images.pexels.com/photos/6952033/pexels-photo-6952033.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: "خصم",
    description: "فستان أنيق مزخرف بتطريزات مستوحاة من الفن المصري، مناسب للمناسبات الخاصة."
  },
  {
    id: 4,
    name: "بلوزة نسائية كاجوال",
    category: "نسائي",
    categoryEn: "women",
    price: 320,
    oldPrice: null,
    image: "https://images.pexels.com/photos/6311475/pexels-photo-6311475.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: null,
    description: "بلوزة نسائية عصرية بخامة مريحة وتصميم أنيق، مثالية للإطلالة اليومية."
  },
  {
    id: 5,
    name: "تيشيرت أطفال قطني",
    category: "أطفال",
    categoryEn: "kids",
    price: 180,
    oldPrice: 220,
    image: "https://images.pexels.com/photos/4144038/pexels-photo-4144038.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: "خصم",
    description: "تيشيرت أطفال من القطن المصري الناعم، مريح وعملي للاستخدام اليومي."
  },
  {
    id: 6,
    name: "بنطلون جينز أطفال",
    category: "أطفال",
    categoryEn: "kids",
    price: 280,
    oldPrice: null,
    image: "https://images.pexels.com/photos/8365688/pexels-photo-8365688.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: "جديد",
    description: "بنطلون جينز للأطفال بقصة مريحة وخامة متينة، مثالي للارتداء اليومي."
  },
  {
    id: 7,
    name: "حقيبة يد جلدية",
    category: "نسائي",
    categoryEn: "women",
    price: 850,
    oldPrice: 1200,
    image: "https://images.pexels.com/photos/6046183/pexels-photo-6046183.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: "خصم",
    description: "حقيبة يد نسائية من الجلد الطبيعي بتصميم عصري وحجم مناسب."
  },
  {
    id: 8,
    name: "معطف رجالي شتوي",
    category: "رجالي",
    categoryEn: "men",
    price: 1200,
    oldPrice: null,
    image: "https://images.pexels.com/photos/1124468/pexels-photo-1124468.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
    badge: "حصري",
    description: "معطف شتوي أنيق للرجال بخامة دافئة وتصميم عصري، مثالي لفصل الشتاء."
  }
];

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