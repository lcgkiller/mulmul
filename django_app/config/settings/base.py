"""
Django settings for deploy_ec2 project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# .config_secret폴더 및 하위 파일 경로
CONFIG_SECRET_DIR = os.path.join(ROOT_DIR, '.config_secret')
CONFIG_SECRET_COMMON_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_common.json')
CONFIG_SECRET_DEBUG_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_debug.json')
CONFIG_SECRET_DEPLOY_FILE = os.path.join(CONFIG_SECRET_DIR, 'settings_deploy.json')

# config_secret변수에 CONFIG_SECRET_COMMON_FILE경로의 파일을 읽은 값을
# json.loads를 이용해 파이썬 객체로 바꾼형태로 할당

# f = open(CONFIG_SECRET_COMMON_FILE)
# config_secret_string = f.read()
# config_secret = json.loads(config_secret_string)
# f.close()
config_secret_common = json.loads(open(CONFIG_SECRET_COMMON_FILE).read())
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_secret_common['django']['secret_key']

DEBUG = True

ALLOWED_HOSTS = []

# 유저모델
AUTH_USER_MODEL = 'member.User'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The following apps are required:
    'django.contrib.sites',

    'django_extensions',
    'rest_framework',            # django-restframework 라이브러리
    'rest_framework.authtoken',  # django-rest-allauth 라이브러리
    'rest_auth',                 # django-rest-allauth 라이브러리
    'rest_auth.registration',    # django-rest-allauth 라이브러리

    'member',
    'post',
]

######### djang-allauth configuration start#########

INSTALLED_APPS += [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.naver',
]
config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())
FACEBOOK_APP_ID = config_secret_deploy['facebook']['SOCIAL_AUTH_FACEBOOK_KEY']

SITE_ID = 1
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_REDIRECT_URL = "/"
ACCOUNT_AUTHENTICATED_LOGOUT_REDIRECTS = True
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

## 이메일을 로그인 아이디로 사용합니다.
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True

# ACCOUNT_USER_MODEL_USERNAME_FIELD = None # allauth에게 username 필드가 없음을 알린다.
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'nickname'
ACCOUNT_USERNAME_REQUIRED = False


## 소셜 계정으로 가입하는 경우 추가 정보를 기입하기 위한 설정입니다.
SOCIALACCOUNT_ADAPTER = 'member.views.SocialAccountAdapter'
SOCIALACCOUNT_AUTO_SIGNUP = True

## 커스텀 SignUp 폼을 사용합니다.
ACCOUNT_SIGNUP_FORM_CLASS = 'member.forms.UserSignUpForm'


SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
         {'METHOD': 'oauth2',
          'SCOPE': ['email', 'public_profile', 'user_friends'],
          'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
          'FIELDS': [
              'id',
              'email',
              'name',
              'first_name',
              'last_name',
              'verified',
              'locale',
              'timezone',
              'link',
              'gender',
              'updated_time'],
          'EXCHANGE_TOKEN': True,
          'LOCALE_FUNC': lambda request: 'kr_KR',
          'VERIFIED_EMAIL': True,
          'VERSION': 'v2.4'},

#https://nid.naver.com/oauth2.0/authorize?client_id=JwGlpc0lDXYdE4OQApK4
# &redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Faccounts%2Fnaver%2Flogin%2Fcallback%2F
# &scope=없어도 됨
# &response_type=code
# &state=wxkF8ogPqEFV
# &auth_type=reauthenticate
    'naver':
         {
          'response_type': "code",
          'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
          },
     }

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

# REST-AUTH 에서 로그인 시리얼 라이저는 커스텀(email 필드 제거)한 시리얼라이저를 사용합니다.
REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'member.serializers.user_login_serializers.UserLoginSerializer', }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    # 'PAGINATE_BY': 10,                 # Default to 10
    # 'PAGINATE_BY_PARAM': 'page_size',  # Allow client to override, using `?page_size=xxx`.
    # 'MAX_PAGINATE_BY': 100             # Maximum limit allowed when using `?page_size=xxx`.

}


######### django-rest-auth configuration end #########

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
        'DIRS': [
            TEMPLATE_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                'django.template.context_processors.request',
                'utils.context_processors.naver_login_api_info',
            ],
        },
    },
]

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    STATIC_DIR,
]
