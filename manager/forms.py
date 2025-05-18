from django import forms
from ckeditor.widgets import CKEditorWidget
from django_ckeditor_5.widgets import CKEditor5Widget
from django.core.exceptions import ValidationError
from accounts.models import User
from django.db.models import Case, When, IntegerField
from ArchiveViewer.models import Report, Tag, Upload

class CategoryMultipleChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        self.choices_list = []
        super().__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        for id, display_name in self.choices_list:
            if obj.id == id:
                return display_name
        return obj.name

class ReportForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditor5Widget(
            attrs={"class": "django_ckeditor_5", "name": "description"},
            config_name='extends'
        ),
        required=False
    )
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'data-role': 'tagsinput',
            'style': 'display: none;',  # 非表示
            'name': 'tags',
            'list': 'tags_list',
        })
    )
    # categories フィールドは __init__ メソッド内で定義します

    class Meta:
        model = Report
        fields = ['title', 'description', 'tags', 'categories', 'is_public', 'is_recommend']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 'name': 'title'}),
            'description': CKEditorWidget(attrs={'class': 'form-control', 'id': 'description', 'name': 'description'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 遅延インポートしてデータベースアクセスを遅らせます
        from ArchiveViewer.models import Category
        from .utils import get_category_choices

        # choices を取得
        choices = get_category_choices()
        self.fields['categories'] = CategoryMultipleChoiceField(
            queryset=Category.objects.none(),  # 一旦空にする
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label='カテゴリー'
        )
        self.fields['categories'].choices = choices
        self.fields['categories'].choices_list = choices

        # queryset を choices の順序に合わせて並べ替える
        category_ids = [id for id, _ in choices]

        # Case/When を使って ordering を作成
        when_statements = [When(id=pk, then=pos) for pos, pk in enumerate(category_ids)]
        ordering = Case(*when_statements, output_field=IntegerField())

        # queryset を設定
        queryset = Category.objects.filter(id__in=category_ids).annotate(
            custom_order=ordering
        ).order_by('custom_order')
        self.fields['categories'].queryset = queryset

        if self.instance.pk:
            self.fields['tags'].initial = ','.join([tag.name for tag in self.instance.tags.all()])
            self.fields['categories'].initial = self.instance.categories.all()

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.created_by = user
            instance.updated_by = user
        tags = self.cleaned_data.get('tags', '')
        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

        if commit:
            instance.save()
            instance.tags.clear()
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
            instance.categories.set(self.cleaned_data.get('categories', []))
            self.save_m2m()

        return instance

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')

        if not description or description.strip() == '':
            raise ValidationError('説明は必須です。')

# ユーザー作成フォーム
class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='パスワード確認')

    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name', 'is_staff', 'is_superuser']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "パスワードが一致しません。")

        return cleaned_data

class UploadForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'data-role': 'tagsinput',
            'style': 'display: none;',
            'name': 'tags',
            'list': 'tags_list',
        })
    )
    # categories フィールドは __init__ メソッド内で定義します

    class Meta:
        model = Upload
        fields = ['title', 'file_path', 'comment', 'categories', 'tags', 'published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 'name': 'title'}),
            'file_path': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control','id': 'comment', 'name': 'comment'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 遅延インポート
        from ArchiveViewer.models import Category
        from .utils import get_category_choices

        # choices を取得
        choices = get_category_choices()
        self.fields['categories'] = CategoryMultipleChoiceField(
            queryset=Category.objects.none(),  # 一旦空にする
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label='カテゴリー'
        )
        self.fields['categories'].choices = choices
        self.fields['categories'].choices_list = choices

        # queryset を choices の順序に合わせて並べ替える
        category_ids = [id for id, _ in choices]
        when_statements = [When(id=pk, then=pos) for pos, pk in enumerate(category_ids)]
        ordering = Case(*when_statements, output_field=IntegerField())

        queryset = Category.objects.filter(id__in=category_ids).annotate(
            custom_order=ordering
        ).order_by('custom_order')
        self.fields['categories'].queryset = queryset

        if self.instance and self.instance.pk:
            # 編集時には file_path を必須にしない
            self.fields['file_path'].required = False
            self.fields['tags'].initial = ','.join([tag.name for tag in self.instance.tags.all()])
            self.fields['categories'].initial = self.instance.categories.all()
        else:
            # 新規作成時は file_path を必須に設定
            self.fields['file_path'].required = True

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if not title:
            raise ValidationError('タイトルは必須です。')

        file_path = cleaned_data.get('file_path')

        if not self.instance.pk:
            # 新規作成時には file_path が必須
            if not file_path:
                raise ValidationError('ファイルパスは必須です。')
        else:
            # 編集時には file_path の更新がない場合は既存の file_path を保持
            if not file_path:
                cleaned_data['file_path'] = self.instance.file_path

        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.updated_by = user

        # ファイルパスが更新されていない場合、既存のファイルパスを保持
        if not self.cleaned_data.get('file_path') and self.instance.pk:
            instance.file_path = self.instance.file_path

        tags = self.cleaned_data.get('tags', '')
        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        if commit:
            instance.save()
            instance.tags.clear()
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)
            self.save_m2m()

            # カテゴリーの保存
            instance.categories.set(self.cleaned_data.get('categories', []))

        return instance