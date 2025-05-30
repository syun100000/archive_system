# Generated by Django 5.1.1 on 2024-11-07 14:36

import django.db.models.deletion
import django_ckeditor_5.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Announcement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="お知らせタイトル")),
                ("description", models.TextField(verbose_name="お知らせの説明")),
                ("is_public", models.BooleanField(default=False, verbose_name="公開フラグ")),
                ("is_html", models.BooleanField(default=False, verbose_name="HTMLフラグ")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新日時"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="削除フラグ"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_announcements",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="作成者",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="deleted_announcements",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="削除者",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="updated_announcements",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="更新者",
                    ),
                ),
            ],
            options={
                "verbose_name": "お知らせ",
                "verbose_name_plural": "お知らせ",
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="カテゴリー名")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="カテゴリーの説明"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="有効フラグ")),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="ArchiveViewer.category",
                        verbose_name="親カテゴリー",
                    ),
                ),
            ],
            options={
                "verbose_name": "カテゴリー",
                "verbose_name_plural": "カテゴリー",
            },
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="タイトル")),
                (
                    "description",
                    django_ckeditor_5.fields.CKEditor5Field(verbose_name="説明"),
                ),
                ("is_public", models.BooleanField(default=False, verbose_name="公開フラグ")),
                (
                    "is_recommend",
                    models.BooleanField(default=False, verbose_name="おすすめフラグ"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新日時"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="削除フラグ"),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="reports",
                        to="ArchiveViewer.category",
                        verbose_name="カテゴリー",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_reports",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="作成者",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="deleted_reports",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="削除者",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="updated_reports",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="更新者",
                    ),
                ),
            ],
            options={
                "verbose_name": "記事",
                "verbose_name_plural": "記事",
            },
        ),
        migrations.CreateModel(
            name="ReportFavorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ArchiveViewer.report",
                        verbose_name="記事",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name": "お気に入り記事",
                "verbose_name_plural": "お気に入り記事",
            },
        ),
        migrations.CreateModel(
            name="ReportHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "report",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ArchiveViewer.report",
                        verbose_name="記事",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name": "記事履歴",
                "verbose_name_plural": "記事履歴",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Upload",
            fields=[
                ("file_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.TextField(verbose_name="タイトル")),
                ("file_name", models.CharField(max_length=255, verbose_name="ファイル名")),
                ("file_path", models.CharField(max_length=255, verbose_name="ファイルパス")),
                (
                    "comment",
                    models.TextField(blank=True, null=True, verbose_name="コメント"),
                ),
                (
                    "insert_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="挿入日時"),
                ),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新日時")),
                (
                    "delete_flag",
                    models.BooleanField(default=False, verbose_name="削除フラグ"),
                ),
                ("user_id", models.IntegerField(default=0, verbose_name="ユーザーID")),
                ("published", models.BooleanField(default=False, verbose_name="公開フラグ")),
                (
                    "is_unedited",
                    models.BooleanField(default=True, null=True, verbose_name="未編集フラグ"),
                ),
                (
                    "categories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="uploads",
                        to="ArchiveViewer.category",
                        verbose_name="カテゴリー",
                    ),
                ),
            ],
            options={
                "verbose_name": "アーカイブコンテンツ",
                "verbose_name_plural": "アーカイブコンテンツ",
                "db_table": "upload",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=100, unique=True, verbose_name="タグ名"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="タグの説明"),
                ),
                (
                    "report_models",
                    models.ManyToManyField(
                        blank=True, related_name="tags", to="ArchiveViewer.report"
                    ),
                ),
                (
                    "upload_models",
                    models.ManyToManyField(
                        blank=True, related_name="tags", to="ArchiveViewer.upload"
                    ),
                ),
            ],
            options={
                "verbose_name": "タグ",
                "verbose_name_plural": "タグ",
            },
        ),
        migrations.CreateModel(
            name="UploadFavorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "upload",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ArchiveViewer.upload",
                        verbose_name="アーカイブコンテンツ",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name": "お気に入りアーカイブ",
                "verbose_name_plural": "お気に入りアーカイブ",
            },
        ),
        migrations.CreateModel(
            name="UploadHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "upload",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ArchiveViewer.upload",
                        verbose_name="アーカイブコンテンツ",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "verbose_name": "アーカイブコンテンツ履歴",
                "verbose_name_plural": "アーカイブコンテンツ履歴",
                "ordering": ["created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="category",
            constraint=models.UniqueConstraint(
                fields=("parent", "name"), name="unique_category_per_parent"
            ),
        ),
    ]
