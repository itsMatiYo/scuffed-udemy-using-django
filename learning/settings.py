from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default='127.0.0.1')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my app(s)
    'users.apps.UsersConfig',
    'authentication.apps.AuthenticationConfig',
    # 'chat.apps.ChatConfig',
    'lapi.apps.LapiConfig',
    'course.apps.CourseConfig',
    'posts_api.apps.PostsApiConfig',

    'wallet.apps.WalletConfig',
    'wallet_creditcard.apps.WalletCreditcardConfig',
    'wallet_locked.apps.WalletLockedConfig',
    'wallet_packet.apps.WalletPacketConfig',
    'wallet_part.apps.WalletPartConfig',
    'wallet_payment.apps.WalletPaymentConfig',
    'wallet_transaction.apps.WalletTransactionConfig',
    'wallet_withdrawal.apps.WalletWithdrawalConfig',
    "Mail.apps.MailConfig",

    # 3rd party apps
    'rest_framework',
    "corsheaders",
    'django_filters',
    'django_cleanup.apps.CleanupConfig',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,


}

MIDDLEWARE = [
    # django-cors-headers middleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'learning.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'learning.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': config('ENGINE', default="django.db.backends.sqlite3"),
        'NAME': config('NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=""),
        'PASSWORD': config('PASSWORD', default=""),
        # 'HOST': config('HOST', default=""),
        # 'PORT': config('PORT', default="")
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Iran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'

# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000",
# ]
CORS_ALLOW_ALL_ORIGINS = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ! info :
# sevice --> [name : learning | id:1a657524-bde0-4713-854a-d6b689d4b179]
# admin --> [name : learning_admin | password : learning_admin]
