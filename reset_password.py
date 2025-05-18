import sys
import os
import django
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

# Djangoの設定モジュールを指定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'archive_system.settings')
django.setup()

def reset_password(email, new_password):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        print(f"パスワードが正常にリセットされました: {email}")
    except ObjectDoesNotExist:
        print(f"ユーザーが見つかりません: {email}")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        email = sys.argv[1]
        new_password = sys.argv[2]
    else:
        email = input("メールアドレスを入力してください: ")
        new_password = input("新しいパスワードを入力してください: ")
    
    reset_password(email, new_password)