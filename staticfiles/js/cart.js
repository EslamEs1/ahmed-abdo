// Cart and Favorites Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize cart and favorites
    initCart();
    initFavorites();
    setupProductButtons();
});

// Cart functionality
function initCart() {
    // Load cart from localStorage
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    updateCartCount(cart.length);
    
    // Setup cart buttons
    const mobileCartBtn = document.getElementById('mobile-cart-btn');
    const desktopCartBtn = document.getElementById('desktop-cart-btn');
    
    if (mobileCartBtn) {
        mobileCartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showCart();
        });
    }
    
    if (desktopCartBtn) {
        desktopCartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showCart();
        });
    }
}

// Update cart count in the UI
function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(element => {
        element.textContent = count;
    });
}

// Add item to cart
function addToCart(productId, productName, productPrice, productImage) {
    // Get current cart
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Check if product already in cart
    const existingItemIndex = cart.findIndex(item => item.id === productId);
    
    if (existingItemIndex !== -1) {
        // Increment quantity if already in cart
        cart[existingItemIndex].quantity += 1;
    } else {
        // Add new item
        cart.push({
            id: productId,
            name: productName,
            price: productPrice,
            image: productImage,
            quantity: 1
        });
    }
    
    // Save to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Update cart count
    updateCartCount(cart.length);
    
    // Show notification
    showNotification('تمت إضافة المنتج إلى سلة التسوق');
}

// Show cart modal
function showCart() {
    // Get cart items
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    // Create cart modal HTML
    let cartHTML = `
    <div class="cart-modal-overlay">
        <div class="cart-modal">
            <div class="cart-header">
                <h3>سلة التسوق</h3>
                <button class="close-btn"><i class="bi bi-x-lg"></i></button>
            </div>
            <div class="cart-body">
    `;
    
    if (cart.length === 0) {
        cartHTML += `
            <div class="empty-cart">
                <i class="bi bi-cart-x"></i>
                <p>سلة التسوق فارغة</p>
                <a href="/" class="btn btn-primary">تسوق الآن</a>
            </div>
        `;
    } else {
        cartHTML += `<div class="cart-items">`;
        
        let totalPrice = 0;
        
        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            totalPrice += itemTotal;
            
            cartHTML += `
                <div class="cart-item" data-id="${item.id}">
                    <div class="item-image">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div class="item-details">
                        <h4>${item.name}</h4>
                        <div class="item-price">${item.price} ج.م</div>
                        <div class="item-quantity">
                            <button class="quantity-btn decrease-btn">-</button>
                            <span class="quantity">${item.quantity}</span>
                            <button class="quantity-btn increase-btn">+</button>
                        </div>
                    </div>
                    <button class="remove-btn"><i class="bi bi-trash"></i></button>
                </div>
            `;
        });
        
        cartHTML += `</div>
            <div class="cart-footer">
                <div class="cart-total">
                    <span>الإجمالي:</span>
                    <span class="total-price">${totalPrice} ج.م</span>
                </div>
                <a href="/cart/checkout/" class="btn btn-primary checkout-btn">إتمام الطلب</a>
                <a href="/cart/" class="btn btn-outline-secondary view-cart-btn">عرض السلة</a>
                <button class="btn btn-outline-secondary continue-shopping-btn">مواصلة التسوق</button>
            </div>
        `;
    }
    
    cartHTML += `
            </div>
        </div>
    </div>
    `;
    
    // Add cart modal to the page
    const cartModalElement = document.createElement('div');
    cartModalElement.innerHTML = cartHTML;
    document.body.appendChild(cartModalElement.firstElementChild);
    
    // Show with animation
    setTimeout(() => {
        document.querySelector('.cart-modal-overlay').classList.add('active');
    }, 10);
    
    // Setup close button
    document.querySelector('.cart-modal .close-btn').addEventListener('click', closeCartModal);
    document.querySelector('.cart-modal-overlay').addEventListener('click', function(e) {
        if (e.target === this) {
            closeCartModal();
        }
    });
    
    // Setup continue shopping button
    const continueShoppingBtn = document.querySelector('.continue-shopping-btn');
    if (continueShoppingBtn) {
        continueShoppingBtn.addEventListener('click', closeCartModal);
    }
    
    // Setup quantity buttons
    setupCartQuantityButtons();
    
    // Setup remove buttons
    setupCartRemoveButtons();
    
    // Prevent body scrolling
    document.body.style.overflow = 'hidden';
}

// Close cart modal
function closeCartModal() {
    const cartModal = document.querySelector('.cart-modal-overlay');
    cartModal.classList.remove('active');
    
    // Remove modal after animation
    setTimeout(() => {
        document.body.removeChild(cartModal);
    }, 300);
    
    // Restore body scrolling
    document.body.style.overflow = '';
}

// Setup cart quantity buttons
function setupCartQuantityButtons() {
    // Increase quantity
    document.querySelectorAll('.increase-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const cartItem = this.closest('.cart-item');
            const productId = cartItem.dataset.id;
            const quantityElement = cartItem.querySelector('.quantity');
            
            let cart = JSON.parse(localStorage.getItem('cart')) || [];
            const itemIndex = cart.findIndex(item => item.id === productId);
            
            if (itemIndex !== -1) {
                cart[itemIndex].quantity += 1;
                quantityElement.textContent = cart[itemIndex].quantity;
                
                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartTotal();
            }
        });
    });
    
    // Decrease quantity
    document.querySelectorAll('.decrease-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const cartItem = this.closest('.cart-item');
            const productId = cartItem.dataset.id;
            const quantityElement = cartItem.querySelector('.quantity');
            
            let cart = JSON.parse(localStorage.getItem('cart')) || [];
            const itemIndex = cart.findIndex(item => item.id === productId);
            
            if (itemIndex !== -1 && cart[itemIndex].quantity > 1) {
                cart[itemIndex].quantity -= 1;
                quantityElement.textContent = cart[itemIndex].quantity;
                
                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartTotal();
            }
        });
    });
}

// Setup cart remove buttons
function setupCartRemoveButtons() {
    document.querySelectorAll('.remove-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const cartItem = this.closest('.cart-item');
            const productId = cartItem.dataset.id;
            
            let cart = JSON.parse(localStorage.getItem('cart')) || [];
            cart = cart.filter(item => item.id !== productId);
            
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartCount(cart.length);
            
            // Remove item from UI
            cartItem.remove();
            
            // Update total
            updateCartTotal();
            
            // Check if cart is empty
            if (cart.length === 0) {
                const cartBody = document.querySelector('.cart-body');
                cartBody.innerHTML = `
                    <div class="empty-cart">
                        <i class="bi bi-cart-x"></i>
                        <p>سلة التسوق فارغة</p>
                        <a href="/" class="btn btn-primary">تسوق الآن</a>
                    </div>
                `;
            }
        });
    });
}

// Update cart total
function updateCartTotal() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const totalElement = document.querySelector('.total-price');
    
    if (totalElement) {
        let total = 0;
        cart.forEach(item => {
            total += item.price * item.quantity;
        });
        
        totalElement.textContent = `${total} ج.م`;
    }
}

// Favorites functionality
function initFavorites() {
    // Load favorites from localStorage
    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    updateFavoritesCount(favorites.length);
    
    // Setup favorites buttons
    const mobileFavoritesBtn = document.getElementById('mobile-favorites-btn');
    const desktopFavoritesBtn = document.getElementById('desktop-favorites-btn');
    
    if (mobileFavoritesBtn) {
        mobileFavoritesBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showFavorites();
        });
    }
    
    if (desktopFavoritesBtn) {
        desktopFavoritesBtn.addEventListener('click', function(e) {
            e.preventDefault();
            showFavorites();
        });
    }
}

// Update favorites count in the UI
function updateFavoritesCount(count) {
    const favoritesCountElements = document.querySelectorAll('.favorites-count');
    favoritesCountElements.forEach(element => {
        element.textContent = count;
    });
}

// Add item to favorites
function addToFavorites(productId, productName, productPrice, productImage) {
    // Get current favorites
    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    
    // Check if product already in favorites
    const existingItemIndex = favorites.findIndex(item => item.id === productId);
    
    if (existingItemIndex !== -1) {
        // Remove from favorites if already there
        favorites = favorites.filter(item => item.id !== productId);
        showNotification('تم إزالة المنتج من المفضلة');
    } else {
        // Add to favorites
        favorites.push({
            id: productId,
            name: productName,
            price: productPrice,
            image: productImage
        });
        showNotification('تمت إضافة المنتج إلى المفضلة');
    }
    
    // Save to localStorage
    localStorage.setItem('favorites', JSON.stringify(favorites));
    
    // Update favorites count
    updateFavoritesCount(favorites.length);
}

// Show favorites modal
function showFavorites() {
    // Get favorites items
    const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    
    // Create favorites modal HTML
    let favoritesHTML = `
    <div class="favorites-modal-overlay">
        <div class="favorites-modal">
            <div class="favorites-header">
                <h3>المفضلة</h3>
                <button class="close-btn"><i class="bi bi-x-lg"></i></button>
            </div>
            <div class="favorites-body">
    `;
    
    if (favorites.length === 0) {
        favoritesHTML += `
            <div class="empty-favorites">
                <i class="bi bi-heart"></i>
                <p>لا توجد منتجات في المفضلة</p>
                <a href="/" class="btn btn-primary">تسوق الآن</a>
            </div>
        `;
    } else {
        favoritesHTML += `<div class="favorites-items">`;
        
        favorites.forEach(item => {
            favoritesHTML += `
                <div class="favorites-item" data-id="${item.id}">
                    <div class="item-image">
                        <img src="${item.image}" alt="${item.name}">
                    </div>
                    <div class="item-details">
                        <h4>${item.name}</h4>
                        <div class="item-price">${item.price} ج.م</div>
                        <button class="btn btn-primary add-to-cart-btn">أضف إلى السلة</button>
                    </div>
                    <button class="remove-btn"><i class="bi bi-trash"></i></button>
                </div>
            `;
        });
        
        favoritesHTML += `</div>`;
    }
    
    favoritesHTML += `
            </div>
            <div class="favorites-footer">
                <button class="btn btn-outline-secondary continue-shopping-btn">مواصلة التسوق</button>
            </div>
        </div>
    </div>
    `;
    
    // Add favorites modal to the page
    const favoritesModalElement = document.createElement('div');
    favoritesModalElement.innerHTML = favoritesHTML;
    document.body.appendChild(favoritesModalElement.firstElementChild);
    
    // Show with animation
    setTimeout(() => {
        document.querySelector('.favorites-modal-overlay').classList.add('active');
    }, 10);
    
    // Setup close button
    document.querySelector('.favorites-modal .close-btn').addEventListener('click', closeFavoritesModal);
    document.querySelector('.favorites-modal-overlay').addEventListener('click', function(e) {
        if (e.target === this) {
            closeFavoritesModal();
        }
    });
    
    // Setup continue shopping button
    const continueShoppingBtn = document.querySelector('.favorites-modal .continue-shopping-btn');
    if (continueShoppingBtn) {
        continueShoppingBtn.addEventListener('click', closeFavoritesModal);
    }
    
    // Setup remove buttons
    setupFavoritesRemoveButtons();
    
    // Setup add to cart buttons
    setupFavoritesAddToCartButtons();
    
    // Prevent body scrolling
    document.body.style.overflow = 'hidden';
}

// Close favorites modal
function closeFavoritesModal() {
    const favoritesModal = document.querySelector('.favorites-modal-overlay');
    favoritesModal.classList.remove('active');
    
    // Remove modal after animation
    setTimeout(() => {
        document.body.removeChild(favoritesModal);
    }, 300);
    
    // Restore body scrolling
    document.body.style.overflow = '';
}

// Setup favorites remove buttons
function setupFavoritesRemoveButtons() {
    document.querySelectorAll('.favorites-item .remove-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const favoritesItem = this.closest('.favorites-item');
            const productId = favoritesItem.dataset.id;
            
            let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
            favorites = favorites.filter(item => item.id !== productId);
            
            localStorage.setItem('favorites', JSON.stringify(favorites));
            updateFavoritesCount(favorites.length);
            
            // Remove item from UI
            favoritesItem.remove();
            
            // Check if favorites is empty
            if (favorites.length === 0) {
                const favoritesBody = document.querySelector('.favorites-body');
                favoritesBody.innerHTML = `
                    <div class="empty-favorites">
                        <i class="bi bi-heart"></i>
                        <p>لا توجد منتجات في المفضلة</p>
                        <a href="/" class="btn btn-primary">تسوق الآن</a>
                    </div>
                `;
            }
            
            showNotification('تم إزالة المنتج من المفضلة');
        });
    });
}

// Setup favorites add to cart buttons
function setupFavoritesAddToCartButtons() {
    document.querySelectorAll('.favorites-item .add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const favoritesItem = this.closest('.favorites-item');
            const productId = favoritesItem.dataset.id;
            
            let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
            const product = favorites.find(item => item.id === productId);
            
            if (product) {
                addToCart(product.id, product.name, product.price, product.image);
            }
        });
    });
}

// Setup product buttons (Add to cart and Add to favorites)
function setupProductButtons() {
    // Add to cart buttons
    document.querySelectorAll('.action-btn:nth-child(3)').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productCard = this.closest('.product-card');
            if (!productCard) return;
            
            const productId = productCard.dataset.id || 'product-' + Math.random().toString(36).substr(2, 9);
            const productName = productCard.querySelector('.product-title a').textContent;
            const productPrice = parseFloat(productCard.querySelector('.current-price').textContent);
            const productImage = productCard.querySelector('.product-img').src;
            
            addToCart(productId, productName, productPrice, productImage);
        });
    });
    
    // Add to favorites buttons
    document.querySelectorAll('.action-btn:nth-child(2)').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productCard = this.closest('.product-card');
            if (!productCard) return;
            
            const productId = productCard.dataset.id || 'product-' + Math.random().toString(36).substr(2, 9);
            const productName = productCard.querySelector('.product-title a').textContent;
            const productPrice = parseFloat(productCard.querySelector('.current-price').textContent);
            const productImage = productCard.querySelector('.product-img').src;
            
            addToFavorites(productId, productName, productPrice, productImage);
            
            // Toggle heart icon fill
            const heartIcon = this.querySelector('i');
            if (heartIcon.classList.contains('bi-heart')) {
                heartIcon.classList.remove('bi-heart');
                heartIcon.classList.add('bi-heart-fill');
            } else {
                heartIcon.classList.remove('bi-heart-fill');
                heartIcon.classList.add('bi-heart');
            }
        });
    });
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