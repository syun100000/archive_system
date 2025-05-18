import os
from pathlib import Path



# 環境変数から設定ファイルを決定
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'docker':
    from .settings_docker import *
else:
    # デフォルトの開発用設定
    from .settings_development import *
    
