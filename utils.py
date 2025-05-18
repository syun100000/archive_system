"""
このファイルは自作関数をまとめたファイルです。
"""
import urllib.parse
import os
#ユーザーの権限をチェックするデコレーダ
"""
check_user_admin_staffの使い方
from django.contrib.auth.decorators import user_passes_test
をインポートして、
@user_passes_test(check_user_admin_staff)
を関数の上に書くと、その関数にアクセスする前に、ユーザーが認証されているか、
admin または staff 属性を持つかチェックする。
"""

def check_user_admin_staff(user):
    # ユーザーが認証されているかチェック
    if not user.is_authenticated:
        return False
    # admin または staff 属性を持つかチェック
    return user.is_superuser or user.is_staff

def check_user_admin(user):
    # ユーザーが認証されているかチェック
    if not user.is_authenticated:
        return False
    # admin 属性を持つかチェック
    return user.is_superuser


#　YouTubeの埋め込みコードを取得する関数
def get_youtube_embed_code(url,url_only=True):
    #もしURLが空なら、Falseを返す
    if url == "":
        return False
    try:
        #URLから動画識別子を取得する
        #もしURLにv=が含まれている場合は、v=の後ろの11文字を取得する
        if url.find("v=") != -1:
            video_id = url.split("v=")[1]
        #もしURLにv=が含まれていない場合は、youtu.be/の後ろの11文字を取得する
        else:
            video_id = url.split("youtu.be/")[1]
            
        if url_only:
            #URLのみを返す
            encode_url = f"https://www.youtube.com/embed/{video_id}"
            return encode_url
        else:
            #埋め込みコードを返す
            embed_code = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
            return embed_code
    except:
        print("YouTubeの埋め込みコードの取得に失敗しました")
        return False
    
# Uploadのファイルタイプの解析を行う関数
def file_type_check(file_name:str):
    # ファイル名がYouTubeのURLを含む場合
    if 'youtube.com' in file_name:
        return 'youtube'
    # ファイル名がURLを含む場合
    if 'https://' in file_name or 'http://' in file_name:
        return 'URL'
    else:
        #ファイルの拡張子を取得する
        file_type = file_name.split('.')[-1]
        # 小文字に統一する
        file_type = file_type.lower()
        #ファイルの拡張子が、以下の拡張子の場合は、Trueを返す
        if file_type in ['jpg','jpeg','png','gif','bmp']:
            return 'image'
        elif file_type in ['mp4','mov','avi','webm','ogg']:
            return 'video'
        elif file_type in ['mp3','wav','m4a','ogg','flac','aac']:
            return 'audio'
        elif file_type in ['pdf']:
            return 'pdf'
        else:
            return False
        
# URLをデコードする関数
def decode_url(url:str, spaces_as_percent20:bool=False):
    #もしURLが空なら、Falseを返す
    if url == "":
        raise Exception("引数にURLが指定されていません")
    try:
        if spaces_as_percent20:
            url = url.replace(" ", "%20")
        else:
            url = urllib.parse.unquote(url)
        return url
    except:
        raise Exception("URLのデコードに失敗しました")
        
