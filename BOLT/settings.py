import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yh#xj0(y^prqm(algsngjtz#q%zn$+050hhuzw--x_t!-5ys*0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ['stand-metro.uz', 'www.stand-metro.uz', '167.71.49.146', 'localhost']
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'modeltranslation',
    'django.contrib.admin',

    # Local APPS
    'user_app',
    'product_app',
    'settings_app',

    # Global APPS
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # YENİ
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# settings.py

# Redirect to the login page or home after logging out
LOGOUT_REDIRECT_URL = '/'
LOGOUT_URL = '/'


ROOT_URLCONF = 'BOLT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'BOLT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smbolt',
        'USER': 'postgres',
        'PASSWORD': '22',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'uz'

USE_TZ = True

USE_L10N = True

USE_I18N = True

TIME_ZONE = 'Asia/Tashkent'


LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS = [BASE_DIR / "static/"]
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DATA_UPLOAD_MAX_MEMORY_SIZE = 524288333

# New settings
AUTH_USER_MODEL = 'user_app.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
]

# JAZZMIN SETTINGS
JAZZMIN_SETTINGS = {
    "site_title": "Railway Poster",
    "site_header": "Railway Poster",
    "site_brand": "Railway Poster",
    "site_logo": "custom/logo.png",  # Use a high-quality logo
    "login_logo": "custom/logo.png",
    "login_logo_dark": "custom/logo.png",
    "site_logo_classes": "img-circle",
    "site_icon": "custom/logo.png",  # Add a favicon for better branding
    "welcome_sign": "Xush kelibsiz Railway Poster Admin Paneliga!",
    "copyright": "© Qarshi Vagon Deposi",
    "search_model": ["product_app.Maxsulot", "product_app.Order"],
    "user_avatar": "auth.User.profile_image",  # Example for user avatars

    # Top menu links
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Documentation", "url": "https://docs.djangoproject.com/", "new_window": True},
        # please write for the following row my telegram url. @oxunjonabdulla
        {"name": "Support", "url": "https://t.me/oxunjonabdulla", "new_window": True},
    ],



    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": ["auth.user", "auth.group"],

    # Sidebar ordering
    "order_with_respect_to": ["product_app", "auth", "django.contrib"],

    # Icons for apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-users",
        "product_app.Maxsulot": "fas fa-box-open",
        "product_app.Order": "fas fa-shopping-cart",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Related modal
    "related_modal_active": True,

    # UI Tweaks
    "custom_css": "custom/custom.css",  # Include CSS for refined UI
    "custom_js": "custom/custom.js",    # Add JavaScript for interactive UI
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    "language_chooser": True,  # Add a language chooser if needed
}

# Jazzmin UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": True,
    "brand_colour": "navbar-primary",
    "accent": "accent-cyan",
    "navbar": "navbar-dark navbar-primary",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",  # Use a modern theme
    "dark_mode_theme": "darkly",  # Add a dark mode option
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": True,
}
