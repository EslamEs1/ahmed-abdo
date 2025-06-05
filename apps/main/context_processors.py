from .models import Slider

def sliders(request):
    """
    Context processor to make sliders available in templates.
    Detects the current page and provides relevant sliders.
    """
    # Determine the current page based on URL path
    path = request.path.strip('/')
    
    # Map URL paths to slider page types
    page_mapping = {
        '': 'home',  # Root URL maps to home
        'men': 'men',
        'women': 'women',
        'kids': 'kids',
        'collections': 'collection',
        'offers': 'offers'
    }
    
    # Get the current page type or default to home
    current_page = 'home'
    for url_path, page_type in page_mapping.items():
        if path.startswith(url_path):
            current_page = page_type
            break
    
    # Get active sliders for the current page, ordered by their defined order
    page_sliders = Slider.objects.filter(page=current_page, is_active=True).order_by('order')
    
    return {
        'sliders': page_sliders,
    } 