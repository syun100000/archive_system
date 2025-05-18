from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from django.template import Context, Template
from django.db.models import Q, Count
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
import os
import json
import yaml
from .forms import *
from ArchiveViewer.models import *
from accounts.models import User
from utils import *
from .utils import get_category_choices, extract_text_from_pdf
from GPT import GPT
from Ollama import OllamaClient
import logging
logger = logging.getLogger(__name__)
# 権限チェック関数
def can_edit_report(user):
    if not user.is_authenticated:
        return False
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return user.is_superuser or config['staff_authority'].get('can_edit_report', False)
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        return False

def can_edit_upload(user):
    if not user.is_authenticated:
        return False
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return user.is_superuser or config['staff_authority'].get('can_edit_upload', False)
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        return False

def can_edit_announcement(user):
    if not user.is_authenticated:
        return False
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return user.is_superuser or config['staff_authority'].get('can_edit_announcement', False)
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        return False

def can_edit_tag(user):
    if not user.is_authenticated:
        return False
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return user.is_superuser or config['staff_authority'].get('can_edit_tag', False)
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        return False

def can_edit_category(user):
    if not user.is_authenticated:
        return False
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return user.is_superuser or config['staff_authority'].get('can_edit_category', False)
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        return False


"""
@user_passes_test(check_user_admin_staff)の説明
このデコレーターは、ユーザーがログインしているかどうかをチェックします。
"""

# パイソンの実行ファイルのあるディレクトリのパスを取得
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = settings.BASE_DIR
CONFIG_FILE = settings.CONFIG_FILE
User = get_user_model()
# ホーム画面
@user_passes_test(check_user_admin_staff)
def index(request):
    return render(request, "manager/index.html")

#　記事作成(標準版)
@user_passes_test(check_user_admin_staff)
def write_report(request):
    '''
    記事作成ページです．
    モデル本体や管理ページではdjango_ckeditor_5を使用しているが,
    ここではstaticにあるckeditor.jsを使用している.
    '''
    if not can_edit_report(request.user):
        return HttpResponse('権限がありません。', status=403)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=True, user=request.user)
            report.categories.set(form.cleaned_data['categories'])
            return redirect('report_contents_detail', id=report.id)
    else:
        form = ReportForm()
    tags = Tag.objects.all()
    # CKEditor の設定を取得
    ckeditor_config = settings.CKEDITOR_5_CONFIGS.get('extends', {})
    ckeditor_config_json = json.dumps(ckeditor_config, ensure_ascii=False)
    return render(request, "manager/write_report.html", {
        'form': form,
        'ckeditor_config': ckeditor_config_json,
        'tags': tags
        })

# 記事作成(簡易版)
@user_passes_test(check_user_admin_staff)
def easy_write_report(request):
    if not can_edit_report(request.user):
        return HttpResponse('権限がありません。', status=403)
    if request.method == 'POST':
        title = request.POST.get('title')  # 記事のタイトル
        headline_count = request.POST.get('headline_count')  # 見出しの数
        html_content = ""  # HTMLの内容を格納する変数
        is_public = request.POST.get('is_public')  # 公開フラグ
        tags = request.POST.get('tags')  # タグ
        # 添付ファイルの処理を行う
        # 添付ファイルの情報をもつJSONを取得 name selected_files_by_headline
        selected_files_by_headline = request.POST.get("selected_files_by_headline")
        # JSONを辞書型に変換
        selected_files_by_headline = json.loads(selected_files_by_headline)
        # 公開フラグの処理
        if is_public == "2":
            # 非公開にする場合
            is_public = False
        elif is_public == "1":
            # 公開にする場合
            is_public = True
        else:
            # 公開フラグが不正な場合
            messages.error(request, '公開フラグが不正です。')
            return HttpResponse("公開フラグが不正です。")
        # テンプレートファイルの内容を読み込む
        with open(os.path.join(BASE_DIR, 'manager/templates/manager/easy_write/1.html'), 'r', encoding='utf-8') as file:
            template_content = file.read()

        # テンプレートを生成
        template = Template(template_content)
        for i in range(1, int(headline_count) + 1):
            contents_for_headline = selected_files_by_headline.get(str(i), {}).values()
            context = Context({
                'class_name': f'headline{i}',
                'headline': request.POST.get(f'Headline{i}'),
                'text': request.POST.get(f'Headline{i}_content'),
                'file_id': request.POST.get(f'Headline{i}_file_id'),
                'contents': contents_for_headline,
            })
            # テンプレートをレンダリングしてHTMLを生成
            rendered_html = template.render(context)
            # 生成したHTMLをhtml_contentに追加
            html_content += rendered_html
        # 記事を保存
        report = Report.objects.create(title=title, description=html_content, created_by=request.user, updated_by=request.user, is_public=is_public)
        
        # タグの処理
        if tags:
            tags_list = tags.split(',')
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                report.tags.add(tag)
        # 投稿された記事の詳細ページにリダイレクト
        messages.success(request, '記事を作成しました。')
        return redirect('report_contents_detail', id=report.id)
    else:
        return render(request, "manager/easy_write_report.html")
    
# 記事編集
def report_edit(request, id):
    if not can_edit_report(request.user):
        return HttpResponse('権限がありません。', status=403)
    report = get_object_or_404(Report, id=id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            report.categories.set(form.cleaned_data['categories'])
            messages.success(request, '記事を更新しました。')
            return redirect('report_contents_detail', id=report.id)
    else:
        form = ReportForm(instance=report)
    # CKEditor の設定を取得
    ckeditor_config = settings.CKEDITOR_5_CONFIGS.get('extends', {})
    ckeditor_config_json = json.dumps(ckeditor_config, ensure_ascii=False)
    tags = Tag.objects.all()
    return render(request, "manager/write_report.html", {
        'form': form,
        'edit': True,
        'report': report,
        'ckeditor_config': ckeditor_config_json,
        'tags': tags
    })
# 
#　サーバー内のファイルを検索する
@user_passes_test(check_user_admin_staff)
def search_file(request):
    if not can_edit_report(request.user):
        return HttpResponse('権限がありません。', status=403)
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        file_type = request.POST.get('file_type')
        # ファイル名にキーワードを含むファイルを検索
        q = Q(file_name__icontains=keyword) | Q(title__icontains=keyword) | Q(file_id__icontains=keyword) | Q(tags__name__icontains=keyword) | Q(comment__icontains=keyword)
        uploads = Upload.objects.filter(q, delete_flag=False, published=True)
        count = 0
        content = {
            "CODE": 200,
        }
        files = []
        for upload in uploads:
            if file_type_check(upload.file_path) == file_type:
                # Check if the file is already in 'files'
                if not any(f['ID'] == upload.file_id for f in files):
                    count += 1
                    temp = {
                        "ID": upload.file_id,
                        "TITLE": upload.title,
                        "URL": upload.file_path,
                        "NAME": upload.file_name,
                        "TYPE": file_type_check(upload.file_path),
                    }
                    files.append(temp)
            else:
                continue
        print(files)
        if count == 0:
            # 検索結果が0件の場合
            content["CODE"] = 404
            return JsonResponse(content)
        elif count > 100:
            # 検索結果が100件以上の場合
            content["CODE"] = 413
            return JsonResponse(content)
        elif count > 0:
            # 検索結果が1件以上の場合(100件以下)
            content["CODE"] = 200
            content["FILE_COUNT"] = count
            content["FILE_LIST"] = files
            return JsonResponse(content)
        
# 記事一覧
@user_passes_test(check_user_admin_staff)
def reports(request):
    if not can_edit_report(request.user):
        return HttpResponse('権限がありません。', status=403)
    # 初期値
    sort = 'created_at'
    report_id = ''
    keyword = ''
    start_date = None
    end_date = None
    title = ''
    is_public = ''
    is_recommend = ''
    created_by = ''
    reports = Report.objects.all().exclude(is_deleted=True)
    users = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))

    if request.method == 'GET':
        report_id = request.GET.get('report_id')
        if report_id == 'None':
            report_id = None
        sort = request.GET.get('sort', 'created_at')
        if sort == 'None':
            sort = 'created_at'
        keyword = request.GET.get('search', '')
        start_date = request.GET.get('start_date')
        if start_date == 'None':
            start_date = None
        end_date = request.GET.get('end_date')
        if end_date == 'None':
            end_date = None
        title = request.GET.get('title', '')
        if title == 'None':
            title = ''
        is_public = request.GET.get('is_public')
        if is_public == 'None':
            is_public = None
        is_recommend = request.GET.get('is_recommend')
        if is_recommend == 'None':
            is_recommend = None
        created_by = request.GET.get('created_by')
        if created_by == 'None':
            created_by = ''
        # Create a Q object for filtering
        query = Q()
        if report_id:
            query &= Q(id=report_id)
        if keyword:
            query &= Q(title__icontains=keyword)
        if start_date:
            query &= Q(created_at__gte=start_date)
        if end_date:
            query &= Q(created_at__lte=end_date)
        if title:
            query &= Q(title__icontains=title)
        if is_public:
            query &= Q(is_public=is_public == 'True')
        if is_recommend:
            query &= Q(is_recommend=is_recommend == 'True')
        if created_by:
            query &= Q(created_by__in=created_by)
        # Query the database
        reports = Report.objects.filter(query).exclude(is_deleted=True).order_by(sort)

        # ページネーションの設定
        paginator = Paginator(reports, 10)  # 1ページあたり10件のレポートを表示
        page = request.GET.get('page', 1)
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)

    context = {
        "report_id": report_id,
        'reports': reports,
        'sort': sort,
        'keyword': keyword,
        'start_date': start_date,
        'end_date': end_date,
        'title': title,
        'is_public': is_public,
        'is_recommend': is_recommend,
        "users": users,
        "created_by": created_by,
    }

    if request.method == 'POST':
        print(request.POST)
        # reports_idで取得したIDを数値リストに変換
        reports_ids = request.POST.get('report_ids').split(',')  # 取得したIDをリストに変換
        reports_ids = list(map(int, reports_ids))  # 文字列を数値に変換

        action = request.POST.get('action')

        # アクションがおすすめ記事にする場合
        if action == "recommend":
            for report_id in reports_ids:
                report_instance = Report.objects.get(id=report_id)
                report_instance.is_recommend = True
                report_instance.save()
        # アクションがおすすめ記事から外す場合
        elif action == "unrecommend":
            for report_id in reports_ids:
                report_instance = Report.objects.get(id=report_id)
                report_instance.is_recommend = False
                report_instance.save()
        # アクションが公開する場合
        elif action == "public":
            for report_id in reports_ids:
                report_instance = Report.objects.get(id=report_id)
                report_instance.is_public = True
                report_instance.save()
        # アクションが非公開にする場合
        elif action == "unpublic":
            for report_id in reports_ids:
                report_instance = Report.objects.get(id=report_id)
                report_instance.is_public = False
                report_instance.save()
        # アクションが削除する場合
        elif action == "delete":
            for report_id in reports_ids:
                report_instance = Report.objects.get(id=report_id)
                report_instance.is_deleted = True
                report_instance.deleted_by = request.user
                report_instance.save()
        # リダイレクト先を、前のページにする
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "manager/reports.html", context)

# ゴミ箱の記事一覧
@user_passes_test(check_user_admin_staff)
def reports_dustbox(request):
    if not can_edit_report(request.user):
        return HttpResponse('権限がありません。', status=403)
    sort = 'created_at'
    report_id = ''
    reports = ''
    keyword = ''
    start_date = None
    end_date = None
    title = ''
    created_by = ''
    users=User.objects.filter(Q(is_staff=True)|Q(is_superuser=True))

    if request.method == 'GET':
        report_id = request.GET.get('report_id')
        sort = request.GET.get('sort', 'created_at')
        keyword = request.GET.get('search', '')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        title = request.GET.get('title', '')
        created_by = request.GET.get('created_by')
        # Create a Q object for filtering
        query = Q()
        if not request.user.is_superuser:
            query &= Q(deleted_by=request.user)
        if report_id:
            query &= Q(id=report_id)
        if keyword:
            query &= Q(title__icontains=keyword)
        if start_date:
            query &= Q(created_at__gte=start_date)
        if end_date:
            query &= Q(created_at__lte=end_date)
        if title:
            query &= Q(title__icontains=title)
        if created_by:
            query &= Q(created_by__in=created_by)
        # Query the database
        reports = Report.objects.filter(query).exclude(is_deleted=False).order_by(sort)

    context = {
        "report_id": report_id,
        'reports': reports,
        'sort': sort,
        'keyword': keyword,
        'start_date': start_date,
        'end_date': end_date,
        'title': title,
        "users": users,
        "created_by": created_by,
        
    }
    if request.method == 'POST':
        # reports_idで取得したIDを数値リストに変換
        reports_ids = request.POST.get('report_ids').split(',') # 取得したIDをリストに変換
        reports_ids = list(map(int, reports_ids)) # 文字列を数値に変換
        
        action = request.POST.get('action')
        
        # アクションが復元する場合
        if action == "restore":
            for report_id in reports_ids:
                report_instance = Report.objects.get(id=report_id)
                report_instance.is_deleted = False
                report_instance.save()
        # アクションが完全に削除する場合
        elif action == "delete":
            for report_id in reports_ids:
                report_instance = Report.objects.get(id=report_id)
                report_instance.delete()
        # リダイレクト先を、前のページにする
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "manager/reports_dustbox.html", context)

# ユーザー一覧
@user_passes_test(check_user_admin_staff)
def users_list(request):
    users_list = User.objects.all().order_by('last_name')
    paginator = Paginator(users_list, 10)  # 1ページに10件表示
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, "manager/users_list.html", {'users': users})

# ユーザー追加
@user_passes_test(check_user_admin)
def add_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # メールアドレスの重複チェック (User モデルと EmailAddress モデルの両方)
            email_exists_in_user = User.objects.filter(email__iexact=email).exists()
            email_exists_in_emailaddress = EmailAddress.objects.filter(email__iexact=email).exists()
            
            if email_exists_in_user or email_exists_in_emailaddress:
                return JsonResponse(
                    {'success': False, 'errors': {'email': ['このメールアドレスは既に使用されています。']}},
                    status=400
                )
            
            # ユーザーの作成
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # スタッフまたは管理者の場合、メール認証をスキップ
            if user.is_staff or user.is_superuser:
                EmailAddress.objects.create(
                    user=user,
                    email=user.email,
                    verified=True,
                    primary=True
                )
            else:
                # 通常ユーザーの場合はメール認証を必要とする
                EmailAddress.objects.create(
                    user=user,
                    email=user.email,
                    verified=False,
                    primary=True
                )
            
            return JsonResponse(
                {'success': True, 'message': 'ユーザーが正常に追加されました。'}
            )
        else:
            errors = form.errors.get_json_data()
            return JsonResponse(
                {'success': False, 'errors': errors},
                status=400
            )
    else:
        return JsonResponse(
            {'success': False, 'error': '無効なリクエストです。'},
            status=400
        )


#アーカイブコンテンツ一覧
@user_passes_test(check_user_admin_staff)
def upload_list(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    sort = request.GET.get('sort', '-insert_at')
    file_id = request.GET.get('file_id', '') 
    keyword = request.GET.get('keyword', '')
    start_date = request.GET.get('start_date')
    if start_date == 'None':
        start_date = None
    end_date = request.GET.get('end_date')
    if end_date == 'None':
        end_date = None
    title = request.GET.get('title', '')
    published = request.GET.get('published', '')
    is_unedited = request.GET.get('is_unedited', '')  # 新規追加

    uploads = Upload.objects.all().exclude(delete_flag=True)

    # フィルタリング
    if file_id:
        uploads = uploads.filter(file_id=file_id)
    if keyword:
        uploads = uploads.filter(Q(title__icontains=keyword) | Q(comment__icontains=keyword) | Q(file_name__icontains=keyword) | Q(file_path__icontains=keyword) | Q(tags__name__icontains=keyword))
    if start_date:
        uploads = uploads.filter(insert_at__date__gte=start_date)
    if end_date:
        uploads = uploads.filter(insert_at__date__lte=end_date)
    if title:
        uploads = uploads.filter(title__icontains=title)
    if published:
        uploads = uploads.filter(published=(published == '1'))
    if is_unedited:
        uploads = uploads.filter(is_unedited=(is_unedited == '1'))  # 新規追加

    # ソート
    uploads = uploads.order_by(sort)
    
    paginator = Paginator(uploads, 10)  # 1ページに10件表示
    page = request.GET.get('page')
    try:
        uploads = paginator.page(page)
    except PageNotAnInteger:
        uploads = paginator.page(1)
    except EmptyPage:
        uploads = paginator.page(paginator.num_pages)

    context = {
        "file_id": file_id,
        'uploads': uploads,
        'sort': sort,
        'keyword': keyword,
        'start_date': start_date,
        'end_date': end_date,
        'title': title,
        'published': published,
        'is_unedited': is_unedited,  # 新規追加
    }
    # POSTメソッドによるリクエストを処理
    if request.method == 'POST':
        # 'file_ids'で取得したIDを数値リストに変換
        file_ids = request.POST.get('file_ids').split(',')
        file_ids = list(map(int, file_ids))

        action = request.POST.get('action')

        print(f"選択されたID:{file_ids}")
        print(f"選択されたアクション:{action}")

        # アクションが公開する場合
        if action == "public":
            for file_id in file_ids:
                upload_instance = Upload.objects.get(file_id=file_id)
                upload_instance.published = True
                upload_instance.save()
        
        # アクションが非公開にする場合
        elif action == "unpublic":
            for file_id in file_ids:
                upload_instance = Upload.objects.get(file_id=file_id)
                upload_instance.published = False
                upload_instance.save()

        # アクションが削除する場合
        elif action == "delete":
            for file_id in file_ids:
                upload_instance = Upload.objects.get(file_id=file_id)
                upload_instance.delete_flag = True
                upload_instance.save()

        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, "manager/upload_list.html", context)

# アーカイブコンテンツの一括アップロード
@user_passes_test(check_user_admin_staff)
def uploads(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    categories = get_category_choices()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'manager/uploads.html', context)

@user_passes_test(check_user_admin_staff)
def uploads_ajax(request):
    if not can_edit_upload(request.user):
        return JsonResponse({'success': False, 'error': '権限がありません。'}, status=403)
    if request.method == 'POST':
        # アップロードされたファイルを取得
        uploaded_files = request.FILES.getlist('upload_files')
        # カテゴリーを取得
        category = request.POST.get('category')
        # 公開フラグを取得
        published = request.POST.get('published')
        # タグを取得
        tags = request.POST.get('tags')
        # POST変換
        # カテゴリー
        if category:
            print(category)
            category = Category.objects.get(id=category)
        else:
            print("カテゴリーが選択されていません。")
            category = None
        # 公開フラグ
        if published == '1':
            published = True
        else:
            published = False
        # タグ
        tags_list = tags.split(',')
        
        max_files = 100
        if len(uploaded_files) > max_files:
            return JsonResponse({'success': False, 'error': f'最大アップロード件数は{max_files}件です。'}, status=400)
        
        # ファイルの保存先ディレクトリを指定
        upload_dir = settings.MEDIA_ROOT
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in uploaded_files:
            original_name = file.name
            name, ext = os.path.splitext(original_name)
            counter = 1
            new_name = original_name
            file_path = os.path.join(upload_dir, new_name)
            
            # 同じファイル名が存在する場合、(1), (2), ... を付けて新しい名前を生成
            while os.path.exists(file_path):
                new_name = f"{name}({counter}){ext}"
                file_path = os.path.join(upload_dir, new_name)
                counter += 1

            
            
            # ファイルを保存
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # アップロードコンテンツとしてモデルに登録
            upload=Upload.objects.create(
                title=new_name,
                file_name=new_name,
                file_path=os.path.join(settings.MEDIA_URL, new_name),
                comment='',
                insert_at=timezone.now(),
                update_at=timezone.now(),
                user_id=request.user.id,
                published=published,
                is_unedited=True,
            )
            # カテゴリーの処理
            if category:
                upload.categories.add(category)
            # タグの処理
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip())
                upload.tags.add(tag)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': '無効なリクエストです。'}, status=400)
#アーカイブコンテンツのアップロード機能　ページ表示
@user_passes_test(check_user_admin_staff)
def upload(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    categories = get_category_choices()
    tags = Tag.objects.all()
    return render(request, 'manager/upload.html', {'categories': categories, 'tags': tags})


# アーカイブコンテンツをアップロードするための関数(おそらく使っていない)
@user_passes_test(check_user_admin_staff)
def upload_file(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    print("アップロードファイル")
    if request.method =='POST':
        print("POSTを受け取りました。")
        location = os.path.join(settings.MEDIA_ROOT)
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        if request.POST.get('type_select') == '1':
            print("ファイルアップロード")
            #ファイルアップロード
            if 'upload_file' in request.FILES:
                print("ファイルがアップロードされました。")
                uploaded_file = request.FILES['upload_file']
                fs = FileSystemStorage(location=location)
                name = fs.save(uploaded_file.name, uploaded_file)
                # url = fs.url(name)
                url = fs.base_url +"/" + name
            else:
                print("ファイルがアップロードされていません。")
                return HttpResponse('ファイルがアップロードされていません。', status=400)

        elif request.POST.get('type_select') == '2':
            # YouTube動画
            print("YouTube動画")
            url = request.POST.get('URL')
            url = get_youtube_embed_code(url,url_only=True)
            name = "YouTube"
        published = request.POST.get('published')
        # データベースに保存
        Upload.objects.create(title=title,comment=comment,file_name=name,file_path=url,published=published,is_unedited=False,user_id=request.user.id)
        messages.success(request, 'アップロードが完了しました。')
        return redirect('upload')
    else:
        messages.error(request, 'アップロードに失敗しました。')
        return HttpResponse('アップロードに失敗しました。')

# アーカイブコンテンツの編集
@user_passes_test(check_user_admin_staff)
def upload_edit(request, file_id):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    upload = get_object_or_404(Upload, file_id=file_id)
    tags=Tag.objects.all()
    content_type = file_type_check(basename(upload.file_path))
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, instance=upload)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, 'コンテンツが更新されました。')
            return redirect('upload_edit', file_id=file_id)
        else:
            print(form.errors)
            messages.error(request,f"エラーが発生しました:{form.errors}")
    else:
        form = UploadForm(instance=upload)
    return render(request, "manager/upload_edit.html", {'form': form, 'upload': upload,'tags':tags,'content_type':content_type})



# アップロードコンテンツの文字抽出
@user_passes_test(check_user_admin_staff)
def upload_ocr(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    print("アップロードコンテンツの文字抽出")
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        upload = get_object_or_404(Upload, file_id=file_id)
        # extract_text_from_pdfによる処理
        try:
            data = extract_text_from_pdf(upload)
            upload.extracted_text = data
            upload.save()
        except Exception as e:
            messages.error(request, f"エラーが発生しました:{e}")
            return HttpResponse(f"エラーが発生しました:{e}", status=400)
    messages.error(request, '不正なリクエストです。')
    return HttpResponse('不正なリクエストです。')

"""
アップロードコンテンツのGPTによる処理
ajaxでリクエストを受け取り、GPTによる処理を行う
"""
@user_passes_test(check_user_admin_staff)
def upload_gpt(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    print("アップロードコンテンツのGPTによる処理")
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        action = request.POST.get('action')
        upload = get_object_or_404(Upload, file_id=file_id)
        # GPTによる処理
        gpt = GPT()
        data = {}
        code = 500
        try:
            # 画像の説明を行う
            if action == 'describe':
                gpt.file_path = upload.file_path
                gpt.describe_image()
                code = 200
                data['message'] = gpt.get_response_message()
                data['status_code'] = code
                return JsonResponse(data)
                # テスト
                # import time
                # time.sleep(50)
                # return JsonResponse({'message': 'テスト' * 100,"status_code":200})
            # 画像のタグを取得する
            elif action == 'tag':
                gpt.file_path = upload.file_path
                tags_dict=gpt.generate_tags()
                code = 200
                # tags_dictから説明を省いたタグのみを取得
                tags = [tag['tag'] for tag in tags_dict.get('tags', [])]
                data['tags'] = tags
                data['status_code'] = code
                return JsonResponse(data)
        except Exception as e:
            data['message'] = str(e)
            data['status_code'] = code
        return JsonResponse(data)
    messages.error(request, '不正なリクエストです。')
    return HttpResponse('不正なリクエストです。')
"""
アップロードコンテンツのollamaによる処理
ajaxでリクエストを受け取り、ollamaによる処理を行う
"""
@user_passes_test(check_user_admin_staff)
def upload_ollama(request):
    print("アップロードコンテンツのollamaによる処理1")
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    try:
        # 設定ファイルの読み込み
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error reading config file: {e}")
        return False
    # 設定ファイルからollamaが有効かどうかを取得
    ollama_enabled = config.get('AI', {}).get('enabled', False)
    print(ollama_enabled)
    if not ollama_enabled:
        print("OLLAMA機能は無効です。")
        return JsonResponse({'success': False, 'error': 'OLLAMA機能は無効です。'}, status=403)
    print("アップロードコンテンツのollamaによる処理2")
    if request.method == 'POST':
        print("POSTを受け取りました。")
        file_id = request.POST.get('file_id')
        action = request.POST.get('action')
        upload = get_object_or_404(Upload, file_id=file_id)
        # ollamaによる処理
        ollama_client = OllamaClient()
        data = {}
        code = 500
        try:
            # 画像の説明を行う
            if action == 'describe':
                print("画像の説明を行う")
                code = 200
                print(upload.file_path)
                data['message'] = ollama_client.describe_image(image_path = upload.file_path)
                data['status_code'] = code
                return JsonResponse(data)
            # 画像のタグを取得する
            elif action == 'tag':
                print("画像のタグを取得する")
                tags_dict_json = ollama_client.generate_tags_with_image(upload.file_path)
                print(f"tags_dict_json:{tags_dict_json}")
                tags_dict = json.loads(tags_dict_json)
                print(f"tags_dict:{tags_dict}")
                code = 200
                print(f"tags_dict:{tags_dict}")
                tags = tags_dict.get('tags', [])
                print(f"tags!!!:{tags}")
                data['tags'] = tags
                print(tags)
                data['status_code'] = code
                return JsonResponse(data)
        except Exception as e:
            print("エラーが発生しました。")
            print(e)
            # data['message'] = str(e)
            # data['status_code'] = code
            return JsonResponse({'success': False, 'error': f'エラーが発生しました。;{e}'}, status=500)
    messages.error(request, '不正なリクエストです。')
    return HttpResponse('不正なリクエストです。')

# AIによるアーカイブコンテンツの処理
@user_passes_test(check_user_admin_staff)
def upload_ai(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        action = request.POST.get('action')
        upload = get_object_or_404(Upload, file_id=file_id)
        data = {}
        # AIによる処理
        # configからGPTかOLLAMAかを取得
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        ai_model = config.get('AI', {}).get('model', 'gpt')
        if ai_model == 'gpt':
            try:
                gpt = GPT()
                if action == 'describe':
                    gpt.file_path = upload.file_path
                    gpt.describe_image()
                    code = 200
                    data['message'] = gpt.get_response_message()
                elif action == 'tag':
                    gpt.file_path = upload.file_path
                    tags_dict = gpt.generate_tags()
                    code = 200
                    tags = [tag['tag'] for tag in tags_dict.get('tags', [])]
                    data['tags'] = tags
                elif action == 'title':
                    gpt.file_path = upload.file_path
                    code = 200
                    data['message'] = gpt.generate_title()
            except Exception as e:
                data['message'] = str(e)
                code = 500
        elif ai_model == 'ollama':
            try:
                ollama_client = OllamaClient()
                if action == 'describe':
                    code = 200
                    data['message'] = ollama_client.describe_image(image_path=upload.file_path)
                elif action == 'tag':
                    tags_dict_json = ollama_client.generate_tags_with_image(upload.file_path)
                    tags_dict = json.loads(tags_dict_json)
                    code = 200
                    tags = tags_dict.get('tags', [])
                    data['tags'] = tags
                elif action == 'title':
                    code = 200
                    data['message'] = ollama_client.generate_title_with_image(upload.file_path)
            except Exception as e:
                data['message'] = str(e)
                code = 500
        data['status_code'] = code
        return JsonResponse(data)
# ユーザー一覧
@user_passes_test(check_user_admin)
def users(request):
    users = User.objects.all()
    content = {"users": users}
    return render(request, 'manager/users.html', content)

# お知らせ一覧
@user_passes_test(check_user_admin_staff)
def announcements(request):
    if not can_edit_announcement(request.user):
        return HttpResponse('権限がありません。', status=403)
    if request.method == "POST":
        action = request.POST.get('action')
        announcement_ids = request.POST.get('announcement_ids', '').split(',')
        if action == 'delete':
            for announcement_id in announcement_ids:
                announcement = get_object_or_404(Announcement, id=int(announcement_id))
                announcement.is_deleted = True
                announcement.save()
        elif action == 'unpublish':
            for announcement_id in announcement_ids:
                announcement = get_object_or_404(Announcement, id=int(announcement_id))
                announcement.is_public = False
                announcement.save()
        elif action == 'publish':
            for announcement_id in announcement_ids:
                announcement = get_object_or_404(Announcement, id=int(announcement_id))
                announcement.is_public = True
                announcement.save()
        return redirect('announcements')

    sort = request.GET.get('sort', '-created_at')
    announcement_id = request.GET.get('announcement_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    keyword = request.GET.get('keyword')
    title = request.GET.get('title')
    include_unpublished = request.GET.get('include_unpublished', 'all')

    announcements = Announcement.objects.filter(is_deleted=False).order_by(sort)

    if announcement_id:
        announcements = announcements.filter(id=announcement_id)
    if start_date:
        announcements = announcements.filter(created_at__gte=start_date)
    if end_date:
        announcements = announcements.filter(created_at__lte=end_date)
    if keyword:
        announcements = announcements.filter(description__icontains=keyword)
    if title:
        announcements = announcements.filter(title__icontains=title)
    if include_unpublished == 'published':
        announcements = announcements.filter(is_public=True)
    elif include_unpublished == 'unpublished':
        announcements = announcements.filter(is_public=False)

    context = {
        'announcements': announcements,
        'sort': sort,
        'announcement_id': announcement_id,
        'start_date': start_date,
        'end_date': end_date,
        'keyword': keyword,
        'title': title,
        'include_unpublished': include_unpublished,
    }
    return render(request, 'manager/announcements.html', context)
# お知らせの作成
@user_passes_test(check_user_admin_staff)
def announcement_create(request):
    if not can_edit_announcement(request.user):
        return HttpResponse('権限がありません。', status=403)
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_public = request.POST.get('is_public') == '1'
        is_html = request.POST.get('is_html') == '1'

        announcement_id = request.POST.get('announcement_id')
        if announcement_id:
            announcement = get_object_or_404(Announcement, id=announcement_id)
            announcement.title = title
            announcement.description = description
            announcement.updated_at = timezone.now()
            announcement.updated_by = request.user
            announcement.is_public = is_public
            announcement.is_html = is_html
        else:
            if title == '' or description == '':
                return HttpResponse('タイトルと内容は必須です。')
            announcement = Announcement(
                title=title,
                description=description,
                created_by=request.user,
                updated_by=request.user,
                is_public=is_public,
                is_html=is_html,
            )
        announcement.save()
        messages.success(request, 'お知らせを作成しました。')
        return redirect('announcements')  # 適切なリダイレクト先に変更

    else:
        announcement = None
        if 'announcement_id' in request.GET:
            announcement_id = request.GET.get('announcement_id')
            announcement = get_object_or_404(Announcement, id=announcement_id)
        
        context = {
            'announcement': announcement,
        }
        
        return render(request, 'manager/announcement_create.html', context)
# おしらせの編集
@user_passes_test(check_user_admin_staff)
def announcement_edit(request, announcement_id):
    if not can_edit_announcement(request.user):
        return HttpResponse('権限がありません。', status=403)
    announcement = get_object_or_404(Announcement, id=announcement_id)

    if request.method == "POST":
        announcement.title = request.POST.get('title')
        announcement.description = request.POST.get('description')
        announcement.updated_at = timezone.now()
        announcement.updated_by = request.user
        announcement.is_public = request.POST.get('is_public') == '1'
        announcement.is_html = request.POST.get('is_html') == '1'

        announcement.save()
        messages.success(request, 'お知らせを更新しました。')
        return redirect('announcements')  # 適切なリダイレクト先に変更

    return render(request, 'manager/announcement_edit.html', {'announcement': announcement})

# タグ管理
@user_passes_test(check_user_admin_staff)
def tags(request):
    if not can_edit_tag(request.user):
        return HttpResponse('権限がありません。', status=403)
    # タグに関連するアップロードコンテンツ数と記事数をアノテーション
    tags = Tag.objects.annotate(
        upload_count=Count('upload_models', distinct=True),
        report_count=Count('report_models', distinct=True)
    )
    tags_count = tags.count()
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'name')  # デフォルトのソートは名前順

    if search:
        tags = tags.filter(Q(name__icontains=search) | Q(description__icontains=search))

    # 並び替えのロジック
    if sort == 'upload_count_desc':
        tags = tags.order_by('-upload_count')
    elif sort == 'upload_count_asc':
        tags = tags.order_by('upload_count')
    elif sort == 'report_count_desc':
        tags = tags.order_by('-report_count')
    elif sort == 'report_count_asc':
        tags = tags.order_by('report_count')
    else:
        tags = tags.order_by('name')  # 名前順

    paginator = Paginator(tags, 30)  # 1ページに30件表示
    page = request.GET.get('page')

    try:
        tags_page = paginator.page(page)
    except PageNotAnInteger:
        tags_page = paginator.page(1)
    except EmptyPage:
        tags_page = paginator.page(paginator.num_pages)

    context = {
        'tags': tags_page,
        'tags_count': tags_count,
        'search': search,
        'sort': sort,
    }
    return render(request, 'manager/tags.html', context)

# タグの削除
@user_passes_test(check_user_admin)
def tags_bulk_delete_unused(request):
    if not can_edit_tag(request.user):
        return HttpResponse('権限がありません。', status=403)
    if request.method == 'POST':
        # POSTデータからタグIDを取得
        tag_ids = request.POST.getlist('tag_ids')
        if not tag_ids:
            return HttpResponse('削除対象のタグが選択されていません。', status=400)

        # 未使用のタグのみをフィルタリング
        unused_tags = Tag.objects.annotate(
            upload_count=Count('upload_models', distinct=True),
            report_count=Count('report_models', distinct=True)
        ).filter(id__in=tag_ids, upload_count=0, report_count=0)

        deleted_count = unused_tags.count()
        unused_tags.delete()

        # メッセージを表示するためにリダイレクト
        # ここではメッセージフレームワークを使用してメッセージを渡すことができます
        # 例: messages.success(request, f"{deleted_count} 件の未使用タグを削除しました。")
        messages.success(request, f"{deleted_count} 件の未使用タグを削除しました。")
        return redirect('tags')  # 'tags' はURL名として定義されていることを前提とします
    else:
        messages.error(request, '不正なリクエストです。')
        return HttpResponse('不正なリクエストです。', status=400)

# タグ詳細
@user_passes_test(check_user_admin_staff)
def tag_detail(request, name):
    if not can_edit_tag(request.user):
        return HttpResponse('権限がありません。', status=403)
    tag = get_object_or_404(Tag, name=name)
    
    # レポートのページネーション
    reports_list = Report.objects.filter(tags=tag, is_deleted=False)
    report_page = request.GET.get('report_page', 1)
    report_paginator = Paginator(reports_list, 10)  # 1ページに10件表示
    try:
        reports = report_paginator.page(report_page)
    except PageNotAnInteger:
        reports = report_paginator.page(1)
    except EmptyPage:
        reports = report_paginator.page(report_paginator.num_pages)

    # アップロードコンテンツのページネーション
    uploads_list = Upload.objects.filter(tags=tag, delete_flag=False)
    upload_page = request.GET.get('upload_page', 1)
    upload_paginator = Paginator(uploads_list, 10)  # 1ページに10件表示
    try:
        uploads = upload_paginator.page(upload_page)
    except PageNotAnInteger:
        uploads = upload_paginator.page(1)
    except EmptyPage:
        uploads = upload_paginator.page(upload_paginator.num_pages)

    context = {
        'tag': tag,
        'reports': reports,
        'uploads': uploads,
    }
    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            # タグの削除
            tag.delete()
            messages.success(request, 'タグを削除しました。')
        return redirect('tags')
    return render(request, 'manager/tag_detail.html', context)

# 設定ページ
@user_passes_test(check_user_admin, login_url='/accounts/login/')
def config_page(request):
    # 設定の読み込み
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    if config['AI']['model'] == 'ollama' and config['AI']['enabled']:
        try:
            list_models = OllamaClient().list_models()
        except Exception as e:
            list_models = []
            logger.error(f"Error getting OLLAMA models: {e}")
            messages.error(request, 'OLLAMAモデルの取得に失敗しました。')
            messages.error(request, '返されたエラー: ' + str(e))
            messages.error(request, 'APIサーバーが起動しているか確認してください。')
    else:
        list_models = []
    config['ollama_models'] = list_models
    if request.method == 'POST':
        # 設定の更新
        config['location_address'] = request.POST.get('location_address')
        config['location_name'] = request.POST.get('location_name')
        config['location_tel'] = request.POST.get('location_tel')
        config['location_web'] = request.POST.get('location_web')
        config['site_title'] = request.POST.get('site_title')
        config['top_page']['show_recommend'] = request.POST.get('show_recommend') == 'on'
        config['top_page']['show_recent'] = request.POST.get('show_recent') == 'on'
        config['about_page']['title'] = request.POST.get('about_title')
        config['about_page']['content'] = request.POST.get('about_content')
        # スタッフ権限
        # 記事を編集できる
        config['staff_authority']['can_edit_report'] = request.POST.get('can_edit_report') == 'on'
        # アップロードコンテンツを編集できる
        config['staff_authority']['can_edit_upload'] = request.POST.get('can_edit_upload') == 'on'
        # お知らせを編集できる
        config['staff_authority']['can_edit_announcement'] = request.POST.get('can_edit_announcement') == 'on'
        # タグを編集できる
        config['staff_authority']['can_edit_tag'] = request.POST.get('can_edit_tag') == 'on'
        # カテゴリーを編集できる
        config['staff_authority']['can_edit_category'] = request.POST.get('can_edit_category') == 'on'
        # AI設定
        config['AI']['enabled'] = request.POST.get('ai_enabled') == 'on'
        config['AI']['model'] = request.POST.get('ai_model')
        config['AI']['gpt']['model_name'] = request.POST.get('gpt_model_name')
        config['AI']['gpt']['url'] = request.POST.get('gpt_url')
        config['AI']['gpt']['api_key'] = request.POST.get('gpt_api_key')
        config['AI']['gpt']['max_tokens'] = int(request.POST.get('gpt_max_tokens', 300))
        config['AI']['ollama']['model_name'] = request.POST.get('ollama_model_name')
        config['AI']['ollama']['url'] = request.POST.get('ollama_url')
        # 設定の保存
        with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, default_flow_style=False, allow_unicode=True)
        messages.success(request, '設定を更新しました。')
        return redirect('config_page')
    return render(request, 'manager/config_page.html', config)

# ゴミ箱のアップロードコンテンツ一覧
@user_passes_test(check_user_admin_staff)
def uploads_dustbox(request):
    if not can_edit_upload(request.user):
        return HttpResponse('権限がありません。', status=403)
    sort = 'insert_at'
    file_id = ''
    uploads = ''
    keyword = ''
    start_date = None
    end_date = None
    title = ''
    user_id = ''
    published = ''
    
    if request.method == 'GET':
        file_id = request.GET.get('file_id')
        sort = request.GET.get('sort', 'insert_at')
        keyword = request.GET.get('keyword', '')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        title = request.GET.get('title', '')
        user_id = request.GET.get('user_id')
        published = request.GET.get('published')
        query = Q(delete_flag=True)
        if file_id:
            query &= Q(file_id=file_id)
        if keyword:
            query &= Q(title__icontains=keyword) | Q(comment__icontains=keyword) | Q(file_name__icontains=keyword)
        if start_date:
            query &= Q(insert_at__gte=start_date)
        if end_date:
            query &= Q(insert_at__lte=end_date)
        if title:
            query &= Q(title__icontains=title)
        if user_id:
            query &= Q(user_id=user_id)
        # 公開の場合
        if published == "1":
            query &= Q(published='1')
        # 非公開の場合
        elif published == "0":
            query &= Q(published='0')

        uploads = Upload.objects.filter(query).order_by(sort)
    
    context = {
        "file_id": file_id,
        'uploads': uploads,
        'sort': sort,
        'keyword': keyword,
        'start_date': start_date,
        'end_date': end_date,
        'title': title,
        'user_id': user_id,
        'published': published,
    }
    # POSTメソッドによるリクエストを処理
    if request.method == 'POST':
        # 'file_ids'で取得したIDを数値リストに変換
        file_ids = request.POST.get('file_ids').split(',')
        file_ids = list(map(int, file_ids))
        action = request.POST.get('action')
        # アクションが完全に削除する場合
        if action == "delete":
            for file_id in file_ids:
                upload_instance = Upload.objects.get(file_id=file_id)
                upload_instance.delete()
                # ファイルの削除
                file_path = os.path.join(settings.MEDIA_ROOT, upload_instance.file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        # アクションが復元する場合
        elif action == "restore":
            for file_id in file_ids:
                upload_instance = Upload.objects.get(file_id=file_id)
                upload_instance.delete_flag = False
                upload_instance.save()

        return redirect(request.META.get('HTTP_REFERER'))
    return render(request, "manager/uploads_dustbox.html", context)

@csrf_exempt
@user_passes_test(check_user_admin_staff)
def upload_ajax(request):
    if not can_edit_upload(request.user):
        return JsonResponse({'success': False, 'error': '権限がありません。'}, status=403)
    print("アップロードコンテンツのAjax")
    if request.method == 'POST':
        print("アップロードコンテンツのAjaxのPOSTを受け取りました。")
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        published = request.POST.get('published') == '1'
        type_select = request.POST.get('type_select')
        upload_file = request.FILES.get('upload_file')
        url = request.POST.get('URL')
        categories = request.POST.getlist('categories')
        tags = request.POST.get('tags')
        if type_select == '1':
            if not upload_file:
                return JsonResponse({'success': False, 'error': 'ファイルが選択されていません。'})

            fs = FileSystemStorage()
            original_name = upload_file.name
            name, ext = os.path.splitext(original_name)
            counter = 1
            new_name = original_name

            # 同じファイル名が存在する場合、(1), (2), ... を付けて新しい名前を生成
            while fs.exists(new_name):
                new_name = f"{name}({counter}){ext}"
                counter += 1

            filename = fs.save(new_name, upload_file)
            file_url = fs.url(filename)
            file_name = new_name

            if not title:
                title = file_name
        elif type_select == '2':
            if not url:
                return JsonResponse({'success': False, 'error': 'YouTubeのURLを入力してください。'})
            file_url = url
            file_name = ''
            if not title:
                title = 'YouTube'
        else:
            return JsonResponse({'success': False, 'error': '無効なファイルの種類が選択されました。'})
        tags_list = tags.split(',')
        upload=Upload.objects.create(
            title=title,
            comment=comment,
            file_name=file_name,
            file_path=file_url,
            published=published,
            is_unedited=False,
            user_id=request.user.id
        )
        # カテゴリーを保存
        for category_id in categories:
            category = Category.objects.get(id=category_id)
            upload.categories.add(category)
        # タグを保存
        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            upload.tags.add(tag)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': '無効なリクエストです。'}, status=400)

# カテゴリー一覧
@user_passes_test(check_user_admin_staff)
def category_list(request):
    if not can_edit_category(request.user):
        return HttpResponse('権限がありません。', status=403)
    # フィルタリングパラメータを取得
    name = request.GET.get('name', '')
    parent_id = request.GET.get('parent', '')
    is_active = request.GET.get('is_active', '')
    # フィルタリング
    categories_queryset = Category.objects.all().order_by('name')
    #　親カテゴリに属していないカテゴリを取得
    if parent_id == 'none':
        categories_queryset = categories_queryset.filter(parent=None)
    # すべてのカテゴリを取得
    elif parent_id == 'all' or parent_id == '':
        pass
    # IDが指定された親カテゴリに属するカテゴリを取得
    else:
        categories_queryset = categories_queryset.filter(parent_id=parent_id)

    if name:
        categories_queryset = categories_queryset.filter(name__icontains=name)
    if is_active:
        categories_queryset = categories_queryset.filter(is_active=is_active)
    # get_category_choicesを使用して順序付け
    ordered_choices = get_category_choices()
    ordered_ids = [choice[0] for choice in ordered_choices]
    print(f"ordered_ids:{ordered_ids}")
    print(f"ordered_choices:{ordered_choices}")
    # フィルタリングされたカテゴリIDを取得
    filtered_ids = set(categories_queryset.values_list('id', flat=True))

    # フィルタリングされたカテゴリのみを保持
    filtered_ordered_ids = [id for id in ordered_ids if id in filtered_ids]
    # CaseとWhenを使用して順序付け
    preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(filtered_ordered_ids)])
    categories_ordered = Category.objects.filter(id__in=filtered_ordered_ids).order_by(preserved_order)
    # ページネーション設定
    paginator = Paginator(categories_ordered, 10)  # 1ページに10件表示
    page_number = request.GET.get('page')
    
    try:
        paginated_categories = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_categories = paginator.page(1)
    except EmptyPage:
        paginated_categories = paginator.page(paginator.num_pages)
    
    # 親カテゴリーの選択肢を取得（フォーム用）
    all_categories = get_category_choices(categories=Category.objects.all(), parent=None)
    context = {
        'categories': paginated_categories,
        'all_categories': all_categories,  # フィルタフォーム用に階層順のカテゴリを提供
    }

    return render(request, 'manager/category_list.html', context)
# カテゴリー作成
@user_passes_test(check_user_admin_staff)
def category_create(request):
    if not can_edit_category(request.user):
        return HttpResponse('権限がありません。', status=403)
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        description = request.POST.get('description')
        parent_id = request.POST.get('parent')
        is_active = request.POST.get('is_active') == 'on'

        parent = None
        if parent_id:
            try:
                parent = Category.objects.get(id=parent_id)
            except Category.DoesNotExist:
                messages.error(request, '選択された親カテゴリーが存在しません。カテゴリーは作成されませんでした。')
                return redirect('category_create')

        category = Category(
            name=name,
            description=description,
            parent=parent,
            is_active=is_active
        )

        try:
            category.full_clean()  # バリデーションを実行
            category.save()
            messages.success(request, f"カテゴリー「{name}」を作成しました。")
            return redirect('category_create')
        except ValidationError as e:
            # バリデーションエラーを個別にメッセージとして追加
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, error)
    else:
        # GETリクエスト時の処理（フォームの初期化など）
        pass

    categories = get_category_choices()
    return render(request, 'manager/category_create.html', {'categories': categories})
# カテゴリー統合 リクエストは受けない
def merge_categories(source_category, target_category):
    """
    source_category を target_category に統合し、関連するコンテンツを移行します。
    """
    # 関連するアップロードコンテンツを統合
    Upload.objects.filter(category=source_category).update(category=target_category)
    # 必要に応じて他の関連モデルも統合（例：Reportモデル）
    # Report.objects.filter(category=source_category).update(category=target_category)
    # 統合後、元のカテゴリーを削除
    source_category.delete()
    
# カテゴリー編集
@user_passes_test(check_user_admin_staff)
def category_edit(request, category_id):
    if not can_edit_category(request.user):
        return HttpResponse('権限がありません。', status=403)
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        description = request.POST.get('description')
        parent_id = request.POST.get('parent')
        is_active = request.POST.get('is_active') == 'on'

        new_parent = None
        if parent_id:
            try:
                new_parent = Category.objects.get(id=parent_id)
            except Category.DoesNotExist:
                messages.error(request, '選択された親カテゴリーが存在しません。')
                return redirect('category_edit', category_id=category_id)

        # カテゴリー情報の更新
        category.name = name
        category.description = description
        category.parent = new_parent
        category.is_active = is_active

        try:
            category.full_clean()  # バリデーションを実行
            # 同じ親カテゴリー内に同名のカテゴリーが存在する場合
            if Category.objects.filter(parent=new_parent, name=name).exclude(pk=category.pk).exists():
                existing_category = Category.objects.get(parent=new_parent, name=name)
                merge_categories(category, existing_category)
                messages.success(request, 'カテゴリーが既存のカテゴリーと統合されました。')
                return redirect('category_list')
            else:
                category.save()
                messages.success(request, 'カテゴリーが更新されました。')
                return redirect('category_list')
        except ValidationError as e:
            print(e)
            # バリデーションエラーを個別にメッセージとして追加
            for field, errors in e.message_dict.items():
                for error in errors:
                    messages.error(request, error)
    else:
        # 初期表示時の処理
        pass

    categories = get_category_choices()
    return render(request, 'manager/category_edit.html', {'category': category, 'categories': categories})

# カテゴリー削除
@user_passes_test(check_user_admin_staff)
def category_delete(request, category_id):
    if not can_edit_category(request.user):
        return HttpResponse('権限がありません。', status=403)
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, 'カテゴリーが削除されました。')
    return redirect('category_list')


# システム情報
@user_passes_test(check_user_admin)
def system_info(request):
    # 変更履歴を取得
    with open(os.path.join(BASE_DIR, 'archive_system', 'system_history.yml'), 'r', encoding='utf-8') as file:
        system_history = yaml.safe_load(file)

    histories = system_history['histories']
    print(histories)
    # システム情報の取得
    #djangoのバージョンを取得する
    django_version = os.popen("django-admin --version").read()
    #サーバーのバージョンを取得する
    python_version = os.popen("python --version").read()
    #サーバーのバージョンを取得する
    mysql_version = os.popen("mysql --version").read()
    # ソフトウェアのバージョンを取得する
    software_version = system_history['version']
    #サーバーの情報を取得する
    server_info = os.uname()
    #サーバーのOS名を取得する
    server_os = server_info[0]
    #サーバーのホスト名を取得する
    server_hostname = server_info[1]
    #サーバーのOSバージョンを取得する
    server_version = server_info[2]
    #サーバーのOSのビット数を取得する
    server_bit = server_info[4]
    #サーバーのCPU情報を取得する
    server_cpu = " ".join(os.popen("lscpu").read().splitlines()[4:6])
    #サーバーのメモリ情報を取得する
    server_memory = os.popen("free -h").read()
    #サーバーのディスク情報を取得する
    server_disk = os.popen("df -h").read()
    #サーバーのIPアドレスを取得する
    server_ip = os.popen("hostname -I").read()
    content = {
        'django_version': django_version,
        'software_version': software_version,
        'python_version': python_version,
        'mysql_version': mysql_version,
        'server_os': server_os,
        'server_hostname': server_hostname,
        'server_version': server_version,
        'server_bit': server_bit,
        'server_cpu': server_cpu,
        'server_memory': server_memory,
        'server_disk': server_disk,
        'server_ip': server_ip,
        'histories': histories,
    }
    return render(request, 'manager/system_info.html', content)


