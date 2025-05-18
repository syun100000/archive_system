'''
"""
このファイルは、Docker環境でのDjango設定ファイルです。

設定内容:
- DEBUGモードの有効化
- OpenAI APIキーとGPTモデルの設定
- MySQLデータベースの設定
- 許可されるホストの設定
- パスワードバリデーションの設定
- WSGIアプリケーションの設定
- ロギングの設定:
    - バージョン: 1
    - 既存のロガーを無効化しない
    - フィルター:
        - require_debug_false: DEBUGがFalseの場合に適用
        - require_debug_true: DEBUGがTrueの場合に適用
    - フォーマッター:
        - django.server: サーバーのログフォーマット
        - verbose: 詳細なログフォーマット
    - ハンドラー:
        - console: コンソール出力用ハンドラー
        - django.server: サーバーログ用ハンドラー
        - mail_admins: 管理者へのメール送信ハンドラー
    - ロガー:
        - django: Django全体のロガー
        - django.server: サーバーログ用ロガー
        - myapp: アプリケーション用ロガー
"""
このファイルは、Docker環境での設定ファイルです。
このファイルが読み込まれるのはENVIRONMENTが'docker'の場合です。
このファイルは、settings_shared.pyからの設定を継承しています。
'''

from .settings_shared import *
import os  # 環境変数読み込み用
DEBUG = True
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # 環境変数から取得
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o-mini")  # 環境変数から取得

# Tesseractのパスとデータパス（環境変数から取得、なければデフォルト）
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")
TESSDATA_PATH = os.getenv("TESSDATA_PATH", "/usr/share/tesseract-ocr/4.00/tessdata")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DATABASE_NAME", "archive_system"),
        "USER": os.getenv("DATABASE_USER", "root"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "archive_system"),
        "HOST": os.getenv("DATABASE_HOST", "db1"),
        "PORT": os.getenv("DATABASE_PORT", "3306"),
    }
}

# ALLOWED_HOSTSを環境変数から取得（カンマ区切り）
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")  # 例: "localhost,127.0.0.1"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

WSGI_APPLICATION = "archive_system.wsgi.application"

PROJECT_NAME = 'archive_system'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     # ログ出力フォーマットの設定
#     'formatters': {
#         'production': {
#             'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
#                       '%(pathname)s:%(lineno)d %(message)s'
#         },
#     },
#     # ハンドラの設定
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': '/var/log/{}/app.log'.format(PROJECT_NAME),
#             'formatter': 'production',
#         },
#     },
#     # ロガーの設定
#     'loggers': {
#         # 自分で追加したアプリケーション全般のログを拾うロガー
#         '': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#         # Django自身が出力するログ全般を拾うロガー
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }
