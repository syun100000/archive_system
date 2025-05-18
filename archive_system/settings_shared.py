'''
共通設定ファイル
'''

import os
from pathlib import Path
import yaml
from dotenv import load_dotenv  # python-dotenvを使用

# BASE_DIRを設定
BASE_DIR = Path(__file__).resolve().parent.parent

# .envファイルから環境変数を読み込む
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")  # 環境変数から取得
# ALLOWED_HOSTSを環境変数から取得（カンマ区切り）
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")  # 例: "localhost,127.0.0.1"
CSRF_COOKIE_HTTPONLY = False

# 環境設定ファイルの読み込み
CONFIG_FILE = os.path.join(BASE_DIR, 'archive_system', 'config', 'config.yaml')

# SECURITY WARNING: don't run with debug turned on in production!
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



# Application definition

INSTALLED_APPS = [
    # 'grappelli',
    # 'filebrowser',
    "django.contrib.admin", # Django管理サイト
    "django.contrib.auth", # 認証システム
    "django.contrib.contenttypes", # コンテンツタイプフレームワーク
    "django.contrib.sessions", # セッションフレームワーク
    "django.contrib.messages", # メッセージフレームワーク
    "django.contrib.staticfiles", # 静的ファイルの管理
    "django.contrib.sites", # サイトフレームワーク
    # "django.contrib.auth", # 認証フレームワーク
    "allauth", # 認証フレームワーク
    "allauth.account", # 認証フレームワーク
    # "allauth.socialaccount", # 認証フレームワーク
    # 'ckeditor', # テキストエディタ
    # 'ckeditor_uploader', # テキストエディタ
    'django_ckeditor_5',
    "accounts", # アプリケーション
    "ArchiveViewer", # アプリケーション
    "manager", # アプリケーション
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware", # セキュリティ
    "django.contrib.sessions.middleware.SessionMiddleware", # セッション
    "django.middleware.common.CommonMiddleware", # 共通
    "django.middleware.csrf.CsrfViewMiddleware", # CSRF
    "django.contrib.auth.middleware.AuthenticationMiddleware", # 認証
    "django.contrib.messages.middleware.MessageMiddleware", # メッセージ
    "django.middleware.clickjacking.XFrameOptionsMiddleware", # クリックジャッキング
    "allauth.account.middleware.AccountMiddleware" # 認証フレームワーク
]

ROOT_URLCONF = "archive_system.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'archive_system.context_processors.site_settings',
            ],
        },
    },
]




# DATABASE_ROUTERSの設定
# DATABASE_ROUTERS = ['archive_system.dbrouter.ArchiveSystemRouter']


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ja-jp"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = True

# APPEND_SLASH = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# 下記からallauth
# ユーザーモデルをカスタムしたので設定
SITE_ID = 1
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = [ 
#   'django.contrib.auth.backends.ModelBackend',     
  'allauth.account.auth_backends.AuthenticationBackend',
] 

#ユーザーネームは使わない
ACCOUNT_EMAIL_VERIFICATION = False 
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

#認証にはメールアドレスを使用する
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
#ログインURLの指定
LOGIN_URL = "/accounts/login"

#ログイン後のリダイレクト先を指定
LOGIN_REDIRECT_URL = "/"
# ユーザー名の必須設定
ACCOUNT_USERNAME_REQUIRED = False
#ログアウト後のリダイレクト先を指定
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

#メールアドレスが確認済でないとログインできない
ACCOUNT_EMAIL_VERIFICATION = 'none'
# ユーザーが持つことができる最大のメールアドレス数は1
ACCOUNT_CHANGE_EMAIL = False
#即ログアウトとする
ACCOUNT_LOGOUT_ON_GET = True

# Email 本番用
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'apptest'
# EMAIL_HOST_PASSWORD = 'xxxxxxxx'
# EMAIL_USE_TLS = False
# メール送信時の送信元
EMAIL_HOST_USER = 'apptest@localhost.com'
# メール送信のバックエンドを指定 ターミナル使用　デバッグ用
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


customColorPalette = [
    {
        'color': 'hsl(4, 90%, 58%)',
        'label': 'Red'
    },
    {
        'color': 'hsl(340, 82%, 52%)',
        'label': 'Pink'
    },
    {
        'color': 'hsl(291, 64%, 42%)',
        'label': 'Purple'
    },
    {
        'color': 'hsl(262, 52%, 47%)',
        'label': 'Deep Purple'
    },
    {
        'color': 'hsl(231, 48%, 48%)',
        'label': 'Indigo'
    },
    {
        'color': 'hsl(207, 90%, 54%)',
        'label': 'Blue'
    },
]

# CKEditor5の設定
# CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
# CKEDITOR_5_FILE_STORAGE = "path_to_storage.CustomStorage" # optional
CKEDITOR_5_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_5_CONFIGS = {
'default': {
    'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    'language': 'ja',
},
'extends': {
    'language': 'ja',
    'blockToolbar': [
        'paragraph', 'heading1', 'heading2', 'heading3',
        '|',
        'bulletedList', 'numberedList',
        '|',
        'blockQuote',
    ],
    'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
    'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing',
                'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'insertTable',],
    # 'image': {
    #     'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
    #                 'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
    #     'styles': [
    #         'full',
    #         'side',
    #         'alignLeft',
    #         'alignRight',
    #         'alignCenter',
    #     ],
    # },
    'table': {
        'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
        'tableProperties', 'tableCellProperties' ],
        'tableProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
        },
        'tableCellProperties': {
            'borderColors': customColorPalette,
            'backgroundColors': customColorPalette
        }
    },
    'heading' : {
        'options': [
            { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
            { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
            { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
            { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
        ]
    }
},
'list': {
    'properties': {
        'styles': 'true',
        'startIndex': 'true',
        'reversed': 'true',
    }
}
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "none"  # Possible values: "staff", "authenticated", "any"


# メッセージフレームワークの設定
from django.contrib.messages import constants as messages

# Bootstrap4用のメッセージタグ
MESSAGE_TAGS = {
    messages.DEBUG: 'dark',
    messages.ERROR: 'danger',
}