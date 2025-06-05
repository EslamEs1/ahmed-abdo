from pathlib import Path
import environ
from django.contrib.messages import constants as messages

env = environ.Env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(str(BASE_DIR / ".env"))


APPS_DIR = BASE_DIR / "apps"

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])


# Application definition

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "jazzmin",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "django_cleanup.apps.CleanupConfig",

]

LOCAL_APPS = [
    # "apps.system",
    "apps.main",
    "apps.order",
    "apps.product",
    "apps.contactus",
    "apps.cart",
    
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.main.context_processors.sliders',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": env("POSTGRES_HOST"),
            "PORT": env("POSTGRES_PORT"),
        }
    }


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = True



STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/staticfiles/"
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]


MEDIA_ROOT = "/home/media/"
MEDIA_URL = "/media/"



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "متجر أحمد عبده",
    "site_logo": "https://example.com/logo.png",  # Replace with your logo URL
    "site_header": "إدارة متجر أحمد عبده",
    "site_brand": "متجر أحمد عبده",
    "welcome_sign": "مرحباً بك في لوحة التحكم",
    "copyright": "تطوير: إسلام",
    "topmenu_links": [
        {"name": "الموقع", "url": "/"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["product", "cart", "order"],
    "custom_css": "css/admin.css",
    "custom_js": None,
    "icons": {
        "product.Category": "fas fa-tags",
        "product.Product": "fas fa-tshirt",
        "product.Collection": "fas fa-layer-group",
        "product.Offer": "fas fa-percent",
        "product.Review": "fas fa-star",
        "cart.Cart": "fas fa-shopping-cart",
        "cart.CartItem": "fas fa-shopping-basket",
        "cart.Coupon": "fas fa-ticket-alt",
        "order.Order": "fas fa-file-invoice",
        "order.OrderItem": "fas fa-box",
        "order.ShippingAddress": "fas fa-map-marker-alt",
        "contactus.ContactMessage": "fas fa-envelope",
        "contactus.ContactInfo": "fas fa-info-circle",
        "contactus.Newsletter": "fas fa-paper-plane",
        "main.Slider": "fas fa-images",
    },
    "related_modal_active": True,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "product.Product": "horizontal_tabs",
        "product.Offer": "horizontal_tabs",
        "product.Collection": "horizontal_tabs",
    },
    "language_chooser": False,
    "search_model": ["product.Product", "product.Category"],
    "show_ui_builder": False
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

MESSAGE_TAGS = {
    messages.DEBUG: "alert",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}


LOGIN_URL = env("LOGIN_URL", default="/login/")
LOGIN_REDIRECT_URL = env("LOGIN_REDIRECT_URL", default="/")

LOGOUT_REDIRECT_URL = env("LOGOUT_REDIRECT_URL", default="/")