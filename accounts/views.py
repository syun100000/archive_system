from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from ArchiveViewer.models import *  # 具体的なモデルを必要に応じてインポートする
from accounts.models import User
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView 
from .forms import *
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest
from django.core.signing import SignatureExpired, BadSignature, loads, dumps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.conf import settings
from accounts.models import User
@login_required
@require_POST
# 記事のお気に入り削除
def report_favorite_delete(request):
    if request.method == 'POST':
        ReportFavorite.objects.filter(user_id=request.user.id, report_id=request.POST["report_id"]).delete()
    # リダイレクト先を、前のページにする
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@require_POST
# 記事のお気に入り追加
def report_favorite_add(request):
    if request.method == 'POST':
        report_id = request.POST["report_id"]
        report_instance = Report.objects.get(id=report_id)
        ReportFavorite.objects.create(user=request.user, report=report_instance)
    # リダイレクト先を、前のページにする
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@require_POST
# アーカイブコンテンツのお気に入り削除
def upload_favorites_delete(request):
    print(request.POST)
    if request.method == 'POST':
        UploadFavorite.objects.filter(user_id=request.user.id, upload_id=request.POST["upload_id"]).delete()
    # リダイレクト先を、前のページにする
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@require_POST
#　アーカイブコンテンツのお気に入り追加
def upload_favorite_add(request):
    if request.method == 'POST':
        file_id = request.POST["file_id"]
        upload_instance = Upload.objects.get(file_id=file_id)
        UploadFavorite.objects.create(user=request.user,upload=upload_instance)
    # リダイレクト先を、前のページにする
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
# マイページの表示
def mypage(request):
    #ログインしていない場合は、ログインページにリダイレクト
    if not request.user.is_authenticated:
        return render(request, "account_login")
    report_favorites = ReportFavorite.objects.filter(user=request.user)
    upload_favorites = UploadFavorite.objects.filter(user=request.user)
    upload_histories = UploadHistory.objects.filter(user=request.user).order_by('-created_at')
    report_histories = ReportHistory.objects.filter(user=request.user).order_by('-created_at')
    contents = {'report_favorites': report_favorites, 'upload_favorites': upload_favorites,
                'upload_histories': upload_histories, 'report_histories': report_histories}
    return render(request, "accounts/mypage.html", contents)

@login_required
@require_POST
# ユーザーの氏名を変更
def edit_name(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.save()
            if request.POST["first_name"] == "" or request.POST["last_name"] == "":
                code = 400
                return JsonResponse({"code": code})
            code = 200
        except:
            code = 400
        return JsonResponse({"code": code})
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@require_POST
# アカウントの削除
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        # スタッフか管理者の場合は削除不可
        if user.is_staff or user.is_superuser:
            return JsonResponse({"code": 400, "error": "スタッフまたは管理者のアカウントは削除できません。削除するには、管理者に連絡してください。"})
        user.delete()
        return JsonResponse({"code": 200})
    
    return JsonResponse({"code": 400})


# パスワード変更
class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'account/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'account/password_change_done.html'


# メールアドレス変更
class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'account/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(new_email),
            'user': user,
        }

        subject = render_to_string('account/email/email_change/subject.txt', context)
        message = render_to_string('account/email/email_change/message.txt', context)
        send_mail(subject, message, None, [new_email])

        return redirect('email_change_done')


class EmailChangeDone(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'account/email_change_done.html'


class EmailChangeComplete(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'account/email_change_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            # 新しいメールアドレスが存在しない場合は追加する
            email_address, created = EmailAddress.objects.get_or_create(
                email=new_email, 
                user=request.user, 
                defaults={'verified': True, 'primary': True}
            )
            if not created:
                email_address.set_as_primary()
            # 以前のメールアドレスを削除
            EmailAddress.objects.filter(user=request.user, email=request.user.email).exclude(email=new_email).delete()
            # usermodelのemailを更新
            User.objects.filter(pk=request.user.pk).update(email=new_email)
            
            return super().get(request, **kwargs)