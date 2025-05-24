// Payment Screenshot Upload Handling
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('paymentScreenshot');
    const previewArea = document.getElementById('previewArea');
    const screenshotPreview = document.getElementById('screenshotPreview');
    const removeButton = document.getElementById('removeScreenshot');

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        uploadArea.classList.add('border-primary');
    }

    function unhighlight(e) {
        uploadArea.classList.remove('border-primary');
    }

    // Handle dropped files
    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // Handle file input change
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            
            // Validate file type
            if (!file.type.match('image.*')) {
                showError('الرجاء اختيار صورة صالحة');
                return;
            }

            // Validate file size (5MB max)
            if (file.size > 5 * 1024 * 1024) {
                showError('حجم الصورة يجب أن يكون أقل من 5 ميجابايت');
                return;
            }

            // Preview image
            const reader = new FileReader();
            reader.onload = function(e) {
                screenshotPreview.src = e.target.result;
                previewArea.classList.remove('d-none');
                uploadArea.classList.add('d-none');
            }
            reader.readAsDataURL(file);
        }
    }

    // Remove screenshot
    removeButton.addEventListener('click', function() {
        fileInput.value = '';
        previewArea.classList.add('d-none');
        uploadArea.classList.remove('d-none');
    });

    // Show error message
    function showError(message) {
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger alert-dismissible fade show mt-2';
        errorAlert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        uploadArea.parentNode.insertBefore(errorAlert, uploadArea.nextSibling);
    }
}); 