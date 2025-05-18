from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.template import loader
from .models import *
from django.db.models import Q
import re
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SearchForm
from .search import SearchFunction
import sys
from utils import *
import logging
from urllib.parse import quote
logger = logging.getLogger(__name__)
from django.conf import settings
import yaml
import subprocess
CONFIG_FILE = settings.CONFIG_FILE
BASE_DIR = settings.BASE_DIR
# コンテンツをの説明を抽出する関数
def extract_description(content:object):
    for i in range(len(content)):
        # HTMLタグを削除
        content[i].description = re.sub(r'<.*?>', '', content[i].description)
        # 説明文が50文字以上の場合は、50文字までにカットする
        content[i].description = content[i].description[:50]
        # もし、説明文が空の場合は、タイトルを代入する
        if content[i].description == "":
            content[i].description += content[i].title + "..."
#トップページ
def index(request):
    # 設定の読み込み
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Config file {CONFIG_FILE} not found.")
        messages.error(request, '設定ファイルが見つかりません。')
        return redirect('error_page')
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config file: {e}")
        messages.error(request, '設定ファイルの解析中にエラーが発生しました。')
        return redirect('error_page')
    logger.info("Viewing top page")
    # おすすめコンテンツ
    recommend_contents = Report.objects.filter(is_recommend=True, is_public=True).exclude(is_deleted=True).order_by('-created_at')[:9]
    extract_description(recommend_contents)
    # 最近のコンテンツ
    recent_contents = Report.objects.filter(is_public=True).exclude(is_deleted=True).order_by('-created_at')[:9]
    extract_description(recent_contents)
    # おしらせ
    announcements = Announcement.objects.filter(is_deleted=False, is_public=True).order_by('-created_at')[:5]
    
    return render(request, "ArchiveViewer/index.html", {
        'recommend_contents': recommend_contents,
        'recent_contents': recent_contents,
        'announcements': announcements,
        'config': config
    })
# アーカイブコンテンツを表示する
def upload_contents_detail(request, id):
    # 変数を初期化
    content_type = ""
    is_favorite = False
    try:
        upload_contents = Upload.objects.get(file_id=id)
        # 関連するコンテンツを取得する
        related_contents = Upload.objects.filter(tags__in=upload_contents.tags.all()).exclude(file_id=id).exclude(delete_flag=1).exclude(published=0).order_by('-update_at')[:5]
    except Upload.DoesNotExist:
        logger.warning(f"File with ID {id} does not exist.")
        raise Http404
    # 非公開のコンテンツで、スタッフとしてログインしていない場合は、401を返す
    if not upload_contents.published and (not request.user.is_authenticated or not request.user.is_staff):
        logger.info(f"File with ID {id} is not public and user is not authorized.")
        return HttpResponse('このページへのアクセスは許可されていません', status=401)
    # 削除されたコンテンツで、スタッフとしてログインしていない場合は、404を返す
    if upload_contents.delete_flag and (not request.user.is_authenticated or not request.user.is_staff):
        logger.info(f"File with ID {id} is deleted and user is not authorized.")
        raise Http404
    elif upload_contents.delete_flag and request.user.is_authenticated and request.user.is_staff:
        logger.info(f"File with ID {id} is deleted but user is authorized.")
        messages.warning(request, 'このコンテンツは削除されています。スタッフのみ閲覧可能です。')
    # 通常のコンテンツの処理
    else:
        logger.info(f"Viewing file with ID {id}")
        # もし、ログインしている場合の処理
        if request.user.is_authenticated:
            # 表示中のコンテンツがお気に入りに登録されているか判別する
            is_favorite = UploadFavorite.objects.filter(user_id=request.user.id, upload_id=id).exists()
            # UploadHistoryに閲覧履歴を追加する
            UploadHistory.objects.create(user=request.user, upload=upload_contents)

    # ファイルの種類を判定する
    # ファイルパスを取得し、拡張子を取得する
    content_type = file_type_check(upload_contents.file_path)
    # ファイルパスをエンコードする
    encoded_file_path=decode_url(upload_contents.file_path)
    content = {'upload_contents': upload_contents, 'content_type': content_type, 'is_favorite': is_favorite,'encoded_file_path':encoded_file_path, 'related_contents': related_contents}
    return render(request, "ArchiveViewer/upload_contents_detail.html", content)

# このシステムについてのページを表示する
def about(request):
    logger.info("Viewing about page")
    # 設定の読み込み
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Config file {CONFIG_FILE} not found.")
        messages.error(request, '設定ファイルが見つかりません。')
        return redirect('error_page')
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config file: {e}")
        messages.error(request, '設定ファイルの解析中にエラーが発生しました。')
        return redirect('error_page')
    about_contents = config['about_page']
    # djangoのバージョンを取得する
    django_version = subprocess.getoutput("django-admin --version")
    #サーバーのバージョンを取得する
    python_version = subprocess.getoutput("python --version")
    #サーバーのバージョンを取得する
    mysql_version = subprocess.getoutput("mysql --version")
    with open(os.path.join(BASE_DIR, 'archive_system', 'system_history.yml'), 'r', encoding='utf-8') as file:
        system_history = yaml.safe_load(file)
    # このシステムのバージョンを取得する
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
    server_cpu = ""
    #サーバーのメモリ情報を取得する
    server_memory = subprocess.getoutput("free -h")
    #サーバーのディスク情報を取得する
    server_disk = subprocess.getoutput("df -h")
    #サーバーのIPアドレスを取得する
    server_ip = subprocess.getoutput("hostname -I")
    content = {'server_os': server_os, 'server_hostname': server_hostname, 
               'server_version': server_version, 'server_bit': server_bit, 'server_cpu': server_cpu, 'server_memory': server_memory,
               'server_disk': server_disk, 'server_ip': server_ip,
                'python_version': python_version, 'mysql_version': mysql_version, 'django_version': django_version, 'software_version': software_version, 'about_contents': about_contents}
    return render(request, "ArchiveViewer/about.html", content)

# 記事のページを表示する
def report_contents_detail(request, id):
    logger.info(f"Viewing report with ID {id}")
    # 初期値
    is_favorite = False
    try:
        report_contents = Report.objects.get(id=id)
        # 関連するコンテンツを取得する
        related_reports = Report.objects.filter(tags__in=report_contents.tags.all()).exclude(id=id).exclude(is_deleted=True).exclude(is_public=False).order_by('-updated_at')[:5]
    except Report.DoesNotExist:
        logger.warning(f"Report with ID {id} does not exist.")
        raise Http404
    # 非公開のコンテンツで、スタッフとしてログインしていない場合は、401を返す
    if report_contents.is_public == False and (not request.user.is_authenticated or not request.user.is_staff):
        logger.info(f"Report with ID {id} is not public and user is not authorized.")
        return HttpResponse('このページへのアクセスは許可されていません', status=401)
    # 削除されたコンテンツで、スタッフとしてログインしていない場合は、404を返す
    if report_contents.is_deleted == True and (request.user.is_authenticated and request.user.is_staff):
        logger.info(f"Report with ID {id} is deleted but user is authorized.")
        messages.warning(request, 'このコンテンツは削除されています。スタッフのみ閲覧可能です。')
    elif report_contents.is_deleted == True:
        logger.info(f"Report with ID {id} is deleted.")
        raise Http404
    # 通常のコンテンツの処理
    else:
        logger.info(f"Viewing report with ID {id}")
        # ログインしている場合の処理
        if request.user.is_authenticated:
            # 表示中のコンテンツがお気に入りに登録されているか判別する
            is_favorite = ReportFavorite.objects.filter(user=request.user, report=report_contents).exists()
            # ReportHistoryに閲覧履歴を追加する
            ReportHistory.objects.create(user=request.user, report=report_contents)

    content = {'report_contents': report_contents, 'is_favorite': is_favorite, 'related_reports': related_reports }
    return render(request, "ArchiveViewer/report_contents_detail.html", content)

def search_page(request):
    return render(request, "ArchiveViewer/search.html")

def search(request):
    logger.info("Searching for content")
    form = SearchForm(request.GET or None)
    if request.method == 'GET' and form.is_valid():
        raw_keywords = form.cleaned_data['keyword']
        search_results_upload = None
        search_results_report = None
        # アーカイブ検索のみ
        if form.cleaned_data['searchOption']== 'upload':
            search_results_upload = SearchFunction().upload_search(raw_keywords)
            # ページネーション 1ページに10件表示
            paginator = Paginator(search_results_upload, 10)
            page = request.GET.get('page')
            try:
                search_results_upload = paginator.page(page)
            except PageNotAnInteger:
                search_results_upload = paginator.page(1)
            except EmptyPage:
                search_results_upload = paginator.page(paginator.num_pages)
            return render(request, "ArchiveViewer/upload_search_results.html", {'form': form, 'search_results_upload': search_results_upload, 'search_results_report': search_results_report})
        elif form.cleaned_data['searchOption']== 'report':
            search_results_report = SearchFunction().report_search(raw_keywords)
            extract_description(search_results_report)
            # ページネーション 1ページに10件表示
            paginator = Paginator(search_results_report, 10)
            page = request.GET.get('page')
            try:
                search_results_report = paginator.page(page)
            except PageNotAnInteger:
                search_results_report = paginator.page(1)
            except EmptyPage:
                search_results_report = paginator.page(paginator.num_pages)
            return render(request, "ArchiveViewer/report_search_results.html", {'form': form, 'search_results_upload': search_results_upload, 'search_results_report': search_results_report})
    else:
        #フォーム未入力の場合は前のぺージに戻る
        return redirect(request.META.get('HTTP_REFERER'))
        

# おしらせ詳細
def announcement_detail(request, announcement_id):
    logger.info(f"Viewing announcement with ID {announcement_id}")
    announcement = get_object_or_404(Announcement, id=announcement_id)
    # 非公開かつ、ユーザーがスタッフではない場合は401を返す
    if not announcement.is_public and (not request.user.is_authenticated or not request.user.is_staff):
        return HttpResponse('このページへのアクセスは許可されていません', status=401)
    return render(request, 'ArchiveViewer/announcement_detail.html', {'announcement': announcement})
# お知らせ一覧
def announcements_list(request):
    logger.info("Viewing list of announcements")
    # 非公開のお知らせを除外
    announcements = Announcement.objects.filter(is_deleted=False, is_public=True).order_by('-created_at')
    paginator = Paginator(announcements, 10)  # 1ページに10件表示
    page = request.GET.get('page')

    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)

    return render(request, 'ArchiveViewer/announcements_list.html', {'announcements': announcements})



# カテゴリー一覧を表示する
def category_list(request):
    categories = Category.objects.filter(is_active=True, parent=None)
    for category in categories:
        childrens = Category.objects.filter(parent=category, is_active=True)[:5]
        category.childrens = childrens
    return render(request, 'ArchiveViewer/category_list.html', {'categories': categories})
# カテゴリー詳細を表示する
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id, is_active=True)
    childrens = Category.objects.filter(parent=category, is_active=True)
    uploads = category.uploads.filter(published=True,delete_flag=False).order_by('-update_at')
    reports = category.reports.filter(is_public=True,is_deleted=False).order_by('-updated_at')
    print(category)
    print(uploads)
    print(reports)
    # パンくずリストの作成
    breadcrumbs = []
    current_category = category
    while current_category.parent:
        breadcrumbs.insert(0, current_category.parent)
        current_category = current_category.parent
    
    # ページネーション設定
    upload_paginator = Paginator(uploads, 10)  # アーカイブコンテンツを1ページに10件表示
    report_paginator = Paginator(reports, 10)  # 記事を1ページに10件表示
    
    upload_page_number = request.GET.get('uploads_page')
    report_page_number = request.GET.get('reports_page')
    
    try:
        paginated_uploads = upload_paginator.page(upload_page_number)
    except PageNotAnInteger:
        paginated_uploads = upload_paginator.page(1)
    except EmptyPage:
        paginated_uploads = upload_paginator.page(upload_paginator.num_pages)
    
    try:
        paginated_reports = report_paginator.page(report_page_number)
    except PageNotAnInteger:
        paginated_reports = report_paginator.page(1)
    except EmptyPage:
        paginated_reports = report_paginator.page(report_paginator.num_pages)
    
    context = {
        'category': category,
        'childrens': childrens,
        'uploads': paginated_uploads,
        'reports': paginated_reports,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'ArchiveViewer/category_detail.html', context)
