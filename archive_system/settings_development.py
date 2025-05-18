'''
開発環境用の設定ファイル
ENVIRONMENTが'docker'でない場合に読み込まれます。
このファイルは、settings_shared.pyからの設定を継承しています。
'''

from .settings_shared import *
import os  # 環境変数読み込み用
DEBUG = True
AUTH_PASSWORD_VALIDATORS = []
# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # 環境変数から取得
GPT_MODEL = os.getenv("GPT_MODEL", "gpt-4o-mini")  # 環境変数から取得
import platform
# OSによってTesseractのパスを設定
if platform.system() == "Windows":
    TESSERACT_PATH = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
elif platform.system() == "Darwin":  # macOS
    TESSERACT_PATH = "/opt/homebrew/bin/tesseract"
elif platform.system() == "Linux":
    TESSERACT_PATH = "/usr/bin/tesseract"
else:
    TESSERACT_PATH = "/usr/local/bin/tesseract"  # デフォルトのパス
# 開発環境用のデータベース設定
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("DATABASE_NAME", "archive_system"),  # 環境変数から取得
        "USER": os.getenv("DATABASE_USER", "archive_system"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "archive_system"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", "3306"),
    }
}