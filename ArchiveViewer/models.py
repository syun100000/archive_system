from django.db import models
from os.path import basename, splitext
from ckeditor.fields import RichTextField
from django.utils import timezone
import urllib.parse
from django_ckeditor_5.fields import CKEditor5Field
from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.contrib import messages
import os
from django.conf import settings
from utils import *
import re
def remove_suffix_number(file_name):
    pattern = r'_(\d{14})(\.\w+)$'
    return re.sub(pattern, r'\2', file_name)
'''
このモデルファイルは、このアプリケーションで使うモデルをユーザーモデルをのぞいて定義している。
ユーザーモデルはaccountsアプリケーションで定義している。
ここでの言い回しについて
アーカイブコンテンツ：アーカイブ管理システムのグループが作成したシステムによってアップロードされたコンテンツのこと。
記事：このアプリケーションで作成されたコンテンツのこと。
'''
# タグ用モデル
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="タグ名", unique=True, blank=False, null=False)
    description = models.TextField(verbose_name="タグの説明", blank=True, null=True)
    upload_models = models.ManyToManyField("upload", related_name="tags", blank=True)
    report_models = models.ManyToManyField("Report", related_name="tags", blank=True)

    def __str__(self):
        return self.name
    
    # 削除時の処理
    def delete(self, *args, **kwargs):
        # 関連するレポートやアップロードを削除
        self.upload_models.all().delete()
        self.report_models.all().delete()
        # タグ自体を削除
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "タグ"
        verbose_name_plural = "タグ"

# カテゴリーモデル
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="カテゴリー名")
    description = models.TextField(verbose_name="カテゴリーの説明", blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', blank=True, null=True, verbose_name="親カテゴリー")
    is_active = models.BooleanField(default=True, verbose_name="有効フラグ")

    def __str__(self):
        return self.name
    
    def clean(self):
        super().clean()
        if self.parent == self:
            raise ValidationError({'parent': '親カテゴリーに自身を設定することはできません。'})
        if not self.pk:  # カテゴリー作成時のみ実行
            if self.parent:
                if Category.objects.filter(parent=self.parent, name=self.name).exists():
                    raise ValidationError("同じ親カテゴリー内に同じ名前のカテゴリーが既に存在します。")
            else:
                if Category.objects.filter(parent__isnull=True, name=self.name).exists():
                    raise ValidationError("トップレベルに同じ名前のカテゴリーが既に存在します。")

    class Meta:
        verbose_name = "カテゴリー"
        verbose_name_plural = "カテゴリー"
        constraints = [
            models.UniqueConstraint(
                fields=['parent', 'name'],
                name='unique_category_per_parent'
            )
        ]
# アーカイブコンテンツ用モデル
class Upload(models.Model):
    file_id = models.AutoField(primary_key=True)
    title = models.TextField(verbose_name="タイトル")
    file_name = models.CharField(max_length=255, verbose_name="ファイル名")
    file_path = models.CharField(max_length=255, verbose_name="ファイルパス")
    file_type = models.CharField(max_length=255, verbose_name="ファイルタイプ",default="")
    comment = models.TextField(blank=True, null=True, verbose_name="コメント")
    insert_at = models.DateTimeField(auto_now_add=True, verbose_name="挿入日時")
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    delete_flag = models.BooleanField(default=False, verbose_name="削除フラグ")
    user_id = models.IntegerField(default=0, verbose_name="ユーザーID")
    published = models.BooleanField(default=False, verbose_name="公開フラグ")
    is_unedited = models.BooleanField(default=True, null=True, verbose_name="未編集フラグ")
    categories = models.ManyToManyField(Category, related_name='uploads', blank=True, verbose_name="カテゴリー")
    extracted_text = models.TextField(blank=True, null=True, verbose_name="抽出テキスト")
    def save(self, *args, **kwargs):
        try:
            # 拡張子を元にファイルタイプを設定
            ext = splitext(self.file_path)[1]
            # ファイルタイプを解析して設定
            self.file_type = file_type_check(self.file_name)
            # 削除or非公開の場合はmedia/unpublishedディレクトリに移動して表示させないようにする
            if self.delete_flag or not self.published:
                if not self.file_path.startswith('unpublished'):
                    unpublished_path = os.path.join(settings.MEDIA_ROOT, 'unpublished')
                    os.makedirs(unpublished_path, exist_ok=True)
                    base, ext = splitext(basename(self.file_path))
                    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                    new_file_name = f"{base}_{timestamp}{ext}"
                    os.rename(
                        os.path.join(settings.BASE_DIR, self.file_path.lstrip('/')),
                        os.path.join(unpublished_path, new_file_name)
                    )
                    self.file_path = os.path.join(settings.MEDIA_URL, 'unpublished', new_file_name)
            else:
                if self.file_path.startswith('/media/unpublished'):
                    # 公開する場合はunpublishedディレクトリから移動する
                    base, ext = splitext(remove_suffix_number(basename(self.file_path)))
                    new_file_name = f"{base}{ext}"
                    media_path = settings.MEDIA_ROOT
                    # mediaディレクトリに移動する際にファイル名が重複していた場合は連番をつける
                    while os.path.exists(os.path.join(media_path, new_file_name)):
                        base, ext = splitext(new_file_name)
                        base = base.rsplit('_', 1)[0]
                        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
                        new_file_name = f"{base}_{timestamp}{ext}"
                    os.rename(
                        os.path.join(settings.BASE_DIR, self.file_path.lstrip('/')),
                        os.path.join(media_path, new_file_name)
                    )
                    self.file_path = settings.MEDIA_URL + new_file_name
            
            if self.file_path != self.file_name:
                self.file_name = basename(self.file_path)
        except Exception as e:
            print(e)
        super().save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'upload'
        verbose_name = "アーカイブコンテンツ"
        verbose_name_plural = "アーカイブコンテンツ"

# 記事用モデル
class Report(models.Model):
    title = models.CharField(max_length=100, verbose_name="タイトル")
    description = CKEditor5Field(config_name='extends', verbose_name="説明")
    is_public = models.BooleanField(default=False, verbose_name="公開フラグ")
    is_recommend = models.BooleanField(default=False, verbose_name="おすすめフラグ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="created_reports", verbose_name="作成者")
    updated_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="updated_reports", verbose_name="更新者")
    deleted_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="deleted_reports", null=True, verbose_name="削除者")
    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")
    categories = models.ManyToManyField(Category, related_name="reports", blank=True, verbose_name="カテゴリー")
    def save(self, *args, **kwargs):
        # descriptionの中身のIMGタグのサイズが%以外の場合、100%に変更する
        soup = BeautifulSoup(self.description, 'html.parser')
        for img in soup.find_all('img'):
            if 'width' in img.attrs and not img['width'].endswith('%'):
                img['width'] = '100%'
            if 'height' in img.attrs and not img['height'].endswith('%'):
                img['height'] = '100%'
        self.description = str(soup)
        # 保存処理
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "記事"
        verbose_name_plural = "記事"

# 履歴とお気に入りの抽象モデル
class HistoryFavoriteBase(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, verbose_name="ユーザー")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    class Meta:
        # 抽象モデルとして扱うのでTrue
        abstract = True

# ユーザーが閲覧したアーカイブコンテンツを保存するテーブル
class UploadHistory(HistoryFavoriteBase):
    upload = models.ForeignKey("Upload", on_delete=models.CASCADE, verbose_name="アーカイブコンテンツ")

    class Meta:
        # 作成日時の昇順で並べる
        ordering = ['created_at']
        verbose_name = "アーカイブコンテンツ履歴"
        verbose_name_plural = "アーカイブコンテンツ履歴"

    # ユーザーが閲覧したアーカイブコンテンツの履歴を100件まで保存する
    def clean_history(self):
        history_count = UploadHistory.objects.filter(user=self.user).count()
        if history_count >= 10:
            oldest_history = UploadHistory.objects.filter(user=self.user).order_by('created_at').first()
            oldest_history.delete()

    # オーバーライド
    def save (self, *args, **kwargs):
        self.clean_history()
        super().save(*args, **kwargs)

# ユーザーが閲覧した記事を保存するテーブル
class ReportHistory(HistoryFavoriteBase):
    report = models.ForeignKey("Report", on_delete=models.CASCADE, verbose_name="記事")

    class Meta:
        ordering = ['created_at']
        verbose_name = "記事履歴"
        verbose_name_plural = "記事履歴"

    def clean_history(self):
        history_count = ReportHistory.objects.filter(user=self.user).count()
        if history_count >= 10:
            oldest_history = ReportHistory.objects.filter(user=self.user).order_by('created_at').first()
            oldest_history.delete()

    def save (self, *args, **kwargs):
        self.clean_history()
        super().save(*args, **kwargs)

# ユーザーのお気に入り記事を保存するテーブル
class ReportFavorite(HistoryFavoriteBase):
    report = models.ForeignKey("Report", on_delete=models.CASCADE, verbose_name="記事")
    
    # 重複のないようにする
    def save(self, *args, **kwargs):
        if ReportFavorite.objects.filter(user=self.user, report=self.report).exists():
            return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "お気に入り記事"
        verbose_name_plural = "お気に入り記事"

# ユーザーのお気に入りアーカイブを保存するテーブル
class UploadFavorite(HistoryFavoriteBase):
    upload = models.ForeignKey("Upload", on_delete=models.CASCADE, verbose_name="アーカイブコンテンツ")
    
    # 重複のないようにする
    def save(self, *args, **kwargs):
        if UploadFavorite.objects.filter(user=self.user, upload=self.upload).exists():
            return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "お気に入りアーカイブ"
        verbose_name_plural = "お気に入りアーカイブ"

# お知らせ用モデル
class Announcement(models.Model):
    title = models.CharField(max_length=100, verbose_name="お知らせタイトル")
    description = models.TextField(verbose_name="お知らせの説明")
    is_public = models.BooleanField(default=False, verbose_name="公開フラグ")
    is_html = models.BooleanField(default=False, verbose_name="HTMLフラグ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    created_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="created_announcements", verbose_name="作成者")
    updated_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="updated_announcements", verbose_name="更新者")
    deleted_by = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="deleted_announcements", null=True, verbose_name="削除者")
    is_deleted = models.BooleanField(default=False, verbose_name="削除フラグ")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "お知らせ"
        verbose_name_plural = "お知らせ"
